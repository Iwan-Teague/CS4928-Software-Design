"""Event B (P17 / G22): reprioritise the remaining debt under a fixed one-sprint budget.

Standard library only. Run from the repo root:

    python3 event-b/analysis/event_b_plan.py

Inputs fixed in event-b/PREDICTION.md (tag EVENT_B_PREDICTION) before this script was written:
- technical rule: the frozen Event A rule (correctness risk, design violation, production code), highest first;
  ties broken by smaller size, then item id;
- sizes: ordinal estimates S=1, M=2, L=4 units (D1 and D2 measured after the fix: both S);
- budget: 5 units per sprint, greedy (take an item if it still fits), sensitivity 3..8 units;
- sentiment counterfactual: defects first, then debt items by the M2 Urgency mean of the NEGATIVE variant,
  computed from the raw survey export with the Event A script's filters.

Writes event-b/analysis/event_b_plan.csv and event-b/analysis/event_b_budget_sensitivity.csv.
"""

import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, "event-a", "analysis"))
import event_a  # noqa: E402  (frozen Event A rule and survey loader)

BUDGET = 5
SIZE_UNITS = {"S": 1, "M": 2, "L": 4}

# Same three yes/no criteria as event_a.TECHNICAL_EVIDENCE, applied to the Event B backlog.
# 'vignette' links a debt item to its survey ratings (None for the two new defects).
ITEMS = [
    dict(id="D1", vignette=None, size="S",
         summary="V2 call site: getConstNode() is null for FOO = 1, value pass throws NPE",
         correctness_risk=True, design_violation=False, production_code=True),
    dict(id="D2", vignette=None, size="S",
         summary="ConstPath accepts '::' or blank parts; name/path invariant breaks again",
         correctness_risk=True, design_violation=False, production_code=True),
    dict(id="V3-R2", vignette=3, size="L",
         summary="Split ConstDecl into simple/scoped classes (FIXME's full suggestion)",
         correctness_risk=False, design_violation=True, production_code=True),
    dict(id="V4", vignette=4, size="M",
         summary="Plot-type if/else chain edited by hand for every new type (OCP)",
         correctness_risk=False, design_violation=True, production_code=True),
    dict(id="V2", vignette=2, size="S",
         summary="Value callback would be more efficient; cost stated as low",
         correctness_risk=False, design_violation=False, production_code=True),
    dict(id="V1", vignette=1, size="S",
         summary="Regression-testing-only flags; remove",
         correctness_risk=False, design_violation=False, production_code=False),
]

# Sanity: the vignette items carry exactly the Event A evidence (V3's correctness risk was removed by R1 in Week 9).
for it in ITEMS:
    v = it["vignette"]
    if v in (1, 2, 4):
        e = event_a.TECHNICAL_EVIDENCE[v]
        assert all(it[k] == e[k] for k in ("correctness_risk", "design_violation", "production_code")), it["id"]


def units(item):
    return SIZE_UNITS[item["size"]]


def technical_order(items=ITEMS):
    def key(it):
        return (-it["correctness_risk"], -it["design_violation"], -it["production_code"], units(it), it["id"])
    return sorted(items, key=key)


def sentiment_order(neg_means, items=ITEMS):
    defects = [it for it in items if it["vignette"] is None]
    debt = [it for it in items if it["vignette"] is not None]
    defects.sort(key=lambda it: it["id"])
    debt.sort(key=lambda it: (-neg_means[it["vignette"]], it["id"]))
    return defects + debt


def greedy(order, budget):
    left, taken = budget, []
    for it in order:
        if units(it) <= left:
            taken.append(it["id"])
            left -= units(it)
    return taken, left


def main(csv_path=event_a.DEFAULT_CSV):
    people = event_a.load_respondents(csv_path)
    neg = {v: m for v, (m, _n) in event_a.urgency_means(people, "negative").items()}
    tech, sent = technical_order(), sentiment_order(neg)
    t_taken, t_left = greedy(tech, BUDGET)
    s_taken, s_left = greedy(sent, BUDGET)
    tpos = {it["id"]: i + 1 for i, it in enumerate(tech)}
    spos = {it["id"]: i + 1 for i, it in enumerate(sent)}

    with open(os.path.join(HERE, "event_b_plan.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["item", "summary", "correctness_risk", "design_violation", "production_code", "size", "units",
                    "negative_variant_urgency", "technical_rank", "in_technical_sprint",
                    "sentiment_rank", "in_sentiment_sprint"])
        for it in ITEMS:
            v = it["vignette"]
            w.writerow([it["id"], it["summary"], int(it["correctness_risk"]), int(it["design_violation"]),
                        int(it["production_code"]), it["size"], units(it),
                        "" if v is None else f"{neg[v]:.3f}",
                        tpos[it["id"]], int(it["id"] in t_taken), spos[it["id"]], int(it["id"] in s_taken)])

    rows = []
    for b in range(3, 9):
        tt, _ = greedy(tech, b)
        ss, _ = greedy(sent, b)
        rows.append((b, "+".join(tt), "+".join(ss), int(set(tt) != set(ss))))
    with open(os.path.join(HERE, "event_b_budget_sensitivity.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["budget_units", "technical_sprint", "sentiment_sprint", "sets_differ"])
        w.writerows(rows)

    print(f"valid respondents: {len(people)}")
    print("negative-variant Urgency means:", ", ".join(f"V{v} {neg[v]:.3f}" for v in sorted(neg)))
    print("technical order :", " > ".join(it["id"] for it in tech))
    print("sentiment order :", " > ".join(it["id"] for it in sent))
    print(f"sprint ({BUDGET} units), technical: {' + '.join(t_taken)} (left {t_left})")
    print(f"sprint ({BUDGET} units), sentiment: {' + '.join(s_taken)} (left {s_left})")
    for b, tt, ss, d in rows:
        print(f"  budget {b}: technical {tt:<22} sentiment {ss:<22} {'DIFFERENT SET' if d else 'same set'}")


if __name__ == "__main__":
    main(*sys.argv[1:])
