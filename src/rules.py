"""
Klaviyo Audit Katie — Decision Rules Engine
Evaluates key rules from decision-rules.md and returns Finding objects.
Rules are grouped by section; each function returns 0-N findings.
"""
from __future__ import annotations
from typing import List
from .models import AccountData, Finding


def _f(rule_id: str, severity: str, category: str, description: str,
        business_impact: str, recommended_action: str, priority: str,
        score_impact: str = "", confidence: str = "Confirmed") -> Finding:
    return Finding(
        rule_id=rule_id, severity=severity, category=category,
        description=description, business_impact=business_impact,
        recommended_action=recommended_action, priority=priority,
        score_impact=score_impact, confidence=confidence,
    )


# ── SMS rules ──────────────────────────────────────────────────────────────

def _rules_sms(acct: AccountData) -> List[Finding]:
    findings: List[Finding] = []
    p = acct.profiles

    if not acct.sms_enabled:
        findings.append(_f(
            "SMS-001", "High", "SMS Adoption",
            "SMS is not enabled in this Klaviyo account.",
            "Brands that add SMS alongside email typically see 20–30% incremental revenue lift from the combined channel.",
            "Enable SMS in Klaviyo (Settings → SMS). Set up at least one SMS flow (Welcome or Abandoned Cart) within 30 days.",
            "High", "-8 points SMS Adoption",
        ))
        return findings  # subsequent SMS rules require SMS enabled

    sms_rate = p.sms_consent_rate
    if sms_rate < 0.05:
        findings.append(_f(
            "SMS-002", "High", "SMS Adoption",
            f"SMS consent rate is only {sms_rate:.1%} of emailable profiles.",
            "A small SMS list limits revenue contribution and ROI from SMS infrastructure costs.",
            "Add SMS opt-in to all signup forms and welcome flows. Run an SMS acquisition campaign to existing email subscribers.",
            "High", "-3 points SMS Adoption",
        ))
    elif sms_rate < 0.15:
        findings.append(_f(
            "SMS-003", "Medium", "SMS Adoption",
            f"SMS consent rate is {sms_rate:.1%} — below the 15% benchmark for growing programs.",
            "Under-penetration limits SMS revenue. Most brands can grow SMS list to 20–40% of email list within 6 months.",
            "A/B test SMS-first signup forms. Add SMS upsell to post-purchase emails.",
            "Medium", "-1 point SMS Adoption",
        ))

    sms_in_flows = any(f.sms_count > 0 for f in acct.live_flows)
    if not sms_in_flows:
        findings.append(_f(
            "SMS-004", "High", "SMS Adoption",
            "SMS is enabled but no live flows include SMS messages.",
            "SMS in flows (especially Abandoned Cart) typically generates 15–25% higher recovery rates than email alone.",
            "Add at least one SMS touchpoint to the Abandoned Cart and Welcome flows within 30 days.",
            "High", "-2 points SMS Adoption",
        ))

    if acct.campaigns.sms_campaigns == 0:
        findings.append(_f(
            "SMS-005", "Medium", "SMS Adoption",
            "No SMS campaigns sent during the audit period.",
            "SMS campaigns generate 5–10x higher CTR than email campaigns on average.",
            "Schedule at least one SMS campaign per month. Start with promotional offers to engaged SMS subscribers.",
            "Medium",
        ))

    # Only fire SMS form finding if we actually have form data
    if acct.active_forms:
        sms_form = any(f.collects_sms for f in acct.active_forms)
        if not sms_form:
            findings.append(_f(
                "SMS-006", "Medium", "SMS Adoption",
                "No active signup form collects SMS consent.",
                "SMS list growth stalls without a capture mechanism at the top of the funnel.",
                "Update at least one popup form to offer SMS opt-in alongside email. Test a dual-channel incentive.",
                "Medium",
            ))

    return findings


# ── campaign rules ─────────────────────────────────────────────────────────

