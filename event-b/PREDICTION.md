# Event B prediction (P17, G22), written before any Event B test, fix or plan was run

Start state: tag `PRE_EVENT_B`. The Week 9 decision (`M4-DESIGN.md`) is not
edited in this event. Written 2026-11-12, after reading the Event B sheet and Table 2 of the paper, before writing any code.

## The pressure, made concrete

Event B gives a fixed one-sprint budget and two new defects in the same area. The area is `ConstDeclNode`: Vignette 2 and
Vignette 3 are both comments on it (Table 2: V2 is the caller `Node constNode = constDeclNode.getConstNode();`, V3 is the class).
The sheet does not name the defects, so we define two that can occur in our bounded model at `PRE_EVENT_B`:

- **D1 (V2 call site).** A value-assignment pass written the way V2's snippet reads (`getConstNode()`, then use it) crashes on a
  simple declaration `FOO = 1`, because the Week 9 class still returns `null` from `getConstNode()` for simple declarations
  (kept on purpose for caller compatibility).
- **D2 (single source of truth).** `ConstPath` accepts a name or scope segment that contains `::` or is blank. `setName("B::FOO")`
  gives an unscoped constant whose qualified name looks scoped (the name/path invariant from Week 9 breaks again), and
  `scoped("FOO", "A::B")` prints the same as `scoped("FOO", "A", "B")` but is a different path.

## Prediction

1. The pressure lands on the **null-means-simple convention kept by the Week 9 compatibility shim** (D1) and on **input
   validation of `ConstPath`** (D2), not on the one-field structure of `ConstDeclNode`.
2. Both defects reproduce as failing tests on the `PRE_EVENT_B` code.
3. Both are fixable without splitting the class: at most 3 production files change (`ConstPath`, `ConstDeclNode`, the V2
   caller), and all 18 `PRE_EVENT_B` tests pass **unchanged**.
4. Reprioritising with the frozen Event A technical rule, the sprint takes D1, D2, then V4, then V2; the class split (R2) and V1
   are deferred. A plan ordered by the negative-variant Urgency means (what the emotional comments make people feel) puts
   V2 before V4 and pulls the full split (R2) forward.

## Decision rule for the Week 9 decision (fixed now)

- **Supported:** D1 and D2 fixed with no split and no change to any existing test.
- **Partly supported:** fixed with no split, but the Week 9 shim or an existing test has to change, or the Week 9
  justification turns out to rest on evidence the event weakens.
- **Revise:** D1 or D2 cannot be fixed without the split (R2).

## Planning inputs (fixed now)

- Technical rule: the Event A rule, unchanged (`event-a/analysis/event_a.py`): lexicographic on (correctness risk, design
  violation, production code). Ties: smaller size first, then item id.
- Size: ordinal estimate, S = 1, M = 2, L = 4 units; 1 unit is about one R1-sized change (about 60 lines with tests). These are
  our estimates, not measurements, apart from D1/D2 which are measured after the fix.
- Budget: one sprint = 5 units. Greedy: take items in priority order if they still fit. Sensitivity: 3 to 8 units.
- Sentiment counterfactual: defects first in both plans; debt items then ordered by the M2 Urgency mean of the negative variant.
