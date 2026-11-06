# Urgency-only re-run of analyse_experiment.Rmd
#
# Same data cleaning, model and sampling as the original notebook, restricted to
# the Urgency outcome, with a fixed seed so the run is reproducible.
# Run from the project root (the folder containing export_jan_23_no_ip_no_email.csv):
#   Rscript output_urgency/run_urgency.R

suppressMessages({
  library(brms)
  library(rethinking)
  library(ggplot2)
  library(reshape2)
  library(bayesplot)
})

# L'Ecuyer-CMRG keeps mcreplicate (parallel::mclapply) reproducible too
RNGkind("L'Ecuyer-CMRG")
set.seed(4928)

out_dir <- "output_urgency"
dir.create(out_dir, showWarnings = FALSE)

# ---- Data cleaning (unchanged from the notebook) ----
df <- read.csv("export_jan_23_no_ip_no_email.csv")

# Drop two rows added by qualtrics
df <- df[3:nrow(df),]
df$Experience <- as.numeric(df$Experience)

# Remove the three pilot responses
df <- df[!(df$Create.New.Field.or.Choose.From.Dropdown... %in% "pilot"),]
df <- df[df$Experience < 50,]

df_cast = data.frame(
    `U1` = df$Urgency.1,
    `U2` = df$Urgency.2,
    `U3` = df$Urgency.3,
    `U4` = df$Urgency.4,
    flow = df$flow,
    perception_3 = df$perception.qs_3,
    experience = standardize(df$Experience))

df_cast[,1:ncol(df_cast)] <- sapply(df_cast[,1:ncol(df_cast)], as.numeric)

derive_perception <- function(row, output) {
  val <- row["perception_3"]
  if(is.na(val)) {
    return(NA)
  }
  if(row["perception_3"] > 3) {
    return("Agree")
  } else if(row["perception_3"] < 3) {
    return("Disagree")
  } else {
    return("Neutral")
  }
}

df_cast$perception = apply(df_cast, 1, derive_perception)
df_cast$perception_3 <- NULL

df_urgency <- melt(df_cast, id.vars = c("flow", "perception", "experience"), measure.vars = c('U1', 'U2', 'U3', 'U4'), value.name = "outcome", variable.name = "vignette")
df_urgency$vignette <- as.numeric(df_urgency$vignette)

# ---- Translation of flow -> sentiment / constructed (Table 3 in the manuscript) ----
# the value 2 is used to encode that a vignette was negative,
# while the 1 is used to encode neutral.
derive_sentiment <- function(row, output) {
  if(is.na(row["flow"])) {
    return(NULL)
  }
  if (row["flow"] == 1) {
    if(row["vignette"] == 1) return(2)
    if(row["vignette"] == 2) return(1)
    if(row["vignette"] == 3) return(2)
    if(row["vignette"] == 4) return(1)
  } else {
    if(row["vignette"] == 1) return(1)
    if(row["vignette"] == 2) return(2)
    if(row["vignette"] == 3) return(1)
    if(row["vignette"] == 4) return(2)
  }
}

derive_constructed <- function(row, output) {
  if(is.na(row["flow"])) {
    return(NULL)
  }
  if (row["flow"] == 1) {
    if(row["vignette"] == 1) return(1)
    if(row["vignette"] == 2) return(1)
    if(row["vignette"] == 3) return(2)
    if(row["vignette"] == 4) return(2)
  } else {
    if(row["vignette"] == 1) return(2)
    if(row["vignette"] == 2) return(2)
    if(row["vignette"] == 3) return(1)
    if(row["vignette"] == 4) return(1)
  }
}

code_perception <- function(row, output) {
  if(is.na(row["perception"])) {
    return(NA)
  }
  if(row["perception"] == "Agree") {
    return(3)
  } else if(row["perception"] == "Disagree") {
    return(1)
  } else{
    return(2)
  }
}

df_urgency$perception <- apply(df_urgency, 1, code_perception)
df_urgency$is_neg <- apply(df_urgency, 1, derive_sentiment)
df_urgency$constructed <- apply(df_urgency, 1, derive_constructed)
df_urgency <- df_urgency[!rowSums((is.na(df_urgency))),]

cat("Urgency observations:", nrow(df_urgency), " participants:", nrow(df_urgency) / 4, "\n")

# ---- Model (unchanged) ----
dat <- list(
  O = df_urgency$outcome,
  V = df_urgency$vignette,
  N = df_urgency$is_neg,
  C = df_urgency$constructed,
  P = df_urgency$perception,
  E = df_urgency$experience
)

m_adjust_c <- ulam(
  alist(
    O ~ dordlogit(phi, cutpoints),
    phi <- sentiment[N, P] + constructed[C] + experience*E,
    matrix[2, 3]: sentiment ~ dnorm(0, 0.5),
    vector[2] : constructed ~ dnorm(0, 0.5),
    experience ~ dnorm(0, .5),
    ordered[4] : cutpoints ~ dnorm(0, 2)
  ), data=dat, chains = 4, cores = 4, log_lik = F, iter=2000, force_compile = T)

# ---- Simulated contrasts (unchanged, apart from next_stream()) ----
# With L'Ecuyer-CMRG, mclapply derives the child streams from the parent's seed
# without advancing it, so back-to-back mcreplicate calls would reuse identical
# random numbers (making the negative and neutral draws artificially equal).
# Moving the parent to the next stream before each call keeps them independent.
next_stream <- function() {
  assign(".Random.seed", parallel::nextRNGStream(get(".Random.seed", envir = globalenv())), envir = globalenv())
}

