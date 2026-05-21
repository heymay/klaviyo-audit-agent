# Klaviyo Audit Katie — Recommendation Engine

**Version:** 1.0
**Owner:** National Positions
**Classification:** Internal Operating Framework — Phase 1
**Last Updated:** 2026-05-10

---

## Overview

This document defines the framework for generating, ranking, and presenting recommendations in every Klaviyo audit. Every recommendation produced by Katie follows a consistent structure, is prioritized by revenue impact and implementation effort, and is presented with appropriate confidence levels and disclaimers.

The recommendation engine transforms decision rule findings into actionable, prioritized guidance for both business owners and marketing practitioners.

---

## Recommendation Data Model

Every recommendation includes the following fields:

| Field | Description |
|---|---|
| **Recommendation ID** | Unique identifier (e.g., REC-001) |
| **Source Rule ID** | The decision rule(s) that triggered this recommendation |
| **Issue** | Plain-English description of the problem |
| **Why It Matters** | Business impact of leaving this unaddressed |
| **Expected Impact** | Revenue / deliverability / list growth impact (High / Medium / Low) |
| **Implementation Complexity** | How difficult this is to implement (Easy / Moderate / Complex) |
| **Priority** | Critical / High / Medium / Low |
| **Owner** | Who should implement: NP, Client, or Shared |
| **Timeline** | Immediate / 30 days / 60 days / 90 days |
| **Data Confidence** | Confirmed / Likely / Inferred |
| **Opportunity Note** | Optional directional revenue framing (with disclaimer) |
| **Recommended Next Step** | The single most important first action |

---

## Priority Levels

| Priority | Definition | Timeline |
|---|---|---|
| **Critical** | Revenue-blocking, deliverability-threatening, or legally risky gap | Immediate (within 30 days) |
| **High** | Significant performance gap with clear, measurable revenue impact | Within 30–60 days |
| **Medium** | Meaningful optimization opportunity with positive ROI | Within 60–90 days |
| **Low** | Best practice gap or marginal improvement | Within 90 days or maintenance sprint |

---

## Implementation Complexity Levels

| Complexity | Definition | Examples |
|---|---|---|
| **Easy** | Can be done in Klaviyo UI without development work, typically < 2 hours | Adding SMS opt-in to a form, adding DMARC record, creating an engaged segment |
| **Moderate** | Requires strategy, copywriting, or multi-step Klaviyo configuration; typically 2–8 hours | Building a new flow from scratch, redesigning a signup form, rebuilding campaign targeting |
| **Complex** | Requires developer involvement, platform integration, or significant strategy work; typically 8+ hours | Setting up a branded sending domain, integrating Shopify for new triggers, building multi-branch flows |

---

## Timelines

| Timeline | When to Use |
|---|---|
| **Immediate** | Critical severity issues — should start within 1–2 weeks |
| **30 days** | Critical and High priority items that are Easy or Moderate complexity |
| **60 days** | High and Medium priority items, especially new flow builds |
| **90 days** | Medium and Low priority, strategic improvements, optimizations |

---

## Prioritization Algorithm

When multiple recommendations exist and ordering is needed, Katie uses this priority score to rank them:

```
Priority Score = (Revenue Impact Score × 3) + (Deliverability Impact Score × 2) + (Ease Score × 1)

Where:
- Revenue Impact Score: High = 3, Medium = 2, Low = 1
- Deliverability Impact Score: High = 3, Medium = 2, Low = 1, N/A = 0
- Ease Score (inverse of complexity): Easy = 3, Moderate = 2, Complex = 1

Maximum possible score: (3×3) + (3×2) + (3×1) = 9 + 6 + 3 = 18
```

**Example:**
- Launch SMS program: Revenue=High(3×3=9) + Deliverability=N/A(0) + Ease=Moderate(2×1=2) = 11
- Set up DMARC: Revenue=Medium(2×3=6) + Deliverability=High(3×2=6) + Ease=Easy(3×1=3) = 15
- DMARC ranks higher despite potentially feeling less exciting — it has high deliverability impact and is easy.

---

## Recommendation Deduplication Rules

Multiple decision rules may trigger similar recommendations. Before finalizing:

1. Group all recommendations by their primary action (e.g., "build Abandoned Cart flow" may be triggered by FLOW-004, FLOW-005, and FTIM-001)
2. Merge grouped recommendations into a single entry that cites all source rules
3. Set the severity to the highest severity among the merged rules
4. Combine the findings narrative to cover all sub-issues
5. Do not present the same action as two separate recommendations

