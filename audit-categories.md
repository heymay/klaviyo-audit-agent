# Klaviyo Audit Katie — Audit Categories

**Version:** 1.0
**Owner:** National Positions
**Classification:** Internal Operating Framework — Phase 1
**Last Updated:** 2026-05-10

---

## Overview

Katie evaluates 22 audit categories across every Klaviyo account. Each category has defined analysis criteria, key metrics, common findings, and recommended actions. Categories 1–21 are analytical; Category 22 is the structured output deliverable.

---

## Category 1 — Executive Overview

**What Katie Analyzes:**
The executive overview is not a scored category — it is a synthesized summary of the entire audit designed for a business owner or CMO. Katie identifies the 3–5 most impactful findings from across all categories and frames them as business outcomes, not platform observations.

**Key Metrics:**
- Composite Klaviyo Health Score (0–100)
- Score band (Elite / Strong / Average / Weak / Critical)
- Top 5 issues
- Top 5 wins
- Top 5 revenue opportunities

**Common Findings:**
- "Your Klaviyo score is 44/100 — primarily driven by missing core flows and no SMS program."
- "Campaign strategy is strong but flow revenue is critically low."
- "Deliverability is at risk due to unengaged list sends and elevated spam complaints."

**Recommended Actions:**
- Prioritize the 30/60/90 action plan based on the executive summary findings
- Lead with the highest-revenue-impact issue in every client conversation

---

## Category 2 — SMS Adoption

**What Katie Analyzes:**
Whether the account has SMS enabled, the size of the SMS-consented profile list, whether SMS is used in flows and campaigns, and the overall maturity of the SMS program.

**Key Metrics:**
- SMS enabled (yes / no)
- SMS-consented profiles count
- SMS consent rate (SMS consented / total emailable profiles)
- SMS flows active (count)
- SMS campaigns sent in audit period (count)
- SMS revenue (if attributable)

**Common Findings:**
- SMS not enabled — major missed revenue channel
- SMS enabled but fewer than 10% of profiles consented — list growth needed
- SMS in campaigns only — flows not using SMS
- No SMS signup capture on forms

**Recommended Actions:**
- Enable SMS if not active; determine compliance requirements first
- Add SMS opt-in to all signup forms
- Add SMS steps to all core flows where consent exists
- Run SMS-specific list growth campaigns

---

## Category 3 — Campaign Consistency

**What Katie Analyzes:**
Whether the account sends campaigns on a consistent, predictable schedule or has long gaps, irregular sends, or no campaign history.

**Key Metrics:**
- Total campaigns sent in audit period
- Average campaigns per week
- Longest gap between campaign sends (days)
- Campaign send calendar (distribution across the period)

**Common Findings:**
- No campaigns sent in 30+ days — dormant campaign strategy
- Campaigns sent in bursts around promotions with long gaps between
- Consistent campaign schedule (positive finding)
- Over-sends with no clear strategy (negative)

**Recommended Actions:**
- Establish a minimum weekly campaign cadence
- Build a content/promotions calendar for the next 90 days
- Separate promotional campaigns from nurture/educational sends
- Use smart sending and segmentation to manage fatigue

---

## Category 4 — Campaign Frequency

**What Katie Analyzes:**
Whether campaign frequency is appropriate — not too low (missed revenue) or too high (list fatigue, unsubscribes, deliverability damage).

**Key Metrics:**
- Campaigns per week (average over audit period)
- Campaigns per week to broad lists vs. engaged segments
- Unsubscribe rate trend correlated with send frequency
- Spam complaint rate trend

**Common Findings:**
- Less than 1 campaign per week — underutilization of list
- More than 5 campaigns per week to broad segments — fatigue risk
- High unsubscribes correlating with heavy send weeks
- No frequency cap or smart sending active

