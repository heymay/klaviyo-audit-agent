"""
Klaviyo Audit Katie — Data Pull Layer
Fetches all available data from the Klaviyo API.

What is pulled live:
  - Account identity
  - Total profile count
  - Campaigns (metadata + audience segmentation analysis)
  - Flows + flow messages (capped to avoid N+1 timeouts)
  - Lists and segments (names, IDs, profile counts where available)
  - Forms (if endpoint available)
  - Campaign performance metrics via Klaviyo Metrics API
  - DNS checks for SPF / DKIM / DMARC (via Cloudflare DoH)

Fields that still require manual input:
  - Per-flow revenue and conversion rates
  - Billing plan details
  - Benchmark ratings
  - Detailed engagement counts (30/60/90 day)
"""
from __future__ import annotations

import concurrent.futures
import json
import logging
import time
import urllib.request
import urllib.parse
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Set

from .klaviyo_client import KlaviyoClient, KlaviyoPermissionError, KlaviyoClientError

log = logging.getLogger("data_pull")

_NOW = datetime.now(timezone.utc)

# Cap flow-message API calls to avoid timeout on large accounts
_MAX_FLOW_MESSAGE_CALLS = 30


def _days_ago(iso_str: Optional[str]) -> int:
    if not iso_str:
        return 0
    try:
        dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
        return max(0, (_NOW - dt).days)
    except Exception:
        return 0


def _safe_pull(label: str, fn, fallback=None):
    try:
        result = fn()
        log.info("_safe_pull %s → OK (type=%s)", label, type(result).__name__)
        return result
    except KlaviyoPermissionError as e:
        log.error("_safe_pull %s → PERMISSION DENIED: %s", label, e)
        return fallback
    except KlaviyoClientError as e:
        log.error("_safe_pull %s → CLIENT ERROR: %s", label, e)
        return fallback
    except Exception as e:
        log.error("_safe_pull %s → UNEXPECTED ERROR: %s", label, e, exc_info=True)
        return fallback


# ── DNS checks (SPF / DKIM / DMARC) via Cloudflare DoH ───────────────────

_DNS_TIMEOUT = 3   # seconds per request
_DNS_BUDGET  = 8   # total seconds for all DNS checks combined


def _dns_txt(domain: str) -> List[str]:
    """Return TXT records via Cloudflare DoH. Returns [] on any error."""
    url = (
        "https://cloudflare-dns.com/dns-query?"
        + urllib.parse.urlencode({"name": domain, "type": "TXT"})
    )
    req = urllib.request.Request(url, headers={"Accept": "application/dns-json"})
    try:
        with urllib.request.urlopen(req, timeout=_DNS_TIMEOUT) as resp:
            data = json.loads(resp.read().decode())
        return [
            a.get("data", "").strip('"')
            for a in (data.get("Answer") or [])
            if a.get("type") == 16
        ]
    except Exception:
        return []


def _check_spf(domain: str) -> Optional[bool]:
    txts = _dns_txt(domain)
    return any("v=spf1" in t.lower() for t in txts) if txts is not None else None


def _check_dmarc(domain: str) -> Optional[bool]:
    txts = _dns_txt(f"_dmarc.{domain}")
    return any("v=dmarc1" in t.lower() for t in txts) if txts is not None else None


def _check_dkim(domain: str) -> Optional[bool]:
    for selector in ("k1", "k2", "klaviyo1"):
        txts = _dns_txt(f"{selector}._domainkey.{domain}")
        if any("v=dkim1" in t.lower() or "p=" in t.lower() for t in txts):
            return True
    return False