---

## Opportunity Framing Guidelines

Opportunity ranges should be directional and conservative. Never state a specific revenue dollar amount as guaranteed.

**Correct framing:**
> "Based on missing Abandoned Cart SMS and a current single-email recovery sequence, there may be a meaningful revenue recovery opportunity. Accounts of similar size with a full 3-email + 2-SMS cart recovery sequence typically see higher recovery rates. A National Positions specialist can model this more precisely with your cart abandonment volume."

**Incorrect framing (do not use):**
> "Adding SMS to your Abandoned Cart flow will recover $12,000 per month."

**Opportunity Language Scale:**
- Low: "may represent a modest improvement in..."
- Medium: "could represent a meaningful improvement in..."
- High: "represents a significant and measurable gap in..."
- Critical: "is likely causing material revenue loss that warrants immediate attention"

All opportunity statements must end with: "A National Positions strategist should validate this estimate with your specific account data before any revenue projection is made."

---

## Recommendation Categories

Recommendations fall into these categories for grouping in the report:

| Category | Description |
|---|---|
| **Immediate Fixes** | Quick, high-impact actions (< 2 hours each) |
| **Flow Builds** | New flow creation or major flow rebuilds |
| **Flow Optimizations** | Timing, message count, or channel improvements to existing flows |
| **SMS Launch / Growth** | Enabling SMS, growing SMS list, adding SMS to flows/campaigns |
| **Deliverability** | Technical fixes: domain auth, sending domain, list hygiene |
| **List Growth** | Form improvements, opt-in rate optimization |
| **Segmentation** | Segment creation and campaign targeting improvements |
| **Revenue Attribution** | Attribution setup, benchmark improvement |
| **Compliance** | Legal and technical compliance improvements |
| **Billing** | Plan optimization and profile hygiene |

---

## Worked Example Recommendations

### Example 1 — Launch Full SMS Program

**Recommendation ID:** REC-001
**Source Rule IDs:** SMS-001, SMS-011
**Issue:** SMS is not enabled in the Klaviyo account. No SMS flows, no SMS campaigns, and no SMS opt-in on signup forms.
**Why It Matters:** SMS is an incremental revenue channel that can add 10–20% to total email/SMS revenue for ecommerce brands with a mature email program. Every day without SMS is lost revenue.
**Expected Impact:** High
**Implementation Complexity:** Moderate (requires SMS program setup, TCPA compliance review, form update, and flow additions)
**Priority:** Critical
**Owner:** NP (with client compliance review)
**Timeline:** 30 days
**Data Confidence:** Confirmed
**Opportunity Note:** Accounts similar in size and category with active SMS programs generate meaningful additional revenue. Exact projections require traffic volume and consent rate modeling. A National Positions strategist should validate before forecasting.
**Recommended Next Step:** Schedule a 30-minute kickoff with the National Positions SMS team to review TCPA requirements, set up the Klaviyo SMS account, and add SMS opt-in to the primary signup form.

---

### Example 2 — Rebuild Abandoned Cart Flow

**Recommendation ID:** REC-002
**Source Rule IDs:** FLOW-004, FLOW-005, FLOW-006, FLOW-008, FTIM-001
**Issue:** The Abandoned Cart flow has only 1 email with no SMS, and the first email fires 4 hours after abandonment (target: < 60 minutes).
**Why It Matters:** The Abandoned Cart flow is typically the single highest-revenue automation for ecommerce brands. A 1-email, delayed, no-SMS structure is capturing a small fraction of available recovery revenue.
**Expected Impact:** High
**Implementation Complexity:** Moderate
**Priority:** Critical
**Owner:** NP
**Timeline:** 30 days
**Data Confidence:** Confirmed
**Opportunity Note:** Accounts with a properly structured 3-email + 2-SMS abandoned cart sequence typically recover a higher % of abandoned carts than single-email flows. Exact recovery improvement depends on cart volume, AOV, and current flow performance. A specialist should model this with your specific data.
**Recommended Next Step:** Rebuild the Abandoned Cart flow with 3 emails (60-min, 24-hr, 72-hr) and 2 SMS messages (60-min, 24-hr) for consented profiles. Include a discount offer in email 3.

---

### Example 3 — Resolve Deliverability Risk