**Recommended Actions:**
- Set a target send cadence (1–3 campaigns per week is typical for ecommerce)
- Enable Klaviyo's Smart Sending feature
- Segment campaigns so heavy-send weeks only hit engaged profiles
- Set a 24-hour or 3-day frequency exclusion on non-promotional sends

---

## Category 5 — Campaign Segmentation

**What Katie Analyzes:**
Who receives campaigns — whether they are sent to engaged, qualified segments or blasted to the entire list regardless of engagement status.

**Key Metrics:**
- % of campaigns sent to engaged segments vs. broad lists
- Largest segment targeted in campaigns (size vs. engaged list)
- Overlap between campaign segments and unengaged profiles
- Number of distinct campaign targeting strategies used

**Common Findings:**
- All campaigns sent to full list regardless of engagement
- No engaged-only segment in use
- Over-complex segmentation with overlapping audiences
- VIP customers receiving the same campaigns as cold prospects

**Recommended Actions:**
- Create an Engaged 30-Day and Engaged 90-Day segment for regular campaigns
- Create separate segment tracks for: customers, prospects, VIP, SMS subscribers
- Stop sending to anyone who has not engaged in 180+ days without a re-engagement campaign
- Audit overlapping segments for deduplication

---

## Category 6 — Deliverability Health

**What Katie Analyzes:**
The health of the account's sending reputation — bounce rates, spam complaint rates, unsubscribe rates, domain authentication, and list hygiene signals.

**Key Metrics:**
- Hard bounce rate (%)
- Soft bounce rate (%)
- Spam complaint rate (%)
- Unsubscribe rate per campaign (%)
- SPF record status
- DKIM record status
- DMARC record status
- Branded/dedicated sending domain in use

**Common Findings:**
- Elevated spam complaint rate (> 0.08%) threatening inbox placement
- No DMARC record — domain exposed to spoofing
- Sending to unengaged profiles driving high unsubscribes
- No branded sending domain — using Klaviyo default domain
- Bounce rate increasing over time (list aging)

**Recommended Actions:**
- Set up DMARC at minimum p=none if missing
- Set up a branded sending domain
- Implement bounce suppression rules
- Suppress profiles with spam complaints immediately
- Move to engaged-segment-only sending if spam rate is elevated
- Run a deliverability audit on domain reputation with a third-party tool

---

## Category 7 — Benchmark Performance

**What Katie Analyzes:**
How the account's campaign and flow performance compares to Klaviyo's industry benchmarks. Benchmark data includes ratings for open rate, click rate, conversion rate, flow revenue, and other key metrics.

**Key Metrics:**
- Open rate benchmark rating (Poor / Below Average / Average / Good / Excellent)
- Click rate benchmark rating
- Conversion rate benchmark rating
- Revenue per recipient benchmark rating
- Flow revenue benchmark rating
- Overall benchmark performance summary

**Common Findings:**
- Most benchmarks rated Average or Below Average — general performance maturity issue
- Campaign benchmarks strong but flow benchmarks poor — lifecycle gap
- Flow benchmarks strong but campaign benchmarks weak — segmentation or creative issue
- Excellent benchmarks across the board (positive finding — rare)

**Recommended Actions:**
- If campaigns underperform benchmarks: review subject lines, segmentation, offer structure, and send time
- If flows underperform benchmarks: review timing, message count, copy, and incentive strategy
- Use benchmark data as a baseline for the 90-day improvement plan
- Revisit benchmarks at next audit to measure progress

---

## Category 8 — Core Flow Coverage

**What Katie Analyzes:**
Whether the 7 core ecommerce lifecycle flows exist in the account and are in Live status.

**Core Flows Checked:**

| Flow | Required | Revenue Impact |
|---|---|---|
| Welcome Series | Yes | High — first brand impression, initial conversion |
| Abandoned Cart | Yes | Critical — highest revenue recovery flow |
| Added to Cart | Yes | High — pre-abandonment recovery |
| Browse Abandonment | Yes | Medium-High — mid-funnel recovery |
| Post-Purchase | Yes | High — repeat purchase, LTV |
| Winback / Re-engagement | Yes | Medium — recovers dormant customers |
| VIP / Loyalty | Recommended | Medium — retention of highest-value customers |

