# Klaviyo Audit Katie — Decision Rules

**Version:** 1.0
**Owner:** National Positions
**Classification:** Internal Operating Framework — Phase 1
**Last Updated:** 2026-05-10

---

## Overview

This document defines the rule-based logic that governs Katie's audit findings and recommendations. Each rule specifies a trigger condition, severity level, business impact, recommended action, priority, score impact, and confidence guidance.

Rules are organized by audit category. All rules apply to ecommerce accounts unless labeled otherwise.

---

## Rule Format

```
RULE ID: [CATEGORY-###]
Trigger Condition: IF [observable condition]
Severity: [Critical / High / Medium / Low]
Finding: [what this means for the account]
Business Impact: [revenue / deliverability / growth impact]
Action: THEN [specific recommendation]
Suggested Priority: [Critical / High / Medium / Low]
Score Impact: [e.g., caps Flow Coverage at 4/10]
Confidence: [Confirmed / Likely / Inferred]
Notes: [edge cases or conditions that modify the rule]
```

---

## Section 1 — SMS Rules (SMS-001 through SMS-015)

---

**RULE ID: SMS-001**
**Trigger Condition:** IF SMS is not enabled in the Klaviyo account
**Severity:** Critical
**Finding:** The account has no SMS program. An entire revenue and engagement channel is missing.
**Business Impact:** SMS typically contributes 10–20% of Klaviyo revenue for mature accounts. All of this revenue is currently being missed.
**Action:** THEN flag as a critical missed revenue opportunity. Recommend SMS program launch starting with Klaviyo SMS setup, TCPA compliance review, SMS opt-in on all signup forms, and SMS addition to all core flows.
**Suggested Priority:** Critical
**Score Impact:** SMS category score fixed at 1/10
**Confidence:** Confirmed
**Notes:** Verify SMS is not enabled on a sub-account or connected SMS provider before flagging.

---

**RULE ID: SMS-002**
**Trigger Condition:** IF SMS is enabled but fewer than 5% of emailable profiles have SMS consent
**Severity:** High
**Finding:** SMS is available but the SMS list is critically underdeveloped. The account cannot leverage SMS meaningfully with this small an audience.
**Business Impact:** Low SMS consent limits SMS revenue and reduces the effectiveness of flow automation that relies on SMS steps.
**Action:** THEN recommend SMS list growth strategy: add SMS opt-in to all signup forms, run an SMS list growth campaign to existing email subscribers, add keyboard opt-in language to post-purchase communications.
**Suggested Priority:** High
**Score Impact:** -3 points from SMS category
**Confidence:** Confirmed
**Notes:** 5% threshold is a starting concern; below 2% is near-critical.

---

**RULE ID: SMS-003**
**Trigger Condition:** IF SMS is enabled but fewer than 10% of emailable profiles have SMS consent
**Severity:** Medium
**Finding:** SMS consent rate is below the healthy development threshold. SMS list is growing but not yet mature.
**Business Impact:** Limits SMS revenue and reduces flow SMS impact.
**Action:** THEN recommend adding SMS opt-in to all forms, running SMS capture promotions, and including SMS double opt-in in post-purchase communications.
**Suggested Priority:** High
**Score Impact:** -2 points from SMS category
**Confidence:** Confirmed

---

**RULE ID: SMS-004**
**Trigger Condition:** IF SMS is enabled but no flows contain any SMS messages
**Severity:** High
**Finding:** SMS is available and profiles are consented, but the account is not using SMS in its lifecycle automation. Consented profiles receive no SMS touchpoints through flows.
**Business Impact:** Lost abandonment recovery revenue and lifecycle revenue that SMS touchpoints typically generate.
**Action:** THEN add SMS steps to Welcome, Abandoned Cart, and Browse Abandonment flows at minimum. SMS abandoned cart messages within 1 hour of abandonment are a high-priority recovery tool.
**Suggested Priority:** High
**Score Impact:** -2 points from Flow Configuration Quality; caps SMS to 4/10 if consent rate > 5%
**Confidence:** Confirmed

---

**RULE ID: SMS-005**
**Trigger Condition:** IF SMS is enabled but no SMS campaigns have been sent in the audit period
**Severity:** Medium
**Finding:** SMS-consented profiles are receiving no campaign communications. The SMS channel is underutilized.
**Business Impact:** Missing SMS campaign revenue contribution, which typically adds 5–15% incremental revenue for active senders.
**Action:** THEN launch an SMS campaign cadence — at minimum 1–2 SMS campaigns per month for major promotions, product launches, or flash sales.
**Suggested Priority:** Medium
**Score Impact:** -1 point from SMS category
**Confidence:** Confirmed

---

**RULE ID: SMS-006**
**Trigger Condition:** IF SMS opt-in rate on signup forms is below 30% of the email opt-in rate
**Severity:** Medium
**Finding:** The SMS opt-in field is either not visible, not compelling, or positioned poorly on the signup form. The account is capturing far fewer SMS subscribers than it could.
**Business Impact:** Slow SMS list growth reduces long-term SMS revenue potential.
**Action:** THEN review form design. Test making SMS opt-in more prominent, adding SMS-specific incentive language, and testing a separate SMS opt-in step after email capture.
**Suggested Priority:** Medium
**Score Impact:** -1 point from Signup Forms category
**Confidence:** Confirmed

---

**RULE ID: SMS-007**
**Trigger Condition:** IF SMS consent rate is above 20% of emailable profiles
**Severity:** N/A (Positive Finding)
**Finding:** Strong SMS adoption. The account has a mature SMS list relative to its email audience.
**Business Impact:** Positive — high SMS consent enables strong flow and campaign performance.
**Action:** THEN recognize as a strength. Ensure SMS is fully leveraged in all flows and campaigns.
**Suggested Priority:** Maintain
**Score Impact:** +1 bonus point to SMS category
**Confidence:** Confirmed

---

**RULE ID: SMS-008**
**Trigger Condition:** IF SMS opt-out rate within flows exceeds 3% per message
**Severity:** Medium
**Finding:** Elevated SMS opt-outs in flows indicate SMS messages are being sent at the wrong time, too frequently, or with irrelevant content.
**Business Impact:** Loss of SMS consented profiles reduces long-term SMS revenue.
**Action:** THEN review SMS message timing, frequency, and copy. Ensure SMS messages in flows are concise, relevant, and clearly tied to the trigger action. Avoid sending SMS more than once per flow trigger cycle.
**Suggested Priority:** Medium
**Score Impact:** -1 point from Flow Configuration Quality
**Confidence:** Confirmed

---

**RULE ID: SMS-009**
**Trigger Condition:** IF SMS is not included in the Abandoned Cart flow despite SMS being enabled
**Severity:** High
**Finding:** The highest-revenue flow is missing its highest-urgency channel. SMS abandoned cart messages within 1 hour of cart abandonment are among the highest-converting touchpoints in ecommerce.
**Business Impact:** Estimated 10–30% incremental recovery on carts that would otherwise not convert.
**Action:** THEN add at least 2 SMS messages to the Abandoned Cart flow: one within 60 minutes of abandonment and one 24–48 hours later.
**Suggested Priority:** High
**Score Impact:** -2 points from Flow Configuration Quality
**Confidence:** Confirmed

---

**RULE ID: SMS-010**
**Trigger Condition:** IF SMS is not included in the Welcome flow despite SMS being enabled
**Severity:** Medium
**Finding:** New subscribers who provide SMS consent are not receiving an SMS welcome message. First-impression opportunity is being missed.
**Business Impact:** SMS welcome messages have high open rates and can drive first-purchase conversion.
**Action:** THEN add at least 1 SMS message to the Welcome flow for SMS-consented subscribers, ideally within the first 24 hours.
**Suggested Priority:** Medium
**Score Impact:** -1 point from Flow Configuration Quality
**Confidence:** Confirmed

---

**RULE ID: SMS-011**
**Trigger Condition:** IF no signup form collects SMS consent
**Severity:** High
**Finding:** The account cannot grow its SMS list through organic form capture. All SMS growth must come from other opt-in methods.
**Business Impact:** Severely limits SMS list growth rate, which limits long-term SMS revenue.
**Action:** THEN add an SMS opt-in field to all active signup forms. Use Klaviyo's two-tap SMS consent flow (required for TCPA compliance).
**Suggested Priority:** High
**Score Impact:** -1 point from Signup Forms category; -1 point from SMS category
**Confidence:** Confirmed

---

**RULE ID: SMS-012**
**Trigger Condition:** IF SMS is active but SMS revenue is not attributable (no SMS revenue tracking set up)
**Severity:** Medium
**Finding:** The account cannot see the ROI of its SMS program, which makes optimization impossible.
**Business Impact:** Without attribution, the account cannot prioritize SMS investment or improvement.
**Action:** THEN confirm SMS revenue attribution is configured in Klaviyo. Ensure conversion tracking is linked to placed order events for SMS campaigns and flows.
**Suggested Priority:** Medium
**Score Impact:** -1 point from Revenue Attribution category
**Confidence:** Likely

---

**RULE ID: SMS-013**
**Trigger Condition:** IF SMS is enabled and SMS flows exist AND SMS consent rate is above 15%
**Severity:** N/A (Positive Finding)
**Finding:** SMS program is well-developed. Active flows and a healthy consented list are in place.
**Business Impact:** Positive — set up for strong SMS revenue contribution.
**Action:** THEN focus on optimization: A/B test SMS copy, timing, and offers. Ensure SMS list continues to grow.
**Suggested Priority:** Maintain and optimize
**Score Impact:** Positive — contributes to high SMS category score
**Confidence:** Confirmed

---

**RULE ID: SMS-014**
**Trigger Condition:** IF SMS is not used in Browse Abandonment flow
**Severity:** Medium
**Finding:** Browse abandonment recovery is missing an SMS touchpoint for consented profiles.
**Business Impact:** SMS browse abandonment messages can increase mid-funnel recovery by 15–25%.
**Action:** THEN add at least 1 SMS message to the Browse Abandonment flow, ideally sent 1–2 hours after browsing.
**Suggested Priority:** Medium
**Score Impact:** -1 point from Flow Configuration Quality
**Confidence:** Confirmed

