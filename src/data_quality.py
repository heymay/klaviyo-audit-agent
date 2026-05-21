"""
Klaviyo Audit Katie — Data Quality Layer
Detects suspicious zeros and missing fields before scoring runs.
Returns DataGap objects that are surfaced as Low/Medium findings and
lower confidence on affected category scores.

A "suspicious zero" is a field that is 0 but where 0 is implausible
for any active Klaviyo account (e.g., 0 emailable profiles when total
profiles > 0, or 0 campaign open rate when campaigns were sent).
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
from .models import AccountData, Finding


@dataclass
class DataGap:
    field: str
    description: str
    affects_categories: List[str]
    severity: str = "Low"   # Low | Medium — gaps don't score as High/Critical


def detect_gaps(acct: AccountData) -> List[DataGap]:
    gaps: List[DataGap] = []
    p = acct.profiles
    c = acct.campaigns
    d = acct.deliverability
    r = acct.revenue

    # ── Profile data ──────────────────────────────────────────────────────
    if p.total_profiles > 0 and p.emailable_profiles == 0:
        gaps.append(DataGap(
            field="profiles.emailable_profiles",
            description="Emailable profile count is 0 while total profiles > 0 — likely not entered in manual_inputs.json.",
            affects_categories=["List Health & Engagement", "SMS Adoption", "Signup Forms & List Growth"],
        ))

    if p.total_profiles > 0 and p.engaged_90_day == 0 and p.emailable_profiles > 0:
        gaps.append(DataGap(
            field="profiles.engaged_*",
            description="All engagement counts (30/60/90/180 day) are 0 — enter these in manual_inputs.json from Klaviyo Analytics.",
            affects_categories=["List Health & Engagement", "Segmentation Quality"],
            severity="Medium",
        ))

    # ── Campaign metrics ───────────────────────────────────────────────────
    if c.total_sent > 0 and c.avg_open_rate == 0.0:
        gaps.append(DataGap(
            field="campaigns.avg_open_rate",
            description=f"{c.total_sent} campaigns sent but open rate is 0 — enter campaign metrics in manual_inputs.json.",
            affects_categories=["Campaign Strategy", "Deliverability Health"],
            severity="Medium",
        ))

    if c.total_sent > 0 and c.pct_to_engaged_segments == 0.0:
        gaps.append(DataGap(
            field="campaigns.pct_to_engaged_segments",
            description="% campaigns to engaged segments is 0 — enter this in manual_inputs.json (check campaign audience filters).",
            affects_categories=["Campaign Strategy", "Segmentation Quality"],
        ))

    # ── Deliverability ─────────────────────────────────────────────────────
    deliv_all_zero = (
        d.hard_bounce_rate == 0.0
        and d.spam_complaint_rate == 0.0
        and d.avg_unsubscribe_rate == 0.0
        and not d.has_spf and not d.has_dkim and not d.has_dmarc
    )
    if deliv_all_zero and c.total_sent > 0:
        gaps.append(DataGap(
            field="deliverability.*",
            description="All deliverability fields are at zero/false defaults — enter deliverability data in manual_inputs.json.",
            affects_categories=["Deliverability Health"],
            severity="Medium",
        ))

    # ── Revenue ────────────────────────────────────────────────────────────
    if r.revenue_attribution_configured and r.total_klaviyo_revenue == 0.0:
        live_flow_count = len(acct.live_flows)
        if live_flow_count > 0 or c.total_sent > 0:
            gaps.append(DataGap(
                field="revenue.total_klaviyo_revenue",
                description="Revenue attribution is marked configured but total Klaviyo revenue is $0 — enter revenue data in manual_inputs.json.",
                affects_categories=["Revenue Attribution"],
            ))

    # ── Flow metrics ───────────────────────────────────────────────────────
    live_with_zero_revenue = [f for f in acct.live_flows if f.revenue == 0.0]
    if len(live_with_zero_revenue) > 2:
        gaps.append(DataGap(
            field="flows[*].revenue",
            description=f"{len(live_with_zero_revenue)} live flows show $0 revenue — enter per-flow revenue in manual_inputs.json.",
            affects_categories=["Revenue Attribution", "Core Flow Coverage"],
        ))

    # ── Billing ────────────────────────────────────────────────────────────
    if acct.billing.plan_profile_limit == 0 and p.total_profiles > 0:
        gaps.append(DataGap(
            field="billing.plan_profile_limit",
            description="Billing plan profile limit is 0 — enter plan details in manual_inputs.json (Klaviyo Settings → Billing).",
            affects_categories=["Billing Efficiency"],
        ))

    return gaps


def gaps_to_findings(gaps: List[DataGap]) -> List[Finding]:
    """Convert DataGaps into Finding objects so they appear in the report."""
    findings = []
    for i, gap in enumerate(gaps):
        findings.append(Finding(
            rule_id=f"DQ-{i+1:03d}",
            severity=gap.severity,
            category="Data Quality",
            description=gap.description,
            business_impact=f"Affects scoring accuracy for: {', '.join(gap.affects_categories)}.",
            recommended_action="Complete the manual_inputs.json file with the missing data before finalizing this audit.",
            priority=gap.severity,
            score_impact="Scoring may be conservative due to missing data.",
            confidence="Data Unavailable",
        ))
    return findings


def confidence_for_category(category_name: str, gaps: List[DataGap]) -> str:
    """Return 'Partial' if any gap affects this category, else 'Confirmed'."""
    for gap in gaps:
        if category_name in gap.affects_categories:
            return "Partial"
    return "Confirmed"
