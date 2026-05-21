"""Unit tests for src/rules.py — verifies rules fire on correct conditions and stay silent otherwise."""
import unittest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.models import (
    AccountData, ProfileMetrics, CampaignData, FlowData, FlowMessage,
    FormData, DeliverabilityData, RevenueData, BillingData,
    SegmentationData, BenchmarkData,
)
from src.rules import run_rules, _rules_sms, _rules_campaigns, _rules_deliverability, _rules_flows


def _base_acct(**kwargs) -> AccountData:
    defaults = dict(
        business_name="Test", website="test.com", sms_enabled=True,
        profiles=ProfileMetrics(
            total_profiles=20000, emailable_profiles=18000,
            sms_consented_profiles=2000, suppressed_profiles=1000,
            engaged_30_day=4000, engaged_60_day=7000,
            engaged_90_day=10000, engaged_180_day=14000,
        ),
        flows=[
            FlowData(name="Welcome Series", status="Live", trigger_type="list_subscribe",
                     messages=[FlowMessage("email", 1, 5, True),
                                FlowMessage("email", 2, 2880, False),
                                FlowMessage("email", 3, 7200, False)],
                     revenue=15000.0, conversion_rate=0.06, last_updated_days_ago=30),
            FlowData(name="Abandoned Cart Recovery", status="Live", trigger_type="checkout_started",
                     messages=[FlowMessage("sms", 1, 30, False),
                                FlowMessage("email", 2, 60, False),
                                FlowMessage("email", 3, 1440, True)],
                     revenue=30000.0, conversion_rate=0.08, last_updated_days_ago=30),
            FlowData(name="Post-Purchase Thank You", status="Live", trigger_type="placed_order",
                     messages=[FlowMessage("email", 1, 30, False),
                                FlowMessage("email", 2, 4320, False)],
                     revenue=8000.0, conversion_rate=0.04, last_updated_days_ago=60),
        ],
        campaigns=CampaignData(
            total_sent=60, email_campaigns=55, sms_campaigns=5,
            avg_open_rate=0.24, avg_click_rate=0.028, avg_unsubscribe_rate=0.002,
            avg_spam_complaint_rate=0.0002, avg_hard_bounce_rate=0.004,
            pct_to_engaged_segments=0.70, total_revenue=80000.0,
            weeks_in_period=52, longest_gap_days=10, open_rate_trend="flat",
        ),
        forms=[FormData(form_id="f1", name="Popup", form_type="popup",
                        status="Published", views=100000, submits=3000,
                        mobile_views=60000, mobile_submits=1800,
                        collects_sms=True, has_incentive=True)],
        deliverability=DeliverabilityData(
            hard_bounce_rate=0.004, soft_bounce_rate=0.002,
            spam_complaint_rate=0.0002, avg_unsubscribe_rate=0.002,
            has_spf=True, has_dkim=True, has_dmarc=True,
            has_branded_sending_domain=True, open_rate_trend="flat",
        ),
        revenue=RevenueData(
            total_klaviyo_revenue=133000.0, campaign_revenue=80000.0,
            flow_revenue=53000.0, revenue_attribution_configured=True,
            benchmarks=BenchmarkData(),
        ),
        billing=BillingData(plan_tier="Standard", plan_profile_limit=25000),
        segmentation=SegmentationData(
            has_engaged_30_segment=True, has_engaged_90_segment=True,
            has_vip_segment=True, has_purchaser_segment=True,
            has_sunset_segment=True, pct_campaigns_to_engaged=0.70,
        ),
        ecommerce_events_configured=True,
    )
    defaults.update(kwargs)
    return AccountData(**defaults)


def _rule_ids(findings) -> set:
    return {f.rule_id for f in findings}