---

**RULE ID: SMS-015**
**Trigger Condition:** IF the account has run both SMS and email campaigns and SMS click rate exceeds email click rate
**Severity:** N/A (Positive Finding)
**Finding:** SMS is outperforming email on click rate — strong signal that the SMS audience is highly engaged.
**Business Impact:** Positive — justify increased SMS investment and expanded SMS flow coverage.
**Action:** THEN increase SMS campaign frequency and add SMS to additional flows.
**Suggested Priority:** Expand
**Score Impact:** +1 bonus point to SMS category
**Confidence:** Confirmed

---

## Section 2 — Campaign Rules (CAMP-001 through CAMP-015)

---

**RULE ID: CAMP-001**
**Trigger Condition:** IF fewer than 2 campaigns have been sent in the last 30 days
**Severity:** High
**Finding:** Campaign strategy is inactive or severely underutilized. The email list is not being worked.
**Business Impact:** Significant campaign revenue being left on the table. List may be cooling, leading to deliverability degradation over time.
**Action:** THEN establish a minimum campaign cadence of 1–2 sends per week. Build a 90-day promotions calendar and a content strategy to support consistent sends.
**Suggested Priority:** High
**Score Impact:** -3 points from Campaign category
**Confidence:** Confirmed

---

**RULE ID: CAMP-002**
**Trigger Condition:** IF no campaigns have been sent in 90+ days
**Severity:** Critical
**Finding:** Account is dormant from a campaign standpoint. The list is at risk of forgetting the brand, which will drive high unsubscribes when campaigns resume.
**Business Impact:** Severe revenue gap. List reactivation campaigns will be needed before normal sends resume.
**Action:** THEN before relaunching campaigns, run a re-engagement campaign to warm the list. Start with highly engaged profiles only. Ramp volume slowly. Monitor deliverability closely.
**Suggested Priority:** Critical
**Score Impact:** Campaign score capped at 2/10
**Confidence:** Confirmed

---

**RULE ID: CAMP-003**
**Trigger Condition:** IF campaigns are sent more than 5 times per week to broad (non-engaged) segments
**Severity:** High
**Finding:** Campaign frequency is dangerously high relative to audience engagement. List fatigue and deliverability damage are likely.
**Business Impact:** Elevated unsubscribes, rising spam complaints, declining open rates, and potential inbox placement failure.
**Action:** THEN reduce to 2–3 campaigns per week max. Implement engaged-only targeting for all sends. Add frequency caps. Enable Klaviyo Smart Sending.
**Suggested Priority:** High
**Score Impact:** -2 points from Campaign category; -1 point from Deliverability
**Confidence:** Confirmed

---

**RULE ID: CAMP-004**
**Trigger Condition:** IF all campaigns in the audit period were sent to the full subscriber list with no segmentation
**Severity:** High
**Finding:** Every campaign reaches unengaged, dormant, and cold profiles. This directly damages deliverability and wastes sends.
**Business Impact:** Higher spam complaints and unsubscribes, lower open and click rates, declining inbox placement.
**Action:** THEN immediately create an Engaged 90-Day segment and make it the default audience for all campaign sends going forward.
**Suggested Priority:** High
**Score Impact:** -2 points from Campaign category; -1 point from Segmentation
**Confidence:** Confirmed

---

**RULE ID: CAMP-005**
**Trigger Condition:** IF campaign open rates are below 15% on average over the audit period
**Severity:** Medium
**Finding:** Campaign open rates are below average. Subject lines, sender reputation, or audience relevance may be contributing.
**Business Impact:** Low open rates reduce campaign revenue per send and signal potential deliverability issues.
**Action:** THEN A/B test subject lines, test send time optimization, review sender name (brand vs. person), and audit segmentation to ensure only engaged profiles are receiving campaigns.
**Suggested Priority:** Medium
**Score Impact:** -1 point from Campaign category
**Confidence:** Confirmed

---

**RULE ID: CAMP-006**
**Trigger Condition:** IF campaign click rates are below 1% on average
**Severity:** Medium
**Finding:** Campaign content is not compelling recipients to take action. Offer, creative, or CTA may be the issue.
**Business Impact:** Low click rates reduce conversion and campaign revenue.
**Action:** THEN review offer strategy (is there a clear, compelling offer?), CTA design (single prominent button), and email layout (reduce complexity, increase white space). A/B test CTA copy.
**Suggested Priority:** Medium
**Score Impact:** -1 point from Campaign category
**Confidence:** Confirmed

---

**RULE ID: CAMP-007**
**Trigger Condition:** IF the account has not sent any promotional campaigns in the audit period (all sends are newsletter or informational)
**Severity:** Medium
**Finding:** No revenue-driving campaigns detected. Campaigns are not being used as a direct revenue tool.
**Business Impact:** Missing direct campaign revenue contribution.
**Action:** THEN introduce promotional campaigns with clear offers. Aim for a 70/30 mix of promotional vs. non-promotional sends.
**Suggested Priority:** Medium
**Score Impact:** -1 point from Campaign category
**Confidence:** Likely

---

**RULE ID: CAMP-008**
**Trigger Condition:** IF campaign unsubscribe rate exceeds 0.5% consistently
**Severity:** High
**Finding:** Campaigns are causing accelerated list decay. Frequency, relevance, or targeting may be misaligned.
**Business Impact:** Accelerated list shrinkage, deliverability damage, and reduced future revenue potential.
**Action:** THEN reduce send frequency, improve segmentation, and review offer relevance. Suppress profiles after multiple campaigns without engagement.
**Suggested Priority:** High
**Score Impact:** -2 points from Campaign category; -1 point from Deliverability
**Confidence:** Confirmed

---

**RULE ID: CAMP-009**
**Trigger Condition:** IF email campaigns are sent but no SMS campaigns have been sent in the audit period
**Severity:** Medium
**Finding:** Campaign channel mix is email-only. SMS campaign channel not activated despite SMS being available.
**Business Impact:** Missing incremental SMS campaign revenue.
**Action:** THEN launch SMS campaigns for major promotions and flash sales. Start with 1–2 SMS campaigns per month.
**Suggested Priority:** Medium
**Score Impact:** -1 point from SMS category
**Confidence:** Confirmed

---

**RULE ID: CAMP-010**
**Trigger Condition:** IF campaign revenue per recipient is declining quarter-over-quarter
**Severity:** High
**Finding:** Campaign revenue efficiency is degrading. List quality, offer fatigue, or deliverability may be the cause.
**Business Impact:** Revenue per email sent is declining — the campaign channel is becoming less efficient over time.
**Action:** THEN diagnose: review open rate trend, click rate trend, offer variety, and segment health. Run a list hygiene and re-engagement campaign.
**Suggested Priority:** High
**Score Impact:** -1 point from Revenue Attribution category
**Confidence:** Confirmed

---

**RULE ID: CAMP-011**
**Trigger Condition:** IF subject lines consistently exceed 60 characters
**Severity:** Low
**Finding:** Long subject lines are likely truncated on mobile devices, reducing inbox impression effectiveness.
**Business Impact:** Lower open rates from mobile recipients.
**Action:** THEN keep subject lines under 50 characters for mobile optimization. Test short, punchy subject lines against longer ones.
**Suggested Priority:** Low
**Score Impact:** -0.5 points from Campaign category (rounded in composite)
**Confidence:** Likely

---

**RULE ID: CAMP-012**
**Trigger Condition:** IF preview text is missing on more than 50% of campaigns
**Severity:** Low
**Finding:** Missing preview text is wasted inbox real estate. Preview text doubles the visible message in most email clients.
**Business Impact:** Lower open rates from reduced inbox impression quality.
**Action:** THEN make preview text mandatory on all campaigns. It should complement (not repeat) the subject line.
**Suggested Priority:** Low
**Score Impact:** Minor negative signal in Campaign category
**Confidence:** Confirmed

---

**RULE ID: CAMP-013**
**Trigger Condition:** IF campaigns are consistently sent on Monday or Friday only, with no mid-week sends
**Severity:** Low
**Finding:** Send timing may not be optimized for the audience. Most ecommerce audiences respond better to Tuesday–Thursday sends.
**Business Impact:** Potential 5–15% improvement in open rates from timing optimization.
**Action:** THEN test send time optimization. Klaviyo's Smart Send Time feature can help identify optimal send windows for this specific audience.
**Suggested Priority:** Low
**Score Impact:** Minor note in Campaign category — not a score deduction
**Confidence:** Inferred

---

**RULE ID: CAMP-014**
**Trigger Condition:** IF campaigns are targeted to engaged segments consistently (90-day or better) and open rates exceed 25%
**Severity:** N/A (Positive Finding)
**Finding:** Campaign strategy is strong — engaged targeting and healthy performance confirmed.
**Business Impact:** Positive — protects deliverability and maximizes revenue per send.
**Action:** THEN recognize as a strength. Continue and expand segmentation sophistication.
**Suggested Priority:** Maintain
**Score Impact:** Contributes to high Campaign category score
**Confidence:** Confirmed

---

**RULE ID: CAMP-015**
**Trigger Condition:** IF campaigns have no variety (same template, same offer type, same send time every week)
**Severity:** Low
**Finding:** Campaign monotony reduces engagement over time. Audiences disengage when every email looks and feels identical.
**Business Impact:** Gradual decline in open and click rates from audience habituation.
**Action:** THEN introduce campaign variety: test different offer types (%, $, free shipping, exclusive, urgency), template styles, and content formats (product spotlight, how-to, social proof).
**Suggested Priority:** Low
**Score Impact:** Minor negative in Campaign category
**Confidence:** Inferred

---

## Section 3 — Deliverability Rules (DELV-001 through DELV-015)

---

**RULE ID: DELV-001**
**Trigger Condition:** IF spam complaint rate exceeds 0.10%
**Severity:** Critical
**Finding:** Spam complaint rate has crossed Gmail's published threshold for inbox placement penalties. Inbox placement is at active risk.
**Business Impact:** If uncorrected, this will cause campaigns to land in spam folders for a large percentage of Gmail recipients, dramatically reducing revenue.
**Action:** THEN immediately stop sending to unengaged profiles. Switch all campaigns to engaged-30-day targeting only. Review and remove any purchased or incentivized-sign-up lists. Contact Klaviyo deliverability support.
**Suggested Priority:** Critical
**Score Impact:** Deliverability score capped at 3/10
**Confidence:** Confirmed

