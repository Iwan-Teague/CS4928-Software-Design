"""Unit tests for wording_only_plan.py (post-hoc check added 2026-11-13). Run from the repo root:
    python3 -m unittest discover -s event-b/analysis/tests -v
They read the authors' survey export through the Event A loader, so they also guard the numbers quoted in EVENT-B.md.
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import wording_only_plan as w  # noqa: E402


class WordingOnlyTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.people = w.event_a.load_respondents()
        cls.effects = {r["vignette"]: r for r in w.wording_effects(cls.people)}
        cls.plans = {r["budget_units"]: r for r in w.sprint_plans(cls.people)}

    def test_sample_is_the_59_respondents_of_m2(self):
        self.assertEqual(len(self.people), 59)

    def test_v3_urgency_does_not_depend_on_wording(self):
        # The basis of the claim that the class split (R2) is pulled forward by ratings, not by wording.
        self.assertAlmostEqual(self.effects[3]["mean_negative"], 2.733, places=3)
        self.assertAlmostEqual(self.effects[3]["mean_neutral"], 2.759, places=3)
        self.assertLess(abs(self.effects[3]["negative_minus_neutral"]), 0.05)

    def test_v2_wording_effect_is_larger_than_the_smallest_detectable_difference(self):
        e = self.effects[2]
        self.assertAlmostEqual(e["negative_minus_neutral"], 0.985, places=3)
        self.assertGreater(abs(e["negative_minus_neutral"]), e["min_detectable_diff_80pct"])

    def test_v1_difference_is_far_below_the_smallest_detectable_difference(self):
        e = self.effects[1]
        self.assertAlmostEqual(e["negative_minus_neutral"], -0.147, places=3)
        self.assertLess(abs(e["negative_minus_neutral"]), 0.5 * e["min_detectable_diff_80pct"])
        self.assertAlmostEqual(e["min_detectable_diff_80pct"], 0.69, delta=0.01)

    def test_negative_and_neutral_plans_agree_where_event_b_claims_ratings_not_wording(self):
        # At 4, 6 and 8 units both rating-based plans give the same sprint (V4 left out at 4, R2 pulled forward at 6).
        for b in (4, 6, 8):
            self.assertEqual(set(self.plans[b]["negative_based"]), set(self.plans[b]["neutral_based"]), b)
        self.assertNotIn("V4", self.plans[4]["negative_based"])
        self.assertIn("V3-R2", self.plans[6]["negative_based"])
        self.assertIn("V3-R2", self.plans[6]["neutral_based"])

    def test_wording_only_difference_is_a_single_v1_v2_swap(self):
        for b in (3, 5, 7):
            self.assertEqual(w.wording_only_difference(self.plans[b]), ["V1", "V2"], b)
            self.assertIn("V2", self.plans[b]["negative_based"])
            self.assertIn("V1", self.plans[b]["neutral_based"])

    def test_at_the_five_unit_budget_negative_plan_selects_the_technical_set(self):
        self.assertEqual(set(self.plans[5]["negative_based"]), set(self.plans[5]["technical"]))


if __name__ == "__main__":
    unittest.main()
