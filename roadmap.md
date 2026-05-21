# Klaviyo Audit Katie — Product Roadmap

**Version:** 1.0
**Owner:** National Positions
**Classification:** Internal Operating Framework — Phase 1
**Last Updated:** 2026-05-10

---

## Overview

This roadmap defines the 10-phase build plan for Klaviyo Audit Katie, from methodology documentation through full marketing automation optimization capabilities. Each phase builds on the previous one and has a defined scope, deliverables, and success criteria.

**Current Phase:** Phase 1 — Methodology & Documentation

---

## Phase 1 — Methodology and Documentation

**Status:** In Progress (Current Phase)
**Objective:** Define the complete audit methodology, scoring framework, decision logic, and output structure before writing any code.

**Deliverables:**
- README.md — project overview
- agent.md — agent definition and persona
- skill.md — step-by-step audit methodology
- input-checklist.md — all required inputs
- klaviyo-connection-plan.md — API connection architecture
- klaviyo-data-map.md — data objects and field mapping
- audit-categories.md — all 22 audit categories
- metrics-glossary.md — all metrics defined
- scoring-rubric.md — weighted scoring framework
- decision-rules.md — 125+ IF/THEN rules
- output-template.md — complete report structure
- recommendation-engine.md — recommendation logic
- lead-capture-and-cta.md — NP CTA and lead capture
- security-and-privacy.md — credential and data handling
- human-review-workflow.md — 7-stage review process
- roadmap.md — this file

**Dependencies:** None
**Estimated Effort:** 1–2 weeks (documentation sprint)
**Success Criteria:** All 16 documentation files complete, reviewed by NP team lead, and ready to serve as the implementation blueprint for Phase 2.

---

## Phase 2 — Local MVP with Manual Data and Mock Accounts

**Status:** Planned
**Objective:** Build a working local version of the audit engine that can process manually exported Klaviyo data and mock account data to validate the methodology before live API integration.

**Deliverables:**
- Python or Node.js script that accepts JSON/CSV Klaviyo exports
- Scoring engine implementation (based on scoring-rubric.md)
- Decision rules engine (IF/THEN logic from decision-rules.md)
- Recommendation generator (based on recommendation-engine.md)
- Plain-text or Markdown report output
- Mock Klaviyo account data set (3–5 accounts at varying health levels)
- Test results showing correct scoring across all 10 categories

**Dependencies:** Phase 1 complete
**Estimated Effort:** 2–4 weeks
**Success Criteria:** System correctly scores 3 mock accounts. Output matches expected score ranges. All 125+ decision rules fire correctly on appropriate data conditions. A National Positions strategist can read the output and recognize it as audit-quality.

---

## Phase 3 — Read-Only Klaviyo API Connection

**Status:** Planned
**Objective:** Replace manual data exports with a live, read-only Klaviyo API connection. The system pulls real account data automatically.

**Deliverables:**
- Klaviyo API client (Python or Node.js)
- Secure API key ingestion (environment variable, no frontend exposure)
- Data pull for all objects: accounts, campaigns, flows, forms, lists, segments, profiles (aggregates), metrics, events, templates
- Pagination handling for large accounts
- Rate limit handling with exponential backoff
- Error handling (401, 403, 429, 5xx)
- Data normalization layer (raw API → internal data model)
- Connection validation (confirms read-only access before proceeding)
- Disconnect / credential revocation flow

**Dependencies:** Phase 2 complete, Klaviyo API documentation verified
**Estimated Effort:** 3–5 weeks
**Success Criteria:** System successfully connects to 3+ real Klaviyo accounts, pulls all required data objects, normalizes data correctly, and produces audit output consistent with Phase 2 mock results. API key never appears in any log or output.

**Important Note:** All API endpoints and permissions must be verified against the current Klaviyo API documentation before implementation begins. Endpoint availability and response formats may differ from what is documented in klaviyo-connection-plan.md.

---

## Phase 4 — Scoring Engine and Recommendation Engine

**Status:** Planned
**Objective:** Productionize the scoring and recommendation logic from Phase 2 into a reliable, testable engine that handles edge cases, missing data, and varying account configurations.

**Deliverables:**
- Scoring engine with all 10 weighted categories
- Per-category 1–10 scoring with band criteria
- Composite 0–100 score calculation
- Penalty logic (missing flows, no SMS, low deliverability)
- Bonus logic (strong opt-in rates, excellent benchmarks)
- Missing data handling (graceful degradation with confidence flags)
- Recommendation engine with prioritization algorithm
- Opportunity range estimation with disclaimer injection
- Severity assignment (Critical / High / Medium / Low) for each finding
- Unit tests for all scoring and rule logic

**Dependencies:** Phase 3 complete
**Estimated Effort:** 3–4 weeks
**Success Criteria:** Scoring engine passes all unit tests. Recommendations are correctly prioritized by revenue impact × effort. Missing data does not cause crashes — it triggers "data unavailable" flags. Output is reviewed and validated by a National Positions strategist on 5 real accounts.

---

## Phase 5 — Web-Based Audit Report

**Status:** Planned
**Objective:** Build a web interface where users can connect their Klaviyo account, run the audit, and view a formatted interactive report.

**Deliverables:**
- Next.js frontend (or equivalent)
- Supabase or equivalent backend / database
- User-facing input form (business context, date range)
- Secure API key entry (masked input, server-side handling only)
- Audit progress indicator
- Interactive report UI with all 22 sections
- Score visualization (gauge chart or equivalent)
- Category score breakdown (table + visual)
- 30/60/90 action plan display
- National Positions CTA section (styled, prominent)
- Mobile-responsive layout

