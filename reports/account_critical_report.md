# Klaviyo Account Audit Report

**CONFIDENTIAL** — Prepared for internal review and client delivery by National Positions

| Field | Value |
|---|---|
| Client / Brand | Ember & Oak Co. |
| Website | emberandoak.com |
| Klaviyo Account | Ember & Oak Co. — Klaviyo |
| Audit Period | Last 12 months (365 days) |
| Ecommerce Platform | Shopify |
| Date Generated | 2026-05-10 |
| Prepared By | Klaviyo Audit Katie — National Positions |
| Approved By | [NP Reviewer Name — required before delivery] |

---

## Section 2 — Klaviyo Health Score: 21/100 — 🚨 Critical

This account scored **21 out of 100** — rated **Critical**.

| Band | Range | Description |
|---|---|---|
| 🏆 Elite | 90–100 | Best-in-class Klaviyo operation |
| ✅ Strong | 75–89 | High-performing with minor gaps |
| 📊 Average | 60–74 | Functional but meaningful opportunities remain |
| ⚠️ Weak | 40–59 | Significant gaps requiring attention |
| 🚨 Critical | 0–39 | Fundamental issues requiring immediate action |

---

## Section 3 — Score Breakdown by Category

| Category | Score (1–10) | Weight | Weighted Points |
|---|---|---|---|
| Deliverability Health | 1/10 | 15% | 1.5 |
| Core Flow Coverage | 2/10 | 15% | 3.0 |
| Flow Configuration Quality | 3/10 | 15% | 4.5 |
| Campaign Strategy | 1/10 | 12% | 1.2 |
| SMS Adoption | 2/10 | 10% | 2.0 |
| Signup Forms & List Growth | 1/10 | 10% | 1.0 |
| List Health & Engagement | 3/10 | 10% | 3.0 |
| Segmentation Quality | 3/10 | 6% | 1.8 |
| Revenue Attribution | 2/10 | 5% | 1.0 |
| Billing Efficiency | 8/10 | 2% | 1.6 |
| **COMPOSITE TOTAL** | — | 100% | **21/100** |

---

## Section 4 — Executive Summary

This Klaviyo audit covers last 12 months of account activity for **Ember & Oak Co.** across campaigns, flows, forms, list health, deliverability, SMS adoption, segmentation, and revenue attribution.

The account scored **21/100** (Critical), with **10 Critical** and **13 High** priority findings. The most impactful opportunities center on the areas highlighted in Sections 5–7.

---

## Section 5 — Top 5 Wins

1. **Billing Efficiency** (8/10) — Profile utilization 84% within efficient range

---

## Section 6 — Top 5 Issues

1. 🔴 **[Critical] CAMP-003** — Only 5% of campaigns are sent to engaged segments — the vast majority go to the full list.
   - *Business Impact:* Sending to unengaged subscribers dramatically increases bounce and spam rates, damaging sender reputation.
   - *Action:* Immediately shift to segmented sends. Create an engaged 90-day segment and target it for all campaigns.

2. 🔴 **[Critical] CAMP-006** — Campaign spam complaint rate is 0.120% — above Google/Yahoo's 0.1% threshold.
   - *Business Impact:* Exceeding 0.1% spam complaints risks Gmail bulk folder placement or sending suspension.
   - *Action:* Stop broad list sends immediately. Clean the list to engaged subscribers only. Review unsubscribe flow.

3. 🔴 **[Critical] DELV-001** — Hard bounce rate is 2.20% — above the 2% critical threshold.
   - *Business Impact:* ISPs interpret persistent hard bounces as evidence of poor list hygiene, leading to inbox placement loss.
   - *Action:* Halt sends to any segment with high bounce concentration. Run full list through email verification service immediately.

4. 🔴 **[Critical] DELV-003** — Spam complaint rate is 0.120% — above the 0.1% critical threshold.
   - *Business Impact:* Gmail and Yahoo will route all email to spam or block sending if complaint rates exceed 0.1%.
   - *Action:* Immediately switch to engaged-only sends. Review unsubscribe process for friction. Suppress all complainers.

5. 🔴 **[Critical] DELV-005** — DKIM is not configured for this sending domain.
   - *Business Impact:* Without DKIM, emails fail authentication checks — ISPs are more likely to filter or reject them.
   - *Action:* Configure DKIM in Klaviyo (Settings → Email → Sending Domain) immediately. Required by Google/Yahoo.

