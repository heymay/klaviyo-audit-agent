"""Unit tests for src/scorer.py — all 10 category scorers and composite calculation."""
import unittest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.models import (
    AccountData, ProfileMetrics, CampaignData, FlowData, FlowMessage,
    FormData, DeliverabilityData, RevenueData, BillingData,
    SegmentationData, BenchmarkData,
)
from src.scorer import (
    run_scoring, score_band,
    _score_deliverability, _score_core_flow_coverage, _score_flow_configuration,
    _score_campaign_strategy, _score_sms_adoption, _score_signup_forms,
    _score_list_health, _score_segmentation, _score_revenue_attribution,
    _score_billing,
)


def _make_acct(**kwargs) -> AccountData:
    """Build a minimal AccountData with sensible defaults; override via kwargs."""
    defaults = dict(
        business_name="Test Co",
        website="test.com",
        sms_enabled=False,
        profiles=ProfileMetrics(
            total_profiles=10000, emailable_profiles=9000,
            sms_consented_profiles=0, suppressed_profiles=500,
            engaged_30_day=2000, engaged_60_day=3500,
            engaged_90_day=5000, engaged_180_day=7000,
        ),
        flows=[],
        campaigns=CampaignData(
            total_sent=50, email_campaigns=50, sms_campaigns=0,
            avg_open_rate=0.22, avg_click_rate=0.025,
            avg_unsubscribe_rate=0.002, avg_spam_complaint_rate=0.0003,
            avg_hard_bounce_rate=0.005, pct_to_engaged_segments=0.60,
            total_revenue=50000.0, weeks_in_period=52,
            longest_gap_days=10, open_rate_trend="flat",
        ),
        forms=[],
        deliverability=DeliverabilityData(
            hard_bounce_rate=0.005, soft_bounce_rate=0.002,
            spam_complaint_rate=0.0003, avg_unsubscribe_rate=0.002,
            has_spf=True, has_dkim=True, has_dmarc=True,
            has_branded_sending_domain=True, open_rate_trend="flat",
        ),
        revenue=RevenueData(
            total_klaviyo_revenue=80000.0, campaign_revenue=50000.0,
            flow_revenue=30000.0, revenue_attribution_configured=True,
            benchmarks=BenchmarkData(),
        ),
        billing=BillingData(plan_tier="Standard", plan_profile_limit=25000),
        segmentation=SegmentationData(
            has_engaged_30_segment=True, has_engaged_90_segment=True,
            has_vip_segment=False, has_purchaser_segment=True,
            has_sunset_segment=False, pct_campaigns_to_engaged=0.60,
        ),
        ecommerce_events_configured=True,
    )
    defaults.update(kwargs)
    return AccountData(**defaults)


def _live_flow(name: str, emails: int = 3, sms: int = 0,
               has_discount: bool = False, delay_first: int = 5,
               revenue: float = 10000.0) -> FlowData:
    msgs = [FlowMessage("email", i + 1, delay_first if i == 0 else 1440, has_discount and i == emails - 1)
            for i in range(emails)]
    msgs += [FlowMessage("sms", emails + j + 1, 30, False) for j in range(sms)]
    return FlowData(name=name, status="Live", trigger_type="list_subscribe",
                    messages=msgs, revenue=revenue, conversion_rate=0.05,
                    last_updated_days_ago=30)


class TestScoreBand(unittest.TestCase):
    def test_bands(self):
        self.assertEqual(score_band(95), "Elite")
        self.assertEqual(score_band(80), "Strong")
        self.assertEqual(score_band(65), "Average")
        self.assertEqual(score_band(50), "Weak")
        self.assertEqual(score_band(30), "Critical")
        self.assertEqual(score_band(0), "Critical")
        self.assertEqual(score_band(75), "Strong")
        self.assertEqual(score_band(60), "Average")
        self.assertEqual(score_band(90), "Elite")