def _rules_campaigns(acct: AccountData) -> List[Finding]:
    findings: List[Finding] = []
    c = acct.campaigns

    if c.campaigns_per_week < 0.5:
        findings.append(_f(
            "CAMP-001", "High", "Campaign Strategy",
            f"Campaign frequency is only {c.campaigns_per_week:.1f} per week — below the 1/week minimum for active programs.",
            "Infrequent campaigns leave revenue on the table and reduce subscriber engagement over time.",
            "Increase email campaign frequency to at least 1 per week. Build a monthly editorial calendar.",
            "High", "-3 points Campaign Strategy",
        ))
    elif c.campaigns_per_week > 7:
        findings.append(_f(
            "CAMP-002", "Medium", "Campaign Strategy",
            f"Campaign frequency is {c.campaigns_per_week:.1f} per week — potential over-sending risk.",
            "Over-sending drives unsubscribes, spam complaints, and list fatigue.",
            "Audit which segments receive daily sends. Limit broad-list sends to 3–4 per week max.",
            "Medium", "-2 points Campaign Strategy",
        ))

    if c.pct_to_engaged_segments < 0.25:
        findings.append(_f(
            "CAMP-003", "Critical", "Campaign Strategy",
            f"Only {c.pct_to_engaged_segments:.0%} of campaigns are sent to engaged segments — the vast majority go to the full list.",
            "Sending to unengaged subscribers dramatically increases bounce and spam rates, damaging sender reputation.",
            "Immediately shift to segmented sends. Create an engaged 90-day segment and target it for all campaigns.",
            "Critical", "-2 points Campaign Strategy",
        ))
    elif c.pct_to_engaged_segments < 0.50:
        findings.append(_f(
            "CAMP-004", "High", "Campaign Strategy",
            f"Only {c.pct_to_engaged_segments:.0%} of campaigns target engaged segments — below the 50% benchmark.",
            "Sending to unengaged profiles inflates complaint rates and suppresses deliverability.",
            "Increase engaged-segment targeting to 75%+ of campaigns within 60 days.",
            "High", "-1 point Campaign Strategy",
        ))

    if c.avg_open_rate < 0.15:
        findings.append(_f(
            "CAMP-005", "High", "Campaign Strategy",
            f"Average campaign open rate is {c.avg_open_rate:.1%} — below the 15% critical threshold.",
            "Low open rates signal list hygiene issues, deliverability problems, or weak subject lines.",
            "Audit list health, suppress non-openers (180+ days), and A/B test subject lines.",
            "High",
        ))

    if c.avg_spam_complaint_rate >= 0.001:
        findings.append(_f(
            "CAMP-006", "Critical", "Campaign Strategy",
            f"Campaign spam complaint rate is {c.avg_spam_complaint_rate:.3%} — above Google/Yahoo's 0.1% threshold.",
            "Exceeding 0.1% spam complaints risks Gmail bulk folder placement or sending suspension.",
            "Stop broad list sends immediately. Clean the list to engaged subscribers only. Review unsubscribe flow.",
            "Critical",
        ))

    if c.avg_hard_bounce_rate >= 0.01:
        findings.append(_f(
            "CAMP-007", "High", "Campaign Strategy",
            f"Campaign hard bounce rate is {c.avg_hard_bounce_rate:.2%} — above the 1% action threshold.",
            "High bounce rates signal list quality issues and damage sender reputation.",
            "Remove hard bounces immediately. Run a list verification service on the entire database.",
            "High",
        ))

    if c.longest_gap_days > 30:
        findings.append(_f(
            "CAMP-008", "Medium", "Campaign Strategy",
            f"Longest campaign gap was {c.longest_gap_days} days — subscribers went more than a month without communication.",
            "Extended silence increases unsubscribe rates when communication resumes and reduces brand recall.",
            "Create a minimum-viable send calendar to maintain at least bi-weekly contact.",
            "Medium",
        ))

    return findings


# ── deliverability rules ───────────────────────────────────────────────────

