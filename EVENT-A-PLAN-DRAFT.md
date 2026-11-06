# Event A plan (adopted 2026-11-06, after the run; NOT frozen before it), CS4928 Software Design (Abdul Razzaq), group G22, project P17

Drafted 29 Oct 2026 by an AI assistant (Claude Code) from the P17 pack, the P17 Event A sheet, the brief and our `RESULT.md`, as a proposal for the group to
discuss, change and then freeze. **The prediction in section 4 is the group's own judgement, not the assistant's.** The AI help is recorded in
`project/p17-artefact/AI_USE.md`.

Adoption timeline:

- **2026-10-29** - this plan drafted and committed (`8bc019e`) as a proposal, marked DRAFT.
- **2026-10-30 and 2026-11-02** - the group was unsure Event A applied to P17 and **asked the lecturer by email, then waited for his clarification**. His replies came on 2026-10-30 and 2026-11-03.
- **2026-11-03** - the lecturer's reply confirmed Event A is applicable and that a partial attempt is acceptable.
- **Through 2026-11-05** - the tracker's Event A prediction cell still said a prediction was impossible; no prediction was frozen.
- **2026-11-06** - the run landed on branch `iwan` (merge `4a17430`, 11:34 UTC). The plan and prediction were recorded **after** the run; tag `EVENT_A_PLAN` was created 2026-11-06, after the run, and says so. Recorded status: Partial.

Deadline: **Fri 30 Oct 18:00** (Brightspace folder "Deadline - Event 1 Transfer Test"). Event A prediction assessment in the lab: extended to **Mon 2 Nov** for
students who missed Monday's (bank holiday) lab (announcement 28 Oct).

## 0. Order of work (the freeze comes before any run)

1. Group call (30 min): agree sections 1-5 below; change what you disagree with.
2. Enter in the Student Tracker (G22 / P17 row): held-out material, **prediction before execution**, and the outcome that would challenge M2.
3. Commit this plan (final wording) to `project/p17-artefact` and tag it `EVENT_A_PLAN` **before running anything**. That tag is the proof of the freeze.
4. Run the frozen method (section 3). Do not retune. If you improve it later, report the first result separately.
5. Compare with M2, write the design implication, link the evidence, fill the tracker's result field, upload to Brightspace.

## 1. What Event A asks for (from the P17 Event A sheet)

"Take the same bounded debt items used in M2, but ignore their original emotional/priority wording while making a new ranking. Define a prioritisation rule
based only on technical evidence, then compare that ranking with the original sentiment-influenced ordering." Plus: say what transfers and what does not,
name one software-design, refactoring or maintainability implication (no design pattern unless the evidence justifies it), and link raw evidence.

## 2. Held-out material and items (to record in the tracker)

- **Items:** the same bounded items as M2, as frozen at M1: the four survey vignettes (source-code comments about technical debt), each seen by a respondent in
  either a neutral or a negative variant; 59 valid respondents, 236 Urgency ratings (`RESULT.md`, M1 rule). Raw data: `work/evidence Urgency.csv` and
  `export_jan_23_no_ip_no_email.csv` (sha256 in `RESULT.md`). Artefact: figshare article 26863435, accessed 2026-10-13.
  **[GROUP DECIDES]** If the tracker's M1 row lists a different bounded set (for example the first 20 SATD examples from the pack's manual-inspection task), use exactly
  that set and replace "4 vignettes" with its identifiers throughout. Check this first.
- **What is held out in this event:** M2 used the Urgency outcome only. The data also holds Importance and Effort ratings for the same vignettes. The **transfer
  test** applies the frozen M2 method, unchanged, to Importance and to Effort (only the outcome column changes). These were not looked at in M2, so they are
  genuinely unseen results. **[GROUP DECIDES]** whether this secondary test is in scope; the primary task below is the ranking comparison the sheet describes.

## 3. Frozen method

**3a. Original (sentiment-influenced) ordering.** Rank the four vignettes by their mean Urgency rating over all respondents who saw them, from the raw data,
before any modelling. Record the ranks (1 = most urgent) and how ties are broken (**[GROUP DECIDES]**: by vignette number).