class TestDeliverabilityScorer(unittest.TestCase):
    def test_perfect_deliverability(self):
        acct = _make_acct()
        cs = _score_deliverability(acct)
        self.assertGreaterEqual(cs.score, 9)

    def test_critical_bounce_caps_at_2(self):
        acct = _make_acct(deliverability=DeliverabilityData(
            hard_bounce_rate=0.025, spam_complaint_rate=0.0003,
            has_spf=True, has_dkim=True, has_dmarc=True, has_branded_sending_domain=True,
        ))
        cs = _score_deliverability(acct)
        self.assertLessEqual(cs.score, 2)

    def test_critical_spam_caps_at_2(self):
        acct = _make_acct(deliverability=DeliverabilityData(
            hard_bounce_rate=0.001, spam_complaint_rate=0.0015,
            has_spf=True, has_dkim=True, has_dmarc=True, has_branded_sending_domain=True,
        ))
        cs = _score_deliverability(acct)
        self.assertLessEqual(cs.score, 2)

    def test_missing_dkim_penalised(self):
        acct_with = _make_acct()
        acct_without = _make_acct(deliverability=DeliverabilityData(
            hard_bounce_rate=0.005, spam_complaint_rate=0.0003,
            has_spf=True, has_dkim=False, has_dmarc=True, has_branded_sending_domain=True,
        ))
        self.assertGreater(_score_deliverability(acct_with).score,
                           _score_deliverability(acct_without).score)

    def test_improving_trend_bonus(self):
        acct_flat = _make_acct()
        acct_improving = _make_acct(deliverability=DeliverabilityData(
            hard_bounce_rate=0.005, spam_complaint_rate=0.0003,
            has_spf=True, has_dkim=True, has_dmarc=True, has_branded_sending_domain=True,
            open_rate_trend="improving",
        ))
        self.assertGreaterEqual(_score_deliverability(acct_improving).score,
                                _score_deliverability(acct_flat).score)

    def test_weight_is_15pct(self):
        acct = _make_acct()
        cs = _score_deliverability(acct)
        self.assertAlmostEqual(cs.weight, 0.15)


class TestCoreFlowCoverageScorer(unittest.TestCase):
    def _acct_with_flows(self, *names):
        flows = [_live_flow(n) for n in names]
        return _make_acct(flows=flows)

    def test_all_six_core_flows_scores_high(self):
        acct = self._acct_with_flows(
            "Welcome Series", "Abandoned Cart Recovery",
            "Browse Abandonment", "Added to Cart",
            "Post-Purchase Thank You", "Win Back",
        )
        cs = _score_core_flow_coverage(acct)
        self.assertGreaterEqual(cs.score, 9)

    def test_no_flows_scores_at_most_2(self):
        # No flows → both welcome and abandoned cart missing → cap at 2
        acct = _make_acct(flows=[])
        cs = _score_core_flow_coverage(acct)
        self.assertLessEqual(cs.score, 2)

    def test_missing_abandoned_cart_caps_at_4(self):
        acct = self._acct_with_flows("Welcome Series", "Browse Abandonment", "Post-Purchase")
        cs = _score_core_flow_coverage(acct)
        self.assertLessEqual(cs.score, 4)

    def test_missing_welcome_caps_at_4(self):
        acct = self._acct_with_flows("Abandoned Cart Recovery", "Browse Abandonment")
        cs = _score_core_flow_coverage(acct)
        self.assertLessEqual(cs.score, 4)

    def test_missing_both_critical_flows_caps_at_2(self):
        acct = self._acct_with_flows("Browse Abandonment", "Post-Purchase Thank You")
        cs = _score_core_flow_coverage(acct)
        self.assertLessEqual(cs.score, 2)

    def test_vip_flow_adds_bonus(self):
        acct_no_vip = self._acct_with_flows(
            "Welcome Series", "Abandoned Cart Recovery", "Browse Abandonment",
            "Added to Cart", "Post-Purchase", "Win Back",
        )
        acct_with_vip = self._acct_with_flows(
            "Welcome Series", "Abandoned Cart Recovery", "Browse Abandonment",
            "Added to Cart", "Post-Purchase", "Win Back", "VIP Loyalty",
        )
        self.assertGreaterEqual(_score_core_flow_coverage(acct_with_vip).score,
                                _score_core_flow_coverage(acct_no_vip).score)

    def test_weight_is_15pct(self):
        acct = _make_acct()
        cs = _score_core_flow_coverage(acct)
        self.assertAlmostEqual(cs.weight, 0.15)