---

## Section 7 — Top 5 Revenue Opportunities

1. **Campaigns are sent to the full list rather than engaged segments.**
   - *Why it matters:* Full-list sends damage deliverability, suppress open rates, and inflate complaint rates — a compounding problem.
   - *Opportunity:* Shifting to engaged-segment sends will improve open rates, reduce complaints, and protect sender reputation.
   - *Next step:* Create engaged 30/90/180-day segments immediately. Mandate that all campaigns target one of these segments.
   - Impact: **High** | Complexity: Easy | Timeline: Immediate

2. **DKIM authentication is missing — emails fail authentication checks.**
   - *Why it matters:* Google and Yahoo require DKIM for bulk senders. Missing DKIM risks filtering or rejection.
   - *Opportunity:* Authentication is table stakes — all other improvements depend on emails reaching the inbox.
   - *Next step:* Configure DKIM in Klaviyo (Settings → Email → Sending Domain). Verify DNS propagation within 48 hours.
   - Impact: **High** | Complexity: Easy | Timeline: Immediate

3. **Signup form opt-in rate is below 1% — the form is not converting.**
   - *Why it matters:* A sub-1% opt-in rate means 99%+ of site visitors who could become email subscribers are not captured.
   - *Opportunity:* Improving opt-in rate from <1% to 3% could triple monthly subscriber acquisition at zero additional traffic cost.
   - *Next step:* Redesign the form: add a clear incentive, rewrite the headline, test exit-intent vs. timed display. A/B test immediately.
   - Impact: **High** | Complexity: Easy | Timeline: 30 days

4. **No engaged segment infrastructure exists — campaigns cannot be targeted by engagement.**
   - *Why it matters:* Engagement-based segmentation is the single most impactful deliverability and revenue lever available.
   - *Opportunity:* Creating engagement segments costs nothing and can be done in under 30 minutes — the ROI is immediate.
   - *Next step:* Create 4 segments: Engaged 30d, Engaged 90d, Engaged 180d, Never Engaged. Use these for all campaign targeting.
   - Impact: **High** | Complexity: Easy | Timeline: Immediate

5. **Campaign frequency is too low — the list is under-monetized.**
   - *Why it matters:* Consistent weekly campaigns are the baseline of email revenue. Sub-weekly sending leaves predictable revenue unrealized.
   - *Opportunity:* Increasing to 1–2 campaigns per week for engaged segments could substantially lift campaign revenue.
   - *Next step:* Build a 4-week editorial calendar. Prioritize promotional and educational content. Send to engaged segments only.
   - Impact: **High** | Complexity: Easy | Timeline: 30 days

---

## Section 8 — SMS Audit

**SMS Enabled:** No
**SMS Consented Profiles:** 0 (0.0% of emailable list)
**SMS in Flows:** No
**SMS Campaigns (audit period):** 0

**Findings:**
- 🟠 [High] SMS is not enabled in this Klaviyo account.

---

## Section 9 — Campaign Strategy Audit

| Metric | Value |
|---|---|
| Total Campaigns (period) | 14 |
| Email Campaigns | 14 |
| SMS Campaigns | 0 |
| Campaigns per Week | 0.3 |
| Avg Open Rate | 11.0% |
| Avg Click Rate | 0.8% |
| Avg Unsubscribe Rate | 0.70% |
| Avg Spam Complaint Rate | 0.120% |
| Avg Hard Bounce Rate | 2.20% |
| % Sent to Engaged Segments | 5% |
| Open Rate Trend | Declining |
| Longest Send Gap | 45 days |

**Findings:**
- 🔴 [Critical] Only 5% of campaigns are sent to engaged segments — the vast majority go to the full list.
- 🔴 [Critical] Campaign spam complaint rate is 0.120% — above Google/Yahoo's 0.1% threshold.
- 🟠 [High] Campaign frequency is only 0.3 per week — below the 1/week minimum for active programs.
- 🟠 [High] Average campaign open rate is 11.0% — below the 15% critical threshold.
- 🟠 [High] Campaign hard bounce rate is 2.20% — above the 1% action threshold.
- 🟡 [Medium] Longest campaign gap was 45 days — subscribers went more than a month without communication.

---