def _rules_deliverability(acct: AccountData) -> List[Finding]:
    findings: List[Finding] = []
    d = acct.deliverability

    if d.hard_bounce_rate >= 0.02:
        findings.append(_f(
            "DELV-001", "Critical", "Deliverability",
            f"Hard bounce rate is {d.hard_bounce_rate:.2%} — above the 2% critical threshold.",
            "ISPs interpret persistent hard bounces as evidence of poor list hygiene, leading to inbox placement loss.",
            "Halt sends to any segment with high bounce concentration. Run full list through email verification service immediately.",
            "Critical", "-5 points Deliverability",
        ))
    elif d.hard_bounce_rate >= 0.01:
        findings.append(_f(
            "DELV-002", "High", "Deliverability",
            f"Hard bounce rate is {d.hard_bounce_rate:.2%} — above the 1% concern threshold.",
            "Bounce accumulation degrades sender reputation and risks ISP filtering.",
            "Review acquisition sources for invalid address entry. Clean the list using a verification service.",
            "High", "-3 points Deliverability",
        ))

    if d.spam_complaint_rate >= 0.001:
        findings.append(_f(
            "DELV-003", "Critical", "Deliverability",
            f"Spam complaint rate is {d.spam_complaint_rate:.3%} — above the 0.1% critical threshold.",
            "Gmail and Yahoo will route all email to spam or block sending if complaint rates exceed 0.1%.",
            "Immediately switch to engaged-only sends. Review unsubscribe process for friction. Suppress all complainers.",
            "Critical", "-5 points Deliverability",
        ))
    elif d.spam_complaint_rate >= 0.0008:
        findings.append(_f(
            "DELV-004", "High", "Deliverability",
            f"Spam complaint rate is {d.spam_complaint_rate:.3%} — approaching the 0.1% Google threshold.",
            "Rising spam complaints are an early warning of deliverability degradation.",
            "Tighten segmentation, reduce frequency to unengaged subscribers, and review content relevance.",
            "High",
        ))

    if not d.has_dkim:
        findings.append(_f(
            "DELV-005", "Critical", "Deliverability",
            "DKIM is not configured for this sending domain.",
            "Without DKIM, emails fail authentication checks — ISPs are more likely to filter or reject them.",
            "Configure DKIM in Klaviyo (Settings → Email → Sending Domain) immediately. Required by Google/Yahoo.",
            "Critical", "-2 points Deliverability",
        ))

    if not d.has_spf:
        findings.append(_f(
            "DELV-006", "High", "Deliverability",
            "SPF record is not configured for this sending domain.",
            "Missing SPF increases the likelihood of email spoofing and ISP filtering.",
            "Add the Klaviyo SPF record to your DNS configuration.",
            "High", "-1 point Deliverability",
        ))

    if not d.has_dmarc:
        findings.append(_f(
            "DELV-007", "High", "Deliverability",
            "DMARC policy is not configured.",
            "DMARC is required by Google and Yahoo for bulk senders. Absence risks delivery issues.",
            "Implement a DMARC record (p=none initially) and monitor alignment. Escalate to p=quarantine within 60 days.",
            "High", "-1 point Deliverability",
        ))

    if not d.has_branded_sending_domain:
        findings.append(_f(
            "DELV-008", "Medium", "Deliverability",
            "Email is sent from a shared Klaviyo domain rather than a branded sending domain.",
            "Shared domains carry reputation risk from other senders. Branded domains improve deliverability and brand trust.",
            "Set up a dedicated sending subdomain (e.g., mail.yourbrand.com) in Klaviyo.",
            "Medium", "-1 point Deliverability",
        ))

    if d.avg_unsubscribe_rate >= 0.005:
        findings.append(_f(
            "DELV-009", "High", "Deliverability",
            f"Average unsubscribe rate is {d.avg_unsubscribe_rate:.2%} — above the 0.5% concern threshold.",
            "High unsubscribe rates erode list size and signal content/frequency mismatch.",
            "Survey recent unsubscribers. Audit send frequency and content relevance. Implement preference center.",
            "High", "-2 points Deliverability",
        ))

    return findings


# ── core flow rules ────────────────────────────────────────────────────────

