# AI use: G22 / P17 (brief material contributions only)

Per the project brief, this records only AI contributions that affected an engineering or research decision.
No prompt logs. AI output is not evidence; the evidence is the data, the computation and the checks below.

This file covers Iwan's own use. Teammates add their own use under their own heading (Saif's branch `saif`,
Minh's `minh` runs, Samuel's RQ drafting, and so on); nothing about them is asserted here.

## Iwan: material AI contributions (Claude, via Claude Code)

| Date | What the AI did | Decision it affected | How it was checked |
|---|---|---|---|
| 2026-09-25 | Early AI discussion helped iron out the RQ1 scope options; the group picked straight reproduction with a fixed seed | The group's RQ1 direction at M1 | Scope checked against the project pack and the paper before the M1 freeze |
| 2026-10-13 | Diagnosed the failed Docker build (`The package 'remotes' is required`) and proposed adding `RUN install2.r -e remotes` before the cmdstanr step | Deviation 1 in `DEVIATIONS.md` | Build log of the failed attempt (`build-attempt1-failed.log`) and of the fixed build (`build.log`); rest of the image unchanged |
| 2026-10-13 | Proposed the seeded Urgency-only copy of the notebook (`work/analyse_urgency_seeded.Rmd`): fixed seed, Urgency loop only, save numeric evidence ratios | Deviations 2-4; the seed was fixed before any result was seen | `diff` against `original/analyse_experiment.Rmd`; 236 = 59 x 4 rows confirmed from the rendered notebook; Q9 split (22/11/26) recounted independently from the CSV |
| 2026-10-13 | Wrote the OR from the saved contrast files (P(contrast > 0) / P(contrast < 0)) as a stand-in for the tracker's wording | Reported result REPRODUCED (Agree OR 1.940) | Recomputed with a separate `awk` command on 2026-10-14 (same numbers); sensitivity seeds 1, 2, 3 chosen before running; Saif's independent run gives 1.933; sha256 of all raw files recorded and re-verified on 2026-10-14. Open threat: whether the tracker's OR wording means this computation (stated in `RESULT.md`) |
| 2026-10-13 and 14 | Drafted `RESULT.md` and `DEVIATIONS.md` | Structure of the evidence trail | Iwan reviewed; every number in them was recomputed from raw files (above) |
| 2026-10-29 | Drafted the Event A plan and its prediction wording from the pack, the brief and `RESULT.md` | The Event A plan (`EVENT-A-PLAN-DRAFT.md`), adopted by the group on 2026-11-06, after the run | The prediction is the group's judgement; the plan file itself discloses the drafting |
| 2026-11-06 | Wrote the Event A deliverables: technical-ranking script (`event-a/analysis/`), bounded Java model of the Vignette 3 debt (`event-a/design/`), tests for both | Event A submission | 15 Python and 18 Java tests green (rerun 2026-11-06); the ranking output recomputed from the raw CSV filters; the design model is a bounded rewrite, not the original project's code, and says so in its sources |
| 2026-11-06 | Audited the RQ2 v2 run on branch `minh` (ORs, evidence-ratio proxy, notebook diff) and drafted the v2 sections | `RESULT.md` v2 entry and `DEVIATIONS.md` item 5 | ORs recomputed from Minh's raw contrast CSVs with the v1 `awk` rule; Q8 split (7/12/40) recounted independently from the raw export; sha256 of his files recorded |
| 2026-11-06 | Drafted `M4-DESIGN.md` and this file | The M4 design record (PRE_EVENT_B) | Every claim in it points to committed tests, rerun green on 2026-11-06 |

## What was rejected or corrected

None recorded in this repo's history: no AI suggestion was rejected or needed correcting beyond the normal
review-and-recompute checks in the table.

## Rule used in this project

AI may help read code, write scripts and draft text. A number is only reported if it can be recomputed from raw
files in this repository. Commit messages in this repo carry no AI trailers (a local commit hook strips them);
this file is the record of AI use instead.