## Section 10 — Deliverability Audit

| Metric | Value | Status |
|---|---|---|
| Hard Bounce Rate | 2.20% | 🔴 Critical |
| Soft Bounce Rate | 0.80% | — |
| Spam Complaint Rate | 0.120% | 🔴 Critical |
| Unsubscribe Rate | 0.70% | 🟠 High |
| SPF | 🔴 Missing | — |
| DKIM | 🔴 Missing | — |
| DMARC | 🔴 Missing | — |
| Branded Sending Domain | 🟡 No | — |

**Findings:**
- 🔴 [Critical] Hard bounce rate is 2.20% — above the 2% critical threshold.
- 🔴 [Critical] Spam complaint rate is 0.120% — above the 0.1% critical threshold.
- 🔴 [Critical] DKIM is not configured for this sending domain.
- 🟠 [High] SPF record is not configured for this sending domain.
- 🟠 [High] DMARC policy is not configured.
- 🟠 [High] Average unsubscribe rate is 0.70% — above the 0.5% concern threshold.
- 🟡 [Medium] Email is sent from a shared Klaviyo domain rather than a branded sending domain.

---

## Section 11 — Core Flow Coverage

| Flow | Status | Revenue | Emails | SMS |
|---|---|---|---|---|
| Welcome Series | ✅ Live | $4,200 | 1 | 0 |
| Abandoned Cart | ❌ Missing | — | — | — |
| Added to Cart | ❌ Missing | — | — | — |
| Browse Abandonment | ❌ Missing | — | — | — |
| Post-Purchase | ❌ Missing | — | — | — |
| Winback / Re-engagement | ❌ Missing | — | — | — |
| VIP / Loyalty | ❌ Missing | — | — | — |

**Findings:**
- 🔴 [Critical] No Abandoned Cart flow is live.
- 🟠 [High] Welcome flow first email is delayed 120 minutes (>60min threshold).
- 🟠 [High] No Browse Abandonment flow is live.
- 🟠 [High] No Post-Purchase flow is live.
- 🟡 [Medium] Welcome flow has only 1 email(s) — less than the 3-email minimum for an effective series.
- 🟡 [Medium] No Winback / Re-engagement flow is live.
- 🟡 [Medium] No Added to Cart flow is live.
- 🔵 [Low] Flow 'Welcome Email' has not been updated in 420 days.

---

## Section 12 — Flow Configuration Audit

### Welcome Email
- Status: Live | Emails: 1 | SMS: 0
- First message delay: 120 minutes
- Has incentive: No
- Last updated: 420 days ago

---

## Section 13 — Signup Form Audit

**Active Forms:** 1

| Form | Type | Opt-In Rate | Mobile Opt-In | SMS Capture | Incentive |
|---|---|---|---|---|---|
| Footer Email Signup | embed | 0.60% | 0.40% | No | No |

**Findings:**
- 🔴 [Critical] Primary signup form opt-in rate is 0.60% — below the 1% critical floor.
- 🟡 [Medium] Primary signup form does not offer an incentive.

---

## Section 14 — Benchmark Review

| Metric | Rating |
|---|---|
| Open Rate | Poor |
| Click Rate | Poor |
| Conversion Rate | Poor |
| Flow Revenue | Poor |
| List Growth | Below Average |
| **Overall** | **Poor** |

---

## Section 15 — List Health Review

| Metric | Value |
|---|---|
| Total Profiles | 42,000 |
| Emailable Profiles | 38,000 |
| SMS Consented | 0 (0.0%) |
| Suppressed | 4,000 (9.5%) |
| Engaged (30 days) | 1,200 (3.2%) |
| Engaged (90 days) | 4,200 (11.1%) |
| Dormant (180+ days) | 29,500 (77.6%) |

**Findings:**
- 🔴 [Critical] Dormant profile rate is 77.6% — more than 60% of emailable profiles have not engaged in 180 days.
- 🟠 [High] Only 3.2% of emailable profiles opened in the last 30 days.

---

## Section 16 — Segmentation Review

| Segment | Exists |
|---|---|
| Engaged 30-day | ❌ |
| Engaged 90-day | ❌ |
| VIP / High-Value | ❌ |
| Purchaser / Customer | ❌ |
| Sunset / Hygiene | ❌ |
| % Campaigns to Engaged | 5% |

