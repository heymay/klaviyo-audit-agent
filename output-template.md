# Klaviyo Audit Katie — Audit Output Template

**Version:** 1.0
**Owner:** National Positions
**Classification:** Internal Operating Framework — Phase 1
**Audience:** Client-Facing (Executive + Marketing Team) after human review
**Last Updated:** 2026-05-10

---

## Document Header (Required on Every Audit)

```
KLAVIYO AUDIT REPORT
Prepared by: National Positions — Klaviyo Audit Katie
Client: [Client Brand Name]
Website: [Root Domain URL]
Klaviyo Account: [Klaviyo Account Name / ID]
Audit Period: [Start Date] to [End Date]
Comparison Period: [Prior Period] or [Year Over Year] or [N/A]
Data Sources: Klaviyo API (read-only) | [Any manual data provided]
Date Generated: [YYYY-MM-DD]
Prepared For: [Client Contact Name, Title]
Approved By: [NP Marketing Automation Strategist Name]
Confidentiality: This document is confidential and intended for [Client Brand Name] only.
```

---

## Section 1 — Audit Snapshot

*One-paragraph plain-English summary. Write for a business owner, not a platform specialist.*

**Template:**
> [Brand Name]'s Klaviyo account received an overall Health Score of [X]/100 — placing it in the [Score Band] range. The audit covered [X] campaigns, [X] flows, [X] signup forms, and [X] audience segments over the period from [Start] to [End]. The most significant opportunities identified are [top 2–3 findings in plain English]. This report outlines a prioritized 90-day plan to address the highest-impact gaps and position [Brand Name] for stronger retention revenue.

---

## Section 2 — Overall Klaviyo Health Score

```
KLAVIYO HEALTH SCORE

[SCORE] / 100

Score Band: [Elite / Strong / Average / Weak / Critical]

[0 ——————————————————— 100]
         [Current Score Position]
```

**Score Band Communication:**

| Band | Range | What It Means |
|---|---|---|
| Elite | 90–100 | Best-in-class. Optimize for growth and competitive edge. |
| Strong | 75–89 | Strong foundation with clear opportunities to push further. |
| Average | 60–74 | Solid base with meaningful gaps limiting email and SMS revenue. |
| Weak | 40–59 | Significant issues preventing Klaviyo from performing at its potential. |
| Critical | 0–39 | Critical gaps across multiple categories. Likely missing substantial revenue. |

**Benchmark Note:** [Brief comparison to industry average if available — e.g., "The average Klaviyo Health Score for similar ecommerce accounts is approximately 62/100."]

---

## Section 3 — Score Breakdown by Category

| # | Category | Score (/10) | Weight | Weighted Points |
|---|---|---|---|---|
| 1 | Deliverability Health | /10 | 15% | |
| 2 | Core Flow Coverage | /10 | 15% | |
| 3 | Flow Configuration Quality | /10 | 15% | |
| 4 | Campaign Strategy & Consistency | /10 | 12% | |
| 5 | SMS Adoption & Usage | /10 | 10% | |
| 6 | Signup Forms & List Growth | /10 | 10% | |
| 7 | List Health & Engagement | /10 | 10% | |
| 8 | Segmentation Quality | /10 | 6% | |
| 9 | Revenue Attribution & Benchmarks | /10 | 5% | |
| 10 | Billing Efficiency | /10 | 2% | |
| | **COMPOSITE SCORE** | | **100%** | **/100** |

**Score Justification Summary:**

*For each category, include 1–2 sentences explaining the score. Examples:*

- **Deliverability (X/10):** Spam complaint rate of 0.12% exceeds Gmail's 0.10% threshold. DKIM is in place but DMARC is missing and no branded sending domain is configured.
- **Core Flow Coverage (X/10):** Welcome and Abandoned Cart flows are live. Browse Abandonment, Added to Cart, Post-Purchase, and Winback flows do not exist.
- **SMS (X/10):** SMS is not enabled in the account. No SMS flows, no SMS campaigns, and no SMS opt-in on signup forms.

