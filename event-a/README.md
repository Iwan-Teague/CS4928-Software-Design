# Event A (P17, G22): technical-only ranking and Vignette 3 refactoring

Two parts, each with its own tests. Nothing here changes `original/`, `work/` or the M2 result.

## 1. `analysis/`: technical ranking vs the M2 ordering (Python 3, standard library only)

- `event_a.py` reads `work/export_jan_23_no_ip_no_email.csv` with the same filters as the authors'
  notebook (drop 2 Qualtrics header rows, drop pilots, Experience < 50 -> 59 respondents, 236 Urgency
  ratings). It defines the technical prioritisation rule (fixed before comparing with M2) and computes the
  per-vignette Urgency means: overall, and split by negative and neutral variant.
- Output: `analysis/event_a_result.csv`.
- Technical rule: lexicographic on (correctness risk, design-principle violation, production code), judged
  on the filtered vignette text only. It has no sentiment input.

Run from the repo root:

    python3 event-a/analysis/event_a.py
    python3 -m unittest discover -s event-a/analysis/tests -v      # 15 tests

Result:

| Vignette | Technical rank | M2 rank (mean, all) | Mean all (n=59) | Mean negative | Mean neutral | Neg - neu |
|---|---|---|---|---|---|---|
| V1 test-only code | 4 | 2 | 2.339 | 2.267 (n=30) | 2.414 (n=29) | -0.147 |
| V2 missing callback | 3 | 4 | 2.051 | 2.552 (n=29) | 1.567 (n=30) | +0.985 |
| V3 ConstDecl out of sync | 1 | 1 | 2.746 | 2.733 (n=30) | 2.759 (n=29) | -0.025 |
| V4 plot-type if/else | 2 | 3 | 2.322 | 2.379 (n=29) | 2.267 (n=30) | +0.113 |

Note: the overall mean mixes both variants. V1's high M2 rank does not come from its negative wording:
the negative V1 is rated lower than the neutral V1, and V1 ranks 2nd among neutral ratings as well.
The largest negative-minus-neutral gap is V2 (+0.99). Descriptive means only; this is not the M2 Bayesian model.

## 2. `design/`: Vignette 3 refactoring (Java 17, JUnit 5, Maven)

A bounded model of the Vignette 3 debt, reconstructed from the comment text. It is **not** the original
project's source code.

- `p17.v3.before.ConstDeclNode`: name stored twice (`name` field and inside `constNode`), nothing
  keeping them consistent.
- `p17.v3.after.ConstDeclNode`: same public methods, one source of truth (`constNode`); `getName()`
  is derived from it. No design pattern introduced; the class split from the FIXME is deferred.

Tests (`src/test/java/p17/v3`):

| Test class | Runs against | What it shows |
|---|---|---|
| `BeforeCharacterisationTest` / `AfterCharacterisationTest` | before / after | Same behaviour for consistent use: the refactoring changes no observable behaviour callers rely on. |
| `BeforeSyncBugTest` | before | Reproduces the defect: setConstNode/setName/constructor leave name and constNode out of sync; a seeded 1000-step random update sequence breaks the invariant (at step 7). |
| `AfterSyncInvariantTest` | after | The same scenarios keep name and constNode in sync; the same seeded sequence never breaks the invariant. 5 of its 6 tests fail if pointed at the before class. |

Run (needs JDK 17+ and Maven):

    cd event-a/design
    mvn test                       # 18 tests
