"""
Klaviyo Audit Katie — Scoring Engine
Implements all 10 weighted categories from scoring-rubric.md.
Composite score = Σ (category_score / 10 × weight × 100), rounded to int.
"""
from __future__ import annotations
from typing import List, Tuple
from .models import AccountData, CategoryScore


# ── weights ────────────────────────────────────────────────────────────────
WEIGHTS = {
    "Deliverability Health":         0.15,
    "Core Flow Coverage":            0.15,
    "Flow Configuration Quality":    0.15,
    "Campaign Strategy":             0.12,
    "SMS Adoption":                  0.10,
    "Signup Forms & List Growth":    0.10,
    "List Health & Engagement":      0.10,
    "Segmentation Quality":          0.06,
    "Revenue Attribution":           0.05,
    "Billing Efficiency":            0.02,
}

SCORE_BANDS = [
    (90, "Elite"),
    (75, "Strong"),
    (60, "Average"),
    (40, "Weak"),
    (0,  "Critical"),
]


def score_band(composite: int) -> str:
    for threshold, band in SCORE_BANDS:
        if composite >= threshold:
            return band
    return "Critical"


# ── individual scorers ─────────────────────────────────────────────────────

def _score_deliverability(acct: AccountData) -> CategoryScore:
    d = acct.deliverability
    penalties: List[str] = []
    bonuses: List[str] = []
    score = 10

    # Bounce/spam/unsub rates require Klaviyo metrics API — unavailable.
    # Only score these if we have real non-zero values (not API fallback zeros).
    if d.hard_bounce_rate >= 0.02:
        score = min(score, 2)
        penalties.append(f"Hard bounce rate {d.hard_bounce_rate:.1%} ≥ 2% (Critical cap: 2)")
    elif d.hard_bounce_rate >= 0.01:
        score -= 3
        penalties.append(f"Hard bounce rate {d.hard_bounce_rate:.1%} ≥ 1%")
    elif d.hard_bounce_rate >= 0.005:
        score -= 1
        penalties.append(f"Hard bounce rate {d.hard_bounce_rate:.1%} ≥ 0.5%")

    if d.spam_complaint_rate >= 0.001:
        score = min(score, 2)
        penalties.append(f"Spam complaint rate {d.spam_complaint_rate:.3%} ≥ 0.1% (Critical cap: 2)")
    elif d.spam_complaint_rate >= 0.0008:
        score -= 3
        penalties.append(f"Spam complaint rate {d.spam_complaint_rate:.3%} ≥ 0.08%")

    if d.avg_unsubscribe_rate >= 0.005:
        score -= 2
        penalties.append(f"Unsubscribe rate {d.avg_unsubscribe_rate:.2%} ≥ 0.5%")

    # DNS authentication — SPF and DMARC confirmed via live DNS lookup
    if not d.has_spf:
        score -= 1
        penalties.append("Missing SPF record")
    else:
        bonuses.append("SPF configured ✓")

    if not d.has_dmarc:
        score -= 1
        penalties.append("Missing DMARC policy")
    else:
        bonuses.append("DMARC configured ✓")

    # DKIM and Branded Domain: not reliably detectable via DNS in current setup
    # — do not penalise for these

    score = max(1, min(10, score))

    # Build justification with only confirmed data
    dns_parts = []
    if d.has_spf:
        dns_parts.append("SPF ✓")
    if d.has_dmarc:
        dns_parts.append("DMARC ✓")

    rate_parts = []
    if d.hard_bounce_rate > 0:
        rate_parts.append(f"Bounce: {d.hard_bounce_rate:.2%}")
    if d.spam_complaint_rate > 0:
        rate_parts.append(f"Spam: {d.spam_complaint_rate:.3%}")
    if d.avg_unsubscribe_rate > 0:
        rate_parts.append(f"Unsub: {d.avg_unsubscribe_rate:.2%}")

    justification_parts = rate_parts + dns_parts
    if not rate_parts:
        justification_parts = ["Bounce/spam/unsub data unavailable via API"] + dns_parts

    justification = " | ".join(justification_parts)

    return CategoryScore(
        name="Deliverability Health",
        score=score,
        weight=WEIGHTS["Deliverability Health"],
        justification=justification,
        penalties_applied=penalties,
        bonuses_applied=bonuses,
    )