---

## Section 4 — Executive Summary

*This section must stand alone as a 1-page client communication. No technical jargon. Write for a CMO, VP of Ecommerce, or founder.*

### 4.1 What We Found

[3–5 sentence plain-English summary of the account's current Klaviyo health, the primary opportunities, and the single most important thing to change.]

### 4.2 The Opportunity

[2–3 sentences describing the revenue opportunity in directional, non-guaranteed terms.]

**Template:**
> Based on this audit, [Brand Name] has meaningful opportunities in [top 1–2 areas]. Accounts of similar size and category that address these gaps typically see improvement in [flow revenue contribution / SMS revenue / list growth / deliverability]. The 90-day plan in this report provides a clear path to capturing these opportunities.

### 4.3 What's Working

[Brief acknowledgment of what the account is doing well.]

---

## Section 5 — Top 5 Wins

*What the account is doing well. Frame as strengths to protect and build on.*

| # | Win | Why It Matters |
|---|---|---|
| 1 | [e.g., Welcome flow is live with 5 emails] | [e.g., New subscribers receive a structured onboarding sequence driving first-purchase conversion] |
| 2 | | |
| 3 | | |
| 4 | | |
| 5 | | |

---

## Section 6 — Top 5 Issues

*The highest-severity findings that most urgently need attention.*

| # | Issue | Severity | Category | Impact |
|---|---|---|---|---|
| 1 | [e.g., No SMS program] | Critical | SMS Adoption | Entire SMS revenue channel missing |
| 2 | | | | |
| 3 | | | | |
| 4 | | | | |
| 5 | | | | |

---

## Section 7 — Top 5 Revenue Opportunities

*The specific gaps with the highest estimated revenue recovery potential.*

| # | Opportunity | Estimated Impact | Complexity | Timeline |
|---|---|---|---|---|
| 1 | [e.g., Build full Abandoned Cart flow with SMS] | High | Moderate | 30 days |
| 2 | | | | |
| 3 | | | | |
| 4 | | | | |
| 5 | | | | |

*Note: Impact estimates are directional. A National Positions strategist should model specific projections with client data before making revenue commitments.*

---

## Section 8 — SMS Audit

### 8.1 SMS Status Summary

| Metric | Value | Status |
|---|---|---|
| SMS Enabled | Yes / No | |
| SMS-Consented Profiles | # | |
| SMS Consent Rate | % of emailable | |
| SMS Flows Active | # | |
| SMS Campaigns Sent (audit period) | # | |
| SMS Opt-In on Signup Forms | Yes / No | |
| SMS Revenue (if trackable) | $ | |

### 8.2 SMS Findings

[List all findings triggered by SMS rules with severity, impact, and recommended action.]

| Finding | Severity | Rule ID | Recommended Action |
|---|---|---|---|
| | | | |

### 8.3 SMS Score

**Score:** [X]/10
**Justification:** [2–3 sentences citing specific data from above.]

---

## Section 9 — Campaign Strategy Audit

### 9.1 Campaign Performance Summary

| Metric | Value | Benchmark / Target |
|---|---|---|
| Total Campaigns Sent | # | |
| Average Per Week | # | 1–3 |
| Email Campaigns | # | |
| SMS Campaigns | # | |
| Average Open Rate | % | ≥ 25% |
| Average Click Rate | % | ≥ 2% |
| Average Unsubscribe Rate | % | < 0.3% |
| Average Spam Complaint Rate | % | < 0.08% |
| % Campaigns to Engaged Segments | % | > 80% |
| Total Campaign Revenue | $ | |

### 9.2 Campaign Findings

[List findings triggered by Campaign rules.]

### 9.3 Campaign Score

**Score:** [X]/10
**Justification:** [2–3 sentences.]

---

## Section 10 — Deliverability Audit

### 10.1 Deliverability Health Level

**Overall Level:** [Critical / Needs Improvement / Acceptable / Strong]

### 10.2 Deliverability Metrics

| Metric | Value | Threshold | Status |
|---|---|---|---|
| Hard Bounce Rate | % | < 0.5% | |
| Soft Bounce Rate | % | < 1% | |
| Spam Complaint Rate | % | < 0.08% | |
| Unsubscribe Rate (avg per campaign) | % | < 0.3% | |
| SPF Record | Present / Missing | Required | |
| DKIM Record | Present / Missing | Required | |
| DMARC Record | Present / Missing | Recommended | |
| Branded Sending Domain | Yes / No | Recommended | |
| Open Rate Trend | Improving / Flat / Declining | | |

### 10.3 Deliverability Findings

[List findings triggered by DELV rules.]

### 10.4 Deliverability Score

**Score:** [X]/10
**Justification:** [2–3 sentences.]

---

## Section 11 — Core Flow Audit

### 11.1 Core Flow Existence Table

| Flow | Exists | Status | Last Updated | Revenue (Period) |
|---|---|---|---|---|
| Welcome Series | Yes / No | Live / Draft / Manual | | $ |
| Abandoned Cart | Yes / No | | | $ |
| Added to Cart | Yes / No | | | $ |
| Browse Abandonment | Yes / No | | | $ |
| Post-Purchase | Yes / No | | | $ |
| Winback / Re-engagement | Yes / No | | | $ |
| VIP / Loyalty | Yes / No | | | $ |

### 11.2 Core Flow Findings

[List all Critical and High flow coverage findings from FLOW rules.]

### 11.3 Core Flow Score

**Score:** [X]/10
**Justification:** [2–3 sentences noting which critical flows are missing and what the coverage gap means for revenue.]

---

## Section 12 — Flow Configuration Audit

### 12.1 Flow Configuration Detail

For each existing Live flow:

**[Flow Name] — [Status]**

| Attribute | Current | Target / Standard |
|---|---|---|
| Email Messages | # | [Minimum per rubric] |
| SMS Messages | # | [Minimum per rubric] |
| First Message Timing | [X hours/minutes] | [< 60 min for cart flows] |
| Delay Between Messages | [X hours] | [~24h for message 2] |
| Incentive Present | Yes / No | Recommended for cart flows |
| Revenue (Period) | $ | |
| Conversion Rate | % | |

### 12.2 Flow Configuration Findings

[List timing, structure, and channel mix findings from FTIM and FLOW rules.]

### 12.3 Flow Configuration Score

**Score:** [X]/10
**Justification:** [2–3 sentences.]

---

## Section 13 — Signup Form Audit

### 13.1 Form Performance Summary

| Form Name | Type | Status | Views | Submits | Opt-In Rate | SMS Capture | Incentive |
|---|---|---|---|---|---|---|---|
| | Popup / Flyout / Embed | Published / Draft | # | # | % | Yes / No | Yes / No |

**Overall Opt-In Rate:** [%] — [Weak / Average / Good / Excellent]
**Mobile Opt-In Rate:** [%]
**Desktop Opt-In Rate:** [%]

### 13.2 Form Findings

[List findings from FORM rules.]

### 13.3 Signup Forms Score

**Score:** [X]/10
**Justification:** [2–3 sentences.]

---

## Section 14 — Benchmark Review

### 14.1 Benchmark Performance Summary

| Metric | Account Value | Benchmark Rating | Industry Context |
|---|---|---|---|
| Campaign Open Rate | % | Poor / Below Avg / Average / Good / Excellent | |
| Campaign Click Rate | % | | |
| Campaign Conversion Rate | % | | |
| Flow Open Rate | % | | |
| Flow Click Rate | % | | |
| Flow Revenue per Recipient | $ | | |
| List Growth Rate | % | | |

*Note: Benchmark ratings sourced from Klaviyo's in-platform benchmarks where available. If unavailable via API, industry-standard benchmarks are used and labeled accordingly.*

### 14.2 Benchmark Findings

[Overall benchmark performance narrative — are most ratings Good/Excellent or Poor/Average?]

---

## Section 15 — List Health Review

### 15.1 List Health Summary

| Metric | Value | % of Emailable | Assessment |
|---|---|---|---|
| Total Profiles | # | | |
| Emailable Profiles | # | 100% | |
| Suppressed Profiles | # | % | |
| Engaged 30-Day | # | % | |
| Engaged 60-Day | # | % | |
| Engaged 90-Day | # | % | |
| Engaged 180-Day | # | % | |
| Dormant (180+ days) | # | % | |
| SMS Consented | # | % | |

### 15.2 List Health Findings

[List health findings from LIST rules. Include suppression trend if data supports it.]

### 15.3 List Health Score

**Score:** [X]/10
**Justification:** [2–3 sentences.]

---

## Section 16 — Segmentation Review

### 16.1 Segmentation Inventory

| Segment Name | Profile Count | Type | In Active Use for Campaigns |
|---|---|---|---|
| | # | Engagement / Behavioral / Static | Yes / No |

**Engagement-Based Segments Active:** Yes / No
**VIP Segment Active:** Yes / No
**Purchaser Segment Active:** Yes / No
**% of Campaigns Sent to Engaged Segments:** [%]

### 16.2 Segmentation Findings

[Findings from Campaign and List segmentation rules.]

### 16.3 Segmentation Score

**Score:** [X]/10
**Justification:** [2–3 sentences.]

---

## Section 17 — Revenue Attribution Review

### 17.1 Revenue Attribution Summary

| Source | Revenue (Period) | % of Total Klaviyo Revenue |
|---|---|---|
| Campaign Revenue (Email) | $ | % |
| Campaign Revenue (SMS) | $ | % |
| Flow Revenue (Email) | $ | % |
| Flow Revenue (SMS) | $ | % |
| **Total Klaviyo Revenue** | **$** | **100%** |

**Top 3 Revenue Flows:**
1. [Flow Name] — $[X] — [X]% of flow revenue
2.
3.

**Top 3 Revenue Campaigns:**
1. [Campaign Name / Date] — $[X]
2.
3.

### 17.2 Revenue Attribution Findings

[Revenue findings from REV rules.]

### 17.3 Revenue Attribution Score

**Score:** [X]/10
**Justification:** [2–3 sentences.]

---

## Section 18 — Billing Efficiency Review

### 18.1 Billing Summary

| Metric | Value | Notes |
|---|---|---|
| Plan Tier | [Name] | Requires manual verification if not via API |
| Plan Profile Limit | # | |
| Total Profiles in Account | # | |
| Emailable Profiles | # | |
| Billing Utilization Rate | % | |
| Overpay Risk | High / Medium / Low / None | |

*Note: Billing data may not be accessible via API. If not available, this section is based on manually provided plan information or is flagged for client confirmation.*

### 18.2 Billing Findings

[Findings from BILL rules.]

### 18.3 Billing Score

**Score:** [X]/10
**Justification:** [1–2 sentences.]

---

## Section 19 — Compliance and Consent Review

### 19.1 Compliance Status

| Area | Status | Notes |
|---|---|---|
| SPF Record | Present / Missing | |
| DKIM Record | Present / Missing | |
| DMARC Record | Present / Missing / p=none / p=quarantine / p=reject | |
| Branded Sending Domain | Yes / No | |
| SMS TCPA Consent Process | Present / Not Verified / Risk Flagged | |
| Unsubscribe Link in Emails | Present / Not Verified | |
| Physical Address in Footer | Present / Not Verified | |
| Double Opt-In | Enabled / Disabled | |
| GDPR Considerations | Not Applicable / Flagged for Review | |
| CCPA Considerations | Not Applicable / Flagged for Review | |

### 19.2 Compliance Findings

[Findings from COMP rules. Include severity and flag for legal review where required.]

**Disclaimer:** This compliance review identifies potential risks for further investigation. National Positions does not provide legal advice and cannot certify compliance. All compliance findings should be reviewed by qualified legal counsel.

---

## Section 20 — 30 / 60 / 90 Day Action Plan

### 30-Day Priorities (Critical and Quick Wins)

| # | Task | Owner | Effort | Estimated Impact | Dependencies |
|---|---|---|---|---|---|
| 1 | | NP / Client | Easy / Moderate / Complex | High / Medium / Low | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

### 60-Day Priorities (Core Build-Outs)

| # | Task | Owner | Effort | Estimated Impact | Dependencies |
|---|---|---|---|---|---|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

### 90-Day Priorities (Strategic Improvements)

| # | Task | Owner | Effort | Estimated Impact | Dependencies |
|---|---|---|---|---|---|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

**Owner Key:**
- **NP:** National Positions marketing automation team
- **Client:** Client-side team (IT, brand, ecommerce manager)
- **Shared:** Collaboration required

---

## Section 21 — Estimated Opportunity Summary

*All opportunity estimates are directional. They are not revenue guarantees.*

| Opportunity | Conservative Estimate | Moderate Estimate | Notes |
|---|---|---|---|
| Abandoned Cart Flow Rebuild | TBD | TBD | Estimate requires cart abandonment volume and current recovery rate |
| SMS Program Launch | TBD | TBD | Estimate based on SMS consent rate and AOV |
| Signup Form Optimization | TBD | TBD | Based on traffic volume and current opt-in rate vs. target |
| Welcome Flow Improvement | TBD | TBD | Based on subscriber acquisition rate and first-purchase conversion |
| Post-Purchase Flow Build | TBD | TBD | Based on customer volume and repeat purchase rate |

**Important Disclaimer:**
> Revenue opportunity estimates in this report are directional ranges based on industry averages, account-specific data, and National Positions' experience with similar ecommerce accounts. They are not guarantees of revenue improvement. Actual results depend on implementation quality, product economics, traffic volume, and market conditions. A National Positions strategist should validate and refine these estimates before they are used for planning or investment decisions.

---

## Section 22 — National Positions CTA

---

### Your Klaviyo Account Has Real Opportunities to Improve

This audit has identified [X] critical issues and [X] high-priority opportunities across your email and SMS program. The findings above point to meaningful gaps in [top 2–3 areas] that are limiting your retention revenue.

---

### What National Positions Can Do For You

National Positions' Marketing Automation team can help you:

- **Rebuild your core flows** — Welcome, Abandoned Cart, Browse Abandonment, Post-Purchase, Winback — with the right structure, timing, and copy
- **Launch or grow your SMS program** — from list building to flow integration to SMS campaign strategy
- **Improve deliverability** — set up DKIM, DMARC, branded sending domains, and list hygiene programs
- **Optimize your signup forms** — improve opt-in rates and add SMS capture
- **Build smart segmentation** — engaged segments, VIP tracks, purchaser targeting
- **Manage Klaviyo on an ongoing basis** — strategy, execution, and reporting

---

### Ready to Turn This Audit Into Revenue?

> **Schedule a consultation with National Positions' Marketing Automation team.**
>
> [CALENDLY LINK PLACEHOLDER]
>
> Or email us at: [NP Contact Email]
> Or visit: nationalpositions.com

We'll walk through your audit findings together and show you exactly what we'd prioritize to improve your Klaviyo performance.

---

**Disclaimer:**
> This audit is diagnostic and informational only. Findings are based on data available at the time of audit and are subject to change. Revenue opportunity estimates are directional and are not guarantees of results. National Positions does not make changes to your Klaviyo account without explicit authorization. All implementation work is performed by qualified specialists with your approval.

---

*Klaviyo Audit Report prepared by National Positions — Klaviyo Audit Katie*
*Version 1.0 | [Audit Date] | Confidential — [Client Brand Name] only*

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-05-10 | Initial output template — Phase 1 |
