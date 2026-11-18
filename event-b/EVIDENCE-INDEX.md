# Evidence index for the Event B response (P17, G22)

Links every claim in [`EVENT-B.md`](EVENT-B.md) to the file, commit, tag or command that supports it.
Status: **R** = re-run it and compare; **F** = a file, commit or tag you can open; **J** = our judgement, with the
reasoning shown in the linked file; **P** = depends on the published paper (not stored in this repository).

Paper: Cassee et al., "Negativity in self-admitted technical debt: how sentiment influences prioritization",
Empirical Software Engineering (2025), https://link.springer.com/article/10.1007/s10664-024-10611-z.
Authors' data package: figshare article 26863435 (`ACCESSED.txt` holds the access date and the sha256 of the zip).

## Re-run everything (repository root)

```
python3 event-a/analysis/event_a.py                      # writes event-a/analysis/event_a_result.csv
python3 event-b/analysis/event_b_plan.py                 # writes event_b_plan.csv, event_b_budget_sensitivity.csv
python3 event-b/analysis/wording_only_plan.py            # writes event_b_wording_effects.csv, event_b_wording_only_plan.csv
python3 -m unittest discover -s event-b/analysis/tests   # 13 tests
(cd event-a/analysis && python3 -m unittest tests.test_event_a)   # 15 tests
(cd event-a/design && mvn test)                          # 25 tests
```

The three scripts rewrite their CSV files; `git diff` should then show no change.

## 1. Starting point and prediction

| # | Claim | Evidence | Status |
|---|---|---|---|
| 1 | Event B starts from tag `PRE_EVENT_B` | `git rev-parse PRE_EVENT_B^{commit}` = `f1d8b89`; the tag is in this repository (`git tag -l PRE_EVENT_B`) | F |
| 2 | The Week 9 design is the Vignette 3 refactoring first built for Event A (`3eb0d4a`) and recorded as M4 (`18f6ff7`); no code or test changed between them | `git diff --stat 3eb0d4a PRE_EVENT_B -- event-a/design event-a/analysis` prints nothing; `git show --stat 18f6ff7` lists only `M4-DESIGN.md`; `AI_USE.md` rows dated 2026-11-06 | R / F |
| 3 | The prediction was committed and tagged before the tests and the fix | Tag `EVENT_B_PREDICTION` = `fab93f0`; the test commit `9fe8adb` and the fix commit `874c055` come after it in history (`git log --format='%h %ad %s' --date=iso EVENT_B_PREDICTION..EVENT_B`) | F |
| 4 | The first version of this response is tag `EVENT_B` (`874c055`); code, tests and evidence files from that tag are unchanged | `git diff --stat EVENT_B HEAD` lists only `event-b/EVENT-B.md` (reworded on 13 November), `README.md`, `AI_USE.md` (13 November entries), the files added on 13 November (`wording_only_plan.py`, its tests, two CSVs, `EVIDENCE-INDEX.md`, `mvn-test-2026-11-13.txt`, `EVENT-A-STATUS.md`), an unrelated PDF, and Minh's RQ2 files (`RQ2_results/`, five data files and `analyse_experiment_minh.Rmd`, brought in by the 12 November merge), and, added on 18 November, the RQ2 rerun and notes (`RESULT.md`, `DEVIATIONS.md`, `run_seeds_rq2.sh`, `work/rq2-s20261013/`, `work/rq2-seed-1/` to `-3/`, `work/seeds-status-rq2.txt`) and the dated local-branch notes in `EVENT-A-PLAN-DRAFT.md`; nothing under `event-a/design` or `event-a/analysis` changed since `EVENT_B` (`git diff --stat EVENT_B HEAD -- event-a/design event-a/analysis` prints nothing) | R |
| 5 | The task sheet does not name the two defects, so we defined them | Event B task sheet for P17 (Brightspace, Event B folder): "two new defects affecting the same area" | F (external) |
| 6 | `ConstDeclNode` is the class discussed in Vignettes 2 and 3 | Paper Table 2 | P |
| 7 | Our four predictions | `event-b/PREDICTION.md` at tag `EVENT_B_PREDICTION` (`git show EVENT_B_PREDICTION:event-b/PREDICTION.md`). The file here is identical to the tag: `git diff EVENT_B_PREDICTION HEAD -- event-b/PREDICTION.md` prints nothing | R |

