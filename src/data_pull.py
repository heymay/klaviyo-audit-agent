"""
Klaviyo Audit Katie — Data Pull Layer
Fetches all required objects from the Klaviyo API and returns a raw dict
that the normalizer maps to AccountData.

What is pulled from the API (Phase 3):
  - Account identity
  - Total profile count (via profiles endpoint meta)
  - Campaigns (metadata: channel, send time, audience)
  - Flows (name, status, trigger type, updated timestamp)
  - Flow messages (channel, position — per flow)
  - Lists (names and IDs)
  - Segments (names and IDs)
  - Forms (name, status, views, submits — if endpoint available)

What requires manual input (see manual_inputs_template.json):
  - Profile engagement counts (30/60/90/180 day) — requires segment queries
  - Suppressed and SMS-consented profile counts
  - Campaign performance metrics (open/click/bounce/spam rates)
  - Deliverability data (SPF/DKIM/DMARC, bounce rates)
  - Flow revenue and conversion rates
  - Revenue attribution totals
  - Billing plan details
  - Benchmark ratings
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from .klaviyo_client import KlaviyoClient, KlaviyoPermissionError, KlaviyoClientError

log = logging.getLogger("data_pull")

_NOW = datetime.now(timezone.utc)


def _days_ago(iso_str: Optional[str]) -> int:
    """Convert an ISO 8601 timestamp string to days-ago integer."""
    if not iso_str:
        return 0
    try:
        dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
        return max(0, (_NOW - dt).days)
    except Exception:
        return 0


def _safe_pull(label: str, fn) -> Any:
    """Run a pull function; on permission/client error, log and return the fallback."""
    try:
        return fn()
    except KlaviyoPermissionError:
        log.warning("Skipping %s — API key lacks permission for this endpoint.", label)
        return None
    except KlaviyoClientError as e:
        log.warning("Skipping %s — API error: %s", label, e)
        return None


# ── individual pull functions ──────────────────────────────────────────────

def _pull_account(client: KlaviyoClient) -> Dict:
    info = client.validate_connection()
    log.info("Connected to account: %s (id: %s)", info["account_name"], info["account_id"])
    return info


def _pull_total_profile_count(client: KlaviyoClient) -> int:
    """
    Fetches total profile count from metadata without pulling individual records.
    Uses page[size]=1 to minimize data transfer.
    """
    body = client.get("/api/profiles/", {"page[size]": 1})
    total = (body.get("meta") or {}).get("total", 0)
    if not total:
        # Fallback: count via pagination (slower but more reliable)
        log.info("meta.total not available — counting profiles via pagination")
        total = sum(1 for _ in client.paginate("/api/profiles/", {"fields[profile]": "id"}))
    log.info("Total profiles: %d", total)
    return total


def _pull_campaigns(client: KlaviyoClient) -> List[Dict]:
    """
    Pull all campaigns. Filters to email and sms channels only.
    Returns list of raw campaign attribute dicts with derived fields.
    """
    campaigns = []
    for rec in client.paginate("/api/campaigns/", {
        "fields[campaign]": "name,status,send_time,created_at,audiences",
    }):
        attrs = rec.get("attributes", {})
        status = attrs.get("status", "")
        # Only count sent campaigns for audit metrics
        if status not in ("Sent", "sent"):
            continue

        # Determine channel from campaign-messages relationship or archived type
        # Klaviyo campaigns have a 'channel' field in some API versions;
        # fall back to checking name/type hints
        channel = attrs.get("channel", "email")
        campaigns.append({
            "id": rec.get("id", ""),
            "name": attrs.get("name", ""),
            "channel": channel,
            "send_time": attrs.get("send_time") or attrs.get("created_at"),
            "audiences": attrs.get("audiences", {}),
        })

    log.info("Campaigns pulled: %d sent", len(campaigns))
    return campaigns


def _pull_flows(client: KlaviyoClient) -> List[Dict]:
    """
    Pull all flows with their messages.
    Returns list of flow dicts including messages sub-list.
    """
    flows = []
    for rec in client.paginate("/api/flows/", {
        "fields[flow]": "name,status,trigger_type,updated",
    }):
        attrs = rec.get("attributes", {})
        flow_id = rec.get("id", "")

        # Pull messages for this flow
        messages = _safe_pull(
            f"flow-messages/{flow_id}",
            lambda fid=flow_id: list(client.paginate(
                f"/api/flows/{fid}/flow-messages/",
                {"fields[flow-message]": "channel,position,action_type"},
            )),
        ) or []

        parsed_messages = []
        for msg in messages:
            mattrs = msg.get("attributes", {})
            parsed_messages.append({
                "channel": mattrs.get("channel", "email"),
                "position": mattrs.get("position", 1),
                "delay_minutes": 0,      # requires deep action parsing — manual input
                "has_discount": False,    # requires content analysis — manual input
            })

        updated_iso = attrs.get("updated", "")
        flows.append({
            "flow_id": flow_id,
            "name": attrs.get("name", ""),
            "status": _normalize_flow_status(attrs.get("status", "")),
            "trigger_type": attrs.get("trigger_type", ""),
            "last_updated_days_ago": _days_ago(updated_iso),
            "messages": parsed_messages,
            "revenue": 0.0,           # manual input
            "conversion_rate": 0.0,   # manual input
        })

    log.info("Flows pulled: %d", len(flows))
    return flows


def _normalize_flow_status(raw: str) -> str:
    mapping = {
        "live": "Live", "manual": "Manual",
        "draft": "Draft", "archived": "Archived",
    }
    return mapping.get(raw.lower(), raw.title() if raw else "Draft")


def _pull_lists(client: KlaviyoClient) -> List[Dict]:
    lists = []
    for rec in client.paginate("/api/lists/", {"fields[list]": "name,created"}):
        attrs = rec.get("attributes", {})
        lists.append({
            "id": rec.get("id", ""),
            "name": attrs.get("name", ""),
            "created": attrs.get("created", ""),
        })
    log.info("Lists pulled: %d", len(lists))
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
    log.info("Segments pulled: %d", len(segments))
    return segments


def _pull_forms(client: KlaviyoClient) -> List[Dict]:
    """
    Pull signup forms. Returns empty list if the endpoint is unavailable
    (forms API is not available on all Klaviyo plans).
    """
    forms = []
    result = _safe_pull("forms", lambda: list(client.paginate(
        "/api/forms/",
        {"fields[form]": "name,status,ab_test"},
    )))
    if not result:
        log.info("Forms endpoint not available or returned no data.")
        return []

    for rec in result:
        attrs = rec.get("attributes", {})
        forms.append({
            "form_id": rec.get("id", ""),
            "name": attrs.get("name", ""),
            "status": "Published" if attrs.get("status") == "published" else attrs.get("status", ""),
            # Views/submits/mobile stats require form analytics endpoint — manual input
            "views": 0,
            "submits": 0,
            "mobile_views": 0,
            "mobile_submits": 0,
            "collects_sms": False,   # requires form content inspection — manual input
            "has_incentive": False,  # requires form content inspection — manual input
        })
    log.info("Forms pulled: %d", len(forms))
    return forms


# ── main pull orchestrator ─────────────────────────────────────────────────

def pull_all(client: KlaviyoClient) -> Dict[str, Any]:
    """
    Pull all available data from the Klaviyo API.
    Returns a raw dict that normalizer.py maps to AccountData.

    Fields marked 'MANUAL' in the returned dict must be filled in
    via manual_inputs.json before running the audit.
    """
    print("  [1/6] Validating connection and pulling account info...")
    account_info = _pull_account(client)

    print("  [2/6] Pulling total profile count...")
    total_profiles = _safe_pull("profiles", lambda: _pull_total_profile_count(client)) or 0

    print("  [3/6] Pulling campaigns...")
    campaigns_raw = _safe_pull("campaigns", lambda: _pull_campaigns(client)) or []

    print("  [4/6] Pulling flows and flow messages...")
    flows_raw = _safe_pull("flows", lambda: _pull_flows(client)) or []

    print("  [5/6] Pulling lists and segments...")
    lists_raw = _safe_pull("lists", lambda: _pull_lists(client)) or []
    segments_raw = _safe_pull("segments", lambda: _pull_segments(client)) or []

    print("  [6/6] Pulling forms...")
    forms_raw = _safe_pull("forms", lambda: _pull_forms(client)) or []

    # Derive campaign summary metrics from raw campaign list
    email_campaigns = [c for c in campaigns_raw if c["channel"] == "email"]
    sms_campaigns = [c for c in campaigns_raw if c["channel"] == "sms"]

    send_times = sorted(
        [c["send_time"] for c in campaigns_raw if c.get("send_time")],
        key=lambda s: s or "",
    )
    longest_gap_days = _compute_longest_gap(send_times)

    return {
        "account_info": account_info,
        "klaviyo_account_name": account_info.get("account_name", ""),
        "total_profiles": total_profiles,
        "email_campaign_count": len(email_campaigns),
        "sms_campaign_count": len(sms_campaigns),
        "total_campaign_count": len(campaigns_raw),
        "campaign_send_times": send_times,
        "longest_gap_days": longest_gap_days,
        "flows": flows_raw,
        "lists": lists_raw,
        "segments": segments_raw,
        "forms": forms_raw,
        # All fields below require manual_inputs.json
        "_manual_required": [
            "profiles.sms_consented_profiles",
            "profiles.suppressed_profiles",
            "profiles.engaged_30_day",
            "profiles.engaged_60_day",
            "profiles.engaged_90_day",
            "profiles.engaged_180_day",
            "campaigns.avg_open_rate",
            "campaigns.avg_click_rate",
            "campaigns.avg_unsubscribe_rate",
            "campaigns.avg_spam_complaint_rate",
            "campaigns.avg_hard_bounce_rate",
            "campaigns.pct_to_engaged_segments",
            "campaigns.open_rate_trend",
            "deliverability.*",
            "flows[*].revenue",
            "flows[*].conversion_rate",
            "flows[*].delay_minutes (per message)",
            "flows[*].has_discount (per message)",
            "revenue.*",
            "billing.*",
            "benchmarks.*",
        ],
    }


def _compute_longest_gap(sorted_send_times: List[str]) -> int:
    """Return the longest gap in days between consecutive campaign sends."""
    if len(sorted_send_times) < 2:
        return 0
    max_gap = 0
    for i in range(1, len(sorted_send_times)):
        try:
            t1 = datetime.fromisoformat(sorted_send_times[i - 1].replace("Z", "+00:00"))
            t2 = datetime.fromisoformat(sorted_send_times[i].replace("Z", "+00:00"))
            gap = abs((t2 - t1).days)
            max_gap = max(max_gap, gap)
        except Exception:
            continue
    return max_gap
