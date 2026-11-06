package p17.v3.after;

import p17.v3.ConstPath;

import java.util.Objects;

/**
 * AFTER: the same public methods as {@link p17.v3.before.ConstDeclNode}, with the duplicated
 * state removed.
 *
 * Refactoring: the constant's name now has one source of truth, {@code constNode}.
 * {@link #getName()} is derived from it, and every update goes through it, so the
 * two can no longer disagree. A simple declaration (FOO = 1) is stored as a
 * ConstPath with an empty scope instead of a null constNode.
 *
 * No design pattern is introduced: the problem is one duplicated field. The class split
 * suggested in the FIXME is deferred until there is evidence it is needed.
 */
public class ConstDeclNode {
    private ConstPath constNode;   // never null
    private Object value;

    /**
     * Same signature as before. A null constNode means a simple declaration. If both
     * arguments are given they must agree; the old class accepted a mismatch silently.
     */
    public ConstDeclNode(String name, ConstPath constNode, Object value) {
        if (constNode == null) {
            this.constNode = ConstPath.simple(name);
        } else {
            if (name != null && !name.equals(constNode.name())) {
                throw new IllegalArgumentException(
                        "name '" + name + "' does not match constNode '" + constNode + "'");
            }
            this.constNode = constNode;
        }
        this.value = value;
    }

    public String getName() { return constNode.name(); }

    /** Returns null for a simple declaration, exactly as before, so callers are unaffected. */
    public ConstPath getConstNode() { return constNode.isScoped() ? constNode : null; }

    public Object getValue() { return value; }

    public boolean isScoped() { return constNode.isScoped(); }

    public String qualifiedName() { return constNode.toString(); }

    /** A null argument turns the declaration back into a simple one, keeping the current name. */
    public void setConstNode(ConstPath constNode) {
        this.constNode = constNode != null ? constNode : ConstPath.simple(getName());
    }

    /** Renames the constant and keeps its scope. */
    public void setName(String name) {
        this.constNode = new ConstPath(constNode.scope(), Objects.requireNonNull(name, "name"));
    }

    public void setValue(Object value) { this.value = value; }
}
