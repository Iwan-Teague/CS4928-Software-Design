# Event B – P17, G22: Fixed Sprint Budget and Two New Defects in ConstDeclNode

Every claim in this write-up is linked to its evidence (file, commit, tag or command) in [`EVIDENCE-INDEX.md`](EVIDENCE-INDEX.md).

## 1. Starting Point and Prediction

We started Event B from the `PRE_EVENT_B` Git tag, which contains our original Week 9 design decision (`M4-DESIGN.md`). We left that decision unchanged.

The Week 9 design is the Vignette 3 refactoring (R1) that we first built for Event A on 6 November (commit `3eb0d4a`) and recorded as our M4 decision later the same day (commit `18f6ff7`, `M4-DESIGN.md`). The M4 commit added only that document; no code or tests changed between the two commits. Tag `PRE_EVENT_B` (`f1d8b89`) freezes this state. Our frozen M4 tracker entry therefore cites Event A evidence. Event B starts from that frozen state.

Before running the defect tests or the fix, we wrote down our predictions and agreed on how we would judge the results. This was saved in `event-b/PREDICTION.md` and tagged as `EVENT_B_PREDICTION` (commit `fab93f0`), which comes before the commits that added the defect tests (`9fe8adb`) and the fix (`874c055`) in the history.

Once the work was complete, we saved the first version of this response under the `EVENT_B` tag (commit `874c055`, 12 November). The code, tests and evidence files from that tag have not been changed. On 13 November we only added files: a wording check (`event-b/analysis/wording_only_plan.py`, its tests and two CSV outputs) and a Maven test log (`event-b/evidence/mvn-test-2026-11-13.txt`). This write-up was reworded for readability on 13 November; the current text is in the `event-b/` folder. `event-b/PREDICTION.md` is the text exactly as tagged `EVENT_B_PREDICTION`.

### What Problems Were We Expecting?

Event B gave us:
- A fixed budget of one sprint.
- Two new defects affecting the same area of the code.
- The need to reprioritise our remaining technical debt.
- The need to explain how negative or emotional wording could lead to the wrong decisions.

Both new defects related to `ConstDeclNode`, which is the class discussed in Vignettes 2 and 3 of the research paper.

The instructions didn't specify exactly what the defects should be, so we defined two realistic problems based on our existing code.

**Defect 1 (D1 – Vignette 2 / Calling Code)**

The first problem was that code trying to read a constant's value could crash.

For a simple declaration like `FOO = 1`, calling `getConstNode()` returns `null` because we deliberately kept this behaviour in Week 9 to avoid breaking existing code.

However, if another part of the program tries to use that returned value without checking for `null`, it causes a crash (NullPointerException).

**Defect 2 (D2 – Keeping Constant Paths Consistent)**

The second problem was that `ConstPath` allowed invalid names and scope values.

For example:
- A constant name could contain `::`, even though this should only be used to separate scopes.
- Empty names or scope values were allowed.
- Two different ways of defining a constant path could produce the same displayed result while being stored differently internally.

For example, `scoped("FOO", "A::B")` and `scoped("FOO", "A", "B")` produce the same qualified name, but represent different paths.

This breaks the rule we established in Week 9 that a constant's name and its path should always agree.

### What Did We Predict?

We predicted that both problems would come from the existing `null` behaviour and the lack of input validation in `ConstPath`, rather than the basic one-field structure of `ConstDeclNode`.

We also predicted that:
- Both defects would be reproducible through failing tests.
- Both could be fixed by changing no more than three production code files.
- All 18 existing Week 9 tests would pass without any changes.
- The sprint priorities would be D1, D2, V4 and then V2.
- Splitting the class (R2) and V1 would be postponed.

## 2. Solutions We Considered

We considered three different ways of dealing with the problems.

### Option B0 – Keep the Existing Structure and Add Checks Everywhere

The first option was to leave the class as it was and add checks wherever `getConstNode()` was used.

We would also validate constant names at each place they were created.

The advantage was that it required the smallest change to the existing class.

However, the problem was that every current and future caller would need to remember to perform these checks. If someone forgot, the same problems could happen again.

This is a shotgun-surgery risk: the same check has to be repeated in many places. Our Week 9 record makes the same point about setters ("every future setter must remember to check", `M4-DESIGN.md`, option R0).

**Decision: Rejected.**

### Option B1 – Fix the Problems at Their Source

The second option was to fix the problems directly in the classes responsible for them.

We made three main changes:
- `ConstPath` now checks every name and scope part, rejecting empty values and values containing `::`.
- `ConstDeclNode` now has a new `path()` method that always returns a valid, non-null path.
- We kept the old `getConstNode()` method for compatibility but marked it as `@Deprecated`. The Vignette 2 caller was changed to use the new `path()` method instead.

This means we have two ways of accessing the path for now. Existing code can continue using the old method, while new code can use the safer alternative.

One other change is that invalid inputs that were previously accepted now throw an `IllegalArgumentException`.

**Decision: Chosen.**

