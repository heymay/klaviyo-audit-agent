# Klaviyo Audit Katie — Skill Definition (Audit Methodology)

**Version:** 1.0
**Owner:** National Positions
**Classification:** Internal Operating Framework — Phase 1
**Last Updated:** 2026-05-10

---

## Overview

This document defines the complete, step-by-step methodology Katie follows when conducting a Klaviyo audit. The methodology is organized into 11 phases, from account intake through report generation and CTA delivery.

Each phase includes: objective, required inputs, step-by-step instructions, outputs produced, and key questions to answer before proceeding.

---

## Phase 0 — Account Intake

**Objective:** Collect all business context and required inputs before touching any Klaviyo data.

**Required Inputs:**
- Business name and website URL
- Ecommerce platform (Shopify, WooCommerce, etc.)
- Monthly revenue range
- Average order value (if available)
- Audit date range
- Klaviyo API key (read-only)
- User consent acknowledgment

**Steps:**
1. Present the intake form (see input-checklist.md) to the user
2. Confirm all required fields are complete before proceeding
3. Log the business name, website, and audit date range in the audit metadata block
4. Set the comparison period (prior period or YoY) based on user selection
5. Confirm user has provided explicit consent to access Klaviyo data
6. Store the API key in a secure environment variable — never in a code file or log
7. Flag any missing recommended inputs and note their impact on audit depth

**Outputs:** Completed intake record, audit metadata header, API key ready for validation

**Key Questions Before Proceeding:**
- Is all required information present?
- Is the API key stored securely and not logged anywhere?
- Has user consent been confirmed?

---

## Phase 1 — API Connection and Validation

**Objective:** Confirm the Klaviyo API key is valid, read-only, and has access to the necessary data objects.

**Required Inputs:** API key from Phase 0

**Steps:**
1. Call `GET /api/accounts/` with the provided API key
2. If 200 OK: log account name and account ID (not the API key)
3. If 401: stop audit — notify user of invalid key, request new credentials
4. If 403: stop audit — notify user that key lacks required permissions, request read-only key
5. If rate limited (429): apply exponential backoff and retry
6. Confirm account identity matches the expected client before proceeding
7. Test each primary data endpoint to confirm accessibility:
   - Campaigns, Campaign Messages
   - Flows, Flow Messages
   - Lists, Segments
   - Profiles (aggregate)
   - Forms
   - Metrics, Events
   - Templates
8. Log which endpoints return data vs. which return 403/404
9. Flag any inaccessible endpoints as "data unavailable" for that audit section
10. Confirm connection is read-only: do not test any write endpoint

**Outputs:** API validation report (accessible endpoints, account confirmed), connection status log

**Key Questions Before Proceeding:**
- Did the connection succeed?
- Do we have access to the minimum required endpoints (campaigns, flows, forms, lists, profiles)?
- Are any critical endpoints inaccessible — and if so, which audit categories will be affected?

---

## Phase 2 — Data Pull

**Objective:** Retrieve all required Klaviyo data objects for the audit period. Normalize data into a consistent internal format for analysis.

**Required Inputs:** Validated API connection, audit date range

**Steps:**
1. Pull **Account** data: account name, timezone, currency, industry, plan tier (if accessible)
2. Pull **Campaigns** for the audit period:
   - Filter by send date within the audit date range
   - Pull all sent campaigns (email + SMS)
   - Paginate until all campaign records are retrieved
3. Pull **Campaign Messages** for each campaign:
   - Retrieve performance metrics: open rate, click rate, conversion, revenue, bounces, unsubscribes, spam complaints
4. Pull **Flows**:
   - Retrieve all flows regardless of status (Live, Draft, Manual, Archived)
   - Pull flow revenue and conversion data for the audit period
5. Pull **Flow Messages** for each flow:
   - Retrieve per-message metrics: channel, delay timing, position, open rate, click rate, revenue
