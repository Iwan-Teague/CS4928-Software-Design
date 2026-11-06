package p17.v3;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import p17.v3.after.ConstDeclNode;

import static org.junit.jupiter.api.Assertions.*;

/** The AFTER class keeps name and constNode in sync: one test per bug in BeforeSyncBugTest. */
class AfterSyncInvariantTest {

    @Test @DisplayName("FIXED: setConstNode updates name")
    public void setConstNodeUpdatesName() {
        Decl d = Decl.after("FOO", ConstPath.scoped("FOO", "A"), 1);
        d.setConstNode(ConstPath.scoped("BAR", "A"));
        assertEquals("BAR", d.getName());
        assertEquals("A::BAR", d.qualifiedName());
        assertTrue(Decl.inSync(d));
    }

    @Test @DisplayName("FIXED: setName on a scoped declaration keeps the scope")
    public void setNameKeepsScope() {
        Decl d = Decl.after("FOO", ConstPath.scoped("FOO", "A"), 1);
        d.setName("BAR");
        assertEquals("BAR", d.getName());
        assertEquals("A::BAR", d.qualifiedName());
        assertTrue(Decl.inSync(d));
    }

    @Test @DisplayName("FIXED: constructor rejects a name that contradicts constNode")
    public void constructorRejectsMismatch() {
        assertThrows(IllegalArgumentException.class,
                () -> new ConstDeclNode("FOO", ConstPath.scoped("BAR", "A"), 1));
    }

    @Test @DisplayName("constructor accepts a null name when constNode is given")
    public void nullNameWithConstNode() {
        Decl d = Decl.after(null, ConstPath.scoped("FOO", "A"), 1);
        assertEquals("FOO", d.getName());
    }

    @Test @DisplayName("setConstNode(null) turns it back into a simple declaration")
    public void setConstNodeNull() {
        Decl d = Decl.after("FOO", ConstPath.scoped("FOO", "A"), 1);
        d.setConstNode(null);
        assertNull(d.getConstNode());
        assertEquals("FOO", d.qualifiedName());
        assertTrue(Decl.inSync(d));
    }

    @Test @DisplayName("FIXED: invariant holds over 1000 random updates (same seed as the bug test)")
    public void randomUpdatesKeepInvariant() {
        assertEquals(-1, InvariantFuzz.firstViolation(Decl::after, 20261106L, 1000));
    }
}
