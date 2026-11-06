package p17.v3;

/** Runs the characterisation tests against the BEFORE class. */
class BeforeCharacterisationTest extends ConstDeclCharacterisationTest {
    @Override
    Decl create(String n, ConstPath p, Object v) { return Decl.before(n, p, v); }
}
