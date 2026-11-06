package p17.v3;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Reproduces the Vignette 3 defect on the BEFORE class. These tests PASS because the bug
 * exists. Each one is the "fails on the old code" half of the evidence: the matching test in
 * AfterSyncInvariantTest asserts the opposite and passes on the AFTER class.
 */
class BeforeSyncBugTest {

    @Test @DisplayName("BUG: setConstNode leaves name stale")
    public void setConstNodeLeavesNameStale() {
        Decl d = Decl.before("FOO", ConstPath.scoped("FOO", "A"), 1);
        d.setConstNode(ConstPath.scoped("BAR", "A"));
        assertEquals("FOO", d.getName());
        assertEquals("A::BAR", d.qualifiedName());
        assertFalse(Decl.inSync(d));
    }

    @Test @DisplayName("BUG: setName on a scoped declaration leaves constNode stale")
    public void setNameLeavesConstNodeStale() {
        Decl d = Decl.before("FOO", ConstPath.scoped("FOO", "A"), 1);
        d.setName("BAR");
        assertEquals("BAR", d.getName());
        assertEquals("A::FOO", d.qualifiedName());
        assertFalse(Decl.inSync(d));
    }

    @Test @DisplayName("BUG: constructor accepts a name that contradicts constNode")
    public void constructorAcceptsMismatch() {
        Decl d = Decl.before("FOO", ConstPath.scoped("BAR", "A"), 1);
        assertFalse(Decl.inSync(d));
    }

    @Test @DisplayName("BUG: random update sequence breaks the invariant")
    public void randomUpdatesBreakInvariant() {
        assertTrue(InvariantFuzz.firstViolation(Decl::before, 20261106L, 1000) >= 0,
                "expected the old class to go out of sync");
    }
}