6. Pull **Lists**: all lists with profile counts and creation dates
7. Pull **Segments**: all segments with profile counts and condition definitions
8. Pull **Profiles** (aggregate counts only):
   - Total profiles, emailable, SMS consented, suppressed
   - Engaged 30/60/90/180-day counts (via segment or aggregate API)
9. Pull **Forms**: all forms with view counts, submit counts, opt-in rates, and channel breakdown
10. Pull **Metrics**: confirm which event types are actively tracked
11. Pull **Events** for the audit period:
    - Email events: received, opened, clicked, unsubscribed, spam complaints, bounces
    - SMS events: received, clicked, opted out
12. Pull **Templates**: count and type
13. Pull **Benchmarks** if accessible via API
14. Pull **Billing/Plan data** if accessible via API
15. Normalize all data into the internal data model (see klaviyo-data-map.md)
16. Flag any data fields that returned null, empty, or unavailable

**Outputs:** Complete normalized dataset for all audit categories, data pull log with timestamps and record counts

**Key Questions Before Proceeding:**
- Was all critical data retrieved (campaigns, flows, forms, profiles)?
- Are there significant data gaps that will affect specific audit categories?
- Does the data cover the full audit date range?

---

## Phase 3 — SMS Adoption Review

**Objective:** Assess the maturity and completeness of the account's SMS program.

**Required Inputs:** Profiles data (SMS consented count), Flows data (SMS message presence), Campaigns data (SMS campaigns sent), Forms data (SMS opt-in presence)

**Steps:**
1. Check if SMS is enabled in the account (presence of SMS metrics or SMS campaign sends)
2. Calculate SMS consent rate: SMS consented profiles ÷ emailable profiles
3. Count SMS campaigns sent in the audit period
4. Count flows with at least 1 SMS message
5. Count flows with 0 SMS messages (identify each by name)
6. Check signup forms: do any forms collect SMS consent?
7. Calculate SMS opt-in rate on forms that collect SMS
8. Check for SMS revenue attribution (is there SMS-attributed revenue in the audit period?)
9. Apply SMS decision rules: SMS-001 through SMS-015
10. Assign SMS category score (1–10) per scoring rubric

**Key Questions:**
- Is SMS enabled?
- What % of the list is SMS consented?
- Are flows using SMS?
- Are forms collecting SMS?
- What is the SMS revenue contribution?

**Outputs:** SMS adoption score, SMS findings list with severity and priority

---

## Phase 4 — Campaign Review

**Objective:** Evaluate campaign frequency, segmentation, performance, and strategic consistency.

**Required Inputs:** Campaigns data, Campaign Messages data (performance metrics), Segments data

**Steps:**
1. Calculate campaign send frequency: total campaigns ÷ weeks in audit period
2. Identify campaign channel mix: email campaigns vs. SMS campaigns
3. For each campaign, record: send date, recipient count, audience (segment or list used)
4. Calculate % of campaigns sent to engaged segments vs. broad lists
5. Calculate average campaign open rate, click rate, unsubscribe rate, spam complaint rate, and revenue for the period
6. Identify the highest-revenue and lowest-revenue campaigns
7. Check subject line lengths: flag any consistently over 60 characters
8. Check preview text: flag campaigns with missing preview text
9. Identify whether campaign strategy is promotions-only or varied (promotional + educational + brand)
10. Apply Campaign decision rules: CAMP-001 through CAMP-015
11. Assign Campaign Strategy & Consistency score (1–10)

**Key Questions:**
- How often is the account sending?
- Who are campaigns going to?
- Are open and click rates healthy?
- Is the campaign strategy varied or monotonous?

**Outputs:** Campaign score, campaign findings list, frequency summary, performance metrics table

---

## Phase 5 — Deliverability Review

**Objective:** Assess the account's email sending reputation and identify any deliverability risks.

**Required Inputs:** Email Events data (bounces, spam complaints, unsubscribes, opens), Account data (sending domain), Domain authentication records (SPF/DKIM/DMARC — may require manual verification)

