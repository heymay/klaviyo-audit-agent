# Klaviyo Audit Katie — Project Overview

**Version:** 1.0
**Owner:** National Positions
**Classification:** Internal Operating Framework — Phase 1
**Last Updated:** 2026-05-10

---

## What Is Klaviyo Audit Katie?

Klaviyo Audit Katie is National Positions' AI-powered Klaviyo audit and diagnostic agent. Katie connects to a client's Klaviyo account using read-only API credentials, analyzes the health and performance of their email and SMS marketing setup, identifies what is working and what is missing, assigns a score out of 100, and generates a prioritized action plan.

Katie is built for ecommerce brands. She audits the areas that matter most to retention revenue: flows, campaigns, SMS adoption, deliverability, list health, segmentation, signup forms, benchmarks, billing efficiency, compliance, and lifecycle coverage.

Every completed audit ends with a National Positions CTA, positioning the agency to implement the recommendations as a paid engagement.

---

## Who Is This For?

| Audience | How They Use It |
|---|---|
| **Ecommerce brands** | Understand the health of their Klaviyo account and what to fix first |
| **National Positions team** | Accelerate internal audits, enforce methodology, create consistent deliverables |
| **Prospective NP clients** | Receive a free or paid diagnostic as a lead generation entry point |
| **NP account managers** | Use audit output as a sales conversation starter and scope-of-work foundation |

---

## How National Positions Will Use It

1. **Internal audit acceleration** — Katie does the heavy lifting of data collection, analysis, and scoring. A senior strategist reviews and approves the output before it reaches a client.
2. **New business lead generation** — Prospective clients connect their Klaviyo account, receive a scored audit, and see a clear CTA to engage National Positions for implementation.
3. **Existing client QBRs** — Quarterly audits show progress, surface new opportunities, and reinforce NP's value.
4. **Onboarding baseline** — New NP clients receive a baseline audit in week one to establish starting health and prioritize early wins.

---

## Phase 1 Scope

**Phase 1 is documentation and methodology only.**

Phase 1 delivers:
- Complete audit methodology (skill.md)
- Agent definition and persona (agent.md)
- Input requirements (input-checklist.md)
- Klaviyo API connection plan (klaviyo-connection-plan.md)
- Data map for all Klaviyo objects (klaviyo-data-map.md)
- All 22 audit categories defined (audit-categories.md)
- Complete metrics glossary (metrics-glossary.md)
- Weighted scoring rubric (scoring-rubric.md)
- 125+ decision rules (decision-rules.md)
- Full output template (output-template.md)
- Recommendation engine framework (recommendation-engine.md)
- Lead capture and CTA framework (lead-capture-and-cta.md)
- Security and privacy requirements (security-and-privacy.md)
- Human review workflow (human-review-workflow.md)
- Phased product roadmap (roadmap.md)

**Phase 1 does NOT include:**
- Live API connections
- Working code
- Database schemas
- Deployed applications
- Billing or payment logic
- Multi-user permissions
- Any write-back to Klaviyo

---

## Future Phases

| Phase | Description |
|---|---|
| **Phase 2** | Local MVP with manual Klaviyo exports and mock data |
| **Phase 3** | Read-only Klaviyo API connection and data pull layer |
| **Phase 4** | Scoring engine and recommendation engine (code) |
| **Phase 5** | Web-based audit report (Next.js frontend) |
| **Phase 6** | PDF / Google Doc / Google Slides export |
| **Phase 7** | Lead capture form and CRM handoff |
| **Phase 8** | Benchmark refinement and opportunity modeling |
| **Phase 9** | Shopify, GA4, AdBeacon, Meta Ads, Google Ads enrichments |
| **Phase 10** | Human-approved implementation workflows |

---

## High-Level Audit Workflow

