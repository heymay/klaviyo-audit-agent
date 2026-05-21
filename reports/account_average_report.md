# Klaviyo Account Audit Report

**CONFIDENTIAL** — Prepared for internal review and client delivery by National Positions

| Field | Value |
|---|---|
| Client / Brand | Solara Skincare |
| Website | solaraskincare.com |
| Klaviyo Account | Solara Skincare — Klaviyo |
| Audit Period | Last 12 months (365 days) |
| Ecommerce Platform | Shopify |
| Date Generated | 2026-05-10 |
| Prepared By | Klaviyo Audit Katie — National Positions |
| Approved By | [NP Reviewer Name — required before delivery] |

---

## Section 2 — Klaviyo Health Score: 56/100 — ⚠️ Weak

This account scored **56 out of 100** — rated **Weak**.

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
| Deliverability Health | 8/10 | 15% | 12.0 |
| Core Flow Coverage | 5/10 | 15% | 7.5 |
| Flow Configuration Quality | 5/10 | 15% | 7.5 |
| Campaign Strategy | 7/10 | 12% | 8.4 |
| SMS Adoption | 3/10 | 10% | 3.0 |
| Signup Forms & List Growth | 5/10 | 10% | 5.0 |
| List Health & Engagement | 4/10 | 10% | 4.0 |
| Segmentation Quality | 8/10 | 6% | 4.8 |
| Revenue Attribution | 6/10 | 5% | 3.0 |
| Billing Efficiency | 5/10 | 2% | 1.0 |
| **COMPOSITE TOTAL** | — | 100% | **56/100** |

---

## Section 4 — Executive Summary

This Klaviyo audit covers last 12 months of account activity for **Solara Skincare** across campaigns, flows, forms, list health, deliverability, SMS adoption, segmentation, and revenue attribution.

The account scored **56/100** (Weak), with **0 Critical** and **8 High** priority findings. The most impactful opportunities center on the areas highlighted in Sections 5–7.

---

## Section 5 — Top 5 Wins

1. **Deliverability Health** (8/10) — Performing at or above benchmark.
2. **Segmentation Quality** (8/10) — Engaged 30-day segment exists; Engaged 90-day segment exists; Purchaser/customer segment exists
3. **Campaign Strategy** (7/10) — Performing at or above benchmark.

---

## Section 6 — Top 5 Issues

1. 🟠 **[High] SMS-004** — SMS is enabled but no live flows include SMS messages.
   - *Business Impact:* SMS in flows (especially Abandoned Cart) typically generates 15–25% higher recovery rates than email alone.
   - *Action:* Add at least one SMS touchpoint to the Abandoned Cart and Welcome flows within 30 days.

2. 🟠 **[High] CAMP-004** — Only 35% of campaigns target engaged segments — below the 50% benchmark.
   - *Business Impact:* Sending to unengaged profiles inflates complaint rates and suppresses deliverability.
   - *Action:* Increase engaged-segment targeting to 75%+ of campaigns within 60 days.

3. 🟠 **[High] DELV-007** — DMARC policy is not configured.
   - *Business Impact:* DMARC is required by Google and Yahoo for bulk senders. Absence risks delivery issues.
   - *Action:* Implement a DMARC record (p=none initially) and monitor alignment. Escalate to p=quarantine within 60 days.

4. 🟠 **[High] FLOW-007** — No Browse Abandonment flow is live.
   - *Business Impact:* Browse abandonment flows target high-intent visitors before they leave — typically 2–5% conversion.
   - *Action:* Build a 2-email Browse Abandonment flow triggered by Viewed Product event. Send first email within 1 hour.

5. 🟠 **[High] LIST-002** — Suppression rate is 11.6% — above the 10% concern threshold.
   - *Business Impact:* A growing suppression rate indicates ongoing deliverability issues or acquisition quality problems.
   - *Action:* Review suppression growth trend. Audit acquisition sources adding invalid or spam-trap addresses.

---

## Section 7 — Top 5 Revenue Opportunities

1. **SMS is not used in any live flows.**
   - *Why it matters:* SMS in flows (especially Abandoned Cart) increases recovery rate by 15–25% over email alone.
   - *Opportunity:* Adding one SMS touchpoint to the Abandoned Cart flow alone can generate meaningful monthly revenue lift.
   - *Next step:* Add an SMS message 30–60 minutes after the abandoned cart trigger, before the first email.
   - Impact: **High** | Complexity: Easy | Timeline: 30 days

