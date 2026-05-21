"""
Klaviyo Audit Katie — Recommendation Engine
Converts findings into deduplicated, prioritized Recommendation objects.
Priority score formula: (Revenue Impact × 3) + (Deliverability Impact × 2) + (Effort Inverse × 1)
"""
from __future__ import annotations
from typing import List, Dict
from .models import Finding, Recommendation


# ── recommendation catalog ─────────────────────────────────────────────────
# Keyed by rule_id. Each entry defines the consolidated recommendation
# that maps to one or more source findings.

_CATALOG: Dict[str, dict] = {
    "SMS-001": dict(
        rec_id="REC-SMS-001",
        issue="SMS is not enabled — this revenue channel is completely untapped.",
        why_it_matters="Email + SMS programs generate 20–30% more revenue than email alone. Abandoning SMS is abandoning a full revenue channel.",
        expected_impact="High",
        complexity="Moderate",
        priority="High",
        owner="Shared",
        timeline="30 days",
        opportunity_note="Enabling SMS and adding it to core flows could add a meaningful incremental revenue stream within 60–90 days.",
        next_step="Enable SMS in Klaviyo Settings → SMS. Add SMS opt-in to the primary signup form. Build a Welcome SMS within 30 days.",
    ),
    "SMS-002": dict(
        rec_id="REC-SMS-002",
        issue="SMS consent rate is critically low — the SMS list is too small to drive meaningful revenue.",
        why_it_matters="Small SMS lists limit ROI. Growing to 15–25% of the email list is achievable within 6 months with focused acquisition.",
        expected_impact="Medium",
        complexity="Easy",
        priority="High",
        owner="Shared",
        timeline="30 days",
        opportunity_note="Improving SMS consent rate to 15%+ of the email list typically adds 8–15% incremental attributed revenue.",
        next_step="Add SMS opt-in to all active signup forms. A/B test a dual-channel incentive. Run an SMS acquisition campaign to existing email subscribers.",
    ),
    "SMS-004": dict(
        rec_id="REC-SMS-004",
        issue="SMS is not used in any live flows.",
        why_it_matters="SMS in flows (especially Abandoned Cart) increases recovery rate by 15–25% over email alone.",
        expected_impact="High",
        complexity="Easy",
        priority="High",
        owner="Shared",
        timeline="30 days",
        opportunity_note="Adding one SMS touchpoint to the Abandoned Cart flow alone can generate meaningful monthly revenue lift.",
        next_step="Add an SMS message 30–60 minutes after the abandoned cart trigger, before the first email.",
    ),
    "CAMP-001": dict(
        rec_id="REC-CAMP-001",
        issue="Campaign frequency is too low — the list is under-monetized.",
        why_it_matters="Consistent weekly campaigns are the baseline of email revenue. Sub-weekly sending leaves predictable revenue unrealized.",
        expected_impact="High",
        complexity="Easy",
        priority="High",
        owner="Shared",
        timeline="30 days",
        opportunity_note="Increasing to 1–2 campaigns per week for engaged segments could substantially lift campaign revenue.",
        next_step="Build a 4-week editorial calendar. Prioritize promotional and educational content. Send to engaged segments only.",
    ),
    "CAMP-003": dict(
        rec_id="REC-CAMP-003",
        issue="Campaigns are sent to the full list rather than engaged segments.",
        why_it_matters="Full-list sends damage deliverability, suppress open rates, and inflate complaint rates — a compounding problem.",
        expected_impact="High",
        complexity="Easy",
        priority="Critical",
        owner="Shared",
        timeline="Immediate",
        opportunity_note="Shifting to engaged-segment sends will improve open rates, reduce complaints, and protect sender reputation.",
        next_step="Create engaged 30/90/180-day segments immediately. Mandate that all campaigns target one of these segments.",
    ),
    "DELV-001": dict(
        rec_id="REC-DELV-001",
        issue="Hard bounce rate is critically high — sender reputation is at risk.",
        why_it_matters="ISPs blacklist senders with persistent high bounce rates. Deliverability damage is slow to recover.",
        expected_impact="High",
        complexity="Moderate",
        priority="Critical",
        owner="Shared",
        timeline="Immediate",
        opportunity_note="Fixing bounce rates is a prerequisite for all other revenue opportunities. Damaged deliverability makes every send less effective.",
        next_step="Run full list through ZeroBounce or NeverBounce immediately. Remove all hard bounces. Audit acquisition sources.",
    ),
    "DELV-003": dict(
        rec_id="REC-DELV-003",
        issue="Spam complaint rate exceeds Google's 0.1% threshold — inbox placement is at risk.",
        why_it_matters="Gmail routes email to spam or blocks senders who exceed 0.1% complaint rates. This affects all subscribers, not just complainers.",
        expected_impact="High",
        complexity="Moderate",
        priority="Critical",
        owner="Shared",
        timeline="Immediate",
        opportunity_note="Resolving deliverability issues is the highest-leverage action — every other optimization depends on landing in the inbox.",
        next_step="Switch immediately to engaged-only sends (30-day openers). Add one-click unsubscribe. Review list acquisition quality.",
    ),
    "DELV-005": dict(
        rec_id="REC-DELV-005",
        issue="DKIM authentication is missing — emails fail authentication checks.",
        why_it_matters="Google and Yahoo require DKIM for bulk senders. Missing DKIM risks filtering or rejection.",
        expected_impact="High",
        complexity="Easy",
        priority="Critical",
        owner="Shared",
        timeline="Immediate",
        opportunity_note="Authentication is table stakes — all other improvements depend on emails reaching the inbox.",
        next_step="Configure DKIM in Klaviyo (Settings → Email → Sending Domain). Verify DNS propagation within 48 hours.",
    ),
    "DELV-007": dict(
        rec_id="REC-DELV-007",
        issue="DMARC policy is missing — required by Google/Yahoo for bulk senders.",
        why_it_matters="DMARC protects against spoofing and is now a requirement for bulk email delivery.",
        expected_impact="High",
        complexity="Easy",
        priority="High",
        owner="Client",
        timeline="Immediate",
        opportunity_note="DMARC configuration is a one-time DNS change with permanent deliverability benefits.",
        next_step="Add a DMARC TXT record to DNS (p=none initially). Monitor alignment reports. Escalate to p=quarantine in 30 days.",
    ),
    "FLOW-001": dict(
        rec_id="REC-FLOW-001",
        issue="No Welcome Series flow exists — the highest-ROI automation is missing.",
        why_it_matters="New subscribers are most engaged in their first 48 hours. A Welcome Series converts more first-time buyers than any other flow.",
        expected_impact="High",
        complexity="Moderate",
        priority="Critical",
        owner="Shared",
        timeline="Immediate",
        opportunity_note="A 3-email Welcome Series typically drives 15–25% of all flow revenue in mature Klaviyo accounts.",
        next_step="Build a 3–5 email Welcome Series triggered on List Subscribe. Email 1: within 5 minutes. Include brand story, bestsellers, and a welcome discount.",
    ),
    "FLOW-004": dict(
        rec_id="REC-FLOW-004",
        issue="No Abandoned Cart flow exists — the highest-recovery automation is missing.",
        why_it_matters="Abandoned cart flows recover 5–15% of abandoned carts and are typically the top revenue-generating automation.",
        expected_impact="High",
        complexity="Moderate",
        priority="Critical",
        owner="Shared",
        timeline="Immediate",
        opportunity_note="Brands without an abandoned cart flow are leaving significant monthly revenue unrealized.",
        next_step="Build a 3-email Abandoned Cart flow: (1) 1-hour reminder, (2) 24-hour social proof, (3) 48-hour discount. Add SMS at step 1.",
    ),
    "FLOW-007": dict(
        rec_id="REC-FLOW-007",
        issue="No Browse Abandonment flow exists.",
        why_it_matters="Browse abandonment captures high-intent visitors before they leave — typically 2–5% conversion.",
        expected_impact="Medium",
        complexity="Easy",
        priority="High",
        owner="Shared",
        timeline="30 days",
        opportunity_note="Browse abandonment flows generate incremental revenue without cannibalizing cart recovery.",
        next_step="Build a 2-email Browse Abandonment flow triggered by Viewed Product. First email within 1 hour. Second email at 24 hours.",
    ),
    "FLOW-008": dict(
        rec_id="REC-FLOW-008",
        issue="No Post-Purchase flow exists.",
        why_it_matters="Post-purchase flows are the highest-ROI retention automation — they drive repeat purchases and reduce refund rates.",
        expected_impact="Medium",
        complexity="Moderate",
        priority="High",
        owner="Shared",
        timeline="30 days",
        opportunity_note="Post-purchase flows typically increase repeat purchase rate by 10–20% in the 60 days following a first order.",
        next_step="Build a 4-step Post-Purchase flow: (1) Thank you, (2) Product tips, (3) Related products, (4) Review request (day 14).",
    ),
    "FLOW-009": dict(
        rec_id="REC-FLOW-009",
        issue="No Winback flow exists — dormant subscribers are not being re-engaged.",
        why_it_matters="Even a 5–10% winback rate from a large dormant segment can generate meaningful revenue.",
        expected_impact="Medium",
        complexity="Moderate",
        priority="Medium",
        owner="Shared",
        timeline="60 days",
        opportunity_note="Winback flows also improve list hygiene by identifying who truly cannot be re-engaged.",
        next_step="Build a 3-email Winback flow for 90+ day non-openers. Final email: 'This is goodbye' with a strong incentive.",
    ),
    "FORM-001": dict(
        rec_id="REC-FORM-001",
        issue="No active signup forms — list growth is not happening.",
        why_it_matters="A list that doesn't grow shrinks. Without forms, every subscriber who unsubscribes is a permanent loss.",
        expected_impact="High",
        complexity="Easy",
        priority="Critical",
        owner="Shared",
        timeline="Immediate",
        opportunity_note="Adding a high-converting popup (3–5% opt-in) can add hundreds to thousands of new subscribers per month.",
        next_step="Create a popup form in Klaviyo with a compelling offer (10–15% off or free shipping). Publish on all pages except checkout.",
    ),
    "FORM-002": dict(
        rec_id="REC-FORM-002",
        issue="Signup form opt-in rate is below 1% — the form is not converting.",
        why_it_matters="A sub-1% opt-in rate means 99%+ of site visitors who could become email subscribers are not captured.",
        expected_impact="High",
        complexity="Easy",
        priority="High",
        owner="Shared",
        timeline="30 days",
        opportunity_note="Improving opt-in rate from <1% to 3% could triple monthly subscriber acquisition at zero additional traffic cost.",
        next_step="Redesign the form: add a clear incentive, rewrite the headline, test exit-intent vs. timed display. A/B test immediately.",
    ),
    "LIST-003": dict(
        rec_id="REC-LIST-003",
        issue="Over 60% of the list is dormant — the majority of emailable profiles are cold.",
        why_it_matters="Sending to dormant subscribers suppresses engagement rates, inflates billing, and damages deliverability.",
        expected_impact="High",
        complexity="Moderate",
        priority="Critical",
        owner="Shared",
        timeline="Immediate",
        opportunity_note="Cleaning the list improves all engagement metrics, reduces billing costs, and protects sender reputation.",
        next_step="Immediately stop sending to 180+ day non-openers. Run a 3-email winback campaign. Suppress non-responders permanently.",
    ),
    "SEG-001": dict(
        rec_id="REC-SEG-001",
        issue="No engaged segment infrastructure exists — campaigns cannot be targeted by engagement.",
        why_it_matters="Engagement-based segmentation is the single most impactful deliverability and revenue lever available.",
        expected_impact="High",
        complexity="Easy",
        priority="High",
        owner="NP",
        timeline="Immediate",
        opportunity_note="Creating engagement segments costs nothing and can be done in under 30 minutes — the ROI is immediate.",
        next_step="Create 4 segments: Engaged 30d, Engaged 90d, Engaged 180d, Never Engaged. Use these for all campaign targeting.",
    ),
    "REV-001": dict(
        rec_id="REC-REV-001",
        issue="Revenue attribution is not configured — Klaviyo cannot measure ROI.",
        why_it_matters="Without attribution data, it's impossible to know which emails drive revenue or optimize for conversions.",
        expected_impact="High",
        complexity="Moderate",
        priority="Critical",
        owner="Shared",
        timeline="Immediate",
        opportunity_note="Attribution configuration unlocks revenue reporting across all flows and campaigns — essential for optimization.",
        next_step="Verify Klaviyo ecommerce integration (Shopify app or API). Confirm Placed Order metric is firing. Test with a transaction.",
    ),
}