**Steps:**
1. Calculate aggregate hard bounce rate: hard bounces ÷ sent emails (audit period)
2. Calculate aggregate soft bounce rate
3. Calculate aggregate spam complaint rate: spam complaints ÷ sent emails
4. Calculate average unsubscribe rate per campaign
5. Track open rate trend over the audit period (improving, declining, or flat)
6. Check for branded/dedicated sending domain (present or default Klaviyo domain)
7. Flag SPF, DKIM, DMARC status (may require manual DNS lookup or client confirmation in Phase 1)
8. Check whether campaigns are being sent to engaged-only segments vs. full list
9. Check for suppression growth trend
10. Apply Deliverability decision rules: DELV-001 through DELV-015
11. Assign Deliverability Health Level: Critical / Needs Improvement / Acceptable / Strong
12. Assign Deliverability score (1–10)

**Key Questions:**
- Are bounce and spam rates within acceptable thresholds?
- Is DKIM/SPF/DMARC configured?
- Is a branded sending domain in use?
- Are campaigns going to cold profiles?

**Outputs:** Deliverability score, deliverability health level, findings list with severity

---

## Phase 6 — Core Flow Review

**Objective:** Evaluate whether all 7 core lifecycle flows exist and are in Live status.

**Required Inputs:** Flows data (all flows, status, name, trigger, message count)

**Steps:**
1. List all flows in the account by name and status
2. Match each flow to a core flow category using name pattern matching (see klaviyo-data-map.md)
3. For each core flow type, determine:
   - Does it exist? (yes / no)
   - Is it Live? (only Live flows count)
   - When was it last updated?
4. Core flows to check: Welcome, Abandoned Cart, Added to Cart, Browse Abandonment, Post-Purchase, Winback, VIP
5. Flag any flows in Draft or Manual status as "exists but not active"
6. Flag any entirely missing flows as lifecycle gaps
7. Check for non-core value-add flows: Replenishment, Sunset/Unengaged, Loyalty
8. Apply Core Flow decision rules: FLOW-001 through FLOW-020
9. Assign Core Flow Coverage score (1–10) applying special penalty rules from scoring-rubric.md

**Key Questions:**
- Are Welcome and Abandoned Cart flows Live? (critical)
- Are all 7 core flows present?
- How many flows are Live vs. Draft?

**Outputs:** Core flow existence table (name, status, last updated), Core Flow Coverage score, critical gaps flagged

---

## Phase 7 — Flow Configuration Review

**Objective:** Evaluate the quality, timing, channel mix, and structure of all existing Live flows.

**Required Inputs:** Flow Messages data (channel, delay, position, metrics), Flows data (revenue, conversion rate)

**Steps:**
1. For each Live flow, retrieve all messages ordered by position
2. Count email messages and SMS messages per flow
3. Calculate email-to-SMS ratio per flow
4. For Abandoned Cart flow: check timing of first message (goal: < 60 minutes)
5. For Abandoned Cart flow: check timing of second message (goal: ~24 hours after first)
6. For Abandoned Cart flow: check timing of third message (goal: ~72 hours after abandonment)
7. For Welcome flow: count emails (minimum 4)
8. For all transactional flows: check for SMS presence
9. For Abandoned Cart and Added to Cart: check for incentive/discount in messages 2 or 3
10. Review flow revenue contribution per flow (which flows generate the most revenue?)
11. Calculate flow revenue as % of total Klaviyo revenue
12. Apply Flow Timing rules: FTIM-001 through FTIM-010
13. Apply relevant Flow rules from FLOW section
14. Assign Flow Configuration Quality score (1–10)

**Key Questions:**
- Does Abandoned Cart fire within 1 hour?
- Are flows meeting minimum message count standards?
- Does each transactional flow include SMS?
- Which flows are generating revenue, and which are not?

**Outputs:** Per-flow configuration table (message count, timing, SMS presence, revenue), Flow Configuration score, timing findings

---

## Phase 8 — Signup Form and List Growth Review

