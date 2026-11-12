# Event B (P17, G22): fixed sprint budget, two new defects in ConstDeclNode

Start state: tag `PRE_EVENT_B` (Week 9, `M4-DESIGN.md`, not edited here). Prediction and decision rule frozen first:
`event-b/PREDICTION.md`, tag `EVENT_B_PREDICTION`. Response: tag `EVENT_B` on branch `event-b`.

## 1. Pressure and prediction

Event B sheet: one-sprint budget, two new defects in the same area, reprioritise the remaining debt, and say where emotional
wording would have led the decision astray. The area is `ConstDeclNode`: Vignettes 2 and 3 are both comments on it (Table 2).
The sheet does not name the defects; we defined two that occur in our model at `PRE_EVENT_B` (details in `PREDICTION.md`):

- **D1**: V2's caller (`getConstNode()`, then use it) throws NPE on a simple declaration `FOO = 1`, because the Week 9 class
  still returns `null` there for compatibility.
- **D2**: `ConstPath` accepts `::` or blank parts, so `setName("B::FOO")` breaks the name/path invariant again and
  `scoped("FOO","A::B")` prints like `scoped("FOO","A","B")`.

Predicted: the pressure lands on the Week 9 null shim and on `ConstPath` validation, not on the one-field structure; both
fixable in at most 3 production files with the 18 Week 9 tests unchanged; sprint = D1, D2, V4, V2; split (R2) and V1 deferred.

## 2. Responses compared

| Response | Main trade-off | Decision |
|---|---|---|
| B0: no structural change - null-check in each caller, validate names at each call site | Smallest diff to the class, but every present and future caller must remember both checks (the shotgun-surgery risk Week 9 rejected for R0) | Rejected |
| B1: fix at the source - `ConstPath` validates every part (rejects blank and `::`); `ConstDeclNode` gains a non-null `path()`; `getConstNode()` kept but `@Deprecated`; the V2 caller uses `path()` | One extra accessor: two ways to read the path coexist until old callers move off `getConstNode()`; inputs that were silently accepted now throw `IllegalArgumentException` | **Chosen** (smallest, local) |
| B2: split `ConstDecl` into simple and scoped classes (the FIXME, Week 9's R2) | Removes the null-means-simple convention for good, but touches every caller, costs about 4 of the 5 sprint units, and no failing test remains for it to fix once B1 is in | Deferred again |

## 3. Implementation and verification

Change (`git diff PRE_EVENT_B EVENT_B -- event-a/design/src/main`): `ConstPath.java` +3 lines, `after/ConstDeclNode.java` +11/-1,
new `v2/ConstValueAssigner.java` (31 lines, bounded model of V2's caller, written as V2's snippet reads). No new class
hierarchy, no pattern.

| State | Tests | Result | Evidence |
|---|---|---|---|
| `PRE_EVENT_B` | 18 Week 9 tests | 18 pass | rerun at the start of Event B |
| prediction + defect tests, no fix (`0e4ab59`) | 18 + 7 Event B | 20 pass, **5 fail** (D1 NPE; 4 x D2 "nothing was thrown") | `event-b/evidence/defects-before-fix.txt` |
| `EVENT_B` | 18 + 7 | **25 pass, 0 fail**; Week 9 test files unchanged (`git diff PRE_EVENT_B -- event-a/design/src/test/java/p17/v3` is empty) | `event-b/evidence/tests-after-fix.txt` |
| planner | 6 Python tests (Event A's 15 still pass) | pass | `event-b/analysis/tests/` |

Run note: the tests were compiled with `javac --release 17` and run on the JUnit Platform (Jupiter 5.8.2) because Maven Central
was unreachable from the run environment. A group member should rerun `cd event-a/design && mvn test` (expect 25) before FINAL.

## 4. Reprioritised backlog (one sprint = 5 units)

`python3 event-b/analysis/event_b_plan.py` (output: `event_b_plan.csv`, `event_b_budget_sensitivity.csv`, `evidence/plan-output.txt`).
Technical rule = the frozen Event A rule; sizes are our ordinal estimates (S=1, M=2, L=4).

| Item | Technical rank | Negative-variant Urgency (M2 data) | Sentiment rank | Technical sprint |
|---|---|---|---|---|
| D1 null at V2 call site | 1 | - | 1 | yes |
| D2 `::`/blank in ConstPath | 2 | - | 2 | yes |
| V4 plot-type if/else (OCP) | 3 | 2.379 | 5 | yes |
| V3-R2 split ConstDecl | 4 | 2.733 | 3 | no (L, does not fit) |
| V2 value callback | 5 | 2.552 | 4 | yes |
| V1 regression-only flags | 6 | 2.267 | 6 | no |

At exactly 5 units both orders select the same four items, but in a different order (V2 before V4). At 4 units the sentiment
plan takes V2 + V1 and drops V4's OCP problem; at 6-7 units it spends the budget on the full split (R2).

## 5. Where negative wording would have changed the decision incorrectly

1. **V3 framing (our own Week 9 record).** The original V3 comment is the neutral one: constNode and name "never exist at the
   same time", and both fields are `final` (Table 2). "Never in sync" comes from the ChatGPT-generated negative variant. Week 9
   (`M4-DESIGN.md`) quoted the negative variant, so it modelled a setter-driven sync bug. The real pressure is two mutually exclusive
   representations in one class, and D1 is that pressure surviving in Week 9's null shim.
2. **V2.** The negative variant ("This is frustrating!") raises Urgency by +0.99, the largest gap in the M2 data
   (`event-a/analysis/event_a_result.csv`). It moves a low-cost efficiency TODO above V4's design violation.
3. **V3's "should have been divided".** The negative wording pushes the full split forward; our tests show D1 and D2 do not
   need it.

Note: the tracker's Event A result says V1 was made more urgent by negative wording. The Event A output does not support that:
negative V1 is rated lower than neutral V1 (-0.15, `event-a/README.md`). The wording effect in this backlog is on V2.

## 6. Conclusion

**Week 9 decision: partly supported.** The intervention holds: both defects were fixed locally, with no split and no change to the
18 Week 9 tests, as predicted. But Week 9's justification rested partly on the negative wording ("never in sync"). Also, its
compatibility shim (null for simple declarations) was the cause of D1, so we adapted it (`path()`, `getConstNode()` deprecated)
rather than revising it. **Trade-off / anti-pattern risk still remaining:** two accessors for one concept, and null used as a type
flag for remaining callers of `getConstNode()`, until they migrate; the split (R2) stays on the backlog as the way to remove it.
