"""Unit tests for event_b_plan.py. Run from the repo root:
    python3 -m unittest discover -s event-b/analysis/tests -v
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import event_b_plan as p  # noqa: E402


class PlanTest(unittest.TestCase):
    def test_defects_rank_first_under_the_technical_rule(self):
        self.assertEqual([it["id"] for it in p.technical_order()][:2], ["D1", "D2"])

    def test_technical_order_is_strict_and_matches_prediction(self):
        self.assertEqual([it["id"] for it in p.technical_order()], ["D1", "D2", "V4", "V3-R2", "V2", "V1"])

    def test_vignette_items_reuse_frozen_event_a_evidence(self):
        for it in p.ITEMS:
            if it["vignette"] in (1, 2, 4):
                e = p.event_a.TECHNICAL_EVIDENCE[it["vignette"]]
                for k in ("correctness_risk", "design_violation", "production_code"):
                    self.assertEqual(it[k], e[k], (it["id"], k))

    def test_greedy_respects_budget_and_skips_items_that_do_not_fit(self):
        taken, left = p.greedy(p.technical_order(), 5)
        self.assertEqual(taken, ["D1", "D2", "V4", "V2"])
        self.assertEqual(left, 0)
        self.assertNotIn("V3-R2", taken)  # L = 4 units never fits after the defects at budget 5

    def test_sentiment_order_uses_negative_variant_means_from_raw_data(self):
        people = p.event_a.load_respondents()
        neg = {v: m for v, (m, _n) in p.event_a.urgency_means(people, "negative").items()}
        self.assertEqual(len(people), 59)
        self.assertAlmostEqual(neg[2], 2.552, places=3)
        self.assertEqual([it["id"] for it in p.sentiment_order(neg)], ["D1", "D2", "V3-R2", "V2", "V4", "V1"])

    def test_budget_four_shows_the_sentiment_plan_dropping_v4(self):
        people = p.event_a.load_respondents()
        neg = {v: m for v, (m, _n) in p.event_a.urgency_means(people, "negative").items()}
        self.assertEqual(p.greedy(p.technical_order(), 4)[0], ["D1", "D2", "V4"])
        self.assertEqual(p.greedy(p.sentiment_order(neg), 4)[0], ["D1", "D2", "V2", "V1"])


if __name__ == "__main__":
    unittest.main()