---

**RULE ID: DELV-002**
**Trigger Condition:** IF spam complaint rate exceeds 0.30%
**Severity:** Critical
**Finding:** Spam complaint rate is at a level that will cause severe inbox placement failures and may trigger Klaviyo account review.
**Business Impact:** Most campaigns likely landing in spam. Near-total loss of email revenue until resolved.
**Action:** THEN halt all broad campaign sends immediately. Send only to engaged-30-day segment. Audit list acquisition history. Engage Klaviyo deliverability support immediately.
**Suggested Priority:** Critical — stop-everything
**Score Impact:** Deliverability score capped at 2/10
**Confidence:** Confirmed

---

**RULE ID: DELV-003**
**Trigger Condition:** IF hard bounce rate exceeds 1%
**Severity:** High
**Finding:** Hard bounce rate is above the danger threshold. List contains a significant number of invalid email addresses.
**Business Impact:** High bounce rates damage sender reputation and signal list quality problems to receiving mail servers.
**Action:** THEN run a list hygiene campaign. Klaviyo suppresses hard bounces automatically, but review acquisition sources for typos, fake emails, or poor-quality data.
**Suggested Priority:** High
**Score Impact:** -2 points from Deliverability category
**Confidence:** Confirmed

---

**RULE ID: DELV-004**
**Trigger Condition:** IF hard bounce rate exceeds 2%
**Severity:** Critical
**Finding:** Hard bounce rate is critically high. Sender reputation is at serious risk.
**Business Impact:** Inbox placement failures likely. Revenue from email campaigns directly impacted.
**Action:** THEN pause campaigns to the full list. Send only to a verified engaged segment. Audit acquisition sources. Consider email validation on all forms.
**Suggested Priority:** Critical
**Score Impact:** Deliverability score capped at 3/10
**Confidence:** Confirmed

---

**RULE ID: DELV-005**
**Trigger Condition:** IF SPF record is not set up for the sending domain
**Severity:** High
**Finding:** Missing SPF record means receiving mail servers cannot verify the account is authorized to send from this domain.
**Business Impact:** Increased likelihood of emails landing in spam. Also leaves domain vulnerable to spoofing.
**Action:** THEN set up SPF record immediately. Klaviyo provides SPF configuration instructions in account settings. Verify with MXToolbox or equivalent.
**Suggested Priority:** High
**Score Impact:** -2 points from Deliverability category
**Confidence:** Likely (inferred from domain check — requires manual DNS verification)

---

**RULE ID: DELV-006**
**Trigger Condition:** IF DKIM record is not set up for the sending domain
**Severity:** High
**Finding:** Missing DKIM record means emails are not cryptographically signed. This reduces trust with receiving mail servers.
**Business Impact:** Increased spam filtering. Without DKIM, DMARC cannot be fully enforced.
**Action:** THEN configure DKIM signing for the sending domain in Klaviyo settings. Verify with an email header analyzer or MXToolbox.
**Suggested Priority:** High
**Score Impact:** -2 points from Deliverability category
**Confidence:** Likely

---

**RULE ID: DELV-007**
**Trigger Condition:** IF DMARC record is not present on the domain
**Severity:** Medium
**Finding:** Missing DMARC leaves the domain exposed to spoofing and limits deliverability authority.
**Business Impact:** Without DMARC, Gmail and Yahoo cannot enforce alignment. Domain is more vulnerable to phishing abuse.
**Action:** THEN add a DMARC record at minimum p=none to start visibility without enforcement. Escalate to p=quarantine or p=reject as sending health improves.
**Suggested Priority:** Medium
**Score Impact:** -1 point from Deliverability category
**Confidence:** Likely

---

**RULE ID: DELV-008**
**Trigger Condition:** IF the account is sending from a Klaviyo default domain (e.g., klaviyomail.com) without a branded/dedicated sending domain
**Severity:** Medium
**Finding:** Sending from a shared domain reduces deliverability authority and brand recognition in the inbox.
**Business Impact:** Lower open rates from reduced brand recognition. Deliverability partially dependent on other senders on the same shared domain.
**Action:** THEN set up a branded sending domain (e.g., send.brandname.com). Klaviyo supports custom sending domains in account settings.
**Suggested Priority:** Medium
**Score Impact:** -1 point from Deliverability category; missing bonus point
**Confidence:** Confirmed

---

**RULE ID: DELV-009**
**Trigger Condition:** IF a branded/dedicated sending domain is in use
**Severity:** N/A (Positive Finding)
**Finding:** Branded sending domain is configured. This is a deliverability best practice that strengthens inbox placement.
**Business Impact:** Positive — improved brand recognition and deliverability independence.
**Action:** THEN recognize as a strength. Ensure DKIM is signed on this domain and DMARC is configured.
**Suggested Priority:** Maintain
**Score Impact:** +1 bonus point to Deliverability (max 10)
**Confidence:** Confirmed

---

**RULE ID: DELV-010**
**Trigger Condition:** IF unsubscribe rate per campaign is consistently above 0.5%
**Severity:** High
**Finding:** Persistent high unsubscribes indicate audience fatigue, frequency issues, or content/offer mismatch.
**Business Impact:** Accelerated list shrinkage and deliverability damage.
**Action:** THEN reduce campaign frequency, tighten segmentation to engaged profiles only, and review offer and content relevance.
**Suggested Priority:** High
**Score Impact:** -2 points from Deliverability category; -1 point from Campaign category
**Confidence:** Confirmed

---

**RULE ID: DELV-011**
**Trigger Condition:** IF deliverability appears healthy across all metrics (spam < 0.02%, bounce < 0.2%, unsubscribe < 0.1%) AND branded domain AND DKIM/SPF/DMARC all present
**Severity:** N/A (Positive Finding)
**Finding:** Deliverability is excellent. All signals indicate a well-maintained sending reputation.
**Business Impact:** Positive — inbox placement is strong, maximizing campaign revenue efficiency.
**Action:** THEN recognize as a strength. Continue engaged-segment targeting to maintain health.
**Suggested Priority:** Maintain
**Score Impact:** Deliverability score in 9–10 range
**Confidence:** Confirmed

---

**RULE ID: DELV-012**
**Trigger Condition:** IF open rate trend is declining more than 20% over the audit period (e.g., 28% open rate 6 months ago, now 22%)
**Severity:** Medium
**Finding:** Declining open rate trend may signal deliverability degradation, list fatigue, or content relevance issues.
**Business Impact:** Declining open rates reduce campaign revenue efficiency over time.
**Action:** THEN investigate: review whether list composition has changed, whether spam complaints have increased, and whether campaigns are reaching engaged segments. Run a list hygiene check.
**Suggested Priority:** Medium
**Score Impact:** -1 point from Deliverability category
**Confidence:** Confirmed

---

**RULE ID: DELV-013**
**Trigger Condition:** IF the account has double opt-in disabled for all lists
**Severity:** Low
**Finding:** Single opt-in allows typos and fake emails into the list, increasing bounce rates over time.
**Business Impact:** Higher hard bounce rates, more suppressed profiles, and list quality degradation.
**Action:** THEN consider enabling double opt-in for main signup forms. Note: double opt-in will reduce total opt-in rate but improve list quality. Balance based on list growth goals.
**Suggested Priority:** Low
**Score Impact:** Minor note in Deliverability — not a deduction unless bounce rate is elevated
**Confidence:** Confirmed

---

**RULE ID: DELV-014**
**Trigger Condition:** IF the account sends to profiles who have not opened or clicked in more than 180 days without a re-engagement step
**Severity:** High
**Finding:** Sending to cold profiles directly damages deliverability. Mail servers see low engagement as a spam signal.
**Business Impact:** Rising spam complaints and declining inbox placement from sending to cold audience.
**Action:** THEN create an engaged-only segment for all campaigns. Move unengaged profiles into a sunset/re-engagement flow before suppressing.
**Suggested Priority:** High
**Score Impact:** -2 points from Deliverability category; -2 points from List Health category
**Confidence:** Likely

---

**RULE ID: DELV-015**
**Trigger Condition:** IF soft bounce rate exceeds 3% on any campaign
**Severity:** Medium
**Finding:** Elevated soft bounce rate may indicate inbox capacity issues on the receiving side or reputation signals causing temporary deferrals.
**Business Impact:** Reduced deliverability and inbox placement for that campaign's recipients.
**Action:** THEN monitor the trend. If soft bounces are persistent on multiple campaigns, investigate sending infrastructure, IP reputation, and content flagging.
**Suggested Priority:** Medium
**Score Impact:** -1 point from Deliverability category if persistent
**Confidence:** Likely

---

## Section 4 — Core Flow Rules (FLOW-001 through FLOW-020)

---

**RULE ID: FLOW-001**
**Trigger Condition:** IF the Welcome flow does not exist or is not in Live status
**Severity:** Critical
**Finding:** The account has no Welcome flow. New subscribers receive no automated brand introduction or first-purchase nurture.
**Business Impact:** New subscribers are not converted to customers through automation. First-purchase conversion is left entirely to chance.
**Action:** THEN build a Welcome flow immediately. Minimum: 4 emails over 7–10 days. Include brand story, product showcase, social proof, and first-purchase incentive.
**Suggested Priority:** Critical
**Score Impact:** Core Flow Coverage score capped at 4/10
**Confidence:** Inferred (absence of flow in API = does not exist)

---

**RULE ID: FLOW-002**
**Trigger Condition:** IF the Welcome flow exists but has fewer than 3 email messages
**Severity:** High
**Finding:** Welcome flow is underdeveloped. Too few touchpoints to effectively convert new subscribers to buyers.
**Business Impact:** Lower first-purchase conversion rate and missed LTV from early-stage subscriber nurture.
**Action:** THEN expand to at least 4 emails: (1) Welcome + brand story, (2) Product showcase / best sellers, (3) Social proof + reviews, (4) Incentive or urgency close.
**Suggested Priority:** High
**Score Impact:** -2 points from Flow Configuration Quality
**Confidence:** Confirmed

