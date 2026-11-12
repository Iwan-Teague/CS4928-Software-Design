# RESULT: P17 (G22), RQ1

One section per version of the code we run. Never edit an earlier section after the fact; add a new version and say what changed.
Frozen M1 (Student Tracker, G22 / P17) is quoted, not rewritten.

## M1 rule (frozen before any run)

- RQ1: "Can the reported effect of negative sentiment on perceived Urgency be reproduced from the published data and analysis code?"
- Sample: 236 Urgency ratings (vignettes 1-4) from 59 valid respondents, grouped by Q9 (22 Agree / 11 No Opinion / 26 Disagree).
- Method: rerun the authors' Model 1 on Urgency with a fixed seed; each group's odds ratio is P(score up) / P(score down), with its evidence ratio.
- Reproduced if: the Agree OR is within 1.85-2.05 with "Strong for" evidence while the other two groups stay near 1.
- Expected ORs: about 1.95 (Agree), 1.07 (No Opinion), 1.10 (Disagree).

## Version log

| Version | Code | Change from the previous version | Run? |
|---|---|---|---|
| v0 | authors' files, unmodified (`original/`, `docker/Dockerfile`) | none | Build failed at `devtools::install_github('stan-dev/cmdstanr')`: "The package 'remotes' is required" (`build-attempt1-failed.log`). No analysis was run. |
| v1 | `work/analyse_urgency_seeded.Rmd` in the image built from `docker/Dockerfile.fixed` | Deviations 1-4 in `DEVIATIONS.md`: `remotes` added to the build; `set.seed(20261013)` and `ulam(seed=20261013)`; Urgency only; numeric evidence ratios saved. Model, priors, data filters and sampling are the authors'. | Yes, once, 2026-10-13 |

## v1: run 2026-10-13, seed 20261013

Environment: image `p17-rstudio:original` (arm64, Docker 29.8.0, R 4.6.1, rethinking 2.42, rstan 2.32.7, brms 2.23.0, bayesplot 1.16.0 = today's CRAN, not the authors' 2024 versions).

Command (from `project/p17-artefact`):

    docker run --rm -d --name p17-run -v "$PWD/work:/home/rstudio/work" -w /home/rstudio/work p17-rstudio:original \
      Rscript -e 'rmarkdown::render("analyse_urgency_seeded.Rmd", output_format="html_document", quiet=FALSE)'

Sample check (from the rendered notebook, `analyse_urgency_seeded.html`): 236 Urgency rows after cleaning = 59 x 4, matching M1.
The Q9 split recomputed independently from the CSV (stdlib count, not part of the model): 22 Agree / 11 No Opinion / 26 Disagree.

OR taken from the saved contrast files as P(contrast > 0) / P(contrast < 0), where contrast = simulated score (negative vignette) minus
simulated score (neutral vignette), 100,000 draws per group:

    awk -F, 'NR>1{n++; if($1>0)u++; else if($1<0)d++} END{print n,u,d,u/d}' "Urgency perception-<j>.csv"   # j: 3 Agree, 2 No Opinion, 1 Disagree

| Group (Q9) | n draws | up | down | same | OR | Evidence ratio (Agree > 0 etc.) | Posterior prob. | M1 expected | In M1 range / near 1? |
|---|---|---|---|---|---|---|---|---|---|
| Agree (j=3) | 100000 | 48741 | 25121 | 26138 | **1.940** | **141.86** ("Strong for", > 10) | 0.993 | about 1.95 | yes (1.85-2.05) |
| No Opinion (j=2) | 100000 | 37493 | 35380 | 27127 | 1.060 | 1.24 (anecdotal) | 0.553 | about 1.07 | yes (near 1) |
| Disagree (j=1) | 100000 | 37253 | 34248 | 28499 | 1.088 | 1.59 (anecdotal) | 0.614 | about 1.10 | yes (near 1) |

Status against the frozen rule: **REPRODUCED** (Agree OR 1.940 inside 1.85-2.05 with "Strong for" evidence; the other two groups near 1).

