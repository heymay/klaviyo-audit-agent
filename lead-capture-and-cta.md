# Klaviyo Audit Katie — Lead Capture and CTA Framework

**Version:** 1.0
**Owner:** National Positions
**Classification:** Internal Operating Framework — Phase 1
**Last Updated:** 2026-05-10

---

## Overview

Every Klaviyo audit produced by Katie is also a lead generation asset for National Positions. This document defines the lead capture strategy, CTA copy, lead scoring logic, sales handoff process, and follow-up sequence that convert audit completions into qualified sales consultations.

The audit creates value for the prospect. The CTA converts that value into a National Positions opportunity.

---

## Audit as a Lead Generation Tool

The Klaviyo audit serves two simultaneous purposes:
1. **Client value:** A genuine, data-driven diagnostic that helps any Klaviyo account improve
2. **NP lead gen:** A structured entry point that demonstrates NP's expertise and frames implementation as the obvious next step

The audit is not a pitch — it is a proof of competence. The CTA is positioned after a full, honest diagnostic, not before. This increases conversion because the prospect has already experienced NP's analytical depth.

---

## Audit Landing Page Positioning

**Headline Options:**
- "Find Out What Your Klaviyo Account Is Missing"
- "Get Your Free Klaviyo Account Audit — Score Out of 100"
- "Klaviyo Audit: See What's Working, What's Not, and What to Fix First"

**Subheadline:**
> Connect your Klaviyo account in minutes. Get a complete health score, prioritized findings, and a 90-day action plan — powered by National Positions' marketing automation team.

**Trust Signals (below the CTA button):**
- "Read-only access — we never make changes to your account"
- "No spam. Your audit report is sent directly to you."
- "Reviewed by a National Positions marketing automation specialist"
- National Positions logo + years in business
- Client logos or testimonials where available

**Page Sections:**
1. Headline + subheadline
2. What the audit covers (22 categories, score out of 100)
3. Sample report preview (redacted example)
4. How it works (3-step visual: Connect → Audit → Get Your Plan)
5. Lead capture form
6. FAQ (Is my data safe? How long does it take? What do you audit?)
7. National Positions about section

---

## Lead Capture Form

Collect the following fields in this order. Minimize friction — only required fields should block form submission.

### Required Fields

| Field | Type | Notes |
|---|---|---|
| First Name | Text | |
| Last Name | Text | |
| Business Email | Email | Validate format |
| Company / Brand Name | Text | |
| Website URL | URL | Validate format |
| Monthly Ecommerce Revenue Range | Dropdown | See options below |
| Ecommerce Platform | Dropdown | See options below |
| Klaviyo API Key | Text (masked) | Clearly labeled as read-only |
| Permission to Contact | Checkbox | Required to submit |

### Revenue Range Options
- Under $10,000/month
- $10,000–$50,000/month
- $50,000–$200,000/month
- $200,000–$1,000,000/month
- Over $1,000,000/month
- Prefer not to say

### Platform Options
- Shopify
- WooCommerce
- BigCommerce
- Magento / Adobe Commerce
- Salesforce Commerce Cloud
- Custom / Headless
- Other

### Recommended Additional Fields (not blocking)

| Field | Type |
|---|---|
| Biggest Email/SMS Challenge | Textarea (optional) |
| Audit Date Range | Dropdown (Last 30 days / 90 days / 6 months / 12 months) |
| How did you hear about us? | Dropdown (optional) |

---

## Consent Language

Required on the form, above the submit button:

> By submitting this form, you authorize National Positions to connect to your Klaviyo account using the read-only API key you provide, for the purpose of conducting a diagnostic audit. Your Klaviyo account data will be accessed in read-only mode — no changes will be made. National Positions will not share your credentials or data with third parties. You may revoke access at any time by deleting the API key in your Klaviyo account.
>
> By checking the box below, you also consent to National Positions contacting you about your audit results and related services.
>
> [ ] I agree to the above and consent to be contacted by National Positions.
>
> [Privacy Policy link] | [Terms of Service link]

---

## CTA Copy Options

### Primary CTA (in-report — Section 22)

> **Want help turning this audit into revenue?**
>
> National Positions can help you rebuild flows, improve deliverability, launch SMS, optimize forms, refine segmentation, and manage Klaviyo on an ongoing basis.
>
> **Schedule a consultation with our Marketing Automation team.**
>
> [SCHEDULE A CONSULTATION — CTA BUTTON]
> [CALENDLY LINK PLACEHOLDER]
>
> Or contact us at: [NP email] | nationalpositions.com

---

### CTA Variant 2 (High-Score Accounts — 75+)

