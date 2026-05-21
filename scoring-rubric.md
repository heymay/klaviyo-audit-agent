# Klaviyo Audit Katie — Scoring Rubric

**Version:** 1.0
**Owner:** National Positions
**Classification:** Internal Operating Framework — Phase 1
**Last Updated:** 2026-05-10

---

## Overview

The scoring rubric defines how Katie evaluates and scores every audit. It produces two output types:

1. **Category Scores** — Each of the 10 scored categories is evaluated independently on a 1–10 scale
2. **Composite Klaviyo Health Score** — Weighted aggregate of all category scores, expressed as 0–100

Scoring is evidence-based. Every score must be accompanied by a written justification citing specific findings from the account's data. Integer scores only — no decimals.

---

## Composite Klaviyo Health Score Structure

### Category Weights

| # | Category | Weight | Max Weighted Points |
|---|---|---|---|
| 1 | Deliverability Health | 15% | 15 |
| 2 | Core Flow Coverage | 15% | 15 |
| 3 | Flow Configuration Quality | 15% | 15 |
| 4 | Campaign Strategy & Consistency | 12% | 12 |
| 5 | SMS Adoption & Usage | 10% | 10 |
| 6 | Signup Forms & List Growth | 10% | 10 |
| 7 | List Health & Engagement | 10% | 10 |
| 8 | Segmentation Quality | 6% | 6 |
| 9 | Revenue Attribution & Benchmarks | 5% | 5 |
| 10 | Billing Efficiency | 2% | 2 |
| | **TOTAL** | **100%** | **100** |

### Composite Score Calculation

```
Composite Score = Σ (Category Score / 10 × Category Weight × 100)

Example:
Deliverability Health:        6/10 × 15% = 9.0
Core Flow Coverage:           4/10 × 15% = 6.0
Flow Configuration Quality:   3/10 × 15% = 4.5
Campaign Strategy:            7/10 × 12% = 8.4
SMS Adoption:                 1/10 × 10% = 1.0
Signup Forms & List Growth:   5/10 × 10% = 5.0
List Health & Engagement:     6/10 × 10% = 6.0
Segmentation Quality:         4/10 × 6%  = 2.4
Revenue Attribution:          5/10 × 5%  = 2.5
Billing Efficiency:           7/10 × 2%  = 1.4
COMPOSITE SCORE = 46.2 → 46 / 100
```

Round composite score to the nearest whole number.

---

## Score Bands

| Score Range | Band Label | Client Communication | Urgency |
|---|---|---|---|
| 90–100 | **Elite** | "Your Klaviyo account is performing at a best-in-class level. Focus is on growth, refinement, and competitive edge." | Maintenance + strategic expansion |
| 75–89 | **Strong** | "Strong foundation in place with clear opportunities to push performance further." | Systematic optimization |
| 60–74 | **Average** | "Solid base with meaningful gaps that are limiting your email and SMS revenue." | Prioritized improvement |
| 40–59 | **Weak** | "Significant issues are preventing your Klaviyo account from performing at its potential. Action required." | Urgent remediation |
| 0–39 | **Critical** | "Critical gaps exist across multiple categories. Your account is likely missing substantial revenue. Immediate intervention needed." | Emergency intervention |

---

## Severity Level Definitions

Every individual finding is assigned a severity level independently of its category score.

| Severity | Definition | Client Communication |
|---|---|---|
| **Critical** | Actively blocking revenue, creating deliverability risk, or representing a major lifecycle gap | Escalate immediately — address within 30 days |
| **High** | Significantly limiting performance — measurably suppressing revenue or deliverability | Address in 30/60-day roadmap |
| **Medium** | Meaningful optimization gap — fixing it produces measurable improvement | Address in 60-day roadmap |
| **Low** | Best practice gap or marginal opportunity — real but not urgent | Address in 90-day roadmap or maintenance sprint |

---

## Confidence Levels

Confidence levels document the quality of evidence behind each finding. Confidence does NOT change severity — an inferred Critical finding is still Critical.