def _rules_flows(acct: AccountData) -> List[Finding]:
    findings: List[Finding] = []

    welcome = acct.get_flow("welcome")
    if not welcome:
        findings.append(_f(
            "FLOW-001", "Critical", "Core Flows",
            "No Welcome Series flow is live.",
            "The Welcome flow is the highest-ROI automation — new subscribers are most engaged in their first 48 hours.",
            "Build a 3–5 email Welcome Series. First email within 5 minutes of signup. Include brand story, best sellers, and a first-purchase incentive.",
            "Critical", "-cap Core Flow Coverage to 4/10",
        ))
    else:
        if welcome.first_message_delay_minutes > 60:
            findings.append(_f(
                "FLOW-002", "High", "Core Flows",
                f"Welcome flow first email is delayed {welcome.first_message_delay_minutes} minutes (>{60}min threshold).",
                "Engagement rates drop sharply if the welcome email arrives more than an hour after signup.",
                "Move the first welcome email to within 5 minutes of signup trigger.",
                "High", "-2 points Flow Configuration",
            ))
        if welcome.email_count < 3:
            findings.append(_f(
                "FLOW-003", "Medium", "Core Flows",
                f"Welcome flow has only {welcome.email_count} email(s) — less than the 3-email minimum for an effective series.",
                "A single welcome email misses the opportunity to educate, inspire, and convert.",
                "Expand the Welcome Series to at least 3 emails: (1) Brand intro, (2) Best sellers or social proof, (3) First-purchase offer.",
                "Medium",
            ))

    ac = acct.get_flow("abandoned_cart")
    if not ac:
        findings.append(_f(
            "FLOW-004", "Critical", "Core Flows",
            "No Abandoned Cart flow is live.",
            "Abandoned cart recovery is typically the single highest-revenue automation, averaging 5–15% cart recovery.",
            "Build a 3-part Abandoned Cart flow: (1) Reminder at 1 hour, (2) Social proof/urgency at 24 hours, (3) Discount at 48 hours.",
            "Critical", "-cap Core Flow Coverage to 4/10",
        ))
    else:
        if ac.email_count < 2:
            findings.append(_f(
                "FLOW-005", "High", "Core Flows",
                f"Abandoned Cart flow has only {ac.email_count} email(s) — single-touch recovery is suboptimal.",
                "Multi-touch cart recovery generates 2–3x more revenue than a single reminder.",
                "Add a second email (24h) and consider a third (48–72h) with an incentive.",
                "High",
            ))
        if not ac.has_incentive:
            findings.append(_f(
                "FLOW-006", "Medium", "Core Flows",
                "Abandoned Cart flow does not include a discount or incentive.",
                "Adding an incentive to the final cart recovery email typically increases recovery rate by 20–40%.",
                "Add a time-limited discount code (10–15%) to the final abandoned cart email.",
                "Medium",
            ))

    ba = acct.get_flow("browse_abandonment")
    if not ba:
        findings.append(_f(
            "FLOW-007", "High", "Core Flows",
            "No Browse Abandonment flow is live.",
            "Browse abandonment flows target high-intent visitors before they leave — typically 2–5% conversion.",
            "Build a 2-email Browse Abandonment flow triggered by Viewed Product event. Send first email within 1 hour.",
            "High",
        ))

    pp = acct.get_flow("post_purchase")
    if not pp:
        findings.append(_f(
            "FLOW-008", "High", "Core Flows",
            "No Post-Purchase flow is live.",
            "Post-purchase flows drive repeat purchases, reduce refund rates, and build brand loyalty.",
            "Build a Post-Purchase flow: (1) Order confirmation + thank you, (2) Product education/tips, (3) Related products upsell, (4) Review request.",
            "High",
        ))

    wb = acct.get_flow("winback")
    if not wb:
        findings.append(_f(
            "FLOW-009", "Medium", "Core Flows",
            "No Winback / Re-engagement flow is live.",
            f"With {acct.profiles.dormant_rate:.0%} of the list dormant, a winback flow is essential for list hygiene and revenue recovery.",
            "Build a Winback flow for subscribers inactive 90+ days. 3-email sequence with a final 'last chance' offer before sunset.",
            "Medium",
        ))

    atc = acct.get_flow("added_to_cart")
    if not atc:
        findings.append(_f(
            "FLOW-010", "Medium", "Core Flows",
            "No Added to Cart flow is live.",
            "Added-to-cart triggers capture intent before checkout — higher conversion than browse abandonment alone.",
            "Build an Added to Cart flow triggered by the Added to Cart Klaviyo metric. Separate from Abandoned Checkout.",
            "Medium",
        ))

    # Stale flows
    stale = [f for f in acct.live_flows if f.last_updated_days_ago > 365]
    for flow in stale:
        findings.append(_f(
            "FLOW-011", "Low", "Core Flows",
            f"Flow '{flow.name}' has not been updated in {flow.last_updated_days_ago} days.",
            "Stale flows may reference outdated offers, expired coupons, or discontinued products.",
            f"Review and refresh the '{flow.name}' flow content, subject lines, and any coupon codes.",
            "Low", confidence="Confirmed",
        ))

    return findings