**Dependencies:** Phase 4 complete
**Estimated Effort:** 4–6 weeks
**Success Criteria:** A prospective client can visit the web app, connect Klaviyo, run an audit, and view a complete scored report — all without NP team involvement. Report includes every section from output-template.md. NP CTA is visible and functional. Mobile experience is fully usable.

---

## Phase 6 — PDF, Google Doc, and Google Slides Export

**Status:** Planned
**Objective:** Allow audit reports to be exported as professional documents suitable for client delivery and QBR presentations.

**Deliverables:**
- PDF export with NP branding
- Google Doc export (structured, section-based)
- Google Slides export (executive presentation format — 10–15 slides)
- Export templates matching NP brand standards
- One-click export from web report

**Dependencies:** Phase 5 complete
**Estimated Effort:** 2–3 weeks
**Success Criteria:** All three export formats produce client-ready documents. PDFs are printable. Slides are presentable without editing. Exports include all 22 report sections. NP logo and branding are present.

---

## Phase 7 — Lead Capture Form and CRM Handoff

**Status:** Planned
**Objective:** Build the lead generation layer — capturing prospect information during or after the audit and routing qualified leads to the NP sales team.

**Deliverables:**
- Lead capture form (name, email, company, website, revenue range, platform, challenge, consent)
- Lead scoring logic (audit score + issues found + revenue range)
- CRM integration (HubSpot or equivalent)
- Automated lead routing to appropriate NP account manager
- Follow-up email sequence (3 emails, based on lead-capture-and-cta.md)
- Calendly embed or scheduling link in CTA
- Lead source tracking (which audit, which date, which score)

**Dependencies:** Phase 5 complete
**Estimated Effort:** 2–3 weeks
**Success Criteria:** Every completed audit captures lead data. Qualified leads (score < 75, revenue > $50k/month) auto-route to NP sales. CRM shows audit score and top findings in the lead record. NP team can respond within 24 hours of audit completion.

---

## Phase 8 — Benchmark Refinement and Opportunity Modeling

**Status:** Planned
**Objective:** Replace generic benchmarks with NP-proprietary benchmarks built from aggregated (anonymized) client data. Improve opportunity range estimation with real-world recovery rates.

**Deliverables:**
- NP benchmark database (by vertical, platform, revenue tier)
- Dynamic benchmark comparison in reports
- Opportunity modeling framework (recovery rate assumptions by flow type, industry)
- Confidence-weighted opportunity ranges
- "Similar accounts" comparison where data supports it

**Dependencies:** Phase 7 complete, sufficient audit volume for benchmark aggregation
**Estimated Effort:** 4–6 weeks
**Success Criteria:** Reports include NP vertical benchmarks for at least 5 ecommerce categories. Opportunity estimates are backed by real recovery data from NP client history. Benchmark comparisons are flagged as "NP internal data" vs. "industry standard."

---

## Phase 9 — Platform and Channel Enrichments

**Status:** Planned
**Objective:** Enrich Klaviyo audit data with signals from connected platforms — Shopify, GA4, AdBeacon, Meta Ads, Google Ads — to produce a full omnichannel retention picture.

**Deliverables:**
- Shopify integration (order data, customer segments, product performance)
- GA4 integration (landing page conversion, email-driven traffic)
- AdBeacon integration (blended ROAS, email-attributed revenue)
- Meta Ads integration (audience overlap, retargeting gaps)
- Google Ads integration (lifecycle signal correlation)
- Cross-channel revenue attribution view
- "Email-First vs. Paid-First" customer segment analysis

**Dependencies:** Phase 8 complete, client consent for additional platform connections
**Estimated Effort:** 6–10 weeks (per integration)
**Success Criteria:** At least Shopify and GA4 integrations are live and producing enriched audit data. Cross-channel revenue view is visible in the report. No additional platforms are added until Shopify + GA4 are stable.

---

## Phase 10 — Human-Approved Implementation Workflows

**Status:** Future Vision
**Objective:** Allow the NP team to implement audit recommendations directly inside Klaviyo — with every action gated behind human review and explicit client authorization.

**Deliverables:**
- Implementation workflow UI (NP team-facing, not client-facing)
- Per-recommendation approval flow (NP strategist approves each change before execution)
- Flow creation templates (welcome, abandoned cart, etc.)
- Campaign creation templates
- Form optimization suggestions with A/B test setup
- Segment creation automation
- Change log for every modification made
- Client authorization requirement before any write action

**Dependencies:** Phase 9 complete, Klaviyo write-permission OAuth scope, legal review of write-back workflow
**Estimated Effort:** 8–12 weeks
**Success Criteria:** NP team can approve and execute audit recommendations from within the platform. Every change is logged with NP practitioner name, date, and client authorization record. No change is ever made without explicit human approval.

**Important Constraint:** Phase 10 introduces write-access to Klaviyo. This phase requires a full legal, security, and compliance review before development begins. Write-access is never given to an automated agent without human approval on every individual action.

---

## Roadmap Summary

| Phase | Name | Status | Effort |
|---|---|---|---|
| 1 | Methodology & Documentation | In Progress | 1–2 weeks |
| 2 | Local MVP with Mock Data | Planned | 2–4 weeks |
| 3 | Read-Only Klaviyo API | Planned | 3–5 weeks |
| 4 | Scoring & Recommendation Engine | Planned | 3–4 weeks |
| 5 | Web-Based Audit Report | Planned | 4–6 weeks |
| 6 | PDF / Doc / Slides Export | Planned | 2–3 weeks |
| 7 | Lead Capture & CRM Handoff | Planned | 2–3 weeks |
| 8 | Benchmark Refinement | Planned | 4–6 weeks |
| 9 | Platform & Channel Enrichments | Planned | 6–10 weeks |
| 10 | Human-Approved Implementation | Future Vision | 8–12 weeks |

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-05-10 | Initial roadmap — Phase 1 |