**3b. Technical-evidence-only rule (proposed; edit freely, then freeze).** For each vignette, two coders (Iwan and Saif; Sam breaks ties) read only the
code comment with emotional words masked (list the masked words in the evidence) and give each item:
- *Impact class* from what the comment says is wrong, not how it is phrased: 0 cosmetic or naming, 1 maintainability only, 2 performance or reliability risk, 3 correctness or security risk;
- *Scope*: 0 one statement, 1 one function, 2 one module, 3 cross-module;
- *Fix size*: 0 under 5 minutes, 1 under an hour, 2 under a day, 3 more than a day, judged from the stated fix.
Priority score = Impact + Scope - Fix size. Rank by score; ties broken by Impact, then by vignette number. Coders score independently first; record both sets and
Cohen's kappa; disagreements are settled by Sam before looking at section 3a's ordering. **The respondents' Urgency, Importance and Effort ratings must not be used
in this rule** (they carry the sentiment effect under study).

**3c. Comparison.** Spearman rank correlation and the number of items that change rank between 3a and 3b (with 4 items, rho takes only a few values, so report the
ranks themselves too, not only rho). If the set is 20 items, also report Kendall's tau with a bootstrap interval.

**3d. M2 method applied first, unchanged.** Same seed (20261013), same model, same OR rule and acceptance band as M2 (`RESULT.md`), run on Urgency again so the
event's evidence sits on the same footing; then the same script on Importance and on Effort (if section 2's secondary test is in scope).

## 4. Prediction before execution (written 2026-11-06, after the run; see timeline)

Wording entered in the tracker:
- The technical-only ranking will **differ from the sentiment-influenced ranking in at least one position**, because in M2 negative wording raised Urgency
  noticeably (Agree group OR 1.94, evidence ratio about 140) while the other two groups stayed near 1 (OR 1.06 and 1.09), so sentiment moved ratings for only part of the sample.
- The **largest rank change** will be a negative-variant item whose comment states a weak technical problem.
- The Agree-group effect will **appear again on Importance but be weaker or absent on Effort** (negativity should look urgent and important more than costly). Reasoning: M2 only tested Urgency.

**Outcome that would challenge the M2 conclusion** (REPRODUCED): any of: the technical-only ranking equals the sentiment ranking exactly (so sentiment did
not change what is prioritised); or the Agree OR on Urgency re-run falls outside 1.85-2.05 under the same seed; or the same effect appears equally in the Disagree
group on Importance or Effort (so the effect is not specific to people who think negativity signals priority).

## 5. What to write up (for the tracker and Brightspace)

- Held-out material and ids; frozen rule and tag; prediction; result (ranks, rho, ORs); what transfers and what does not; the strongest evidence for each.
- **One design/maintainability implication** from the module (candidates, pick one the evidence supports): comments that mix mood with technical content hide the
  design pressure, so prefer a structured debt annotation (what is wrong, scope, estimated fix) over free-text complaint; or a no-change decision if the ranking did not move.
  Do not introduce a pattern unless the evidence and design forces justify it.
- Link: commit hash and tags (`M1_PLAN`, `M2_REPRO`, `PRE_EVENT_A`, `EVENT_A_PLAN`), the coder sheets, the ranking table, raw model output with sha256.
- Threats: four items is a very small ranking; respondents are 59 volunteers; coders know the study; the rule is ours, not the paper's; environment drift from 2024 package versions (as in M2).

## 6. Open questions (settled when the plan was adopted, 2026-11-06)

The lecturer's reply of 2026-11-03 confirmed Event A applies to P17; the group settled these when adopting the plan.

1. Which items does the tracker's M1 row list as the bounded set (4 vignettes or 20 SATD examples)?
2. Has anyone already entered an Event A prediction in the tracker? (Do not overwrite an earlier record; add a note.)
3. Does the Brightspace folder want a document, the repo link, or the tracker screenshot, and is it one upload per group (Sam submitted M2 for the group)?
4. Who is coder 1, coder 2 and tie-breaker.
