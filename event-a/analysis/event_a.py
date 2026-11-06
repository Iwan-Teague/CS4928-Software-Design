"""Event A (P17 / G22): technical-only ranking vs the M2 urgency ordering.

Standard library only. Run from the repo root:

    python3 event-a/analysis/event_a.py

It reads the authors' survey export (work/export_jan_23_no_ip_no_email.csv),
applies the same row filters as the authors' notebook (analyse_experiment.Rmd),
and writes event-a/analysis/event_a_result.csv.

Filters copied from the notebook, in order:
  1. drop the two extra Qualtrics header rows,
  2. drop the pilot responses,
  3. keep Experience < 50 (this also drops rows where Experience is not a number).

Which variant a respondent saw (Table 3 of the paper, derive_sentiment() in the notebook):
  flow 1 -> vignettes 1 and 3 negative, 2 and 4 neutral
  flow 2 -> vignettes 2 and 4 negative, 1 and 3 neutral
"""

import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
DEFAULT_CSV = os.path.join(REPO, "work", "export_jan_23_no_ip_no_email.csv")
OUT_CSV = os.path.join(HERE, "event_a_result.csv")

VIGNETTES = (1, 2, 3, 4)

# ---------------------------------------------------------------------------
# Technical prioritisation rule (fixed before comparing with M2).
# Each vignette is judged only on its filtered, emotion-free text, using three
# yes/no criteria. The order of the criteria is the priority order:
#   correctness_risk : can the debt produce wrong behaviour/state in production?
#   design_violation : does it break a design principle (SRP, OCP) that raises
#                      the cost of every future change?
#   production_code  : does the debt sit in code that runs in production?
# Vignettes are ranked lexicographically on (correctness_risk, design_violation,
# production_code), highest first.
# ---------------------------------------------------------------------------
TECHNICAL_EVIDENCE = {
    1: dict(summary="Code used only for regression testing; remove it.",
            correctness_risk=False, design_violation=False, production_code=False),
    2: dict(summary="A value callback would be more efficient; cost is low.",
            correctness_risk=False, design_violation=False, production_code=True),
    3: dict(summary="ConstDecl should be split; constNode and name never in sync.",
            correctness_risk=True, design_violation=True, production_code=True),
    4: dict(summary="Plot-type code must be edited by hand for every new type.",
            correctness_risk=False, design_violation=True, production_code=True),
}


def technical_key(v):
    e = TECHNICAL_EVIDENCE[v]
    return (e["correctness_risk"], e["design_violation"], e["production_code"])


def technical_ranking():
    """Vignette ids, most urgent first, by the technical rule only."""
    ranked = sorted(VIGNETTES, key=technical_key, reverse=True)
    keys = [technical_key(v) for v in ranked]
    if len(set(keys)) != len(keys):
        raise ValueError("technical rule produces a tie; it must give a strict order")
    return ranked


# ---------------------------------------------------------------------------
# Survey data
# ---------------------------------------------------------------------------
def _num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def load_respondents(path=DEFAULT_CSV):
    """Return one dict per valid respondent: flow and Urgency-1..4."""
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    header, body = rows[0], rows[3:]  # rows 1-2 are extra Qualtrics headers
    col = {name: i for i, name in enumerate(header)}
    out = []
    for r in body:
        if r[col["Create New Field or Choose From Dropdown..."]] == "pilot":
            continue
        exp = _num(r[col["Experience"]])
        if exp is None or not exp < 50:
            continue
        out.append({
            "flow": int(_num(r[col["flow"]])),
            "urgency": {v: _num(r[col[f"Urgency-{v}"]]) for v in VIGNETTES},
        })
    return out


def is_negative(flow, vignette):
    """True if this respondent saw the negative variant of this vignette."""
    if flow == 1:
        return vignette in (1, 3)
    if flow == 2:
        return vignette in (2, 4)
    raise ValueError(f"unknown flow {flow}")


def _mean(xs):
    xs = [x for x in xs if x is not None]
    return sum(xs) / len(xs), len(xs)


def urgency_means(respondents, variant="all"):
    """Mean Urgency per vignette. variant: 'all', 'negative' or 'neutral'."""
    res = {}
    for v in VIGNETTES:
        vals = []
        for p in respondents:
            neg = is_negative(p["flow"], v)
            if variant == "all" or (variant == "negative") == neg:
                vals.append(p["urgency"][v])
        res[v] = _mean(vals)
    return res


def rank_by(means):
    return sorted(means, key=lambda v: means[v][0], reverse=True)


def rank_positions(order):
    return {v: i + 1 for i, v in enumerate(order)}


def main(path=DEFAULT_CSV):
    people = load_respondents(path)
    tech = technical_ranking()
    m_all = urgency_means(people, "all")
    m_neg = urgency_means(people, "negative")
    m_neu = urgency_means(people, "neutral")
    pos = {name: rank_positions(o) for name, o in [
        ("tech", tech), ("all", rank_by(m_all)),
        ("neg", rank_by(m_neg)), ("neu", rank_by(m_neu))]}

    fields = ["vignette", "technical_rank", "m2_rank_all", "mean_all", "n_all",
              "rank_negative", "mean_negative", "n_negative",
              "rank_neutral", "mean_neutral", "n_neutral", "negative_minus_neutral"]
    with open(OUT_CSV, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(fields)
        for v in VIGNETTES:
            w.writerow([v, pos["tech"][v], pos["all"][v], f"{m_all[v][0]:.3f}", m_all[v][1],
                        pos["neg"][v], f"{m_neg[v][0]:.3f}", m_neg[v][1],
                        pos["neu"][v], f"{m_neu[v][0]:.3f}", m_neu[v][1],
                        f"{m_neg[v][0] - m_neu[v][0]:+.3f}"])

    print(f"valid respondents: {len(people)}")
    print("technical ranking :", " > ".join(f"V{v}" for v in tech))
    for label, m in [("M2 mean, all     ", m_all), ("negative variant ", m_neg),
                     ("neutral variant  ", m_neu)]:
        print(label + ":", " > ".join(f"V{v} ({m[v][0]:.2f})" for v in rank_by(m)))
    print("negative - neutral:", ", ".join(
        f"V{v} {m_neg[v][0] - m_neu[v][0]:+.2f}" for v in VIGNETTES))
    print(f"wrote {os.path.relpath(OUT_CSV, REPO)}")


if __name__ == "__main__":
    main(*sys.argv[1:])