---

**RULE ID: FLOW-003**
**Trigger Condition:** IF the Welcome flow exists but has not been updated in more than 12 months
**Severity:** Medium
**Finding:** Welcome flow content may be stale — outdated offers, old product images, or irrelevant messaging.
**Business Impact:** Reduced first-purchase conversion as content loses relevance.
**Action:** THEN review and refresh Welcome flow copy, product imagery, offers, and incentive amounts. Annual refresh minimum.
**Suggested Priority:** Medium
**Score Impact:** -1 point from Flow Configuration Quality
**Confidence:** Confirmed

---

**RULE ID: FLOW-004**
**Trigger Condition:** IF the Abandoned Cart flow does not exist or is not in Live status
**Severity:** Critical
**Finding:** No Abandoned Cart flow. The single highest-revenue recovery automation is missing entirely.
**Business Impact:** 100% of abandoned cart revenue is being lost. This is typically the #1 revenue recovery flow for ecommerce brands.
**Action:** THEN build an Abandoned Cart flow immediately. Minimum: 3 emails + 2 SMS (where consent exists). First email within 1 hour.
**Suggested Priority:** Critical
**Score Impact:** Core Flow Coverage score capped at 4/10
**Confidence:** Inferred

---

**RULE ID: FLOW-005**
**Trigger Condition:** IF the Abandoned Cart flow exists but has only 1 email
**Severity:** Critical
**Finding:** A 1-email abandoned cart flow is severely underbuilt. Most abandoned carts require 2–3 touchpoints to convert.
**Business Impact:** The majority of recoverable cart revenue is being left unretrieved after the first email fails to convert.
**Action:** THEN rebuild to 3-email structure: Email 1 (< 1 hour, urgency + product reminder), Email 2 (24 hours, social proof or benefit focus), Email 3 (72 hours, discount or final offer).
**Suggested Priority:** Critical
**Score Impact:** -3 points from Flow Configuration Quality
**Confidence:** Confirmed

---

**RULE ID: FLOW-006**
**Trigger Condition:** IF the Abandoned Cart flow's first email fires more than 2 hours after abandonment
**Severity:** High
**Finding:** First cart recovery email is delayed. The optimal window for recovery is within 60 minutes — after 2 hours, conversion rates drop significantly.
**Business Impact:** Lower abandoned cart recovery rate. Cart abandoners who would have converted in the first hour are being lost.
**Action:** THEN reset the first email delay to fire within 60 minutes of cart abandonment event. Confirm trigger is "Started Checkout" or "Added to Cart" metric, not a daily batch.
**Suggested Priority:** High
**Score Impact:** -2 points from Flow Configuration Quality
**Confidence:** Confirmed

---

**RULE ID: FLOW-007**
**Trigger Condition:** IF the Abandoned Cart flow has no discount or incentive in any message
**Severity:** Medium
**Finding:** No incentive in the Abandoned Cart flow. For price-sensitive shoppers, no offer means no reason to return.
**Business Impact:** Lower conversion on messages 2 and 3 of the sequence.
**Action:** THEN add a discount offer to email 3 (at minimum). Consider a free shipping offer in email 2. Test % off vs. $ off vs. free shipping.
**Suggested Priority:** Medium
**Score Impact:** -1 point from Flow Configuration Quality
**Confidence:** Confirmed

---

**RULE ID: FLOW-008**
**Trigger Condition:** IF the Abandoned Cart flow has fewer than 2 SMS messages despite SMS being enabled
**Severity:** High
**Finding:** Abandoned Cart is missing its most time-sensitive channel. SMS cart recovery within 1 hour converts at a high rate.
**Business Impact:** Missing SMS abandoned cart messages reduces total cart recovery revenue.
**Action:** THEN add at minimum 2 SMS messages: one within 60 minutes and one 24–48 hours later. Keep SMS copy short, product-specific, and include a direct link.
**Suggested Priority:** High
**Score Impact:** -2 points from Flow Configuration Quality; -1 point from SMS category
**Confidence:** Confirmed

---

**RULE ID: FLOW-009**
**Trigger Condition:** IF the Browse Abandonment flow does not exist
**Severity:** High
**Finding:** No Browse Abandonment flow. The mid-funnel — shoppers who viewed products but didn't add to cart — is completely unaddressed.
**Business Impact:** A meaningful portion of high-intent traffic is leaving without any recovery attempt.
**Action:** THEN build a Browse Abandonment flow. Minimum: 1 email within 1–4 hours + 1 SMS (if consent). Show the specific product browsed.
**Suggested Priority:** High
**Score Impact:** -2 points from Core Flow Coverage
**Confidence:** Inferred

---

**RULE ID: FLOW-010**
**Trigger Condition:** IF the Added to Cart flow does not exist
**Severity:** High
**Finding:** Missing Added to Cart flow. There is no recovery automation for the stage between browse and checkout abandonment.
**Business Impact:** Revenue recovery gap between Browse Abandonment and Abandoned Cart flows.
**Action:** THEN build an Added to Cart flow. Mirror the Abandoned Cart structure: 3 emails, 2 SMS, with the first message within 1 hour.
**Suggested Priority:** High
**Score Impact:** -1 point from Core Flow Coverage
**Confidence:** Inferred

---

**RULE ID: FLOW-011**
**Trigger Condition:** IF the Post-Purchase flow does not exist
**Severity:** High
**Finding:** No Post-Purchase flow. Customers receive no automated communication after buying — repeat purchase is left entirely to chance.
**Business Impact:** Lower repeat purchase rate and LTV. Cross-sell and upsell opportunities are lost.
**Action:** THEN build a Post-Purchase flow. Minimum: Email 1 (thank you + order confirmation info), Email 2 (product usage or care tips), Email 3 (review request), Email 4 (cross-sell or replenishment nudge).
**Suggested Priority:** High
**Score Impact:** -1 point from Core Flow Coverage; -1 point from Lifecycle Coverage category
**Confidence:** Inferred

---

**RULE ID: FLOW-012**
**Trigger Condition:** IF the Winback flow does not exist
**Severity:** Medium
**Finding:** No Winback flow. Churned customers are never reactivated through automation.
**Business Impact:** Lost repeat purchase revenue from customers who bought once but drifted away.
**Action:** THEN build a Winback flow targeting customers who purchased 90–180 days ago with no recent engagement. Include a compelling offer. End with a sunset/suppression step.
**Suggested Priority:** Medium
**Score Impact:** -1 point from Core Flow Coverage
**Confidence:** Inferred

---

**RULE ID: FLOW-013**
**Trigger Condition:** IF no VIP or loyalty flow exists
**Severity:** Low
**Finding:** High-LTV customers are receiving the same experience as all other subscribers. No VIP recognition program.
**Business Impact:** Missed opportunity to retain and monetize the most valuable customer segment.
**Action:** THEN create a VIP segment (top 10% by purchase value or frequency) and a VIP flow with exclusive offers and early access.
**Suggested Priority:** Low
**Score Impact:** Minor deduction from Core Flow Coverage if other flows are present
**Confidence:** Inferred

---

**RULE ID: FLOW-014**
**Trigger Condition:** IF flows exist but none have been updated in more than 12 months
**Severity:** Medium
**Finding:** All flows are stale. Offers, copy, product images, and strategies may be outdated.
**Business Impact:** Declining flow performance as content becomes irrelevant. Potential discount amounts that no longer reflect current strategy.
**Action:** THEN schedule a quarterly flow review. Update offer amounts, images, copy, and incentive strategy annually at minimum.
**Suggested Priority:** Medium
**Score Impact:** -1 point from Flow Configuration Quality
**Confidence:** Confirmed

---

**RULE ID: FLOW-015**
**Trigger Condition:** IF the account has the Abandoned Cart flow in Draft status (not Live)
**Severity:** Critical
**Finding:** Abandoned Cart flow exists but is not running. Zero cart recovery is happening through automation.
**Business Impact:** 100% of recoverable cart revenue is being lost from the automation channel.
**Action:** THEN review and activate the Abandoned Cart flow immediately. Confirm all messages are Live within the flow before activating.
**Suggested Priority:** Critical
**Score Impact:** Same as FLOW-004 (Critical — counts as missing)
**Confidence:** Confirmed

---

**RULE ID: FLOW-016**
**Trigger Condition:** IF the Welcome flow has 4+ emails and also includes SMS messages
**Severity:** N/A (Positive Finding)
**Finding:** Welcome flow is well-structured and multi-channel. Both email and SMS subscribers receive appropriate onboarding.
**Business Impact:** Positive — higher first-purchase conversion expected from strong multi-touch welcome sequence.
**Action:** THEN recognize as a strength. Ensure timing and offer are reviewed regularly.
**Suggested Priority:** Maintain
**Score Impact:** Positive contributor to Flow Configuration Quality score
**Confidence:** Confirmed

---

**RULE ID: FLOW-017**
**Trigger Condition:** IF flow revenue contribution is less than 10% of total Klaviyo revenue
**Severity:** Critical
**Finding:** Lifecycle automation is generating almost no revenue. The account is almost entirely dependent on manual campaign sends.
**Business Impact:** Revenue is fragile — it stops when campaigns stop. Flow revenue should compound without ongoing effort.
**Action:** THEN treat flow rebuild as the highest-priority initiative. Start with Abandoned Cart, then Welcome, then Browse Abandonment.
**Suggested Priority:** Critical
**Score Impact:** -3 points from Revenue Attribution category
**Confidence:** Confirmed

---

**RULE ID: FLOW-018**
**Trigger Condition:** IF a Replenishment flow does not exist for an account selling consumable or replenishable products
**Severity:** Medium
**Finding:** Replenishable product brands without a replenishment reminder flow are missing predictable repeat purchase revenue.
**Business Impact:** Lost subscription-equivalent repeat purchase revenue. Competitor brands with replenishment flows may capture the reorder.
**Action:** THEN build a replenishment flow triggered 20–30 days after first purchase (adjust based on product consumption cycle). Include a direct reorder CTA.
**Suggested Priority:** Medium
**Score Impact:** -1 point from Lifecycle Coverage
**Confidence:** Inferred (requires knowing product type — flag only if applicable)