class TestFlowConfigurationScorer(unittest.TestCase):
    def test_no_live_flows_scores_1(self):
        acct = _make_acct(flows=[])
        cs = _score_flow_configuration(acct)
        self.assertEqual(cs.score, 1)

    def test_late_welcome_email_penalised(self):
        early = _live_flow("Welcome Series", delay_first=5)
        late = FlowData(name="Welcome Series", status="Live", trigger_type="list_subscribe",
                        messages=[FlowMessage("email", 1, 200, False)],  # 200 min delay
                        revenue=5000.0, conversion_rate=0.05, last_updated_days_ago=30)
        acct_early = _make_acct(flows=[early])
        acct_late = _make_acct(flows=[late])
        self.assertGreater(_score_flow_configuration(acct_early).score,
                           _score_flow_configuration(acct_late).score)

    def test_abandoned_cart_without_incentive_penalised(self):
        with_disc = _live_flow("Abandoned Cart Recovery", emails=3, has_discount=True)
        without_disc = _live_flow("Abandoned Cart Recovery", emails=3, has_discount=False)
        acct_with = _make_acct(flows=[with_disc])
        acct_without = _make_acct(flows=[without_disc])
        self.assertGreaterEqual(_score_flow_configuration(acct_with).score,
                                _score_flow_configuration(acct_without).score)

    def test_sms_enabled_no_sms_in_flows_penalised(self):
        email_only_flow = _live_flow("Welcome Series", emails=3, sms=0)
        acct_no_sms = _make_acct(sms_enabled=False, flows=[email_only_flow])
        acct_sms_no_flow = _make_acct(sms_enabled=True, flows=[email_only_flow])
        self.assertGreaterEqual(_score_flow_configuration(acct_no_sms).score,
                                _score_flow_configuration(acct_sms_no_flow).score)


class TestCampaignStrategyScorer(unittest.TestCase):
    def test_very_low_frequency_penalised(self):
        low = CampaignData(total_sent=10, email_campaigns=10, sms_campaigns=0,
                           avg_open_rate=0.25, avg_click_rate=0.03,
                           avg_unsubscribe_rate=0.001, avg_spam_complaint_rate=0.0002,
                           avg_hard_bounce_rate=0.003, pct_to_engaged_segments=0.7,
                           weeks_in_period=52, longest_gap_days=5, open_rate_trend="flat")
        good = CampaignData(total_sent=80, email_campaigns=80, sms_campaigns=0,
                            avg_open_rate=0.25, avg_click_rate=0.03,
                            avg_unsubscribe_rate=0.001, avg_spam_complaint_rate=0.0002,
                            avg_hard_bounce_rate=0.003, pct_to_engaged_segments=0.7,
                            weeks_in_period=52, longest_gap_days=5, open_rate_trend="flat")
        acct_low = _make_acct(campaigns=low)
        acct_good = _make_acct(campaigns=good)
        self.assertGreater(_score_campaign_strategy(acct_good).score,
                           _score_campaign_strategy(acct_low).score)

    def test_critical_spam_rate_penalised(self):
        bad = CampaignData(total_sent=50, email_campaigns=50, sms_campaigns=0,
                           avg_open_rate=0.20, avg_click_rate=0.02,
                           avg_unsubscribe_rate=0.002, avg_spam_complaint_rate=0.0015,
                           avg_hard_bounce_rate=0.004, pct_to_engaged_segments=0.5,
                           weeks_in_period=52, longest_gap_days=10, open_rate_trend="flat")
        acct = _make_acct(campaigns=bad)
        cs = _score_campaign_strategy(acct)
        self.assertLessEqual(cs.score, 4)

    def test_low_engaged_segment_rate_penalised(self):
        bad_seg = CampaignData(total_sent=50, email_campaigns=50, sms_campaigns=0,
                               avg_open_rate=0.22, avg_click_rate=0.025,
                               avg_unsubscribe_rate=0.002, avg_spam_complaint_rate=0.0003,
                               avg_hard_bounce_rate=0.005, pct_to_engaged_segments=0.10,
                               weeks_in_period=52, longest_gap_days=10, open_rate_trend="flat")
        acct = _make_acct(campaigns=bad_seg)
        cs = _score_campaign_strategy(acct)
        self.assertLessEqual(cs.score, 5)

    def test_weight_is_12pct(self):
        cs = _score_campaign_strategy(_make_acct())
        self.assertAlmostEqual(cs.weight, 0.12)