2. **Campaigns are sent to the full list rather than engaged segments.**
   - *Why it matters:* Full-list sends damage deliverability, suppress open rates, and inflate complaint rates — a compounding problem.
   - *Opportunity:* Shifting to engaged-segment sends will improve open rates, reduce complaints, and protect sender reputation.
   - *Next step:* Create engaged 30/90/180-day segments immediately. Mandate that all campaigns target one of these segments.
   - Impact: **High** | Complexity: Easy | Timeline: Immediate

3. **DKIM authentication is missing — emails fail authentication checks.**
   - *Why it matters:* Google and Yahoo require DKIM for bulk senders. Missing DKIM risks filtering or rejection.
   - *Opportunity:* Authentication is table stakes — all other improvements depend on emails reaching the inbox.
   - *Next step:* Configure DKIM in Klaviyo (Settings → Email → Sending Domain). Verify DNS propagation within 48 hours.
   - Impact: **High** | Complexity: Easy | Timeline: Immediate

4. **No engaged segment infrastructure exists — campaigns cannot be targeted by engagement.**
   - *Why it matters:* Engagement-based segmentation is the single most impactful deliverability and revenue lever available.
   - *Opportunity:* Creating engagement segments costs nothing and can be done in under 30 minutes — the ROI is immediate.
   - *Next step:* Create 4 segments: Engaged 30d, Engaged 90d, Engaged 180d, Never Engaged. Use these for all campaign targeting.
   - Impact: **High** | Complexity: Easy | Timeline: Immediate

5. **Over 60% of the list is dormant — the majority of emailable profiles are cold.**
   - *Why it matters:* Sending to dormant subscribers suppresses engagement rates, inflates billing, and damages deliverability.
   - *Opportunity:* Cleaning the list improves all engagement metrics, reduces billing costs, and protects sender reputation.
   - *Next step:* Immediately stop sending to 180+ day non-openers. Run a 3-email winback campaign. Suppress non-responders permanently.
   - Impact: **High** | Complexity: Moderate | Timeline: Immediate

---

## Section 8 — SMS Audit

**SMS Enabled:** Yes
**SMS Consented Profiles:** 7,500 (8.9% of emailable list)
**SMS in Flows:** No
**SMS Campaigns (audit period):** 4

**Findings:**
- 🟠 [High] SMS is enabled but no live flows include SMS messages.
- 🟡 [Medium] SMS consent rate is 8.9% — below the 15% benchmark for growing programs.

---

## Section 9 — Campaign Strategy Audit

| Metric | Value |
|---|---|
| Total Campaigns (period) | 62 |
| Email Campaigns | 58 |
| SMS Campaigns | 4 |
| Campaigns per Week | 1.2 |
| Avg Open Rate | 22.0% |
| Avg Click Rate | 2.5% |
| Avg Unsubscribe Rate | 0.25% |
| Avg Spam Complaint Rate | 0.045% |
| Avg Hard Bounce Rate | 0.55% |
| % Sent to Engaged Segments | 35% |
| Open Rate Trend | Flat |
| Longest Send Gap | 18 days |

**Findings:**
- 🟠 [High] Only 35% of campaigns target engaged segments — below the 50% benchmark.

---

## Section 10 — Deliverability Audit

| Metric | Value | Status |
|---|---|---|
| Hard Bounce Rate | 0.55% | ✅ OK |
| Soft Bounce Rate | 0.30% | — |
| Spam Complaint Rate | 0.045% | ✅ OK |
| Unsubscribe Rate | 0.25% | ✅ OK |
| SPF | ✅ Configured | — |
| DKIM | ✅ Configured | — |
| DMARC | 🔴 Missing | — |
| Branded Sending Domain | ✅ Yes | — |

**Findings:**
- 🟠 [High] DMARC policy is not configured.

---

## Section 11 — Core Flow Coverage

| Flow | Status | Revenue | Emails | SMS |
|---|---|---|---|---|
| Welcome Series | ✅ Live | $38,500 | 3 | 0 |
| Abandoned Cart | ✅ Live | $72,000 | 2 | 0 |
| Added to Cart | ❌ Missing | — | — | — |
| Browse Abandonment | ❌ Missing | — | — | — |
| Post-Purchase | ✅ Live | $22,000 | 2 | 0 |
| Winback / Re-engagement | ❌ Missing | — | — | — |
| VIP / Loyalty | ❌ Missing | — | — | — |

**Findings:**
- 🟠 [High] No Browse Abandonment flow is live.
- 🟡 [Medium] No Winback / Re-engagement flow is live.
- 🟡 [Medium] No Added to Cart flow is live.

---

## Section 12 — Flow Configuration Audit

### Welcome Series
- Status: Live | Emails: 3 | SMS: 0
- First message delay: 5 minutes
- Has incentive: Yes
- Last updated: 90 days ago