**Key Metrics:**
- Number of core flows that are Live
- Number of core flows missing entirely
- Number of core flows in Draft or Manual status (not actively running)
- Core flow coverage score

**Common Findings:**
- Welcome flow missing — critical lifecycle gap
- Abandoned cart flow exists but is in Draft — not recovering any revenue
- No post-purchase flow — repeat purchase revenue at risk
- Only welcome and cart flows exist — browse abandonment and winback missing

**Recommended Actions:**
- Build any missing critical flow (Welcome, Abandoned Cart) within 30 days
- Set all Draft flows to Live after review
- Build Added to Cart and Browse Abandonment within 60 days
- Build Post-Purchase and Winback within 90 days

---

## Category 9 — Flow Structure and Timing

**What Katie Analyzes:**
Whether each existing flow is configured correctly — the right number of messages, correct timing delays, proper email/SMS mix, and appropriate incentive structure.

**Key Metrics per Flow:**
- Message count (emails + SMS)
- First message delay (time from trigger to first message)
- Delay between messages (sequence timing)
- SMS presence (yes / no)
- Incentive presence in messages 2–3 for transactional flows
- Email/SMS ratio

**Minimum Configuration Standards:**

| Flow | Min Emails | SMS Recommended | First Email Timing | Incentive |
|---|---|---|---|---|
| Welcome | 4 | Yes (if consent) | Within 1 hour | Optional |
| Abandoned Cart | 3 | 2+ | Within 1 hour | Email 2 or 3 |
| Added to Cart | 3 | 2+ | Within 1 hour | Email 2 or 3 |
| Browse Abandonment | 1–2 | 1+ | Within 1–4 hours | Optional |
| Post-Purchase | 3+ | Optional | Within 24 hours | Not required |
| Winback | 3+ | Optional | 90–180 days after last engage | Yes — compelling offer |
| VIP | 2+ | Optional | As earned | Exclusive offer |

**Common Findings:**
- Abandoned cart has only 1 email — missing recovery sequence
- Welcome flow has 6 emails but no SMS — SMS consented profiles not activated
- First abandoned cart email goes out 6 hours after abandonment — should be within 1 hour
- No incentive in any abandoned cart message — conversion rate suppressed
- Flows unchanged in 12+ months — stale copy and outdated offers

**Recommended Actions:**
- Rebuild any flow that falls below minimum message count
- Fix timing on abandoned cart first email to fire within 60 minutes
- Add SMS steps to all transactional flows where consent is available
- Add a discount or incentive to messages 2 and/or 3 of abandoned cart
- Review and refresh all flow copy and offers annually

---

## Category 10 — Flow Revenue Contribution

**What Katie Analyzes:**
How much of the account's total Klaviyo-attributed revenue comes from flows vs. campaigns, and whether flow revenue is at a healthy level relative to account maturity.

**Key Metrics:**
- Total Klaviyo revenue (audit period)
- Flow revenue (total and by flow)
- Campaign revenue (total)
- Flow revenue as % of total Klaviyo revenue
- Top 3 revenue-generating flows
- Underperforming flows (exist but generate minimal revenue)

**Benchmarks:**
- Flows < 20% of Klaviyo revenue: Lifecycle automation is underperforming
- Flows 20–35%: Developing — room to improve
- Flows 35–50%: Healthy — strong automation
- Flows > 50%: Excellent — highly automated retention revenue

**Common Findings:**
- Flow revenue is 8% of total — critical lifecycle underperformance
- Abandoned cart flow exists but generates only $200/month — likely misconfigured
- Campaign revenue is high but flow revenue is near zero — no automation working
- Welcome flow drives most flow revenue; other flows contribute nothing

