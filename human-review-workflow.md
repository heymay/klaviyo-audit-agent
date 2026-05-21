# Klaviyo Audit Katie — Human Review Workflow

**Version:** 1.0
**Owner:** National Positions
**Classification:** Internal Operating Framework — Phase 1
**Last Updated:** 2026-05-10

---

## Overview

No Klaviyo audit report reaches a client without passing through a multi-stage human review process. This workflow defines the 7 review stages, what each reviewer checks, the approval and rejection criteria, and the final sign-off requirements.

**The human review is not optional.** It is a core quality and compliance control. Katie produces the draft — National Positions professionals verify, contextualize, and approve the output before any client receives it.

---

## Review Workflow Summary

| Stage | Reviewer | Purpose | Gate Type |
|---|---|---|---|
| 1 | NP Analyst | Data completeness and API validation | Blocking |
| 2 | NP Technical Lead | Data pull verification | Blocking |
| 3 | Marketing Automation Strategist | Finding accuracy and strategic review | Blocking |
| 4 | Deliverability Specialist | Deliverability findings review | Blocking (if deliverability is Critical or High) |
| 5 | Compliance Review | Legal/compliance risk check | Conditional (required if compliance flags exist) |
| 6 | Account Manager / Sales | CTA and opportunity framing review | Blocking |
| 7 | Account Team Lead | Final sign-off | Blocking |

"Blocking" means the audit cannot proceed to the next stage without approval. Conditional stages are required only when specific trigger conditions exist.

---

## Stage 1 — Data Completeness Review

**Reviewer:** NP Analyst (junior to mid-level)
**When:** Immediately after the audit intake form is submitted and before the API connection is initiated

### What to Check

- [ ] All required inputs are present: business name, website URL, API key, consent, date range
- [ ] API key format appears valid
- [ ] User consent checkbox is checked and timestamped
- [ ] Audit date range is specified and reasonable (not future dates, not more than 24 months)
- [ ] Business name matches the website domain (basic sanity check)
- [ ] No obviously problematic inputs (e.g., disposable email address, fake company name)

### Approval Criteria

All required fields present, consent confirmed, API key format valid.

### Rejection Criteria

Any required field missing, consent not confirmed, date range invalid, API key format appears wrong.

### If Rejected

Return the intake form to the submitter with specific instructions on what is missing. Do not attempt to validate the API key or pull any data until the intake is complete.

---

## Stage 2 — API Connection and Data Pull Validation

**Reviewer:** NP Technical Lead or Senior Analyst
**When:** Immediately after the data pull completes and before the audit engine runs

### What to Check

- [ ] API connection authenticated successfully (no 401 or 403 errors)
- [ ] Account identity confirmed — the Klaviyo account name matches the expected client
- [ ] Data pull log reviewed — which endpoints returned data vs. which returned errors
- [ ] Critical endpoints returned data: campaigns, flows, forms, lists, profiles
- [ ] Pagination completed — all records were retrieved (no truncation)
- [ ] Total record counts are plausible (e.g., 47 campaigns in 12 months for an active account is reasonable; 0 campaigns is a red flag worth confirming)
- [ ] Any inaccessible endpoints are documented and flagged for the audit
- [ ] No write-access errors were triggered (confirms read-only)
- [ ] API key or OAuth token is not present in any log output

### Approval Criteria

Successful connection, account identity confirmed, minimum required data present, no credential exposure in logs.

### Rejection Criteria

Authentication failure, wrong account connected, critical endpoints inaccessible (campaigns, flows, profiles all missing), credential exposure in log.

### If Rejected

Halt the audit. Notify the NP account manager and the client. Depending on the issue:
- Invalid key: request a new API key
- Wrong account: confirm correct account and reconnect
- Credential exposure: escalate to NP security team immediately

---

## Stage 3 — Marketing Automation Strategist Review

**Reviewer:** Senior Marketing Automation Strategist
**When:** After the audit engine has produced a draft report (all scores and findings generated)

### What to Check

**Score Validation:**
- [ ] All 10 category scores are present and fall within the 1–10 range
- [ ] Composite score is calculated correctly (verify math on 2–3 categories manually)
- [ ] Score band is correctly assigned
- [ ] Penalty rules are applied correctly where relevant (e.g., missing flows capped appropriately)
- [ ] Bonus points are applied correctly where relevant