**Objective:** Evaluate the account's list growth mechanisms — signup form existence, opt-in rates, and channel capture.

**Required Inputs:** Forms data (views, submits, opt-in rate, channel, device, incentive, display rules)

**Steps:**
1. List all published (active) signup forms
2. For each form, calculate opt-in rate: submits ÷ views
3. Separate opt-in rate by device (mobile vs. desktop)
4. Check whether each form collects email only vs. email + SMS
5. Check for incentive presence on each form (discount, free shipping, lead magnet)
6. Check display rules: popup, flyout, embed, exit-intent, scroll-trigger, time-delay
7. Identify the primary form (highest traffic) and its opt-in rate
8. Flag if no popup or flyout exists (footer-embed-only account)
9. Calculate SMS opt-in rate on forms that have SMS collection
10. Apply Form decision rules: FORM-001 through FORM-010
11. Assign Signup Forms & List Growth score (1–10)

**Key Questions:**
- Does an active signup form exist?
- What is the overall opt-in rate?
- Does the form collect SMS?
- Is mobile opt-in rate healthy?
- Is there an incentive?

**Outputs:** Form performance table, Signup Forms score, opt-in rate assessment, list growth findings

---

## Phase 9 — List Health and Segmentation Review

**Objective:** Assess the engagement health of the list and the sophistication of the segmentation strategy.

**Required Inputs:** Profiles data (engagement counts), Segments data (definitions, sizes), Campaigns data (audience targeting)

**Steps:**
1. Calculate engagement distribution:
   - Engaged 30-day as % of emailable
   - Engaged 60-day as % of emailable
   - Engaged 90-day as % of emailable
   - Engaged 180-day as % of emailable
   - Dormant (not in 180-day) as % of emailable
2. Calculate suppression rate and assess suppression trend
3. Review all segments: identify engagement-based segments, purchaser segments, VIP segments
4. Check whether campaigns were sent to engaged segments or broad lists
5. Identify whether an engaged-only segment is actively used for campaign targeting
6. Check for a sunset / unengaged segment
7. Assess segment sophistication (static lists vs. dynamic behavioral segments)
8. Apply List Health rules: LIST-001 through LIST-010
9. Apply Segmentation rules from CAMP section where applicable
10. Assign List Health & Engagement score (1–10)
11. Assign Segmentation Quality score (1–10)

**Key Questions:**
- What % of the list is engaged in the last 30, 60, 90, and 180 days?
- Is the dormant rate concerning?
- Do engagement-based segments exist?
- Are campaigns using engaged-segment targeting?

**Outputs:** List engagement distribution table, segmentation inventory, List Health score, Segmentation score

---

## Phase 10 — Revenue Attribution, Benchmark, and Billing Review

**Objective:** Assess revenue attribution quality, benchmark performance ratings, and billing efficiency.

**Required Inputs:** Campaign revenue, Flow revenue, Benchmark data (if available), Account plan/billing data (if available)

**Steps:**
1. Calculate total Klaviyo revenue for the audit period (campaigns + flows)
2. Calculate campaign revenue as % of total Klaviyo revenue
3. Calculate flow revenue as % of total Klaviyo revenue
4. Identify top 3 revenue-generating flows and top 3 revenue-generating campaigns
5. Calculate revenue per recipient for campaigns and flows separately
6. Review benchmark ratings where available (open rate, click rate, flow revenue, etc.)
7. Summarize benchmark performance: mostly Good/Excellent, mixed, or mostly Poor/Average
8. Pull billing/plan data if available: plan tier, profile limit, current profile count
9. Calculate billing utilization rate (if data available)
10. Identify overpay risk (if utilization is very low)
11. Apply Revenue rules: REV-001 through REV-010
12. Apply Billing rules: BILL-001 through BILL-005
13. Assign Revenue Attribution & Benchmarks score (1–10)
14. Assign Billing Efficiency score (1–10)

