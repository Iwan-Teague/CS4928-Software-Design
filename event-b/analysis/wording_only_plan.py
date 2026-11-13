"""Event B (P17 / G22): post-hoc check that separates the effect of WORDING from the effect of RATINGS.

Added on 2026-11-13, after the Event B results were known. It is NOT part of the prediction frozen at tag
EVENT_B_PREDICTION and it does not change any frozen output (event_a_result.csv, event_b_plan.csv,
event_b_budget_sensitivity.csv are untouched).

Standard library only. Run from the repo root:

    python3 event-b/analysis/wording_only_plan.py

Question: event_b_plan.py compares our technical plan with a plan ordered by the NEGATIVE-variant Urgency means.
Any difference between those two plans mixes two causes: (a) developers' ratings differ from our technical rule,
and (b) the negative wording itself. To isolate (b), this script orders the same plan by the NEUTRAL-variant means
and compares the two rating-based plans with each other. Differences between them are wording effects only.

Writes event-b/analysis/event_b_wording_effects.csv (per vignette: means, SDs, n, difference, smallest
difference this sample could reliably detect) and event-b/analysis/event_b_wording_only_plan.csv (sprint sets at
3 to 8 units for the technical, negative-based and neutral-based plans).

Smallest detectable difference = (1.96 + 0.8416) * sqrt(sd_neg^2/n_neg + sd_neu^2/n_neu): two-sided 5% level,
80% power, normal approximation. It is a planning figure, not a test result.
"""

import csv
import math
import os
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, "event-a", "analysis"))
sys.path.insert(0, HERE)
import event_a  # noqa: E402
import event_b_plan as plan  # noqa: E402

Z_ALPHA_2SIDED = 1.96
Z_POWER_80 = 0.8416


def split_ratings(people, vignette):
    """Urgency ratings for one vignette: (negative-variant list, neutral-variant list)."""
    neg, neu = [], []
    for p in people:
        value = p["urgency"][vignette]
        if value is None:
            continue
        (neg if event_a.is_negative(p["flow"], vignette) else neu).append(value)
    return neg, neu


def wording_effects(people):
    """One dict per vignette: negative and neutral mean/SD/n, difference, smallest reliably detectable difference."""
    rows = []
    for v in event_a.VIGNETTES:
        neg, neu = split_ratings(people, v)
        se = math.sqrt(statistics.variance(neg) / len(neg) + statistics.variance(neu) / len(neu))
        rows.append(dict(
            vignette=v,
            n_negative=len(neg), mean_negative=statistics.mean(neg), sd_negative=statistics.stdev(neg),
            n_neutral=len(neu), mean_neutral=statistics.mean(neu), sd_neutral=statistics.stdev(neu),
            negative_minus_neutral=statistics.mean(neg) - statistics.mean(neu),
            min_detectable_diff_80pct=(Z_ALPHA_2SIDED + Z_POWER_80) * se,
        ))
    return rows


def sprint_plans(people, budgets=range(3, 9)):
    """For each budget: technical sprint, negative-based sprint, neutral-based sprint (lists of item ids)."""
    neg = {v: m for v, (m, _n) in event_a.urgency_means(people, "negative").items()}
    neu = {v: m for v, (m, _n) in event_a.urgency_means(people, "neutral").items()}
    tech_order = plan.technical_order()
    neg_order = plan.sentiment_order(neg)
    neu_order = plan.sentiment_order(neu)
    rows = []
    for b in budgets:
        t, _ = plan.greedy(tech_order, b)
        n, _ = plan.greedy(neg_order, b)
        u, _ = plan.greedy(neu_order, b)
        rows.append(dict(budget_units=b, technical=t, negative_based=n, neutral_based=u))
    return rows


def wording_only_difference(row):
    """Items in exactly one of the negative-based and neutral-based sprints: the wording-only difference."""
    return sorted(set(row["negative_based"]) ^ set(row["neutral_based"]))


def main(csv_path=event_a.DEFAULT_CSV):
    people = event_a.load_respondents(csv_path)
    effects = wording_effects(people)
    plans = sprint_plans(people)

    with open(os.path.join(HERE, "event_b_wording_effects.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["vignette", "n_negative", "mean_negative", "sd_negative", "n_neutral", "mean_neutral",
                    "sd_neutral", "negative_minus_neutral", "min_detectable_diff_80pct"])
        for r in effects:
            w.writerow([r["vignette"], r["n_negative"], f"{r['mean_negative']:.3f}", f"{r['sd_negative']:.2f}",
                        r["n_neutral"], f"{r['mean_neutral']:.3f}", f"{r['sd_neutral']:.2f}",
                        f"{r['negative_minus_neutral']:+.3f}", f"{r['min_detectable_diff_80pct']:.2f}"])

    with open(os.path.join(HERE, "event_b_wording_only_plan.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["budget_units", "technical_sprint", "negative_based_sprint", "neutral_based_sprint",
                    "wording_only_difference"])
        for r in plans:
            w.writerow([r["budget_units"], "+".join(r["technical"]), "+".join(r["negative_based"]),
                        "+".join(r["neutral_based"]), "+".join(wording_only_difference(r)) or "none"])

    print(f"valid respondents: {len(people)}")
    print("vignette | negative mean (sd, n) | neutral mean (sd, n) | diff | smallest reliably detectable diff")
    for r in effects:
        print(f"  V{r['vignette']}     | {r['mean_negative']:.3f} ({r['sd_negative']:.2f}, {r['n_negative']}) | "
              f"{r['mean_neutral']:.3f} ({r['sd_neutral']:.2f}, {r['n_neutral']}) | "
              f"{r['negative_minus_neutral']:+.3f} | {r['min_detectable_diff_80pct']:.2f}")
    print("budget | technical | negative-based | neutral-based | wording-only difference")
    for r in plans:
        print(f"  {r['budget_units']}    | {'+'.join(r['technical'])} | {'+'.join(r['negative_based'])} | "
              f"{'+'.join(r['neutral_based'])} | {'+'.join(wording_only_difference(r)) or 'none'}")


if __name__ == "__main__":
    main(*sys.argv[1:])