def _score_core_flow_coverage(acct: AccountData) -> CategoryScore:
    CORE_FLOWS = ["welcome", "abandoned_cart", "added_to_cart", "browse_abandonment",
                  "post_purchase", "winback"]
    penalties: List[str] = []
    bonuses: List[str] = []

    present = {ft for ft in CORE_FLOWS if acct.get_flow(ft) is not None}
    missing = set(CORE_FLOWS) - present
    count = len(present)

    # Hard caps for missing critical flows
    if "welcome" in missing and "abandoned_cart" in missing:
        score = 2
        penalties.append("Missing both Welcome and Abandoned Cart flows (cap: 2)")
    elif "abandoned_cart" in missing:
        score = min(4, count + 1)
        penalties.append("Missing Abandoned Cart flow (cap: 4)")
    elif "welcome" in missing:
        score = min(4, count + 1)
        penalties.append("Missing Welcome flow (cap: 4)")
    else:
        # 6 core flows → scale 5–10 based on count
        score_map = {6: 10, 5: 8, 4: 6, 3: 5, 2: 4, 1: 3, 0: 1}
        score = score_map.get(count, 1)

    for ft in missing:
        penalties.append(f"Missing {ft.replace('_', ' ').title()} flow")

    # VIP bonus
    if acct.get_flow("vip"):
        score = min(10, score + 1)
        bonuses.append("VIP / Loyalty flow present")

    score = max(1, min(10, score))

    justification = (
        f"{count}/6 core flows live: {', '.join(sorted(present)) or 'none'}. "
        f"Missing: {', '.join(sorted(missing)) or 'none'}."
    )
    return CategoryScore(
        name="Core Flow Coverage",
        score=score,
        weight=WEIGHTS["Core Flow Coverage"],
        justification=justification,
        penalties_applied=penalties,
        bonuses_applied=bonuses,
    )


def _score_flow_configuration(acct: AccountData) -> CategoryScore:
    penalties: List[str] = []
    bonuses: List[str] = []
    score = 7  # start optimistic; deduct for gaps

    live_flows = acct.live_flows
    if not live_flows:
        return CategoryScore(
            name="Flow Configuration Quality",
            score=1,
            weight=WEIGHTS["Flow Configuration Quality"],
            justification="No live flows to evaluate.",
            penalties_applied=["No live flows exist"],
            bonuses_applied=[],
        )

    # NOTE: flow message counts (email_count, sms_count) are unavailable in
    # Klaviyo API 2024-02-15 — flow-messages endpoints return 404/405.
    # Only evaluate timing, stale status, and presence — not message counts.
    has_message_data = any(len(f.messages) > 0 for f in live_flows)

    welcome = acct.get_flow("welcome")
    if welcome and has_message_data:
        if welcome.first_message_delay_minutes > 60:
            score -= 2
            penalties.append(
                f"Welcome first email delayed {welcome.first_message_delay_minutes}min (>60min threshold)"
            )

    ac = acct.get_flow("abandoned_cart")
    if ac and has_message_data:
        if not ac.has_incentive:
            score -= 1
            penalties.append("Abandoned cart flow has no discount/incentive")
        else:
            bonuses.append("Abandoned cart includes an incentive")

    if not has_message_data:
        bonuses.append(f"{len(live_flows)} live flows detected (message detail unavailable via API)")

    # Stale flows — only penalise if clearly neglected (>365 days, not 180)
    stale = [f for f in live_flows if f.last_updated_days_ago > 365]
    if stale:
        score -= 1
        penalties.append(f"{len(stale)} live flow(s) not updated in >1 year")

    score = max(1, min(10, score))
    stale_label = f"{len(stale)} stale (>1yr)" if stale else "no stale flows"
    justification = f"{len(live_flows)} live flows | {len(acct.flows)} total | {stale_label} | message detail unavailable via API"
    return CategoryScore(
        name="Flow Configuration Quality",
        score=score,
        weight=WEIGHTS["Flow Configuration Quality"],
        justification=justification,
        penalties_applied=penalties,
        bonuses_applied=bonuses,
    )