# ── form rules ─────────────────────────────────────────────────────────────

def _rules_forms(acct: AccountData) -> List[Finding]:
    findings: List[Finding] = []
    forms = acct.active_forms

    if not forms:
        # Forms endpoint unavailable in current Klaviyo API revision —
        # cannot confirm or deny form presence. Suppress this finding.
        return findings

    primary = acct.primary_form
    if primary:
        opt_in = primary.opt_in_rate
        if opt_in < 0.01:
            findings.append(_f(
                "FORM-002", "Critical", "Signup Forms",
                f"Primary signup form opt-in rate is {opt_in:.2%} — below the 1% critical floor.",
                "A sub-1% opt-in rate indicates the form is poorly positioned, timed, or lacks an incentive.",
                "Redesign the form: test a compelling incentive (10–15% off), improved copy, and better display timing.",
                "Critical", "-cap Signup Forms to 3/10",
            ))
        elif opt_in < 0.02:
            findings.append(_f(
                "FORM-003", "High", "Signup Forms",
                f"Primary form opt-in rate is {opt_in:.2%} — below the 2% benchmark.",
                "Below-average opt-in rates slow list growth and increase cost per subscriber.",
                "A/B test the form headline, CTA button copy, and incentive offer. Aim for 2–4% opt-in.",
                "High",
            ))

        mob_rate = primary.mobile_opt_in_rate
        if primary.mobile_views > 0 and mob_rate < primary.opt_in_rate * 0.5:
            findings.append(_f(
                "FORM-004", "Medium", "Signup Forms",
                f"Mobile opt-in rate ({mob_rate:.2%}) is less than half the desktop rate — form is not mobile-optimized.",
                "More than 60% of ecommerce traffic is mobile. A broken mobile form cuts list growth in half.",
                "Redesign the form for mobile: single-field, large CTA button, no image, fast-loading.",
                "Medium",
            ))

        if not primary.has_incentive:
            findings.append(_f(
                "FORM-005", "Medium", "Signup Forms",
                "Primary signup form does not offer an incentive.",
                "Incentivized forms typically convert at 2–3x the rate of non-incentivized forms.",
                "Add a first-purchase discount (10–15%) or free shipping offer as the signup incentive.",
                "Medium",
            ))

    if acct.sms_enabled and not any(f.collects_sms for f in forms):
        findings.append(_f(
            "FORM-006", "High", "Signup Forms",
            "SMS is enabled but no active form collects SMS opt-in.",
            "Without SMS capture in the signup flow, SMS list growth is near-zero.",
            "Add SMS opt-in to the primary popup form. Test a dedicated SMS-first form with a text-to-join offer.",
            "High",
        ))

    return findings


# ── list health rules ──────────────────────────────────────────────────────

def _rules_list_health(acct: AccountData) -> List[Finding]:
    findings: List[Finding] = []
    p = acct.profiles

    if p.emailable_profiles == 0:
        return findings

    if p.suppression_rate >= 0.20:
        findings.append(_f(
            "LIST-001", "Critical", "List Health",
            f"Suppression rate is {p.suppression_rate:.1%} — over 20% of total profiles are suppressed.",
            "High suppression inflates billing costs (suppressed profiles count toward plan limits) and signals historical deliverability damage.",
            "Audit suppression causes (bounces vs. unsubscribes vs. spam). Consider cleaning suppressed profiles older than 12 months.",
            "Critical",
        ))
    elif p.suppression_rate >= 0.10:
        findings.append(_f(
            "LIST-002", "High", "List Health",
            f"Suppression rate is {p.suppression_rate:.1%} — above the 10% concern threshold.",
            "A growing suppression rate indicates ongoing deliverability issues or acquisition quality problems.",
            "Review suppression growth trend. Audit acquisition sources adding invalid or spam-trap addresses.",
            "High",
        ))

    if p.dormant_rate >= 0.60:
        findings.append(_f(
            "LIST-003", "Critical", "List Health",
            f"Dormant profile rate is {p.dormant_rate:.1%} — more than 60% of emailable profiles have not engaged in 180 days.",
            f"Sending to {p.dormant_profiles:,} dormant profiles damages deliverability and wastes budget.",
            "Immediately suppress all sends to 180+ day non-engagers. Run a winback campaign before final suppression.",
            "Critical",
        ))
    elif p.dormant_rate >= 0.40:
        findings.append(_f(
            "LIST-004", "High", "List Health",
            f"Dormant rate is {p.dormant_rate:.1%} — a large portion of the list is cold.",
            "Cold profiles inflate list size metrics without contributing to engagement or revenue.",
            "Launch a re-engagement campaign for 90–180 day non-openers. Suppress those who don't respond.",
            "High",
        ))

    if p.engaged_30_pct < 0.05:
        findings.append(_f(
            "LIST-005", "High", "List Health",
            f"Only {p.engaged_30_pct:.1%} of emailable profiles opened in the last 30 days.",
            "A tiny active segment indicates broad-list sending practices and deliverability degradation.",
            "Shift all campaigns to engaged segments (30/60/90 day). Stop sending to the full list immediately.",
            "High",
        ))

    return findings


