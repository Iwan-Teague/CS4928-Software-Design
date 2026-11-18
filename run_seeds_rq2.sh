#!/bin/sh
# RQ2 sensitivity runs: same notebook as the RQ2 rerun (work/rq2-s20261013/analyse_urgency_rq2.Rmd = v1 code, grouping column qs_2),
# only the seed differs. Seeds 1, 2, 3 are the same as run_seeds.sh and were fixed before any RQ2 seed run (2026-11-18).
cd "$(dirname "$0")"
for s in 1 2 3; do
  d=work/rq2-seed-$s
  mkdir -p "$d"
  sed -e "s/set.seed(20261013)/set.seed($s)/" -e "s/seed=20261013/seed=$s/" work/rq2-s20261013/analyse_urgency_rq2.Rmd > "$d/analyse_urgency_rq2.Rmd"
  cp work/rq2-s20261013/export_jan_23_no_ip_no_email.csv "$d/"
  docker run --rm -v "$PWD/$d:/home/rstudio/work" -w /home/rstudio/work p17-rstudio:original \
    Rscript -e 'rmarkdown::render("analyse_urgency_rq2.Rmd", output_format="html_document", quiet=TRUE)' > "$d/run.log" 2>&1
  echo "rq2 seed $s exit $?" >> work/seeds-status-rq2.txt
done
