####### Dockerfile #######
FROM rocker/rstudio AS base

ENV DEBIAN_FRONTEND noninteractive

#COPY data.csv brms.R README.md /home/rstudio/

#COPY validation /home/rstudio/validation

#COPY docs /home/rstudio/docs

#COPY pdfs /home/rstudio/pdfs

FROM base AS apt-get
RUN apt-get update -qq \ 
  && apt-get -y --no-install-recommends install apt-utils libgit2-dev libssh2-1-dev libv8-dev libxml2-dev build-essential ed pkg-config apt-utils libglu1-mesa-dev libnlopt-dev nano libgsl-dev libz-dev libxt6 curl libglpk-dev

FROM apt-get as cmdstan 

WORKDIR /install 

RUN git clone https://github.com/stan-dev/cmdstan.git --recursive 

WORKDIR /install/cmdstan

RUN make -j8 build 

ENV CMDSTAN=/install/cmdstan

FROM cmdstan AS r-packages
RUN mkdir -p $HOME/.R/ \ 
  && echo "CXXFLAGS=-O3 -Wno-unused-variable -Wno-unused-function -Wno-macro-redefined" >> $HOME/.R/Makevars \
  && echo "CXXFLAGS+=-flto -Wno-unused-local-typedefs" >> $HOME/.R/Makevars \
  && echo "CXXFLAGS += -Wno-ignored-attributes -Wno-deprecated-declarations" >> $HOME/.R/Makevars \
  && echo "rstan::rstan_options(auto_write = TRUE)" >> /home/rstudio/.Rprofile \
  && echo "options(mc.cores = parallel::detectCores())" >> /home/rstudio/.Rprofile

RUN install2.r -e devtools remotes rstan plyr bayesplot brms gridExtra haven tidyr readxl sjstats ggthemes xml2 roxygen2 dagitty truncnorm ggdag cowplot bayesplot svglite ggridges forcats reshape2 scales

RUN R -e "devtools::install_github('stan-dev/cmdstanr')"

FROM r-packages AS r-source

COPY pt_1.1.tar.gz /home/rstudio

RUN install2.r -e /home/rstudio/pt_1.1.tar.gz

RUN R -e "devtools::install_github('rmcelreath/rethinking',ref='Experimental')"

RUN R -e "devtools::install_github('mjskay/tidybayes.rethinking')"

RUN rm /home/rstudio/pt_1.1.tar.gz

RUN rm -rf /tmp/downloaded_packages/ /tmp/*.rds

RUN chmod -R 777 /install

FROM r-source AS final

# Ship the analysis, data, pre-computed outputs and dashboard with the image
COPY --chown=rstudio:rstudio analyse_experiment.Rmd export_jan_23_no_ip_no_email.csv /home/rstudio/project/
COPY --chown=rstudio:rstudio output /home/rstudio/project/output