---

**RULE ID: FLOW-019**
**Trigger Condition:** IF a Sunset or Unengaged flow does not exist
**Severity:** Medium
**Finding:** No mechanism to suppress permanently unengaged profiles. They accumulate, inflate billing, and damage deliverability.
**Business Impact:** List decay accelerates. Billing inflated by non-engaged profiles. Deliverability impacted by sending to cold contacts.
**Action:** THEN build a Sunset flow for profiles unengaged for 365+ days. Include a final re-engagement offer, then suppress non-responders.
**Suggested Priority:** Medium
**Score Impact:** -1 point from List Health category
**Confidence:** Inferred

---

**RULE ID: FLOW-020**
**Trigger Condition:** IF all 7 core flows are Live AND all meet minimum message count standards
**Severity:** N/A (Positive Finding)
**Finding:** Full core lifecycle automation is in place and meets baseline configuration standards.
**Business Impact:** Positive — comprehensive automation foundation in place.
**Action:** THEN recognize as a strength. Focus on optimization: A/B test subject lines, offers, timing, and SMS.
**Suggested Priority:** Optimize and maintain
**Score Impact:** Core Flow Coverage score in 9–10 range
**Confidence:** Confirmed

---

## Section 5 — Flow Timing Rules (FTIM-001 through FTIM-010)

---

**RULE ID: FTIM-001**
**Trigger Condition:** IF the Abandoned Cart first email fires more than 60 minutes after the trigger event
**Severity:** High
**Finding:** Delayed first abandoned cart email. The 60-minute window is critical for cart recovery — after this, urgency fades.
**Business Impact:** Meaningful reduction in abandoned cart recovery rate compared to a sub-60-minute first touch.
**Action:** THEN set the first email delay to 0 minutes after trigger (immediate) or at most 30 minutes. Do not exceed 60 minutes.
**Suggested Priority:** High
**Score Impact:** -2 points from Flow Configuration Quality
**Confidence:** Confirmed

---

**RULE ID: FTIM-002**
**Trigger Condition:** IF the second Abandoned Cart email fires fewer than 18 hours after the first
**Severity:** Medium
**Finding:** Second abandoned cart email is too close to the first. Back-to-back emails feel aggressive and may drive unsubscribes.
**Business Impact:** Elevated unsubscribes, lower conversion on email 2.
**Action:** THEN set a 22–26 hour delay between email 1 and email 2 (approximately 24 hours after abandonment total).
**Suggested Priority:** Medium
**Score Impact:** -1 point from Flow Configuration Quality
**Confidence:** Confirmed

---

**RULE ID: FTIM-003**
**Trigger Condition:** IF the third Abandoned Cart email fires more than 5 days after the second
**Severity:** Medium
**Finding:** Too long a gap between email 2 and email 3 reduces urgency and relevance of the final recovery offer.
**Business Impact:** Lower conversion on email 3, as the cart context has faded.
**Action:** THEN set email 3 to fire 48–72 hours after email 2 (approximately 3–4 days after initial abandonment).
**Suggested Priority:** Medium
**Score Impact:** -1 point from Flow Configuration Quality
**Confidence:** Confirmed

---

**RULE ID: FTIM-004**
**Trigger Condition:** IF Welcome flow email 1 fires more than 1 hour after subscription
**Severity:** Medium
**Finding:** First welcome email is delayed. New subscribers expect a near-immediate response after opting in.
**Business Impact:** Lower first-email open rate. Subscriber may forget they opted in if email arrives hours later.
**Action:** THEN set Welcome email 1 to fire immediately (0 minutes) or within 15 minutes of subscription.
**Suggested Priority:** Medium
**Score Impact:** -1 point from Flow Configuration Quality
**Confidence:** Confirmed

---

**RULE ID: FTIM-005**
**Trigger Condition:** IF Welcome flow has fewer than 3 days of total duration (all emails sent within 72 hours)
**Severity:** Low
**Finding:** Welcome flow is too compressed. New subscribers are receiving multiple emails in a short window — may feel like spam.
**Business Impact:** Elevated unsubscribes in welcome flow. Lower per-email engagement as recipients feel overwhelmed.
**Action:** THEN spread Welcome flow over 7–10 days. Suggested timing: Day 0, Day 2, Day 5, Day 8.
**Suggested Priority:** Low
**Score Impact:** Minor note in Flow Configuration Quality
**Confidence:** Confirmed

---

**RULE ID: FTIM-006**
**Trigger Condition:** IF Browse Abandonment first email fires more than 4 hours after the browse event
**Severity:** Medium
**Finding:** Browse abandonment email is too delayed. The shopper's intent is strongest within 1–4 hours of browsing.
**Business Impact:** Lower browse abandonment recovery rate compared to a 1–2 hour trigger.
**Action:** THEN set Browse Abandonment first message to fire 1–2 hours after the view product event.
**Suggested Priority:** Medium
**Score Impact:** -1 point from Flow Configuration Quality
**Confidence:** Confirmed

---

**RULE ID: FTIM-007**
**Trigger Condition:** IF Winback flow targets customers who last purchased fewer than 60 days ago
**Severity:** Medium
**Finding:** Winback flow is triggering too early. 60 days post-purchase may still be within the natural purchase cycle for many categories.
**Business Impact:** Aggressive re-engagement may feel unwanted and drive unsubscribes from still-active customers.
**Action:** THEN adjust Winback flow trigger to 90–180 days post-last-purchase, depending on average purchase cycle.
**Suggested Priority:** Medium
**Score Impact:** -1 point from Flow Configuration Quality
**Confidence:** Confirmed

---

**RULE ID: FTIM-008**
**Trigger Condition:** IF Post-Purchase flow email 1 fires more than 24 hours after purchase
**Severity:** Low
**Finding:** First post-purchase email is delayed. Customers expect a thank-you or order confirmation communication quickly.
**Business Impact:** Lower post-purchase satisfaction signal; missed opportunity to start the next-purchase nurture cycle promptly.
**Action:** THEN set first Post-Purchase email to fire within 1–4 hours of purchase (after order confirmation is handled by the platform).
**Suggested Priority:** Low
**Score Impact:** Minor note — not a direct score deduction
**Confidence:** Confirmed

---

**RULE ID: FTIM-009**
**Trigger Condition:** IF SMS messages in flows fire more than 30 minutes after the equivalent email in the same step
**Severity:** Low
**Finding:** SMS and email are not aligned within flow steps. For abandonment flows, SMS should fire close to the email trigger (or before).
**Business Impact:** Minor — SMS loses urgency advantage if sent significantly after the email.
**Action:** THEN align SMS timing so it fires within 5–15 minutes of the email in the same flow step, or set SMS to fire first for maximum urgency.
**Suggested Priority:** Low
**Score Impact:** Minor note — not a direct score deduction
**Confidence:** Inferred

---

**RULE ID: FTIM-010**
**Trigger Condition:** IF abandoned cart flow timing is: Email 1 within 1 hour, Email 2 approximately 24 hours, Email 3 approximately 72 hours, with 2 SMS messages appropriately placed
**Severity:** N/A (Positive Finding)
**Finding:** Abandoned Cart timing is optimally configured.
**Business Impact:** Positive — maximized cart recovery at each stage of the sequence.
**Action:** THEN recognize as a strength. A/B test offer and copy variations within this timing framework.
**Suggested Priority:** Maintain
**Score Impact:** Positive contributor to Flow Configuration Quality score
**Confidence:** Confirmed

---

## Section 6 — Form Rules (FORM-001 through FORM-010)

---

**RULE ID: FORM-001**
**Trigger Condition:** IF no active signup form exists in the account
**Severity:** Critical
**Finding:** There is no mechanism for capturing new email subscribers. List growth is entirely dependent on checkout and other passive capture points.
**Business Impact:** List growth is stunted. Without a dedicated opt-in form, the account is leaving potentially hundreds of new subscribers per month on the table.
**Action:** THEN publish a popup or flyout signup form immediately. Include an incentive (discount, free shipping, or exclusive offer). Target a 3%+ opt-in rate.
**Suggested Priority:** Critical
**Score Impact:** Signup Forms score fixed at 1/10
**Confidence:** Inferred

---

**RULE ID: FORM-002**
**Trigger Condition:** IF the signup form opt-in rate is below 2%
**Severity:** High
**Finding:** Signup form is underperforming. The current capture rate is below the minimum acceptable threshold.
**Business Impact:** List growth is slower than it should be. Every missed subscriber is a missed lifetime revenue opportunity.
**Action:** THEN redesign the form. Test: stronger incentive (% off vs. free shipping), headline copy, display timing (exit-intent vs. time-delay), and mobile layout.
**Suggested Priority:** High
**Score Impact:** Signup Forms score capped at 3/10
**Confidence:** Confirmed

---

**RULE ID: FORM-003**
**Trigger Condition:** IF the signup form opt-in rate is between 2% and 3.9%
**Severity:** Low
**Finding:** Form is performing at an average level. Meaningful improvement is possible.
**Business Impact:** A 2–3% lift in opt-in rate could meaningfully increase monthly subscriber volume.
**Action:** THEN A/B test incentive type, form headline, and display timing. Set a target of 4%+ opt-in rate.
**Suggested Priority:** Low
**Score Impact:** Minor positive but below strong threshold
**Confidence:** Confirmed

---

**RULE ID: FORM-004**
**Trigger Condition:** IF the signup form opt-in rate is between 4% and 5.9%
**Severity:** N/A (Positive Finding)
**Finding:** Signup form is performing well. Above-average list capture rate.
**Business Impact:** Positive — strong list growth foundation.
**Action:** THEN maintain current form while testing if further improvements can push to 6%+. Continue A/B testing.
**Suggested Priority:** Optimize
**Score Impact:** Strong positive in Signup Forms category
**Confidence:** Confirmed

---