### Raw evidence (sha256)

    bd57c812208ff7eb6edff88c7c495396edd02b00d22bfb53cb02121ae4ea8a6d  work/analyse_urgency_seeded.Rmd
    67344927ade1b80ccd69a054a7aa51447f4c2eda863d8409a964edec55481383  work/analyse_urgency_seeded.html
    683728081b8b9faba2f1c379c89afdb059de039dc3521827fd6b94c1dfe0eb27  work/evidence Urgency.csv
    87b30d0312bbbd95a1dc1672db7f1494a78476a50c8ed32e232f3b2bbe6383b5  work/Urgency perception-1.csv
    35b679389f5fe6e73b7e0ab0d543d751c21cdfdab8aba96c454ffc3acc3ea4da  work/Urgency perception-2.csv
    041dbc687d1ffb6b639f424eec20fafc99d83483521345604b18fb3b20a9398a  work/Urgency perception-3.csv

Committed in this repo at 51cbcd5 (branch `iwan`).

> Note, 2026-10-14: the branch `iwan` was rewritten once to remove commit-message trailers. File contents, authors and dates are unchanged. Commit hashes changed: `51cbcd5` is now `e0f945b`, `7df8f3d` is now `6bcc2d6`, `8a72cae` is now `a63db14`. Earlier text in this file that names an old hash refers to the same content.

> Note, 2026-11-06: the history was rewritten on this day to remove AI attribution (the no-AI-trailer rule), before push. File contents and author dates are unchanged; commit hashes changed: `71bccb1` -> `f447363`, `b6916aa` -> `f935f08`, `49483e3` -> `c627582`, `d90e088` -> `8bc019e`, `f1263d6` -> `cdd594e` (author and committer corrected from "Claude" to Iwan Teague, same author date), PR merge `4c4e713` -> `d2dc89b`, merge `4108152` -> `4a17430`; every descendant of these, including the tip that carries this note, was rewritten with them. The `EVENT_A_PLAN` tag was re-pointed at the rewritten plan commit `8bc019e` (same date and message). The AI contributions themselves are disclosed in `AI_USE.md`. Earlier text anywhere in this repo that names an old hash refers to the same content.

### Threats and limits

- **OR definition.** The Rmd does not compute an OR; we derived it from the simulated contrasts as above. If the tracker's wording of "P(score up) / P(score down)" means something else (for example on posterior contrasts instead of simulated scores), the numbers change. Check the wording before the Week 7 entry.
- **One seed, one run.** The acceptance band is narrow (1.85-2.05). Any extra seeds are a labelled sensitivity check, not a replacement for v1; the seed was fixed before seeing a result and is not to be changed to pick a better one.
- **Environment drift.** Package versions differ from 2024; one Dockerfile line added (Deviation 1).
- **Simulated, not observed.** Both the OR and the evidence ratio come from model output on the 59 respondents; the paper's own tables were not re-read in this run.

## Planned versions (update this table when each is run)

| Version | Planned change | Purpose |
|---|---|---|
| v1 seeds 1, 2, 3 (sensitivity) | seed only | DONE 2026-10-13, see the section above |
| v2 (RQ2) | grouping column `perception.qs_3` (Q9) replaced by `perception.qs_2` (Q8, "acceptable practice") | M1 RQ2: "swapping Q9 for Q8". DONE 2026-10-22 (Minh, seed 42), see the v2 section below |

## v1 sensitivity: seeds 1, 2, 3 (run 2026-10-13, after v1)

Same code as v1 (`work/seed-N/analyse_urgency_seeded.Rmd` differs from v1 only in the two seed values), same image. Seeds 1, 2, 3 were chosen
and written into `run_seeds.sh` before any of them was run. These runs do not replace v1; v1 (seed 20261013) stays the reported result.
Run with `./run_seeds.sh`; per-seed output in `work/seed-N/`. All three exited 0.

| Seed | Agree OR | Agree evidence ratio | No Opinion OR | Disagree OR | Agree in 1.85-2.05 with "Strong for"? |
|---|---|---|---|---|---|
| 20261013 (v1) | 1.940 | 141.86 | 1.060 | 1.088 | yes |
| 1 | 1.950 | 99.00 | 1.040 | 1.085 | yes |
| 2 | 1.958 | 101.56 | 1.044 | 1.093 | yes |
| 3 | 1.956 | 128.03 | 1.046 | 1.067 | yes |

