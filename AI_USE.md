# AI use: G22 / P17 (brief material contributions only)

Per the project brief, this records only AI contributions that affected an engineering or research decision.
No prompt logs. AI output is not evidence; the evidence is the data, the computation and the checks listed against each entry.
Entries are grouped by project stage: M1, M2, RQ2, Event A, M4, Event B, Final.

## M1: plan and research questions (Week 5)

| Date | What the AI did | Decision it affected | How it was checked |
|---|---|---|---|
| 2026-09-25 | Early AI discussion helped iron out the RQ1 scope options; the group picked straight reproduction with a fixed seed | The group's RQ1 direction at M1 | Scope checked against the project pack and the paper before the M1 freeze |
| 2026-09-25 to 10-01 | Helped tighten the wording of RQ1 and RQ2 (Q9 grouping; swapping Q9 for Q8) and the "reproduced if" / "different if" decision rules | Wording of the frozen M1 entry. The thresholds (Agree OR 1.85-2.05; OR move > 0.3 or a changed evidence rating) and the expected ORs were set by the group from the paper | Expected ORs and the 22/11/26 Q9 split checked against the paper and the CSV; M1 entry frozen in the Student Tracker before any run |
| 2026-10-21 | Helped structure and proofread `Our M1 Plan and Reproduction Results.pdf` from the frozen M1 entry and `RESULT.md` | Presentation of the M1 plan and M2 result | Every number in the PDF taken from `RESULT.md`, which is recomputed from raw files (M2 below) |

## M2: bounded reproduction of RQ1 (tags `M1_PLAN`, `M2_REPRO`, `PRE_EVENT_A`)

