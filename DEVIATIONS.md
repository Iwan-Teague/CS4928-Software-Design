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
