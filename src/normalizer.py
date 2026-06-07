"""
Klaviyo Audit Katie — Normalizer
Maps raw data_pull output + manual_inputs.json → AccountData.

The normalizer is the bridge between the live API layer (Phase 3)
and the scoring/rules engine (Phase 2). AccountData produced here
is identical in structure to what the mock JSON files produce,
so all downstream scoring and reporting code runs unchanged.
"""
from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from .models import AccountData


_NOW = datetime.now(timezone.utc)
_WEEKS_IN_YEAR = 52


def normalize(raw: Dict[str, Any], manual: Dict[str, Any], context: Dict[str, Any]) -> AccountData:
    """
    Build an AccountData from:
      raw     — output of data_pull.pull_all()
      manual  — contents of manual_inputs.json (filled in by NP analyst)
      context — business context (business_name, website, audit_period, platform, etc.)
    """
    profiles = _build_profiles(raw, manual)
    campaigns = _build_campaigns(raw, manual)
    flows = _build_flows(raw, manual)
    forms = _build_forms(raw, manual)
    deliverability = _build_deliverability(raw, manual)
    revenue = _build_revenue(manual)
    billing = _build_billing(manual)
    segmentation = _build_segmentation(raw, manual)

    sms_enabled = _resolve_sms_enabled(raw, manual, flows, campaigns)

    return AccountData(
        business_name=context.get("business_name", ""),
        website=context.get("website", ""),
        klaviyo_account_name=raw.get("klaviyo_account_name", ""),
        audit_period_label=context.get("audit_period_label", "Last 12 months"),
        audit_period_days=context.get("audit_period_days", 365),
        ecommerce_platform=context.get("ecommerce_platform", "Shopify"),
        monthly_revenue_range=context.get("monthly_revenue_range", ""),
        sms_enabled=sms_enabled,
        ecommerce_events_configured=manual.get("revenue", {}).get("revenue_attribution_configured", True),
        profiles=profiles,
        flows=flows,
        campaigns=campaigns,
        forms=forms,
        deliverability=deliverability,
        revenue=revenue,
        billing=billing,
        segmentation=segmentation,
        list_count=len(raw.get("lists", [])),
        segment_count=len(raw.get("segments", [])),
    )


# ── profiles ───────────────────────────────────────────────────────────────

def _build_profiles(raw: Dict, manual: Dict):
    from .models import ProfileMetrics
    m = manual.get("profiles", {})
    return ProfileMetrics(
        total_profiles=raw.get("total_profiles", 0),
        emailable_profiles=m.get("emailable_profiles", raw.get("total_profiles", 0)),
        sms_consented_profiles=m.get("sms_consented_profiles", 0),
        suppressed_profiles=m.get("suppressed_profiles", 0),
        engaged_30_day=m.get("engaged_30_day", 0),
        engaged_60_day=m.get("engaged_60_day", 0),
        engaged_90_day=m.get("engaged_90_day", 0),
        engaged_180_day=m.get("engaged_180_day", 0),
    )


# ── campaigns ──────────────────────────────────────────────────────────────

def _build_campaigns(raw: Dict, manual: Dict):
    from .models import CampaignData
    m = manual.get("campaigns", {})

    # For rates: prefer live API data, then manual override.
    # If neither is available, use None so rules skip rather than fire on 0.
    def _rate(api_key: str, manual_key: str, fallback=None):
        api_val = raw.get(api_key)
        if api_val is not None:
            return api_val
        manual_val = m.get(manual_key)
        if manual_val is not None:
            return manual_val
        return fallback

    # pct_to_engaged_segments: use live analysis, else manual, else 0.5 (neutral)
    pct_seg = raw.get("pct_to_engaged_segments")
    if pct_seg is None:
        pct_seg = m.get("pct_to_engaged_segments")
    if pct_seg is None:
        pct_seg = 0.5   # unknown → neutral (won't trigger CAMP-003 or CAMP-004)

    return CampaignData(
        total_sent=raw.get("total_campaign_count", 0),
        email_campaigns=raw.get("email_campaign_count", 0),
        sms_campaigns=raw.get("sms_campaign_count", 0),
        avg_open_rate=_rate("avg_open_rate", "avg_open_rate", fallback=0.25),
        avg_click_rate=_rate("avg_click_rate", "avg_click_rate", fallback=0.02),
        avg_unsubscribe_rate=_rate("avg_unsubscribe_rate", "avg_unsubscribe_rate", fallback=0.001),
        avg_spam_complaint_rate=_rate("avg_spam_complaint_rate", "avg_spam_complaint_rate", fallback=0.0),
        avg_hard_bounce_rate=_rate("avg_hard_bounce_rate", "avg_hard_bounce_rate", fallback=0.0),
        pct_to_engaged_segments=pct_seg,
        total_revenue=manual.get("revenue", {}).get("campaign_revenue", 0.0),
        weeks_in_period=_WEEKS_IN_YEAR,
        longest_gap_days=raw.get("longest_gap_days", 0),
        open_rate_trend=m.get("open_rate_trend", "flat"),
    )


