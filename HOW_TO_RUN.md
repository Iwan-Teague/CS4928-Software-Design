# How to run the SATD negativity analysis (Docker)

You need [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running, and about 20 GB of free disk space.

## 1. Load the image

Put `satd-image.tar.gz` somewhere on your machine and run this in a terminal from the same folder:

```bash
docker load -i satd-image.tar.gz
```

This takes several minutes. When it finishes it prints `Loaded image: satd:latest`.

## 2. Start RStudio

```bash
docker run --rm -p 8787:8787 -e PASSWORD=choose-a-password satd:latest
```

Open http://localhost:8787 in a browser. Log in with username `rstudio` and the password you chose above.

## 3. Open the project

In RStudio, the files are in `~/project`:

| File | What it is |
|---|---|
| `analyse_experiment.Rmd` | The full analysis: data cleaning, the Bayesian ordered-logit model (`rethinking::ulam`) and the plots |
| `export_jan_23_no_ip_no_email.csv` | Anonymised survey responses (Qualtrics export) |
| `output/` | Pre-computed results (contrast CSVs and posterior/prior plots) |
| `output/dashbaord_Saif.html` | Interactive dashboard of the data (also opens in any browser without Docker) |

To re-run the analysis, open `analyse_experiment.Rmd`, set the working directory to `~/project` (Session → Set Working Directory → To Source File Location) and click **Knit**, or run the chunks one by one. Fitting the models takes a while.

**Note:** anything you change inside the container is lost when it stops. To keep your work, mount a folder from your machine instead, for example:

```bash
docker run --rm -p 8787:8787 -e PASSWORD=choose-a-password -v "$PWD/work:/home/rstudio/work" satd:latest
```