**Recommendation ID:** REC-003
**Source Rule IDs:** DELV-001, DELV-007, DELV-008
**Issue:** Spam complaint rate is 0.11% (above Gmail's 0.10% threshold). No DMARC record is in place. Sending is on the Klaviyo default domain with no branded sending domain.
**Why It Matters:** Inbox placement is at active risk. If spam complaints are not reduced immediately, Gmail will begin filtering a significant portion of campaigns to the spam folder — dramatically reducing open rates and campaign revenue.
**Expected Impact:** High (deliverability; secondary revenue impact)
**Implementation Complexity:** Moderate (DMARC = Easy; sending domain = Moderate)
**Priority:** Critical
**Owner:** Shared (NP recommends, client IT/dev implements with NP guidance)
**Timeline:** Immediate
**Data Confidence:** Confirmed
**Opportunity Note:** Resolving deliverability risks doesn't generate new revenue directly — but it stops the ongoing loss of campaign revenue from inbox placement failures.
**Recommended Next Step:** (1) Switch all campaigns to Engaged 30-Day targeting immediately to reduce spam complaints. (2) Add DMARC record at p=none this week. (3) Begin branded sending domain setup within 30 days.

---

### Example 4 — Improve Signup Form Opt-In Rate

**Recommendation ID:** REC-004
**Source Rule IDs:** FORM-002, FORM-008, FORM-006
**Issue:** Signup form opt-in rate is 1.2% (below 2% threshold). Form has no incentive and collects email only.
**Why It Matters:** Every visitor who doesn't subscribe is a missed lifetime revenue opportunity. A 3× improvement in opt-in rate (from 1.2% to 3.6%) would triple monthly subscriber acquisition without changing traffic volume.
**Expected Impact:** High (compounds over time)
**Implementation Complexity:** Easy to Moderate
**Priority:** High
**Owner:** NP
**Timeline:** 30 days
**Data Confidence:** Confirmed
**Opportunity Note:** Improving opt-in rate increases the size of the audience for all future campaigns and flows. The compound revenue effect grows over 6–12 months as more subscribers move through the lifecycle.
**Recommended Next Step:** (1) Add a 10% off first order incentive to the popup. (2) Add an SMS opt-in field. (3) Set display timing to exit-intent rather than immediate. A/B test the new vs. old version.

---

### Example 5 — Create Engaged Segmentation Strategy

**Recommendation ID:** REC-005
**Source Rule IDs:** CAMP-004, LIST-002, DELV-014
**Issue:** All campaigns are sent to the full subscriber list (82,000 profiles) with no engagement filtering. Engaged 30-day audience is only 8,400 profiles (10% of list).
**Why It Matters:** Sending to 74,000 unengaged profiles generates spam complaints, unsubscribes, and deliverability damage — without generating meaningful revenue. These sends are actively harming the program.
**Expected Impact:** High (deliverability and campaign efficiency)
**Implementation Complexity:** Easy (segment creation) + Moderate (re-training campaign workflow)
**Priority:** High
**Owner:** NP
**Timeline:** 30 days
**Data Confidence:** Confirmed
**Opportunity Note:** Switching to engaged-only targeting will reduce campaign reach but significantly improve open rates, click rates, and per-send revenue. The deliverability improvement compounds to improve inbox placement over 60–90 days.
**Recommended Next Step:** Create an Engaged 90-Day segment immediately and use it as the default audience for all campaigns. Create an Engaged 30-Day segment for high-frequency sends. Stop sending to the full list.

---

## Missing Data Handling in Recommendations

When a recommendation cannot be confirmed due to missing data:

1. Flag it as "Inferred" in the Data Confidence field
2. Use language such as: "Based on the absence of [data point], we recommend verifying [action]"
3. Do not assign a specific revenue opportunity range — instead say "impact to be determined upon data availability"
4. Add a note: "This recommendation should be validated by the National Positions strategist during the account review"

---

## Human Review Gate for Recommendations

Before any recommendation reaches a client:

1. A National Positions Marketing Automation Strategist reviews all Critical and High recommendations
2. The strategist confirms that the recommendation is appropriate for this specific client context
3. Revenue opportunity language is reviewed and approved before inclusion
4. Any recommendation involving compliance, legal, or billing requires additional sign-off
5. The strategist may adjust priority, timeline, or complexity based on client-specific knowledge

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-05-10 | Initial recommendation engine — Phase 1 |