**Key Questions:**
- What % of revenue comes from flows vs. campaigns?
- Are benchmark ratings mostly good or poor?
- Is the account overpaying for its plan tier?
- Is revenue attribution properly set up?

**Outputs:** Revenue attribution summary table, benchmark ratings table, Billing Efficiency summary, Revenue score, Billing score

---

## Phase 11 — Scoring, Recommendations, and Report Generation

**Objective:** Synthesize all phase findings into a composite score, generate prioritized recommendations, build the 30/60/90 action plan, and produce the final report.

**Required Inputs:** All category scores and findings from Phases 3–10

**Steps:**
1. **Calculate Composite Score:**
   - Apply weights per scoring-rubric.md
   - Apply all penalty rules (automatic score caps)
   - Apply all bonus rules
   - Calculate composite: Σ (Category Score / 10 × Weight × 100)
   - Round to nearest whole number

2. **Assign Score Band:**
   - Elite (90–100), Strong (75–89), Average (60–74), Weak (40–59), Critical (0–39)

3. **Generate Findings List:**
   - For each triggered decision rule, create a finding entry with:
     - Rule ID
     - Severity
     - Finding description
     - Business impact
     - Recommended action
     - Priority
     - Confidence level
   - Sort findings by severity (Critical → High → Medium → Low)

4. **Identify Top 5 Wins:**
   - Positive findings from decision rules
   - Areas where the account scores 8+ in a category
   - Specific strengths confirmed by data

5. **Identify Top 5 Issues:**
   - Highest-severity findings, ranked by revenue impact
   - At least one finding from each Critical or High severity category

6. **Identify Top 5 Revenue Opportunities:**
   - Missing flows with estimated recovery potential
   - SMS missing from account or from flows
   - Form opt-in improvement potential
   - Benchmark underperformance gaps
   - Deliverability recovery opportunity

7. **Generate Prioritized Recommendations:**
   - Apply recommendation engine framework (see recommendation-engine.md)
   - Assign: issue, why it matters, expected impact, complexity, priority, owner, timeline

8. **Build 30/60/90 Day Action Plan:**
   - 30 days: Critical and High findings that are Easy or Moderate complexity
   - 60 days: High and Medium findings that require build-outs
   - 90 days: Medium and Low findings, strategic improvements

9. **Generate Opportunity Summary:**
   - Conservative, moderate, and optimistic revenue opportunity ranges
   - Always include disclaimer: directional estimates only, not guarantees
   - Frame around specific gaps identified in the audit

10. **Write Executive Summary:**
    - 3–5 sentences for a CMO or business owner
    - Lead with the score and what drives it
    - Name the top 1–2 most impactful opportunities
    - Close with a forward-looking statement

11. **Assemble Full Report:**
    - Follow output-template.md section by section
    - Include all 22 sections
    - Append National Positions CTA as Section 22

12. **Route for Human Review:**
    - Mark report as DRAFT — not for client delivery
    - Assign to National Positions Marketing Automation Strategist for Gate 2 review
    - Flag any findings that require compliance, legal, or senior review

**Outputs:** Complete audit report (draft), composite score, recommendations list, 30/60/90 plan, opportunity summary, NP CTA — all staged for human review

---

## Date Range and Comparison Period Handling

Every phase that involves time-based data must respect the defined audit date range.

**Audit Date Range:**
- All campaign metrics, flow metrics, event data, and growth calculations are filtered to the audit period
- The audit period start and end dates are displayed on every page of the report

**Comparison Period (when selected):**
- Where applicable, metrics are compared to the prior period or year-over-year equivalent
- Trend indicators (improving, flat, declining) are added to key metrics where comparison data exists
- Comparison metrics are displayed alongside current-period metrics in report tables

**Report Header Requirement:**
Every report must include in the document header:
- Client/company name
- Website URL
- Klaviyo account name
- Audit period (start date to end date)
- Comparison period (if used)
- Data sources used
- Date report was generated

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-05-10 | Initial skill definition — Phase 1 |
