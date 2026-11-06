package p17.v3;

import java.util.Random;

/** Applies a seeded random sequence of updates and reports the first step that breaks sync. */
final class InvariantFuzz {
    interface Factory { Decl create(String name, ConstPath p, Object v); }

    private static final String[] NAMES = {"FOO", "BAR", "BAZ"};
    private static final String[] SCOPES = {"A", "B"};

    /** @return index of the first operation after which {@link Decl#inSync} is false, or -1. */
    static int firstViolation(Factory f, long seed, int steps) {
        Random r = new Random(seed);
        Decl d = f.create("FOO", null, 0);
        for (int i = 0; i < steps; i++) {
            String n = NAMES[r.nextInt(NAMES.length)];
            switch (r.nextInt(3)) {
                case 0 -> d.setName(n);
                case 1 -> d.setConstNode(r.nextBoolean()
                        ? ConstPath.scoped(n, SCOPES[r.nextInt(SCOPES.length)])
                        : ConstPath.simple(n));
                default -> d.setValue(i);
            }
            if (!Decl.inSync(d)) return i;
        }
        return -1;
    }

    private InvariantFuzz() {}
}