Spread across the four runs: Agree OR 1.940-1.958 (range 0.018), well inside the acceptance band; No Opinion 1.040-1.060; Disagree 1.067-1.093;
evidence ratio for Agree 99-142, always above 10 ("Strong for"). The conclusion (REPRODUCED under the frozen rule) does not depend on the seed.

Raw files per seed: `work/seed-N/Urgency perception-{1,2,3}.csv`, `evidence Urgency.csv`, `analyse_urgency_seeded.html`. sha256:

    f5b9202a5b98952e6f360f94c25b0c947e2ea363777fee0d6edcd2eb8837096b  work/seed-1/evidence Urgency.csv
    fa117457eab97032cec21a3a8bd885aee480c852f8244b0a72fa8b6f8609f502  work/seed-2/evidence Urgency.csv
    fb26b6dac29e06db7c7672db4b802a0a3b6d184529cfa03fb84d0dca135acaa7  work/seed-3/evidence Urgency.csv
    3fe2c47c60a9d8788aebd3f5275bc1be22abf7a11b3c9493a1b6aed0fbf4964f  work/seed-1/Urgency perception-1.csv
    c03188358c47fbd053850f5185e45a06968524ac4cd1f53d46bdf8ace6d81b49  work/seed-1/Urgency perception-2.csv
    b4ce23b392466ecf3b0643fa27c7cdc83767b9f4c1a534fd252928680f54746d  work/seed-1/Urgency perception-3.csv
    797f8482fb0642f789e6db74a08c58c2a0eb84d33510a34cf334541c34f5261b  work/seed-2/Urgency perception-1.csv
    f1187e28e5b308d5f97a8772e6e5b89a20596f8eb9a162fa4d4fa833d0196ae2  work/seed-2/Urgency perception-2.csv
    1c46171fafb5dcc16c38a01cb1f28fa7fa56976ef4e70d74a0e1f06588fef2b1  work/seed-2/Urgency perception-3.csv
    006d3cd30206cf0b5255ad32c4f2f30d6fbff6d145a6814b8a8eb2dc18be1884  work/seed-3/Urgency perception-1.csv
    cdaee33a66487fb2d28f4a2c3f2c963d568a7a83f4339afc190a53c475117925  work/seed-3/Urgency perception-2.csv
    09e2844a57ad9f38ff6407a9d9f4edbca95a1fafd14ac5ce02c2020f865968ae  work/seed-3/Urgency perception-3.csv
    ad5cd2fa04abee40f8a985dfda8779516afd12580726f8cdf60608bdefaa2730  work/seed-1/analyse_urgency_seeded.html
    64e942ee04f91adf50178009a55c184d6e52560ad801e47ef4089c797bece825  work/seed-2/analyse_urgency_seeded.html
    943800c735af3143246113779cd7c2a4dcf46498dee323c949451c34c81300ad  work/seed-3/analyse_urgency_seeded.html

## Independent cross-check by Saif Khawaldeh (added 2026-10-14; does not replace v1)