**RULE ID: FORM-005**
**Trigger Condition:** IF the signup form opt-in rate is 6% or above
**Severity:** N/A (Positive Finding)
**Finding:** Excellent form performance. Top-tier list capture rate.
**Business Impact:** Positive — list is growing rapidly at high efficiency.
**Action:** THEN recognize as a strength. Protect this performance — avoid unnecessary changes. Continue testing to maintain.
**Suggested Priority:** Maintain
**Score Impact:** +1 bonus point to Signup Forms (max 10)
**Confidence:** Confirmed

---

**RULE ID: FORM-006**
**Trigger Condition:** IF the form collects email only and does not have an SMS opt-in field
**Severity:** High
**Finding:** The form is not collecting SMS consent. SMS list growth is blocked at the primary capture point.
**Business Impact:** SMS list cannot grow through organic form capture. SMS revenue potential is being structurally limited.
**Action:** THEN add an SMS opt-in field to the signup form. Ensure it complies with TCPA requirements (clear disclosure language, two-tap consent).
**Suggested Priority:** High
**Score Impact:** -1 point from Signup Forms; -1 point from SMS Adoption
**Confidence:** Confirmed

---

**RULE ID: FORM-007**
**Trigger Condition:** IF the mobile form opt-in rate is less than 50% of the desktop opt-in rate
**Severity:** Medium
**Finding:** Mobile form is significantly underperforming relative to desktop. Mobile visitors are not converting at an acceptable rate.
**Business Impact:** Most ecommerce traffic is mobile. A poor mobile opt-in rate is suppressing the majority of list growth opportunity.
**Action:** THEN redesign the mobile popup: simplify to 1 field (email only), reduce required clicks, ensure form does not cover the entire screen, and check that the close button is visible.
**Suggested Priority:** Medium
**Score Impact:** -1 point from Signup Forms
**Confidence:** Confirmed

---

**RULE ID: FORM-008**
**Trigger Condition:** IF the form has no incentive (discount, free shipping, lead magnet, or exclusive offer)
**Severity:** Medium
**Finding:** No incentive on the signup form. Asking for an email without offering something in return depresses opt-in rates significantly.
**Business Impact:** Lower opt-in rate directly reduces list growth and all downstream revenue.
**Action:** THEN add an incentive. Test: 10% off first order, free shipping on first order, or a free guide/resource relevant to the brand. Typical incentive-added lift: 1–3 percentage points on opt-in rate.
**Suggested Priority:** Medium
**Score Impact:** -1 point from Signup Forms if opt-in rate is also below 4%
**Confidence:** Confirmed

---

**RULE ID: FORM-009**
**Trigger Condition:** IF there is only a footer embed form and no popup or flyout form
**Severity:** High
**Finding:** Footer-only form has extremely low visibility. Most visitors never scroll to the footer. A popup or flyout is required for meaningful opt-in rates.
**Business Impact:** Near-zero list growth from form capture alone without a popup.
**Action:** THEN add a popup or flyout form with exit-intent or scroll-trigger display rules. Keep the footer form as a secondary capture point.
**Suggested Priority:** High
**Score Impact:** -2 points from Signup Forms
**Confidence:** Confirmed

---

**RULE ID: FORM-010**
**Trigger Condition:** IF the form is actively A/B testing different headlines, offers, or display timing
**Severity:** N/A (Positive Finding)
**Finding:** Form optimization is active. A/B testing demonstrates a commitment to improving list growth performance.
**Business Impact:** Positive — continuous improvement in opt-in rate compounds over time.
**Action:** THEN maintain testing cadence. Document results and apply winners. Test one variable at a time.
**Suggested Priority:** Maintain
**Score Impact:** Positive note in Signup Forms category
**Confidence:** Confirmed

---

## Section 7 — List Health Rules (LIST-001 through LIST-010)

---

**RULE ID: LIST-001**
**Trigger Condition:** IF more than 50% of emailable profiles have not engaged in 180+ days
**Severity:** Critical
**Finding:** The majority of the email list is cold. Sending campaigns to this list at full volume will damage deliverability.
**Business Impact:** High deliverability risk. Spam complaints and unsubscribes from unengaged recipients will suppress inbox placement for engaged recipients too.
**Action:** THEN immediately restrict campaigns to the engaged 90-day segment. Run a re-engagement campaign for the 90–180 day group. Suppress the 180+ day group after a sunset attempt.
**Suggested Priority:** Critical
**Score Impact:** -3 points from List Health; -1 point from Deliverability
**Confidence:** Confirmed

---

**RULE ID: LIST-002**
**Trigger Condition:** IF the engaged 30-day segment is less than 5% of the emailable list
**Severity:** High
**Finding:** Active, highly engaged audience is very small relative to list size. The list has a high proportion of cold contacts.
**Business Impact:** Limited campaign effectiveness. Low open rates and high relative spam complaint rates.
**Action:** THEN focus campaigns on this engaged core. Run a re-engagement campaign for the 30–90 day group. Grow the engaged segment through better email frequency and content.
**Suggested Priority:** High
**Score Impact:** -2 points from List Health
**Confidence:** Confirmed

---

**RULE ID: LIST-003**
**Trigger Condition:** IF the suppression rate is above 20%
**Severity:** High
**Finding:** One in five profiles is suppressed. This indicates historical list quality issues, frequency abuse, or poor acquisition practices.
**Business Impact:** High suppression inflates billing tier (paying for unusable profiles) and signals poor historical deliverability.
**Action:** THEN audit acquisition sources for purchased lists. Review historical sending frequency. Implement a forward-looking list hygiene program to prevent further suppression growth.
**Suggested Priority:** High
**Score Impact:** -2 points from List Health; -1 point from Billing Efficiency
**Confidence:** Confirmed

---

**RULE ID: LIST-004**
**Trigger Condition:** IF the suppression rate is growing month-over-month (increasing by > 2% per month)
**Severity:** High
**Finding:** Suppression is actively growing. This means more profiles are disengaging faster than new ones are being added with quality.
**Business Impact:** List is shrinking in effective reach. Deliverability will continue to degrade if this trend continues.
**Action:** THEN investigate: Are new acquisition sources introducing low-quality contacts? Is send frequency too high? Is content relevance declining? Address root cause immediately.
**Suggested Priority:** High
**Score Impact:** -2 points from List Health
**Confidence:** Confirmed

---

**RULE ID: LIST-005**
**Trigger Condition:** IF list growth rate is negative (list is shrinking net of new subscribers)
**Severity:** Critical
**Finding:** The email list is shrinking. Suppressions, bounces, and unsubscribes are outpacing new subscriber acquisition.
**Business Impact:** Long-term revenue decline as the addressable email audience contracts.
**Action:** THEN prioritize list growth: improve signup form opt-in rate, add SMS opt-in to forms, review paid acquisition channels driving email capture, and consider lead magnet or sweepstakes list growth campaigns.
**Suggested Priority:** Critical
**Score Impact:** -2 points from Signup Forms and List Health
**Confidence:** Confirmed

---

**RULE ID: LIST-006**
**Trigger Condition:** IF the engaged 90-day segment represents more than 30% of the emailable list
**Severity:** N/A (Positive Finding)
**Finding:** List health is strong. A significant portion of emailable profiles remain actively engaged.
**Business Impact:** Positive — healthy deliverability foundation and strong revenue potential.
**Action:** THEN maintain by continuing engaged-segment targeting and regular list hygiene practices.
**Suggested Priority:** Maintain
**Score Impact:** Positive contributor to List Health score
**Confidence:** Confirmed

---

**RULE ID: LIST-007**
**Trigger Condition:** IF the account has never run a re-engagement campaign
**Severity:** Medium
**Finding:** No re-engagement strategy exists. Cold profiles accumulate indefinitely without a systematic attempt to reactivate or sunset them.
**Business Impact:** Growing dead weight on the list that damages deliverability and inflates billing.
**Action:** THEN run a re-engagement campaign for profiles inactive 90–180 days. Build a Sunset flow for 180+ day inactive profiles.
**Suggested Priority:** Medium
**Score Impact:** -1 point from List Health
**Confidence:** Inferred

---

**RULE ID: LIST-008**
**Trigger Condition:** IF the account has multiple lists with overlapping audiences and no deduplication strategy
**Severity:** Low
**Finding:** Overlapping lists may cause duplicate sends and audience confusion. Profiles on multiple lists may receive the same campaign twice.
**Business Impact:** Duplicate sends damage sender reputation and frustrate recipients.
**Action:** THEN audit list structure. Consolidate where possible. Use segments instead of lists for campaign targeting where overlap is common. Klaviyo deduplicates across lists for campaign sends — confirm this is configured.
**Suggested Priority:** Low
**Score Impact:** Minor note — not a direct score deduction
**Confidence:** Inferred

---

**RULE ID: LIST-009**
**Trigger Condition:** IF the account uses purchased email lists
**Severity:** Critical
**Finding:** Purchased lists violate Klaviyo's Terms of Service and are the leading cause of deliverability failures, high spam complaint rates, and account suspension.
**Business Impact:** Severe deliverability damage, potential account suspension, and legal exposure.
**Action:** THEN remove all purchased list contacts immediately. Audit which lists came from purchased sources and suppress those contacts. Never upload a purchased list again.
**Suggested Priority:** Critical
**Score Impact:** -3 points from Deliverability; -3 points from List Health
**Confidence:** Inferred (requires list source investigation — flag for manual review)

---

**RULE ID: LIST-010**
**Trigger Condition:** IF the account has fewer than 500 emailable profiles
**Severity:** Medium
**Finding:** The emailable list is very small. Campaign and flow revenue will be limited by audience size.
**Business Impact:** Even well-configured automation will generate limited revenue with a small list. List growth is the top priority.
**Action:** THEN prioritize all list growth activities: optimize signup form opt-in rate, add SMS opt-in, explore paid list growth campaigns (lead gen ads), and improve post-purchase email capture.
**Suggested Priority:** Medium
**Score Impact:** Context-dependent — not a score deduction, but a limiting factor noted in the report
**Confidence:** Confirmed

---

## Section 8 — Revenue Rules (REV-001 through REV-010)

---