class TestSMSRules(unittest.TestCase):
    def test_sms_001_fires_when_sms_disabled(self):
        acct = _base_acct(sms_enabled=False)
        findings = _rules_sms(acct)
        self.assertIn("SMS-001", _rule_ids(findings))

    def test_sms_001_silent_when_sms_enabled(self):
        acct = _base_acct(sms_enabled=True)
        findings = _rules_sms(acct)
        self.assertNotIn("SMS-001", _rule_ids(findings))

    def test_sms_disabled_returns_only_sms_001(self):
        """When SMS is disabled, only SMS-001 fires — later SMS rules are skipped."""
        acct = _base_acct(sms_enabled=False)
        findings = _rules_sms(acct)
        ids = _rule_ids(findings)
        self.assertEqual(ids, {"SMS-001"})

    def test_sms_002_fires_when_consent_rate_very_low(self):
        acct = _base_acct(sms_enabled=True, profiles=ProfileMetrics(
            total_profiles=20000, emailable_profiles=18000,
            sms_consented_profiles=200,   # 1.1% — below 5% threshold
            suppressed_profiles=1000, engaged_30_day=4000, engaged_60_day=7000,
            engaged_90_day=10000, engaged_180_day=14000,
        ))
        findings = _rules_sms(acct)
        self.assertIn("SMS-002", _rule_ids(findings))

    def test_sms_004_fires_when_no_sms_in_flows(self):
        email_only_flow = FlowData(
            name="Welcome Series", status="Live", trigger_type="list_subscribe",
            messages=[FlowMessage("email", 1, 5, True), FlowMessage("email", 2, 2880, False)],
            revenue=5000.0, conversion_rate=0.05, last_updated_days_ago=30,
        )
        acct = _base_acct(sms_enabled=True, flows=[email_only_flow])
        findings = _rules_sms(acct)
        self.assertIn("SMS-004", _rule_ids(findings))

    def test_sms_004_silent_when_sms_in_flows(self):
        """Base acct has SMS in Abandoned Cart — SMS-004 should not fire."""
        acct = _base_acct()
        findings = _rules_sms(acct)
        self.assertNotIn("SMS-004", _rule_ids(findings))


class TestCampaignRules(unittest.TestCase):
    def test_camp_001_fires_on_low_frequency(self):
        low_freq = CampaignData(
            total_sent=15, email_campaigns=15, sms_campaigns=0,
            avg_open_rate=0.22, avg_click_rate=0.02, avg_unsubscribe_rate=0.002,
            avg_spam_complaint_rate=0.0002, avg_hard_bounce_rate=0.004,
            pct_to_engaged_segments=0.70, total_revenue=20000.0,
            weeks_in_period=52, longest_gap_days=10, open_rate_trend="flat",
        )
        acct = _base_acct(campaigns=low_freq)
        findings = _rules_campaigns(acct)
        self.assertIn("CAMP-001", _rule_ids(findings))

    def test_camp_001_silent_on_good_frequency(self):
        acct = _base_acct()
        findings = _rules_campaigns(acct)
        self.assertNotIn("CAMP-001", _rule_ids(findings))

    def test_camp_003_fires_on_very_low_segment_rate(self):
        bad = CampaignData(
            total_sent=60, email_campaigns=60, sms_campaigns=0,
            avg_open_rate=0.22, avg_click_rate=0.02, avg_unsubscribe_rate=0.002,
            avg_spam_complaint_rate=0.0002, avg_hard_bounce_rate=0.004,
            pct_to_engaged_segments=0.10,  # below 25%
            total_revenue=50000.0, weeks_in_period=52,
            longest_gap_days=10, open_rate_trend="flat",
        )
        acct = _base_acct(campaigns=bad)
        findings = _rules_campaigns(acct)
        self.assertIn("CAMP-003", _rule_ids(findings))

    def test_camp_006_critical_severity_on_high_spam(self):
        bad = CampaignData(
            total_sent=60, email_campaigns=60, sms_campaigns=0,
            avg_open_rate=0.22, avg_click_rate=0.02, avg_unsubscribe_rate=0.002,
            avg_spam_complaint_rate=0.0015,   # above 0.1% threshold
            avg_hard_bounce_rate=0.004, pct_to_engaged_segments=0.70,
            total_revenue=50000.0, weeks_in_period=52,
            longest_gap_days=10, open_rate_trend="flat",
        )
        acct = _base_acct(campaigns=bad)
        findings = _rules_campaigns(acct)
        spam_findings = [f for f in findings if f.rule_id == "CAMP-006"]
        self.assertTrue(spam_findings)
        self.assertEqual(spam_findings[0].severity, "Critical")