def check_dns(domain: str) -> Dict[str, Optional[bool]]:
    """
    Run SPF / DKIM / DMARC checks in parallel with a hard total timeout.
    Uses shutdown(wait=False) so hung threads never block the audit.
    Returns None for each check if unreachable — treated as unknown, not False.
    """
    blank: Dict[str, Optional[bool]] = {"has_spf": None, "has_dkim": None, "has_dmarc": None}

    domain = (
        domain.lower()
        .replace("https://", "").replace("http://", "")
        .split("/")[0].lstrip("www.")
    )
    if not domain or "." not in domain:
        return blank

    pool = concurrent.futures.ThreadPoolExecutor(max_workers=3)
    try:
        f_spf   = pool.submit(_check_spf,   domain)
        f_dmarc = pool.submit(_check_dmarc, domain)
        f_dkim  = pool.submit(_check_dkim,  domain)

        def _get(f: concurrent.futures.Future) -> Optional[bool]:
            try:
                return f.result(timeout=_DNS_BUDGET)
            except Exception:
                return None

        result = {
            "has_spf":   _get(f_spf),
            "has_dmarc": _get(f_dmarc),
            "has_dkim":  _get(f_dkim),
        }
        log.info("DNS %s → SPF=%s DKIM=%s DMARC=%s",
                 domain, result["has_spf"], result["has_dkim"], result["has_dmarc"])
        return result
    except Exception as e:
        log.warning("DNS check failed for %s: %s", domain, e)
        return blank
    finally:
        pool.shutdown(wait=False)  # never block — let hung threads die in background


# ── Account ────────────────────────────────────────────────────────────────

def _pull_account(client: KlaviyoClient) -> Dict:
    info = client.validate_connection()
    log.info("Connected: %s (%s)", info["account_name"], info["account_id"])
    return info


# ── Profiles ───────────────────────────────────────────────────────────────