We chose this option because it fixes both problems locally without requiring a major redesign of the class.

### Option B2 – Split ConstDecl Into Separate Classes

The third option was to split `ConstDecl` into separate classes for simple and scoped constants.

This was the original idea discussed in Week 9 (R2).

The advantage is that it would completely remove the need to use `null` to represent a simple constant declaration.

However, it would require changes to every part of the code that interacts with these classes. We estimated that it would use around 4 of our 5 available sprint units.

Since our chosen solution already fixes both defects, there wasn't enough justification for making such a large change.

**Decision: Deferred again.**

## 3. Implementation and Testing

We implemented our chosen solution without splitting `ConstDeclNode` into multiple classes.

### What We Changed

The changes were:

- `ConstPath.java`: Added 3 lines to validate names and scope values.
- `after/ConstDeclNode.java`: Added 11 lines and removed 1 line to introduce the new `path()` method and deprecate the old accessor.
- `v2/ConstValueAssigner.java`: Added a new 31-line class representing the Vignette 2 calling code, written to behave like the example in the paper.

Overall, we made changes to three production code files.

We did not introduce a new class hierarchy or use a design pattern.

### Testing Results

We tested the code at three different stages to see whether our predictions were correct.

| Stage | Tests | Result |
|---|---|---|
| Before Event B (`PRE_EVENT_B`) | 18 Week 9 tests | All 18 passed |
| Before fixing the defects | 18 existing + 7 new tests | 20 passed, 5 failed |
| After our fixes (`EVENT_B`) | 18 existing + 7 new tests | All 25 passed |

**Before the fixes:**

The new tests successfully reproduced both defects:
- D1 caused a NullPointerException when trying to read a simple constant.
- D2 caused four tests to fail because invalid inputs were not rejected when expected.

This confirmed that both problems existed in our original code.

**After the fixes:**

All 25 tests passed, with no failures.

Importantly, we did not have to change any of the original 18 Week 9 tests. We checked this using Git, and there were no differences in the original test files.

We also tested our Python planning tool. All 6 new Event B planner tests passed, and the original 15 Event A tests continued to pass (`python3 -m unittest discover -s event-b/analysis/tests`; `cd event-a/analysis && python3 -m unittest tests.test_event_a`). On 13 November we added 7 tests for the wording check described in section 4; all pass.

### How We Ran the Tests

On 12 November we compiled the tests using `javac --release 17` and ran them using the JUnit Platform (Jupiter 5.8.2), because Maven Central was unreachable in our testing environment (`event-b/evidence/defects-before-fix.txt`, `event-b/evidence/tests-after-fix.txt`).

On 13 November we also ran the project's own build, `cd event-a/design && mvn test`: 25 tests, 0 failures, 0 errors (`event-b/evidence/mvn-test-2026-11-13.txt`). The Java sources and tests are identical to those at tag `EVENT_B`.

## 4. Reprioritising the Technical Debt

We now needed to decide which technical debt items should be addressed within our one-sprint budget of 5 units.

We used our original Event A prioritisation method, which ranks work based on:
1. Correctness risk.
2. How much the design is being violated.
3. How much production code needs to change.

We also compared this with an alternative plan based on how negatively people described the technical debt.

The task sizes were estimated as follows:

- Small (S) = 1 unit.
- Medium (M) = 2 units.
- Large (L) = 4 units.

### Comparing the Two Prioritisation Methods

| Item | Technical Priority | Negative Urgency Score | Sentiment Priority | Included in Technical Sprint? |
|---|---:|---:|---:|---|
| D1 – Null value at V2 call site | 1 | - | 1 | Yes |
| D2 – Invalid values in ConstPath | 2 | - | 2 | Yes |
| V4 – Plot-type if/else (OCP) | 3 | 2.379 | 5 | Yes |
| V3-R2 – Split ConstDecl | 4 | 2.733 | 3 | No |
| V2 – Value callback | 5 | 2.552 | 4 | Yes |
| V1 – Regression-only flags | 6 | 2.267 | 6 | No |

The technical priority column shows the order produced by our original Event A rules.

The negative urgency score comes from the average Urgency ratings for the negative versions of the M2 comments.

### What Happens With a 5-Unit Sprint Budget?

Using our technical prioritisation method, we select:

1. D1 – Fix the potential crash.
2. D2 – Fix invalid constant paths.
3. V4 – Address the plot-type if/else design issue.
4. V2 – Address the value callback.

These are the four items selected within the 5-unit budget.

If we instead prioritise using negative sentiment, we select the same four items at exactly 5 units, but the order changes. V2 moves ahead of V4.

However, changing the sprint budget produces more noticeable differences:

- **At 4 units:** The sentiment-based plan selects V2 and V1, meaning V4's design problem is left out.
- **At 6–7 units:** The sentiment-based plan brings forward the full class split (R2), using more of the available budget.