```
Step 1 — Business Context
  User enters: website URL, business name, ecommerce platform, revenue range,
  audit date range, and any optional context (AOV, goals, challenges)

Step 2 — Klaviyo Connection
  User provides a read-only Klaviyo private API key (MVP) or connects via OAuth (production)
  System confirms credentials are read-only before proceeding

Step 3 — API Validation
  System tests the connection by calling GET /api/accounts/
  System confirms accessible data objects and logs any unavailable endpoints

Step 4 — Data Pull
  System pulls: account info, campaigns, campaign messages, flows, flow messages,
  lists, segments, profiles (aggregate), forms, metrics, events, templates,
  benchmarks (if available), and billing/plan data (if available)

Step 5 — Data Normalization
  System maps raw API responses to the Klaviyo data model defined in klaviyo-data-map.md
  System flags any missing or incomplete data fields

Step 6 — Audit Execution
  System evaluates all 22 audit categories against the decision rules in decision-rules.md
  System assigns findings, severity levels, and score impacts per category

Step 7 — Composite Score Generation
  System calculates the Klaviyo Health Score (0–100) using the weighted rubric
  in scoring-rubric.md

Step 8 — Findings and Recommendations
  System generates prioritized findings with severity, business impact, and
  recommended actions using the recommendation engine framework

Step 9 — Prioritized Action Plan
  System assembles a 30/60/90-day action plan with owners, effort, and estimated impact

Step 10 — National Positions CTA
  Every completed report ends with a call to action for a National Positions
  consultation, framed around the client's specific audit findings
```

---

## Audit Categories (22 Total)

1. Executive Overview
2. SMS Adoption
3. Campaign Consistency
4. Campaign Frequency
5. Campaign Segmentation
6. Deliverability Health
7. Benchmark Performance
8. Core Flow Coverage
9. Flow Structure and Timing
10. Flow Revenue Contribution
11. SMS in Flows
12. Signup Forms
13. Form Opt-In Rate
14. List Health
15. Engagement Segmentation
16. Revenue Attribution
17. Billing Efficiency
18. Compliance and Consent
19. Template and Creative Quality
20. Lifecycle Coverage
21. Missed Revenue Opportunities
22. 30/60/90 Day Plan

---

## Scoring Summary

| Score Range | Band | Meaning |
|---|---|---|
| 90–100 | Elite | Best-in-class Klaviyo setup |
| 75–89 | Strong | Strong foundation, targeted improvements available |
| 60–74 | Average | Solid base with meaningful gaps to close |
| 40–59 | Weak | Significant issues limiting retention revenue |
| 0–39 | Critical | Fundamental problems requiring immediate attention |

---

## Important Rules

- Katie is **read-only**. She never makes changes to Klaviyo.
- Katie does not send campaigns, edit flows, suppress contacts, or modify billing.
- Katie does not guarantee revenue outcomes — all projections are directional estimates.
- Every audit requires human review by a National Positions strategist before client delivery.
- API credentials are never logged, never stored client-side, and never exposed in any output.

---

## File Index

| File | Purpose |
|---|---|
| `README.md` | This file — project overview |
| `agent.md` | Agent definition, persona, responsibilities, rules |
| `skill.md` | Complete step-by-step audit methodology |
| `input-checklist.md` | All required, recommended, and optional inputs |
| `klaviyo-connection-plan.md` | API connection architecture and security |
| `klaviyo-data-map.md` | Data objects, fields, and audit mappings |
| `audit-categories.md` | All 22 audit categories defined |
| `metrics-glossary.md` | Definitions and interpretation for all metrics |
| `scoring-rubric.md` | Weighted scoring framework (0–100) |
| `decision-rules.md` | 125+ IF/THEN audit logic rules |
| `output-template.md` | Complete report structure (22 sections) |
| `recommendation-engine.md` | Recommendation generation and prioritization framework |
| `lead-capture-and-cta.md` | NP CTA, lead capture, and sales handoff |
| `security-and-privacy.md` | Credential handling and data privacy requirements |
| `human-review-workflow.md` | 7-stage review and approval process |
| `roadmap.md` | 10-phase product development roadmap |
