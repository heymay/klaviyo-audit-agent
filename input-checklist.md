# Klaviyo Audit Katie — Input Checklist

**Version:** 1.0
**Owner:** National Positions
**Classification:** Internal Operating Framework — Phase 1
**Last Updated:** 2026-05-10

---

## Overview

This checklist defines all inputs required, recommended, and optional for a Klaviyo audit. Katie cannot produce a complete, scored audit without the required inputs. Missing recommended inputs reduce the depth and confidence of specific audit categories. Missing optional inputs are flagged in the output but do not block the audit.

**Before starting any audit, confirm the required section is fully complete.**

---

## Required Inputs

These inputs are mandatory. The audit cannot begin without them.

| # | Input | Format | Notes |
|---|---|---|---|
| 1 | **Business name** | Text | The brand/company name as it appears in Klaviyo |
| 2 | **Website URL** | URL (https://...) | Root domain — e.g., https://brandname.com |
| 3 | **Klaviyo private API key** | String (pk\_...) | Must be read-only — confirmed before audit begins |
| 4 | **User consent** | Checkbox / signed consent | User must explicitly authorize Klaviyo data access |
| 5 | **Audit date range** | Date range selection | See date range options below |

### Date Range Options

| Option | Description |
|---|---|
| Last 30 days | Most recent 30 calendar days |
| Last month | Previous full calendar month |
| Last quarter | Previous full calendar quarter |
| Last 6 months | Previous 180 days |
| Last 12 months | Previous 365 days (recommended default) |
| Custom | User-specified start and end date |

### Comparison Period Options (for trend analysis)

| Option | Description |
|---|---|
| Previous period | Same-length period immediately before the audit period |
| Year over year | Same period from the prior year |
| Custom | User-specified comparison start and end date |

**Every report must clearly label:** client name, website, Klaviyo account, audit period, comparison period (if used), data sources used, and date generated.

---

## API Key Validation Checklist

Before pulling any data, confirm all of the following:

- [ ] API key format is valid (typically begins with `pk_`)
- [ ] API key authenticates successfully against `GET /api/accounts/`
- [ ] API key is confirmed as **read-only** (not full-access or private-write)
- [ ] API key does not have write, send, or admin permissions
- [ ] API key is stored in an environment variable — not in any code file, log, or output
- [ ] User has been informed that their Klaviyo data will be read for audit purposes only
- [ ] User has provided explicit consent

If any of the above checks fail, **stop and resolve before proceeding.**

---

## Recommended Inputs

These inputs meaningfully improve the depth and accuracy of specific audit sections. Collect as many as possible.

| # | Input | Format | Audit Section Impacted |
|---|---|---|---|
| 1 | **Ecommerce platform** | Shopify / WooCommerce / BigCommerce / Magento / Custom | Flow review, integration context |
| 2 | **Monthly ecommerce revenue range** | Range (e.g., $50k–$200k/mo) | Revenue attribution, billing efficiency, opportunity modeling |
| 3 | **Email revenue goal** | Dollar amount or % of total revenue | Revenue attribution, benchmark comparison |
| 4 | **SMS revenue goal** | Dollar amount or % of total revenue | SMS adoption audit |
| 5 | **Main product categories** | Text list | Flow relevance, segmentation review |
| 6 | **Average order value (AOV)** | Dollar amount | Revenue opportunity estimation |
| 7 | **Gross margin** | Percentage | Revenue opportunity estimation (more precise) |
| 8 | **Customer purchase cycle** | One-time / Occasional / Repeat / Subscription | Lifecycle coverage, winback timing |
| 9 | **Current marketing automation goals** | Text | Recommendation prioritization |
| 10 | **Promotions calendar** | Text or dates | Campaign frequency context |
| 11 | **Brand positioning** | Text (premium / value / mass / niche) | Creative and offer review context |

---

## Optional Inputs

These inputs are not required but can significantly enrich specific audit sections when available.

| # | Input | Format | Audit Section Impacted |
|---|---|---|---|
| 1 | **Shopify admin access** | OAuth or export | Flow trigger validation, order data, product catalog |
| 2 | **GA4 access** | OAuth or export | Revenue attribution, email-driven traffic |
| 3 | **AdBeacon data** | Export | Blended ROAS, attribution cross-reference |
| 4 | **Meta Ads data** | Export or access | Audience overlap, retargeting gap analysis |
| 5 | **Google Ads data** | Export or access | Lifecycle signal correlation |
| 6 | **Prior audit reports** | PDF or Doc | Trend comparison, historical context |
| 7 | **Existing flow strategy** | Text or document | Flow configuration context |
| 8 | **Creative examples** | Screenshots or links | Template and creative quality review |
| 9 | **Brand guidelines** | PDF or Doc | Tone and creative review context |
| 10 | **Compliance requirements** | Text | EU/GDPR, CCPA, SMS compliance flags |
| 11 | **Internal notes from account team** | Text | Client-specific context not in Klaviyo data |

---

## Missing Data Handling

When required data is unavailable, Katie follows these rules:

| Situation | Katie's Behavior |
|---|---|
| Required input missing | Audit cannot begin — flag and request from client |
| API key invalid or expired | Audit cannot begin — request updated credentials |
| API endpoint returns no data | Flag as "data unavailable" in that category — do not fabricate |
| Recommended input missing | Reduce confidence level for affected category, note in report |
| Optional input missing | Note in report, do not reduce score |
| Benchmarks unavailable via API | Use documented industry benchmarks with source citation |
| Billing data unavailable | Note in Billing Efficiency section, flag for manual review |
| Form data unavailable | Flag as "forms not accessible via API" — escalate to manual check |

**Rule:** Katie never fabricates data. If a metric cannot be confirmed, she flags it as unavailable and assigns a lower confidence level to that section of the audit.

---

## Intake Form — Recommended Field Order

When collecting inputs from a client or prospect, collect in this order:

```
1. Business Name: _______________
2. Website URL: _______________
3. Ecommerce Platform: [ Shopify ] [ WooCommerce ] [ BigCommerce ] [ Magento ] [ Custom ]
4. Monthly Revenue Range:
   [ Under $10k ] [ $10k–$50k ] [ $50k–$200k ] [ $200k–$1M ] [ $1M+ ]
5. Average Order Value: $_______________
6. Main Product Categories: _______________
7. Customer Purchase Cycle:
   [ One-time ] [ Occasional (2–3x/year) ] [ Repeat (monthly+) ] [ Subscription ]
8. Email Revenue Goal: _______________
9. SMS Revenue Goal (or "Not using SMS"): _______________
10. Biggest Klaviyo Challenge: _______________
11. Audit Date Range:
    [ Last 30 days ] [ Last 90 days ] [ Last 6 months ] [ Last 12 months ] [ Custom: __ to __ ]
12. Klaviyo API Key (read-only): _______________
    [ ] I confirm this key is read-only
    [ ] I authorize National Positions to access my Klaviyo account for audit purposes only
```

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-05-10 | Initial checklist — Phase 1 |