| Confidence | Definition |
|---|---|
| **Confirmed** | Finding is based on directly observed data from the Klaviyo API |
| **Likely** | Finding is based on partial data or reasonable inference from available data |
| **Inferred** | Finding is based on absence of data (e.g., a flow not appearing in the API suggests it doesn't exist) |

---

## Missing Data Handling

When data is unavailable for a category:
- Do not score the category if no data is accessible
- Mark the category as "Incomplete — Data Unavailable" in the report
- Reduce the overall composite score confidence level to "Partial"
- Flag the missing data as a gap to resolve in the 30-day action plan

When data is partially available:
- Score based on available data only
- Note the data gap in the justification
- Assign a "Likely" or "Inferred" confidence level

---

## Category 1 — Deliverability Health (Weight: 15%)

**What Is Scored:** Bounce rates, spam complaint rates, unsubscribe rates, sending domain authentication (SPF/DKIM/DMARC), branded sending domain, and list hygiene signals.

| Score | Criteria |
|---|---|
| **9–10** | All rates excellent (spam < 0.02%, hard bounce < 0.2%, unsubscribe < 0.1%). SPF, DKIM, DMARC all in place. Branded/dedicated sending domain in use. No deliverability flags. |
| **7–8** | Rates within acceptable range. At least SPF and DKIM in place. DMARC may be missing or at p=none. Branded domain in use or in progress. Minor list hygiene opportunity. |
| **5–6** | One or two metrics elevated (unsubscribe 0.3–0.5%, bounce 0.5–1%, or spam 0.05–0.1%). At least SPF in place. No DMARC or branded domain. Some list hygiene work needed. |
| **3–4** | Elevated metrics across multiple areas. Spam complaint rate approaching 0.1%. Missing DKIM or DMARC. No branded domain. Active deliverability risk. |
| **1–2** | Spam complaint rate > 0.1% (Critical threshold). Hard bounce rate > 1%. Missing SPF and/or DKIM. No branded domain. Significant risk of inbox placement failure or account suspension. |

**Special Rules:**
- Spam complaint rate > 0.3% → automatic score cap of 2/10 (Critical severity)
- Hard bounce rate > 2% → automatic score cap of 3/10
- Missing DKIM AND SPF → minimum -2 point deduction regardless of other factors
- Branded sending domain in use → +1 bonus point (max 10)

---

## Category 2 — Core Flow Coverage (Weight: 15%)

**What Is Scored:** Existence and Live status of the 7 core lifecycle flows.

| Score | Criteria |
|---|---|
| **9–10** | All 7 core flows exist and are Live (Welcome, Abandoned Cart, Added to Cart, Browse Abandonment, Post-Purchase, Winback, VIP). Replenishment flow may also be present. |
| **7–8** | 5–6 of 7 core flows exist and are Live. Missing one may be VIP or Replenishment (lower priority). |
| **5–6** | 4 core flows exist and are Live. May be missing Browse Abandonment, Winback, or VIP. |
| **3–4** | 2–3 core flows exist. Critical flows (Abandoned Cart, Welcome) exist but several others are missing. |
| **1–2** | 0–1 core flows exist, OR critical flows (Welcome, Abandoned Cart) are missing entirely. |

**Special Rules:**
- Missing Welcome flow → automatic score cap of 4/10 (regardless of other flows)
- Missing Abandoned Cart flow → automatic score cap of 4/10
- Missing both Welcome AND Abandoned Cart → automatic score cap of 3/10
- Flows in Draft or Manual status do not count as "existing" — only Live flows qualify
- Added to Cart and Browse Abandonment together count as one "unit" if both are missing

---

## Category 3 — Flow Configuration Quality (Weight: 15%)

**What Is Scored:** Message count, email/SMS mix, timing correctness, incentive structure, and revenue contribution across all Live flows.

| Score | Criteria |
|---|---|
| **9–10** | All core flows meet minimum message counts. Abandoned cart fires within 1 hour. SMS is present in all transactional flows. Incentives are used in messages 2–3 of transactional flows. Flows generate healthy revenue relative to account size. |
| **7–8** | Most flows meet minimum message counts. Timing is mostly correct. SMS present in primary flows (at minimum abandoned cart). Some incentive gaps. Flow revenue is developing. |
| **5–6** | Some flows meet standards; others are underdeveloped. Abandoned cart may have 1–2 emails only. SMS absent from some flows. Timing may be off. Revenue is low but flows exist and are running. |
| **3–4** | Most flows are underbuilt (1 email only, no SMS, no incentive). Timing is incorrect on key flows. Minimal revenue contribution. Flows exist but are not performing. |
| **1–2** | Flows are mostly empty, non-functional, or extremely underdeveloped. No SMS anywhere. No incentives. First abandoned cart email delayed by 6+ hours. Revenue near zero. |

**Special Rules:**
- Abandoned cart first email delayed > 4 hours → -2 points from this category
- No SMS in any flow despite SMS being enabled → -2 points
- Welcome flow with fewer than 3 emails → -1 point
- Abandoned cart with fewer than 2 emails → -2 points

---

## Category 4 — Campaign Strategy & Consistency (Weight: 12%)

**What Is Scored:** Campaign send frequency, segmentation quality, open/click/spam/unsubscribe rate performance, and overall strategy coherence.

| Score | Criteria |
|---|---|
| **9–10** | 1–3 campaigns per week, consistently. Campaigns targeted to engaged segments. Open rates ≥ 25%. Click rates ≥ 2%. Spam complaints < 0.05%. Clear strategic variety (promotional, nurture, educational). |
| **7–8** | 1–2 campaigns per week with reasonable consistency. Mostly engaged-segment targeting. Open rates 15–25%. Click rates 1–2%. Spam below 0.1%. Strategy is present but not fully varied. |
| **5–6** | Campaigns sent 2–3 times per month. Some segmentation but broad list sends common. Open rates 10–20%. Click rates 0.5–1.5%. Unsubscribes 0.3–0.5%. Strategy is promotional-only. |
| **3–4** | Infrequent campaigns (< 2/month) OR too frequent to broad lists (> 5/week). Poor segmentation. Open rates < 15%. Elevated spam or unsubscribes. No clear strategy. |
| **1–2** | No campaigns sent in 60+ days OR campaigns blasted to entire list every day. Open rates < 10%. Spam complaints elevated. No segmentation. |

**Special Rules:**
- Campaign spam complaint rate > 0.1% → automatic score cap of 4/10 (overlaps with Deliverability category)
- No campaigns in 90+ days → automatic score cap of 2/10
- All campaigns sent to 100% of list with no segmentation → -2 points

---

## Category 5 — SMS Adoption & Usage (Weight: 10%)

**What Is Scored:** Whether SMS is enabled, SMS consent rate, SMS in flows, SMS in campaigns, and overall SMS program maturity.

| Score | Criteria |
|---|---|
| **9–10** | SMS fully active. ≥ 20% of emailable profiles are SMS consented. SMS is in all core flows. SMS campaigns run regularly. SMS list growing. SMS opt-in on all signup forms. |
| **7–8** | SMS active. 10–20% SMS consent rate. SMS in primary flows (cart, welcome). Some SMS campaigns. Form includes SMS opt-in. |
| **5–6** | SMS active. 5–10% consent rate. SMS present in some flows. Limited SMS campaigns. Form may not have SMS opt-in. |
| **3–4** | SMS active but underdeveloped. < 5% consent rate. SMS not in flows or campaigns. No SMS opt-in on forms. |
| **1–2** | SMS not enabled at all, OR SMS account suspended / inactive. No SMS list. No SMS flows. No SMS campaigns. |

**Special Rules:**
- SMS not enabled → automatic score of 1/10 (Critical gap)
- SMS enabled but < 2% of profiles consented → score cap of 3/10
- SMS enabled but used in zero flows AND zero campaigns → score cap of 4/10

---

## Category 6 — Signup Forms & List Growth (Weight: 10%)

**What Is Scored:** Form existence, form opt-in rate, SMS capture, mobile performance, incentive quality, and display rules.

| Score | Criteria |
|---|---|
| **9–10** | Active popup and/or flyout with ≥ 6% opt-in rate. Email + SMS capture. Strong incentive. Exit-intent or scroll-triggered timing. Mobile optimized. A/B testing active. |
| **7–8** | Active signup form with 4–5.9% opt-in rate. Email + SMS capture or just email. Good incentive. Reasonable display timing. Mobile renders well. |
| **5–6** | Active form with 2–3.9% opt-in rate. Email capture only. Incentive present. Display timing may not be optimized. Mobile acceptable. |
| **3–4** | Active form with < 2% opt-in rate, OR form exists but collects email only with no incentive. Mobile may be broken or not tested. |
| **1–2** | No active signup form at all, OR form has < 0.5% opt-in rate and email only with no incentive. |

**Special Rules:**
- No active signup form → automatic score of 1/10 (Critical gap)
- Form opt-in rate < 2% → score cap of 3/10
- Form collects email only (no SMS) → -1 point from this category
- Mobile opt-in rate < 1% → -1 point

---

## Category 7 — List Health & Engagement (Weight: 10%)

**What Is Scored:** Engaged profile ratios, dormant profile ratio, suppression rate, and suppression growth trend.

| Score | Criteria |
|---|---|
| **9–10** | Engaged 90-day > 40% of emailable list. Engaged 30-day > 20%. Dormant rate < 20%. Suppression rate < 10%. Suppression stable or declining. |
| **7–8** | Engaged 90-day 25–40%. Engaged 30-day 10–20%. Dormant 20–35%. Suppression 10–15%. Stable. |
| **5–6** | Engaged 90-day 15–25%. Dormant 35–50%. Suppression 15–20%. List growing but engagement not keeping pace. |
| **3–4** | Engaged 90-day < 15%. Dormant 50–65%. Suppression 20–30%. Suppression growing. Active list health problem. |
| **1–2** | Engaged 90-day < 5%. Dormant > 65%. Suppression > 30%. List is critically degraded. Deliverability at risk. |

**Special Rules:**
- Dormant rate > 70% → automatic score cap of 2/10
- Suppression growing by > 5% month-over-month → -2 points
- Engaged 30-day segment < 3% of emailable list → -2 points

---

## Category 8 — Segmentation Quality (Weight: 6%)

**What Is Scored:** Whether engagement-based segments exist and are used in campaigns, whether purchaser/VIP segments exist, and the overall sophistication of the segmentation strategy.

| Score | Criteria |
|---|---|
| **9–10** | Engaged 30/60/90-day segments in active use. Purchaser segment. VIP/high-LTV segment. Category interest segments. Predictive analytics segments (if on qualifying plan). Campaigns consistently targeted to right segments. |
| **7–8** | Engaged segments in use. Purchaser segment exists. Some campaign targeting by segment. VIP segment developing. |
| **5–6** | Engaged segment exists but inconsistently used. No purchaser or VIP segment. Campaigns sometimes targeted, sometimes blasted. |
| **3–4** | Minimal segmentation. No engagement-based targeting. Campaigns sent to full list. Possibly a few static lists. |
| **1–2** | No meaningful segmentation. All campaigns to full unfiltered list. No engagement-based segments. |

---

## Category 9 — Revenue Attribution & Benchmarks (Weight: 5%)

**What Is Scored:** Flow revenue as % of total Klaviyo revenue, campaign revenue health, benchmark performance ratings, and overall revenue attribution clarity.

| Score | Criteria |
|---|---|
| **9–10** | Flow revenue ≥ 40% of Klaviyo revenue. Most benchmark ratings are Good or Excellent. Revenue per recipient strong. Email + SMS revenue both attributable. |
| **7–8** | Flow revenue 25–40%. Benchmark ratings mostly Average or Good. Revenue per recipient healthy. Clear attribution setup. |
| **5–6** | Flow revenue 15–25%. Mixed benchmark ratings (Average with some Below Average). Revenue attribution is set up but flows underperform. |
| **3–4** | Flow revenue < 15%. Benchmark ratings mostly Below Average or Poor. Limited revenue from flows. Campaign-dependent revenue model. |
| **1–2** | Flow revenue near zero. No benchmark data available or all ratings are Poor. No SMS revenue. Revenue entirely campaign-driven. |

---

## Category 10 — Billing Efficiency (Weight: 2%)

**What Is Scored:** Billing utilization rate (active profiles vs. plan limit) and overpay risk.

| Score | Criteria |
|---|---|
| **9–10** | Billing utilization 60–85% of plan limit. Plan tier matches active audience well. No significant overpay. |
| **7–8** | Utilization 40–60% or 85–95%. Plan is reasonably matched to usage. |
| **5–6** | Utilization 25–40% or approaching 95%+. Some inefficiency or upgrade risk. |
| **3–4** | Utilization < 25% (paying for significantly more than being used) or > 95% (immediate upgrade needed). |
| **1–2** | Utilization < 10% — severe overpay risk — paying for 10× the active audience. OR billing data unavailable for review. |

---

## Penalty Logic Summary

| Condition | Penalty |
|---|---|
| No SMS enabled | SMS category score fixed at 1/10 |
| No active signup form | Forms category score fixed at 1/10 |
| Missing Welcome flow | Core Flow Coverage score capped at 4/10 |
| Missing Abandoned Cart flow | Core Flow Coverage score capped at 4/10 |
| Missing both Welcome + Cart | Core Flow Coverage score capped at 3/10 |
| Spam complaint rate > 0.3% | Deliverability score capped at 2/10 |
| Hard bounce rate > 2% | Deliverability score capped at 3/10 |
| Form opt-in rate < 2% | Forms score capped at 3/10 |
| No campaigns in 90+ days | Campaign score capped at 2/10 |
| Dormant rate > 70% | List Health score capped at 2/10 |

---

## Bonus Logic

| Condition | Bonus |
|---|---|
| Branded/dedicated sending domain in use | +1 point to Deliverability (max 10) |
| Form opt-in rate ≥ 6% | +1 point to Forms (max 10) |
| SMS consent rate ≥ 25% | +1 point to SMS (max 10) |
| All 7 core flows Live AND all meeting minimum message counts | +1 point to Core Flow Coverage (max 10) |
| Flow revenue > 50% of Klaviyo revenue | +1 point to Revenue Attribution (max 10) |

---

## Scoring Constraints

1. All category scores are integers between 1 and 10. No scores of 0.
2. Composite score is rounded to the nearest whole number.
3. Every score must be accompanied by a 2–4 sentence written justification citing specific data.
4. Penalties and bonuses are applied after the initial score is assigned, not before.
5. If a penalty would reduce a score below 1, the score is fixed at 1.
6. If a bonus would increase a score above 10, the score is fixed at 10.
7. Scores marked as "Inferred" (due to missing data) must be flagged as lower confidence in the report.

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-05-10 | Initial scoring rubric — Phase 1 |