Saif ran the Urgency analysis independently on branch `saif` (commit `283d458`, 2026-10-13): a standalone script `output_urgency/run_urgency.R`, a different seed (4928), `RNGkind("L'Ecuyer-CMRG")`, and his own Docker image (`-march=native` removed). It is a different route from v1 (which runs the authors' notebook with three recorded edits), so it counts as a cross-check, not as a second version of this reproduction. His own deviations are not recorded in a deviation file; that is for him to add if the group wants his run in the formal record.

The ORs below were computed by us with the same rule as v1 (P(contrast > 0) / P(contrast < 0)) from Saif's raw files `output_urgency/Urgency perception-{1,2,3}.csv` (100,000 draws each), using the same `awk` command as v1:

| Group (Q9) | Saif up | Saif down | OR (Saif, seed 4928) | OR (v1, seed 20261013) | In M1 range / near 1? |
|---|---|---|---|---|---|
| Agree (j=3) | 48671 | 25184 | **1.933** | 1.940 | yes (1.85-2.05) |
| No Opinion (j=2) | 37407 | 35899 | 1.042 | 1.060 | yes (near 1) |
| Disagree (j=1) | 37016 | 34048 | 1.087 | 1.088 | yes (near 1) |

Saif's own summary (`output_urgency/urgency_posterior_summary.csv`) gives an evidence ratio of 113.29 for Agree ("Strong for"), against 141.86 in v1. The conclusion agrees: REPRODUCED under the frozen rule.

Limits: his files were read from git, not re-run by us; his script was not diffed line by line against the authors' notebook here; the check relies on the same OR definition as v1.

## v2: RQ2, run by Tien Nhat Minh Nguyen on 2026-10-22 (branch `minh`, commit `5e37f15`, seed 42)

v2 is M1's second question: the model is rerun with the grouping column swapped from `perception.qs_3` (Q9) to
`perception.qs_2` (Q8, the "acceptable practice" response). The notebook is Minh's own copy of the authors'
`analyse_experiment.Rmd` on branch `minh`; his deviations are item 5 in `DEVIATIONS.md` (recorded 2026-11-06,
after the run; the differences were verified by diffing his file against `original/analyse_experiment.Rmd`).

Sample check: the Q8 split recounted independently from `work/export_jan_23_no_ip_no_email.csv` (branch `minh`),
same cleaning rule as v1 (skip the two Qualtrics header rows, drop pilot rows, Experience < 50):
59 valid respondents; Q8 split 7 Agree / 12 No Opinion / 40 Disagree, matching the M1 sample definition.

ORs computed from Minh's saved contrast files `RQ2_results/Urgency perception-{1,2,3}.csv` (100,000 draws per
group) with the same rule and `awk` command as v1. Under Q8 the Disagree group is the one that calls negativity
unacceptable (40 respondents), so M1's expectation ("OR above 1.10" for them) applies to Disagree:

| Group (Q8) | n draws | up | down | same | OR | Evidence ratio (proxy: up/down) | v1 OR (Q9) | OR move |
|---|---|---|---|---|---|---|---|---|
| Agree (j=3) | 100000 | 45827 | 27306 | 26867 | **1.678** | 1.68 ("Anecdotal for", proxy) | 1.940 | -0.262 |
| No Opinion (j=2) | 100000 | 39489 | 33577 | 26934 | 1.176 | 1.18 ("Anecdotal for", proxy) | 1.060 | +0.116 |
| Disagree (j=1) | 100000 | 40833 | 31567 | 27600 | **1.294** | 1.29 ("Anecdotal for", proxy) | 1.088 | +0.206 |

Status against the frozen decision rule ("Q2 is different if any group's evidence rating changes or its OR moves
by more than 0.3"):

- No OR moves by more than 0.3 (largest: Agree, -0.262).
- The Agree evidence rating changes: v1 "Strong for" (Evid.Ratio 141.86 from the saved notebook file) vs v2
  "Anecdotal for" on the contrast proxy.
- Therefore v2 is **DIFFERENT** under the frozen rule, driven by the evidence rating.
- M1's directional expectation holds: Disagree OR 1.294 > 1.10.

Threat on the rating comparison: Minh's run did not save the notebook's numeric evidence ratios (no equivalent of
Deviation 4), so the v2 rating uses the contrast proxy (up/down), which is not like-for-like with v1's brms
`hypothesis()` Evid.Ratio. Before the Week 10 Event B response cites the rating change, rerun the v1
evidence-ratio save under the v2 manipulation (recorded as the open next step; not run for this entry).

Other threats: one seed (42), chosen by Minh, no sensitivity seeds; his files were read from git, not rerun by us;
the grouping swap itself was verified in the diff (column `perception.qs_2`, exactly the M1 manipulation).

Raw evidence (sha256, branch `minh`):

    0e22c314bdd1599d204cf6be37fa9de27a0351f57981dd8be58b0f80e086ba36  RQ2_results/Urgency perception-1.csv
    a1941587ae54c6a0be3cd292d18e04c2c50343670ea7b3f666521e4043764bb7  RQ2_results/Urgency perception-2.csv
    fe839e615c484ea56c86888d8e855af2c9821aa6ee219af59cae89f469af4eda  RQ2_results/Urgency perception-3.csv