class TestSMSAdoptionScorer(unittest.TestCase):
    def test_sms_disabled_scores_2(self):
        acct = _make_acct(sms_enabled=False)
        cs = _score_sms_adoption(acct)
        self.assertEqual(cs.score, 2)

    def test_sms_enabled_with_flows_and_campaigns_scores_above_2(self):
        # SMS enabled + good consent rate + SMS in flows + SMS campaigns → scores > 2
        sms_flow = FlowData(
            name="Welcome Series", status="Live", trigger_type="list_subscribe",
            messages=[FlowMessage("email", 1, 5, True), FlowMessage("sms", 2, 60, False)],
            revenue=5000.0, conversion_rate=0.05, last_updated_days_ago=30,
        )
        sms_form = FormData(form_id="f1", name="Popup", form_type="popup",
                            status="Published", views=100000, submits=3000,
                            mobile_views=0, mobile_submits=0,
                            collects_sms=True, has_incentive=True)
        acct = _make_acct(
            sms_enabled=True,
            flows=[sms_flow],
            forms=[sms_form],
            profiles=ProfileMetrics(
                total_profiles=10000, emailable_profiles=9000,
                sms_consented_profiles=2000, suppressed_profiles=500,
                engaged_30_day=2000, engaged_60_day=3500,
                engaged_90_day=5000, engaged_180_day=7000,
            ),
            campaigns=CampaignData(
                total_sent=50, email_campaigns=45, sms_campaigns=5,
                avg_open_rate=0.22, avg_click_rate=0.025, avg_unsubscribe_rate=0.002,
                avg_spam_complaint_rate=0.0003, avg_hard_bounce_rate=0.005,
                pct_to_engaged_segments=0.60, total_revenue=50000.0,
                weeks_in_period=52, longest_gap_days=10, open_rate_trend="flat",
            ),
        )
        cs = _score_sms_adoption(acct)
        self.assertGreater(cs.score, 2)

    def test_low_sms_consent_rate_penalised(self):
        high_consent = _make_acct(sms_enabled=True, profiles=ProfileMetrics(
            total_profiles=10000, emailable_profiles=9000,
            sms_consented_profiles=3000, suppressed_profiles=500,
            engaged_30_day=2000, engaged_60_day=3500,
            engaged_90_day=5000, engaged_180_day=7000,
        ))
        low_consent = _make_acct(sms_enabled=True, profiles=ProfileMetrics(
            total_profiles=10000, emailable_profiles=9000,
            sms_consented_profiles=100, suppressed_profiles=500,
            engaged_30_day=2000, engaged_60_day=3500,
            engaged_90_day=5000, engaged_180_day=7000,
        ))
        self.assertGreater(_score_sms_adoption(high_consent).score,
                           _score_sms_adoption(low_consent).score)

    def test_weight_is_10pct(self):
        cs = _score_sms_adoption(_make_acct())
        self.assertAlmostEqual(cs.weight, 0.10)


