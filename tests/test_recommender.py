"""Unit tests for src/recommender.py — deduplication, merge groups, and priority ordering."""
import unittest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.models import Finding
from src.recommender import build_recommendations, _canonical_rule_id, _MERGE_GROUPS


def _finding(rule_id: str, severity: str = "High", confidence: str = "Confirmed") -> Finding:
    return Finding(
        rule_id=rule_id, severity=severity,
        category="Test", description="Test finding",
        business_impact="Impact", recommended_action="Action",
        priority=severity, confidence=confidence,
    )


class TestCanonicalRuleId(unittest.TestCase):
    def test_non_merged_returns_self(self):
        self.assertEqual(_canonical_rule_id("FLOW-001"), "FLOW-001")
        self.assertEqual(_canonical_rule_id("SMS-001"), "SMS-001")
        self.assertEqual(_canonical_rule_id("CAMP-001"), "CAMP-001")

    def test_merge_group_members_map_to_canonical(self):
        # Auth group: DELV-005, DELV-006, DELV-007, DELV-008 → DELV-005
        self.assertEqual(_canonical_rule_id("DELV-006"), _canonical_rule_id("DELV-005"))
        self.assertEqual(_canonical_rule_id("DELV-007"), _canonical_rule_id("DELV-005"))
        self.assertEqual(_canonical_rule_id("DELV-008"), _canonical_rule_id("DELV-005"))

    def test_campaign_seg_group_merges(self):
        self.assertEqual(_canonical_rule_id("CAMP-004"), _canonical_rule_id("CAMP-003"))

    def test_sms_growth_group_merges(self):
        self.assertEqual(_canonical_rule_id("SMS-003"), _canonical_rule_id("SMS-002"))


class TestDeduplication(unittest.TestCase):
    def test_same_rule_id_not_duplicated(self):
        findings = [_finding("FLOW-001"), _finding("FLOW-001")]
        recs = build_recommendations(findings)
        rec_ids = [r.rec_id for r in recs]
        self.assertEqual(len(rec_ids), len(set(rec_ids)), "Duplicate rec_ids found")

    def test_merged_rules_produce_single_recommendation(self):
        findings = [
            _finding("DELV-005"),
            _finding("DELV-006"),
            _finding("DELV-007"),
            _finding("DELV-008"),
        ]
        recs = build_recommendations(findings)
        delv_recs = [r for r in recs if "DELV" in r.rec_id]
        self.assertEqual(len(delv_recs), 1, f"Expected 1 DELV rec, got {len(delv_recs)}")

    def test_merged_rec_lists_all_source_rules(self):
        findings = [_finding("DELV-005"), _finding("DELV-007")]
        recs = build_recommendations(findings)
        delv_recs = [r for r in recs if "DELV" in r.rec_id]
        self.assertTrue(delv_recs)
        source_rules = delv_recs[0].source_rules
        self.assertIn("DELV-005", source_rules)
        self.assertIn("DELV-007", source_rules)


class TestPriorityOrdering(unittest.TestCase):
    def test_recommendations_sorted_by_priority_score_descending(self):
        findings = [
            _finding("FLOW-001", "Critical"),
            _finding("CAMP-001", "High"),
            _finding("FLOW-009", "Medium"),
        ]
        recs = build_recommendations(findings)
        for i in range(len(recs) - 1):
            self.assertGreaterEqual(
                recs[i].priority_score, recs[i + 1].priority_score,
                f"Rec {recs[i].rec_id} (score {recs[i].priority_score}) should come before "
                f"{recs[i+1].rec_id} (score {recs[i+1].priority_score})",
            )

    def test_critical_finding_generates_recommendation(self):
        findings = [_finding("FLOW-001", "Critical")]
        recs = build_recommendations(findings)
        self.assertTrue(recs, "Expected at least one recommendation from FLOW-001")

    def test_unknown_rule_id_produces_no_recommendation(self):
        findings = [_finding("UNKNOWN-999")]
        recs = build_recommendations(findings)
        self.assertEqual(recs, [])

    def test_empty_findings_produces_no_recommendations(self):
        self.assertEqual(build_recommendations([]), [])


class TestConfidence(unittest.TestCase):
    def test_confirmed_finding_yields_confirmed_rec(self):
        findings = [_finding("FLOW-001", confidence="Confirmed")]
        recs = build_recommendations(findings)
        self.assertTrue(recs)
        self.assertEqual(recs[0].confidence, "Confirmed")

    def test_inferred_finding_yields_inferred_rec(self):
        findings = [_finding("FLOW-001", confidence="Inferred")]
        recs = build_recommendations(findings)
        self.assertTrue(recs)
        self.assertEqual(recs[0].confidence, "Inferred")


class TestRecommendationFields(unittest.TestCase):
    def test_all_required_fields_populated(self):
        findings = [_finding("FLOW-004", "Critical")]
        recs = build_recommendations(findings)
        self.assertTrue(recs)
        r = recs[0]
        self.assertTrue(r.rec_id)
        self.assertTrue(r.issue)
        self.assertTrue(r.why_it_matters)
        self.assertIn(r.expected_impact, ("High", "Medium", "Low"))
        self.assertIn(r.complexity, ("Easy", "Moderate", "Complex"))
        self.assertIn(r.priority, ("Critical", "High", "Medium", "Low"))
        self.assertIn(r.owner, ("NP", "Client", "Shared"))
        self.assertTrue(r.next_step)
        self.assertTrue(r.opportunity_note)
        self.assertGreater(r.priority_score, 0)


if __name__ == "__main__":
    unittest.main()