draw_contrast_causal <- function(chosen_model, perception_val = 1, constructed = 1, use_priors = F) {
  if(use_priors) {
    next_stream()
    priors <- extract.prior(chosen_model)
    next_stream()
    Rsim_neutr <- mcreplicate(100,sim(chosen_model, data = list(P=perception_val, N=1, C=constructed, E=0), post=priors), mc.cores=4)
    next_stream()
    Rsim_neg <- mcreplicate(100,sim(chosen_model, data = list(P=perception_val, N=2, C=constructed, E=0), post=priors), mc.cores=4)
  } else {
    next_stream()
    Rsim_neutr <- mcreplicate(100,sim(chosen_model, data = list(P=perception_val, N=1, C=constructed, E=0)), mc.cores=4)
    next_stream()
    Rsim_neg <- mcreplicate(100,sim(chosen_model, data = list(P=perception_val, N=2, C=constructed, E=0)), mc.cores=4)
  }
  # If this is greater than zero then the score of the negative vignette was larger.
  Rsim_neg - Rsim_neutr
}

for(j in 1:3) {
  contrast <- draw_contrast_causal(m_adjust_c, perception_val = j, use_priors = F)
  write.csv(data.frame(list(contrast=c(contrast))), file.path(out_dir, paste("Urgency perception-", j, ".csv", sep="")), row.names = FALSE)
  contrast_priors <- draw_contrast_causal(m_adjust_c, perception_val = j, use_priors = T)
  write.csv(data.frame(list(contrast=c(contrast_priors))), file.path(out_dir, paste("priors Urgency perception-", j, ".csv", sep="")), row.names = FALSE)
}

# ---- Parameter-level contrasts, plots and hypothesis tests ----
posterior_raw <- extract.samples(m_adjust_c)
priors <- extract.prior(m_adjust_c)

sentiment_contrasts <- function(s) data.frame(
  "Disagree" = s$sentiment[, 2, 1] - s$sentiment[, 1, 1],
  "No Opinion" = s$sentiment[, 2, 2] - s$sentiment[, 1, 2],
  "Agree" = s$sentiment[, 2, 3] - s$sentiment[, 1, 3]
)
df_posterior <- sentiment_contrasts(posterior_raw)
df_prior <- sentiment_contrasts(priors)

# Raw contrast draws, so the dashboard can draw the densities
write.csv(df_posterior, file.path(out_dir, "posterior_sentiment_contrast_draws.csv"), row.names = FALSE)
write.csv(df_prior, file.path(out_dir, "prior_sentiment_contrast_draws.csv"), row.names = FALSE)

# Convert the value of evidence ratio to text using the definitions of 10.3758/s13428-018-01189-8
evid_ratio_to_text <- function(evid_ratio) {
  if(evid_ratio < 1/10) return("Strong against")
  if(evid_ratio < 1/3) return("Moderate against")
  if(evid_ratio < 1) return("Anecdotal against")
  if(evid_ratio < 3) return("Anecdotal for")
  if(evid_ratio < 10) return("Moderate for")
  return("Strong for")
}

summary_rows <- lapply(c("Disagree", "No.Opinion", "Agree"), function(g) {
  x <- df_posterior[[g]]
  pi89 <- PI(x, prob = 0.89)
  h <- hypothesis(df_posterior, paste(g, "> 0"))
  data.frame(
    group = sub("No.Opinion", "No Opinion", g),
    mean = mean(x), sd = sd(x),
    pi89_low = unname(pi89[1]), pi89_high = unname(pi89[2]),
    prob_positive = mean(x > 0),
    evid_ratio = h$hypothesis$Evid.Ratio,
    evidence = evid_ratio_to_text(h$hypothesis$Evid.Ratio)
  )
})
summary_df <- do.call(rbind, summary_rows)
write.csv(summary_df, file.path(out_dir, "urgency_posterior_summary.csv"), row.names = FALSE)
print(summary_df)

# Sampler diagnostics
diag <- precis(m_adjust_c, depth = 3)
write.csv(data.frame(parameter = rownames(diag), as.data.frame(diag)), file.path(out_dir, "urgency_model_precis.csv"), row.names = FALSE)

bayesplot_theme_set(theme_minimal())
plot_areas <- function(d, title) {
  mcmc_areas(d, prob = 0.89, prob_outer = 0.99, point_est = "mean") +
    ggtitle(title) +
    theme(plot.title = element_text(hjust = 0.5)) +
    scale_y_discrete(labels = c("Disagree", "No Opinion", "Agree")) +
    geom_vline(xintercept = c(0), linetype = "dotted", color = "black")
}
ggsave(file.path(out_dir, "Posterior_Urgency.pdf"), plot = plot_areas(df_posterior, "Posteriors for Urgency"), device = "pdf", width = 3.5, height = 7)
ggsave(file.path(out_dir, "Prior_Urgency.pdf"), plot = plot_areas(df_prior, "Priors for Urgency"), device = "pdf", width = 3.5, height = 7)

writeLines(capture.output(sessionInfo()), file.path(out_dir, "sessionInfo.txt"))
cat("Done.\n")
