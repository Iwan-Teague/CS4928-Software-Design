# P17 setup: Negativity in SATD (Cassee et al., EMSE 2025)

Group G22, project P17. Artefact: https://figshare.com/s/3a28b8b5d019d6a17c45 (article 26863435), accessed 2026-10-13, GPL 3.0+.
Checksums are in `ACCESSED.txt`.

- `original/`  read-only, exactly as downloaded (zip + unpacked files). Never edit.
- `docker/`    the authors' unmodified `Dockerfile` and `pt_1.1.tar.gz` (the build context).
- `work/`      our working copy of `analyse_experiment.Rmd` and the CSV, mounted into the container. Edit here only.
- `docker-compose.yml`  RStudio on http://localhost:8787 (no login, localhost only).
- `build.log`  the image build.

Build once: `docker build -t p17-rstudio:original docker` (compiles cmdstan, installs about 20 R packages: slow).
Run: `docker compose up -d`, then open http://localhost:8787 and knit `work/analyse_experiment.Rmd`.

Rules (brief and Abdul's updates): RQ1 reproduces the paper as is, whatever the result. Record commands, raw output, sample IDs and every
deviation from the original before re-running. Never overwrite M1 or earlier entries. No Event material before PRE_EVENT_A is frozen.

## Repository map (added 2026-10-14, after merging `iwan` into `main`)

Two layouts sit side by side. Only the first is the group's M2 evidence trail.

- **Evidence trail (start here):** `RESULT.md` (result, version log, sha256 of raw files, threats, independent cross-check), `DEVIATIONS.md`, `ACCESSED.txt`, `original/`, `docker/`, `work/` (v1 and seeds 1, 2, 3), `run_seeds.sh`, build logs. Git tags: `M1_PLAN`, `M2_REPRO`, `PRE_EVENT_A`.
- **Saif's original package copy, as committed on `main` before the merge:** the root-level `Dockerfile`, `analyse_experiment.Rmd`, `export_jan_23_no_ip_no_email.csv`, `pt_1.1/`, `pt_1.1.tar.gz` and `output/`. Not edited by us. `output/` has not been checked against the authors' published results here.
- **Saif's urgency re-run and dashboards** are on branch `saif` (`283d458`), not in `main`. `RESULT.md` credits it as an independent cross-check.
