# Deviations from the authors' artefact (record BEFORE re-running)

1. 2026-10-13, build: the original `Dockerfile` fails at `devtools::install_github('stan-dev/cmdstanr')` with
   "The package 'remotes' is required" (current devtools no longer bundles it; build.log, first attempt).
   Fix: `docker/Dockerfile.fixed` adds one line, `RUN install2.r -e remotes`, before that step. Nothing else changed.
   Consequence: environment only, no effect on the model or data. Package versions are whatever CRAN gives today, not
   the authors' 2024 versions (threat: tiny numeric differences).

2-4. 2026-10-13, run, BEFORE the first run. `work/analyse_urgency_seeded.Rmd` is `analyse_experiment.Rmd` with only these changes
   (diff it against `original/`):
   2. `set.seed(20261013)` before the data is read, and `seed=20261013` in the `ulam()` call (M1 says "fixed seed"; the original has none).
   3. The final loop runs only Urgency (`for(i in 2)`, outcome_dfs[[2]]) instead of Effort, Urgency, Importance (M1 only needs Urgency).
   4. One added line saves the numeric evidence ratios to `evidence Urgency.csv` (the original only keeps the text label).
   The OR is computed afterwards from the saved `Urgency perception-j.csv` contrasts as P(contrast>0) / P(contrast<0).
   Seed 20261013 is arbitrary and was chosen before seeing any result.

5. 2026-10-22, run by Tien Nhat Minh Nguyen; deviations recorded 2026-11-06
   after the run, verified by diffing his notebook against `original/analyse_experiment.Rmd`. His
   `analyse_experiment.Rmd` is the authors' file with only these changes:
   - the grouping column `perception.qs_3` (Q9) is replaced by `perception.qs_2` (Q8) - this is the M1 RQ2
     manipulation itself, not drift;
   - `seed=42` in the `ulam()` call and `set.seed(42)` in `draw_contrast_causal`;
   - an added print block computing the ORs from the saved contrasts;
   - the final loop runs only Urgency (`for(i in 2:2)`).
   Unlike v1, no evidence-ratio file is saved (no equivalent of Deviation 4), so the v2 evidence rating in
   `RESULT.md` uses the contrast proxy (up/down), not the notebook's Evid.Ratio. Model, priors, data filters
   and sampling are otherwise the authors'.

6. 2026-11-18, RQ2 like-for-like rerun (v2b in `RESULT.md`), run by Iwan Teague. Recorded after the seed-20261013 run was started
   (that run was launched first; the seed runs 1, 2, 3 were written into `run_seeds_rq2.sh` before they ran).
   `work/rq2-s20261013/analyse_urgency_rq2.Rmd` is v1's `work/analyse_urgency_seeded.Rmd` with exactly one line changed (line 71):
   `perception_3 = df$perception.qs_3` -> `df$perception.qs_2` (the M1 RQ2 manipulation, as in item 5). Seed 20261013 kept, numeric evidence
   ratios saved (item 4 stays in the notebook), Urgency only, same image `p17-rstudio:original`. Seeds 1, 2, 3 differ only in the two seed values
   (`work/rq2-seed-N/`). It replaces the up/down proxy of item 5 with the notebook's own Evid.Ratio.
   The first launch failed at the Stan compile (the Docker VM killed `cc1plus`: out of memory); nothing from it was used, the run was repeated unchanged.
