"""Tests for event_a.py. Run from the repo root:

    python3 -m unittest discover -s event-a/analysis/tests -v
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import event_a  # noqa: E402


class TestSampleMatchesM2(unittest.TestCase):
    """The filters must give the same 59-respondent sample as M1/M2."""

    @classmethod
    def setUpClass(cls):
        cls.people = event_a.load_respondents()

    def test_59_valid_respondents(self):
        self.assertEqual(len(self.people), 59)

    def test_236_urgency_ratings(self):
        n = sum(1 for p in self.people for v in event_a.VIGNETTES
                if p["urgency"][v] is not None)
        self.assertEqual(n, 236)

    def test_flow_split(self):
        flows = [p["flow"] for p in self.people]
        self.assertEqual(flows.count(1), 30)
        self.assertEqual(flows.count(2), 29)

    def test_every_respondent_sees_two_negative_and_two_neutral(self):
        for flow in (1, 2):
            negs = [v for v in event_a.VIGNETTES if event_a.is_negative(flow, v)]
            self.assertEqual(len(negs), 2)


class TestTechnicalRule(unittest.TestCase):
    """The technical rule uses only the filtered text and gives a strict order."""

    def test_ranking(self):
        self.assertEqual(event_a.technical_ranking(), [3, 4, 2, 1])

    def test_rule_has_no_ties(self):
        keys = [event_a.technical_key(v) for v in event_a.VIGNETTES]
        self.assertEqual(len(set(keys)), 4)

    def test_rule_ignores_sentiment(self):
        # The evidence table holds no sentiment field, so wording cannot affect the rank.
        for e in event_a.TECHNICAL_EVIDENCE.values():
            self.assertEqual(set(e) - {"summary"},
                             {"correctness_risk", "design_violation", "production_code"})


class TestM2Ordering(unittest.TestCase):
    """Reproduces the per-vignette urgency means reported in the Event A write-up."""

    @classmethod
    def setUpClass(cls):
        people = event_a.load_respondents()
        cls.all = event_a.urgency_means(people, "all")
        cls.neg = event_a.urgency_means(people, "negative")
        cls.neu = event_a.urgency_means(people, "neutral")

    def test_reported_means(self):
        expected = {1: 2.34, 2: 2.05, 3: 2.75, 4: 2.32}
        for v, m in expected.items():
            self.assertAlmostEqual(self.all[v][0], m, places=2)
            self.assertEqual(self.all[v][1], 59)

    def test_m2_ranking(self):
        self.assertEqual(event_a.rank_by(self.all), [3, 1, 4, 2])

    def test_v3_top_in_both_rankings(self):
        self.assertEqual(event_a.technical_ranking()[0], 3)
        self.assertEqual(event_a.rank_by(self.all)[0], 3)

    def test_v1_is_where_the_rankings_disagree_most(self):
        tech = event_a.rank_positions(event_a.technical_ranking())
        m2 = event_a.rank_positions(event_a.rank_by(self.all))
        gaps = {v: tech[v] - m2[v] for v in event_a.VIGNETTES}
        self.assertEqual(max(gaps, key=gaps.get), 1)
        self.assertEqual(gaps[1], 2)  # technical #4, M2 #2

    def test_variant_counts(self):
        # Each vignette is seen negative by one flow group and neutral by the other.
        for v in event_a.VIGNETTES:
            self.assertEqual(self.neg[v][1] + self.neu[v][1], 59)

    # Facts about the split by variant. These limit how the V1 result can be read.
    def test_v1_negative_variant_is_not_rated_more_urgent(self):
        self.assertLess(self.neg[1][0], self.neu[1][0])

    def test_v1_ranks_second_even_among_neutral_ratings(self):
        self.assertEqual(event_a.rank_by(self.neu)[1], 1)

    def test_v2_has_the_largest_negative_minus_neutral_gap(self):
        diff = {v: self.neg[v][0] - self.neu[v][0] for v in event_a.VIGNETTES}
        self.assertEqual(max(diff, key=diff.get), 2)
        self.assertGreater(diff[2], 0.9)


if __name__ == "__main__":
    unittest.main()
