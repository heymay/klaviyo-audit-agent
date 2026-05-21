"""
Klaviyo Audit Katie — Markdown Report Generator
Produces a structured Markdown audit report matching output-template.md (22 sections).
"""
from __future__ import annotations
from datetime import date
from typing import List
from .models import AuditResult, Finding, Recommendation, CategoryScore
from .opportunity import format_opportunity_section, OpportunityRange


_TODAY = date.today().isoformat()

_DISCLAIMER = (
    "> **Disclaimer:** This audit is diagnostic and informational only. All findings are based on "
    "data available at the time of the audit. Revenue opportunity estimates are directional ranges "
    "only and are not guarantees of results. National Positions does not make changes to your "
    "Klaviyo account without your explicit authorization. This audit does not constitute legal, "
    "compliance, or financial advice."
)

_NP_CTA = """---

## Section 22 — National Positions Consultation

**Want help turning this audit into revenue?**

National Positions can help you rebuild flows, improve deliverability, launch SMS, optimize forms,
refine segmentation, and manage Klaviyo on an ongoing basis.

**Schedule a consultation with our Marketing Automation team.**

> [SCHEDULE A CONSULTATION — CALENDLY LINK PLACEHOLDER]
>
> Or contact us at: **nationalpositions.com**

---

### Why National Positions?

- Klaviyo-certified marketing automation specialists
- Ecommerce-first methodology — built for Shopify, WooCommerce, and beyond
- Data-driven: every recommendation tied to measurable business impact
- Full-service: strategy, implementation, optimization, and ongoing management

---

{disclaimer}

*Prepared by Klaviyo Audit Katie | National Positions | {today}*
""".format(disclaimer=_DISCLAIMER, today=_TODAY)


def _severity_emoji(sev: str) -> str:
    return {"Critical": "🔴", "High": "🟠", "Medium": "🟡", "Low": "🔵", "Positive": "✅"}.get(sev, "•")


def _band_label(band: str) -> str:
    labels = {
        "Elite": "🏆 Elite",
        "Strong": "✅ Strong",
        "Average": "📊 Average",
        "Weak": "⚠️ Weak",
        "Critical": "🚨 Critical",
    }
    return labels.get(band, band)