### Abandoned Cart Recovery
- Status: Live | Emails: 2 | SMS: 0
- First message delay: 60 minutes
- Has incentive: Yes
- Last updated: 60 days ago

### Post-Purchase Thank You
- Status: Live | Emails: 2 | SMS: 0
- First message delay: 30 minutes
- Has incentive: No
- Last updated: 180 days ago

---

## Section 13 — Signup Form Audit

**Active Forms:** 2

| Form | Type | Opt-In Rate | Mobile Opt-In | SMS Capture | Incentive |
|---|---|---|---|---|---|
| Homepage Popup | popup | 2.20% | 1.60% | Yes | Yes |
| Footer Embed | embed | 0.50% | 0.40% | No | No |


---

## Section 14 — Benchmark Review

| Metric | Rating |
|---|---|
| Open Rate | Average |
| Click Rate | Average |
| Conversion Rate | Average |
| Flow Revenue | Below Average |
| List Growth | Average |
| **Overall** | **Average** |

---

## Section 15 — List Health Review

| Metric | Value |
|---|---|
| Total Profiles | 95,000 |
| Emailable Profiles | 84,000 |
| SMS Consented | 7,500 (8.9%) |
| Suppressed | 11,000 (11.6%) |
| Engaged (30 days) | 9,200 (11.0%) |
| Engaged (90 days) | 26,500 (31.5%) |
| Dormant (180+ days) | 43,000 (51.2%) |

**Findings:**
- 🟠 [High] Suppression rate is 11.6% — above the 10% concern threshold.
- 🟠 [High] Dormant rate is 51.2% — a large portion of the list is cold.

---

## Section 16 — Segmentation Review

| Segment | Exists |
|---|---|
| Engaged 30-day | ✅ |
| Engaged 90-day | ✅ |
| VIP / High-Value | ❌ |
| Purchaser / Customer | ✅ |
| Sunset / Hygiene | ❌ |
| % Campaigns to Engaged | 35% |

**Findings:**
- 🟡 [Medium] No VIP or high-value customer segment exists.
- 🟡 [Medium] No sunset / list hygiene segment exists.

---

## Section 17 — Revenue Attribution Review

| Metric | Value |
|---|---|
| Total Klaviyo Revenue | $317,500 |
| Flow Revenue | $132,500 (42%) |
| Campaign Revenue | $185,000 (58%) |
| Attribution Configured | Yes |


---

## Section 18 — Billing Efficiency Review

| Field | Value |
|---|---|
| Plan Tier | Klaviyo Email + SMS — 100,000 profiles |
| Plan Profile Limit | 100,000 |
| Current Profile Count | 95,000 |
| Utilization | 95% |

**Findings:**
- 🟠 [High] Profile count (95,000) is at 95% of the plan limit (100,000).

---

## Section 19 — Compliance and Consent Review

> This section identifies potential compliance risk areas. It does not constitute legal advice. Consult qualified legal counsel for definitive guidance.

| Control | Status |
|---|---|
| SPF | ✅ Configured |
| DKIM | ✅ Configured |
| DMARC | ❌ Missing |
| Branded Sending Domain | ✅ Yes |
| SMS Consent Documented | ✅ Yes |

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
| Critical | Over 60% of the list is dormant — the majority of emailable profiles are cold. | Shared | High |

### 30-Day Plan

| Priority | Action | Owner | Impact |
|---|---|---|---|
| High | SMS is not used in any live flows. | Shared | High |
| High | No Browse Abandonment flow exists. | Shared | Medium |
| High | SMS consent rate is critically low — the SMS list is too small to drive meaningful revenue. | Shared | Medium |

### 60-Day Plan

| Priority | Action | Owner | Impact |
|---|---|---|---|
| Medium | No Winback flow exists — dormant subscribers are not being re-engaged. | Shared | Medium |

### 90-Day Plan

*No 90-day actions.*

---

## Section 21 — Estimated Opportunity Summary

Based on the 8 recommendations in this audit, **5 High-impact opportunities** have been identified.

Addressing the critical and high-priority items in this report — particularly around flows, deliverability, and segmentation — is expected to generate meaningful revenue improvement. Typical outcomes for accounts at this maturity level include:

- **Conservative:** 10–20% lift in email-attributed revenue within 90 days
- **Moderate:** 20–40% lift within 6 months with full flow and segmentation buildout
- **Optimistic:** 40–80% lift within 12 months with SMS launch, flow optimization, and ongoing campaign strategy

> **Disclaimer:** This audit is diagnostic and informational only. All findings are based on data available at the time of the audit. Revenue opportunity estimates are directional ranges only and are not guarantees of results. National Positions does not make changes to your Klaviyo account without your explicit authorization. This audit does not constitute legal, compliance, or financial advice.

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
