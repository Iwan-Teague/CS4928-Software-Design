# M4: design pressure and smallest intervention (P17, Week 9, PRE_EVENT_B)

Brief requirement for week 9: "Identify the concrete design pressure, compare at least two realistic responses
including no structural change where appropriate, implement/analyse the smallest justified intervention, and
verify it." Tag: `PRE_EVENT_B`. This file and the tests it cites are the frozen state before the Week 10
Event B response (due 2026-11-13 18:00), which is not part of this tag.

## The concrete design pressure

Vignette 3's FIXME (P17 vignette set; filtered text quoted in the source): "ConstDecl should be divided into
distinct classes. constNode and name are never in sync."

Made concrete in the bounded model
`event-a/design/src/main/java/p17/v3/before/ConstDeclNode.java` (a rewrite written for this exercise, not the
original project's source code):

- the constant's name is stored twice: in the `name` field and inside `constNode`;
- nothing ties them together: `setConstNode` updates only `constNode`, `setName` updates only `name`;
- `qualifiedName()` mixes both sources, so a reader can get a name that disagrees with the constant's actual path.

Impact: any downstream consumer (resolver, printer, serialiser) can read a stale name after a one-sided update.
Complexity: two fields where one suffices. This is the pressure Event A already ranked first on technical
evidence alone: the technical-only script puts Vignette 3 at rank 1 with and without sentiment features
(`event-a/analysis/event_a_result.csv`).

## Responses compared

| Response | What it is | Cost | Decision |
|---|---|---|---|
| R0: no structural change | Keep both fields; document the invariant and check it at call sites | Smallest change, but the drift stays possible at every write site: every future setter must remember to check. `BeforeSyncBugTest` shows the failure mode - a seeded 1000-step random update sequence breaks `name == constNode.name()` at step 7. | Rejected as the end state: the bug class survives every unguarded write. Kept as the characterisation baseline. |
| R1: remove the duplicated field - the smallest justified intervention | One source of truth (`constNode`): `getName()` is derived from it, every update goes through it, a simple declaration becomes a `ConstPath` with an empty scope instead of a null `constNode` | About 60 lines including tests; the constructor now rejects a mismatched name/`constNode` instead of accepting it silently; public method signatures unchanged | **Chosen.** Fixes the pressure at its root without new abstractions. Proportionate to a two-field bug: impact, complexity and effort are all small and known (the 30 October mail asks for exactly this kind of technical evidence). |
| R2: the FIXME's full suggestion - split `ConstDecl` into distinct classes | Separate types for scoped and simple declarations | Touches every caller and grows the API surface; nothing in the model shows the split earning its keep yet | Deferred: FIXME kept in the `after/` source until there is evidence the extra structure is needed. |

## The intervention and its verification

`event-a/design/src/main/java/p17/v3/after/ConstDeclNode.java` implements R1. No design pattern is introduced:
the problem is one duplicated field, not missing architecture.

Verified 2026-11-06, `cd event-a/design && mvn test`: 18 tests, 0 failures (JUnit 5, Maven 3.10.0, Java 21):

- `BeforeCharacterisationTest` (4) and `AfterCharacterisationTest` (4): behaviour preserved for callers across
  the change;
- `BeforeSyncBugTest` (4): reproduces the pressure - the invariant breaks at step 7 of the seeded sequence;
- `AfterSyncInvariantTest` (6): the single-source invariant holds after any sequence; 5 of its 6 cases fail if
  pointed at the `before/` class, so the tests discriminate instead of passing trivially.

(Same verification run, Python side: 15 unit tests for the Event A ranking script, green - unrelated to M4's
design claim but part of the same session's checks.)

## Where this leaves the design

R1 removes the sync bug class; R0 documents it; R2 stays open behind the FIXME. If Event B's response needs a
bigger restructuring, the characterisation tests already pin the behaviour any larger change must keep.