def _score_campaign_strategy(acct: AccountData) -> CategoryScore:
    c = acct.campaigns
    penalties: List[str] = []
    bonuses: List[str] = []
    score = 7

    # Send frequency
    if c.campaigns_per_week < 0.5:
        score -= 3
        penalties.append(f"Campaigns per week {c.campaigns_per_week:.1f} < 0.5 (very infrequent)")
    elif c.campaigns_per_week < 1.0:
        score -= 1
        penalties.append(f"Campaigns per week {c.campaigns_per_week:.1f} < 1.0 (low)")
    elif c.campaigns_per_week > 7:
        score -= 2
        penalties.append(f"Campaigns per week {c.campaigns_per_week:.1f} > 7 (potential fatigue)")

    # Segmentation
    if c.pct_to_engaged_segments < 0.25:
        score -= 2
        penalties.append(f"Only {c.pct_to_engaged_segments:.0%} of campaigns sent to engaged segments")
    elif c.pct_to_engaged_segments >= 0.75:
        bonuses.append(f"{c.pct_to_engaged_segments:.0%} of campaigns use engaged segments")

    # Open rate
    if c.avg_open_rate < 0.15:
        score -= 2
        penalties.append(f"Average open rate {c.avg_open_rate:.1%} < 15% (poor)")
    elif c.avg_open_rate >= 0.35:
        bonuses.append(f"Strong open rate {c.avg_open_rate:.1%}")

    # Spam complaint
    if c.avg_spam_complaint_rate >= 0.001:
        score -= 2
        penalties.append(f"Campaign spam complaint rate {c.avg_spam_complaint_rate:.3%} ≥ 0.1%")

    # Hard bounce
    if c.avg_hard_bounce_rate >= 0.01:
        score -= 1
        penalties.append(f"Campaign hard bounce rate {c.avg_hard_bounce_rate:.2%} ≥ 1%")

    # Open rate trend
    if c.open_rate_trend == "improving":
        bonuses.append("Campaign open rate trend improving")
    elif c.open_rate_trend == "declining":
        score -= 1
        penalties.append("Campaign open rate trend declining")

    # Long send gap
    if c.longest_gap_days > 30:
        score -= 1
        penalties.append(f"Longest campaign gap was {c.longest_gap_days} days (>30)")

    score = max(1, min(10, score))
    # Only show confirmed real data — open/click/spam rates unavailable via API
    justification = (
        f"{c.campaigns_per_week:.1f} campaigns/wk | "
        f"Email: {c.email_campaigns} | SMS: {c.sms_campaigns} | "
        f"Engaged-segment rate: {c.pct_to_engaged_segments:.0%}"
    )
    return CategoryScore(
        name="Campaign Strategy",
        score=score,
        weight=WEIGHTS["Campaign Strategy"],
        justification=justification,
        penalties_applied=penalties,
        bonuses_applied=bonuses,
    )


def _score_sms_adoption(acct: AccountData) -> CategoryScore:
    penalties: List[str] = []
    bonuses: List[str] = []

    if not acct.sms_enabled:
        return CategoryScore(
            name="SMS Adoption",
            score=2,
            weight=WEIGHTS["SMS Adoption"],
            justification="SMS not enabled in this Klaviyo account.",
            penalties_applied=["SMS not enabled (-8 points from max)"],
            bonuses_applied=[],
        )

    score = 6  # baseline for SMS enabled
    p = acct.profiles
    sms_rate = p.sms_consent_rate

    # SMS consent counts require profile segment queries — unavailable via basic API
    # Only penalise if we have actual profile data showing a real low rate
    if p.emailable_profiles > 0 and p.sms_consented_profiles > 0:
        if sms_rate < 0.05:
            score -= 3
            penalties.append(f"SMS consent rate {sms_rate:.1%} < 5% (very low)")
        elif sms_rate < 0.15:
            score -= 1
            penalties.append(f"SMS consent rate {sms_rate:.1%} < 15%")
        elif sms_rate >= 0.30:
            score += 1
            bonuses.append(f"SMS consent rate {sms_rate:.1%} ≥ 30%")
    else:
        bonuses.append("SMS consent count unavailable via API — not penalised")

    # flow-messages unavailable via API — use SMS campaigns as proxy for SMS usage
    sms_in_flows = any(f.sms_count > 0 for f in acct.live_flows)
    has_sms_campaigns = acct.campaigns.sms_campaigns > 0
    if not sms_in_flows and not has_sms_campaigns:
        score -= 2
        penalties.append("No SMS messages in flows or SMS campaigns found")
    elif has_sms_campaigns:
        bonuses.append(f"{acct.campaigns.sms_campaigns} SMS campaigns sent (flow detail unavailable)")

    if acct.campaigns.sms_campaigns == 0:
        score -= 1
        penalties.append("No SMS campaigns sent in audit period")
    elif acct.campaigns.sms_campaigns >= 4:
        bonuses.append(f"{acct.campaigns.sms_campaigns} SMS campaigns sent")

    # SMS form capture
    sms_form = any(f.collects_sms for f in acct.active_forms)
    if not sms_form:
        score -= 1
        penalties.append("No active form collects SMS consent")
    else:
        bonuses.append("At least one form collects SMS consent")

    score = max(1, min(10, score))
    justification = (
        f"SMS enabled | Consent rate: {sms_rate:.1%} | "
        f"SMS in flows: {sms_in_flows} | SMS campaigns: {acct.campaigns.sms_campaigns}"
    )
    return CategoryScore(
        name="SMS Adoption",
        score=score,
        weight=WEIGHTS["SMS Adoption"],
        justification=justification,
        penalties_applied=penalties,
        bonuses_applied=bonuses,
    )