# ── flows ──────────────────────────────────────────────────────────────────

def _build_flows(raw: Dict, manual: Dict) -> list:
    from .models import FlowData, FlowMessage

    flow_overrides: Dict[str, Dict] = manual.get("flows", {})

    flows = []
    for f in raw.get("flows", []):
        name = f.get("name", "")

        # Match manual overrides by flow name (case-insensitive substring)
        override = _find_flow_override(name, flow_overrides)

        messages = []
        for i, msg in enumerate(f.get("messages", [])):
            # delay_minutes and has_discount can be overridden per message index
            msg_overrides = (override.get("messages") or [{}])
            msg_ov = msg_overrides[i] if i < len(msg_overrides) else {}
            messages.append(FlowMessage(
                channel=msg.get("channel", "email"),
                position=msg.get("position", i + 1),
                delay_minutes=msg_ov.get("delay_minutes", msg.get("delay_minutes", 0)),
                has_discount=msg_ov.get("has_discount", msg.get("has_discount", False)),
            ))

        flows.append(FlowData(
            flow_id=f.get("flow_id", ""),
            name=name,
            status=f.get("status", "Live"),
            trigger_type=f.get("trigger_type", ""),
            messages=messages,
            revenue=override.get("revenue", f.get("revenue", 0.0)),
            conversion_rate=override.get("conversion_rate", f.get("conversion_rate", 0.0)),
            last_updated_days_ago=f.get("last_updated_days_ago", 0),
        ))

    return flows


def _find_flow_override(name: str, overrides: Dict[str, Dict]) -> Dict:
    """Find a manual override entry whose key is a substring of the flow name (case-insensitive)."""
    name_lower = name.lower()
    for key, val in overrides.items():
        if key.lower() in name_lower:
            return val
    return {}


# ── forms ──────────────────────────────────────────────────────────────────

def _build_forms(raw: Dict, manual: Dict) -> list:
    from .models import FormData

    form_overrides: List[Dict] = manual.get("forms", [])
    forms = []

    raw_forms = raw.get("forms", [])
    # Merge API forms with manual overrides (matched by name)
    for i, f in enumerate(raw_forms):
        name = f.get("name", "")
        ov = _find_form_override(name, form_overrides)
        forms.append(FormData(
            form_id=f.get("form_id", ""),
            name=name,
            form_type=ov.get("form_type", f.get("form_type", "popup")),
            status=f.get("status", "Published"),
            views=ov.get("views", f.get("views", 0)),
            submits=ov.get("submits", f.get("submits", 0)),
            mobile_views=ov.get("mobile_views", f.get("mobile_views", 0)),
            mobile_submits=ov.get("mobile_submits", f.get("mobile_submits", 0)),
            collects_sms=ov.get("collects_sms", f.get("collects_sms", False)),
            has_incentive=ov.get("has_incentive", f.get("has_incentive", False)),
        ))

    # Any manual forms not matched to API forms (forms endpoint not available)
    api_names = {f.get("name", "").lower() for f in raw_forms}
    for ov in form_overrides:
        if ov.get("name", "").lower() not in api_names:
            forms.append(FormData(
                form_id=ov.get("form_id", ""),
                name=ov.get("name", "Manual Form"),
                form_type=ov.get("form_type", "popup"),
                status=ov.get("status", "Published"),
                views=ov.get("views", 0),
                submits=ov.get("submits", 0),
                mobile_views=ov.get("mobile_views", 0),
                mobile_submits=ov.get("mobile_submits", 0),
                collects_sms=ov.get("collects_sms", False),
                has_incentive=ov.get("has_incentive", False),
            ))

    return forms


def _find_form_override(name: str, overrides: List[Dict]) -> Dict:
    name_lower = name.lower()
    for ov in overrides:
        if ov.get("name", "").lower() in name_lower or name_lower in ov.get("name", "").lower():
            return ov
    return {}


# ── deliverability ─────────────────────────────────────────────────────────

def _build_deliverability(raw: Dict, manual: Dict):
    from .models import DeliverabilityData
    m = manual.get("deliverability", {})

    # DNS values: prefer live check (raw), then manual override, then True (benefit of doubt)
    def _dns(raw_key: str, manual_key: str) -> bool:
        raw_val = raw.get(raw_key)
        if raw_val is not None:
            return bool(raw_val)
        manual_val = m.get(manual_key)
        if manual_val is not None:
            return bool(manual_val)
        return True  # unknown → assume configured; real issues will surface elsewhere

    return DeliverabilityData(
        hard_bounce_rate=raw.get("avg_hard_bounce_rate") or m.get("hard_bounce_rate", 0.0),
        soft_bounce_rate=m.get("soft_bounce_rate", 0.0),
        spam_complaint_rate=raw.get("avg_spam_complaint_rate") or m.get("spam_complaint_rate", 0.0),
        avg_unsubscribe_rate=raw.get("avg_unsubscribe_rate") or m.get("avg_unsubscribe_rate", 0.0),
        has_spf=_dns("has_spf", "has_spf"),
        has_dkim=_dns("has_dkim", "has_dkim"),
        has_dmarc=_dns("has_dmarc", "has_dmarc"),
        has_branded_sending_domain=m.get("has_branded_sending_domain", False),
        open_rate_trend=m.get("open_rate_trend", "flat"),
    )


