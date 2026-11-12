package p17.v2;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import p17.v3.ConstPath;
import p17.v3.after.ConstDeclNode;

import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Event B: the two new defects, written as the behaviour we want. At PRE_EVENT_B the D1 test and the
 * D2 tests fail (run log: event-b/evidence/defects-before-fix.txt); after the fix they pass.
 */
class EventBDefectTest {

    // ---- D1: V2's call site crashes on a simple declaration (getConstNode() is null for FOO = 1)

    @Test @DisplayName("D1: assigning a simple declaration FOO = 1 records its value")
    public void d1SimpleDeclarationIsAssigned() {
        ConstValueAssigner a = new ConstValueAssigner();
        a.assign(new ConstDeclNode("FOO", null, 1));
        assertEquals(1, a.value(List.of(), "FOO"));
    }

    @Test @DisplayName("D1 control: a scoped declaration A::FOO = 2 is assigned in scope A")
    public void d1ScopedDeclarationIsAssigned() {
        ConstValueAssigner a = new ConstValueAssigner();
        a.assign(new ConstDeclNode("FOO", ConstPath.scoped("FOO", "A"), 2));
        assertEquals(2, a.value(List.of("A"), "FOO"));
        assertNull(a.value(List.of(), "FOO"));
    }

    // ---- D2: ConstPath accepts '::' or blank parts, so the single source of truth can lie

    @Test @DisplayName("D2: a constant name containing '::' is rejected by the constructor")
    public void d2ConstructorRejectsSeparatorInName() {
        assertThrows(IllegalArgumentException.class, () -> new ConstDeclNode("B::FOO", null, 1));
    }

    @Test @DisplayName("D2: setName with '::' is rejected and leaves the declaration unchanged")
    public void d2SetNameRejectsSeparator() {
        ConstDeclNode d = new ConstDeclNode("FOO", null, 1);
        assertThrows(IllegalArgumentException.class, () -> d.setName("B::FOO"));
        assertEquals("FOO", d.getName());
        assertEquals("FOO", d.qualifiedName());
        assertFalse(d.isScoped());
    }

    @Test @DisplayName("D2: a scope segment containing '::' is rejected (no look-alike paths)")
    public void d2ScopeSegmentWithSeparatorRejected() {
        assertThrows(IllegalArgumentException.class, () -> ConstPath.scoped("FOO", "A::B"));
    }

    @Test @DisplayName("D2: a blank scope segment is rejected")
    public void d2BlankScopeSegmentRejected() {
        assertThrows(IllegalArgumentException.class, () -> ConstPath.scoped("FOO", ""));
        assertThrows(IllegalArgumentException.class, () -> ConstPath.scoped("FOO", "A", " "));
    }

    @Test @DisplayName("D2 control: valid multi-segment paths are still accepted")
    public void d2ValidPathsStillAccepted() {
        assertEquals("A::B::FOO", ConstPath.scoped("FOO", "A", "B").toString());
        assertEquals("FOO", ConstPath.simple("FOO").toString());
    }
}