**Findings:**
- 🔴 [Critical] Only 5% of campaigns target engaged segments — most sends go to the full list.
- 🟠 [High] No engaged 30-day segment exists.
- 🟡 [Medium] No engaged 90-day segment exists.
- 🟡 [Medium] No VIP or high-value customer segment exists.
- 🟡 [Medium] No sunset / list hygiene segment exists.

---

## Section 17 — Revenue Attribution Review

| Metric | Value |
|---|---|
| Total Klaviyo Revenue | $14,000 |
| Flow Revenue | $4,200 (30%) |
| Campaign Revenue | $9,800 (70%) |
| Attribution Configured | No |

**Findings:**
- 🔴 [Critical] Revenue attribution is not configured in Klaviyo.

---

## Section 18 — Billing Efficiency Review

| Field | Value |
|---|---|
| Plan Tier | Klaviyo Email — 50,000 profiles |
| Plan Profile Limit | 50,000 |
| Current Profile Count | 42,000 |
| Utilization | 84% |


---

## Section 19 — Compliance and Consent Review

> This section identifies potential compliance risk areas. It does not constitute legal advice. Consult qualified legal counsel for definitive guidance.

| Control | Status |
|---|---|
| SPF | ❌ Missing |
| DKIM | ❌ Missing |
| DMARC | ❌ Missing |
| Branded Sending Domain | ⚠️ No |
| SMS Consent Documented | N/A |

**Findings:**
- 🟠 [High] DMARC is not configured — required by Google and Yahoo for bulk senders as of 2024.

---

## Section 20 — 30/60/90 Day Action Plan

### Immediate (Do This Week)

| Priority | Action | Owner | Impact |
|---|---|---|---|
| Critical | Campaigns are sent to the full list rather than engaged segments. | Shared | High |
| Critical | DKIM authentication is missing — emails fail authentication checks. | Shared | High |
| High | No engaged segment infrastructure exists — campaigns cannot be targeted by engagement. | NP | High |
| Critical | Hard bounce rate is critically high — sender reputation is at risk. | Shared | High |
| Critical | Spam complaint rate exceeds Google's 0.1% threshold — inbox placement is at risk. | Shared | High |
| Critical | No Abandoned Cart flow exists — the highest-recovery automation is missing. | Shared | High |
| Critical | Over 60% of the list is dormant — the majority of emailable profiles are cold. | Shared | High |
| Critical | Revenue attribution is not configured — Klaviyo cannot measure ROI. | Shared | High |

### 30-Day Plan

| Priority | Action | Owner | Impact |
|---|---|---|---|
| High | Signup form opt-in rate is below 1% — the form is not converting. | Shared | High |
| High | Campaign frequency is too low — the list is under-monetized. | Shared | High |
| High | SMS is not enabled — this revenue channel is completely untapped. | Shared | High |
| High | No Browse Abandonment flow exists. | Shared | Medium |
| High | No Post-Purchase flow exists. | Shared | Medium |

### 60-Day Plan

| Priority | Action | Owner | Impact |
|---|---|---|---|
| Medium | No Winback flow exists — dormant subscribers are not being re-engaged. | Shared | Medium |

### 90-Day Plan

*No 90-day actions.*

---

## Section 21 — Estimated Opportunity Summary

Based on the 14 recommendations in this audit, **11 High-impact opportunities** have been identified.

| Scenario | Estimated Annual Revenue Lift |
|---|---|
| Conservative | $46,500–$88,500 / yr |
| Moderate | $88,500–$173,500 / yr |
| Optimistic | $173,500–$347,000 / yr |

Based on estimated annual Klaviyo revenue of **$225,000** (derived from monthly revenue range — actual Klaviyo revenue not provided).

*Revenue estimates are directional ranges only, based on industry benchmarks and comparable account improvements. They are not guarantees of results. Actual outcomes depend on implementation quality, market conditions, and account-specific factors. National Positions does not guarantee revenue outcomes.*

---

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

> **Disclaimer:** This audit is diagnostic and informational only. All findings are based on data available at the time of the audit. Revenue opportunity estimates are directional ranges only and are not guarantees of results. National Positions does not make changes to your Klaviyo account without your explicit authorization. This audit does not constitute legal, compliance, or financial advice.

*Prepared by Klaviyo Audit Katie | National Positions | 2026-05-10*
