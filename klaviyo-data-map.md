# Klaviyo Audit Katie — Klaviyo Data Map

**Version:** 1.0
**Owner:** National Positions
**Classification:** Internal Operating Framework — Phase 1
**Last Updated:** 2026-05-10

---

## Overview

This document maps every Klaviyo data object Katie needs for the audit. For each object, it defines the specific fields required, why those fields matter, which audit categories they support, and what metrics or findings can be derived from them.

All field names and availability must be verified against the current Klaviyo API documentation during implementation. Field availability may vary by Klaviyo plan tier.

---

## Object 1 — Account

**API Endpoint (estimated):** `GET /api/accounts/`

| Field | Why It Matters | Audit Section |
|---|---|---|
| Account ID | Confirms connection to the correct account | All sections |
| Account name | Appears on every page of the report | Document header |
| Contact email | Deliverability/domain cross-reference | Deliverability |
| Timezone | Ensures campaign timing analysis is correct | Campaign, Flow timing |
| Currency | Revenue figures display correctly | Revenue attribution |
| Industry | Benchmark comparison context | Benchmark |
| Plan tier / subscription | Billing efficiency, profile limit | Billing efficiency |

**Derived Metrics:**
- Plan tier label for report header
- Billing tier name for billing section

---

## Object 2 — Campaigns

**API Endpoint (estimated):** `GET /api/campaigns/`

| Field | Why It Matters | Audit Section |
|---|---|---|
| Campaign ID | Unique identifier | All campaign sections |
| Campaign name | Display and categorization | Campaign audit |
| Status (sent / draft / scheduled) | Only sent campaigns are analyzed | Campaign audit |
| Send datetime | Frequency calculation, day-of-week analysis | Campaign frequency |
| Channel (email / SMS) | Channel mix analysis | SMS adoption, Campaign |
| Audience (list or segment ID) | Segmentation quality | Campaign segmentation |
| Message ID (linked) | Pull message-level details | Campaign audit |
| Send count (recipients) | Reach and scale | Campaign audit |
| Subject line | Creative and optimization review | Template quality |
| Preview text | Creative review | Template quality |

**Derived Metrics:**
- Campaigns sent per week/month
- Email vs. SMS campaign split
- % campaigns sent to engaged segments vs. broad lists
- Average recipients per campaign

---

## Object 3 — Campaign Messages

**API Endpoint (estimated):** `GET /api/campaign-messages/`

| Field | Why It Matters | Audit Section |
|---|---|---|
| Message ID | Links to campaign | Campaign audit |
| Channel (email / SMS) | Channel analysis | SMS audit |
| Open rate | Deliverability, creative, subject line performance | Deliverability, Campaign |
| Click rate | Engagement, CTA effectiveness | Campaign audit |
| Conversion rate | Revenue driving effectiveness | Revenue attribution |
| Placed order rate | Direct purchase attribution | Revenue attribution |
| Revenue | Campaign revenue contribution | Revenue attribution |
| Bounce rate | Deliverability health | Deliverability |
| Unsubscribe rate | List fatigue, frequency issues | Campaign, Deliverability |
| Spam complaint rate | Critical deliverability signal | Deliverability |
| Unique opens | Reach analysis | Campaign |
| Unique clicks | Engagement depth | Campaign |

**Derived Metrics:**
- Average campaign open rate (over audit period)
- Average click rate
- Average unsubscribe rate
- Average spam complaint rate
- Revenue per campaign
- Revenue per recipient (revenue / send count)

---

## Object 4 — Flows

**API Endpoint (estimated):** `GET /api/flows/`

| Field | Why It Matters | Audit Section |
|---|---|---|
| Flow ID | Unique identifier | Flow audit |
| Flow name | Identifies flow type | Flow coverage |
| Status (Live / Draft / Manual / Archived) | Only Live flows are counted as active | Flow coverage |
| Trigger type (e.g., list, segment, metric) | Flow logic validation | Flow configuration |
| Created date | Flow age context | Flow audit |
| Last updated date | How recently maintained | Flow configuration |
| Message count | Coverage depth per flow | Flow configuration |
| Revenue (if available) | Flow revenue contribution | Revenue attribution |
| Conversion rate (if available) | Flow effectiveness | Revenue attribution |
| Tags | Organization and flow categorization | Flow audit |