**RULE ID: REV-001**
**Trigger Condition:** IF flow revenue is less than 20% of total Klaviyo revenue
**Severity:** Critical
**Finding:** Lifecycle automation contributes less than 20% of email/SMS revenue. The account is overly reliant on manual campaign sends.
**Business Impact:** Revenue stops when campaigns stop. Flow revenue should run passively and compound over time.
**Action:** THEN prioritize core flow builds. Target 30%+ flow revenue contribution within 90 days through Welcome, Abandoned Cart, and Browse Abandonment flow improvements.
**Suggested Priority:** Critical
**Score Impact:** -3 points from Revenue Attribution
**Confidence:** Confirmed

---

**RULE ID: REV-002**
**Trigger Condition:** IF campaign revenue is strong but flow revenue is near zero
**Severity:** Critical
**Finding:** The account is campaign-dependent. All lifecycle automation is non-functional or missing.
**Business Impact:** Maximum revenue vulnerability — any pause in campaigns (holiday, resource gap, platform issue) collapses revenue.
**Action:** THEN treat core flow rebuild as the #1 priority before any other optimization.
**Suggested Priority:** Critical
**Score Impact:** -3 points from Revenue Attribution; amplifies Core Flow deductions
**Confidence:** Confirmed

---

**RULE ID: REV-003**
**Trigger Condition:** IF benchmark ratings for campaigns are mostly Poor or Below Average
**Severity:** High
**Finding:** Campaign performance is lagging behind comparable accounts. Multiple dimensions likely contribute: subject lines, segmentation, offer, or deliverability.
**Business Impact:** Revenue per send is below what similar accounts achieve.
**Action:** THEN diagnose systematically: review open rate trend, click rate trend, offer strategy, and segmentation. Do not attempt to fix everything at once — prioritize the biggest gap.
**Suggested Priority:** High
**Score Impact:** -2 points from Revenue Attribution category
**Confidence:** Confirmed

---

**RULE ID: REV-004**
**Trigger Condition:** IF benchmark ratings for flows are mostly Poor or Below Average
**Severity:** High
**Finding:** Flow performance is below comparable accounts. Flow revenue per recipient is lower than industry norms.
**Business Impact:** Existing flows are running but underperforming. Optimization can improve revenue without new flow builds.
**Action:** THEN focus on flow optimization: A/B test subject lines, offers, and timing. Review message count. Add SMS where missing.
**Suggested Priority:** High
**Score Impact:** -2 points from Revenue Attribution category
**Confidence:** Confirmed

---

**RULE ID: REV-005**
**Trigger Condition:** IF email revenue is strong but SMS revenue is zero or not trackable
**Severity:** High
**Finding:** Email channel is performing but SMS channel generates no attributed revenue. An entire incremental revenue stream is missing.
**Business Impact:** Industry data suggests SMS can add 10–20% incremental revenue to accounts with mature email programs.
**Action:** THEN launch SMS if not active, or audit why SMS is not generating attributable revenue. Ensure SMS revenue attribution is configured in Klaviyo.
**Suggested Priority:** High
**Score Impact:** -2 points from SMS category; -1 point from Revenue Attribution
**Confidence:** Confirmed

---

**RULE ID: REV-006**
**Trigger Condition:** IF Klaviyo revenue is declining quarter-over-quarter
**Severity:** High
**Finding:** Email and SMS revenue is trending down. One or more of: campaign performance, flow performance, deliverability, or list health is degrading.
**Business Impact:** Direct revenue decline from the Klaviyo channel.
**Action:** THEN run a full diagnostic: open rate trend, click rate trend, flow revenue trend, deliverability metrics, list health metrics. Identify the primary degradation signal before prescribing a fix.
**Suggested Priority:** High
**Score Impact:** -1 point from Revenue Attribution; other deductions based on root cause
**Confidence:** Confirmed

---

**RULE ID: REV-007**
**Trigger Condition:** IF revenue per recipient is below $0.05 on campaigns
**Severity:** Medium
**Finding:** Campaign revenue per recipient is very low. Either the offer is weak, segmentation is poor, or deliverability is suppressing reach.
**Business Impact:** Low RPR means the campaign channel is undermonetized relative to its size.
**Action:** THEN review offer quality, segmentation, and click-to-conversion rates. The issue may be post-click (landing page, checkout) rather than email-specific.
**Suggested Priority:** Medium
**Score Impact:** -1 point from Revenue Attribution
**Confidence:** Confirmed (note: RPR norms vary significantly by AOV and industry)

---

**RULE ID: REV-008**
**Trigger Condition:** IF flow revenue > 40% of total Klaviyo revenue
**Severity:** N/A (Positive Finding)
**Finding:** Strong lifecycle automation revenue contribution. Flows are running effectively and driving passive revenue.
**Business Impact:** Positive — highly resilient revenue model with strong automation foundation.
**Action:** THEN recognize as a strength. Focus on optimization and adding additional flow types (VIP, replenishment).
**Suggested Priority:** Maintain
**Score Impact:** +1 bonus point to Revenue Attribution (max 10)
**Confidence:** Confirmed

---

**RULE ID: REV-009**
**Trigger Condition:** IF the account has not set up revenue attribution properly (no placed order event connected)
**Severity:** High
**Finding:** Revenue cannot be attributed to Klaviyo. The account cannot see what campaigns or flows are driving sales.
**Business Impact:** Without attribution, it's impossible to prioritize optimization. Decisions are made blind.
**Action:** THEN ensure the ecommerce platform integration is properly connected and the Placed Order event is firing. Verify in Klaviyo's Metrics section.
**Suggested Priority:** High
**Score Impact:** Revenue Attribution score capped at 4/10
**Confidence:** Inferred

---

**RULE ID: REV-010**
**Trigger Condition:** IF the account's Klaviyo benchmark ratings are mostly Good or Excellent
**Severity:** N/A (Positive Finding)
**Finding:** Account performance exceeds industry benchmarks. Both campaigns and flows are performing at a high level.
**Business Impact:** Positive — revenue per subscriber is strong. Focus on growing the audience to scale results.
**Action:** THEN recognize as a strength. Prioritize list growth and SMS adoption to expand the high-performing program.
**Suggested Priority:** Maintain and scale
**Score Impact:** +1 bonus point to Revenue Attribution (max 10)
**Confidence:** Confirmed

---

## Section 9 — Billing Rules (BILL-001 through BILL-005)

---

**RULE ID: BILL-001**
**Trigger Condition:** IF billing utilization rate (emailable profiles / plan profile limit) is below 25%
**Severity:** High
**Finding:** The account is paying for 4× more profile capacity than it is using. Significant overpay risk.
**Business Impact:** Direct cost inefficiency — monthly Klaviyo fees may be significantly higher than they need to be.
**Action:** THEN flag for client review. Recommend the client evaluate whether a lower Klaviyo plan tier would meet their needs after a list hygiene campaign.
**Suggested Priority:** High
**Score Impact:** Billing Efficiency score in 1–3 range
**Confidence:** Likely (requires plan data — may be inferred from profile count)
**Notes:** Do not recommend a plan downgrade without a client conversation — billing decisions require client authorization.

---

**RULE ID: BILL-002**
**Trigger Condition:** IF suppressed profiles account for more than 30% of the plan's profile tier limit
**Severity:** Medium
**Finding:** A large portion of the plan's profile allowance is consumed by suppressed (non-sendable) profiles, inflating the billing tier.
**Business Impact:** Client is paying for profiles they can never email.
**Action:** THEN confirm Klaviyo's billing policy for suppressed profiles. If suppressed profiles count toward the plan tier, recommend requesting a billing review with Klaviyo or a plan restructure.
**Suggested Priority:** Medium
**Score Impact:** -1 point from Billing Efficiency
**Confidence:** Likely

---

**RULE ID: BILL-003**
**Trigger Condition:** IF the account is approaching its plan profile limit (> 90% utilization)
**Severity:** Medium
**Finding:** The account is near its plan profile limit. A plan upgrade will be needed soon or list hygiene is required to avoid overage charges.
**Business Impact:** Overage charges or automatic plan tier upgrades can increase monthly costs significantly.
**Action:** THEN flag for client attention. Options: (1) upgrade plan proactively, (2) run a list hygiene campaign to remove permanently suppressed or unengaged profiles, or (3) monitor growth rate and plan accordingly.
**Suggested Priority:** Medium
**Score Impact:** -1 point from Billing Efficiency
**Confidence:** Likely

---

**RULE ID: BILL-004**
**Trigger Condition:** IF billing data is not accessible via API and no plan tier information was provided
**Severity:** Low
**Finding:** Billing efficiency cannot be assessed without plan tier data.
**Business Impact:** Cannot identify overpay risk without data.
**Action:** THEN request plan tier and profile limit information from the client directly. Flag Billing Efficiency as "Requires Manual Review" in the report.
**Suggested Priority:** Low
**Score Impact:** Billing Efficiency scored as "Insufficient Data" — note in report
**Confidence:** N/A

---

**RULE ID: BILL-005**
**Trigger Condition:** IF billing utilization is between 60% and 85%
**Severity:** N/A (Positive Finding)
**Finding:** Billing is efficient. The account's plan tier is well-matched to its active audience.
**Business Impact:** Positive — no overpay risk and sufficient headroom for growth.
**Action:** THEN no action required. Continue monitoring as list grows.
**Suggested Priority:** Monitor
**Score Impact:** Billing Efficiency score in 7–9 range
**Confidence:** Likely

---

## Section 10 — Compliance Rules (COMP-001 through COMP-010)

---

**RULE ID: COMP-001**
**Trigger Condition:** IF SMS subscribers were collected without proper TCPA consent language on the opt-in form
**Severity:** Critical
**Finding:** SMS consent may not be legally compliant with TCPA requirements. This exposes the brand to regulatory and legal risk.
**Business Impact:** Potential TCPA violations carry fines of $500–$1,500 per message sent. Legal exposure is significant.
**Action:** THEN stop sending SMS immediately until consent documentation is reviewed by legal counsel. Rebuild opt-in forms with clear TCPA-compliant disclosure language.
**Suggested Priority:** Critical
**Score Impact:** -2 points from Compliance category; flag for legal review
**Confidence:** Inferred (requires manual review of form copy)
**Notes:** Katie flags this as a risk for legal review — she does not make legal compliance determinations.

