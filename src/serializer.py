"""
Klaviyo Audit Katie — JSON Serializer
Converts AuditResult to a clean dict for the FastAPI response and Supabase storage.
"""
from __future__ import annotations
from typing import Any, Dict
from .models import AuditResult


def audit_result_to_dict(result: AuditResult) -> Dict[str, Any]:
    opp = getattr(result, "_opportunity", None)
    acct = result.account
    p = acct.profiles
    c = acct.campaigns
    d = acct.deliverability
    r = acct.revenue

    return {
        "account": {
            "business_name": acct.business_name,
            "website": acct.website,
            "klaviyo_account_name": acct.klaviyo_account_name,
            "audit_period_label": acct.audit_period_label,
            "ecommerce_platform": acct.ecommerce_platform,
            "monthly_revenue_range": acct.monthly_revenue_range,
            "sms_enabled": acct.sms_enabled,
        },
        "composite_score": result.composite_score,
        "score_band": result.score_band,
        "category_scores": [
            {
                "name": cs.name,
                "score": cs.score,
                "weight": cs.weight,
                "weighted_points": round(cs.weighted_points, 2),
                "justification": cs.justification,
                "penalties": cs.penalties_applied,
                "bonuses": cs.bonuses_applied,
            }
            for cs in result.category_scores
        ],
        "findings": [
            {
                "rule_id": f.rule_id,
                "severity": f.severity,
                "category": f.category,
                "description": f.description,
                "business_impact": f.business_impact,
                "recommended_action": f.recommended_action,
                "priority": f.priority,
                "score_impact": f.score_impact,
                "confidence": f.confidence,
            }
            for f in result.findings
        ],
        "recommendations": [
            {
                "rec_id": rec.rec_id,
                "source_rules": rec.source_rules,
                "issue": rec.issue,
                "why_it_matters": rec.why_it_matters,
                "expected_impact": rec.expected_impact,
                "complexity": rec.complexity,
                "priority": rec.priority,
                "owner": rec.owner,
                "timeline": rec.timeline,
                "confidence": rec.confidence,
                "opportunity_note": rec.opportunity_note,
                "next_step": rec.next_step,
                "priority_score": rec.priority_score,
            }
            for rec in result.recommendations
        ],
        "opportunity": opp.as_dict() if opp else None,
        "data_gaps": result.data_gaps,
        "profile_metrics": {
            "total_profiles": p.total_profiles,
            "emailable_profiles": p.emailable_profiles,
            "sms_consented_profiles": p.sms_consented_profiles,
            "suppressed_profiles": p.suppressed_profiles,
            "suppression_rate": round(p.suppression_rate, 4),
            "engaged_30_day": p.engaged_30_day,
            "engaged_90_day": p.engaged_90_day,
            "engaged_30_pct": round(p.engaged_30_pct, 4),
            "engaged_90_pct": round(p.engaged_90_pct, 4),
            "dormant_profiles": p.dormant_profiles,
            "dormant_rate": round(p.dormant_rate, 4),
        },
        "campaign_metrics": {
            "total_sent": c.total_sent,
            "email_campaigns": c.email_campaigns,
            "sms_campaigns": c.sms_campaigns,
            "campaigns_per_week": round(c.campaigns_per_week, 2),
            "avg_open_rate": c.avg_open_rate,
            "avg_click_rate": c.avg_click_rate,
            "avg_unsubscribe_rate": c.avg_unsubscribe_rate,
            "avg_spam_complaint_rate": c.avg_spam_complaint_rate,
            "avg_hard_bounce_rate": c.avg_hard_bounce_rate,
            "pct_to_engaged_segments": c.pct_to_engaged_segments,
            "longest_gap_days": c.longest_gap_days,
            "open_rate_trend": c.open_rate_trend,
        },
        "deliverability": {
            "hard_bounce_rate": d.hard_bounce_rate,
            "soft_bounce_rate": d.soft_bounce_rate,
            "spam_complaint_rate": d.spam_complaint_rate,
            "avg_unsubscribe_rate": d.avg_unsubscribe_rate,
            "has_spf": d.has_spf,
            "has_dkim": d.has_dkim,
            "has_dmarc": d.has_dmarc,
            "has_branded_sending_domain": d.has_branded_sending_domain,
            "open_rate_trend": d.open_rate_trend,
        },
        "revenue": {
            "total_klaviyo_revenue": r.total_klaviyo_revenue,
            "campaign_revenue": r.campaign_revenue,
            "flow_revenue": r.flow_revenue,
            "flow_revenue_pct": round(r.flow_revenue_pct, 4),
            "revenue_attribution_configured": r.revenue_attribution_configured,
            "benchmark_overall": r.benchmarks.overall_rating,
        },
        "flows": [
            {
                "name": f.name,
                "status": f.status,
                "flow_type": f.flow_type,
                "email_count": f.email_count,
                "sms_count": f.sms_count,
                "revenue": f.revenue,
                "has_incentive": f.has_incentive,
                "first_message_delay_minutes": f.first_message_delay_minutes,
                "last_updated_days_ago": f.last_updated_days_ago,
            }
            for f in acct.flows
        ],
        "forms": [
            {
                "name": f.name,
                "form_type": f.form_type,
                "status": f.status,
                "opt_in_rate": round(f.opt_in_rate, 4),
                "mobile_opt_in_rate": round(f.mobile_opt_in_rate, 4),
                "collects_sms": f.collects_sms,
                "has_incentive": f.has_incentive,
                "views": f.views,
                "submits": f.submits,
            }
            for f in acct.forms
        ],
        "segmentation": {
            "has_engaged_30_segment": acct.segmentation.has_engaged_30_segment,
            "has_engaged_90_segment": acct.segmentation.has_engaged_90_segment,
            "has_vip_segment": acct.segmentation.has_vip_segment,
            "has_purchaser_segment": acct.segmentation.has_purchaser_segment,
            "has_sunset_segment": acct.segmentation.has_sunset_segment,
            "pct_campaigns_to_engaged": acct.segmentation.pct_campaigns_to_engaged,
            "list_count": acct.list_count,
            "segment_count": acct.segment_count,
        },
        "billing": {
            "plan_tier": acct.billing.plan_tier,
            "plan_profile_limit": acct.billing.plan_profile_limit,
        },
    }
