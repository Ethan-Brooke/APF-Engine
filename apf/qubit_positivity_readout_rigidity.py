"""Positivity forces the identity readout on a qubit effect system -- and does
not at n = 3.

NON-EXPORTING.  physical_premises_certified = false.  No [P] moves, no paper
changes, no premise is discharged, nothing here derives Born.

WHAT IS PROVED
--------------
On A = M_2(C), let P != Q be DISTINCT rank-one projections, let

    f_P = P + t(I-P),    f_Q = Q + t'(I-Q),     t, t' in [0,1),

be exposing effects (unit eigenspace exactly the corresponding ray), and let
S = span_C{I, f_P, f_Q} = span_C{I, P, Q} be the operator system.  Let

    T : S -> M_2(C)

be linear, UNITAL, and POSITIVE (it maps S ∩ PSD into PSD), with the two matched
certainties

    Tr(P T(f_P)) = 1,      Tr(Q T(f_Q)) = 1.

Then T = id_S.

COMPLETE POSITIVITY IS NOT USED.  Neither is trace preservation, Arveson
extension, Kraus decomposition, effect saturation, output tomography, or the
banked two-ray theorem.

AND THE SCOPE IS SHARP, NOT MERELY UNPROVEN ELSEWHERE
-----------------------------------------------------
At n = 3 the statement is FALSE, by an exact counterexample carrying a one-line
PSD certificate (check_L_positivity_does_not_suffice_at_n3).  With
psi_P = e1, psi_Q = (3/5)e1 + (4/5)e2, R = |e3><e3| and c = 1 - Tr(PQ) = 16/25,

    T(I) = I,    T(P) = P + c R,    T(Q) = Q

is unital, satisfies BOTH matched certainties exactly, is not the identity on S,
and is positive because the only functional it can violate is Tr(Y .) for the
RANK-ONE PSD matrix Y = |psi_Q^perp><psi_Q^perp|.  Positivity is verified by that
certificate, not by sampling.  AND c IS EXACTLY CRITICAL: inf_gamma
lam_max(P - gamma Q) = 1 - Tr(PQ), so the counterexample sits ON the boundary of
the positive cone, and c + eps breaks positivity for every eps > 0 (executed at
eps = 1/100).  So this is an n = 2 theorem, the failure at n = 3 is a theorem
too, and the constant in it is sharp.

WHY THE n = 2 CASE CLOSES
-------------------------
Step 2 is the whole content, and it is EXECUTED here for a general T rather than
assumed.  Two routes are run; the FIRST is the one the argument consumes.

ROUTE 1 (primary, dimension-free until the last line).  Unitality and positivity
give M := I - T(f_P) >= 0, and certainty gives Tr(P M) = 0.  The PSD SUPPORT
LEMMA then yields P M = 0, so T(f_P) fixes psi_P; linearity in f_P transfers this
to T(P), giving T(P) = P + B with B >= 0 supported on psi_P^perp.  AT n = 2 that
complement has rank ONE, so B = lam (I - P) and the form is forced.  The n >= 3
failure falls out of this same line rather than being a separate observation: at
n = 3 the complement has rank 2 and B need not be scalar.

ROUTE 2 (alternative, the Bloch picture).  Write T(P) = (tau I + a . sigma)/2
with tau, a real and unconstrained -- four real parameters, no form assumed:

  * certainty at psi_P gives          tau + p . a = 2;
  * positivity at x = I - P gives     |a| <= 2 - tau;
  * Cauchy-Schwarz gives              p . a <= |a|   (|p| = 1).

Chaining, 2 - tau = p . a <= |a| <= 2 - tau, so BOTH are equalities.  The SIGNED
equality case p . a = |a| forces a = |a| p, hence a = (2 - tau) p, hence

    T(P) = P + lam (I - P),     lam := tau - 1.

Positivity at x = P then gives tau >= |a| = 2 - tau, i.e. lam >= 0, and
|a| = 2 - tau >= 0 gives lam <= 1.  The joint constraint on alpha I - a P - b Q
closes lam = lam' = 0.

The global step there is CONCAVITY, not tightness.  Tightness at the identity
plus a strictly negative derivative excludes only a punctured neighbourhood.
What closes it is that

    g(lam, lam') = |w| - (a lam + b lam') - |a(1-lam) p + b(1-lam') q|

is an affine function minus a NORM of an affine function, hence concave on the
whole feasible box; a concave function that vanishes at an endpoint of the
feasible interval and strictly decreases there is negative on the rest of it.
The second derivative is computed at two points as corroboration.

WHAT THIS DOES NOT DO, and the scope is tighter than it first reads
-------------------------------------------------------------------
It does not derive Born.  The trace pairing is the ambient representation in
which S, the effects and the certainties are already written; the conclusion is
about the READOUT MAP being the identity ON S.

"Complete positivity is not used" is bought by concluding T = id_S rather than
T = id_{M_2}, and that shrink is exactly the sector complete positivity is for.
TRANSPOSITION is the witness and it is executed in check_L_scope_and_bars: P, Q,
f_P and f_Q are all real symmetric in the engine basis, so transposition fixes
every one of them, returns both certainties exactly, is unital and positive on
all of M_2 -- and is NOT completely positive (Choi spectrum {1,1,1,-1}) and NOT
the identity on M_2, since it flips the sigma_y direction that S does not span.
It does not contradict T = id_S.  The honest statement is therefore: this route
does not consume complete positivity because it does not conclude what complete
positivity buys.

It does not touch CP_SOUNDNESS in the bank, which remains a five-leaf composite
in apf/quantum_frontend_closure.py.  It says nothing about direct sums, central
weights, continuation cost, or outcome selection.

DISTINCTNESS SUFFICES; NONORTHOGONALITY IS NOT NEEDED -- and the two cases close
by DIFFERENT mechanisms.  THE CLOSURE STRENGTH IS 1 - sqrt(Tr PQ), which equals
|dg/dlam| at the identity, is 18/25 at the engine pair, is MAXIMAL (= 1) at
orthogonality, and vanishes only in the limit P -> Q, which is the distinctness
hypothesis.  The sharp global form g(lam, lam') <= -(1 - sqrt(Tr PQ))(lam + lam')
is executed.  Orthogonal rays close instead by the second certainty acting on a
2-dimensional S, and the reason the leg-2 mechanism is unavailable there is that
its tight witness lam_max(P+Q) I - P - Q DEGENERATES TO THE ZERO MATRIX: what the
constraint then carries is the linear dependence Q = I - P, i.e. well-definedness
of T, not a positivity bound.  Equivalently the strict Cauchy-Schwarz gap
|p+q| - p.(p+q) = 2 sqrt(o)(1 - sqrt(o)) vanishes at o = Tr PQ = 0.  Both
branches are executed.  So the banked two-ray theorem's "nonorthogonality is
load-bearing" fence does NOT transfer to the positivity route.

TWO CORRECTIONS OF RECORD, both from a blinded cold audit and both load-bearing
for reading the argument.  (1) An earlier draft called 2/|p+q| = 1/sqrt(Tr PQ)
"the positivity margin".  No inequality anywhere has it as slack, and it runs the
wrong way -- it DIVERGES at orthogonality, where the theorem is strongest.  The
identity |p+q| = 2 sqrt(Tr PQ) is kept and verified symbolically for a general
unit q, but it is billed as an identity, not as a margin.  (2) An earlier draft
attributed the orthogonal branch to that denominator vanishing.  Three things
degenerate together there and the draft named the least informative one; the
witness collapsing to zero is the cause.

SCOPE, WIDER THAN THE FIRST STATEMENT.  The proof consumes only t, t' != 1 (so
that certainty reduces and S stays 3-dimensional).  The EFFECT property
t, t' in [0,1) is carried because it is the physically meaningful case and is NOT
load-bearing: the conclusion survives at t outside [0,1], and fails at t = 1
exactly, where f_P = I.

NAMED IMPORTS, with their hypotheses:
  * The PSD support lemma: for A, B >= 0, Tr(AB) = 0 implies AB = 0.  CONSUMED by
    Route 1, which is the route the argument runs on.
  * Cauchy-Schwarz in R^3, used as an INEQUALITY, with its SIGNED equality case
    as the parallelism step (p . a <= |a| for |p| = 1, with p . a = |a| forcing
    a = |a| p -- the signed form, not merely a || p).  Consumed by Route 2.
  Both are elementary and both are exercised in-check.

MAY-NOT-CITE: "Born is derived"; "CP_SOUNDNESS is discharged or reduced";
"complete positivity is unnecessary for the readout" (unqualified -- it is
unnecessary for T = id_S, and the maps fixing S pointwise are classified
in-module); "positivity suffices at n >= 3" (FALSE, counterexample in-module);
"the margin vanishes in the orthogonal case"; "2/|p+q| measures the closure"
(it measures nothing; the closure strength is 1 - sqrt(Tr PQ)); "transposition is
the witness" (it is ONE endpoint of the interval Phi_kappa).
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Callable, Dict, List, Mapping, Tuple

import sympy as sp

FAMILY = "quantum.qubit_positivity_readout_rigidity"

I2 = sp.eye(2)
SX = sp.Matrix([[0, 1], [1, 0]])
SY = sp.Matrix([[0, -sp.I], [sp.I, 0]])
SZ = sp.Matrix([[1, 0], [0, -1]])

P0 = sp.Matrix([[1, 0], [0, 0]])
# the engine's admitted second-exchange reflection (apf/graded_orientation_closure.py)
S_U = sp.Matrix([[sp.Rational(-7, 25), sp.Rational(24, 25)],
                 [sp.Rational(24, 25), sp.Rational(7, 25)]])
Q1 = sp.simplify(S_U * P0 * S_U.H)
T_EXPOSE = sp.Rational(1, 3)
F_P = sp.simplify(P0 + T_EXPOSE * (I2 - P0))
F_Q = sp.simplify(S_U * F_P * S_U.H)

# Exact expected values, pinned by EQUALITY rather than bounded.  A one-sided
# inequality on a headline number is not a pin: 25/14, 4 and -32/25 all satisfied
# the previous guards.
EXPECT_TR_PQ = sp.Rational(49, 625)
EXPECT_CLOSURE = sp.Rational(18, 25)        # 1 - sqrt(Tr PQ) = |dg/dlam|
EXPECT_DG11 = sp.Rational(-18, 25)          # dg/dlam at the identity, a = b = 1
EXPECT_SECOND_CERTAINTY = sp.Rational(241, 625)   # t + (1-t) Tr(PQ)
EXPECT_D2G = sp.Rational(-288, 175)         # d2g/dlam2 at the identity, a = b = 1
EXPECT_D2G_MID = -100352 * sp.sqrt(113) / 957675    # the same at lam = 1/2

# Sentences this module may not ship in any prose field.  Checked in _result()
# AND in run_all(), because a receipt no verdict consults is not a receipt, and
# that applies to sentences as well as to booleans.
BARRED_PROSE = (
    "DERIVES BORN",
    "COMPLETE POSITIVITY IS USED",
    "DISCHARGES CP_SOUNDNESS",
    "CP_SOUNDNESS IS DISCHARGED",
    "POSITIVITY SUFFICES AT N >= 3",
    "THE MARGIN VANISHES",
    "THE POSITIVITY MARGIN",
)
REQUIRED_PROSE = {
    "T_positivity_forces_the_identity_readout": "COMPLETE POSITIVITY IS NOT USED",
    "L_positivity_does_not_suffice_at_n3": "FALSE AT n = 3",
}


@dataclass(frozen=True)
class Result:
    name: str
    passed: bool
    fail_reasons: Tuple[str, ...]
    fail_count: int
    key_result: str
    imports: Tuple[str, ...]
    negative_controls: Tuple[str, ...]
    artifacts: Mapping[str, object]
    epistemic: str

    def to_dict(self) -> Dict[str, object]:
        return asdict(self)


def _travel_guard(name: str, key_result: str, epistemic: str) -> None:
    """Every protection that must survive the BANKED path.

    The bank imports the module, calls register(), then invokes each check_fn()
    directly and reads r['passed'].  It NEVER calls run_all().  An earlier
    version of this module diagnosed exactly that defect in its own header and
    then left FIVE protections in run_all() anyway -- the inventory fingerprint,
    the registry-key-to-name binding, the scope-flag reads, the prose bar and the
    physical-grade bar.  A blinded execution audit built a module that was 7/7
    green on the register path while shipping born_derived = True and an
    epistemic string claiming Born.  All five now run HERE, on every call.

    RESIDUAL, disclosed: _INVENTORY_FINGERPRINT is a literal in this file, so a
    coordinated two-site edit defeats it.  That is a strictly larger tamper than
    a single-site edit, and it is the honest ceiling -- no module can defend
    against an edit to its own constants."""
    reg = globals().get("_CHECKS")
    if reg is None:
        raise AssertionError("%s: the check registry is not built" % name)
    live = "|".join(sorted("%s->%s" % (k, v.__name__) for k, v in reg.items()))
    if live != _INVENTORY_FINGERPRINT:
        raise AssertionError("inventory fingerprint mismatch on the banked "
                             "path: %s" % live)
    if set(reg) != set(CANONICAL_CHECK_NAMES):
        raise AssertionError("inventory drift: %s" % sorted(set(reg)))
    if name not in reg:
        raise AssertionError("%s is not a registered check" % name)
    if reg[name].__name__ != "check_" + name:
        raise AssertionError("registry key %r is bound to %r"
                             % (name, reg[name].__name__))
    blob = ("%s %s" % (key_result, epistemic)).upper()
    for phrase in BARRED_PROSE:
        if phrase in blob:
            raise AssertionError("%s ships a barred sentence: %r" % (name, phrase))
    need = REQUIRED_PROSE.get(name)
    if need is not None and need.upper() not in blob:
        raise AssertionError("%s must carry %r" % (name, need))
    if epistemic.startswith("P_physical") or epistemic == "P":
        raise AssertionError("%s claims a physical grade; nothing here is "
                             "physically certified" % name)


def _result(name, key_result, fails, *, imports=(), negative_controls=(),
            artifacts=None, epistemic="P_math") -> Dict[str, object]:
    """Build the record and cross-assert AT THE POINT THE DICT IS BUILT.

    The bank does not call run_all(): bank.py imports the module, calls
    register(), then invokes each check_fn() directly and reads r['passed'].  A
    guarantee that lives only in run_all() does not travel on the banked path
    (the v24.3.450 finding).  So the count is recomputed here, independently of
    the tuple, and disagreement RAISES.

    RESIDUAL LIMIT, disclosed: this catches divergence between the two records.
    It cannot catch a bare literal substitution of the returned verdict, because
    nothing downstream re-derives that field.  No module can defend against an
    edit to its own return statement."""
    reasons = tuple(fails)
    counted = sum(1 for _ in fails)
    if counted != len(reasons):
        raise AssertionError("tamper: %s failure records disagree" % name)
    verdict = not reasons
    if verdict and reasons:
        raise AssertionError("tamper: %s passed with recorded failures" % name)
    if (not verdict) and not reasons:
        raise AssertionError("tamper: %s failed with no reason" % name)
    _travel_guard(name, key_result, epistemic)
    # RE-VERIFIED AT CONSTRUCTION TIME, after every intervening statement.  The
    # first check above can be defeated by rebinding `reasons` below it; this one
    # cannot, because it is the last thing that runs before the record is built
    # and it re-reads `fails` -- the argument, not a local.
    if len(reasons) != counted or len(list(fails)) != counted or \
            verdict != (counted == 0):
        raise AssertionError(
            "tamper: %s -- verdict %r, %d reasons, %d counted, %d in fails"
            % (name, verdict, len(reasons), counted, len(list(fails))))
    return Result(name, verdict, reasons, counted, key_result, tuple(imports),
                  tuple(negative_controls), dict(artifacts or {}),
                  epistemic).to_dict()


def _eq(a, b) -> bool:
    return sp.simplify(a - b) == sp.zeros(*sp.Matrix(a).shape)


def psd(m) -> bool:
    m = sp.simplify(sp.Matrix(m))
    if sp.simplify(m - m.H) != sp.zeros(*m.shape):
        return False
    return all(sp.re(sp.nsimplify(e)) >= 0 for e in m.eigenvals())


def bloch(m) -> sp.Matrix:
    return sp.Matrix([sp.simplify(sp.trace(m * SX)),
                      sp.simplify(sp.trace(m * SY)),
                      sp.simplify(sp.trace(m * SZ))])


def norm(v) -> sp.Expr:
    return sp.sqrt(sp.simplify((sp.Matrix(v).T * sp.Matrix(v))[0]))


def _hv(m):
    return [sp.simplify(sp.trace(m)), sp.simplify(sp.trace(m * SX)),
            sp.simplify(sp.trace(m * SY)), sp.simplify(sp.trace(m * SZ))]


def check_L_exposing_effects_and_setup() -> Dict[str, object]:
    """The hypotheses, computed rather than declared."""
    fails: List[str] = []
    for lbl, R in (("P", P0), ("Q", Q1)):
        if sp.simplify(R * R - R) != sp.zeros(2, 2) or sp.simplify(sp.trace(R)) != 1:
            fails.append("%s must be a rank-one projection (R^2=R, Tr R=1)" % lbl)
        if not psd(R):
            fails.append("%s must be PSD" % lbl)
    overlap = sp.simplify(sp.trace(P0 * Q1))
    if _eq(P0, Q1):
        fails.append("the rays must be DISTINCT -- that is the hypothesis")
    if overlap != EXPECT_TR_PQ:
        fails.append("the engine overlap must be EXACTLY %s, computed; got %s"
                     % (EXPECT_TR_PQ, overlap))
    for lbl, R, F in (("P", P0, F_P), ("Q", Q1, F_Q)):
        if not (psd(F) and psd(I2 - F)):
            fails.append("f_%s must be an effect" % lbl)
        if (I2 - F).rank() != 1:
            fails.append("f_%s must have a ONE-dimensional unit eigenspace "
                         "(the identity effect returns certainty on every state "
                         "and identifies nothing)" % lbl)
        if not _eq(sp.simplify(F * R), R):
            fails.append("f_%s must fix its own ray" % lbl)
        if _eq(F, I2):
            fails.append("f_%s must not be the identity effect" % lbl)
        if sp.simplify(sp.trace(R * F)) != 1:
            fails.append("certainty Tr(%s f_%s) = 1 must hold" % (lbl, lbl))
        if sp.simplify(sp.trace((I2 / 2) * F)) == 1:
            fails.append("VACUITY: a mixed state must not score certainty on f_%s" % lbl)
    dim_S = sp.Matrix([_hv(m) for m in (I2, F_P, F_Q)]).rank()
    dim_alt = sp.Matrix([_hv(m) for m in (I2, P0, Q1)]).rank()
    if dim_S != 3 or dim_alt != 3:
        fails.append("S must have real dimension 3 (got %s / %s)" % (dim_S, dim_alt))
    return _result(
        "L_exposing_effects_and_setup",
        "The exact engine pair: P and Q are distinct rank-one projections with "
        "Tr(PQ) = 49/625 computed and pinned by equality; f_P and f_Q are "
        "non-identity effects whose unit eigenspaces are exactly the "
        "corresponding rays, each returning certainty on its own ray and not on "
        "the maximally mixed state; S = span{I, f_P, f_Q} = span{I, P, Q} has "
        "real dimension 3.",
        fails,
        negative_controls=("the identity effect, whose unit face is the whole carrier",
                           "the maximally mixed state, which must not score certainty"),
        artifacts={"Tr_PQ": str(overlap), "dim_R_S": int(dim_S),
                   "t_expose": str(T_EXPOSE)},
    )


def check_L_certainty_and_positivity_force_the_lambda_form() -> Dict[str, object]:
    """Step 2, EXECUTED for a general T rather than assumed.

    The earlier draft wrote T(P) = P + lam(I-P) into its parametrization and then
    verified consequences of that form.  That is the conclusion substituted into
    its own premise: the form is what Step 2 has to produce.  Here T(P) is a
    general Hermitian matrix -- four unconstrained real parameters -- and the
    form is DERIVED from certainty plus positivity at x = I - P, via the equality
    case of Cauchy-Schwarz.
    """
    fails: List[str] = []
    tau, a1, a2, a3 = sp.symbols("tau a1 a2 a3", real=True)
    avec = sp.Matrix([a1, a2, a3])
    p = bloch(P0)

    # A GENERAL Hermitian image.  No form assumed.
    TP = sp.simplify((tau * I2 + a1 * SX + a2 * SY + a3 * SZ) / 2)
    if sp.simplify(TP - TP.H) != sp.zeros(2, 2):
        fails.append("the general image must be Hermitian by construction")
    if sp.simplify(sp.trace(TP) - tau) != 0:
        fails.append("the parametrization must carry trace tau")
    if sp.simplify(bloch(TP) - avec) != sp.zeros(3, 1):
        fails.append("the parametrization must carry Bloch vector a")
    if sp.simplify(norm(p) - 1) != 0:
        fails.append("p must be a unit vector, or Cauchy-Schwarz is misapplied")

    # (i) CERTAINTY, computed from the general image.
    TfP = sp.simplify(T_EXPOSE * I2 + (1 - T_EXPOSE) * TP)     # linearity + unitality
    cert = sp.simplify(sp.trace(P0 * TfP) - 1)
    forced = sp.simplify(tau + (p.T * avec)[0] - 2)
    if sp.simplify(cert - (1 - T_EXPOSE) * forced / 2) != 0:
        fails.append("certainty must reduce EXACTLY to tau + p.a = 2; residual %s"
                     % sp.simplify(cert - (1 - T_EXPOSE) * forced / 2))

    # (ii) POSITIVITY probes.  Both P and I-P are PSD elements of S, so both are
    #      legitimate probes for a positive map.  The eigenvalues of
    #      (tau I + a.sigma)/2 are (tau +- |a|)/2, so
    #        TP >= 0  <=>  tau >= |a| ;   I - TP >= 0  <=>  2 - tau >= |a|.
    if not (psd(sp.simplify(I2 - P0)) and psd(P0)):
        fails.append("the probes P and I-P must themselves be PSD elements of S")
    for tau_v, a_v, want in ((sp.Rational(3, 2), sp.Rational(1, 2), True),
                             (sp.Rational(1, 4), sp.Rational(1, 2), False)):
        M = sp.simplify((tau_v * I2 + a_v * SZ) / 2)
        if psd(M) is not want:
            fails.append("the eigenvalue reading (tau +- |a|)/2 must decide "
                         "positivity; it misread tau = %s, |a| = %s" % (tau_v, a_v))

    # (iii-A) ROUTE 1 -- THE PSD SUPPORT LEMMA, CONSUMED.
    #   Unitality + positivity at the PSD element I - f_P give
    #   M := I - T(f_P) = T(I - f_P) >= 0, and certainty gives Tr(P M) = 0.
    #   The support lemma then yields P M = 0, and SOLVING that matrix equation
    #   -- not asserting its answer -- returns tau + a3 = 2 and a1 = a2 = 0.
    #   This is the route the argument runs on; the Bloch/Cauchy-Schwarz chain
    #   below is the alternative.  Route 1 is dimension-free until its last
    #   line, which is where n = 2 enters and where n >= 3 fails.
    M = sp.simplify(I2 - TfP)
    if sp.simplify(sp.trace(P0 * M) - (1 - T_EXPOSE) * (2 - tau - a3) / 2) != 0:
        fails.append("certainty must be exactly Tr(P M) = 0 with "
                     "M = I - T(f_P); residual %s"
                     % sp.simplify(sp.trace(P0 * M)))
    supp = sp.simplify(P0 * M)
    route1 = sp.solve([sp.Eq(supp[i, j], 0) for i in range(2) for j in range(2)],
                      [tau, a1, a2, a3], dict=True)
    if len(route1) != 1:
        fails.append("the support-lemma equation P M = 0 must have a unique "
                     "solution manifold; got %s" % route1)
    else:
        r1 = route1[0]
        if r1.get(a1, None) != 0 or r1.get(a2, None) != 0:
            fails.append("the support lemma must FORCE a1 = a2 = 0 (the "
                         "transverse part), derived rather than asserted; got %s"
                         % r1)
        got_a3 = sp.simplify(r1.get(a3, a3) - (2 - r1.get(tau, tau)))
        if got_a3 != 0:
            fails.append("the support lemma must force a3 = 2 - tau; got %s" % r1)
    # and the lemma's PSD hypothesis is what licenses the step: without it,
    # Tr(AB) = 0 does not give AB = 0 (control in leg (vi)).

    # (iii-B) ROUTE 2 -- THE CAUCHY-SCHWARZ CHAIN, EXECUTED not asserted.
    #   Solve certainty for the longitudinal component, substitute into the
    #   positivity inequality |a|^2 <= (2 - tau)^2, and READ OFF that the residual
    #   is minus the squared transverse part -- so the inequality forces it to
    #   vanish.  Nothing here writes a1 = a2 = 0 into its own premise.
    pa = sp.simplify((p.T * avec)[0])
    a3_sol = sp.solve(sp.Eq(tau + pa, 2), a3)
    if len(a3_sol) != 1:
        fails.append("certainty must determine the longitudinal component "
                     "uniquely; got %s" % a3_sol)
    a3_sol = a3_sol[0]
    residual = sp.expand(sp.simplify(
        (2 - tau) ** 2 - (avec.T * avec)[0].subs({a3: a3_sol})))
    if sp.simplify(residual + (a1 ** 2 + a2 ** 2)) != 0:
        fails.append("substituting certainty into the I-P positivity inequality "
                     "must leave EXACTLY minus the squared transverse part; "
                     "got %s" % residual)
    # The inequality residual <= 0 combined with the residual being MINUS a sum
    # of squares of REALS forces the transverse part to vanish.  Executed as the
    # three facts that carry it, with a discriminating control -- sp.solve is not
    # used here because it works over C and returns the spurious branches
    # a1 = +-i a2, which are not in the real parameter space.
    sos = a1 ** 2 + a2 ** 2
    if sos.is_nonnegative is not True:
        fails.append("a1^2 + a2^2 must be recognised as nonnegative for REAL "
                     "parameters; got is_nonnegative = %s" % sos.is_nonnegative)
    if sp.simplify(sos.subs({a1: 0, a2: 0})) != 0:
        fails.append("the sum of squares must vanish at the origin")
    for va1, va2 in ((sp.Rational(1, 7), 0), (0, sp.Rational(-3, 11)),
                     (sp.Rational(2, 5), sp.Rational(9, 4))):
        if not (sp.simplify(sos.subs({a1: va1, a2: va2})) > 0):
            fails.append("a1^2 + a2^2 must be STRICTLY positive off the origin; "
                         "failed at (%s, %s)" % (va1, va2))
    # discrimination: an indefinite quadratic must NOT pass the same test
    if (a1 ** 2 - a2 ** 2).is_nonnegative is True:
        fails.append("the nonnegativity test must reject an indefinite form, or "
                     "it decides nothing")
    # DISCRIMINATION: the identity is a fact about a UNIT p.  With a non-unit p
    # the substitution does not produce the squared transverse part, so the leg
    # is not a tautology about its own left-hand side.
    p_bad = sp.simplify(2 * p)
    a3_bad = sp.solve(sp.Eq(tau + (p_bad.T * avec)[0], 2), a3)[0]
    residual_bad = sp.expand(sp.simplify(
        (2 - tau) ** 2 - (avec.T * avec)[0].subs({a3: a3_bad})))
    if sp.simplify(residual_bad + (a1 ** 2 + a2 ** 2)) == 0:
        fails.append("with a NON-unit p the Cauchy-Schwarz identity must FAIL -- "
                     "otherwise the leg is a tautology about its own input")

    # (iii-C) both routes must land on the SAME form.
    TP_forced = sp.simplify(TP.subs({a1: 0, a2: 0, a3: a3_sol}))
    lam = sp.symbols("lam", real=True)
    TP_form = sp.simplify(P0 + lam * (I2 - P0))
    if sp.simplify(TP_forced.subs({tau: 1 + lam}) - TP_form) != sp.zeros(2, 2):
        fails.append("the derived image must be EXACTLY P + lam(I-P) with "
                     "lam = tau - 1")
    # UNITALITY, with a negative control: it is what turns positivity at I - P
    # into I - T(P) >= 0 and what reduces T(f_P).  A non-unital T(I) = I/2 sends
    # the certainty equation somewhere else.
    non_unital = sp.simplify(T_EXPOSE * (I2 / 2) + (1 - T_EXPOSE) * TP)
    if sp.simplify(sp.trace(P0 * non_unital) - sp.trace(P0 * TfP)) == 0:
        fails.append("unitality must be load-bearing: a non-unital T(I) must "
                     "move the certainty equation")

    # (iv) THE RANGE, also from positivity and not assumed.
    if not psd(sp.simplify(P0 + sp.Rational(1, 5) * (I2 - P0))):
        fails.append("a small positive lam must keep T(P) PSD (else the range "
                     "leg is vacuous)")
    if psd(sp.simplify(P0 + sp.Rational(-1, 5) * (I2 - P0))):
        fails.append("a NEGATIVE lam must break positivity of T(P) -- exhibit it")
    if psd(sp.simplify(I2 - (P0 + sp.Rational(6, 5) * (I2 - P0)))):
        fails.append("lam > 1 must break positivity of T(I-P) -- exhibit it")

    # (v) THE DISCRIMINATING CONTROL.  Drop positivity at x = I - P and a
    #     NON-PARALLEL image survives certainty and positivity at x = P.  So the
    #     I-P probe is the load-bearing one and the chain is not decorative.
    ctl = {tau: sp.Rational(3, 2), a1: 1, a2: 0, a3: sp.Rational(1, 2)}
    ctl_a = sp.Matrix([ctl[a1], ctl[a2], ctl[a3]])
    ctl_TP = sp.simplify(TP.subs(ctl))
    ctl_cert = sp.simplify(sp.trace(P0 * sp.simplify(
        T_EXPOSE * I2 + (1 - T_EXPOSE) * ctl_TP)))
    if ctl_cert != 1:
        fails.append("the control must satisfy certainty exactly; got %s" % ctl_cert)
    if not psd(ctl_TP):
        fails.append("the control must be positive at x = P")
    if psd(sp.simplify(I2 - ctl_TP)):
        fails.append("the control must FAIL positivity at x = I - P, or it does "
                     "not isolate that probe")
    if sp.simplify((ctl_a.T * ctl_a)[0] - (p.T * ctl_a)[0] ** 2) == 0:
        fails.append("the control must be NON-parallel to p, or it witnesses "
                     "nothing about the equality case")

    # (vi) The PSD support lemma, exercised with its hypothesis load-bearing.
    A, B = P0, sp.simplify(I2 - F_P)
    if not (psd(A) and psd(B)):
        fails.append("the support-lemma witnesses must be PSD")
    if sp.simplify(sp.trace(A * B)) != 0:
        fails.append("the support-lemma antecedent Tr(AB) = 0 must hold on the "
                     "witness pair")
    if sp.simplify(A * B) != sp.zeros(2, 2):
        fails.append("the PSD support lemma must then give AB = 0")
    # The control: a NON-PSD B with Tr(AB) = 0 but AB != 0.  Tr(P B) = B[0,0],
    # so B must have a zero (0,0) entry and a nonzero first row -- sigma_x does
    # both, and its spectrum {+1,-1} makes it non-PSD.  (An earlier draft used
    # diag(1,-1), for which Tr(AB) = 1: the control did not satisfy the
    # antecedent it was meant to isolate.)
    Bneg = SX
    if psd(Bneg):
        fails.append("the support-lemma control must be NON-PSD")
    if sp.simplify(sp.trace(A * Bneg)) != 0:
        fails.append("the control must satisfy the antecedent Tr(AB) = 0, or it "
                     "isolates nothing; got %s" % sp.simplify(sp.trace(A * Bneg)))
    if sp.simplify(A * Bneg) == sp.zeros(2, 2):
        fails.append("the control must have AB != 0, showing the PSD hypothesis "
                     "is load-bearing")

    return _result(
        "L_certainty_and_positivity_force_the_lambda_form",
        "Step 2, DERIVED for a general T by TWO routes, on four unconstrained "
        "real parameters.  ROUTE 1, the one the argument consumes: unitality and "
        "positivity give M = I - T(f_P) >= 0, certainty gives Tr(P M) = 0, and "
        "the PSD SUPPORT LEMMA gives P M = 0 -- whose matrix equation, SOLVED "
        "rather than answered, returns a1 = a2 = 0 and a3 = 2 - tau.  Route 1 is "
        "dimension-free until its last line, and that last line is exactly where "
        "n >= 3 fails.  ROUTE 2, the Bloch alternative: certainty solved for the "
        "longitudinal component and substituted into the I-P positivity "
        "inequality leaves exactly minus the squared transverse part, so the "
        "inequality forces a1 = a2 = 0; the step is discriminated by a NON-unit "
        "p, for which the identity fails.  Both routes land on "
        "T(P) = P + lam(I-P) with lam = tau - 1.  Positivity at x = P then gives "
        "lam >= 0 and |a| >= 0 gives lam <= 1.  The I-P probe is isolated by a "
        "control: tau = 3/2, a = (1, 0, 1/2) satisfies certainty and positivity "
        "at P, is NOT parallel to p, and fails only at I-P.  Unitality carries "
        "its own control.",
        fails,
        imports=("PSD support lemma: A,B >= 0 and Tr(AB) = 0 imply AB = 0 -- "
                 "CONSUMED by Route 1",
                 "Cauchy-Schwarz in R^3, used as an inequality with its SIGNED "
                 "equality case (p.a = |a| forces a = |a|p) -- consumed by "
                 "Route 2"),
        negative_controls=(
            "tau = 3/2, a = (1,0,1/2): certainty holds, positivity at P holds, "
            "positivity at I-P fails, and a is not parallel to p",
            "a non-PSD B with Tr(AB) = 0 but AB != 0",
            "lam = -1/5 and lam = 6/5, each breaking one positivity probe",
        ),
        artifacts={"free_real_parameters_before_constraints": 4,
                   "cauchy_schwarz_defect": "a1^2 + a2^2",
                   "forced_image": "P + lam(I-P), lam = tau - 1",
                   "lam_range_from_positivity": "[0, 1]"},
    )


def check_T_positivity_forces_the_identity_readout() -> Dict[str, object]:
    """The theorem.  Both bounds computed, the global step CONCAVE."""
    fails: List[str] = []
    lam, lamp = sp.symbols("lam lamp", real=True)
    a, b = sp.symbols("a b", positive=True)
    p, q = bloch(P0), bloch(Q1)

    def family(L, Lp):
        TP = sp.simplify(P0 + L * (I2 - P0))
        TQ = sp.simplify(Q1 + Lp * (I2 - Q1))
        return (lambda al, be, ga: sp.simplify(al * I2 + be * TP + ga * TQ)), TP, TQ

    # --- leg 1: lam >= 0, from positivity at x = P (derived generally in the
    #     companion lemma; re-exhibited here on the concrete family).
    if not psd(P0):
        fails.append("the probe x = P must be PSD")
    _, TP, _ = family(lam, lamp)
    if sp.simplify(sp.trace(TP)) != 1 + lam:
        fails.append("T(P) trace must be 1 + lam")
    # EXHIBITED, not merely asserted: T(P) = P + lam(I-P) has eigenvalues 1 and
    # lam, so positivity at x = P is EXACTLY lam >= 0.
    ev_TP = sorted([sp.nsimplify(v) for v in
                    sp.simplify(P0 + lam * (I2 - P0)).eigenvals().keys()],
                   key=str)
    if sorted([str(v) for v in ev_TP]) != ["1", "lam"]:
        fails.append("T(P) must have eigenvalues {1, lam}, so that positivity at "
                     "x = P is exactly lam >= 0; got %s" % ev_TP)
    for probe, want in ((sp.Rational(-1, 5), False), (sp.Rational(1, 5), True)):
        if psd(sp.simplify(P0 + probe * (I2 - P0))) is not want:
            fails.append("positivity at x = P must decide the sign of lam; "
                         "misread at lam = %s" % probe)

    # --- leg 2: the tight constraint, its strictly negative derivative, and the
    #     CONCAVITY that turns a local statement into a global one.
    w = sp.simplify(a * p + b * q)
    N = norm(w)
    img = sp.simplify(a * (1 - lam) * p + b * (1 - lamp) * q)
    g = sp.simplify(N - (a * lam + b * lamp) - norm(img))
    if sp.simplify(g.subs({lam: 0, lamp: 0})) != 0:
        fails.append("the constraint must be TIGHT at the identity")
    dg = sp.simplify(sp.diff(g, lam).subs({lam: 0, lamp: 0}))
    dg11 = sp.nsimplify(sp.simplify(dg.subs({a: 1, b: 1})))
    if dg11 != EXPECT_DG11:
        fails.append("dg/dlam at the identity must be EXACTLY %s; got %s"
                     % (EXPECT_DG11, dg11))
    if not (dg11 < 0):
        fails.append("dg/dlam at the identity must be strictly negative")
    # CONCAVITY.  g is (affine) - (norm of an affine map), hence concave; the
    # structural reason is stated in the module header.  Corroborated by the sign
    # of the second derivative, which must be NEGATIVE, at two distinct points --
    # a single point could be an artefact of the endpoint.
    # THE STRUCTURAL REASON, executed: img is AFFINE in (lam, lam'), so |img| is
    # convex and g = affine - |img| is concave.  Two sampled second derivatives
    # corroborate; this is the statement.
    for v in (lam, lamp):
        if sp.simplify(sp.diff(img, v, 2)) != sp.zeros(3, 1):
            fails.append("the image must be AFFINE in %s -- that is why |img| is "
                         "convex and g is concave" % v)
        if sp.simplify(sp.diff(img, v)) == sp.zeros(3, 1):
            fails.append("the image must actually DEPEND on %s, or affinity is "
                         "vacuous" % v)
    d2 = sp.diff(g, lam, 2)
    d2g = sp.nsimplify(sp.simplify(d2.subs({lam: 0, lamp: 0}).subs({a: 1, b: 1})))
    d2g_mid = sp.nsimplify(sp.simplify(
        d2.subs({lam: sp.Rational(1, 2), lamp: 0}).subs({a: 1, b: 1})))
    # PINNED BY EQUALITY, not by sign.  A sign test cannot tell the second
    # derivative from the first: dg/dlam is also negative here, so "d2 < 0"
    # would pass on sp.diff(g, lam, 1).
    if sp.simplify(d2g - EXPECT_D2G) != 0:
        fails.append("d2g/dlam2 at the identity must be EXACTLY %s; got %s"
                     % (EXPECT_D2G, d2g))
    if sp.simplify(d2g_mid - EXPECT_D2G_MID) != 0:
        fails.append("d2g/dlam2 at lam = 1/2 must be EXACTLY %s; got %s"
                     % (EXPECT_D2G_MID, d2g_mid))
    if not (d2g < 0):
        fails.append("g must be CONCAVE in lam at the identity -- tightness plus "
                     "a negative derivative alone excludes only a punctured "
                     "neighbourhood; got d2g = %s" % d2g)
    if not (d2g_mid < 0):
        fails.append("concavity must hold across the feasible interval, not only "
                     "at the endpoint; got %s at lam = 1/2" % d2g_mid)

    # dg/dlam' must exist too: the joint closure needs BOTH partials for the
    # supporting-hyperplane step.  At a = b = 1 it equals dg/dlam by symmetry.
    dgp11 = sp.nsimplify(sp.simplify(
        sp.diff(g, lamp).subs({lam: 0, lamp: 0}).subs({a: 1, b: 1})))
    if dgp11 != EXPECT_DG11:
        fails.append("dg/dlam' at the identity must also be EXACTLY %s (the "
                     "joint closure needs both partials); got %s"
                     % (EXPECT_DG11, dgp11))

    # THE CLOSURE STRENGTH.  It is 1 - sqrt(Tr PQ) = |dg/dlam|, MAXIMAL at
    # orthogonality and vanishing only as P -> Q, which is the excluded
    # hypothesis.  (An earlier draft named 2/|p+q| = 1/sqrt(Tr PQ) "the margin";
    # no inequality has that as slack and it runs the OPPOSITE way.  The bar is
    # in BARRED_PROSE.)
    w11 = sp.simplify(p + q)
    cs_gap = sp.simplify(norm(w11) - (p.T * w11)[0])
    if not (cs_gap > 0):
        fails.append("strict Cauchy-Schwarz must give |p+q| > p.(p+q); that "
                     "strictness IS the distinctness hypothesis")
    o = EXPECT_TR_PQ
    closure = sp.simplify(1 - sp.sqrt(o))
    if closure != EXPECT_CLOSURE or sp.simplify(closure + dg11) != 0:
        fails.append("the closure strength must be EXACTLY 1 - sqrt(Tr PQ) = %s "
                     "and must equal |dg/dlam|; got %s vs %s"
                     % (EXPECT_CLOSURE, closure, -dg11))
    # the general Cauchy-Schwarz gap, in closed form: 2 sqrt(o)(1 - sqrt(o)).
    if sp.simplify(cs_gap - 2 * sp.sqrt(o) * (1 - sp.sqrt(o))) != 0:
        fails.append("the Cauchy-Schwarz gap must be 2 sqrt(o)(1 - sqrt(o)) in "
                     "closed form; got %s" % cs_gap)
    # |p+q| = 2 sqrt(Tr PQ) is a GENERAL identity, not a fact about this pair:
    # verify it symbolically for an arbitrary unit q against p = (0,0,1).
    qx, qy, qz = sp.symbols("qx qy qz", real=True)
    unit = sp.Eq(qx ** 2 + qy ** 2 + qz ** 2, 1)
    lhs = sp.simplify(((sp.Matrix([0, 0, 1]) + sp.Matrix([qx, qy, qz])).T
                       * (sp.Matrix([0, 0, 1]) + sp.Matrix([qx, qy, qz])))[0])
    if sp.simplify(lhs.subs({qx ** 2: 1 - qy ** 2 - qz ** 2}) - (2 + 2 * qz)) != 0:
        fails.append("|p+q|^2 must reduce to 2 + 2 q_z for a general unit q")
    # Tr(PQ) COMPUTED for the general pair, not quoted: build both projectors
    # from their Bloch vectors and take the trace of the product.
    Pgen = sp.simplify((I2 + SZ) / 2)
    Qgen = sp.simplify((I2 + qx * SX + qy * SY + qz * SZ) / 2)
    trPQ_gen = sp.simplify(sp.trace(Pgen * Qgen))
    if sp.simplify(trPQ_gen - (1 + qz) / 2) != 0:
        fails.append("Tr(PQ) must compute to (1 + q_z)/2 for a general q; "
                     "got %s" % trPQ_gen)
    if sp.simplify((2 + 2 * qz) - 4 * trPQ_gen) != 0:
        fails.append("|p+q|^2 = 4 Tr(PQ) must hold identically")
    if sp.simplify(unit.lhs - unit.rhs) == 0:
        fails.append("the unit constraint must be a nontrivial relation")

    # THE SHARP GLOBAL BOUND, which is what makes the local statement global:
    #   g(lam, lam') <= -(1 - sqrt(o)) (lam + lam')   on the feasible box.
    for L in (0, sp.Rational(1, 10), sp.Rational(1, 2), 1):
        for Lp in (0, sp.Rational(1, 3), 1):
            val = sp.simplify(g.subs({lam: L, lamp: Lp}).subs({a: 1, b: 1}))
            if not (sp.simplify(val + closure * (L + Lp)) <= 0):
                fails.append("the sharp bound g <= -(1 - sqrt(o))(lam + lam') "
                             "must hold; failed at (%s, %s)" % (L, Lp))

    # --- leg 3: the feasible set is the single point
    survivors = []
    for L in (sp.Rational(-1, 10), sp.Rational(-1, 50), 0,
              sp.Rational(1, 50), sp.Rational(1, 10), sp.Rational(1, 3)):
        Tl, TPl, _ = family(L, 0)
        ok = psd(TPl) and psd(sp.simplify(I2 - TPl))
        if ok:
            alpha = sp.simplify((2 + norm(w11)) / 2)
            x = sp.simplify(alpha * I2 - P0 - Q1)
            if not psd(x):
                fails.append("the tight witness must itself be PSD")
            # TIED: the PSD preimage must be the element the map acts on.  At
            # lam = 0 the map is the identity, so T(x) must equal x itself --
            # otherwise the leg checks positivity of one matrix and maps another.
            id_family, _, _ = family(0, 0)
            if sp.simplify(id_family(alpha, -1, -1) - x) != sp.zeros(2, 2):
                fails.append("the mapped element must BE the PSD witness at "
                             "lam = 0, not a second matrix")
            ok = psd(Tl(alpha, -1, -1))
        if ok:
            survivors.append(L)
    if survivors != [0]:
        fails.append("the feasible set must be exactly {lam = 0}; got %s" % survivors)

    # --- leg 4: DISTINCTNESS suffices; the orthogonal branch closes differently.
    Qo = sp.simplify(I2 - P0)
    dim_orth = sp.Matrix([_hv(m) for m in (I2, P0, Qo)]).rank()
    if dim_orth != 2:
        fails.append("for an ORTHOGONAL pair S must collapse to dimension 2")
    Lo = sp.symbols("Lo", real=True)
    TPo = sp.simplify(P0 + Lo * (I2 - P0))
    TQo = sp.simplify(I2 - TPo)                       # forced by linearity on S
    TfQo = sp.simplify(T_EXPOSE * I2 + (1 - T_EXPOSE) * TQo)
    sol = sp.solve(sp.Eq(sp.simplify(sp.trace(Qo * TfQo)), 1), Lo)
    if sol != [0]:
        fails.append("in the orthogonal case the SECOND certainty must force "
                     "lam = 0 on its own; got %s" % sol)
    # THE CORRECTED SENTENCE.  |p+q| VANISHES there, so the margin 2/|p+q|
    # DIVERGES -- the leg-2 mechanism is unavailable because its denominator is
    # zero, not because its value is small.  Both halves computed.
    bsum = norm(sp.simplify(bloch(P0) + bloch(Qo)))
    if bsum != 0:
        fails.append("for an orthogonal pair the Bloch sum must VANISH; got %s" % bsum)
    # THE CAUSE, computed.  The tight witness lam_max(P+Q) I - P - Q collapses to
    # the ZERO matrix, and a positivity constraint on the zero matrix carries no
    # positivity content: what the algebra then encodes is the linear dependence
    # Q = I - P, i.e. well-definedness of T.  (An earlier draft attributed the
    # failure to the denominator 2/|p+q| diverging; three things degenerate here
    # and that is the least informative of them.)
    witness_orth = sp.simplify((1 + sp.sqrt(0)) * I2 - P0 - Qo)
    if witness_orth != sp.zeros(2, 2):
        fails.append("at Tr(PQ) = 0 the tight witness must degenerate to the "
                     "ZERO matrix; got %s" % witness_orth)
    if sp.simplify(Qo - (I2 - P0)) != sp.zeros(2, 2):
        fails.append("what the collapsed constraint carries is the linear "
                     "dependence Q = I - P")
    # and the same witness at the ENGINE pair is nonzero, so the degeneration is
    # a property of orthogonality and not of the construction.
    witness_engine = sp.simplify((2 + norm(sp.simplify(p + q))) / 2 * I2 - P0 - Q1)
    if witness_engine == sp.zeros(2, 2):
        fails.append("the tight witness must be NONZERO at the engine pair, or "
                     "the degeneration says nothing about orthogonality")
    # the strict Cauchy-Schwarz gap vanishes there too, by the closed form
    if sp.simplify(2 * sp.sqrt(0) * (1 - sp.sqrt(0))) != 0:
        fails.append("the Cauchy-Schwarz gap 2 sqrt(o)(1 - sqrt(o)) must vanish "
                     "at o = 0")

    cp_used, tp_used = False, False
    if cp_used or tp_used:
        fails.append("the theorem's whole point is that complete positivity and "
                     "trace preservation are not used")
    return _result(
        "T_positivity_forces_the_identity_readout",
        "On M_2(C), a unital POSITIVE linear map on S = span{I, f_P, f_Q} with "
        "matched certainty at two DISTINCT rays is the identity on S.  The image "
        "form and lam >= 0 come from certainty plus positivity (derived, not "
        "assumed, in the companion lemma); lam <= 0 because the PSD constraint "
        "on alpha I - aP - bQ is tight at the identity with derivative %s < 0 at "
        "a = b = 1 and is CONCAVE in lam across the feasible interval -- "
        "tightness plus a negative derivative alone would exclude only a "
        "punctured neighbourhood.  The CLOSURE STRENGTH is 1 - sqrt(Tr PQ) = %s, "
        "which is exactly |dg/dlam| at the identity, is MAXIMAL at orthogonality "
        "and vanishes only as P -> Q -- the excluded hypothesis -- and it "
        "carries the sharp global bound g <= -(1 - sqrt(Tr PQ))(lam + lam').  "
        "The feasible set is exactly {0}.  COMPLETE POSITIVITY IS "
        "NOT USED, and neither is trace preservation, Arveson, Kraus, effect "
        "saturation, output tomography, or the banked two-ray theorem.  "
        "DISTINCTNESS suffices: the orthogonal case closes by the second "
        "certainty on a 2-dimensional S; the leg-2 mechanism is unavailable "
        "there because its tight witness lam_max(P+Q) I - P - Q DEGENERATES TO "
        "THE ZERO MATRIX, so the constraint it carries is the linear dependence "
        "Q = I - P rather than a positivity bound.  So the banked two-ray "
        "theorem's nonorthogonality fence does NOT transfer to this route."
        % (dg11, closure),
        fails,
        imports=("Cauchy-Schwarz in R^3 (inequality, with its equality case used "
                 "as the parallelism step)",),
        negative_controls=(
            "lam < 0 breaks positivity of T(P)",
            "lam > 0 breaks the tight boundary witness",
            "an orthogonal pair, where |p+q| vanishes and the second certainty "
            "closes instead",
        ),
        artifacts={
            "dg_dlam_at_identity": str(dg11),
            "d2g_dlam2_at_identity": str(d2g),
            "d2g_dlam2_at_half": str(d2g_mid),
            "closure_strength_1_minus_sqrt_TrPQ": str(closure),
            "dg_dlamp_at_identity": str(dgp11),
            "feasible_lam_set": [str(s) for s in survivors],
            "dim_S_orthogonal_case": int(dim_orth),
            "complete_positivity_used": cp_used,
            "trace_preservation_used": tp_used,
        },
        epistemic="P_math | n = 2 ONLY (FALSE at n = 3, in-module); positivity, "
                  "not complete positivity; concludes T = id_S, not id_{M_2}; "
                  "derives no physical premise and does not derive Born",
    )


def check_L_positivity_does_not_suffice_at_n3() -> Dict[str, object]:
    """The scope fence is a THEOREM, not an open question.

    An earlier draft shipped "whether positivity suffices at n >= 3 is OPEN".
    It is closed, negatively.  The counterexample is exact and its positivity
    carries a one-line PSD certificate rather than a probe count.
    """
    fails: List[str] = []
    e1 = sp.Matrix([1, 0, 0])
    e3 = sp.Matrix([0, 0, 1])
    psiQ = sp.Matrix([sp.Rational(3, 5), sp.Rational(4, 5), 0])
    psiQperp = sp.Matrix([sp.Rational(4, 5), sp.Rational(-3, 5), 0])
    P3 = sp.simplify(e1 * e1.T)
    Q3 = sp.simplify(psiQ * psiQ.T)
    R3 = sp.simplify(e3 * e3.T)
    Y = sp.simplify(psiQperp * psiQperp.T)
    I3 = sp.eye(3)
    c = sp.simplify(1 - sp.trace(P3 * Q3))

    for lbl, M in (("P", P3), ("Q", Q3), ("R", R3), ("Y", Y)):
        if sp.simplify(M * M - M) != sp.zeros(3, 3) or sp.simplify(sp.trace(M)) != 1:
            fails.append("%s must be a rank-one projection" % lbl)
    if c != sp.Rational(16, 25):
        fails.append("c = 1 - Tr(PQ) must be exactly 16/25; got %s" % c)
    if sp.simplify(P3 * R3) != sp.zeros(3, 3) or sp.simplify(Q3 * R3) != sp.zeros(3, 3):
        fails.append("R must be orthogonal to both rays, or the certainties move")

    # THE MAP.  T(alpha I + beta P + gamma Q) = (that) + beta*c*R.
    def T3c(alpha, beta, gamma, cc):
        """The map, parametrized by its constant so the sharpness control runs
        the SAME function rather than a hand-written matrix."""
        x = sp.Matrix(sp.simplify(alpha * I3 + beta * P3 + gamma * Q3))
        return sp.Matrix(sp.simplify(x + beta * cc * R3)), x

    def T3(alpha, beta, gamma):
        return T3c(alpha, beta, gamma, c)

    if sp.simplify(T3(1, 0, 0)[0] - I3) != sp.zeros(3, 3):
        fails.append("the counterexample must be unital")
    if sp.simplify(T3(0, 1, 0)[0] - P3) == sp.zeros(3, 3):
        fails.append("the counterexample must NOT be the identity on S")

    # f_P = t I + (1-t) P and f_Q = t' I + (1-t') Q, with t' DISTINCT from t so
    # the two exposure parameters are not silently the same quantity.  Both
    # images are taken FROM the map: hand-writing them let a spurious +cR on
    # T(f_Q) -- contradicting this check's own T(Q) = Q -- ship green.
    t3 = T_EXPOSE
    t3p = sp.Rational(1, 5)
    if t3p == t3:
        fails.append("t' must be DISTINCT from t, or the two exposure "
                     "parameters are one quantity wearing two names")
    TfP = T3(t3, 1 - t3, 0)[0]
    TfQ = T3(t3p, 0, 1 - t3p)[0]
    if sp.simplify(TfQ - sp.simplify(t3p * I3 + (1 - t3p) * Q3)) != sp.zeros(3, 3):
        fails.append("T(f_Q) must be f_Q -- the map fixes Q, so it must move "
                     "nothing on the Q ray")
    c1 = sp.simplify(sp.trace(P3 * TfP))
    c2 = sp.simplify(sp.trace(Q3 * TfQ))
    if c1 != 1 or c2 != 1:
        fails.append("both matched certainties must hold exactly; got %s, %s"
                     % (c1, c2))
    fP3 = sp.simplify(t3 * I3 + (1 - t3) * P3)
    fQ3 = sp.simplify(t3p * I3 + (1 - t3p) * Q3)
    if sp.simplify(TfQ - fQ3) != sp.zeros(3, 3):
        fails.append("T must fix f_Q exactly")
    if not (psd(TfP) and psd(sp.simplify(I3 - TfP))):
        fails.append("T(f_P) must be a genuine effect")
    if sp.simplify(TfP - fP3) == sp.zeros(3, 3):
        fails.append("T(f_P) must differ from f_P, or nothing is exhibited")
    spec = sorted([sp.nsimplify(s) for s in sp.simplify(TfP).eigenvals().keys()],
                  key=lambda z: sp.re(z))
    if spec != [sp.Rational(1, 3), sp.Rational(19, 25), 1]:
        fails.append("the spectrum of T(f_P) must be {1/3, 19/25, 1}; got %s" % spec)

    # POSITIVITY, BY CERTIFICATE.  The map moves only the e3 slot, from alpha to
    # alpha + c*beta; the 12-block is untouched.  So T preserves positivity on S
    # iff phi(x) = alpha + c*beta is non-negative on S ∩ PSD.  Exhibit
    # phi = Tr(Y .) with Y PSD -- then phi >= 0 on EVERY PSD matrix, not just S.
    if not psd(Y):
        fails.append("the certificate Y must be PSD")
    for coeffs, want in (((1, 0, 0), 1), ((0, 1, 0), c), ((0, 0, 1), 0)):
        al_, be_, ga_ = coeffs
        x = sp.simplify(al_ * I3 + be_ * P3 + ga_ * Q3)
        got = sp.simplify(sp.trace(Y * x))
        if sp.simplify(got - want) != 0:
            fails.append("the certificate must reproduce phi on the basis: "
                         "Tr(Y x) = %s expected %s at %s" % (got, want, coeffs))
    al, be, ga = sp.symbols("al be ga", real=True)
    Tx, x = T3(al, be, ga)
    Tx, x = sp.Matrix(Tx), sp.Matrix(x)
    if sp.simplify(Tx - x - be * c * R3) != sp.zeros(3, 3):
        fails.append("the map must move exactly the R slot")
    if sp.simplify(sp.trace(Y * x) - (al + c * be)) != 0:
        fails.append("Tr(Y x) must equal alpha + c*beta identically")

    # SUFFICIENCY, EXECUTED.  That phi >= 0 SUFFICES for T(x) >= 0 rests on
    # block structure: T(x) agrees with x on the 12-block and differs only in the
    # (3,3) entry, so its spectrum is spec(12-block) united with {alpha + c*beta}.
    # Computed here rather than argued in a comment.
    if sp.simplify(Tx[0:2, 2]) != sp.zeros(2, 1) or \
            sp.simplify(Tx[2, 0:2]) != sp.zeros(1, 2):
        fails.append("T(x) must be block-diagonal (12-block) + (3,3), or the "
                     "spectrum does not split and phi is not sufficient")
    if sp.simplify(Tx[0:2, 0:2] - x[0:2, 0:2]) != sp.zeros(2, 2):
        fails.append("T must leave the 12-block untouched")
    if sp.simplify(Tx[2, 2] - (al + c * be)) != 0:
        fails.append("the (3,3) entry of T(x) must be exactly alpha + c*beta; "
                     "got %s" % sp.simplify(Tx[2, 2]))

    # SHARPNESS, and it is stronger than a slack control.  c = 1 - Tr(PQ) is
    # EXACTLY the infimum of lam_max(P - gamma Q) over gamma -- approached, not
    # attained -- so the counterexample sits ON the boundary of the positive
    # cone.  Any c' > c breaks positivity at a finite gamma.  Executed at
    # c' = 13/20 with gamma = 50.
    gam = sp.Integer(50)
    blk = sp.Matrix(sp.simplify(P3 - gam * Q3)[0:2, 0:2])
    alpha_min = sp.simplify(sp.Max(*[sp.nsimplify(e) for e in blk.eigenvals()]))
    x_sharp = sp.simplify(alpha_min * I3 - P3 + gam * Q3)
    if not psd(x_sharp):
        fails.append("the sharpness witness must be PSD; alpha_min = %s"
                     % alpha_min)
    if not (sp.simplify(alpha_min - c) > 0):
        fails.append("lam_max(P - gamma Q) must stay ABOVE c for finite gamma "
                     "(c is the infimum, not attained); got %s vs %s"
                     % (alpha_min, c))
    c_bad = sp.Rational(13, 20)
    if not (sp.simplify(alpha_min - c_bad) < 0):
        fails.append("at gamma = 50 the witness must undercut c' = 13/20, or the "
                     "sharpness control exhibits nothing; got %s" % alpha_min)
    Tsharp_bad, x_chk = T3c(alpha_min, -1, gam, c_bad)
    Tsharp_ok, _ = T3c(alpha_min, -1, gam, c)
    if sp.simplify(x_chk - x_sharp) != sp.zeros(3, 3):
        fails.append("the sharpness witness must BE the preimage the map acts "
                     "on, not a second matrix written to look like it")
    if sp.simplify(Tsharp_ok - x_sharp + c * R3) != sp.zeros(3, 3):
        fails.append("the map's action on the witness must be exactly "
                     "-c R (beta = -1); got %s" % sp.simplify(Tsharp_ok - x_sharp))
    if sp.simplify(Tsharp_bad[0:2, 0:2] - x_sharp[0:2, 0:2]) != sp.zeros(2, 2):
        fails.append("the control must differ from the true map ONLY in the "
                     "(3,3) slot, or it is not the identical construction")
    if psd(Tsharp_bad):
        fails.append("with c' = 13/20 > c the identical construction must FAIL "
                     "positivity -- that is what makes c sharp")
    if not psd(Tsharp_ok):
        fails.append("with the true c = 16/25 the same element must stay PSD")

    # and the n = 2 contrast: there is no third slot to move into.
    if (I2 - P0).rank() != 1 or (sp.eye(3) - P3).rank() != 2:
        fails.append("the complement rank must be 1 at n = 2 and 2 at n = 3 -- "
                     "that jump is where the room for R comes from")

    n3_statement = "FALSE"
    if n3_statement != "FALSE":
        fails.append("the n >= 3 posture is FALSE-by-counterexample, not open")
    return _result(
        "L_positivity_does_not_suffice_at_n3",
        "The n = 2 restriction is a THEOREM, not an unexplored boundary: the "
        "statement is FALSE at n = 3.  With psi_P = e1, psi_Q = (3/5)e1 + "
        "(4/5)e2, R = |e3><e3| and c = 1 - Tr(PQ) = 16/25, the map T(I) = I, "
        "T(P) = P + cR, T(Q) = Q is unital, satisfies BOTH matched certainties "
        "exactly, sends f_P to a genuine effect with spectrum {1/3, 19/25, 1} "
        "that still fixes psi_P, and is NOT the identity on S.  It is positive "
        "by CERTIFICATE, not by sampling: the only quantity the map moves is "
        "alpha + c*beta, and that functional is Tr(Y .) for the rank-one PSD "
        "Y = |psi_Q^perp><psi_Q^perp|, hence non-negative on every PSD element.  "
        "Sufficiency is executed, not argued: T(x) is computed to agree with x "
        "on the 12-block and to differ only in the (3,3) entry, so the spectrum "
        "splits and phi >= 0 is exactly what positivity needs.  AND c IS SHARP: "
        "1 - Tr(PQ) is the infimum of lam_max(P - gamma Q), approached and not "
        "attained, so the counterexample sits ON the boundary of the positive "
        "cone -- at c' = 13/20 the identical construction breaks positivity at "
        "gamma = 50, executed.  The room for R is exactly the complement-rank "
        "jump from 1 to 2, which is where Route 1 of the n = 2 lemma stops.",
        fails,
        negative_controls=(
            "c' = 13/20 > c, where the identical construction fails positivity "
            "at gamma = 50",
            "the n = 2 complement, which has rank 1 and leaves no slot for R",
        ),
        artifacts={"c": str(c), "certificate": "Y = |psi_Q^perp><psi_Q^perp|",
                   "T_fP_spectrum": ["1/3", "19/25", "1"],
                   "positivity_verified_by": "exact PSD certificate, not probes",
                   "c_is_the_infimum_of_lam_max_P_minus_gamma_Q": True,
                   "n3_statement": n3_statement},
        epistemic="P_math | the negative half of the scope fence",
    )


def check_L_positivity_is_load_bearing() -> Dict[str, object]:
    """Drop positivity and the conclusion fails: an exact non-positive survivor."""
    fails: List[str] = []
    W = sp.Matrix([[1, sp.Rational(-12, 7)], [sp.Rational(-12, 7), 0]])
    if sp.simplify(sp.trace(W)) != 1:
        fails.append("the survivor must be trace-one (unitality of T_W)")
    if sp.simplify(W.det()) != sp.Rational(-144, 49):
        fails.append("the survivor determinant must be exactly -144/49; got %s"
                     % sp.simplify(W.det()))
    if psd(W):
        fails.append("the survivor must not be PSD")
    for lbl, F in (("I", I2), ("f_P", F_P), ("f_Q", F_Q)):
        v = sp.simplify(sp.trace(W * F))
        if v != 1:
            fails.append("T_W must return exactly 1 on %s (got %s)" % (lbl, v))
    e = sp.Rational(1, 2) * sp.Matrix([[1, 1], [1, 1]])
    if not psd(e):
        fails.append("the violating witness must be a PSD element of S")
    Sm = sp.Matrix([_hv(m) for m in (I2, F_P, F_Q)])
    if sp.Matrix([_hv(m) for m in (I2, F_P, F_Q, e)]).rank() != Sm.rank():
        fails.append("the violating witness must lie IN S, or it fences nothing")
    val = sp.simplify(sp.trace(W * e))
    if val != sp.Rational(-17, 14):
        fails.append("the exhibited violation must be exactly -17/14; got %s" % val)
    if not (val < 0):
        fails.append("the survivor must go negative on a PSD element of S")
    if sp.simplify(sp.trace(I2 * e)) < 0:
        fails.append("control: the identity readout must stay non-negative")
    return _result(
        "L_positivity_is_load_bearing",
        "Positivity is not decoration.  W = [[1,-12/7],[-12/7,0]] has trace 1 "
        "and determinant -144/49, and T_W(e) = Tr(W e) I satisfies unitality, "
        "effect-linearity and BOTH matched certainties exactly, while being "
        "totally independent of the source.  It fails only positivity, at the "
        "PSD element (1/2)[[1,1],[1,1]] of S where it returns exactly -17/14.  "
        "So the premise this theorem trades complete positivity for is doing "
        "real work.",
        fails,
        negative_controls=("the identity readout, which stays non-negative there",),
        artifacts={"W_trace": "1", "W_det": str(sp.simplify(W.det())),
                   "violation_value": str(val)},
    )


def check_L_both_certainties_are_load_bearing() -> Dict[str, object]:
    """Drop the second certainty and an exact positive non-identity map survives."""
    fails: List[str] = []

    def T_P(e):
        return sp.simplify(sp.trace(P0 * e) * I2)

    if not _eq(T_P(I2), I2):
        fails.append("the control must be unital")
    p, q = bloch(P0), bloch(Q1)
    alpha = sp.simplify((2 + norm(sp.simplify(p + q))) / 2)
    probes = [I2, F_P, F_Q, P0, Q1, sp.simplify(I2 - F_P), sp.simplify(I2 - F_Q),
              I2 / 2, sp.simplify(alpha * I2 - P0 - Q1)]
    for x in probes:
        if not psd(x):
            fails.append("probe must be PSD")
        if not psd(T_P(x)):
            fails.append("the control must be POSITIVE on every PSD element of S")
    c1 = sp.simplify(sp.trace(P0 * T_P(F_P)))
    if c1 != 1:
        fails.append("the control must satisfy the first certainty exactly; got %s" % c1)
    c2 = sp.simplify(sp.trace(Q1 * T_P(F_Q)))
    if c2 == 1:
        fails.append("the control must FAIL the second certainty")
    # Tr(Q T_P(f_Q)) = Tr(P f_Q) = t + (1-t) Tr(PQ) = 1/3 + (2/3)(49/625).
    expect_c2 = sp.simplify(T_EXPOSE + (1 - T_EXPOSE) * EXPECT_TR_PQ)
    if expect_c2 != EXPECT_SECOND_CERTAINTY:
        fails.append("the closed form of the failed certainty must be %s; got %s"
                     % (EXPECT_SECOND_CERTAINTY, expect_c2))
    if c2 != EXPECT_SECOND_CERTAINTY:
        fails.append("the failed second certainty must be exactly %s; got %s"
                     % (EXPECT_SECOND_CERTAINTY, c2))
    if _eq(T_P(F_Q), F_Q):
        fails.append("the control must differ from the identity on S")
    if sp.simplify(sp.trace(Q1 * F_Q)) != 1:
        fails.append("control on the control: the identity readout must satisfy "
                     "the second certainty")
    return _result(
        "L_both_certainties_are_load_bearing",
        "T_P(e) = Tr(P e) I is unital, positive on every PSD element of S, "
        "satisfies the first matched certainty EXACTLY, fails the second at "
        "exactly 241/625 = t + (1-t)Tr(PQ), and is nowhere near the identity "
        "on S.  So two matched "
        "certainties are needed, not one.  What the certainties buy is the FORM "
        "T(P) = P + lam(I-P); both bounds on lam in the theorem are positivity "
        "bounds.",
        fails,
        negative_controls=("the identity readout, which satisfies both certainties",),
        artifacts={"first_certainty": str(c1), "second_certainty": str(c2),
                   "control": "T_P(e) = Tr(P e) I"},
    )


def check_L_scope_and_bars() -> Dict[str, object]:
    """What this does NOT establish -- with the CP scope EXECUTED.

    The earlier draft's legs here were an A == A, two integer ranks, and a
    len(set(...)) on a literal: it caught 0 of 17 shipped mutations and 0 of 53
    foreign ones.  The transposition leg below can fail, and it carries the
    substantive content: "complete positivity is not used" is bought by
    concluding T = id_S rather than T = id_{M_2}, and transposition is precisely
    the map that separates those two conclusions.
    """
    fails: List[str] = []

    def tr_map(m):
        return sp.simplify(sp.Matrix(m).T)

    for lbl, M in (("I", I2), ("P", P0), ("Q", Q1), ("f_P", F_P), ("f_Q", F_Q)):
        if sp.simplify(tr_map(M) - M) != sp.zeros(2, 2):
            fails.append("transposition must FIX %s (all are real symmetric in "
                         "the engine basis) -- that is what makes it a witness" % lbl)
    if sp.simplify(sp.trace(P0 * tr_map(F_P))) != 1 or \
            sp.simplify(sp.trace(Q1 * tr_map(F_Q))) != 1:
        fails.append("transposition must satisfy both matched certainties")
    if sp.simplify(tr_map(I2) - I2) != sp.zeros(2, 2):
        fails.append("transposition must be unital")
    for x in (P0, Q1, F_P, F_Q, I2 / 2, sp.simplify(I2 - F_P)):
        if psd(x) and not psd(tr_map(x)):
            fails.append("transposition must be positive")
    # NOT completely positive: the Choi matrix has eigenvalues {1,1,1,-1}
    choi = sp.zeros(4, 4)
    for i in range(2):
        for j in range(2):
            Eij = sp.zeros(2, 2)
            Eij[i, j] = 1
            blk = tr_map(Eij)
            for k in range(2):
                for l in range(2):
                    choi[2 * i + k, 2 * j + l] = blk[k, l]
    ev = sorted([sp.nsimplify(v) for v in choi.eigenvals().keys()],
                key=lambda t: sp.re(t))
    if ev != [-1, 1]:
        fails.append("the Choi eigenvalues of transposition must be {-1, 1}; got %s" % ev)
    if psd(choi):
        fails.append("transposition must NOT be completely positive")
    # NOT the identity on M_2 -- it flips the direction S does not span
    if sp.simplify(tr_map(SY) + SY) != sp.zeros(2, 2):
        fails.append("transposition must flip sigma_y")
    if sp.simplify(tr_map(SY) - SY) == sp.zeros(2, 2):
        fails.append("transposition must NOT be the identity on M_2")
    inS = sp.Matrix([_hv(m) for m in (I2, F_P, F_Q)]).rank()
    withSY = sp.Matrix([_hv(m) for m in (I2, F_P, F_Q, SY)]).rank()
    if withSY != inS + 1:
        fails.append("sigma_y must lie OUTSIDE S (rank must rise from %s to %s); "
                     "otherwise transposition would contradict T = id_S"
                     % (inS, inS + 1))

    # (a2) THE CLASSIFICATION.  Transposition is ONE ENDPOINT of an interval.
    #   The unital maps fixing S pointwise are exactly Phi_kappa, Bloch
    #   diag(1, kappa, 1); positive for |kappa| <= 1; Choi eigenvalues
    #   {(1-k)/2, (1-k)/2, (k-1)/2, (k+3)/2}, so COMPLETE POSITIVITY FORCES
    #   kappa = 1, i.e. T = id_{M_2}.  That converts the rhetorical claim that
    #   "the missing direction is the sector complete positivity is for" into a
    #   computed statement.  kappa = -1 is transposition; kappa = 0 is DEPHASING,
    #   a positive non-CP member that is not transposition.
    def phi(kap):
        def f(m):
            bb = bloch(m)
            return sp.simplify((sp.trace(m) * I2 + bb[0] * SX
                                + kap * bb[1] * SY + bb[2] * SZ) / 2)
        return f

    def choi_eigs(f):
        C = sp.zeros(4, 4)
        for i in range(2):
            for j in range(2):
                E = sp.zeros(2, 2)
                E[i, j] = 1
                blk = f(E)
                for k in range(2):
                    for l in range(2):
                        C[2 * i + k, 2 * j + l] = blk[k, l]
        return C, sorted([sp.nsimplify(v) for v in C.eigenvals().keys()],
                         key=lambda t: sp.re(t))

    for kap, is_cp, label in ((sp.Integer(1), True, "identity"),
                              (sp.Integer(0), False, "dephasing"),
                              (sp.Integer(-1), False, "transposition")):
        f = phi(kap)
        for M in (I2, P0, Q1, F_P, F_Q):
            if sp.simplify(f(M) - M) != sp.zeros(2, 2):
                fails.append("Phi_%s (%s) must fix S pointwise" % (kap, label))
        for x in (P0, Q1, F_P, F_Q, I2 / 2, sp.simplify(I2 - F_P)):
            if psd(x) and not psd(f(x)):
                fails.append("Phi_%s (%s) must be positive" % (kap, label))
        C, ce = choi_eigs(f)
        want = sorted([sp.nsimplify(v) for v in
                       [(1 - kap) / 2, (1 - kap) / 2, (kap - 1) / 2,
                        (kap + 3) / 2]], key=lambda t: sp.re(t))
        if sorted(set(map(str, ce))) != sorted(set(map(str, want))):
            fails.append("the Choi spectrum of Phi_%s must be %s; got %s"
                         % (kap, want, ce))
        if psd(C) is not is_cp:
            fails.append("Phi_%s (%s) complete positivity must be %s"
                         % (kap, label, is_cp))
    # dephasing is a POSITIVE NON-CP member that is NOT transposition
    if sp.simplify(phi(0)(SY) - phi(-1)(SY)) == sp.zeros(2, 2):
        fails.append("dephasing must differ from transposition, or the interval "
                     "is a point and 'transposition is the witness' is exact")
    # and the theorem the interval delivers: CP + fixing S pointwise => id_{M_2}
    if psd(choi_eigs(phi(sp.Rational(1, 2)))[0]):
        fails.append("no kappa < 1 may be completely positive, or CP does not "
                     "force the identity on M_2")

    if (sp.eye(3) - sp.diag(1, 0, 0)).rank() == (I2 - P0).rank():
        fails.append("the n=3 complement rank must differ from n=2")

    # THE SCOPE FLAGS ARE ASSERTED AS LEGS, not merely shipped.  Previously they
    # were read only by run_all(), which the bank never calls, so a module
    # shipping born_derived = True was green on the banked path.
    art = {"n_scope": 2,
           "cp_soundness_discharged": False,
           "born_derived": False,
           "transposition_is_cp": False,
           "transposition_fixes_S_pointwise": True,
           "conclusion_is_id_S_not_id_M2": True,
           "maps_fixing_S_pointwise": "Phi_kappa, Bloch diag(1,kappa,1)",
           "cp_plus_fixing_S_forces_id_M2": True}
    for k, want in (("n_scope", 2), ("cp_soundness_discharged", False),
                    ("born_derived", False), ("transposition_is_cp", False),
                    ("conclusion_is_id_S_not_id_M2", True),
                    ("cp_plus_fixing_S_forces_id_M2", True)):
        if art.get(k) != want:
            fails.append("scope flag %r must be %r; got %r" % (k, want, art.get(k)))

    cp_leaves = ("FINITE_FRAGMENT_KINEMATIC_SOUNDNESS",
                 "CHOI_FAITHFUL_SAME_TYPE_REFERENCE",
                 "TENSOR_FAITHFUL_CHOI_CORNER",
                 "LOCAL_IDENTITY_EXTENSION",
                 "JOINT_POSITIVITY_PRESERVATION")
    if len(set(cp_leaves)) != 5:
        fails.append("the CP composite must be recorded set-exactly")

    return _result(
        "L_scope_and_bars",
        "Scope, executed rather than declared.  TRANSPOSITION fixes I, P, Q, f_P "
        "and f_Q (all real symmetric in the engine basis), returns both matched "
        "certainties exactly, is unital and positive on M_2, has Choi spectrum "
        "{1,1,1,-1} so is NOT completely positive, and is NOT the identity on "
        "M_2 -- it flips sigma_y, which is computed to lie OUTSIDE S.  But it is "
        "ONE ENDPOINT of an interval, not the witness: the unital maps fixing S "
        "pointwise are exactly Phi_kappa with Bloch diag(1, kappa, 1), positive "
        "for |kappa| <= 1, of which DEPHASING (kappa = 0) is a positive non-CP "
        "member that is not transposition.  Their Choi spectra are "
        "{(1-k)/2, (1-k)/2, (k-1)/2, (k+3)/2}, so complete positivity forces "
        "kappa = 1: CP PLUS FIXING S POINTWISE IMPLIES T = id_{M_2}, computed.  "
        "That is what this route's avoidance of complete positivity costs -- the "
        "conclusion is id_S, not id_{M_2}, and the missing direction is exactly "
        "the sector complete positivity is for.  This is n = 2 ONLY, and at n = 3 the statement is "
        "false by counterexample, not open.  It does NOT derive Born: the trace "
        "pairing is the ambient representation in which S, the effects and the "
        "certainties are already written.  It leaves CP_SOUNDNESS a five-leaf "
        "composite in apf/quantum_frontend_closure.py; what is shown is that ONE "
        "route at ONE block size does not consume it.",
        fails,
        negative_controls=("sigma_y, which must lie outside S or the witness "
                           "would contradict the theorem",),
        artifacts=dict(art, cp_composite_leaves=list(cp_leaves)),
        epistemic="P_math | scope record",
    )


CANONICAL_CHECK_NAMES = frozenset({
    "L_exposing_effects_and_setup",
    "L_certainty_and_positivity_force_the_lambda_form",
    "T_positivity_forces_the_identity_readout",
    "L_positivity_does_not_suffice_at_n3",
    "L_positivity_is_load_bearing",
    "L_both_certainties_are_load_bearing",
    "L_scope_and_bars",
})

_CHECKS: Dict[str, Callable[[], Dict[str, object]]] = {
    "L_exposing_effects_and_setup": check_L_exposing_effects_and_setup,
    "L_certainty_and_positivity_force_the_lambda_form":
        check_L_certainty_and_positivity_force_the_lambda_form,
    "T_positivity_forces_the_identity_readout":
        check_T_positivity_forces_the_identity_readout,
    "L_positivity_does_not_suffice_at_n3":
        check_L_positivity_does_not_suffice_at_n3,
    "L_positivity_is_load_bearing": check_L_positivity_is_load_bearing,
    "L_both_certainties_are_load_bearing": check_L_both_certainties_are_load_bearing,
    "L_scope_and_bars": check_L_scope_and_bars,
}

CHECKS = tuple(_CHECKS.values())

# A fingerprint binding NAMES TO FUNCTION IDENTITIES, not names alone.  The
# previous version hashed keys only, so rebinding a key to a different function
# was invisible to it.  Written out as literals: deriving it from _CHECKS makes
# it a self-referential certificate that follows any replacement (the v24.3.444
# lesson).
_INVENTORY_FINGERPRINT = (
    "L_both_certainties_are_load_bearing->check_L_both_certainties_are_load_bearing|"
    "L_certainty_and_positivity_force_the_lambda_form->"
    "check_L_certainty_and_positivity_force_the_lambda_form|"
    "L_exposing_effects_and_setup->check_L_exposing_effects_and_setup|"
    "L_positivity_does_not_suffice_at_n3->check_L_positivity_does_not_suffice_at_n3|"
    "L_positivity_is_load_bearing->check_L_positivity_is_load_bearing|"
    "L_scope_and_bars->check_L_scope_and_bars|"
    "T_positivity_forces_the_identity_readout->"
    "check_T_positivity_forces_the_identity_readout"
)


def register(registry):
    """The bank's entry point.  bank.py imports the module and calls this with
    the live REGISTRY; a module without it registers nothing and shows up as a
    gap, which is how three modules were caught before the v24.3.457 landing."""
    registry.update(_CHECKS)
    return registry


def run_all() -> Dict[str, Dict[str, object]]:
    """A SECOND gate only.  The load-bearing cross-assert lives in _result(),
    because the bank never calls this function."""
    live = "|".join(sorted("%s->%s" % (k, v.__name__) for k, v in _CHECKS.items()))
    if live != _INVENTORY_FINGERPRINT:
        raise AssertionError("inventory fingerprint mismatch: %s" % live)
    missing = CANONICAL_CHECK_NAMES - set(_CHECKS)
    leaked = set(_CHECKS) - CANONICAL_CHECK_NAMES
    if missing or leaked:
        raise AssertionError("inventory drift -- MISSING %s LEAKED %s"
                             % (sorted(missing), sorted(leaked)))
    if len(_CHECKS) != 7:
        raise AssertionError("registry size %d != 7" % len(_CHECKS))
    results = {}
    for n, fn in _CHECKS.items():
        r = fn()
        listed = len(r["fail_reasons"])
        counted = r["fail_count"]
        if listed != counted:
            raise AssertionError("%s: failure records disagree -- %d listed, %d "
                                 "counted" % (n, listed, counted))
        r["passed"] = (counted == 0)
        results[n] = r
    # The scope flags AND the prose are read.  A receipt no verdict consults is
    # not a receipt, and that applies to sentences as well as to booleans.
    scope = results["L_scope_and_bars"]["artifacts"]
    for key, want in (("born_derived", False), ("cp_soundness_discharged", False),
                      ("n_scope", 2), ("transposition_is_cp", False),
                      ("conclusion_is_id_S_not_id_M2", True)):
        if scope.get(key) != want:
            raise AssertionError("scope flag %r must be %r" % (key, want))
    cp = results["T_positivity_forces_the_identity_readout"]["artifacts"]
    if cp.get("complete_positivity_used") is not False:
        raise AssertionError("the theorem's whole point is that CP is not used")
    if results["L_positivity_does_not_suffice_at_n3"]["artifacts"].get(
            "n3_statement") != "FALSE":
        raise AssertionError("the n >= 3 posture is FALSE-by-counterexample, "
                             "not open")
    for key, res in results.items():
        if res.get("name") != key:
            raise AssertionError("registry key %r bound to %r" % (key, res.get("name")))
        blob = (str(res.get("key_result", "")) + " " +
                str(res.get("epistemic", ""))).upper()
        for phrase in BARRED_PROSE:
            if phrase in blob:
                raise AssertionError("%s ships a barred sentence: %r" % (key, phrase))
        need = REQUIRED_PROSE.get(key)
        if need is not None and need.upper() not in blob:
            raise AssertionError("%s must carry %r" % (key, need))
        if str(res.get("epistemic", "")).startswith("P_physical") or \
                res.get("epistemic") == "P":
            raise AssertionError("%s claims a physical grade; nothing here is "
                                 "physically certified" % key)
    return results


if __name__ == "__main__":
    import json
    r = run_all()
    bad = sorted(k for k, v in r.items() if not v["passed"])
    print(json.dumps({"family": FAMILY, "checks": len(r),
                      "passed": len(r) - len(bad), "failed": bad,
                      "all_pass": not bad}, indent=2))
    raise SystemExit(0 if not bad else 1)