---

**RULE ID: COMP-002**
**Trigger Condition:** IF the account sends to contacts in the EU without a GDPR-compliant opt-in process
**Severity:** High
**Finding:** EU contacts may not have provided GDPR-compliant consent. Explicit, informed opt-in is required for EU subscribers.
**Business Impact:** GDPR violations can result in fines up to 4% of annual global revenue.
**Action:** THEN flag for legal/compliance review. Consider enabling double opt-in for EU traffic. Ensure privacy policy is linked on the signup form.
**Suggested Priority:** High
**Score Impact:** -1 point from Compliance category; flag for legal review
**Confidence:** Inferred
**Notes:** Katie flags this risk — she does not determine legal compliance.

---

**RULE ID: COMP-003**
**Trigger Condition:** IF no privacy policy link is present on signup forms
**Severity:** Medium
**Finding:** Signup forms should link to the brand's privacy policy. Its absence may create compliance exposure and reduce form trust.
**Business Impact:** Legal exposure and potential opt-in rate reduction from trust signals being absent.
**Action:** THEN add a privacy policy link to all signup forms below the submit button.
**Suggested Priority:** Medium
**Score Impact:** Minor flag in Compliance category
**Confidence:** Inferred (requires manual form review)

---

**RULE ID: COMP-004**
**Trigger Condition:** IF unsubscribe links are not present or functional in email campaigns
**Severity:** Critical
**Finding:** Every commercial email must include a working unsubscribe link under CAN-SPAM law. Missing or broken unsubscribe links are a serious legal violation.
**Business Impact:** Legal exposure and potential ISP blocking.
**Action:** THEN ensure Klaviyo's unsubscribe block is present and functional in all email templates. Test unsubscribe process end-to-end.
**Suggested Priority:** Critical
**Score Impact:** -2 points from Compliance; flag immediately
**Confidence:** Inferred (requires template inspection)

---

**RULE ID: COMP-005**
**Trigger Condition:** IF the sending email address or "From" name appears misleading or does not match the brand
**Severity:** Medium
**Finding:** A misleading sender name or email address may violate CAN-SPAM requirements for truthful header information.
**Business Impact:** Legal exposure and reduced inbox trust.
**Action:** THEN update the From name and email address to clearly represent the brand. Avoid generic "noreply@" addresses — use a monitored address.
**Suggested Priority:** Medium
**Score Impact:** -1 point from Compliance
**Confidence:** Inferred

---

**RULE ID: COMP-006**
**Trigger Condition:** IF the account has a physical mailing address in email footers (as required by CAN-SPAM)
**Severity:** N/A (Positive Finding)
**Finding:** CAN-SPAM compliance — physical address is present in email footers.
**Business Impact:** Positive — reduces legal exposure.
**Action:** THEN maintain.
**Suggested Priority:** Maintain
**Score Impact:** Positive signal in Compliance category
**Confidence:** Inferred

---

**RULE ID: COMP-007**
**Trigger Condition:** IF the sending domain does not have DMARC set to at least p=none
**Severity:** Medium
**Finding:** No DMARC record. Domain is not protected against spoofing and fails email authentication best practices increasingly required by major inbox providers.
**Business Impact:** Yahoo and Google have announced requirements for DMARC for bulk senders. Without it, deliverability will be impacted.
**Action:** THEN add a DMARC record. Start at p=none, monitor reports, then move to p=quarantine or p=reject over time.
**Suggested Priority:** Medium
**Score Impact:** -1 point from Deliverability; -1 point from Compliance
**Confidence:** Likely

---

**RULE ID: COMP-008**
**Trigger Condition:** IF the account's email opt-in process is single opt-in with no confirmation
**Severity:** Low
**Finding:** Single opt-in allows fake or mistyped emails into the list without verification. This is acceptable in most jurisdictions but increases bounce risk.
**Business Impact:** Higher bounce rates over time; potential EU compliance risk.
**Action:** THEN evaluate whether double opt-in makes sense for this account's audience. For EU audiences, strongly recommend double opt-in. For North American audiences, single opt-in is acceptable if list quality is maintained.
**Suggested Priority:** Low
**Score Impact:** Minor note — not a direct score deduction for non-EU accounts
**Confidence:** Confirmed

---

**RULE ID: COMP-009**
**Trigger Condition:** IF the account has a California (CCPA) customer base and no CCPA-compliant privacy disclosures
**Severity:** Medium
**Finding:** California consumers have data rights under CCPA. Brands without CCPA-compliant privacy policies and data handling practices may be exposed.
**Business Impact:** CCPA fines and reputational risk.
**Action:** THEN flag for legal/compliance review. Ensure privacy policy addresses CCPA requirements including opt-out of data sale.
**Suggested Priority:** Medium
**Score Impact:** Minor flag in Compliance category
**Confidence:** Inferred

---

**RULE ID: COMP-010**
**Trigger Condition:** IF the account sends SMS to numbers in area codes associated with countries where TCPA or local equivalent does not apply or is unknown
**Severity:** Medium
**Finding:** International SMS compliance varies widely. Sending to international numbers without understanding local regulations creates risk.
**Business Impact:** Regulatory exposure in international markets.
**Action:** THEN flag for legal review if international SMS sending is occurring. Confirm Klaviyo's supported SMS regions and applicable regulations for each market.
**Suggested Priority:** Medium
**Score Impact:** Flag in Compliance category — not a direct deduction unless risk is confirmed
**Confidence:** Inferred

---

---

## Section 11 — Supplemental Rules (SUPP-001 through SUPP-005)

---

**RULE ID: SUPP-001**
**Trigger Condition:** IF the account has no tags applied to any flows, campaigns, or lists
**Severity:** Low
**Finding:** No tagging or organizational taxonomy exists in the account. As the account grows, finding and managing assets becomes increasingly difficult.
**Business Impact:** Operational inefficiency — harder to audit, duplicate assets created, onboarding new team members is slower.
**Action:** THEN implement a tagging convention: tag flows by funnel stage (acquisition, conversion, retention), campaigns by type (promotional, educational, transactional), and lists by source.
**Suggested Priority:** Low
**Score Impact:** Minor operational note — no direct score impact
**Confidence:** Confirmed

---

**RULE ID: SUPP-002**
**Trigger Condition:** IF the account has flows with identical or near-identical names that may cause confusion
**Severity:** Low
**Finding:** Duplicate or ambiguous flow names increase the risk of the wrong flow being edited or confused with an active flow.
**Business Impact:** Operational risk — accidental edits to the wrong flow, difficulty identifying which flow is generating revenue.
**Action:** THEN rename flows with a consistent naming convention: [Stage] — [Trigger Type] — [Channel] (e.g., "Retention — Abandoned Cart — Email + SMS"). Archive any truly duplicate flows.
**Suggested Priority:** Low
**Score Impact:** No direct score impact
**Confidence:** Confirmed

---

**RULE ID: SUPP-003**
**Trigger Condition:** IF the account has more than 50 segments and no apparent organizational strategy
**Severity:** Low
**Finding:** Excessive number of segments without clear categorization creates management complexity and potential audience overlap.
**Business Impact:** Campaigns may accidentally include overlapping audiences, leading to duplicate sends and inflated send counts.
**Action:** THEN audit all segments. Archive unused or duplicate segments. Organize active segments into logical groups (engagement, lifecycle stage, product interest, channel).
**Suggested Priority:** Low
**Score Impact:** Minor deduction from Segmentation category if overlapping audiences confirmed
**Confidence:** Inferred

---

**RULE ID: SUPP-004**
**Trigger Condition:** IF the account has not used A/B testing on any campaign or flow in the audit period
**Severity:** Low
**Finding:** No experimentation is occurring. Performance is not being actively optimized through testing.
**Business Impact:** Missed incremental improvements from subject line, offer, and timing optimization that compound over time.
**Action:** THEN recommend starting a simple A/B testing program: begin with campaign subject lines (test 2 variants per send). Move to flow message timing and offer testing in 60 days.
**Suggested Priority:** Low
**Score Impact:** Minor note — not a direct score deduction
**Confidence:** Inferred

---

**RULE ID: SUPP-005**
**Trigger Condition:** IF the account's ecommerce platform integration is not confirmed as active (no Placed Order, Added to Cart, or Active on Site events found in metrics)
**Severity:** Critical
**Finding:** The ecommerce platform integration may not be connected or firing correctly. Without these events, flow triggers for cart abandonment, browse abandonment, and post-purchase will not work — and revenue attribution will be broken.
**Business Impact:** Abandoned cart, added to cart, browse abandonment, and post-purchase flows cannot trigger without platform events. All flow revenue attribution is also broken.
**Action:** THEN verify the ecommerce platform integration in Klaviyo (Integrations → Shopify or equivalent). Confirm that key events (Placed Order, Started Checkout, Added to Cart, Viewed Product) are actively firing. Reconnect or reinstall the integration if events are absent.
**Suggested Priority:** Critical
**Score Impact:** -3 points from Core Flow Coverage (flows cannot function); -2 points from Revenue Attribution (revenue cannot be tracked)
**Confidence:** Inferred

---

## Application Notes

**Rule Conflicts:** When two rules conflict (e.g., SMS-001 and SMS-013 both apply), the more severe rule takes precedence for scoring. Both findings may still appear in the report.

**Rule Stacking:** Multiple rules from the same category can stack to reduce a category score. However, the minimum score is always 1/10 — no category can be scored at 0.

**Confidence and Scoring:** A finding with "Inferred" confidence should be presented as a risk flag rather than a confirmed finding. Use language like "may be" and "we recommend verifying."

**Missing Data:** If data required to evaluate a rule is unavailable, the rule is skipped and the gap is noted in the report as "Data required to evaluate this area."

**Priority Override:** If a client has shared specific business context that changes the priority of a rule (e.g., they are actively mid-launch of SMS), the strategist may adjust the priority in the human review stage.

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-05-10 | Initial decision rules — 125 rules across 11 sections — Phase 1 |