**Core Flows to Specifically Check (by name pattern matching):**

| Flow Type | Common Name Patterns |
|---|---|
| Welcome Series | "Welcome", "New Subscriber", "Welcome Series" |
| Abandoned Cart | "Abandoned Cart", "Cart Abandonment" |
| Added to Cart | "Added to Cart", "Browse + Cart" |
| Browse Abandonment | "Browse Abandonment", "Viewed Product" |
| Post-Purchase | "Post-Purchase", "Thank You", "After Purchase" |
| Winback / Re-engagement | "Winback", "Win Back", "Re-engagement", "We Miss You" |
| VIP / Loyalty | "VIP", "Loyalty", "Top Customer" |
| Replenishment | "Replenishment", "Reorder", "Running Low" |
| Sunset / Unengaged | "Sunset", "Unengaged", "Last Chance" |

**Derived Metrics:**
- Total live flows
- Core flow coverage score (how many of the 7 core flows exist and are live)
- % of flows with SMS messages
- Flow revenue as % of total Klaviyo revenue

---

## Object 5 — Flow Messages

**API Endpoint (estimated):** `GET /api/flow-messages/`

| Field | Why It Matters | Audit Section |
|---|---|---|
| Message ID | Unique identifier | Flow configuration |
| Flow ID (linked) | Links to parent flow | Flow configuration |
| Channel (email / SMS) | Channel mix within flow | SMS in flows |
| Position in flow | Message sequence order | Flow timing |
| Time delay (from trigger or prior message) | Timing correctness | Flow timing |
| Subject line (email) | Creative review | Template quality |
| Open rate | Message performance | Flow configuration |
| Click rate | Engagement | Flow configuration |
| Conversion rate | Revenue attribution | Revenue |
| Revenue | Per-message revenue contribution | Revenue attribution |
| Status (Live / Draft) | Only live messages count | Flow coverage |

**Derived Metrics:**
- Number of emails per flow
- Number of SMS messages per flow
- Email-to-SMS ratio per flow
- Time from trigger to first message (critical for abandoned cart)
- Time between messages (delay sequence validation)
- Flow message performance scores

---

## Object 6 — Lists

**API Endpoint (estimated):** `GET /api/lists/`

| Field | Why It Matters | Audit Section |
|---|---|---|
| List ID | Unique identifier | List health |
| List name | Context and categorization | List health |
| Profile count | List size baseline | List health |
| Created date | List age context | List health |
| Opt-in process (single vs. double) | Compliance and deliverability | Compliance |
| Folder / tag | Organization | List health |

**Derived Metrics:**
- Total list profiles vs. total account profiles
- Main list size
- Number of lists (organizational complexity)

---

## Object 7 — Segments

**API Endpoint (estimated):** `GET /api/segments/`

| Field | Why It Matters | Audit Section |
|---|---|---|
| Segment ID | Unique identifier | Segmentation |
| Segment name | Identifies segment type | Segmentation |
| Profile count | Segment size | Segmentation |
| Segment definition / conditions | Segmentation sophistication | Segmentation |
| Created date | How recently set up | Segmentation |
| Is engaged segment | Critical for deliverability-safe sending | Campaign segmentation |
| Is VIP segment | Lifecycle sophistication | Lifecycle coverage |
| Is purchaser segment | Behavioral targeting | Segmentation |

**Segments to Specifically Check:**

| Segment Type | Why It Matters |
|---|---|
| Engaged 30-day | Should be used for broadcast campaigns |
| Engaged 60-day | Secondary broadcast target |
| Engaged 90-day | Outer boundary for safe sending |
| Active customers | Purchaser targeting |
| VIP / high LTV | Premium segment for exclusive offers |
| Unengaged / sunset candidates | Should not receive campaigns |
| SMS consented | SMS send eligibility |
| Non-purchasers | Conversion-focused targeting |

