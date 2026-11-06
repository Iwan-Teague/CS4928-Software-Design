package p17.v3.before;

import p17.v3.ConstPath;

/**
 * BEFORE: bounded model of Vignette 3 (P17, Table 2), not the original project's code.
 *
 * FIXME (filtered vignette text): "ConstDecl should be divided into distinct classes.
 * constNode and name are never in sync."
 *
 * The constant's name is stored twice: in {@code name} and inside {@code constNode}.
 * Nothing ties the two together, so they drift apart as soon as one is changed on its own.
 */
public class ConstDeclNode {
    private String name;
    private ConstPath constNode;   // null for a simple declaration (FOO = 1)
    private Object value;

    public ConstDeclNode(String name, ConstPath constNode, Object value) {
        this.name = name;          // no check that name matches constNode.name()
        this.constNode = constNode;
        this.value = value;
    }

    public String getName() { return name; }

    public ConstPath getConstNode() { return constNode; }

    public Object getValue() { return value; }

    public boolean isScoped() { return constNode != null && constNode.isScoped(); }

    /** Fully qualified name, built from constNode when present, otherwise from name. */
    public String qualifiedName() {
        return constNode != null ? constNode.toString() : name;
    }

    public void setConstNode(ConstPath constNode) { this.constNode = constNode; } // name not updated

    public void setName(String name) { this.name = name; }                        // constNode not updated

    public void setValue(Object value) { this.value = value; }
}