# Rule IDs that should be collapsed together (merged into one recommendation)
_MERGE_GROUPS = [
    {"DELV-005", "DELV-006", "DELV-007", "DELV-008"},  # → all auth/domain issues → DELV-005 rec
    {"CAMP-003", "CAMP-004"},                            # → segmentation → CAMP-003 rec
    {"SMS-002", "SMS-003"},                              # → SMS growth → SMS-002 rec
    {"LIST-003", "LIST-004"},                            # → dormant → LIST-003 rec
    {"SEG-001", "SEG-002", "SEG-003", "SEG-004", "SEG-005"},  # → all segmentation → SEG-001 rec
]


def _canonical_rule_id(rule_id: str) -> str:
    """Map a rule_id to its canonical recommendation key (handles merge groups)."""
    for group in _MERGE_GROUPS:
        if rule_id in group:
            return sorted(group)[0]  # lowest-sorted ID becomes the canonical
    return rule_id


def _priority_score(entry: dict) -> int:
    impact_map = {"High": 3, "Medium": 2, "Low": 1}
    effort_inverse = {"Easy": 3, "Moderate": 2, "Complex": 1}
    severity_map = {"Critical": 3, "High": 2, "Medium": 1, "Low": 0}
    rev = impact_map.get(entry["expected_impact"], 1)
    delv = severity_map.get(entry.get("delv_impact", "Low"), 0)
    effort = effort_inverse.get(entry["complexity"], 1)
    return rev * 3 + delv * 2 + effort