**Derived Metrics:**
- Engaged 30-day segment size as % of total emailable profiles
- Engaged 90-day segment size
- % of campaigns sent to engaged segments
- Number of engagement-based segments vs. static segments

---

## Object 8 — Profiles (Aggregate Only)

**API Endpoint (estimated):** `GET /api/profiles/`

**Important:** Katie uses only aggregate-level profile statistics. Individual profile records are not retrieved, stored, or included in any output. PII is never collected.

| Metric | Why It Matters | Audit Section |
|---|---|---|
| Total profile count | Account scale | List health, Billing |
| Emailable profile count | Deliverable audience size | List health, Deliverability |
| SMS consented profile count | SMS opportunity sizing | SMS adoption |
| Engaged 30-day count | Active, high-value audience | List health |
| Engaged 60-day count | Secondary active audience | List health |
| Engaged 90-day count | Outer engagement boundary | List health, Deliverability |
| Engaged 180-day count | Broad engagement baseline | List health |
| Suppressed profile count | List decay and deliverability signal | Deliverability, Billing |
| Customer vs. prospect split | Lifecycle marketing coverage | Lifecycle coverage |
| Profiles with purchase history | Purchaser audience sizing | Revenue attribution |

**Derived Metrics:**
- Engaged 30-day % of total emailable profiles
- Suppression rate (suppressed / total profiles)
- SMS consent rate (SMS consented / emailable profiles)
- Dormant profile ratio (not engaged in 180 days / total emailable)

---

## Object 9 — Forms

**API Endpoint (estimated):** `GET /api/forms/` (verify availability)

| Field | Why It Matters | Audit Section |
|---|---|---|
| Form ID | Unique identifier | Signup forms |
| Form name | Context and type | Signup forms |
| Status (Published / Draft / Archived) | Active forms only | Signup forms |
| Form type (popup / flyout / embed / full-page) | Format strategy | Signup forms |
| Views | Traffic to form | Opt-in rate |
| Submits | Successful captures | Opt-in rate |
| Opt-in rate (submits / views) | List growth efficiency | Form opt-in rate |
| Email capture enabled | Core capture | Signup forms |
| SMS capture enabled | SMS list growth | SMS adoption |
| Incentive type (discount / lead magnet / none) | Conversion driver | Form opt-in rate |
| Display rules (timing, scroll, exit-intent) | Conversion optimization | Form opt-in rate |
| Mobile views / mobile submits | Mobile optimization | Form opt-in rate |
| Desktop opt-in rate vs. mobile opt-in rate | Device-specific performance | Form opt-in rate |

**Derived Metrics:**
- Overall form opt-in rate
- Mobile-specific opt-in rate
- SMS capture rate (SMS submits / total submits)
- % of forms collecting both email and SMS

---

## Object 10 — Metrics

**API Endpoint (estimated):** `GET /api/metrics/`

| Field | Why It Matters | Audit Section |
|---|---|---|
| Metric ID | Unique identifier | Revenue attribution |
| Metric name | Identifies what's being tracked | All metric-dependent sections |
| Metric integration source | Confirms ecommerce platform connection | Technical setup |

**Key Metrics to Confirm Are Active:**

| Metric | Audit Impact If Missing |
|---|---|
| Placed Order | Cannot calculate revenue attribution |
| Ordered Product | Cannot assess product-level performance |
| Active on Site | Browse abandonment trigger may not work |
| Viewed Product | Browse abandonment trigger dependency |
| Added to Cart | Added to cart flow trigger dependency |
| Started Checkout | Abandoned cart trigger dependency |
| Fulfilled Order | Post-purchase flow trigger dependency |
| Received Email / Clicked Email | Core email engagement tracking |
| Received SMS / Clicked SMS | Core SMS engagement tracking |

---

## Object 11 — Email Events

**API Endpoint (estimated):** `GET /api/events/` (filtered by metric)