**Recommended Actions:**
- Rebuild underperforming flows with correct timing and message count
- Add SMS to low-performing flows where consent exists
- Set up missing flows to grow automation revenue share
- Track flow revenue monthly and set a 12-month improvement target

---

## Category 11 — SMS in Flows

**What Katie Analyzes:**
Whether SMS messages are included in existing flows, and whether the account is activating its SMS-consented audience through lifecycle automation.

**Key Metrics:**
- Number of flows with at least one SMS message
- Number of flows with zero SMS messages (despite SMS being enabled)
- SMS messages in abandoned cart (target: 2+ where consent exists)
- SMS messages in welcome flow
- SMS opt-out rate within flows
- SMS click rate within flows

**Common Findings:**
- SMS enabled in account but no flows use SMS
- Abandoned cart has 3 emails but 0 SMS — major gap if SMS consented profiles exist
- Welcome flow sends 6 emails but no SMS to consented subscribers
- SMS is used in flows but only for one touchpoint — not fully activated
- SMS opt-out rate is elevated — SMS copy or timing needs review

**Recommended Actions:**
- Add SMS steps to all transactional flows for SMS-consented profiles
- Prioritize abandoned cart SMS — it typically has the highest recovery rate
- Review SMS timing (immediate follow-ups for cart/browse abandonment)
- Review SMS content — SMS must be concise and include a clear CTA
- Monitor SMS opt-out rate — if elevated, review frequency and relevance

---

## Category 12 — Signup Forms

**What Katie Analyzes:**
Whether the account has active signup forms, how many there are, and whether they are collecting both email and SMS consent.

**Key Metrics:**
- Number of published signup forms
- Form types (popup / flyout / embed / full page)
- Email capture enabled (yes / no)
- SMS capture enabled (yes / no)
- Incentive offered (yes / no / type)
- Display rules (exit-intent / time-delay / scroll / always-on)

**Common Findings:**
- No active signup form — list growth is entirely organic or purchased
- Signup form collects email only — SMS not being collected
- Form has no incentive — opt-in rate suppressed
- Only a footer embed with no popup — low visibility and conversion
- Multiple forms but no A/B testing active

**Recommended Actions:**
- Publish a popup with an incentive (discount, lead magnet, or exclusive offer)
- Add SMS opt-in option to all signup forms
- Test exit-intent vs. scroll-triggered popup timing
- A/B test incentive types (% vs. $ vs. free shipping)
- Ensure mobile popup complies with Google's mobile interstitial guidelines

---

## Category 13 — Form Opt-In Rate

**What Katie Analyzes:**
The conversion rate of existing signup forms — how many people who see the form actually submit their email (and/or phone number).

**Key Metrics:**
- Overall opt-in rate (submits / views)
- Email opt-in rate
- SMS opt-in rate (where applicable)
- Mobile opt-in rate vs. desktop opt-in rate
- Opt-in rate by form type

**Performance Benchmarks:**

| Opt-In Rate | Performance Level |
|---|---|
| Under 2% | Weak — needs significant improvement |
| 2–3.9% | Average — acceptable but improvable |
| 4–5.9% | Good — strong performance |
| 6%+ | Excellent — top-tier capture rate |

**Common Findings:**
- Popup opt-in rate is 0.8% — below 2% minimum threshold
- Mobile opt-in rate (0.6%) significantly below desktop (2.1%)
- No incentive on form — opt-in rate depressed
- Form displays too quickly (immediately on page load) — dismissal rate high
- Form is tested and achieving 5.2% opt-in — positive finding

**Recommended Actions:**
- If opt-in rate < 2%: test a new offer, change display timing, redesign form
- If mobile opt-in rate is weak: optimize mobile form design, reduce fields
- Add or upgrade the incentive
- Test exit-intent timing vs. scroll-trigger timing
- A/B test form headline copy