def _score_signup_forms(acct: AccountData) -> CategoryScore:
    penalties: List[str] = []
    bonuses: List[str] = []
    forms = acct.active_forms

    if not forms:
        # Forms API unavailable in this Klaviyo API revision — can't confirm or deny
        # Score neutrally rather than penalising for missing data
        return CategoryScore(
            name="Signup Forms & List Growth",
            score=5,
            weight=WEIGHTS["Signup Forms & List Growth"],
            justification="Signup form data unavailable via Klaviyo API (endpoint requires newer revision). Unable to score.",
            penalties_applied=[],
            bonuses_applied=["Score held at neutral (5) — data not available via API"],
        )

    score = 6
    primary = acct.primary_form  # highest-traffic form

    if primary:
        opt_in = primary.opt_in_rate
        if opt_in < 0.01:
            score = min(score, 3)
            penalties.append(f"Primary form opt-in rate {opt_in:.2%} < 1% (cap: 3)")
        elif opt_in < 0.02:
            score -= 2
            penalties.append(f"Primary form opt-in rate {opt_in:.2%} < 2%")
        elif opt_in < 0.03:
            score -= 1
            penalties.append(f"Primary form opt-in rate {opt_in:.2%} < 3%")
        elif opt_in >= 0.05:
            score += 1
            bonuses.append(f"Primary form opt-in rate {opt_in:.2%} ≥ 5%")

        # Mobile opt-in
        mob_rate = primary.mobile_opt_in_rate
        if primary.mobile_views > 0 and mob_rate < 0.01:
            score -= 1
            penalties.append(f"Mobile form opt-in rate {mob_rate:.2%} < 1%")

        if not primary.has_incentive:
            score -= 1
            penalties.append("Primary form offers no incentive")
        else:
            bonuses.append("Primary form includes an incentive")

    sms_form = any(f.collects_sms for f in forms)
    if acct.sms_enabled and not sms_form:
        score -= 1
        penalties.append("SMS enabled but no form collects SMS opt-in")
    elif sms_form:
        bonuses.append("Form collects SMS opt-in")

    score = max(1, min(10, score))
    opt_rate_str = f"{primary.opt_in_rate:.2%}" if primary else "N/A"
    justification = (
        f"{len(forms)} active form(s) | Primary opt-in: {opt_rate_str} | "
        f"SMS capture: {sms_form}"
    )
    return CategoryScore(
        name="Signup Forms & List Growth",
        score=score,
        weight=WEIGHTS["Signup Forms & List Growth"],
        justification=justification,
        penalties_applied=penalties,
        bonuses_applied=bonuses,
    )


