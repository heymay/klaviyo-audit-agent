# Klaviyo Audit Katie — Metrics Glossary

**Version:** 1.0
**Owner:** National Positions
**Classification:** Internal Operating Framework — Phase 1
**Last Updated:** 2026-05-10

---

## Overview

This glossary defines every metric Katie uses in the audit. For each metric: definition, formula, data source (Klaviyo object), why it matters, and interpretation guidance (what's good, average, concerning).

All rate metrics are expressed as percentages unless noted. All revenue metrics are in the account's local currency.

---

## Profile Metrics

---

### Total Profiles

**Definition:** The total number of profiles in the Klaviyo account, including all statuses.
**Formula:** Count of all profile records in the account
**Data Source:** Profiles object (`/api/profiles/`)
**Why It Matters:** Establishes the scale of the account and is the denominator for billing tier comparison.
**Interpretation:**
- This number alone is not meaningful — compare to emailable and engaged profiles
- A large total profile count with a small engaged count signals list quality issues

---

### Emailable Profiles

**Definition:** Profiles that are not suppressed and have a valid email address that can receive email.
**Formula:** Total profiles − suppressed profiles − profiles with no email
**Data Source:** Profiles object
**Why It Matters:** This is the actual deliverable audience. Billing is often based on this count.
**Interpretation:**
- Should be tracked over time — a declining trend signals deliverability or list health problems
- Compare to plan profile limit to assess billing efficiency

---

### SMS Consented Profiles

**Definition:** Profiles that have provided valid SMS consent and can legally receive SMS messages.
**Formula:** Count of profiles with SMS consent status = subscribed
**Data Source:** Profiles object
**Why It Matters:** Determines the active SMS audience and the opportunity size for SMS flows and campaigns.
**Interpretation:**
- < 5% of emailable profiles: SMS list is underdeveloped — needs list growth focus
- 5–15%: Developing SMS list
- 15–30%: Healthy SMS program
- > 30%: Strong SMS adoption — maximize SMS revenue

---

### Active Profiles

**Definition:** Profiles that have engaged with at least one email or SMS message in the past 90 days.
**Formula:** Count of profiles with at least one open, click, or SMS click in the past 90 days
**Data Source:** Profiles + Events
**Why It Matters:** Active profiles are the audience most likely to convert and least likely to suppress.
**Interpretation:**
- Active profiles as % of emailable list is a key list health indicator
- < 10% active: list is critically cold
- 10–25%: Average engagement level — needs segmentation work
- 25–50%: Healthy active base
- > 50%: Strong engagement — well-maintained list

---

### Suppressed Profiles

**Definition:** Profiles that cannot receive email (unsubscribed, hard bounced, marked as spam, or manually suppressed).
**Formula:** Count of profiles with suppression status
**Data Source:** Profiles object
**Why It Matters:** Suppressed profiles inflate the total profile count and billing tier while providing no revenue value.
**Interpretation:**
- Suppression rate (suppressed / total profiles):
  - < 10%: Normal — expected attrition
  - 10–20%: Elevated — review list growth sources and frequency
  - > 20%: High — historical list quality issues or frequency abuse
- Growing suppression trend: active deliverability risk signal

---

### Engaged 30-Day Profiles

**Definition:** Profiles that opened or clicked at least one email in the past 30 days.
**Formula:** Count of profiles with an open or click event in the last 30 days
**Data Source:** Profiles + Events
**Why It Matters:** This is the highest-quality, most responsive segment — ideal for campaign targeting.
**Interpretation:**
- As % of emailable list:
  - < 5%: Very small active core — frequency or relevance issue
  - 5–15%: Typical for ecommerce accounts
  - 15–30%: Strong engagement
  - > 30%: Excellent — consistent, highly engaged audience

---

### Engaged 60-Day Profiles

**Definition:** Profiles that opened or clicked at least one email in the past 60 days.
**Formula:** Count of profiles with open or click in last 60 days
**Data Source:** Profiles + Events
**Why It Matters:** The secondary engagement window — used for campaign exclusion logic and deliverability safety.
**Interpretation:** Should be 1.5–2× the size of the engaged 30-day segment. A large drop between 30 and 60 days suggests the audience opens once then goes cold.

---

### Engaged 90-Day Profiles

**Definition:** Profiles that opened or clicked at least one email in the past 90 days.
**Formula:** Count of profiles with open or click in last 90 days
**Data Source:** Profiles + Events
**Why It Matters:** The outer safe-sending boundary. Regular campaigns should generally not exceed this audience for optimal deliverability.
**Interpretation:**
- As % of emailable list:
  - < 10%: List is largely dormant — deliverability at risk
  - 10–30%: Average — room to improve
  - > 30%: Healthy
  - > 50%: Excellent

---

### Engaged 180-Day Profiles

**Definition:** Profiles that opened or clicked at least one email in the past 180 days.
**Formula:** Count of profiles with open or click in last 180 days
**Data Source:** Profiles + Events
**Why It Matters:** The broadest usable engagement window. Profiles not in this segment are strong candidates for re-engagement or sunset.
**Interpretation:** Engaged 180-day profiles that are NOT in the engaged 90-day segment are the re-engagement target. Profiles outside the 180-day window should enter a sunset flow.

---

### Dormant Profiles

**Definition:** Emailable profiles that have not opened or clicked any email in 180+ days.
**Formula:** Emailable profiles − engaged 180-day profiles
**Data Source:** Profiles + Events
**Why It Matters:** Dormant profiles contribute to deliverability problems when emailed. They also inflate the billing tier.
**Interpretation:**
- Dormant rate (dormant / total emailable):
  - < 30%: Manageable — maintain with regular list hygiene
  - 30–50%: Elevated — run a re-engagement campaign
  - > 50%: Critical — list hygiene required before any broad campaign sends

---

## Campaign Metrics

---

### Campaign Send Frequency

**Definition:** The average number of campaigns sent per week or per month in the audit period.
**Formula:** Total campaigns sent ÷ number of weeks (or months) in the audit period
**Data Source:** Campaigns object
**Why It Matters:** Too few campaigns = missed revenue. Too many = list fatigue and deliverability damage.
**Interpretation:**
- < 0.5/week (less than twice monthly): Underutilization — leaving revenue on the table
- 1–2/week: Standard for ecommerce
- 2–3/week: Active — acceptable if segmentation protects engaged audience
- > 5/week to broad list: Fatigue risk — review segmentation and frequency caps

---

### Campaign Open Rate

**Definition:** The percentage of delivered campaign emails that were opened.
**Formula:** Unique opens ÷ delivered emails × 100
**Data Source:** Campaign Messages
**Why It Matters:** Measures subject line effectiveness, sender reputation, and audience relevance.
**Interpretation (industry-adjusted; verify against current Klaviyo benchmarks):**
- < 15%: Below average — subject lines, segmentation, or deliverability issue
- 15–25%: Average
- 25–35%: Good
- > 35%: Excellent

---

### Campaign Click Rate

**Definition:** The percentage of delivered emails that had at least one link clicked.
**Formula:** Unique clicks ÷ delivered emails × 100
**Data Source:** Campaign Messages
**Why It Matters:** Measures content relevance, CTA effectiveness, and design quality.
**Interpretation:**
- < 1%: Below average — CTA, offer, or design issue
- 1–2%: Average
- 2–4%: Good
- > 4%: Excellent

---

### Campaign Conversion Rate

**Definition:** The percentage of recipients who placed an order after receiving a campaign.
**Formula:** Orders placed ÷ delivered emails × 100
**Data Source:** Campaign Messages + Placed Order metric
**Why It Matters:** The most direct measure of campaign revenue driving effectiveness.
**Interpretation:**
- < 0.5%: Below average
- 0.5–1%: Average
- 1–2%: Good
- > 2%: Excellent

---

### Revenue Per Recipient

**Definition:** The average revenue generated per email delivered in a campaign or flow.
**Formula:** Campaign (or flow) revenue ÷ number of recipients (delivered)
**Data Source:** Campaign Messages + Revenue metric
**Why It Matters:** Normalizes revenue by audience size — allows fair comparison across campaigns and flows.
**Interpretation:**
- This varies significantly by product and AOV
- Track trend over time — declining RPR signals list quality, segmentation, or offer degradation

---

### Unsubscribe Rate

**Definition:** The percentage of delivered emails that resulted in an unsubscribe.
**Formula:** Unsubscribes ÷ delivered emails × 100
**Data Source:** Email Events
**Why It Matters:** High unsubscribes signal frequency abuse, irrelevant content, or audience fatigue. Also a direct deliverability signal.
**Interpretation:**
- < 0.1%: Excellent
- 0.1–0.3%: Normal
- 0.3–0.5%: Elevated — review frequency and segmentation
- > 0.5%: High — actionable deliverability concern

---

### Spam Complaint Rate

**Definition:** The percentage of delivered emails marked as spam by recipients.
**Formula:** Spam complaints ÷ delivered emails × 100
**Data Source:** Email Events
**Why It Matters:** The most critical deliverability metric. Gmail's spam threshold is 0.10%; exceeding it triggers inbox placement penalties.
**Interpretation:**
- < 0.02%: Excellent
- 0.02–0.08%: Normal
- 0.08–0.10%: Warning — approaching Gmail's threshold
- > 0.10%: Critical — inbox placement at risk; immediate action required
- > 0.30%: Severe — major deliverability crisis

---

### Hard Bounce Rate

**Definition:** The percentage of sent emails that permanently failed to deliver (invalid address, domain doesn't exist).
**Formula:** Hard bounces ÷ sent emails × 100
**Data Source:** Email Events
**Why It Matters:** Hard bounces signal list quality issues (purchased lists, old lists, typos). High bounce rates damage sender reputation.
**Interpretation:**
- < 0.2%: Excellent
- 0.2–0.5%: Normal
- 0.5–1%: Elevated — list hygiene recommended
- > 1%: High — active list quality problem; review acquisition sources
- > 2%: Critical — sender reputation at risk

---

### Soft Bounce Rate

**Definition:** The percentage of sent emails that temporarily failed to deliver (inbox full, server temporarily unavailable).
**Formula:** Soft bounces ÷ sent emails × 100
**Data Source:** Email Events
**Why It Matters:** Occasional soft bounces are normal. Consistently high soft bounce rates may indicate deliverability or domain reputation issues.
**Interpretation:**
- < 1%: Normal
- 1–3%: Monitor
- > 3%: Investigate — could be infrastructure or reputation issue

---

## Flow Metrics

---

### Flow Revenue

**Definition:** The total revenue attributed to a specific flow (or all flows combined) in the audit period.
**Formula:** Sum of placed order value where the order was attributed to a flow touch
**Data Source:** Flows object + Revenue metric
**Why It Matters:** The primary measure of lifecycle automation performance.
**Interpretation:**
- Track by individual flow and in aggregate
- Flow revenue as % of total Klaviyo revenue is the key ratio (see below)

---

### Flow Revenue as % of Total Klaviyo Revenue

**Definition:** The proportion of total Klaviyo-attributed revenue that comes from flows (vs. campaigns).
**Formula:** Total flow revenue ÷ total Klaviyo revenue × 100
**Data Source:** Flows + Campaigns revenue
**Why It Matters:** A mature Klaviyo setup should have a substantial flow contribution — flows run 24/7 without manual effort.
**Interpretation:**
- < 20%: Lifecycle automation underperforming — core flows missing or misconfigured
- 20–35%: Developing — flows exist but not fully optimized
- 35–50%: Healthy — strong automation foundation
- > 50%: Excellent — highly automated retention revenue engine

---

### Welcome Flow Revenue

**Definition:** Revenue attributed to the Welcome Series flow.
**Formula:** Placed order revenue where last touch = Welcome flow
**Data Source:** Flows revenue
**Why It Matters:** The Welcome flow is the first revenue-generating automation. It should convert new subscribers into first purchasers.

---

### Abandoned Cart Flow Revenue

**Definition:** Revenue attributed to the Abandoned Cart flow.
**Formula:** Placed order revenue where last touch = Abandoned Cart flow
**Data Source:** Flows revenue
**Why It Matters:** The single highest-revenue flow for most ecommerce brands. Underperformance here is the most common lifecycle gap.

---

### Browse Abandonment Flow Revenue

**Definition:** Revenue attributed to the Browse Abandonment flow.
**Formula:** Placed order revenue where last touch = Browse Abandonment flow
**Data Source:** Flows revenue
**Why It Matters:** Mid-funnel recovery — catches shoppers who viewed products but did not add to cart.

---

### Added-to-Cart Flow Revenue

**Definition:** Revenue attributed to the Added to Cart flow (separate from Abandoned Cart).
**Formula:** Placed order revenue where last touch = Added to Cart flow
**Data Source:** Flows revenue
**Why It Matters:** Bridges the gap between browse abandonment and checkout abandonment.

---

## Form Metrics

---

### Form Views

**Definition:** The number of times a signup form was displayed to a visitor.
**Formula:** Count of form view events
**Data Source:** Forms object
**Why It Matters:** Determines the traffic reaching the form — required to calculate opt-in rate.

---

### Form Submits

**Definition:** The number of times a visitor successfully submitted the signup form.
**Formula:** Count of form submit events
**Data Source:** Forms object
**Why It Matters:** The raw conversion count for list growth.

---

### Form Opt-In Rate

**Definition:** The percentage of form views that resulted in a successful submission.
**Formula:** Form submits ÷ form views × 100
**Data Source:** Forms object
**Why It Matters:** The key efficiency metric for list growth. Even small improvements compound over time.
**Interpretation:**
- < 2%: Weak — incentive, design, timing, or offer needs significant improvement
- 2–3.9%: Average — acceptable but improvable
- 4–5.9%: Good — strong performance
- ≥ 6%: Excellent — top-tier capture rate

---

### SMS Opt-In Rate

**Definition:** The percentage of form visitors who provided both email AND phone (SMS consent).
**Formula:** SMS submits ÷ form views × 100
**Data Source:** Forms object (if SMS field is present)
**Why It Matters:** Determines the rate at which the SMS list is growing through organic form capture.
**Interpretation:**
- Should be compared to overall opt-in rate — SMS rate will always be lower
- An SMS opt-in rate of 50–70% of the email opt-in rate is considered healthy (some visitors prefer email only)

---

## List Growth Metrics

---

### List Growth Rate

**Definition:** The percentage change in emailable profile count over the audit period.
**Formula:** (End-period emailable profiles − Start-period emailable profiles) ÷ Start-period emailable profiles × 100
**Data Source:** Profiles
**Why It Matters:** A growing list means the top of the funnel is working. A declining list means acquisition is not keeping pace with suppression.
**Interpretation:**
- Negative growth: List is shrinking — urgent attention needed
- 0–2%: Slow growth — check acquisition sources
- 2–5%: Normal
- > 5%: Strong growth — maintain quality alongside volume

---

### List Decay Rate

**Definition:** The rate at which profiles are leaving the list (suppression, unsubscribes, bounces).
**Formula:** (New suppressions + bounces + unsubscribes) ÷ start-period emailable profiles × 100
**Data Source:** Profiles + Events
**Why It Matters:** Tracks passive list attrition. Every list loses 25–30% of its profiles annually on average.
**Interpretation:**
- Decay rate higher than growth rate: Net list shrinkage — major concern
- Decay and growth roughly balanced: Stable list — optimize for quality
- Growth rate exceeds decay: Healthy expansion

---

## Benchmark and Performance Metrics

---

### Benchmark Rating

**Definition:** Klaviyo's comparative performance rating for a specific metric relative to similar accounts.
**Formula:** Provided by Klaviyo (not calculated) — rated as: Poor / Below Average / Average / Good / Excellent
**Data Source:** Klaviyo Benchmarks (API or in-platform)
**Why It Matters:** Provides context for whether performance numbers are strong or weak relative to peers.
**Interpretation:**
- Poor: In the bottom ~20% of comparable accounts
- Below Average: 20–40th percentile
- Average: 40–60th percentile
- Good: 60–80th percentile
- Excellent: Top ~20% of comparable accounts

---

### Repeat Purchase Rate

**Definition:** The percentage of customers who made more than one purchase in the audit period.
**Formula:** Customers with 2+ orders ÷ total customers × 100
**Data Source:** Placed Order metric (Shopify or ecommerce platform integration required)
**Why It Matters:** Repeat purchase rate is the most direct measure of lifecycle marketing effectiveness.
**Interpretation:**
- < 20%: Low — lifecycle marketing opportunity significant
- 20–35%: Average
- 35–50%: Strong
- > 50%: Excellent — highly sticky product or strong lifecycle program

---

## Billing Metrics

---

### Billing Utilization Rate

**Definition:** The ratio of actively emailable profiles to the plan's profile limit.
**Formula:** Emailable profiles ÷ plan profile limit × 100
**Data Source:** Profiles + Account (plan data)
**Why It Matters:** Identifies whether the client is overpaying for unused profile capacity.
**Interpretation:**
- > 80%: Healthy — at or near plan capacity; may need to upgrade
- 50–80%: Normal
- 25–50%: Borderline — monitor and evaluate if justified
- < 25%: Overpay risk — plan tier is likely too large for actual usage

---

### Unused Profile Allowance

**Definition:** The number of profiles the plan supports above what is currently emailable.
**Formula:** Plan profile limit − emailable profiles
**Data Source:** Account + Profiles
**Why It Matters:** Quantifies the "wasted" capacity the client is paying for.

---

### Overpay Risk Score

**Definition:** A qualitative assessment of whether the client is paying meaningfully more than they need to for their current active audience.
**Formula:** Qualitative — High / Medium / Low / None
**Data Source:** Billing utilization rate
**Interpretation:**
- Utilization > 80%: None
- 50–80%: Low
- 25–50%: Medium
- < 25%: High — flag for billing review

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-05-10 | Initial metrics glossary — Phase 1 |