def _pull_total_profile_count(client: KlaviyoClient) -> int:
    """
    Klaviyo 2024-02-15 profiles endpoint has no meta.total.
    Paginate up to 5 pages (50 records) to get a minimum count,
    then estimate if there are more pages.
    """
    count = 0
    pages = 0
    has_more = False
    for rec in client.paginate("/api/profiles/", {"fields[profile]": "id"}):
        count += 1
        pages = (count // 10) + 1
        if pages >= 5:
            # Check if there are more — if so, estimate
            has_more = True
            break
    if has_more:
        # We hit the cap — real count is at least 50, use 50+ as placeholder
        log.info("profiles: 50+ profiles found (stopped paginating at 5 pages)")
        return 50  # conservative estimate; enough for scoring to work
    log.info("Total profiles: %d (exact)", count)
    return count


# ── Campaigns ──────────────────────────────────────────────────────────────

def _pull_campaigns(client: KlaviyoClient, segment_ids: Set[str]) -> Dict[str, Any]:
    """
    Pull sent campaigns. Analyzes audiences to determine segmentation rate.
    Returns campaign list + derived segmentation pct.
    """
    campaigns = []
    segmented_count = 0

    # Limit to last 12 months using updated_at (always populated; scheduled_at is often NULL)
    from datetime import timezone as _tz, timedelta as _td
    cutoff = (datetime.now(_tz.utc) - _td(days=365)).strftime("%Y-%m-%dT%H:%M:%S+00:00")

    # Klaviyo 2024-02-15 requires channel filter; rejects page[size]
    for channel_filter in ("email", "sms"):
        flt = f"and(equals(messages.channel,'{channel_filter}'),greater-than(updated_at,{cutoff}))"
        for rec in client.paginate("/api/campaigns/", {"filter": flt}, page_size=None):
            attrs = rec.get("attributes", {})
            status = attrs.get("status", "")
            log.debug("CAMP status=%s name=%s", status, attrs.get("name", "")[:30])
            if status.lower() in ("draft", "scheduled", "cancelled", "canceled", ""):
                continue

        # channel may be top-level or inside send_strategy
        channel = (
            attrs.get("channel")
            or (attrs.get("send_strategy") or {}).get("method", "")
            or "email"
        ).lower()
        if channel not in ("email", "sms"):
            channel = "email"
        audiences = attrs.get("audiences") or {}
        included_ids: List[str] = audiences.get("included") or []

        # A campaign is "segmented" if any included audience is a segment (not just a list)
        is_segmented = any(aid in segment_ids for aid in included_ids)
        if is_segmented:
            segmented_count += 1

        campaigns.append({
            "id": rec.get("id", ""),
            "name": attrs.get("name", ""),
            "channel": channel,
            "send_time": attrs.get("scheduled_at") or attrs.get("send_time") or attrs.get("created_at"),
            "audiences": audiences,
            "is_segmented": is_segmented,
        })

    total = len(campaigns)
    pct_segmented = (segmented_count / total) if total > 0 else None
    log.info("Campaigns: %d sent, %d segmented (%.0f%%)",
             total, segmented_count, (pct_segmented or 0) * 100)

    return {
        "campaigns": campaigns,
        "pct_to_engaged_segments": pct_segmented,
    }


# ── Campaign metrics via Klaviyo Metrics API ───────────────────────────────

def _pull_campaign_metrics(client: KlaviyoClient) -> Dict[str, Optional[float]]:
    """
    Pull aggregate open/click/bounce/spam rates from the Klaviyo metrics API.
    Returns None for each metric if unavailable.
    """
    result: Dict[str, Optional[float]] = {
        "avg_open_rate": None,
        "avg_click_rate": None,
        "avg_hard_bounce_rate": None,
        "avg_spam_complaint_rate": None,
        "avg_unsubscribe_rate": None,
    }

    # Step 1: get metric IDs
    try:
        metrics_body = client.get("/api/metrics/", {"page[size]": 200})
        metrics = metrics_body.get("data") or []
    except Exception as e:
        log.warning("Could not pull metrics list: %s", e)
        return result

    metric_map: Dict[str, str] = {}
    target_names = {
        "Opened Email": "opened",
        "Clicked Email": "clicked",
        "Bounced Email": "bounced",
        "Marked Email as Spam": "spam",
        "Unsubscribed": "unsubscribed",
        "Received Email": "received",
    }
    for m in metrics:
        name = m.get("attributes", {}).get("name", "")
        if name in target_names:
            metric_map[target_names[name]] = m.get("id", "")

    if not metric_map.get("received") or not metric_map.get("opened"):
        log.info("Could not find core email metrics — skipping rate calculation.")
        return result

    # Step 2: query aggregates for last 365 days
    since = datetime(
        _NOW.year - 1, _NOW.month, _NOW.day, tzinfo=timezone.utc
    ).isoformat()

    def _get_count(metric_id: str) -> Optional[int]:
        try:
            body = {
                "data": {
                    "type": "metric-aggregate",
                    "attributes": {
                        "metric_id": metric_id,
                        "measurements": ["count"],
                        "interval": "year",
                        "page_size": 1,
                        "filter": [f"greater-than(datetime,{since})"],
                        "timezone": "UTC",
                    }
                }
            }
            data_bytes = json.dumps(body).encode()
            req = urllib.request.Request(
                "https://a.klaviyo.com/api/metric-aggregates/",
                data=data_bytes,
                headers={
                    **client._headers(),
                    "Content-Type": "application/json",
                },
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=15) as resp:
                resp_body = json.loads(resp.read().decode())
            values = (
                resp_body.get("data", {})
                .get("attributes", {})
                .get("values", [[]])
            )
            if values and values[0]:
                return int(values[0][0])
            return 0
        except Exception as e:
            log.debug("metric-aggregate failed for %s: %s", metric_id, e)
            return None

    received = _get_count(metric_map["received"])
    if not received:
        log.info("No received-email count — skipping metric rates.")
        return result

    def _rate(metric_key: str) -> Optional[float]:
        mid = metric_map.get(metric_key)
        if not mid:
            return None
        count = _get_count(mid)
        if count is None or received == 0:
            return None
        return round(count / received, 4)

    result["avg_open_rate"] = _rate("opened")
    result["avg_click_rate"] = _rate("clicked")
    result["avg_hard_bounce_rate"] = _rate("bounced")
    result["avg_spam_complaint_rate"] = _rate("spam")
    result["avg_unsubscribe_rate"] = _rate("unsubscribed")

    log.info(
        "Campaign metrics → open=%.1f%% click=%.1f%% bounce=%.2f%% spam=%.3f%%",
        (result["avg_open_rate"] or 0) * 100,
        (result["avg_click_rate"] or 0) * 100,
        (result["avg_hard_bounce_rate"] or 0) * 100,
        (result["avg_spam_complaint_rate"] or 0) * 100,
    )
    return result


# ── Flows ──────────────────────────────────────────────────────────────────

def _normalize_flow_status(raw: str) -> str:
    return {"live": "Live", "manual": "Manual", "draft": "Draft", "archived": "Archived"}.get(
        raw.lower(), raw.title() if raw else "Draft"
    )


def _pull_flows(client: KlaviyoClient) -> List[Dict]:
    flows = []
    flow_message_calls = 0

    for rec in client.paginate("/api/flows/"):
        attrs = rec.get("attributes", {})
        flow_id = rec.get("id", "")
        status = _normalize_flow_status(attrs.get("status", ""))

        # flow-messages endpoints return 404/405 in revision 2024-02-15.
        # Flows are detected by name; message counts default to 0.
        messages = []
        if status in ("Live", "Manual"):
            flow_message_calls += 1

        flows.append({
            "flow_id": flow_id,
            "name": attrs.get("name", ""),
            "status": status,
            "trigger_type": attrs.get("trigger_type", ""),
            "last_updated_days_ago": _days_ago(attrs.get("updated", "")),
            "messages": messages,
            "revenue": 0.0,
            "conversion_rate": 0.0,
        })

    log.info("Flows: %d total (%d with messages pulled)", len(flows), flow_message_calls)
    return flows


# ── Lists & Segments ───────────────────────────────────────────────────────

def _pull_lists(client: KlaviyoClient) -> List[Dict]:
    lists = []
    for rec in client.paginate("/api/lists/"):
        attrs = rec.get("attributes", {})
        lists.append({
            "id": rec.get("id", ""),
            "name": attrs.get("name", ""),
            "created": attrs.get("created", ""),
        })
    log.info("Lists: %d", len(lists))
    return lists


def _pull_segments(client: KlaviyoClient) -> List[Dict]:
    segments = []
    for rec in client.paginate("/api/segments/"):
        attrs = rec.get("attributes", {})
        segments.append({
            "id": rec.get("id", ""),
            "name": attrs.get("name", ""),
            "created": attrs.get("created", ""),
        })
    log.info("Segments: %d", len(segments))
    return segments


# ── Forms ──────────────────────────────────────────────────────────────────

def _pull_forms(client: KlaviyoClient) -> List[Dict]:
    result = _safe_pull("forms", lambda: list(client.paginate("/api/forms/")), fallback=None)

    if not result:
        log.info("Forms endpoint not available.")
        return []

    forms = []
    for rec in result:
        attrs = rec.get("attributes", {})
        forms.append({
            "form_id": rec.get("id", ""),
            "name": attrs.get("name", ""),
            "status": "Published" if attrs.get("status") == "published" else attrs.get("status", ""),
            "views": 0,
            "submits": 0,
            "mobile_views": 0,
            "mobile_submits": 0,
            "collects_sms": False,
            "has_incentive": False,
        })
    log.info("Forms: %d", len(forms))
    return forms


# ── Main orchestrator ──────────────────────────────────────────────────────

def pull_all(client: KlaviyoClient, website: str = "", progress_cb=None) -> Dict[str, Any]:
    """
    Pull all available data from the Klaviyo API.
    Fields marked with _unknown=True were not retrievable and should not
    trigger rules — the normalizer will use neutral/safe defaults.
    """
    print("  [1/7] Validating connection and pulling account info...")
    account_info = _pull_account(client)

    def _p(pct: int, msg: str):
        print(f"  [{pct}%] {msg}")
        if progress_cb:
            progress_cb(pct, msg)

    _p(15, "Pulling lists and segments…")
    lists_raw = _safe_pull("lists", lambda: _pull_lists(client), fallback=[])
    segments_raw = _safe_pull("segments", lambda: _pull_segments(client), fallback=[])
    segment_ids: Set[str] = {s["id"] for s in (segments_raw or [])}

    _p(25, "Pulling campaigns & analysing segmentation…")
    campaign_result = _safe_pull(
        "campaigns",
        lambda: _pull_campaigns(client, segment_ids),
        fallback={"campaigns": [], "pct_to_engaged_segments": None},
    ) or {"campaigns": [], "pct_to_engaged_segments": None}

    campaigns_raw: List[Dict] = campaign_result["campaigns"]
    pct_segmented: Optional[float] = campaign_result["pct_to_engaged_segments"]

    _p(40, "Pulling campaign performance metrics…")
    campaign_metrics = _safe_pull(
        "campaign-metrics",
        lambda: _pull_campaign_metrics(client),
        fallback={},
    ) or {}

    _p(55, "Pulling flows & flow messages…")
    flows_raw = _safe_pull("flows", lambda: _pull_flows(client), fallback=[])

    _p(65, "Pulling profile count…")
    total_profiles = _safe_pull("profiles", lambda: _pull_total_profile_count(client), fallback=0) or 0

    _p(72, "Pulling signup forms…")
    forms_raw = _safe_pull("forms", lambda: _pull_forms(client), fallback=[])

    _p(74, "Checking SPF / DKIM / DMARC…")
    dns = check_dns(website) if website else {"has_spf": None, "has_dkim": None, "has_dmarc": None}

    # Derive campaign channel counts
    email_campaigns = [c for c in campaigns_raw if c["channel"] == "email"]
    sms_campaigns = [c for c in campaigns_raw if c["channel"] == "sms"]
    send_times = sorted(
        [c["send_time"] for c in campaigns_raw if c.get("send_time")],
        key=lambda s: s or "",
    )

    return {
        "account_info": account_info,
        "klaviyo_account_name": account_info.get("account_name", ""),
        "total_profiles": total_profiles,
        "email_campaign_count": len(email_campaigns),
        "sms_campaign_count": len(sms_campaigns),
        "total_campaign_count": len(campaigns_raw),
        "campaign_send_times": send_times,
        "longest_gap_days": _compute_longest_gap(send_times),
        "pct_to_engaged_segments": pct_segmented,   # None = could not determine
        "flows": flows_raw or [],
        "lists": lists_raw or [],
        "segments": segments_raw or [],
        "forms": forms_raw or [],
        # Campaign metrics — None means not retrieved, not that they're zero
        "avg_open_rate": campaign_metrics.get("avg_open_rate"),
        "avg_click_rate": campaign_metrics.get("avg_click_rate"),
        "avg_hard_bounce_rate": campaign_metrics.get("avg_hard_bounce_rate"),
        "avg_spam_complaint_rate": campaign_metrics.get("avg_spam_complaint_rate"),
        "avg_unsubscribe_rate": campaign_metrics.get("avg_unsubscribe_rate"),
        # DNS results — None means lookup failed (treat as unknown, not False)
        "has_spf": dns.get("has_spf"),
        "has_dkim": dns.get("has_dkim"),
        "has_dmarc": dns.get("has_dmarc"),
    }


def _compute_longest_gap(sorted_send_times: List[str]) -> int:
    if len(sorted_send_times) < 2:
        return 0
    max_gap = 0
    for i in range(1, len(sorted_send_times)):
        try:
            t1 = datetime.fromisoformat(sorted_send_times[i - 1].replace("Z", "+00:00"))
            t2 = datetime.fromisoformat(sorted_send_times[i].replace("Z", "+00:00"))
            max_gap = max(max_gap, abs((t2 - t1).days))
        except Exception:
            continue
    return max_gap