---

## Category 14 — List Health

**What Katie Analyzes:**
The overall quality and engagement health of the email list — how many profiles are active, engaged, and deliverable vs. dormant, suppressed, or decaying.

**Key Metrics:**
- Total profiles
- Emailable profiles
- Suppressed profiles (%)
- Engaged 30-day profiles (%)
- Engaged 90-day profiles (%)
- Engaged 180-day profiles (%)
- Dormant profiles (not engaged in 180+ days) (%)
- Suppression growth trend

**Common Findings:**
- 68% of emailable profiles have not engaged in 180+ days — deliverability risk
- Suppression rate is 22% — unusually high, suggests historical list quality issues
- Engaged 30-day list is less than 5% of total list — extremely narrow active audience
- List growing in total size but engaged segment shrinking — list quality degrading
- List health is strong — engaged 90-day represents 45% of emailable list (positive)

**Recommended Actions:**
- Run a re-engagement / sunset campaign for profiles not engaged in 180+ days
- Suppress non-responders after sunset campaign
- Stop sending regular campaigns to unengaged profiles
- Build and enforce engaged-segment targeting rules for all campaigns
- Review list growth sources — purchased lists or incentive misalignment drive poor engagement

---

## Category 15 — Engagement Segmentation

**What Katie Analyzes:**
Whether the account has active engagement-based segments and whether campaigns are using them to protect deliverability and revenue efficiency.

**Key Metrics:**
- Engaged 30-day segment exists (yes / no)
- Engaged 90-day segment exists (yes / no)
- VIP segment exists (yes / no)
- Purchaser vs. prospect segments in use (yes / no)
- % of campaigns sent to engaged segments (vs. all-subscriber blasts)
- Segment sophistication score

**Common Findings:**
- No engagement-based segments exist — all campaigns go to the full list
- Engaged segment exists but is not used consistently in campaign targeting
- VIP segment exists but receives identical campaign content to general list
- Segments are complex and overlapping — creating deliverability confusion
- Strong segmentation in place (positive finding)

**Recommended Actions:**
- Create engaged 30/60/90-day segments if they do not exist
- Make engaged segment targeting mandatory for all non-promotional broadcast campaigns
- Create a purchaser segment and a high-LTV / VIP segment
- Use Klaviyo's predictive analytics segments where available on plan
- Review and simplify any overly complex segment definitions

---

## Category 16 — Revenue Attribution

**What Katie Analyzes:**
How Klaviyo-attributed revenue is distributed across flows and campaigns, which channels and flows contribute the most, and whether the account's revenue is over-reliant on campaigns vs. automated lifecycle flows.

**Key Metrics:**
- Total Klaviyo revenue (audit period)
- Campaign revenue ($ and % of total)
- Flow revenue ($ and % of total)
- Top 3 revenue-generating flows
- Top 3 revenue-generating campaigns
- Revenue per recipient (campaigns and flows)
- Email revenue vs. SMS revenue split

**Common Findings:**
- 92% of Klaviyo revenue comes from campaigns — almost no flow revenue
- Abandoned cart flow is the #1 revenue flow but still underperforming vs. industry benchmarks
- SMS contributes 0% of Klaviyo revenue — no SMS program
- Revenue per recipient is declining — list fatigue or offer degradation
- Healthy flow/campaign split: flows drive 38% of total Klaviyo revenue (positive)

**Recommended Actions:**
- If flows are < 20% of revenue: treat core flow rebuild as the #1 priority
- If SMS is 0%: SMS launch is the highest-leverage opportunity
- If revenue per recipient declining: review segmentation, offer strategy, list health
- Add revenue attribution tracking to all flows if not already configured
- Benchmark flow revenue against prior period to measure improvement

---

## Category 17 — Billing Efficiency

**What Katie Analyzes:**
Whether the client is paying for a Klaviyo plan that matches their actual usable audience, or whether they are overpaying for profiles they cannot effectively email.