class TestSignupFormsScorer(unittest.TestCase):
    def test_no_forms_scores_1(self):
        acct = _make_acct(forms=[])
        cs = _score_signup_forms(acct)
        self.assertEqual(cs.score, 1)

    def test_sub_1pct_opt_in_caps_at_3(self):
        bad_form = FormData(form_id="f1", name="Popup", form_type="popup",
                            status="Published", views=100000, submits=500,
                            mobile_views=0, mobile_submits=0,
                            collects_sms=False, has_incentive=False)
        acct = _make_acct(forms=[bad_form])
        cs = _score_signup_forms(acct)
        self.assertLessEqual(cs.score, 3)

    def test_good_opt_in_rate_scores_well(self):
        good_form = FormData(form_id="f1", name="Popup", form_type="popup",
                             status="Published", views=100000, submits=5000,
                             mobile_views=60000, mobile_submits=3000,
                             collects_sms=False, has_incentive=True)
        acct = _make_acct(forms=[good_form])
        cs = _score_signup_forms(acct)
        self.assertGreaterEqual(cs.score, 7)

    def test_weight_is_10pct(self):
        cs = _score_signup_forms(_make_acct())
        self.assertAlmostEqual(cs.weight, 0.10)


class TestListHealthScorer(unittest.TestCase):
    def test_high_dormant_rate_critical(self):
        acct = _make_acct(profiles=ProfileMetrics(
            total_profiles=10000, emailable_profiles=9000,
            sms_consented_profiles=0, suppressed_profiles=500,
            engaged_30_day=500, engaged_60_day=800,
            engaged_90_day=1200, engaged_180_day=3000,   # 67% dormant
        ))
        cs = _score_list_health(acct)
        self.assertLessEqual(cs.score, 4)

    def test_high_suppression_penalised(self):
        acct = _make_acct(profiles=ProfileMetrics(
            total_profiles=10000, emailable_profiles=7000,
            sms_consented_profiles=0, suppressed_profiles=3000,  # 30% suppression
            engaged_30_day=2000, engaged_60_day=3500,
            engaged_90_day=5000, engaged_180_day=6000,
        ))
        cs = _score_list_health(acct)
        self.assertLessEqual(cs.score, 6)

    def test_healthy_list_scores_well(self):
        acct = _make_acct(profiles=ProfileMetrics(
            total_profiles=10000, emailable_profiles=9500,
            sms_consented_profiles=2000, suppressed_profiles=300,
            engaged_30_day=3000, engaged_60_day=5000,
            engaged_90_day=6500, engaged_180_day=8500,
        ))
        cs = _score_list_health(acct)
        self.assertGreaterEqual(cs.score, 7)

    def test_zero_emailable_scores_1(self):
        acct = _make_acct(profiles=ProfileMetrics(total_profiles=0, emailable_profiles=0))
        cs = _score_list_health(acct)
        self.assertEqual(cs.score, 1)

    def test_weight_is_10pct(self):
        cs = _score_list_health(_make_acct())
        self.assertAlmostEqual(cs.weight, 0.10)


class TestSegmentationScorer(unittest.TestCase):
    def test_all_segments_scores_high(self):
        acct = _make_acct(segmentation=SegmentationData(
            has_engaged_30_segment=True, has_engaged_90_segment=True,
            has_vip_segment=True, has_purchaser_segment=True,
            has_sunset_segment=True, pct_campaigns_to_engaged=0.80,
        ))
        cs = _score_segmentation(acct)
        self.assertGreaterEqual(cs.score, 9)

    def test_no_segments_scores_low(self):
        acct = _make_acct(segmentation=SegmentationData(
            has_engaged_30_segment=False, has_engaged_90_segment=False,
            has_vip_segment=False, has_purchaser_segment=False,
            has_sunset_segment=False, pct_campaigns_to_engaged=0.05,
        ))
        cs = _score_segmentation(acct)
        self.assertLessEqual(cs.score, 3)

    def test_weight_is_6pct(self):
        cs = _score_segmentation(_make_acct())
        self.assertAlmostEqual(cs.weight, 0.06)


