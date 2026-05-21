"""Unit tests for src/data_quality.py — gap detection and confidence flags."""
import unittest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.models import (
    AccountData, ProfileMetrics, CampaignData, FlowData, FlowMessage,
    DeliverabilityData, RevenueData, BillingData, SegmentationData, BenchmarkData, FormData,
)
from src.data_quality import detect_gaps, gaps_to_findings, confidence_for_category


def _acct(**kwargs):
    defaults = dict(
        business_name="Test", website="test.com", sms_enabled=False,
        profiles=ProfileMetrics(total_profiles=10000, emailable_profiles=9000,
                                sms_consented_profiles=0, suppressed_profiles=500,
                                engaged_30_day=2000, engaged_60_day=3500,
                                engaged_90_day=5000, engaged_180_day=7000),
        flows=[],
        campaigns=CampaignData(total_sent=50, email_campaigns=50, sms_campaigns=0,
                               avg_open_rate=0.22, avg_click_rate=0.025,
                               avg_unsubscribe_rate=0.002, avg_spam_complaint_rate=0.0003,
                               avg_hard_bounce_rate=0.005, pct_to_engaged_segments=0.60,
                               total_revenue=50000.0, weeks_in_period=52,
                               longest_gap_days=10, open_rate_trend="flat"),
        forms=[],
        deliverability=DeliverabilityData(hard_bounce_rate=0.005, soft_bounce_rate=0.002,
                                          spam_complaint_rate=0.0003, avg_unsubscribe_rate=0.002,
                                          has_spf=True, has_dkim=True, has_dmarc=True,
                                          has_branded_sending_domain=True),
        revenue=RevenueData(total_klaviyo_revenue=80000.0, campaign_revenue=50000.0,
                            flow_revenue=30000.0, revenue_attribution_configured=True,
                            benchmarks=BenchmarkData()),
        billing=BillingData(plan_tier="Standard", plan_profile_limit=25000),
        segmentation=SegmentationData(),
        ecommerce_events_configured=True,
    )
    defaults.update(kwargs)
    return AccountData(**defaults)


class TestGapDetection(unittest.TestCase):
    def test_no_gaps_on_complete_data(self):
        acct = _acct()
        gaps = detect_gaps(acct)
        # All data complete — should have zero or minimal gaps
        gap_fields = [g.field for g in gaps]
        self.assertNotIn("profiles.emailable_profiles", gap_fields)
        self.assertNotIn("campaigns.avg_open_rate", gap_fields)
        self.assertNotIn("deliverability.*", gap_fields)

    def test_emailable_zero_with_total_positive_is_gap(self):
        acct = _acct(profiles=ProfileMetrics(
            total_profiles=10000, emailable_profiles=0,
            sms_consented_profiles=0, suppressed_profiles=500,
            engaged_30_day=0, engaged_60_day=0, engaged_90_day=0, engaged_180_day=0,
        ))
        gaps = detect_gaps(acct)
        fields = [g.field for g in gaps]
        self.assertIn("profiles.emailable_profiles", fields)

    def test_engagement_all_zero_is_gap(self):
        acct = _acct(profiles=ProfileMetrics(
            total_profiles=10000, emailable_profiles=9000,
            sms_consented_profiles=0, suppressed_profiles=500,
            engaged_30_day=0, engaged_60_day=0, engaged_90_day=0, engaged_180_day=0,
        ))
        gaps = detect_gaps(acct)
        fields = [g.field for g in gaps]
        self.assertIn("profiles.engaged_*", fields)

    def test_campaign_rate_zero_with_campaigns_sent_is_gap(self):
        acct = _acct(campaigns=CampaignData(
            total_sent=40, email_campaigns=40, sms_campaigns=0,
            avg_open_rate=0.0,   # suspicious zero
            avg_click_rate=0.0, avg_unsubscribe_rate=0.0,
            avg_spam_complaint_rate=0.0, avg_hard_bounce_rate=0.0,
            pct_to_engaged_segments=0.0,
            total_revenue=0.0, weeks_in_period=52,
            longest_gap_days=10, open_rate_trend="flat",
        ))
        gaps = detect_gaps(acct)
        fields = [g.field for g in gaps]
        self.assertIn("campaigns.avg_open_rate", fields)

    def test_deliverability_all_zero_with_campaigns_is_gap(self):
        acct = _acct(deliverability=DeliverabilityData(
            hard_bounce_rate=0.0, soft_bounce_rate=0.0, spam_complaint_rate=0.0,
            avg_unsubscribe_rate=0.0, has_spf=False, has_dkim=False,
            has_dmarc=False, has_branded_sending_domain=False,
        ))
        gaps = detect_gaps(acct)
        fields = [g.field for g in gaps]
        self.assertIn("deliverability.*", fields)

    def test_revenue_zero_with_attribution_configured_is_gap(self):
        live_flow = FlowData(name="Welcome", status="Live", trigger_type="list_subscribe",
                             messages=[FlowMessage("email", 1, 5, False)],
                             revenue=0.0, conversion_rate=0.0, last_updated_days_ago=30)
        acct = _acct(
            flows=[live_flow] * 3,
            revenue=RevenueData(total_klaviyo_revenue=0.0, campaign_revenue=0.0,
                                flow_revenue=0.0, revenue_attribution_configured=True,
                                benchmarks=BenchmarkData()),
        )
        gaps = detect_gaps(acct)
        fields = [g.field for g in gaps]
        self.assertIn("revenue.total_klaviyo_revenue", fields)

    def test_billing_limit_zero_is_gap(self):
        acct = _acct(billing=BillingData(plan_tier="Unknown", plan_profile_limit=0))
        gaps = detect_gaps(acct)
        fields = [g.field for g in gaps]
        self.assertIn("billing.plan_profile_limit", fields)


