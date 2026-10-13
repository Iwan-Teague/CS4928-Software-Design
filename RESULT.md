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

Committed in this repo on branch `iwan`.

### Threats and limits

- **OR definition.** The Rmd does not compute an OR; we derived it from the simulated contrasts as above. If the tracker's wording of "P(score up) / P(score down)" means something else (for example on posterior contrasts instead of simulated scores), the numbers change. Check the wording before the Week 7 entry.
- **One seed, one run.** The acceptance band is narrow (1.85-2.05). Any extra seeds are a labelled sensitivity check, not a replacement for v1; the seed was fixed before seeing a result and is not to be changed to pick a better one.
- **Environment drift.** Package versions differ from 2024; one Dockerfile line added (Deviation 1).
- **Simulated, not observed.** Both the OR and the evidence ratio come from model output on the 59 respondents; the paper's own tables were not re-read in this run.

## Planned versions (update this table when each is run)

| Version | Planned change | Purpose |
|---|---|---|
| v1 seeds 1, 2, 3 (sensitivity) | seed only | DONE 2026-10-13, see the section above |
| v2 (RQ2) | grouping column `perception.qs_3` (Q9) replaced by `perception.qs_2` (Q8, "acceptable practice") | M1 RQ2: "swapping Q9 for Q8" |

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