## 2. The two defects and the options

| # | Claim | Evidence | Status |
|---|---|---|---|
| 8 | D1: for `FOO = 1`, `getConstNode()` returns `null`, deliberately kept in Week 9 | `git show PRE_EVENT_B:event-a/design/src/main/java/p17/v3/after/ConstDeclNode.java`, comment "Returns null for a simple declaration, exactly as before, so callers are unaffected" | F |
| 9 | D1 crashes with a `NullPointerException` on the unfixed code | Test `d1SimpleDeclarationIsAssigned` FAILED with `NullPointerException` in `evidence/defects-before-fix.txt` | F |
| 10 | D2: `ConstPath` accepted `::` and blank parts, and two different paths printed the same | Tests `d2ConstructorRejectsSeparatorInName`, `d2SetNameRejectsSeparator`, `d2ScopeSegmentWithSeparatorRejected`, `d2BlankScopeSegmentRejected` FAILED in `evidence/defects-before-fix.txt`; source `event-a/design/src/test/java/p17/v2/EventBDefectTest.java` | F |
| 11 | Option B0 (checks at every caller) is rejected because every caller must remember | Reasoning; the same argument for setters is in `M4-DESIGN.md`, option R0 ("every future setter must remember to check") | J |
| 12 | Option B1 chosen: validation in `ConstPath` (+3 lines), new `path()` and deprecated `getConstNode()` (+11/−1), V2 caller uses `path()` (new 31-line class) | `git diff --stat PRE_EVENT_B EVENT_B -- event-a/design/src/main` (3 files, +45/−1); `git show EVENT_B:event-a/design/src/main/java/p17/v3/after/ConstDeclNode.java` | R |
| 13 | Invalid inputs now throw `IllegalArgumentException` | The four `d2…Rejected` tests pass in `evidence/tests-after-fix.txt` | F |
| 14 | Option B2 (split the class) would use about 4 of 5 units and is deferred again | Item `V3-R2`, size L = 4 units, in `analysis/event_b_plan.csv`; sizes are estimates (`PREDICTION.md`, "Planning inputs") | J |
| 15 | The split was the Week 9 option R2 | `M4-DESIGN.md`, option R2 | F |

## 3. Implementation and testing

| # | Claim | Evidence | Status |
|---|---|---|---|
| 16 | Before the fix: 18 old + 7 new tests, 20 pass, 5 fail | `evidence/defects-before-fix.txt` ("25 tests found", "20 tests successful", "5 tests failed") | F |
| 17 | After the fix: all 25 pass | `evidence/tests-after-fix.txt` (25 successful, 0 failed); `evidence/mvn-test-2026-11-13.txt` (Maven, `Tests run: 25, Failures: 0, Errors: 0`) | F / R |
| 18 | None of the original 18 tests was changed | `git diff PRE_EVENT_B HEAD -- event-a/design/src/test` shows one new file only, `EventBDefectTest.java` | R |
| 19 | Python tests: 15 (Event A), 6 (Event B planner), 7 (wording check) | The commands at the top of this file | R |

## 4. Reprioritising the debt

