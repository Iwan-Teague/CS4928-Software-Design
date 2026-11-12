package p17.v3;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Characterisation tests: the behaviour callers rely on when the class is used consistently.
 * Written against the BEFORE class first, then run unchanged against the AFTER class
 * (subclasses below). Both must pass: the refactoring must not change this behaviour.
 */
abstract class ConstDeclCharacterisationTest {

    abstract Decl create(String name, ConstPath constNode, Object value);

    @Test @DisplayName("simple declaration FOO = 1")
    public void simpleDeclaration() {
        Decl d = create("FOO", null, 1);
        assertEquals("FOO", d.getName());
        assertNull(d.getConstNode());
        assertFalse(d.isScoped());
        assertEquals("FOO", d.qualifiedName());
        assertEquals(1, d.getValue());
    }

    @Test @DisplayName("scoped declaration A::B::FOO = 2")
    public void scopedDeclaration() {
        ConstPath p = ConstPath.scoped("FOO", "A", "B");
        Decl d = create("FOO", p, 2);
        assertEquals("FOO", d.getName());
        assertEquals(p, d.getConstNode());
        assertTrue(d.isScoped());
        assertEquals("A::B::FOO", d.qualifiedName());
    }

    @Test @DisplayName("setValue replaces the value only")
    public void setValue() {
        Decl d = create("FOO", ConstPath.scoped("FOO", "A"), 1);
        d.setValue("x");
        assertEquals("x", d.getValue());
        assertEquals("FOO", d.getName());
        assertEquals("A::FOO", d.qualifiedName());
    }

    @Test @DisplayName("consistent declarations are in sync")
    public void consistentDeclarationsAreInSync() {
        assertTrue(Decl.inSync(create("FOO", null, 1)));
        assertTrue(Decl.inSync(create("FOO", ConstPath.scoped("FOO", "A"), 1)));
    }
}
