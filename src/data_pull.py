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
        return fn()
    except KlaviyoPermissionError:
        log.warning("Skipping %s — API key lacks permission.", label)
        return fallback
    except KlaviyoClientError as e:
        log.warning("Skipping %s — %s", label, e)
        return fallback
    except Exception as e:
        log.warning("Skipping %s — unexpected error: %s", label, e)
        return fallback


# ── DNS checks (SPF / DKIM / DMARC) via Cloudflare DoH ───────────────────

def _dns_txt(domain: str, timeout: int = 6) -> List[str]:
    """Return TXT records for domain using Cloudflare DNS-over-HTTPS."""
    url = f"https://cloudflare-dns.com/dns-query?name={urllib.parse.quote(domain)}&type=TXT"
    req = urllib.request.Request(
        url,
        headers={"Accept": "application/dns-json"},
        method="GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode())
        answers = data.get("Answer") or []
        return [a.get("data", "").strip('"') for a in answers if a.get("type") == 16]
    except Exception as e:
        log.debug("DNS TXT lookup failed for %s: %s", domain, e)
        return []


def check_dns(domain: str) -> Dict[str, Optional[bool]]:
    """
    Check SPF, DKIM (k1._domainkey), and DMARC for the given domain.
    Returns None for each if the lookup fails (unknown, not False).
    """
    result: Dict[str, Optional[bool]] = {
        "has_spf": None,
        "has_dkim": None,
        "has_dmarc": None,
    }

    # Strip protocol/path — just the apex domain
    domain = domain.lower().replace("https://", "").replace("http://", "").split("/")[0].lstrip("www.")
    if not domain or "." not in domain:
        return result

    try:
        # SPF — TXT record on apex domain containing "v=spf1"
        apex_txts = _dns_txt(domain)
        result["has_spf"] = any("v=spf1" in t.lower() for t in apex_txts)

        # DMARC — TXT record on _dmarc.{domain}
        dmarc_txts = _dns_txt(f"_dmarc.{domain}")
        result["has_dmarc"] = any("v=dmarc1" in t.lower() for t in dmarc_txts)

        # DKIM — check common Klaviyo selectors (k1, k2, klaviyo1)
        dkim_found = False
        for selector in ("k1", "k2", "klaviyo1"):
            records = _dns_txt(f"{selector}._domainkey.{domain}")
            if any("v=dkim1" in t.lower() or "p=" in t.lower() for t in records):
                dkim_found = True
                break
        result["has_dkim"] = dkim_found

        log.info("DNS checks for %s → SPF=%s DKIM=%s DMARC=%s",
                 domain, result["has_spf"], result["has_dkim"], result["has_dmarc"])
    except Exception as e:
        log.warning("DNS check failed for %s: %s", domain, e)

    return result


# ── Account ────────────────────────────────────────────────────────────────

def _pull_account(client: KlaviyoClient) -> Dict:
    info = client.validate_connection()
    log.info("Connected: %s (%s)", info["account_name"], info["account_id"])
    return info


# ── Profiles ───────────────────────────────────────────────────────────────

def _pull_total_profile_count(client: KlaviyoClient) -> int:
    body = client.get("/api/profiles/", {"page[size]": 1})
    total = (body.get("meta") or {}).get("total", 0)
    if not total:
        log.info("meta.total unavailable — counting profiles via pagination (may be slow)")
        total = sum(1 for _ in client.paginate("/api/profiles/", {"fields[profile]": "id"}))
    log.info("Total profiles: %d", total)
    return total


# ── Campaigns ──────────────────────────────────────────────────────────────

def _pull_campaigns(client: KlaviyoClient, segment_ids: Set[str]) -> Dict[str, Any]:
    """
    Pull sent campaigns. Analyzes audiences to determine segmentation rate.
    Returns campaign list + derived segmentation pct.
    """
    campaigns = []
    segmented_count = 0

    for rec in client.paginate("/api/campaigns/", {
        "fields[campaign]": "name,status,send_time,created_at,audiences,channel",
    }):
        attrs = rec.get("attributes", {})
        status = attrs.get("status", "")
        if status.lower() not in ("sent",):
            continue

        channel = attrs.get("channel", "email").lower()
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
            "send_time": attrs.get("send_time") or attrs.get("created_at"),
            "audiences": audiences,
            "is_segmented": is_segmented,
        })

    total = len(campaigns)
    pct_segmented = (segmented_count / total) if total > 0 else None  # None = unknown
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

    for rec in client.paginate("/api/flows/", {
        "fields[flow]": "name,status,trigger_type,updated",
    }):
        attrs = rec.get("attributes", {})
        flow_id = rec.get("id", "")
        status = _normalize_flow_status(attrs.get("status", ""))

        # Only pull messages for Live flows, and cap total calls
        messages = []
        if status == "Live" and flow_message_calls < _MAX_FLOW_MESSAGE_CALLS:
            msgs = _safe_pull(
                f"flow-messages/{flow_id}",
                lambda fid=flow_id: list(client.paginate(
                    f"/api/flows/{fid}/flow-messages/",
                    {"fields[flow-message]": "channel,position,action_type"},
                )),
                fallback=[],
            )
            flow_message_calls += 1
            for msg in (msgs or []):
                mattrs = msg.get("attributes", {})
                messages.append({
                    "channel": mattrs.get("channel", "email"),
                    "position": mattrs.get("position", 1),
                    "delay_minutes": 0,
                    "has_discount": False,
                })

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
    for rec in client.paginate("/api/lists/", {"fields[list]": "name,created"}):
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
    for rec in client.paginate("/api/segments/", {"fields[segment]": "name,created"}):
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
    result = _safe_pull("forms", lambda: list(client.paginate(
        "/api/forms/",
        {"fields[form]": "name,status,ab_test"},
    )), fallback=None)

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

def pull_all(client: KlaviyoClient, website: str = "") -> Dict[str, Any]:
    """
    Pull all available data from the Klaviyo API.
    Fields marked with _unknown=True were not retrievable and should not
    trigger rules — the normalizer will use neutral/safe defaults.
    """
    print("  [1/7] Validating connection and pulling account info...")
    account_info = _pull_account(client)

    print("  [2/7] Pulling lists and segments...")
    lists_raw = _safe_pull("lists", lambda: _pull_lists(client), fallback=[])
    segments_raw = _safe_pull("segments", lambda: _pull_segments(client), fallback=[])
    segment_ids: Set[str] = {s["id"] for s in (segments_raw or [])}

    print("  [3/7] Pulling campaigns and analysing segmentation...")
    campaign_result = _safe_pull(
        "campaigns",
        lambda: _pull_campaigns(client, segment_ids),
        fallback={"campaigns": [], "pct_to_engaged_segments": None},
    ) or {"campaigns": [], "pct_to_engaged_segments": None}

    campaigns_raw: List[Dict] = campaign_result["campaigns"]
    pct_segmented: Optional[float] = campaign_result["pct_to_engaged_segments"]

    print("  [4/7] Pulling campaign performance metrics...")
    campaign_metrics = _safe_pull(
        "campaign-metrics",
        lambda: _pull_campaign_metrics(client),
        fallback={},
    ) or {}

    print("  [5/7] Pulling flows and flow messages...")
    flows_raw = _safe_pull("flows", lambda: _pull_flows(client), fallback=[])

    print("  [6/7] Pulling profile count...")
    total_profiles = _safe_pull("profiles", lambda: _pull_total_profile_count(client), fallback=0) or 0

    print("  [7/7] Pulling forms and checking DNS records...")
    forms_raw = _safe_pull("forms", lambda: _pull_forms(client), fallback=[])
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