**Key Metrics:**
- Plan tier / profile limit
- Total profiles in account
- Emailable profiles (suppressed removed)
- Engaged profiles (active audience)
- Billing utilization rate (emailable / plan limit)
- Estimated monthly overpay (if any)

**Overpay Risk Thresholds:**

| Utilization | Status |
|---|---|
| > 80% of plan limit | Healthy — may need to upgrade soon |
| 50–80% of plan limit | Normal — no action required |
| 25–50% of plan limit | Borderline — review if sustainable |
| < 25% of plan limit | Overpay risk — plan tier likely too large |

**Common Findings:**
- Account has 82,000 profiles but only 23,000 are emailable and engaged — paying for 59,000 unusable profiles
- Suppressed profiles account for 30% of plan tier — inflating billing without value
- Billing utilization is healthy at 71% — no action needed (positive)
- Client upgraded plan for an old campaign list that was never cleaned

**Recommended Actions:**
- If overpay risk: recommend list hygiene, suppression cleanup, and potential plan downgrade
- Suppress permanently unengaged contacts to reduce billable profile count
- Review whether purchased or imported lists that never engaged can be safely purged
- Flag billing review to client — NP does not make billing changes directly

---

## Category 18 — Compliance and Consent

**What Katie Analyzes:**
Whether the account has proper email authentication records in place, whether SMS consent is being collected and documented correctly, and whether any visible compliance risks exist.

**Key Metrics:**
- SPF record present (yes / no)
- DKIM record present (yes / no)
- DMARC record present (yes / no)
- Branded/dedicated sending domain in use (yes / no)
- SMS consent collection method (form opt-in / keyword opt-in / other)
- Double opt-in enabled on email lists (yes / no)
- Compliance jurisdiction flags (GDPR / CCPA noted if applicable)

**Common Findings:**
- No DMARC record — domain vulnerable to spoofing and deliverability scoring penalties
- SMS subscribers collected without proper consent documentation
- Email list includes purchased contacts — high compliance and deliverability risk
- No branded sending domain — sending from Klaviyo default domain
- Single opt-in for EU traffic — potential GDPR exposure

**Recommended Actions:**
- Set up DMARC at minimum p=none immediately
- Set up branded sending domain
- Confirm SMS consent documentation is compliant with TCPA requirements
- Do not purchase email lists — this violates Klaviyo's ToS and damages deliverability
- If EU audience: consider implementing double opt-in or explicit GDPR consent
- Flag compliance concerns to legal or compliance team for review

**Disclaimer:** Katie identifies potential compliance risks. She does not provide legal advice and cannot certify compliance. All compliance recommendations must be reviewed by a qualified professional.

---

## Category 19 — Template and Creative Quality

**What Katie Analyzes:**
The general quality, structure, and optimization of email templates used in campaigns and flows. Note: This category relies partly on manual review, as API data provides limited creative insight.

**Key Metrics (from API where available):**
- Templates in use vs. templates in account
- Channel-specific template count
- Subject line length (characters)
- Presence of personalization tokens in subject lines
- Preview text presence

**Manual Review Criteria (for NP strategist):**
- Mobile responsiveness
- Image-to-text ratio (too many images = spam risk)
- Alt text on images
- CTA button visibility and count
- Personalization beyond first name
- Brand consistency
- Link count (excessive links reduce click focus)
- Discount code display (clear and easy to copy)

**Common Findings:**
- Subject lines exceed 60 characters — mobile truncation likely
- No preview text on 60% of campaigns — missed inbox impression
- Templates are image-heavy with no alt text — poor for image-blocking email clients
- One global template used for all campaigns — no seasonal or campaign-type variation
- Strong personalization and dynamic content in use (positive finding)