**Finding Accuracy:**
- [ ] All Critical and High findings are supported by specific data (not generic)
- [ ] Severity assignments are appropriate (not over-inflated or under-inflated)
- [ ] Findings do not contradict each other
- [ ] Flow findings accurately reflect what's in the account (name matching is correct)
- [ ] SMS findings are accurate (SMS status correctly identified as enabled/disabled)
- [ ] Deliverability findings are plausible relative to the data

**Client Context:**
- [ ] Has NP worked with this client before? If so, are any prior context notes incorporated?
- [ ] Are there any known circumstances that explain unusual data? (e.g., "they just relaunched their store last month — the low campaign count is expected")
- [ ] Are any findings potentially offensive, inaccurate, or embarrassing if read by the client?

**Recommendations:**
- [ ] Top 5 Issues match the highest-severity findings
- [ ] Top 5 Revenue Opportunities are the highest-impact, most relevant gaps
- [ ] 30/60/90 plan is realistic and correctly sequenced (dependencies respected)
- [ ] No "Critical" item is placed in the 90-day plan without explanation

**Revenue Opportunity Language:**
- [ ] All opportunity estimates use ranges, not specific dollar amounts
- [ ] Required disclaimers are present
- [ ] No overpromising language ("will recover," "guaranteed to," etc.)

### Approval Criteria

Scores mathematically correct, findings supported by data, severity appropriate, no overpromising, client context incorporated, 30/60/90 plan is logical.

### Rejection Criteria

Math errors in composite score, Critical findings missing for obvious issues (e.g., no abandoned cart flow flagged correctly), fabricated or unsupported findings, overpromising language in opportunity section.

### If Rejected

Return to Katie with specific revision notes. Strategist annotates the draft with specific changes needed. Katie revises and returns to Stage 3.

---

## Stage 4 — Deliverability Review

**Reviewer:** Deliverability Specialist (or Senior Strategist with deliverability expertise)
**When:** Concurrent with or immediately after Stage 3, triggered automatically if any deliverability finding is Critical or High severity

**Trigger Conditions for Stage 4:**
- Spam complaint rate > 0.08%
- Hard bounce rate > 0.5%
- Missing DKIM or SPF
- Open rate trend declining > 20%
- Any DELV rule with Critical or High severity triggered

### What to Check

- [ ] Spam complaint rate interpretation is correct (does the rate calculation look right?)
- [ ] Bounce rate interpretation is correct (hard vs. soft correctly distinguished)
- [ ] DKIM/SPF/DMARC status is accurately reported (may require manual DNS check to confirm)
- [ ] Deliverability health level (Critical / Needs Improvement / Acceptable / Strong) is correctly assigned
- [ ] Recommended remediation steps are technically accurate
- [ ] No conflicting deliverability recommendations (e.g., "increase send frequency" and "reduce send frequency" should never appear together)
- [ ] If deliverability is Critical: confirm the recommendation includes stopping broad list sends immediately

### Approval Criteria

Deliverability metrics interpreted correctly, health level accurate, remediation steps are technically sound.

### Rejection Criteria

Incorrect health level assignment, technically inaccurate remediation steps, missing recommendation for Critical deliverability status.

### If Not Triggered

This stage is skipped if no deliverability finding exceeds Medium severity. Note this in the review log.

---

## Stage 5 — Compliance Review

**Reviewer:** NP Compliance Lead or external legal counsel
**When:** Triggered when specific compliance flags exist in the audit

**Trigger Conditions for Stage 5:**
- Any COMP rule with Critical or High severity triggered
- SMS consent compliance risk flagged (COMP-001)
- GDPR risk flagged (COMP-002)
- Purchased list suspected (LIST-009)
- Unsubscribe link compliance concern flagged

### What to Check

- [ ] All compliance findings are accurately labeled as "risk flags for further review" (not definitive legal judgments)
- [ ] Required disclaimer is present: "This review identifies potential risks. It does not constitute legal advice."
- [ ] No finding makes a definitive legal compliance determination
- [ ] SMS consent findings are appropriately cautious (not asserting TCPA violation — only flagging risk)
- [ ] GDPR findings are appropriately scoped to relevant EU audiences
- [ ] Client is not being advised to take an action that could itself create legal risk (e.g., suppressing contacts in a way that destroys consent records)

### Approval Criteria

All compliance language is appropriately hedged, legal advice disclaimer is present, no definitive legal determinations made.

### Rejection Criteria

