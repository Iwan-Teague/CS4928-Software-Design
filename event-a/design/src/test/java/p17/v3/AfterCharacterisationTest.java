package p17.v3;

/** Runs the characterisation tests against the AFTER class. */
class AfterCharacterisationTest extends ConstDeclCharacterisationTest {
    @Override
    Decl create(String n, ConstPath p, Object v) { return Decl.after(n, p, v); }
}