def _score_list_health(acct: AccountData) -> CategoryScore:
    p = acct.profiles
    penalties: List[str] = []
    bonuses: List[str] = []
    score = 7

    if p.emailable_profiles == 0:
        # Profile engagement data unavailable via Klaviyo API
        return CategoryScore(
            name="List Health & Engagement",
            score=5,
            weight=WEIGHTS["List Health & Engagement"],
            justification="Profile engagement data unavailable via Klaviyo API (requires aggregate queries). Score held at neutral.",
            penalties_applied=[],
            bonuses_applied=["Score held at neutral (5) — engagement data not available via API"],
        )

    # Suppression rate
    if p.suppression_rate >= 0.20:
        score -= 3
        penalties.append(f"Suppression rate {p.suppression_rate:.1%} ≥ 20%")
    elif p.suppression_rate >= 0.10:
        score -= 1
        penalties.append(f"Suppression rate {p.suppression_rate:.1%} ≥ 10%")

    # Dormant rate (not engaged in 180d)
    if p.dormant_rate >= 0.60:
        score -= 3
        penalties.append(f"Dormant rate {p.dormant_rate:.1%} ≥ 60% (over half the list is cold)")
    elif p.dormant_rate >= 0.40:
        score -= 2
        penalties.append(f"Dormant rate {p.dormant_rate:.1%} ≥ 40%")
    elif p.dormant_rate >= 0.25:
        score -= 1
        penalties.append(f"Dormant rate {p.dormant_rate:.1%} ≥ 25%")

    # Engagement rates — only score if we have actual engagement data
    if p.engaged_30_day > 0:
        if p.engaged_30_pct >= 0.20:
            bonuses.append(f"30-day engagement {p.engaged_30_pct:.1%} ≥ 20% (strong active segment)")
        elif p.engaged_30_pct < 0.05:
            score -= 1
            penalties.append(f"30-day engagement only {p.engaged_30_pct:.1%} < 5%")
    else:
        bonuses.append("Engagement segment data unavailable via API — not penalised")

    if p.engaged_90_pct >= 0.35:
        bonuses.append(f"90-day engagement {p.engaged_90_pct:.1%} ≥ 35%")

    score = max(1, min(10, score))
    justification = (
        f"Total: {p.total_profiles:,} | Emailable: {p.emailable_profiles:,} | "
        f"Suppressed: {p.suppression_rate:.1%} | Dormant: {p.dormant_rate:.1%} | "
        f"Engaged-30d: {p.engaged_30_pct:.1%} | Engaged-90d: {p.engaged_90_pct:.1%}"
    )
    return CategoryScore(
        name="List Health & Engagement",
        score=score,
        weight=WEIGHTS["List Health & Engagement"],
        justification=justification,
        penalties_applied=penalties,
        bonuses_applied=bonuses,
    )


def _score_segmentation(acct: AccountData) -> CategoryScore:
    s = acct.segmentation
    penalties: List[str] = []
    bonuses: List[str] = []
    score = 5

    if s.has_engaged_30_segment:
        score += 1
        bonuses.append("Engaged 30-day segment exists")
    else:
        penalties.append("No engaged 30-day segment")

    if s.has_engaged_90_segment:
        score += 1
        bonuses.append("Engaged 90-day segment exists")
    else:
        penalties.append("No engaged 90-day segment")

    if s.has_vip_segment:
        score += 1
        bonuses.append("VIP segment exists")
    else:
        penalties.append("No VIP segment")

    if s.has_purchaser_segment:
        score += 1
        bonuses.append("Purchaser/customer segment exists")
    else:
        penalties.append("No purchaser segment")

    if s.has_sunset_segment:
        score += 1
        bonuses.append("Sunset/suppression segment exists")
    else:
        penalties.append("No sunset segment for list hygiene")

    if s.pct_campaigns_to_engaged < 0.25:
        score -= 2
        penalties.append(f"Only {s.pct_campaigns_to_engaged:.0%} of campaigns target engaged segments")
    elif s.pct_campaigns_to_engaged >= 0.75:
        bonuses.append(f"{s.pct_campaigns_to_engaged:.0%} of campaigns use engaged segments")

    score = max(1, min(10, score))
    justification = (
        f"Engaged-30: {s.has_engaged_30_segment} | Engaged-90: {s.has_engaged_90_segment} | "
        f"VIP: {s.has_vip_segment} | Purchaser: {s.has_purchaser_segment} | "
        f"Sunset: {s.has_sunset_segment} | Campaign engaged-rate: {s.pct_campaigns_to_engaged:.0%}"
    )
    return CategoryScore(
        name="Segmentation Quality",
        score=score,
        weight=WEIGHTS["Segmentation Quality"],
        justification=justification,
        penalties_applied=penalties,
        bonuses_applied=bonuses,
    )