Report asserts a legal violation (not NP's role), missing legal disclaimer, compliance finding gives specific legal advice beyond NP's scope.

### If Not Triggered

Stage 5 is skipped if no compliance rules above Medium severity were triggered. Note in review log.

---

## Stage 6 — Sales and Account Team Review

**Reviewer:** NP Account Manager or Sales Lead
**When:** After Stages 3–5 are complete

### What to Check

**CTA Review:**
- [ ] CTA copy is appropriate for the client's score and top findings (Critical vs. Strong accounts get different CTA variants)
- [ ] Calendly or scheduling link is correct and functional
- [ ] Contact email and/or phone number in CTA is the correct NP team member
- [ ] CTA does not make implementation promises that NP cannot deliver

**Opportunity Framing:**
- [ ] The Estimated Opportunity Summary is reasonable relative to the client's account size
- [ ] Revenue language is directional and includes required disclaimers
- [ ] The framing positions NP as the obvious implementation partner without being heavy-handed

**Lead Scoring:**
- [ ] Lead score has been calculated and assigned
- [ ] Lead tier routing is correct (Hot → immediate follow-up, etc.)
- [ ] CRM record has been created with the correct fields

**Tone Check:**
- [ ] The report is confident and honest — not alarmist or overly critical
- [ ] Positive findings are acknowledged (Section 5 — Top 5 Wins)
- [ ] The overall tone would make the client want to work with NP, not feel attacked

### Approval Criteria

CTA is appropriate, opportunity language is non-committal and disclaimered, lead score assigned, tone is professional.

### Rejection Criteria

Wrong CTA variant for score band, CTA link broken, opportunity language makes specific revenue promises, tone is off.

### If Rejected

Account manager annotates the specific CTA or tone issues. Return to Stage 3 reviewer for revision.

---

## Stage 7 — Final Report Sign-Off

**Reviewer:** Account Team Lead or NP Director
**When:** After all prior stages have approved

### What to Check

- [ ] All previous review stages are marked approved (no open rejection notes)
- [ ] Document header is complete: client name, website, Klaviyo account, audit period, date generated, approved by
- [ ] "Approved By" field is populated with the Strategist's name from Stage 3
- [ ] Report is formatted correctly and all 22 sections are present
- [ ] No placeholder text remains in the report (e.g., "[CALENDLY LINK PLACEHOLDER]" must be replaced)
- [ ] Confidentiality notice is present in the document header
- [ ] The report is appropriate to send to the client contact named in the header

### Final Sign-Off Checklist

- [ ] Stage 1 approved ✓
- [ ] Stage 2 approved ✓
- [ ] Stage 3 approved ✓
- [ ] Stage 4 approved ✓ (or not triggered)
- [ ] Stage 5 approved ✓ (or not triggered)
- [ ] Stage 6 approved ✓
- [ ] All 22 report sections present ✓
- [ ] No placeholder text remaining ✓
- [ ] NP CTA is correct and functional ✓
- [ ] Approved by [NP Account Team Lead Name] on [Date] ✓

### Delivery

Once Stage 7 is signed off:
- Report is delivered to the client contact via the agreed method (email, secure link, in-person, or through the web app)
- Lead follow-up sequence is triggered (see lead-capture-and-cta.md)
- Report is filed in the client record in the NP CRM/project management system

---

## Review Timeline Standards

| Stage | Maximum Turnaround |
|---|---|
| Stage 1 — Data Completeness | Within 2 hours of intake submission |
| Stage 2 — API / Data Pull Validation | Within 2 hours of data pull completion |
| Stage 3 — Strategist Review | Within 24 hours of draft generation |
| Stage 4 — Deliverability Review | Within 24 hours (concurrent with Stage 3) |
| Stage 5 — Compliance Review | Within 48 hours (if triggered) |
| Stage 6 — Sales Review | Within 4 hours of Stages 3–5 approval |
| Stage 7 — Final Sign-Off | Within 2 hours of Stage 6 approval |

**Total target turnaround:** 24–72 hours from intake to client delivery (without compliance escalation)

---

## Revision Note Format

When returning a draft for revision, reviewers must use this format to annotate issues:

```
REVISION NOTE
Stage: [Stage Number and Name]
Reviewer: [Name]
Date: [YYYY-MM-DD]
Section: [Report Section or Category]
Issue: [Specific description of what is wrong]
Required Change: [What the revision must include]
Priority: [Must Fix Before Delivery / Should Fix / Minor]
```

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-05-10 | Initial human review workflow — Phase 1 |
