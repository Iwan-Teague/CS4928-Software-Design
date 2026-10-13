#!/bin/sh
# Sensitivity runs: same v1 code, only the seed differs. Seeds 1, 2, 3 were fixed before any of them was run.
cd "$(dirname "$0")"
for s in 1 2 3; do
  docker run --rm -v "$PWD/work/seed-$s:/home/rstudio/work" -w /home/rstudio/work p17-rstudio:original \
    Rscript -e 'rmarkdown::render("analyse_urgency_seeded.Rmd", output_format="html_document", quiet=TRUE)' > work/seed-$s/run.log 2>&1
  echo "seed $s exit $?" >> work/seeds-status.txt
done