**Recommended Actions:**
- Keep subject lines under 50 characters for mobile optimization
- Always populate preview text — it doubles the visible inbox real estate
- Add alt text to all images
- Reduce image-to-text ratio; ensure emails render without images
- A/B test subject line personalization
- Review template mobile rendering in Klaviyo's preview tool

---

## Category 20 — Lifecycle Coverage

**What Katie Analyzes:**
Whether the account's flows and campaigns cover the full customer lifecycle — from acquisition through repeat purchase, loyalty, and reactivation.

**Lifecycle Stages Checked:**

| Stage | Coverage Vehicle | Common Gap |
|---|---|---|
| Acquisition | Signup form → Welcome flow | Missing welcome or SMS in welcome |
| First purchase | Abandoned cart + Added to cart | Missing flows or poor timing |
| Post-purchase | Post-purchase flow | Missing entirely |
| Repeat purchase | Campaign segmentation + Browse/Cart flows | No repeat customer track |
| Loyalty / VIP | VIP segment + VIP flow | No VIP recognition |
| Replenishment | Replenishment flow (if applicable) | Missing for replenishable products |
| Winback | Winback flow | Missing or not running |
| Sunset | Sunset / unengaged flow | Missing — cold profiles never removed |

**Common Findings:**
- Account has acquisition and abandonment flows but nothing post-purchase
- No winback flow — churned customers never contacted
- No VIP program — best customers receive identical experience to new subscribers
- Replenishment products sold but no replenishment reminder flow
- No sunset flow — unengaged profiles accumulate indefinitely

**Recommended Actions:**
- Map the full customer journey and identify lifecycle stage gaps
- Build post-purchase flow within 60 days — highest ROI for existing customer base
- Build winback flow for customers inactive 90–180 days
- Build sunset / suppression flow for profiles inactive 365+ days
- Create a VIP segment and a distinct VIP communication track

---

## Category 21 — Missed Revenue Opportunities

**What Katie Analyzes:**
A synthesized view of the top revenue opportunities identified across all categories, quantified (directionally) where data supports it.

**Framework:**
For each major gap, Katie estimates a directional revenue recovery range based on:
- Account's current flow/campaign revenue baseline
- Industry average recovery rates for the missing element
- SMS-consented profile count and average order value

**Example Opportunity Framing:**
> "Based on your current abandoned cart flow structure (1 email, no SMS) and an AOV of approximately $95, adding a full 3-email + 2-SMS abandoned cart sequence may recover a meaningful portion of the estimated monthly cart abandonment value. A National Positions strategist can model this more precisely with your actual traffic and abandonment data."

**Opportunities Always Assessed:**
- Missing abandoned cart SMS (typically highest-impact single gap)
- Missing welcome flow or welcome flow with fewer than 4 emails
- No SMS program (entire SMS revenue channel missing)
- Low form opt-in rate (list growth suppressing all future revenue)
- No post-purchase flow (repeat purchase revenue at risk)
- Unengaged list depleting deliverability (suppressing all channel performance)
- Poor benchmark performance (signal of broader performance degradation)

---

## Category 22 — 30 / 60 / 90 Day Action Plan

**What Katie Produces:**
A structured, prioritized action plan organized into three timeframes based on impact, effort, and dependency order.

**Format:**

| Timeframe | Focus | Example Actions |
|---|---|---|
| 30 Days | Critical fixes and quick wins | Fix abandoned cart timing, launch SMS opt-in on forms, set up DMARC |
| 60 Days | Core build-outs | Build missing flows, improve form opt-in rate, set up engaged segmentation |
| 90 Days | Strategic improvements | Post-purchase flow, winback flow, VIP program, benchmark tracking |

**Each action item includes:**
- Task description
- Why it matters (business impact)
- Owner (client, NP team, or shared)
- Effort (Easy / Moderate / Complex)
- Estimated impact (High / Medium / Low)
- Dependencies (what must be done first)

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-05-10 | Initial audit categories — Phase 1 |