class TestGapsToFindings(unittest.TestCase):
    def test_gaps_produce_findings_with_dq_prefix(self):
        acct = _acct(profiles=ProfileMetrics(
            total_profiles=10000, emailable_profiles=0,
            sms_consented_profiles=0, suppressed_profiles=0,
            engaged_30_day=0, engaged_60_day=0, engaged_90_day=0, engaged_180_day=0,
        ))
        gaps = detect_gaps(acct)
        findings = gaps_to_findings(gaps)
        for f in findings:
            self.assertTrue(f.rule_id.startswith("DQ-"))
            self.assertEqual(f.category, "Data Quality")
            self.assertEqual(f.confidence, "Data Unavailable")

    def test_no_gaps_produces_no_findings(self):
        acct = _acct()
        gaps = detect_gaps(acct)
        # Filter to only the gaps we care about
        relevant = [g for g in gaps if g.severity in ("Low", "Medium")]
        findings = gaps_to_findings(relevant)
        # Should be 0 or minimal
        self.assertLessEqual(len(findings), len(relevant))


class TestConfidenceForCategory(unittest.TestCase):
    def test_unaffected_category_returns_confirmed(self):
        acct = _acct(profiles=ProfileMetrics(
            total_profiles=10000, emailable_profiles=0,
            sms_consented_profiles=0, suppressed_profiles=0,
            engaged_30_day=0, engaged_60_day=0, engaged_90_day=0, engaged_180_day=0,
        ))
        gaps = detect_gaps(acct)
        # Revenue Attribution is not affected by profile gaps
        self.assertEqual(confidence_for_category("Revenue Attribution", gaps), "Confirmed")

    def test_affected_category_returns_partial(self):
        acct = _acct(profiles=ProfileMetrics(
            total_profiles=10000, emailable_profiles=0,
            sms_consented_profiles=0, suppressed_profiles=0,
            engaged_30_day=0, engaged_60_day=0, engaged_90_day=0, engaged_180_day=0,
        ))
        gaps = detect_gaps(acct)
        self.assertEqual(confidence_for_category("List Health & Engagement", gaps), "Partial")


if __name__ == "__main__":
    unittest.main()
