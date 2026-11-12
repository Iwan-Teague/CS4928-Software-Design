package p17.v3;

import java.util.List;
import java.util.Objects;

/**
 * The left-hand side of a constant declaration: optional scope plus the constant's own name.
 * {@code FOO = 1} has an empty scope; {@code A::B::FOO = 1} has scope [A, B] and name FOO.
 * Immutable.
 */
public final class ConstPath {
    private final List<String> scope;
    private final String name;

    public ConstPath(List<String> scope, String name) {
        this.scope = List.copyOf(Objects.requireNonNull(scope, "scope"));
        this.scope.forEach(ConstPath::requireName);   // Event B (D2): scope segments obey the same rule as names
        this.name = requireName(name);
    }

    public static ConstPath simple(String name) {
        return new ConstPath(List.of(), name);
    }

    public static ConstPath scoped(String name, String... scope) {
        return new ConstPath(List.of(scope), name);
    }

    public List<String> scope() { return scope; }

    public String name() { return name; }

    public boolean isScoped() { return !scope.isEmpty(); }

    @Override public boolean equals(Object o) {
        return o instanceof ConstPath p && p.scope.equals(scope) && p.name.equals(name);
    }

    @Override public int hashCode() { return Objects.hash(scope, name); }

    @Override public String toString() {
        return scope.isEmpty() ? name : String.join("::", scope) + "::" + name;
    }

    /** One path part: not null, not blank, and no "::" (Event B, D2: otherwise two paths can print the same). */
    static String requireName(String name) {
        Objects.requireNonNull(name, "name");
        if (name.isBlank()) throw new IllegalArgumentException("name must not be blank");
        if (name.contains("::")) throw new IllegalArgumentException("'" + name + "' must not contain '::'");
        return name;
    }
}