> **Your Klaviyo foundation is strong. Let's make it exceptional.**
>
> Even well-performing accounts have optimization opportunities. National Positions can help you push your score higher, grow your SMS program, and expand your lifecycle coverage.
>
> [EXPLORE WHAT'S NEXT — CTA BUTTON]

---

### CTA Variant 3 (Critical Score Accounts — Below 40)

> **Your Klaviyo account needs immediate attention.**
>
> The gaps identified in this audit are likely costing you meaningful revenue every month. National Positions can help you fix the most critical issues first and build toward a high-performing email and SMS program.
>
> **Let's talk about what to do first.**
>
> [GET URGENT HELP — CTA BUTTON]

---

## Lead Scoring Criteria

When a completed audit is received, assign a lead score to prioritize sales follow-up.

| Factor | Points |
|---|---|
| **Audit Score 0–39 (Critical)** | +20 |
| **Audit Score 40–59 (Weak)** | +15 |
| **Audit Score 60–74 (Average)** | +10 |
| **Revenue > $200k/month** | +20 |
| **Revenue $50k–$200k/month** | +10 |
| **Revenue $10k–$50k/month** | +5 |
| **No SMS enabled** | +10 |
| **Missing Abandoned Cart flow** | +10 |
| **Shopify platform** | +5 |
| **Completed "Biggest Challenge" field** | +5 |
| **Clicked CTA button in report** | +15 |
| **Scheduled Calendly call** | +30 |

**Lead Tiers:**

| Score | Tier | Routing |
|---|---|---|
| 50+ | Hot | Immediate sales team notification; call within 2 hours |
| 30–49 | Warm | Follow-up email within 4 hours; sales call within 24 hours |
| 15–29 | Nurture | Enter automated follow-up email sequence |
| < 15 | Low | Enter general NP marketing list |

---

## Sales Handoff Process

1. Audit completes → Lead record created in CRM (HubSpot or equivalent) with:
   - Contact information from form
   - Klaviyo Health Score
   - Score band
   - Top 3 critical findings (from audit output)
   - Revenue range
   - Platform
   - Lead score

2. Lead score calculated automatically → tier assigned → routed to appropriate NP account manager

3. Account manager receives notification with audit summary and lead score

4. Account manager reviews the audit report before contacting the prospect (must understand their specific findings)

5. Account manager sends personalized outreach within the tier SLA:
   - Reference specific findings from the audit ("We noticed your spam complaint rate is above Google's threshold...")
   - Offer a 30-minute implementation review call
   - Share 1–2 examples of similar client improvements

---

## Follow-Up Email Sequence (Post-Audit)

### Email 1 — Immediate (sent within 5 minutes of audit completion)

**Subject:** Your Klaviyo Audit Results — [Score]/100 — [Brand Name]
**From:** [NP Account Manager Name] at National Positions

> Hi [First Name],
>
> Your Klaviyo audit is complete. Your account scored [X]/100 — [Score Band].
>
> The top 3 things we found:
> 1. [Critical/High finding #1 in plain English]
> 2. [Critical/High finding #2]
> 3. [Critical/High finding #3]
>
> Your full report is attached / available at [link].
>
> If you'd like to walk through the findings with our team and talk through what to fix first, you can schedule a call here: [Calendly link]
>
> Best,
> [Account Manager Name]
> National Positions

---

### Email 2 — Day 2

**Subject:** Quick question about your Klaviyo audit
**From:** [NP Account Manager Name]

> Hi [First Name],
>
> I reviewed your audit results and wanted to reach out personally.
>
> [Personalized observation — e.g., "The fact that your abandoned cart flow has only 1 email is one of the highest-leverage things you can fix. Accounts of similar size that rebuild this flow typically see a meaningful lift in recovery revenue."]
>
> I'd love to spend 20 minutes walking through what we'd prioritize first. No pitch — just a practical conversation about your specific setup.
>
> [Schedule here: Calendly link]
>
> [Account Manager Name]

---

### Email 3 — Day 5

**Subject:** One thing that could move the needle for [Brand Name]
**From:** [NP Account Manager Name]

> Hi [First Name],
>
> Based on your audit, the single highest-impact thing you can do is [top recommendation in plain language].
>
> If you'd like help implementing that — or any of the other recommendations in your report — our team specializes in exactly this.
>
> We've helped ecommerce brands like [reference client type] improve their Klaviyo performance significantly. Happy to share examples on a quick call.
>
> [Schedule here: Calendly link]
>
> If now isn't the right time, no worries — your report will still be there when you're ready.
>
> [Account Manager Name]

---

## Consultation Offer

The NP consultation is positioned as:

**What it is:** A 30-minute strategy session to review the audit findings, answer questions, and outline a tailored implementation plan.

**What it is not:** A sales pitch for a fixed package. The consultation is audit-specific and actionable.

**Consultation framing:**
> "We'll walk through your audit together, answer any questions about the findings, and show you exactly what we'd prioritize — and what we'd do first — if we were managing your Klaviyo account."

---

## Disclaimer Language

Required on all audit-related materials:

> This audit is diagnostic and informational only. All findings are based on data available at the time of the audit. Revenue opportunity estimates are directional ranges only and are not guarantees of results. National Positions does not make changes to your Klaviyo account without your explicit authorization. This audit does not constitute legal, compliance, or financial advice.

---

## Calendly Integration Placeholder

In Phase 5+ (web app), replace [CALENDLY LINK PLACEHOLDER] with:

- NP Marketing Automation team booking page
- 30-minute "Klaviyo Audit Review" appointment type
- Include: audit score, top 3 findings, and contact name in the booking confirmation email to the NP team

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-05-10 | Initial lead capture and CTA framework — Phase 1 |