| Date | What the AI did | Decision it affected | How it was checked |
|---|---|---|---|
| 2026-10-13 | Diagnosed the failed Docker build (`The package 'remotes' is required`) and proposed adding `RUN install2.r -e remotes` before the cmdstanr step | Deviation 1 in `DEVIATIONS.md` | Build log of the failed attempt (`build-attempt1-failed.log`) and of the fixed build (`build.log`); rest of the image unchanged |
| 2026-10-13 | Proposed the seeded Urgency-only copy of the notebook (`work/analyse_urgency_seeded.Rmd`): fixed seed, Urgency loop only, save numeric evidence ratios | Deviations 2-4; the seed was fixed before any result was seen | `diff` against `original/analyse_experiment.Rmd`; 236 = 59 x 4 rows confirmed from the rendered notebook; Q9 split (22/11/26) recounted independently from the CSV |
| 2026-10-13 | Wrote the OR from the saved contrast files (P(contrast > 0) / P(contrast < 0)) as a stand-in for the tracker's wording | Reported result REPRODUCED (Agree OR 1.940) | Recomputed with a separate `awk` command on 2026-10-14 (same numbers); sensitivity seeds 1, 2, 3 chosen before running; the independent cross-check run gives 1.933; sha256 of all raw files recorded and re-verified on 2026-10-14. Open threat: whether the tracker's OR wording means this computation (stated in `RESULT.md`) |
| 2026-10-13 | Suggested the portability changes to the root `Dockerfile` (drop `-march=native`, add `remotes` and the notebook's packages) and helped write the standalone `output_urgency/run_urgency.R` and the HTML dashboards | The portable image and the independent cross-check run (seed 4928) | Image built and run on a second machine (`HOW_TO_RUN.md`); `sessionInfo.txt` and `run_log.txt` saved; cross-check ORs recomputed from the raw contrast files with the v1 `awk` rule (Agree 1.933). Dashboards are presentation only and not cited as evidence |
| 2026-10-13 and 14 | Drafted `RESULT.md` and `DEVIATIONS.md` | Structure of the evidence trail | Reviewed by the group; every number in them was recomputed from raw files (above) |

## RQ2: Q8 grouping (v2 and v2b)

| Date | What the AI did | Decision it affected | How it was checked |
|---|---|---|---|
| 2026-10-22 | Helped locate the grouping column to swap (`perception.qs_3` to `perception.qs_2`) and write the print block that computes the ORs from the saved contrasts | The v2 run (`RQ2_results/`, seed 42) | Grouping swap verified by diffing the v2 notebook against `original/` (Deviation 5); ORs recomputed independently (below) |
| 2026-11-06 | Audited the RQ2 v2 run (ORs, evidence-ratio proxy, notebook diff) and drafted the v2 sections | `RESULT.md` v2 entry (DIFFERENT under the frozen rule) and `DEVIATIONS.md` item 5 | ORs recomputed from the v2 raw contrast CSVs with the v1 `awk` rule; Q8 split (7/12/40) recounted independently from the raw export; sha256 of the v2 files recorded |
| 2026-11-18 | Noticed that v2 compared the notebook's evidence ratio (v1) with an up/down proxy (v2), which are different quantities, and reran RQ2 like-for-like: v1's notebook with the grouping column changed to Q8 (one line), seeds 20261013, 1, 2, 3, numeric evidence ratios saved | `RESULT.md` v2b and `DEVIATIONS.md` item 6. The v2 rating "Agree Strong to Anecdotal" is withdrawn; RQ2 stays DIFFERENT, now because Disagree goes from Anecdotal to Moderate in all four runs and Agree's evidence ratio falls from 99-142 to 8.8-10.3 | One-line `diff` against v1 recorded; ORs recomputed from the saved contrast files with the v1 `awk` rule and matching v2 within seed noise; sha256 of the evidence files recorded and re-verified; a first launch that failed (compiler out of memory) was discarded and repeated unchanged. The Agree label sits on the Moderate/Strong cutoff and is reported as such |

## Event A (tag `EVENT_A_PLAN`; status Partial, see `EVENT-A-STATUS.md`)

| Date | What the AI did | Decision it affected | How it was checked |
|---|---|---|---|
| 2026-10-29 | Drafted the Event A plan and its prediction wording from the pack, the brief and `RESULT.md` | The Event A plan (`EVENT-A-PLAN-DRAFT.md`), adopted by the group on 2026-11-06, after the run | The prediction is the group's judgement; the plan file itself discloses the drafting |
| 2026-11-06 | Wrote the Event A deliverables: technical-ranking script (`event-a/analysis/`), bounded Java model of the Vignette 3 debt (`event-a/design/`), tests for both | Event A submission | 15 Python and 18 Java tests green (rerun 2026-11-06); the ranking output recomputed from the raw CSV filters; the design model is a bounded rewrite, not the original project's code, and says so in its sources |

An AI-drafted V1 conclusion in the Event A cells was later rejected (see "Rejected or corrected").

## M4: design pressure and smallest intervention (tag `PRE_EVENT_B`)

| Date | What the AI did | Decision it affected | How it was checked |
|---|---|---|---|
| 2026-11-06 | Drafted `M4-DESIGN.md` and the first version of this file | The M4 design record (PRE_EVENT_B) | Every claim in it points to committed tests, rerun green on 2026-11-06 |

The same rejected V1 conclusion appeared in the M4 cells (see "Rejected or corrected").

## Event B (tags `EVENT_B_PREDICTION`, `EVENT_B`)

| Date | What the AI did | Decision it affected | How it was checked |
|---|---|---|---|
| 2026-11-12 | Drafted the Event B prediction, defined the two defects (D1, D2) from Table 2 and the PRE_EVENT_B code, wrote the reproduction tests, the fix, the backlog planner and `event-b/EVENT-B.md` | Event B response (B1 chosen, Week 9 "partly supported") | Prediction committed and tagged before any test or fix; 5 defect tests shown failing on the unfixed code and passing after; 18 Week 9 tests unchanged and green; planner means recomputed from the raw export (59 respondents). Tests ran under javac + JUnit Platform, not `mvn` (Maven Central unreachable). `mvn test` was run later, on 2026-11-13 12:48 UTC: 25 tests, BUILD SUCCESS |
| 2026-11-12 | Pointed out that Week 9 quoted the ChatGPT-generated negative V3 comment, not the original neutral one | The section 5 finding in `EVENT-B.md` | Checked against Table 2 of the paper (p. 8) |
| 2026-11-13 | Helped review the Event B draft and the frozen cells against the committed files; wrote the after-the-fact wording-only check (`event-b/analysis/wording_only_plan.py`, 7 tests) and drafted `event-b/EVIDENCE-INDEX.md` and `EVENT-A-STATUS.md` | The corrected Event B write-up and the corrections listed below | Wording-only check labelled as after the fact; its V3 ratings (2.733 / 2.759) recomputed from the raw export; every index entry opened and checked against the file it names; Event A timeline checked against commit times and tags |

## Rejected or corrected

Found in the 13 Nov 2026 review of the frozen cells and the Event B draft against the committed files, and corrected in the
13 Nov text (Event A timing: `EVENT-A-STATUS.md`):

- **V1 claim (Event A and M4 cells).** The AI-drafted conclusion said negative wording made V1 look more urgent. The data say otherwise
  (negative 2.267, neutral 2.414). Rejected; the Event B text follows the data.
- **Wording versus ratings (Event B draft).** The draft said negative wording pulls the class split forward. V3 is rated 2.733 (negative)
  and 2.759 (neutral), so the plan difference comes from ratings, not wording. Replaced by a labelled after-the-fact check
  (`event-b/analysis/wording_only_plan.py`, 7 tests).
- **Unsupported sentence (Event B draft).** A "shotgun surgery ... we wanted to avoid in Week 9" claim that `M4-DESIGN.md` does not make. Replaced.
- **To-do left in the text (Event B draft).** "A group member should rerun `mvn test`". Run on 13 Nov: 25 tests, BUILD SUCCESS
  (`event-b/evidence/mvn-test-2026-11-13.txt`).
- **Event A plan record.** An earlier note claimed a 5 Nov freeze that the tracker history does not support. Corrected on 6 Nov to
  "adopted 6 Nov, after the run" (commit `cb35138`).
- **RQ2 evidence rating (v2).** The v2 entry rated Agree "Anecdotal for" from an up/down proxy and compared it with v1's evidence ratio (141.86, "Strong for"). Different scales; withdrawn on 18 Nov and replaced by the like-for-like rerun (v2b in `RESULT.md`).

This list says what was found and changed. It does not say who caught each item.

## Final: submission

| Date | What the AI did | Decision it affected | How it was checked |
|---|---|---|---|
| 2026-11-18 | Reorganised this file by stage, using the git history and the committed files | The AI-use record submitted with the project | Every row matched to a commit, tag or file in this repository |
| 2026-11-18 | Cross-checked that numbers quoted in `README.md`, `RESULT.md`, `M4-DESIGN.md` and `event-b/EVENT-B.md` agree with each other and with the evidence files | Final consistency of the submitted text | Mismatches, if any, fixed against the raw files, not the AI's reading; tests rerun before the final tag |
| 2026-11-18 | Found three docs that still named the never-pushed local branch `iwan` and added dated notes (nothing rewritten); updated item 4 of `event-b/EVIDENCE-INDEX.md` for the files added since tag `EVENT_B`; drafted the final-conclusion and main-limitation cells of the Student Tracker | What the final repository and tracker row say about where the evidence is and what it cannot show | `git grep` for the branch name; `git diff --name-only EVENT_B HEAD` compared with index item 4; remote tags listed with `git ls-remote`; the tracker cells read back after saving; every number in them taken from `RESULT.md` |

## Rule used in this project

AI may help read code, write scripts and draft text. A number is only reported if it can be recomputed from raw
files in this repository. Commit messages in this repo carry no AI trailers (a local commit hook strips them);
this file is the record of AI use instead.