# ── segmentation rules ─────────────────────────────────────────────────────

def _rules_segmentation(acct: AccountData) -> List[Finding]:
    findings: List[Finding] = []
    s = acct.segmentation

    if not s.has_engaged_30_segment:
        findings.append(_f(
            "SEG-001", "High", "Segmentation",
            "No engaged 30-day segment exists.",
            "The 30-day engaged segment is the foundation for high-performance campaigns — essential for deliverability protection.",
            "Create a segment: 'Opened or clicked email in last 30 days.' Use for all high-priority campaigns.",
            "High",
        ))

    if not s.has_engaged_90_segment:
        findings.append(_f(
            "SEG-002", "Medium", "Segmentation",
            "No engaged 90-day segment exists.",
            "Without a 90-day segment, campaigns cannot be tiered by engagement level.",
            "Create a segment: 'Opened or clicked email in last 90 days.' Use for standard campaigns.",
            "Medium",
        ))

    if not s.has_vip_segment:
        findings.append(_f(
            "SEG-003", "Medium", "Segmentation",
            "No VIP or high-value customer segment exists.",
            "Top customers generate disproportionate revenue — they deserve differentiated treatment.",
            "Create a VIP segment based on purchase frequency or LTV (e.g., 3+ orders or top 10% by revenue).",
            "Medium",
        ))

    if not s.has_sunset_segment:
        findings.append(_f(
            "SEG-004", "Medium", "Segmentation",
            "No sunset / list hygiene segment exists.",
            "Without a sunset segment, inactive subscribers accumulate and drag down engagement metrics.",
            "Create a sunset segment: 'No email open in 180+ days.' Run a final re-engagement campaign, then suppress.",
            "Medium",
        ))

    if s.pct_campaigns_to_engaged < 0.25:
        findings.append(_f(
            "SEG-005", "Critical", "Segmentation",
            f"Only {s.pct_campaigns_to_engaged:.0%} of campaigns target engaged segments — most sends go to the full list.",
            "Full-list sending devastates deliverability and wastes budget on subscribers who will never convert.",
            "Mandate engaged-segment targeting for all campaigns. Create SOPs preventing full-list sends without approval.",
            "Critical",
        ))

    return findings


# ── revenue rules ──────────────────────────────────────────────────────────

def _rules_revenue(acct: AccountData) -> List[Finding]:
    findings: List[Finding] = []
    r = acct.revenue

    if not r.revenue_attribution_configured:
        findings.append(_f(
            "REV-001", "Critical", "Revenue Attribution",
            "Revenue attribution is not configured in Klaviyo.",
            "Without attribution, it's impossible to measure email/SMS ROI or optimize for revenue.",
            "Connect your ecommerce platform to Klaviyo and configure the Placed Order metric. Verify conversion tracking is firing.",
            "Critical", "-cap Revenue Attribution to 2/10",
        ))
        return findings

    if not acct.ecommerce_events_configured:
        findings.append(_f(
            "REV-002", "High", "Revenue Attribution",
            "Ecommerce events are not fully configured.",
            "Missing events (Add to Cart, Checkout Started, etc.) limits automation trigger capabilities and attribution accuracy.",
            "Audit which Klaviyo ecommerce events are firing. Install the Klaviyo tracking snippet or verify Shopify app installation.",
            "High",
        ))

    if r.total_klaviyo_revenue > 0 and r.flow_revenue_pct < 0.20:
        findings.append(_f(
            "REV-003", "High", "Revenue Attribution",
            f"Flows contribute only {r.flow_revenue_pct:.0%} of Klaviyo revenue — significantly below the 40–60% benchmark.",
            "Flow revenue is 'always-on' revenue. Under-contribution means core automations are missing or underperforming.",
            "Audit which flows are missing. Prioritize building Abandoned Cart and Welcome flows to shift flow revenue to 40%+.",
            "High",
        ))

    b = r.benchmarks
    if b.open_rate_rating in ("poor", "below_average"):
        findings.append(_f(
            "REV-004", "Medium", "Revenue Attribution",
            f"Open rate benchmark rating is '{b.open_rate_rating}' — below industry average.",
            "Below-average open rates compress revenue per campaign and signal content or deliverability issues.",
            "A/B test subject lines, preview text, and send times. Move to engaged-segment sends only.",
            "Medium",
        ))

    return findings