These differences are not all caused by wording. As a check we added after seeing the results (it was not part of our prediction), we ordered the same plan by the neutral-variant means instead (`event-b/analysis/wording_only_plan.py`, output in `event-b/analysis/event_b_wording_only_plan.csv`). That plan also leaves V4 out at 4 units and also brings R2 forward at 6 units, because V3 is rated urgent with either wording (2.733 negative, 2.759 neutral). The only differences between the negative-based and neutral-based plans are at 3, 5 and 7 units, and each is a single swap: V2 (negative) takes the place of V1 (neutral). So the effect of wording on the plan is real but narrow: it moves V2 up, matching the V2 effect we measured in Event A (+0.985). The other differences come from planning by developers' ratings rather than by our technical rule.

## 5. Where Negative Wording Could Have Led Us to the Wrong Decision

We identified three examples where our planning or our reading of the evidence could have gone wrong. Two come from negative wording (V3's description in Week 9, and V2's urgency). One comes from planning by urgency ratings, whatever the wording (V3 and the class split).

### 1. V3 – The Way We Described the Class in Week 9

The original V3 comment in the research paper was relatively neutral. It explained that `constNode` and `name` never exist at the same time and that both fields are `final`.

However, the negative version generated by ChatGPT changed this to wording suggesting that the two fields were "never in sync".

In our Week 9 decision (`M4-DESIGN.md`), we quoted this negative version.

This made us think the main problem was keeping two fields synchronised when their values changed.

However, the actual issue is that the class uses two different representations for simple and scoped constants.

The new D1 defect demonstrates that this problem was still present in our Week 9 solution because we continued using `null` to represent simple declarations.

In other words, the negative wording made us focus on the wrong aspect of the design problem.

### 2. V2 – Negative Wording Increased Its Urgency

The negative version of V2 included the phrase "This is frustrating!".

This increased its average Urgency score by 0.99 compared with the neutral version. This was the largest difference in the M2 data.

As a result, V2 moves ahead of V4 in the sentiment-based prioritisation.

The problem is that V2 is mainly an efficiency improvement, whereas V4 represents a design violation.

By giving V2 a higher priority simply because of how negatively it was described, we could end up addressing a less important problem before a more significant design issue. (At our 5-unit budget this changed the order of the work, not the set of items: the negative-based plan selects the same four items as the technical plan.)

### 3. V3 – Planning by urgency ratings would have pulled the class split forward

Developers rate V3 as the most urgent item with either wording (2.733 for the negative version, 2.759 for the neutral one). A plan led by urgency ratings therefore brings the full class split (R2) forward at 6–7 units, whichever wording is used. This is not a wording effect.

However, our testing showed that both new defects could be fixed without splitting the class. A plan led by urgency ratings would have spent 4 of its 6 units on a redesign that the defects did not need.

### An Important Correction From Event A

Our Event A and M4 tracker entries say that negative wording made V1 seem more urgent.

Our own Event A numbers do not support this. The negative version of V1 scored 2.267 (n = 30) and the neutral version 2.414 (n = 29), a difference of −0.15. That is indistinguishable from zero: with groups this size and ratings spread by about 1 point, only differences of about 0.7 or more could be detected (`event-b/analysis/event_b_wording_effects.csv`). Our data therefore neither show nor rule out a wording effect on V1, and the earlier claim that wording inflated V1 is not supported. V1 was second in the M2 ranking only by 0.017 over V4 (2.339 against 2.322), too small to read anything into.

The clear wording effect in our backlog is on V2 (negative 2.552, neutral 1.567, difference +0.985). All numbers come from the authors' survey export and can be re-run with `python3 event-a/analysis/event_a.py`, which writes `event-a/analysis/event_a_result.csv`. The earlier tracker entries are frozen and are left unchanged.

## 6. Conclusion

**Our Week 9 decision is partly supported.**

Our main prediction was correct: we successfully fixed both new defects without splitting `ConstDeclNode` into multiple classes.

We also managed to do this without changing any of the original 18 Week 9 tests. All 25 tests passed after the fixes.

This supports our original decision to keep the existing class structure rather than immediately splitting it.

However, there are two reasons why we cannot say the Week 9 decision was completely supported:

- Part of our original justification relied on the negative wording in V3 ("never in sync"), which did not accurately describe the real design problem.
- Our original compatibility solution, where `getConstNode()` returns `null` for simple declarations, directly caused the new D1 defect.

We addressed this by introducing the new `path()` method and marking `getConstNode()` as deprecated, rather than completely changing the class structure.

### Remaining Problems and Trade-offs

Although our fixes solved both defects, there are still some issues with the current design.

We now have two methods for accessing the same concept: `path()` and `getConstNode()`.

We also still use `null` as a way of identifying simple declarations for any existing code that continues to use `getConstNode()`.

This means the original design problem has not been completely removed.

The full class split (R2) remains on our technical debt backlog as a possible future solution. It would remove the need for the `null` convention, but we have deferred it because the current problems could be fixed with much smaller changes.

**Overall, Event B supports our decision to avoid a full class split for now, but it also shows that our Week 9 compatibility solution introduced a new problem and that some of our original reasoning was influenced by negative wording rather than the actual design issue.**