class TestDeliverabilityRules(unittest.TestCase):
    def test_delv_001_fires_on_critical_bounce(self):
        acct = _base_acct(deliverability=DeliverabilityData(
            hard_bounce_rate=0.025, spam_complaint_rate=0.0002,
            soft_bounce_rate=0.003, avg_unsubscribe_rate=0.002,
            has_spf=True, has_dkim=True, has_dmarc=True, has_branded_sending_domain=True,
        ))
        findings = _rules_deliverability(acct)
        self.assertIn("DELV-001", _rule_ids(findings))

    def test_delv_001_silent_on_acceptable_bounce(self):
        acct = _base_acct()  # hard_bounce_rate = 0.004
        findings = _rules_deliverability(acct)
        self.assertNotIn("DELV-001", _rule_ids(findings))

    def test_delv_005_fires_when_dkim_missing(self):
        acct = _base_acct(deliverability=DeliverabilityData(
            hard_bounce_rate=0.004, spam_complaint_rate=0.0002,
            soft_bounce_rate=0.002, avg_unsubscribe_rate=0.002,
            has_spf=True, has_dkim=False, has_dmarc=True, has_branded_sending_domain=True,
        ))
        findings = _rules_deliverability(acct)
        self.assertIn("DELV-005", _rule_ids(findings))

    def test_delv_005_silent_when_dkim_present(self):
        acct = _base_acct()
        findings = _rules_deliverability(acct)
        self.assertNotIn("DELV-005", _rule_ids(findings))

    def test_delv_003_critical_severity(self):
        acct = _base_acct(deliverability=DeliverabilityData(
            hard_bounce_rate=0.004, spam_complaint_rate=0.0015,
            soft_bounce_rate=0.002, avg_unsubscribe_rate=0.002,
            has_spf=True, has_dkim=True, has_dmarc=True, has_branded_sending_domain=True,
        ))
        findings = _rules_deliverability(acct)
        spam_f = [f for f in findings if f.rule_id == "DELV-003"]
        self.assertTrue(spam_f)
        self.assertEqual(spam_f[0].severity, "Critical")


class TestFlowRules(unittest.TestCase):
    def test_flow_001_fires_when_no_welcome(self):
        acct = _base_acct(flows=[
            FlowData(name="Abandoned Cart Recovery", status="Live",
                     trigger_type="checkout_started",
                     messages=[FlowMessage("email", 1, 60, False)],
                     revenue=20000.0, conversion_rate=0.07, last_updated_days_ago=30),
        ])
        findings = _rules_flows(acct)
        self.assertIn("FLOW-001", _rule_ids(findings))

    def test_flow_001_silent_when_welcome_exists(self):
        acct = _base_acct()
        findings = _rules_flows(acct)
        self.assertNotIn("FLOW-001", _rule_ids(findings))

    def test_flow_004_fires_when_no_abandoned_cart(self):
        acct = _base_acct(flows=[
            FlowData(name="Welcome Series", status="Live",
                     trigger_type="list_subscribe",
                     messages=[FlowMessage("email", 1, 5, True)],
                     revenue=5000.0, conversion_rate=0.04, last_updated_days_ago=30),
        ])
        findings = _rules_flows(acct)
        self.assertIn("FLOW-004", _rule_ids(findings))

    def test_flow_004_silent_when_abandoned_cart_exists(self):
        acct = _base_acct()
        findings = _rules_flows(acct)
        self.assertNotIn("FLOW-004", _rule_ids(findings))

    def test_flow_002_fires_on_late_welcome_email(self):
        late_welcome = FlowData(
            name="Welcome Series", status="Live", trigger_type="list_subscribe",
            messages=[FlowMessage("email", 1, 200, False)],  # 200 min > 60 min threshold
            revenue=5000.0, conversion_rate=0.04, last_updated_days_ago=30,
        )
        acct = _base_acct(flows=[late_welcome])
        findings = _rules_flows(acct)
        self.assertIn("FLOW-002", _rule_ids(findings))

    def test_flow_001_is_critical(self):
        acct = _base_acct(flows=[])
        findings = _rules_flows(acct)
        welcome_findings = [f for f in findings if f.rule_id == "FLOW-001"]
        self.assertTrue(welcome_findings)
        self.assertEqual(welcome_findings[0].severity, "Critical")


class TestRunRules(unittest.TestCase):
    def test_findings_sorted_by_severity(self):
        acct = _base_acct(sms_enabled=False, flows=[])
        findings = run_rules(acct)
        severity_order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
        for i in range(len(findings) - 1):
            self.assertLessEqual(
                severity_order.get(findings[i].severity, 99),
                severity_order.get(findings[i + 1].severity, 99),
                f"Finding {findings[i].rule_id} ({findings[i].severity}) appears before "
                f"{findings[i+1].rule_id} ({findings[i+1].severity})",
            )

    def test_clean_account_has_few_findings(self):
        """A well-configured account should produce minimal findings."""
        acct = _base_acct()
        findings = run_rules(acct)
        critical = [f for f in findings if f.severity == "Critical"]
        self.assertEqual(len(critical), 0, f"Expected 0 critical findings, got: {[f.rule_id for f in critical]}")

    def test_all_findings_have_required_fields(self):
        acct = _base_acct(sms_enabled=False, flows=[])
        for finding in run_rules(acct):
            self.assertTrue(finding.rule_id, f"Finding missing rule_id")
            self.assertIn(finding.severity, ("Critical", "High", "Medium", "Low"))
            self.assertTrue(finding.description)
            self.assertTrue(finding.recommended_action)


if __name__ == "__main__":
    unittest.main()
