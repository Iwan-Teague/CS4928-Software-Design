package p17.v3;

/**
 * Test-only view of a ConstDeclNode, so the same characterisation tests can run against the
 * before and after classes (they share method names but no Java interface).
 */
public interface Decl {
    String getName();
    ConstPath getConstNode();
    Object getValue();
    boolean isScoped();
    String qualifiedName();
    void setConstNode(ConstPath p);
    void setName(String n);
    void setValue(Object v);

    /** The invariant the FIXME says is broken: name agrees with the declared constant path. */
    static boolean inSync(Decl d) {
        return d.getName().equals(lastSegment(d.qualifiedName()));
    }

    static String lastSegment(String qualified) {
        int i = qualified.lastIndexOf("::");
        return i < 0 ? qualified : qualified.substring(i + 2);
    }

    static Decl before(String name, ConstPath p, Object v) {
        var n = new p17.v3.before.ConstDeclNode(name, p, v);
        return new Decl() {
            public String getName() { return n.getName(); }
            public ConstPath getConstNode() { return n.getConstNode(); }
            public Object getValue() { return n.getValue(); }
            public boolean isScoped() { return n.isScoped(); }
            public String qualifiedName() { return n.qualifiedName(); }
            public void setConstNode(ConstPath x) { n.setConstNode(x); }
            public void setName(String x) { n.setName(x); }
            public void setValue(Object x) { n.setValue(x); }
        };
    }

    static Decl after(String name, ConstPath p, Object v) {
        var n = new p17.v3.after.ConstDeclNode(name, p, v);
        return new Decl() {
            public String getName() { return n.getName(); }
            public ConstPath getConstNode() { return n.getConstNode(); }
            public Object getValue() { return n.getValue(); }
            public boolean isScoped() { return n.isScoped(); }
            public String qualifiedName() { return n.qualifiedName(); }
            public void setConstNode(ConstPath x) { n.setConstNode(x); }
            public void setName(String x) { n.setName(x); }
            public void setValue(Object x) { n.setValue(x); }
        };
    }
}