# ── revenue ────────────────────────────────────────────────────────────────

def _build_revenue(manual: Dict):
    from .models import RevenueData, BenchmarkData
    m = manual.get("revenue", {})
    b = manual.get("benchmarks", {})
    benchmarks = BenchmarkData(
        open_rate_rating=b.get("open_rate_rating", "average"),
        click_rate_rating=b.get("click_rate_rating", "average"),
        conversion_rate_rating=b.get("conversion_rate_rating", "average"),
        flow_revenue_rating=b.get("flow_revenue_rating", "average"),
        list_growth_rating=b.get("list_growth_rating", "average"),
    )
    return RevenueData(
        total_klaviyo_revenue=m.get("total_klaviyo_revenue", 0.0),
        campaign_revenue=m.get("campaign_revenue", 0.0),
        flow_revenue=m.get("flow_revenue", 0.0),
        revenue_attribution_configured=m.get("revenue_attribution_configured", True),
        benchmarks=benchmarks,
    )


# ── billing ────────────────────────────────────────────────────────────────

def _build_billing(manual: Dict):
    from .models import BillingData
    m = manual.get("billing", {})
    return BillingData(
        plan_tier=m.get("plan_tier", "Unknown"),
        plan_profile_limit=m.get("plan_profile_limit", 0),
    )


# ── segmentation ───────────────────────────────────────────────────────────

_ENGAGED_30_PATTERNS = ["engaged 30", "30 day", "30-day", "30d"]
_ENGAGED_90_PATTERNS = ["engaged 90", "90 day", "90-day", "90d"]
_VIP_PATTERNS = ["vip", "loyalty", "high value", "high-value", "top customer"]
_PURCHASER_PATTERNS = ["purchaser", "customer", "buyer", "ordered"]
_SUNSET_PATTERNS = ["sunset", "unengaged", "inactive", "lapsed", "hygiene"]


def _name_matches(name: str, patterns: List[str]) -> bool:
    name_lower = name.lower()
    return any(p in name_lower for p in patterns)


def _build_segmentation(raw: Dict, manual: Dict):
    from .models import SegmentationData

    seg_manual = manual.get("segmentation", {})
    segment_names = [s.get("name", "") for s in raw.get("segments", [])]
    list_names = [l.get("name", "") for l in raw.get("lists", [])]
    all_names = segment_names + list_names

    def detect(patterns: List[str], override_key: str) -> bool:
        if override_key in seg_manual:
            return bool(seg_manual[override_key])
        return any(_name_matches(n, patterns) for n in all_names)

    # Prefer live API segmentation data, then manual, then neutral 0.5
    pct = raw.get("pct_to_engaged_segments")
    if pct is None:
        pct = manual.get("campaigns", {}).get("pct_to_engaged_segments")
    if pct is None:
        pct = 0.5  # unknown → neutral, don't fire segmentation rules

    return SegmentationData(
        has_engaged_30_segment=detect(_ENGAGED_30_PATTERNS, "has_engaged_30_segment"),
        has_engaged_90_segment=detect(_ENGAGED_90_PATTERNS, "has_engaged_90_segment"),
        has_vip_segment=detect(_VIP_PATTERNS, "has_vip_segment"),
        has_purchaser_segment=detect(_PURCHASER_PATTERNS, "has_purchaser_segment"),
        has_sunset_segment=detect(_SUNSET_PATTERNS, "has_sunset_segment"),
        pct_campaigns_to_engaged=pct,
    )


# ── SMS detection ──────────────────────────────────────────────────────────

def _resolve_sms_enabled(raw: Dict, manual: Dict, flows: list, campaigns) -> bool:
    # Always infer from API data first — SMS campaigns are definitive proof
    has_sms_flow = any(f.sms_count > 0 for f in flows)
    has_sms_camp = campaigns.sms_campaigns > 0
    has_sms_profiles = manual.get("profiles", {}).get("sms_consented_profiles", 0) > 0

    if has_sms_flow or has_sms_camp or has_sms_profiles:
        return True  # API data confirms SMS — form toggle cannot override this

    # No API evidence of SMS — fall back to the form toggle
    ctx_sms = manual.get("account_context", {}).get("sms_enabled")
    if ctx_sms is not None:
        return bool(ctx_sms)

    return False
