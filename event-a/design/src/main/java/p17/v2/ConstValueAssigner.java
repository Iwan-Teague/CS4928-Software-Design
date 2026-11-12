package p17.v2;

import p17.v3.ConstPath;
import p17.v3.after.ConstDeclNode;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Bounded model of Vignette 2's caller (P17, Table 2), added in Event B; not the original project's code.
 * A pass that records each constant's value under its scope, written the way V2's snippet reads:
 * cast the node, take getConstNode(), use it.
 */
public class ConstValueAssigner {
    private final Map<List<String>, Map<String, Object>> scopes = new HashMap<>();

    public void assign(Object node) {
        ConstDeclNode constDeclNode = (ConstDeclNode) node;
        ConstPath constNode = constDeclNode.getConstNode();
        // TODO: callback for value would be more efficient, but unlikely to be a big cost (constants are rarely assigned)
        scopes.computeIfAbsent(constNode.scope(), k -> new HashMap<>())
              .put(constNode.name(), constDeclNode.getValue());
    }

    /** Value assigned to the constant {@code name} in {@code scope}, or null if none. */
    public Object value(List<String> scope, String name) {
        Map<String, Object> s = scopes.get(scope);
        return s == null ? null : s.get(name);
    }
}