def build_recommendations(findings: List[Finding]) -> List[Recommendation]:
    """Convert findings into deduplicated, prioritized Recommendation objects."""
    seen_canonical: Dict[str, List[str]] = {}  # canonical_id → list of source rule_ids

    for f in findings:
        canonical = _canonical_rule_id(f.rule_id)
        if canonical not in seen_canonical:
            seen_canonical[canonical] = []
        if f.rule_id not in seen_canonical[canonical]:
            seen_canonical[canonical].append(f.rule_id)

    recs: List[Recommendation] = []
    for canonical, source_rules in seen_canonical.items():
        entry = _CATALOG.get(canonical)
        if not entry:
            continue  # no catalog entry — skip (rules without recommendations are informational)

        # Determine highest severity among source findings
        sev_map = {"Critical": 4, "High": 3, "Medium": 2, "Low": 1}
        max_sev = max(
            (sev_map.get(f.severity, 0) for f in findings if f.rule_id in source_rules),
            default=1,
        )
        sev_labels = {4: "Critical", 3: "High", 2: "Medium", 1: "Low"}
        confidence_vals = [f.confidence for f in findings if f.rule_id in source_rules]
        confidence = "Confirmed" if "Confirmed" in confidence_vals else confidence_vals[0] if confidence_vals else "Confirmed"

        ps = _priority_score(entry)

        recs.append(Recommendation(
            rec_id=entry["rec_id"],
            source_rules=source_rules,
            issue=entry["issue"],
            why_it_matters=entry["why_it_matters"],
            expected_impact=entry["expected_impact"],
            complexity=entry["complexity"],
            priority=entry.get("priority", sev_labels.get(max_sev, "Medium")),
            owner=entry["owner"],
            timeline=entry["timeline"],
            confidence=confidence,
            opportunity_note=entry["opportunity_note"],
            next_step=entry["next_step"],
            priority_score=ps,
        ))

    recs.sort(key=lambda r: -r.priority_score)
    return recs