# ── billing rules ──────────────────────────────────────────────────────────

def _rules_billing(acct: AccountData) -> List[Finding]:
    findings: List[Finding] = []
    b = acct.billing
    p = acct.profiles

    if b.plan_profile_limit > 0:
        utilization = p.total_profiles / b.plan_profile_limit
        if utilization >= 0.95:
            findings.append(_f(
                "BILL-001", "High", "Billing",
                f"Profile count ({p.total_profiles:,}) is at {utilization:.0%} of the plan limit ({b.plan_profile_limit:,}).",
                "Exceeding the plan limit triggers automatic Klaviyo billing upgrades or account throttling.",
                "Suppress or delete unengaged profiles to reduce billable count before hitting the limit.",
                "High",
            ))
        elif utilization < 0.40:
            findings.append(_f(
                "BILL-002", "Low", "Billing",
                f"Profile utilization is only {utilization:.0%} — this account may be on an oversized plan.",
                "Overpaying for profile capacity that isn't being used represents unnecessary cost.",
                "Review Klaviyo plan options. If list growth is not projected, consider a lower-tier plan.",
                "Low",
            ))

        if p.suppression_rate >= 0.15:
            findings.append(_f(
                "BILL-003", "Medium", "Billing",
                f"High suppression rate ({p.suppression_rate:.1%}) is inflating the billable profile count.",
                "Suppressed profiles still count toward Klaviyo billing in most plans.",
                "Regularly purge hard-bounced and long-term suppressed profiles (12+ months) to reduce billable count.",
                "Medium",
            ))

    return findings


# ── compliance rules ───────────────────────────────────────────────────────

def _rules_compliance(acct: AccountData) -> List[Finding]:
    findings: List[Finding] = []
    d = acct.deliverability

    if not d.has_dmarc:
        findings.append(_f(
            "COMP-001", "High", "Compliance",
            "DMARC is not configured — required by Google and Yahoo for bulk senders as of 2024.",
            "Failure to comply with Google/Yahoo authentication requirements (SPF, DKIM, DMARC) risks email delivery.",
            "Implement DMARC immediately. Start with p=none for monitoring, escalate to p=quarantine within 60 days.",
            "High", confidence="Confirmed",
        ))

    if acct.sms_enabled and acct.profiles.sms_consent_rate < 0.01:
        findings.append(_f(
            "COMP-002", "High", "Compliance",
            "SMS is enabled with very low consent rates — possible TCPA compliance risk.",
            "Sending SMS to profiles without documented consent is a TCPA violation risk.",
            "Audit SMS consent records. Ensure all SMS subscribers opted in via a compliant double opt-in flow. "
            "This is a risk flag for further review — consult legal counsel.",
            "High", confidence="Inferred",
        ))

    return findings


# ── main entry point ───────────────────────────────────────────────────────

def run_rules(acct: AccountData) -> List[Finding]:
    """Run all rule sections and return a combined list of findings, sorted by severity."""
    all_findings: List[Finding] = []
    rule_sections = [
        _rules_sms,
        _rules_campaigns,
        _rules_deliverability,
        _rules_flows,
        _rules_forms,
        _rules_list_health,
        _rules_segmentation,
        _rules_revenue,
        _rules_billing,
        _rules_compliance,
    ]
    for section in rule_sections:
        all_findings.extend(section(acct))

    severity_order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
    all_findings.sort(key=lambda f: severity_order.get(f.severity, 99))
    return all_findings