| # | Claim | Evidence | Status |
|---|---|---|---|
| 20 | Technical rule: correctness risk, then design violation, then production code; ties by size, then id | `event-a/analysis/event_a.py` (`TECHNICAL_EVIDENCE`, `technical_key`), `event-a/README.md`, `event-b/analysis/event_b_plan.py` (`technical_order`) | R |
| 21 | The yes/no values per item (for example V4 breaks the open-closed principle) | The same files; they are our judgement on the filtered vignette text, with no sentiment input | J |
| 22 | Sizes S = 1, M = 2, L = 4 units; sprint = 5 units; sensitivity 3 to 8 | `PREDICTION.md` ("Planning inputs"); estimates, not measurements | J |
| 23 | Plan table and the 5-unit sprints (technical D1+D2+V4+V2; negative-based D1+D2+V2+V4) | `analysis/event_b_plan.csv`, `evidence/plan-output.txt` | R |
| 24 | Negative-variant means V1 2.267, V2 2.552, V3 2.733, V4 2.379 | `event-a/analysis/event_a_result.csv`, column `mean_negative` | R |
| 25 | Plans at 3 to 8 units | `analysis/event_b_budget_sensitivity.csv` | R |
| 26 | Ordering the same plan by the neutral means leaves V4 out at 4 units and pulls R2 forward at 6 units; the only wording-only differences are V2 instead of V1 at 3, 5 and 7 units | `analysis/event_b_wording_only_plan.csv`; tests in `analysis/tests/test_wording_only.py`. Added after the results were known and not part of the prediction | R |
| 27 | Survey data: the authors' export, 59 respondents after the authors' filters | `event-a/analysis/event_a.py` (docstring lists the filters, copied from the authors' notebook); data in `work/`; `ACCESSED.txt` | R |
| 28 | Which respondents saw the negative variant (flow 1: V1 and V3; flow 2: V2 and V4) | `event_a.py` docstring; paper Table 3 and the authors' `derive_sentiment()` | P |

## 5. Wording

| # | Claim | Evidence | Status |
|---|---|---|---|
| 29 | Week 9 quoted "never in sync" | `M4-DESIGN.md` (quoted comment); the comment in `event-a/design/src/main/java/p17/v3/before/ConstDeclNode.java` | F |
| 30 | The paper's original V3 comment is neutral; "never in sync" is the ChatGPT-generated negative variant | Paper Table 2, p. 8 (`AI_USE.md`: checked 2026-11-12) | P |
| 31 | The negative V2 text contains "This is frustrating!" | Paper Table 2 | P |
| 32 | V2: negative 2.552, neutral 1.567, difference +0.985, the largest in the data | `event-a/analysis/event_a_result.csv` (`negative_minus_neutral`); `analysis/event_b_wording_effects.csv` | R |
| 33 | V2 is mainly an efficiency item and V4 a design violation | `event_a.py`, `TECHNICAL_EVIDENCE` | J |
| 34 | V3 is rated 2.733 (negative) and 2.759 (neutral), so ratings, not wording, drive R2 forward | `event_a_result.csv`; `analysis/event_b_wording_effects.csv`; item 26 | R |
| 35 | A ratings-led plan would spend 4 of its 6 units on R2 | R2 = 4 units (`event_b_plan.csv`); the 6-unit sprint D1+D2+V3-R2 is in `event_b_wording_only_plan.csv` | R |
| 36 | V1: 2.267 (n = 30) against 2.414 (n = 29), difference −0.15; only differences of about 0.7 or more could be detected; V1 led V4 in M2 by 0.017 (2.339 against 2.322) | `event_a_result.csv`; `analysis/event_b_wording_effects.csv` (`min_detectable_diff_80pct`, formula in `wording_only_plan.py`) | R |
| 37 | The Event A and M4 tracker entries say wording made V1 more urgent | Frozen tracker record, group G22 (Brightspace, "Students Event A and M4 Frozen") | F (external) |

## 6. Conclusion

| # | Claim | Evidence | Status |
|---|---|---|---|
| 38 | "Partly supported" follows the decision rule fixed before the work | `git show EVENT_B_PREDICTION:event-b/PREDICTION.md`, section "Decision rule for the Week 9 decision" | F |
| 39 | Reason 1: part of the Week 9 justification rested on the negative wording of V3 | Items 29 and 30 | P |
| 40 | Reason 2: the Week 9 compatibility shim (`getConstNode()` returns `null`) caused D1 | Items 8 and 9 | F |
| 41 | Remaining: `path()` and `getConstNode()` both exist; old callers still get `null`; R2 stays on the backlog | `git show EVENT_B:event-a/design/src/main/java/p17/v3/after/ConstDeclNode.java`; item `V3-R2` in `event_b_plan.csv` | F |

## What is judgement or paper-dependent

- **J (items 11, 14, 21, 22, 33):** our reasoning, estimates and yes/no codings. The reasoning is in the linked files; none is a measurement.
- **P (items 6, 28, 30, 31, 39):** these rest on the paper, which is not stored in this repository. Check them against the paper before relying on them.
- Not claimed anywhere: that wording changed V1's urgency, that the Event B defects exist in the original project's code (they are defined for our bounded model), or that the technical ranking is an independent standard.