def generate_report(result: AuditResult) -> str:
    acct = result.account
    lines: List[str] = []

    # ── Section 1 — Document Header ────────────────────────────────────────
    lines += [
        "# Klaviyo Account Audit Report",
        "",
        f"**CONFIDENTIAL** — Prepared for internal review and client delivery by National Positions",
        "",
        "| Field | Value |",
        "|---|---|",
        f"| Client / Brand | {acct.business_name} |",
        f"| Website | {acct.website} |",
        f"| Klaviyo Account | {acct.klaviyo_account_name} |",
        f"| Audit Period | {acct.audit_period_label} ({acct.audit_period_days} days) |",
        f"| Ecommerce Platform | {acct.ecommerce_platform} |",
        f"| Date Generated | {_TODAY} |",
        f"| Prepared By | Klaviyo Audit Katie — National Positions |",
        f"| Approved By | [NP Reviewer Name — required before delivery] |",
        "",
    ]

    # ── Section 2 — Overall Score ──────────────────────────────────────────
    lines += [
        "---",
        "",
        f"## Section 2 — Klaviyo Health Score: {result.composite_score}/100 — {_band_label(result.score_band)}",
        "",
        f"This account scored **{result.composite_score} out of 100** — rated **{result.score_band}**.",
        "",
        "| Band | Range | Description |",
        "|---|---|---|",
        "| 🏆 Elite | 90–100 | Best-in-class Klaviyo operation |",
        "| ✅ Strong | 75–89 | High-performing with minor gaps |",
        "| 📊 Average | 60–74 | Functional but meaningful opportunities remain |",
        "| ⚠️ Weak | 40–59 | Significant gaps requiring attention |",
        "| 🚨 Critical | 0–39 | Fundamental issues requiring immediate action |",
        "",
    ]

    # ── Section 3 — Score Breakdown ───────────────────────────────────────
    lines += [
        "---",
        "",
        "## Section 3 — Score Breakdown by Category",
        "",
        "| Category | Score (1–10) | Weight | Weighted Points |",
        "|---|---|---|---|",
    ]
    for cs in result.category_scores:
        lines.append(
            f"| {cs.name} | {cs.score}/10 | {cs.weight:.0%} | {cs.weighted_points:.1f} |"
        )
    lines += [
        f"| **COMPOSITE TOTAL** | — | 100% | **{result.composite_score}/100** |",
        "",
    ]

    # ── Section 4 — Executive Summary ─────────────────────────────────────
    critical_count = len(result.critical_findings)
    high_count = len(result.high_findings)
    lines += [
        "---",
        "",
        "## Section 4 — Executive Summary",
        "",
        f"This Klaviyo audit covers {acct.audit_period_label.lower()} of account activity "
        f"for **{acct.business_name}** across campaigns, flows, forms, list health, deliverability, "
        f"SMS adoption, segmentation, and revenue attribution.",
        "",
        f"The account scored **{result.composite_score}/100** ({result.score_band}), with "
        f"**{critical_count} Critical** and **{high_count} High** priority findings. "
        "The most impactful opportunities center on the areas highlighted in Sections 5–7.",
        "",
    ]

    # ── Section 5 — Top 5 Wins ─────────────────────────────────────────────
    lines += [
        "---",
        "",
        "## Section 5 — Top 5 Wins",
        "",
    ]
    strong_cats = sorted(
        [cs for cs in result.category_scores if cs.score >= 7],
        key=lambda x: -x.score,
    )[:5]
    if strong_cats:
        for i, cs in enumerate(strong_cats, 1):
            bonus_text = "; ".join(cs.bonuses_applied) if cs.bonuses_applied else "Performing at or above benchmark."
            lines.append(f"{i}. **{cs.name}** ({cs.score}/10) — {bonus_text}")
    else:
        lines.append("No categories are currently scoring at 7/10 or above. Focus on the critical issues first.")
    lines.append("")

    # ── Data Quality Notice (if gaps detected) ────────────────────────────
    if result.data_gaps:
        lines += [
            "---",
            "",
            "> **Data Quality Notice:** Some fields in this audit are at default/zero values because "
            "manual_inputs.json was not fully completed. Affected scoring categories are marked "
            "with reduced confidence. Complete the manual inputs file and re-run for a final audit.",
            "",
            "> Missing fields:",
        ]
        for gap in result.data_gaps:
            lines.append(f"> - {gap}")
        lines.append("")

    # ── Section 6 — Top 5 Issues ──────────────────────────────────────────
    lines += [
        "---",
        "",
        "## Section 6 — Top 5 Issues",
        "",
    ]
    top_issues = result.scoreable_findings[:5]
    for i, f in enumerate(top_issues, 1):
        lines += [
            f"{i}. {_severity_emoji(f.severity)} **[{f.severity}] {f.rule_id}** — {f.description}",
            f"   - *Business Impact:* {f.business_impact}",
            f"   - *Action:* {f.recommended_action}",
            "",
        ]

    # ── Section 7 — Top 5 Revenue Opportunities ───────────────────────────
    lines += [
        "---",
        "",
        "## Section 7 — Top 5 Revenue Opportunities",
        "",
    ]
    top_recs = result.recommendations[:5]
    for i, r in enumerate(top_recs, 1):
        lines += [
            f"{i}. **{r.issue}**",
            f"   - *Why it matters:* {r.why_it_matters}",
            f"   - *Opportunity:* {r.opportunity_note}",
            f"   - *Next step:* {r.next_step}",
            f"   - Impact: **{r.expected_impact}** | Complexity: {r.complexity} | Timeline: {r.timeline}",
            "",
        ]

    # ── Section 8 — SMS Audit ─────────────────────────────────────────────
    p = acct.profiles
    sms_findings = [f for f in result.findings if f.category == "SMS Adoption"]
    lines += [
        "---",
        "",
        "## Section 8 — SMS Audit",
        "",
        f"**SMS Enabled:** {'Yes' if acct.sms_enabled else 'No'}",
        f"**SMS Consented Profiles:** {p.sms_consented_profiles:,} ({p.sms_consent_rate:.1%} of emailable list)",
        f"**SMS in Flows:** {'Yes' if any(f.sms_count > 0 for f in acct.live_flows) else 'No'}",
        f"**SMS Campaigns (audit period):** {acct.campaigns.sms_campaigns}",
        "",
    ]
    if sms_findings:
        lines.append("**Findings:**")
        for f in sms_findings:
            lines.append(f"- {_severity_emoji(f.severity)} [{f.severity}] {f.description}")
    lines.append("")

    # ── Section 9 — Campaign Strategy ─────────────────────────────────────
    c = acct.campaigns
    camp_findings = [f for f in result.findings if f.category == "Campaign Strategy"]
    lines += [
        "---",
        "",
        "## Section 9 — Campaign Strategy Audit",
        "",
        f"| Metric | Value |",
        f"|---|---|",
        f"| Total Campaigns (period) | {c.total_sent} |",
        f"| Email Campaigns | {c.email_campaigns} |",
        f"| SMS Campaigns | {c.sms_campaigns} |",
        f"| Campaigns per Week | {c.campaigns_per_week:.1f} |",
        f"| Avg Open Rate | {c.avg_open_rate:.1%} |",
        f"| Avg Click Rate | {c.avg_click_rate:.1%} |",
        f"| Avg Unsubscribe Rate | {c.avg_unsubscribe_rate:.2%} |",
        f"| Avg Spam Complaint Rate | {c.avg_spam_complaint_rate:.3%} |",
        f"| Avg Hard Bounce Rate | {c.avg_hard_bounce_rate:.2%} |",
        f"| % Sent to Engaged Segments | {c.pct_to_engaged_segments:.0%} |",
        f"| Open Rate Trend | {c.open_rate_trend.title()} |",
        f"| Longest Send Gap | {c.longest_gap_days} days |",
        "",
    ]
    if camp_findings:
        lines.append("**Findings:**")
        for f in camp_findings:
            lines.append(f"- {_severity_emoji(f.severity)} [{f.severity}] {f.description}")
    lines.append("")

    # ── Section 10 — Deliverability ────────────────────────────────────────
    d = acct.deliverability
    delv_findings = [f for f in result.findings if f.category == "Deliverability"]
    lines += [
        "---",
        "",
        "## Section 10 — Deliverability Audit",
        "",
        "| Metric | Value | Status |",
        "|---|---|---|",
        f"| Hard Bounce Rate | {d.hard_bounce_rate:.2%} | {'🔴 Critical' if d.hard_bounce_rate >= 0.02 else '🟠 High' if d.hard_bounce_rate >= 0.01 else '✅ OK'} |",
        f"| Soft Bounce Rate | {d.soft_bounce_rate:.2%} | — |",
        f"| Spam Complaint Rate | {d.spam_complaint_rate:.3%} | {'🔴 Critical' if d.spam_complaint_rate >= 0.001 else '🟠 High' if d.spam_complaint_rate >= 0.0008 else '✅ OK'} |",
        f"| Unsubscribe Rate | {d.avg_unsubscribe_rate:.2%} | {'🟠 High' if d.avg_unsubscribe_rate >= 0.005 else '✅ OK'} |",
        f"| SPF | {'✅ Configured' if d.has_spf else '🔴 Missing'} | — |",
        f"| DKIM | {'✅ Configured' if d.has_dkim else '🔴 Missing'} | — |",
        f"| DMARC | {'✅ Configured' if d.has_dmarc else '🔴 Missing'} | — |",
        f"| Branded Sending Domain | {'✅ Yes' if d.has_branded_sending_domain else '🟡 No'} | — |",
        "",
    ]
    if delv_findings:
        lines.append("**Findings:**")
        for f in delv_findings:
            lines.append(f"- {_severity_emoji(f.severity)} [{f.severity}] {f.description}")
    lines.append("")

    # ── Section 11 — Core Flow Coverage ───────────────────────────────────
    FLOW_DISPLAY = [
        ("welcome", "Welcome Series"),
        ("abandoned_cart", "Abandoned Cart"),
        ("added_to_cart", "Added to Cart"),
        ("browse_abandonment", "Browse Abandonment"),
        ("post_purchase", "Post-Purchase"),
        ("winback", "Winback / Re-engagement"),
        ("vip", "VIP / Loyalty"),
    ]
    flow_findings = [f for f in result.findings if f.category == "Core Flows"]
    lines += [
        "---",
        "",
        "## Section 11 — Core Flow Coverage",
        "",
        "| Flow | Status | Revenue | Emails | SMS |",
        "|---|---|---|---|---|",
    ]
    for ft, label in FLOW_DISPLAY:
        flow = acct.get_flow(ft)
        if flow:
            lines.append(
                f"| {label} | ✅ Live | ${flow.revenue:,.0f} | {flow.email_count} | {flow.sms_count} |"
            )
        else:
            lines.append(f"| {label} | ❌ Missing | — | — | — |")
    lines.append("")
    if flow_findings:
        lines.append("**Findings:**")
        for f in flow_findings:
            lines.append(f"- {_severity_emoji(f.severity)} [{f.severity}] {f.description}")
    lines.append("")

    # ── Section 12 — Flow Configuration ───────────────────────────────────
    lines += [
        "---",
        "",
        "## Section 12 — Flow Configuration Audit",
        "",
    ]
    for flow in acct.live_flows:
        lines += [
            f"### {flow.name}",
            f"- Status: {flow.status} | Emails: {flow.email_count} | SMS: {flow.sms_count}",
            f"- First message delay: {flow.first_message_delay_minutes} minutes",
            f"- Has incentive: {'Yes' if flow.has_incentive else 'No'}",
            f"- Last updated: {flow.last_updated_days_ago} days ago",
            "",
        ]
    if not acct.live_flows:
        lines.append("*No live flows to display.*\n")

    # ── Section 13 — Signup Forms ──────────────────────────────────────────
    form_findings = [f for f in result.findings if f.category == "Signup Forms"]
    lines += [
        "---",
        "",
        "## Section 13 — Signup Form Audit",
        "",
        f"**Active Forms:** {len(acct.active_forms)}",
        "",
    ]
    if acct.active_forms:
        lines += [
            "| Form | Type | Opt-In Rate | Mobile Opt-In | SMS Capture | Incentive |",
            "|---|---|---|---|---|---|",
        ]
        for form in acct.active_forms:
            lines.append(
                f"| {form.name} | {form.form_type} | {form.opt_in_rate:.2%} | "
                f"{form.mobile_opt_in_rate:.2%} | {'Yes' if form.collects_sms else 'No'} | "
                f"{'Yes' if form.has_incentive else 'No'} |"
            )
    lines.append("")
    if form_findings:
        lines.append("**Findings:**")
        for f in form_findings:
            lines.append(f"- {_severity_emoji(f.severity)} [{f.severity}] {f.description}")
    lines.append("")

    # ── Section 14 — Benchmark Review ─────────────────────────────────────
    b = acct.revenue.benchmarks
    lines += [
        "---",
        "",
        "## Section 14 — Benchmark Review",
        "",
        "| Metric | Rating |",
        "|---|---|",
        f"| Open Rate | {b.open_rate_rating.replace('_', ' ').title()} |",
        f"| Click Rate | {b.click_rate_rating.replace('_', ' ').title()} |",
        f"| Conversion Rate | {b.conversion_rate_rating.replace('_', ' ').title()} |",
        f"| Flow Revenue | {b.flow_revenue_rating.replace('_', ' ').title()} |",
        f"| List Growth | {b.list_growth_rating.replace('_', ' ').title()} |",
        f"| **Overall** | **{b.overall_rating.replace('_', ' ').title()}** |",
        "",
    ]

    # ── Section 15 — List Health ───────────────────────────────────────────
    list_findings = [f for f in result.findings if f.category == "List Health"]
    lines += [
        "---",
        "",
        "## Section 15 — List Health Review",
        "",
        "| Metric | Value |",
        "|---|---|",
        f"| Total Profiles | {p.total_profiles:,} |",
        f"| Emailable Profiles | {p.emailable_profiles:,} |",
        f"| SMS Consented | {p.sms_consented_profiles:,} ({p.sms_consent_rate:.1%}) |",
        f"| Suppressed | {p.suppressed_profiles:,} ({p.suppression_rate:.1%}) |",
        f"| Engaged (30 days) | {p.engaged_30_day:,} ({p.engaged_30_pct:.1%}) |",
        f"| Engaged (90 days) | {p.engaged_90_day:,} ({p.engaged_90_pct:.1%}) |",
        f"| Dormant (180+ days) | {p.dormant_profiles:,} ({p.dormant_rate:.1%}) |",
        "",
    ]
    if list_findings:
        lines.append("**Findings:**")
        for f in list_findings:
            lines.append(f"- {_severity_emoji(f.severity)} [{f.severity}] {f.description}")
    lines.append("")

    # ── Section 16 — Segmentation ──────────────────────────────────────────
    seg = acct.segmentation
    seg_findings = [f for f in result.findings if f.category == "Segmentation"]
    lines += [
        "---",
        "",
        "## Section 16 — Segmentation Review",
        "",
        "| Segment | Exists |",
        "|---|---|",
        f"| Engaged 30-day | {'✅' if seg.has_engaged_30_segment else '❌'} |",
        f"| Engaged 90-day | {'✅' if seg.has_engaged_90_segment else '❌'} |",
        f"| VIP / High-Value | {'✅' if seg.has_vip_segment else '❌'} |",
        f"| Purchaser / Customer | {'✅' if seg.has_purchaser_segment else '❌'} |",
        f"| Sunset / Hygiene | {'✅' if seg.has_sunset_segment else '❌'} |",
        f"| % Campaigns to Engaged | {seg.pct_campaigns_to_engaged:.0%} |",
        "",
    ]
    if seg_findings:
        lines.append("**Findings:**")
        for f in seg_findings:
            lines.append(f"- {_severity_emoji(f.severity)} [{f.severity}] {f.description}")
    lines.append("")

    # ── Section 17 — Revenue Attribution ──────────────────────────────────
    r = acct.revenue
    rev_findings = [f for f in result.findings if f.category == "Revenue Attribution"]
    lines += [
        "---",
        "",
        "## Section 17 — Revenue Attribution Review",
        "",
        f"| Metric | Value |",
        f"|---|---|",
        f"| Total Klaviyo Revenue | ${r.total_klaviyo_revenue:,.0f} |",
        f"| Flow Revenue | ${r.flow_revenue:,.0f} ({r.flow_revenue_pct:.0%}) |",
        f"| Campaign Revenue | ${r.campaign_revenue:,.0f} ({r.campaign_revenue_pct:.0%}) |",
        f"| Attribution Configured | {'Yes' if r.revenue_attribution_configured else 'No'} |",
        "",
    ]
    if rev_findings:
        lines.append("**Findings:**")
        for f in rev_findings:
            lines.append(f"- {_severity_emoji(f.severity)} [{f.severity}] {f.description}")
    lines.append("")

    # ── Section 18 — Billing ───────────────────────────────────────────────
    billing = acct.billing
    bill_findings = [f for f in result.findings if f.category == "Billing"]
    util = (p.total_profiles / billing.plan_profile_limit * 100) if billing.plan_profile_limit > 0 else 0
    lines += [
        "---",
        "",
        "## Section 18 — Billing Efficiency Review",
        "",
        f"| Field | Value |",
        f"|---|---|",
        f"| Plan Tier | {billing.plan_tier} |",
        f"| Plan Profile Limit | {billing.plan_profile_limit:,} |",
        f"| Current Profile Count | {p.total_profiles:,} |",
        f"| Utilization | {util:.0f}% |",
        "",
    ]
    if bill_findings:
        lines.append("**Findings:**")
        for f in bill_findings:
            lines.append(f"- {_severity_emoji(f.severity)} [{f.severity}] {f.description}")
    lines.append("")

    # ── Section 19 — Compliance ────────────────────────────────────────────
    comp_findings = [f for f in result.findings if f.category == "Compliance"]
    lines += [
        "---",
        "",
        "## Section 19 — Compliance and Consent Review",
        "",
        "> This section identifies potential compliance risk areas. It does not constitute legal advice. "
        "Consult qualified legal counsel for definitive guidance.",
        "",
        "| Control | Status |",
        "|---|---|",
        f"| SPF | {'✅ Configured' if d.has_spf else '❌ Missing'} |",
        f"| DKIM | {'✅ Configured' if d.has_dkim else '❌ Missing'} |",
        f"| DMARC | {'✅ Configured' if d.has_dmarc else '❌ Missing'} |",
        f"| Branded Sending Domain | {'✅ Yes' if d.has_branded_sending_domain else '⚠️ No'} |",
        f"| SMS Consent Documented | {'✅ Yes' if acct.sms_enabled and p.sms_consent_rate > 0.01 else '⚠️ Review Required' if acct.sms_enabled else 'N/A'} |",
        "",
    ]
    if comp_findings:
        lines.append("**Findings:**")
        for f in comp_findings:
            lines.append(f"- {_severity_emoji(f.severity)} [{f.severity}] {f.description}")
    lines.append("")

    # ── Section 20 — 30/60/90 Day Action Plan ─────────────────────────────
    immediate = [r for r in result.recommendations if r.timeline == "Immediate"]
    thirty = [r for r in result.recommendations if r.timeline == "30 days"]
    sixty = [r for r in result.recommendations if r.timeline == "60 days"]
    ninety = [r for r in result.recommendations if r.timeline == "90 days"]

    lines += [
        "---",
        "",
        "## Section 20 — 30/60/90 Day Action Plan",
        "",
        "### Immediate (Do This Week)",
        "",
    ]
    if immediate:
        lines += ["| Priority | Action | Owner | Impact |", "|---|---|---|---|"]
        for r in immediate:
            lines.append(f"| {r.priority} | {r.issue} | {r.owner} | {r.expected_impact} |")
    else:
        lines.append("*No immediate actions required.*")

    lines += ["", "### 30-Day Plan", ""]
    if thirty:
        lines += ["| Priority | Action | Owner | Impact |", "|---|---|---|---|"]
        for r in thirty:
            lines.append(f"| {r.priority} | {r.issue} | {r.owner} | {r.expected_impact} |")
    else:
        lines.append("*No 30-day actions required.*")

    lines += ["", "### 60-Day Plan", ""]
    if sixty:
        lines += ["| Priority | Action | Owner | Impact |", "|---|---|---|---|"]
        for r in sixty:
            lines.append(f"| {r.priority} | {r.issue} | {r.owner} | {r.expected_impact} |")
    else:
        lines.append("*No 60-day actions.*")

    lines += ["", "### 90-Day Plan", ""]
    if ninety:
        lines += ["| Priority | Action | Owner | Impact |", "|---|---|---|---|"]
        for r in ninety:
            lines.append(f"| {r.priority} | {r.issue} | {r.owner} | {r.expected_impact} |")
    else:
        lines.append("*No 90-day actions.*")
    lines.append("")

    # ── Section 21 — Estimated Opportunity Summary ─────────────────────────
    high_recs = [r for r in result.recommendations if r.expected_impact == "High"]
    opp = getattr(result, "_opportunity", None)
    lines += [
        "---",
        "",
        "## Section 21 — Estimated Opportunity Summary",
        "",
        f"Based on the {len(result.recommendations)} recommendations in this audit, "
        f"**{len(high_recs)} High-impact opportunities** have been identified.",
        "",
    ]
    if opp:
        lines.append(format_opportunity_section(opp))
    else:
        lines += [
            "- **Conservative:** 10–20% lift in email-attributed revenue within 90 days",
            "- **Moderate:** 20–40% lift within 6 months with full flow and segmentation buildout",
            "- **Optimistic:** 40–80% lift within 12 months with SMS launch, flow optimization, and ongoing campaign strategy",
            "",
            _DISCLAIMER,
        ]
    lines.append("")

    # ── Section 22 — NP CTA ────────────────────────────────────────────────
    lines.append(_NP_CTA)

    return "\n".join(lines)