def _score_revenue_attribution(acct: AccountData) -> CategoryScore:
    r = acct.revenue
    b = r.benchmarks
    penalties: List[str] = []
    bonuses: List[str] = []
    score = 6

    if not r.revenue_attribution_configured:
        return CategoryScore(
            name="Revenue Attribution",
            score=2,
            weight=WEIGHTS["Revenue Attribution"],
            justification="Revenue attribution is not configured.",
            penalties_applied=["Revenue attribution not configured (cap: 2)"],
            bonuses_applied=[],
        )

    if not acct.ecommerce_events_configured:
        score -= 2
        penalties.append("Ecommerce events not fully configured")

    # Flow revenue share — ideally 40–60%
    if r.total_klaviyo_revenue > 0:
        if r.flow_revenue_pct < 0.20:
            score -= 2
            penalties.append(f"Flows contribute only {r.flow_revenue_pct:.0%} of total revenue (<20%)")
        elif r.flow_revenue_pct >= 0.35:
            bonuses.append(f"Flows contribute {r.flow_revenue_pct:.0%} of total revenue")

    # Benchmark-based adjustments
    rating_score = {"poor": -2, "below_average": -1, "average": 0, "good": 1, "excellent": 2}
    overall = b.overall_rating
    adj = rating_score.get(overall, 0)
    if adj > 0:
        score += adj
        bonuses.append(f"Benchmark overall rating: {overall}")
    elif adj < 0:
        score += adj
        penalties.append(f"Benchmark overall rating: {overall}")

    score = max(1, min(10, score))

    # Revenue figures unavailable via Klaviyo API (requires metric aggregates)
    if r.total_klaviyo_revenue == 0:
        justification = (
            "Revenue attribution data unavailable via API — "
            "requires Klaviyo metric aggregates endpoint. Score held at neutral."
        )
    else:
        justification = (
            f"Total Klaviyo revenue: ${r.total_klaviyo_revenue:,.0f} | "
            f"Flow: {r.flow_revenue_pct:.0%} | Campaign: {r.campaign_revenue_pct:.0%} | "
            f"Benchmark overall: {b.overall_rating}"
        )
    return CategoryScore(
        name="Revenue Attribution",
        score=score,
        weight=WEIGHTS["Revenue Attribution"],
        justification=justification,
        penalties_applied=penalties,
        bonuses_applied=bonuses,
    )


def _score_billing(acct: AccountData) -> CategoryScore:
    b = acct.billing
    p = acct.profiles
    penalties: List[str] = []
    bonuses: List[str] = []
    score = 8

    if b.plan_profile_limit > 0 and p.total_profiles > 0:
        utilization = p.total_profiles / b.plan_profile_limit
        if utilization >= 0.95:
            score -= 3
            penalties.append(f"Profile utilization {utilization:.0%} ≥ 95% (overage risk)")
        elif utilization >= 0.85:
            score -= 1
            penalties.append(f"Profile utilization {utilization:.0%} ≥ 85%")
        elif utilization < 0.40:
            score -= 1
            penalties.append(
                f"Profile utilization {utilization:.0%} < 40% — possible plan overpay"
            )
        else:
            bonuses.append(f"Profile utilization {utilization:.0%} within efficient range")

        # Suppression bloat
        if p.suppression_rate >= 0.15 and b.plan_profile_limit > 0:
            penalties.append(
                "High suppression rate driving up billable profile count — consider cleaning list"
            )
            score -= 1
    else:
        score = 5
        penalties.append("Billing plan limits not available — utilization cannot be calculated")

    score = max(1, min(10, score))
    limit_str = f"{b.plan_profile_limit:,}" if b.plan_profile_limit > 0 else "unknown"
    justification = (
        f"Plan: {b.plan_tier} | Limit: {limit_str} profiles | "
        f"Current: {p.total_profiles:,} profiles"
    )
    return CategoryScore(
        name="Billing Efficiency",
        score=score,
        weight=WEIGHTS["Billing Efficiency"],
        justification=justification,
        penalties_applied=penalties,
        bonuses_applied=bonuses,
    )


# ── composite ──────────────────────────────────────────────────────────────

def run_scoring(acct: AccountData) -> Tuple[List[CategoryScore], int, str]:
    """Return (category_scores, composite_score, score_band)."""
    scorers = [
        _score_deliverability,
        _score_core_flow_coverage,
        _score_flow_configuration,
        _score_campaign_strategy,
        _score_sms_adoption,
        _score_signup_forms,
        _score_list_health,
        _score_segmentation,
        _score_revenue_attribution,
        _score_billing,
    ]
    scores = [fn(acct) for fn in scorers]
    composite = round(sum(s.weighted_points for s in scores))
    composite = max(0, min(100, composite))
    band = score_band(composite)
    return scores, composite, band