class TestRevenueAttributionScorer(unittest.TestCase):
    def test_no_attribution_caps_at_2(self):
        acct = _make_acct(revenue=RevenueData(
            total_klaviyo_revenue=0.0, campaign_revenue=0.0,
            flow_revenue=0.0, revenue_attribution_configured=False,
            benchmarks=BenchmarkData(),
        ))
        cs = _score_revenue_attribution(acct)
        self.assertEqual(cs.score, 2)

    def test_low_flow_revenue_share_penalised(self):
        acct = _make_acct(revenue=RevenueData(
            total_klaviyo_revenue=100000.0, campaign_revenue=90000.0,
            flow_revenue=10000.0, revenue_attribution_configured=True,
            benchmarks=BenchmarkData(),
        ))
        cs = _score_revenue_attribution(acct)
        self.assertLessEqual(cs.score, 6)

    def test_weight_is_5pct(self):
        cs = _score_revenue_attribution(_make_acct())
        self.assertAlmostEqual(cs.weight, 0.05)


class TestBillingScorer(unittest.TestCase):
    def test_near_limit_penalised(self):
        acct = _make_acct(
            profiles=ProfileMetrics(total_profiles=24500, emailable_profiles=22000,
                                    suppressed_profiles=1000, sms_consented_profiles=0,
                                    engaged_30_day=5000, engaged_60_day=8000,
                                    engaged_90_day=12000, engaged_180_day=18000),
            billing=BillingData(plan_tier="Standard", plan_profile_limit=25000),
        )
        cs = _score_billing(acct)
        self.assertLessEqual(cs.score, 6)

    def test_severely_underutilised_penalised(self):
        acct = _make_acct(
            profiles=ProfileMetrics(total_profiles=5000, emailable_profiles=4500,
                                    suppressed_profiles=200, sms_consented_profiles=0,
                                    engaged_30_day=1000, engaged_60_day=1500,
                                    engaged_90_day=2500, engaged_180_day=3500),
            billing=BillingData(plan_tier="Standard", plan_profile_limit=50000),
        )
        cs = _score_billing(acct)
        self.assertLessEqual(cs.score, 8)

    def test_weight_is_2pct(self):
        cs = _score_billing(_make_acct())
        self.assertAlmostEqual(cs.weight, 0.02)


class TestCompositeScore(unittest.TestCase):
    def test_weights_sum_to_1(self):
        from src.scorer import WEIGHTS
        self.assertAlmostEqual(sum(WEIGHTS.values()), 1.0, places=10)

    def test_composite_within_0_100(self):
        acct = _make_acct()
        _, composite, _ = run_scoring(acct)
        self.assertGreaterEqual(composite, 0)
        self.assertLessEqual(composite, 100)

    def test_strong_account_scores_above_75(self):
        """Load the strong mock account and verify it scores Strong."""
        import json
        with open("mock_data/account_strong.json") as f:
            data = json.load(f)
        acct = AccountData.from_dict(data)
        _, composite, band = run_scoring(acct)
        self.assertGreaterEqual(composite, 75)
        self.assertEqual(band, "Strong")

    def test_critical_account_scores_below_40(self):
        import json
        with open("mock_data/account_critical.json") as f:
            data = json.load(f)
        acct = AccountData.from_dict(data)
        _, composite, band = run_scoring(acct)
        self.assertLess(composite, 40)
        self.assertEqual(band, "Critical")

    def test_ten_category_scores_returned(self):
        acct = _make_acct()
        scores, _, _ = run_scoring(acct)
        self.assertEqual(len(scores), 10)

    def test_all_scores_in_range_1_to_10(self):
        acct = _make_acct()
        scores, _, _ = run_scoring(acct)
        for cs in scores:
            self.assertGreaterEqual(cs.score, 1, f"{cs.name} score below 1")
            self.assertLessEqual(cs.score, 10, f"{cs.name} score above 10")

    def test_weighted_points_formula(self):
        acct = _make_acct()
        scores, composite, _ = run_scoring(acct)
        expected = round(sum(cs.weighted_points for cs in scores))
        self.assertEqual(composite, expected)


if __name__ == "__main__":
    unittest.main()