| Event Type | Why It Matters | Audit Section |
|---|---|---|
| Received Email | Send volume baseline | Campaign, Flow |
| Opened Email | Engagement signal | Deliverability, Campaign |
| Clicked Email | Engagement depth | Campaign, Flow |
| Unsubscribed | List fatigue, frequency signal | Deliverability |
| Marked as Spam | Critical deliverability alert | Deliverability |
| Bounced Email | List quality, deliverability | Deliverability |
| Failed to Deliver | Technical sending issues | Deliverability |

**Derived Metrics:**
- Aggregate open rate over audit period
- Aggregate click rate
- Aggregate unsubscribe rate
- Aggregate spam complaint rate
- Hard bounce rate
- Soft bounce rate

---

## Object 12 — SMS Events

**API Endpoint (estimated):** `GET /api/events/` (filtered by SMS metrics)

| Event Type | Why It Matters | Audit Section |
|---|---|---|
| Received SMS | SMS send volume | SMS adoption |
| Clicked SMS | SMS engagement | SMS audit |
| Unsubscribed from SMS | SMS list health | SMS adoption |
| Failed SMS | SMS deliverability | SMS audit |
| Opted In via SMS | SMS list growth | SMS adoption |

**Derived Metrics:**
- SMS send volume in audit period
- SMS click rate
- SMS opt-out rate
- SMS vs. email revenue contribution ratio

---

## Object 13 — Deliverability Signals

Deliverability is assessed from aggregated event data, not a single API endpoint.

| Signal | Source | Threshold for Concern |
|---|---|---|
| Hard bounce rate | Email events | > 0.5% is a warning; > 2% is critical |
| Spam complaint rate | Email events | > 0.08% (Gmail threshold); > 0.3% is critical |
| Unsubscribe rate | Email events | > 0.5% per campaign is elevated |
| Open rate trend | Email events | Declining trend signals deliverability degradation |
| SPF record | Technical check (manual or third-party) | Missing = high risk |
| DKIM record | Technical check | Missing = high risk |
| DMARC record | Technical check | Missing = elevated risk |
| Branded/dedicated sending domain | Account configuration | Missing = moderate risk |

**Derived Score:**
Katie produces a Deliverability Health Level:
- **Critical:** Spam complaint rate > 0.3% OR bounce rate > 2% OR missing SPF/DKIM
- **Needs Improvement:** Spam > 0.08% OR bounce 0.5–2% OR missing DMARC
- **Acceptable:** All rates within threshold but no dedicated domain
- **Strong:** All rates within threshold + branded sending domain + DKIM/SPF/DMARC all present

---

## Object 14 — Benchmarks

**API Endpoint:** Verify availability via Klaviyo API (Klaviyo provides benchmark data in some plan tiers)

If available via API:

| Benchmark Field | Why It Matters | Audit Section |
|---|---|---|
| Open rate benchmark (by industry) | Campaign performance context | Benchmark review |
| Click rate benchmark | Campaign performance context | Benchmark review |
| Flow revenue benchmark | Lifecycle performance context | Benchmark review |
| List growth benchmark | Audience health context | Benchmark review |
| Benchmark rating label | Poor / Below Average / Average / Good / Excellent | Benchmark review |

**If not available via API:**
Use Klaviyo's published industry benchmarks (manually updated quarterly by NP). Flag in report as "Industry benchmark — source: Klaviyo published data."

---

## Object 15 — Billing / Plan Data

**API Endpoint:** Verify availability (Klaviyo may not expose billing data via public API)

If available:

| Field | Why It Matters | Audit Section |
|---|---|---|
| Plan tier name | Context for billing review | Billing efficiency |
| Profile limit (paid tier) | Compare to actual profile count | Billing efficiency |
| Active profile count (billed) | Utilization calculation | Billing efficiency |
| Monthly cost (if accessible) | Cost per active profile | Billing efficiency |

**If billing data is not accessible via API:**
- Flag the Billing Efficiency section as "Requires manual review"
- Request plan tier and profile count from client directly
- Estimate billing utilization based on profile count from profiles API

**Derived Metrics:**
- Billing utilization rate = active profiles / plan profile limit
- Overpay risk signal (if utilization < 50%)
- Cost per emailable profile (if billing data provided)

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-05-10 | Initial data map — Phase 1 |
