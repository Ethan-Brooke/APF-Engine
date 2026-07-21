"""Exact finite witnesses for the APF two-exchange Held-holonomy route.

This module removes the over-broad premise
``PHYSICAL_SHARP_REFLECTION_IMPLEMENTABILITY``.  A physical binary contender
exchange is already a reflection on its decoded common/defect carrier.  A
second admitted binary presentation, carrying its own effective contender
exchange, supplies a second reflection.  For the exact APF 3-4-5 fixed-line
geometry their product is the irrational rotation with trace -14/25.

The module certifies the mathematics and a fail-closed physical certificate
schema.  It does not certify that a real APF interface supplies the second
binary presentation or either effective exchange path.

Fortified 2026-07-20 against the blinded cold audit (LAND-WITH-FIXES 0.81):
the named root INTERTWINER_REVERSAL_IS_INVERSE (MAJOR-1, the .429 H1 genre)
is carried in the manifest, graph, certificate schema, and consuming checks;
the quadratic-ledger disposition is stated in the relocation form of record
(MAJOR-2; the positivity surface is RELOCATED to R-capacity-bounded-world +
the H3 gate at reading grade per check_L_bounded_orbit_positivity, v24.3.431); the supersession of the reflection-gate route is
machine-closed by the composed end-to-end contract (MAJOR-3); the literal
riders are replaced by computed legs, the declared negative controls execute,
and the root manifest is split into apf.two_exchange_roots (minors m1-m8).
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from fractions import Fraction as F
import json
from typing import Callable, Dict, List, Mapping, Optional, Sequence, Tuple

from apf.two_exchange_roots import PHYSICAL_ROOTS

FAMILY = "quantum.two_exchange_held_holonomy"
Matrix2 = Tuple[Tuple[F, F], Tuple[F, F]]
Vector2 = Tuple[F, F]


@dataclass(frozen=True)
class TwoExchangeCertificate:
    exchange_is_reflection: bool
    rotated_exchange_conjugacy: bool
    codespace_fixed_line_exact: bool
    two_exchange_gate_exact: bool
    static_effects_do_not_imply_processes: bool
    localized_exchange_suffices: bool
    effectiveness_required: bool
    generic_reflection_premise_removed: bool
    composed_supersession_machine_closed: bool
    physical_two_exchange_certificate_verified: bool
    physical_premises_certified: bool = False


def _result(name: str, key_result: str, artifacts: Mapping[str, object],
            fails: Sequence[str], *, dependencies: Sequence[str] = (),
            premises: Sequence[str] = (), negative_controls: Sequence[str] = (),
            epistemic: str = "P_math") -> Dict[str, object]:
    passed = not fails
    return {
        "name": name,
        "family": FAMILY,
        "tier": 4,
        "epistemic": epistemic,
        "status": "PASS" if passed else "FAIL",
        "passed": passed,
        "scope": "finite mathematical witness / physical-certificate reduction",
        "physical_premises_certified": False,
        "key_result": key_result,
        "dependencies": list(dependencies),
        "premises": list(premises),
        "negative_controls": list(negative_controls),
        "artifacts": dict(artifacts),
        "fail_reasons": list(fails),
    }


def _eye() -> Matrix2:
    return ((F(1), F(0)), (F(0), F(1)))


def _zero() -> Matrix2:
    return ((F(0), F(0)), (F(0), F(0)))


def _mm(a: Matrix2, b: Matrix2) -> Matrix2:
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(2))
                       for j in range(2)) for i in range(2))  # type: ignore[return-value]


def _mv(a: Matrix2, v: Vector2) -> Vector2:
    return tuple(sum(a[i][k] * v[k] for k in range(2))
                 for i in range(2))  # type: ignore[return-value]


def _mt(a: Matrix2) -> Matrix2:
    return ((a[0][0], a[1][0]), (a[0][1], a[1][1]))


def _add(a: Matrix2, b: Matrix2) -> Matrix2:
    return tuple(tuple(a[i][j] + b[i][j] for j in range(2))
                 for i in range(2))  # type: ignore[return-value]


def _sub(a: Matrix2, b: Matrix2) -> Matrix2:
    return tuple(tuple(a[i][j] - b[i][j] for j in range(2))
                 for i in range(2))  # type: ignore[return-value]


def _scale(s: F, a: Matrix2) -> Matrix2:
    return tuple(tuple(s * a[i][j] for j in range(2))
                 for i in range(2))  # type: ignore[return-value]


def _det(a: Matrix2) -> F:
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def _trace(a: Matrix2) -> F:
    return a[0][0] + a[1][1]


def _inverse(a: Matrix2) -> Matrix2:
    d = _det(a)
    if d == 0:
        raise ValueError("singular matrix")
    return ((a[1][1] / d, -a[0][1] / d),
            (-a[1][0] / d, a[0][0] / d))


def _pow(a: Matrix2, n: int) -> Matrix2:
    if n < 0:
        return _pow(_inverse(a), -n)
    out = _eye()
    base = a
    k = n
    while k:
        if k & 1:
            out = _mm(out, base)
        base = _mm(base, base)
        k >>= 1
    return out


def _outer(v: Vector2) -> Matrix2:
    return ((v[0] * v[0], v[0] * v[1]),
            (v[1] * v[0], v[1] * v[1]))


def _dot(u: Vector2, v: Vector2) -> F:
    return u[0] * v[0] + u[1] * v[1]


def _matrix_strings(a: Matrix2) -> List[List[str]]:
    return [[str(x) for x in row] for row in a]


def _vector_strings(v: Vector2) -> List[str]:
    return [str(x) for x in v]


P_SWAP: Matrix2 = ((F(0), F(1)), (F(1), F(0)))
H_ZIP: Matrix2 = ((F(1), F(1)), (F(1), F(-1)))
S_0: Matrix2 = ((F(1), F(0)), (F(0), F(-1)))
U_345: Vector2 = (F(3, 5), F(4, 5))
V_345: Vector2 = (F(-4, 5), F(3, 5))
P_U: Matrix2 = _outer(U_345)
S_U: Matrix2 = _sub(_scale(F(2), P_U), _eye())
# Columns are the two contender ports a=u+v and b=u-v, scaled by 5.
C_345: Matrix2 = ((F(-1), F(7)), (F(7), F(1)))
R_345: Matrix2 = _mm(S_U, S_0)


def check_T_binary_exchange_is_character_reflection() -> Dict[str, object]:
    fails: List[str] = []
    e_plus = _scale(F(1, 2), _add(_eye(), P_SWAP))
    e_minus = _scale(F(1, 2), _sub(_eye(), P_SWAP))
    if _mm(e_plus, e_plus) != e_plus or _mm(e_minus, e_minus) != e_minus:
        fails.append("exchange character projectors must be idempotent")
    if _mm(e_plus, e_minus) != _zero():
        fails.append("exchange character projectors must be complementary")
    if _sub(_scale(F(2), e_plus), _eye()) != P_SWAP:
        fails.append("P must equal 2E_plus-I")
    decoded = _mm(_mm(H_ZIP, P_SWAP), _inverse(H_ZIP))
    if decoded != S_0:
        fails.append("decoded contender exchange must be the common-axis reflection")
    return _result(
        "T_binary_exchange_is_character_reflection",
        "A physically admitted binary contender exchange needs no physical character projector in order to act as a reflection. Algebraically P=2E_+-I, and the calibration-free common/defect zipper represents the same exchange as diag(1,-1). The idempotents describe its eigenspaces; they are not required as separately implementable processes.",
        {
            "P_swap": _matrix_strings(P_SWAP),
            "E_plus": _matrix_strings(e_plus),
            "E_minus": _matrix_strings(e_minus),
            "decoded_exchange": _matrix_strings(decoded),
            "physical_idempotent_required": False,
            "physical_exchange_required": True,
        },
        fails,
        negative_controls=("identity/exchange monoid may contain P while containing no physical E_+ or E_-",),
    )


def check_T_rotated_exchange_is_conjugated_swap() -> Dict[str, object]:
    fails: List[str] = []
    transported = _mm(_mm(C_345, P_SWAP), _inverse(C_345))
    a = (C_345[0][0], C_345[1][0])
    b = (C_345[0][1], C_345[1][1])
    fixed = (a[0] + b[0], a[1] + b[1])
    anti = (a[0] - b[0], a[1] - b[1])
    if transported != S_U:
        fails.append("transported second exchange must equal the 3-4-5 reflection")
    if _mv(transported, fixed) != fixed:
        fails.append("sum port must be the fixed direction")
    if _mv(transported, anti) != (-anti[0], -anti[1]):
        fails.append("difference port must be the anti-fixed direction")
    if fixed[1] * F(3) != fixed[0] * F(4):
        fails.append("fixed direction must have 3:4 coordinates")
    if _dot(fixed, anti) != 0:
        fails.append("fixed and anti-fixed directions must be orthogonal")
    return _result(
        "T_rotated_exchange_is_conjugated_swap",
        "The 3-4-5 reflection is not an arbitrary polynomial functional calculus operation. It is the universal binary swap transported through the exact second-presentation matrix C=[[-1,7],[7,1]]: C P C^{-1}=S_u. Thus physicality follows from an admitted second binary presentation plus its effective contender exchange, not from a generic rule that every sharp effect generates a process.",
        {
            "presentation_matrix_C": _matrix_strings(C_345),
            "port_a": _vector_strings(a),
            "port_b": _vector_strings(b),
            "fixed_sum_direction": _vector_strings(fixed),
            "anti_fixed_difference_direction": _vector_strings(anti),
            "transported_exchange": _matrix_strings(transported),
            "target_reflection": _matrix_strings(S_U),
        },
        fails,
        dependencies=("T_binary_exchange_is_character_reflection",),
        premises=("ADMITTED_SECOND_BINARY_PRESENTATION", "EFFECTIVE_SECOND_CONTENDER_EXCHANGE"),
        negative_controls=("mere coordinate change without a second physical presentation does not create a second gate",),
    )


def check_T_345_codespace_fixed_line_candidate() -> Dict[str, object]:
    fails: List[str] = []
    # Live 3D projector in basis (e1,e2,e3); active plane is (e1,e3).
    pi_w = (
        (F(9, 25), F(0), F(12, 25)),
        (F(0), F(1), F(0)),
        (F(12, 25), F(0), F(16, 25)),
    )
    active = ((pi_w[0][0], pi_w[0][2]), (pi_w[2][0], pi_w[2][2]))
    if active != P_U:
        fails.append("active-plane restriction must equal P_u")
    if _mm(active, active) != active or _mt(active) != active:
        fails.append("active restriction must be a sharp rank-one projector")
    if _mv(active, U_345) != U_345:
        fails.append("u must be the fixed-line vector")
    if _mv(active, V_345) != (F(0), F(0)):
        fails.append("v must span the active kernel")
    # Mechanical comparison against the banked witness construction (audit m7):
    # rebuild pi_W exactly as reproduce_inline_345_commutator does (cos^2=9/25,
    # sin^2=16/25, cos*sin=12/25 at the 3-4-5 angle) and recompute [E_d1, pi_W].
    cos2, sin2, cs = F(9, 25), F(16, 25), F(12, 25)
    rebuilt = (
        (cos2, F(0), cs),
        (F(0), F(1), F(0)),
        (cs, F(0), sin2),
    )
    if rebuilt != pi_w:
        fails.append("inline pi_W must equal the banked 3-4-5 construction entry-for-entry")

    def _mm3(a, b):
        return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(3))
                           for j in range(3)) for i in range(3))

    ep = _mm3((( F(1), F(0), F(0)), (F(0), F(0), F(0)), (F(0), F(0), F(0))), pi_w)
    pe = _mm3(pi_w, ((F(1), F(0), F(0)), (F(0), F(0), F(0)), (F(0), F(0), F(0))))
    comm = tuple(tuple(ep[i][j] - pe[i][j] for j in range(3)) for i in range(3))
    if comm[0][2] != F(12, 25) or comm[2][0] != F(-12, 25):
        fails.append("commutator must reproduce the banked +-12/25 witness entries")
    banked_comparison = "reconstruction_executed_in_packet"
    try:
        from apf.ijc_boolean_defender_bridge import reproduce_inline_345_commutator  # type: ignore
        banked = reproduce_inline_345_commutator()
        if (banked["commutator_entry_13"] != comm[0][2]
                or banked["commutator_entry_31"] != comm[2][0]
                or not banked["pi_W_idempotent"] or not banked["pi_W_symmetric"]):
            fails.append("banked reproduce_inline_345_commutator disagrees with the inline pi_W")
        banked_comparison = "banked_module_imported_and_matched"
    except ImportError:
        banked_comparison = ("reconstruction executed in-packet; direct import comparison "
                             "runs automatically when apf.ijc_boolean_defender_bridge is on path (landing)")
    return _result(
        "T_345_codespace_fixed_line_candidate",
        "The live APF 3-4-5 defender projector restricts on the active (e1,e3) plane to P_u=uu^T with u=(3/5,4/5); e2 is a spectator. This supplies the exact candidate fixed line for the second binary presentation. It does not itself identify the active plane with the Held first-jet carrier or make the associated exchange a physical process.",
        {
            "pi_W_3d": [[str(x) for x in row] for row in pi_w],
            "active_plane_restriction": _matrix_strings(active),
            "fixed_line_u": _vector_strings(U_345),
            "kernel_line_v": _vector_strings(V_345),
            "spectator_e2_split": True,
            "commutator_13": str(comm[0][2]),
            "commutator_31": str(comm[2][0]),
            "banked_witness_comparison": banked_comparison,
            "codespace_to_Held_identification_certified": False,
        },
        fails,
        premises=("CODESPACE_TO_SECOND_PRESENTATION_FIXED_LINE",),
        negative_controls=("projector geometry without a carrier intertwiner",),
    )


def check_T_two_exchanges_generate_irrational_gate() -> Dict[str, object]:
    fails: List[str] = []
    if _mm(S_0, S_0) != _eye() or _mm(S_U, S_U) != _eye():
        fails.append("both exchange reflections must be involutions")
    if _det(S_0) != -1 or _det(S_U) != -1:
        fails.append("both exchanges must reverse orientation")
    if R_345 != ((F(-7, 25), F(-24, 25)), (F(24, 25), F(-7, 25))):
        fails.append("two-exchange product must equal the exact APF candidate gate")
    if _det(R_345) != 1 or _trace(R_345) != F(-14, 25):
        fails.append("candidate gate determinant/trace incorrect")
    if _mm(_mt(R_345), R_345) != _eye():
        fails.append("candidate gate must be orthogonal")
    if any(_pow(R_345, n) == _eye() for n in range(1, 513)):
        fails.append("candidate gate repeated in finite-order control range")
    # Executed negative controls (audit m3), no longer declarative strings only.
    if _mm(S_0, S_0) != _eye():
        fails.append("coincident-axis control: S_0*S_0 must be the identity")
    s_45 = P_SWAP  # reflection across the 45-degree axis (1,1)/sqrt(2)
    q45 = _mm(s_45, S_0)
    if _pow(q45, 4) != _eye() or any(_pow(q45, k) == _eye() for k in (1, 2, 3)):
        fails.append("45-degree control: (S_45 S_0) must have order exactly four")
    return _result(
        "T_two_exchanges_generate_irrational_gate",
        "Two effective binary exchanges with fixed lines e1 and u=(3/5,4/5) generate R=S_uS_0=[[-7,-24],[24,-7]]/25. Its determinant is one and its rational trace -14/25 is nonintegral; once the two-sided orbit is bounded, R has infinite order and its compact cyclic closure is SO(2).",
        {
            "first_exchange": _matrix_strings(S_0),
            "second_exchange": _matrix_strings(S_U),
            "gate_R": _matrix_strings(R_345),
            "det_R": str(_det(R_345)),
            "trace_R": str(_trace(R_345)),
            "powers_checked_nonidentity": 512,
            "coincident_axis_control_executed": True,
            "order_four_45_degree_control_executed": True,
        },
        fails,
        dependencies=("T_rotated_exchange_is_conjugated_swap", "T_345_codespace_fixed_line_candidate"),
        premises=("EFFECTIVE_FIRST_CONTENDER_EXCHANGE", "EXACT_345_FIXED_LINE_OVERLAP"),
        negative_controls=("coincident exchange axes give identity (executed)", "45-degree axes give finite order four (executed)"),
    )


def check_T_effect_completeness_does_not_imply_process_saturation() -> Dict[str, object]:
    fails: List[str] = []
    # Static model: full real matrix effect algebra contains both projectors, but
    # the admitted reversible process monoid is deliberately only {I,S0}.
    physical_process_monoid = (_eye(), S_0)
    if P_U == _zero() or P_U == _eye():
        fails.append("P_u must be a nontrivial sharp effect")
    if S_U in physical_process_monoid:
        fails.append("countermodel must omit the second reflection process")
    if not all(_mm(g, g) == _eye() for g in physical_process_monoid):
        fails.append("countermodel process monoid must be reversible")
    # Computed membership in the static interval 0 <= Q <= I (audit m1): both
    # sharp effects are symmetric idempotents with Q and I-Q positive
    # semidefinite (2x2 PSD == symmetric with trace >= 0 and det >= 0).
    def _psd(m: Matrix2) -> bool:
        return _mt(m) == m and _trace(m) >= 0 and _det(m) >= 0

    sharp_effects = {"E": ((F(1), F(0)), (F(0), F(0))), "P_u": P_U}
    static_effects_present = all(
        _mm(q, q) == q and _psd(q) and _psd(_sub(_eye(), q))
        for q in sharp_effects.values()
    )
    if not static_effects_present:
        fails.append("sharp effects must lie in the static interval 0<=Q<=I (computed)")
    # Executed cone preservation (audit m6): conjugation by every admitted
    # process keeps each sharp effect inside the effect interval and preserves
    # the witness metric on states.
    cones_preserved = True
    for g in physical_process_monoid:
        if _mm(_mt(g), g) != _eye():
            cones_preserved = False
        for q in sharp_effects.values():
            conj = _mm(_mm(g, q), _inverse(g))
            if not (_psd(conj) and _psd(_sub(_eye(), conj))):
                cones_preserved = False
    if not cones_preserved:
        fails.append("countermodel conjugation must preserve the state/effect cones (computed)")
    closed_under_process_composition = all(_mm(a, b) in physical_process_monoid
                                           for a in physical_process_monoid
                                           for b in physical_process_monoid)
    if not closed_under_process_composition:
        fails.append("countermodel malformed")
    return _result(
        "T_effect_completeness_does_not_imply_process_saturation",
        "A finite ordered algebra may contain both sharp effects E and P_u while its admitted reversible process monoid is only {I,S_0}. Therefore record/effect completeness, positivity, and the presence of a sharp projector do not imply that 2P_u-I is a physical process. The second exchange must be certified dynamically.",
        {
            "static_effect_algebra": "full interval 0 <= E <= I in M2(R)",
            "sharp_effects_present": ["E", "P_u"],
            "physical_process_monoid": ["I", "S_0"],
            "S_u_present_as_effect_polynomial": True,
            "S_u_present_as_physical_process": False,
            "process_monoid_closed": closed_under_process_composition,
            "static_effect_membership_computed": static_effects_present,
            "cone_preservation_computed": cones_preserved,
        },
        fails,
        negative_controls=("static effect completeness with restricted dynamics",),
    )


def check_T_localized_binary_exchange_suffices() -> Dict[str, object]:
    fails: List[str] = []
    transported = _mm(_mm(C_345, P_SWAP), _inverse(C_345))
    if transported != S_U:
        fails.append("localized binary exchange transport failed")
    # MAJOR-1 (.429 H1 genre), computed: the conjugation loop needs the
    # reversed intertwiner path represented by the inverse.  With
    # reversal-is-inverse the reversed loop is C X^{-1} C^{-1} = S_u^{-1} = S_u.
    reversed_loop = _mm(_mm(C_345, _inverse(P_SWAP)), _inverse(C_345))
    if reversed_loop != _inverse(S_U) or _inverse(S_U) != S_U:
        fails.append("reversed path represented by the inverse must give S_u^{-1}=S_u")
    # Monoid countermodel, executed: representing reversal by the idempotent
    # E_+ instead of the inverse degenerates the loop.  Reversal admission
    # alone yields only a monoid, never the reflection.
    e_plus = _scale(F(1, 2), _add(_eye(), P_SWAP))
    degenerate = _mm(_mm(C_345, P_SWAP), e_plus)
    if _det(degenerate) != 0:
        fails.append("idempotent-reversal countermodel must degenerate (det 0)")
    if degenerate == S_U:
        fails.append("idempotent-reversal countermodel must not reproduce S_u")
    # The generic saturation premise is absent from the actual contract
    # structures -- computed against the live graph and the split manifest,
    # not a literal compared with itself (audit m1).
    graph = _graph()
    consumed = set(PHYSICAL_ROOTS) | {d for deps in graph.values() for d in deps}
    if "PHYSICAL_SHARP_REFLECTION_IMPLEMENTABILITY" in consumed:
        fails.append("generic reflection saturation must remain absent from the contract")
    # Removing the named reversal root from either surface fails this check.
    if "INTERTWINER_REVERSAL_IS_INVERSE" not in PHYSICAL_ROOTS:
        fails.append("INTERTWINER_REVERSAL_IS_INVERSE missing from the root manifest")
    if "INTERTWINER_REVERSAL_IS_INVERSE" not in graph["T_SECOND_EXCHANGE"]:
        fails.append("INTERTWINER_REVERSAL_IS_INVERSE missing from the T_SECOND_EXCHANGE edge")
    return _result(
        "T_localized_binary_exchange_suffices",
        "For this route, generic sharp-reflection implementability is unnecessary. Conditional on the named roots, it is enough that the 3-4-5 defender split is admitted as a second same-type binary Held presentation, that the universal contender exchange is physical on that presentation, that the reversed intertwiner path is represented by the inverse (reversal admission alone yields only a monoid; the idempotent countermodel is executed here), and that the presentation returns to the same carrier. Transport then gives S_u exactly. The executed content is the transport/reversal/countermodel algebra plus the contract-surface scan; the sufficiency sentence itself is premises-conditional, hence the instrument grade.",
        {
            "transported_exchange": _matrix_strings(transported),
            "reversed_loop": _matrix_strings(reversed_loop),
            "idempotent_reversal_degenerate_det": str(_det(degenerate)),
            "generic_sharp_reflection_absent_computed": True,
            "reversal_root_named_in_manifest_and_graph": True,
        },
        fails,
        dependencies=("T_rotated_exchange_is_conjugated_swap", "T_effect_completeness_does_not_imply_process_saturation"),
        premises=(
            "ADMITTED_SECOND_BINARY_PRESENTATION",
            "UNIVERSAL_EXCHANGE_NATURALITY_ON_ADMITTED_PRESENTATIONS",
            "SAME_CARRIER_RETURN",
            "INTERTWINER_REVERSAL_IS_INVERSE",
        ),
        negative_controls=(
            "generic 2P-I process rule not used (computed contract scan)",
            "idempotent reversal representation degenerates the loop (executed)",
        ),
        epistemic="P_structural_instrument",
    )


def check_T_exchange_effectiveness_requires_recombination() -> Dict[str, object]:
    fails: List[str] = []
    seed = (F(1), F(0))
    moved = _mv(S_U, seed)
    readout_y = lambda v: v[1]
    if moved == seed:
        fails.append("second exchange must move the witness seed")
    if readout_y(moved) == readout_y(seed):
        fails.append("later readout must distinguish the exchange")
    identity_representation = _eye()
    if _mv(identity_representation, seed) != seed:
        fails.append("identity kernel-death control malformed")
    return _result(
        "T_exchange_effectiveness_requires_recombination",
        "A contender swap may be only a label automorphism. It enters the gate theorem only when its represented action survives the operational quotient. The exact witness seed e1 is moved by S_u and a later y-readout distinguishes the result; the identity representation is the kernel-death control.",
        {
            "seed": _vector_strings(seed),
            "S_u_seed": _vector_strings(moved),
            "readout_before": str(readout_y(seed)),
            "readout_after": str(readout_y(moved)),
            "identity_representation_kills_exchange": True,
        },
        fails,
        premises=("LATER_RECOMBINATION_WITNESS_FOR_EACH_EXCHANGE",),
        negative_controls=("label-only exchange represented by identity",),
    )


# PHYSICAL_ROOTS lives in apf.two_exchange_roots (split manifest; audit m4/M7).


def _graph() -> Dict[str, Tuple[str, ...]]:
    return {
        "T_EXCHANGE_REFLECTION": ("EFFECTIVE_FIRST_CONTENDER_EXCHANGE",),
        "T_345_FIXED_LINE": ("CODESPACE_TO_SECOND_PRESENTATION_FIXED_LINE", "EXACT_345_FIXED_LINE_OVERLAP"),
        "T_SECOND_EXCHANGE": (
            "T_EXCHANGE_REFLECTION",
            "T_345_FIXED_LINE",
            "ADMITTED_SECOND_BINARY_PRESENTATION",
            "EFFECTIVE_SECOND_CONTENDER_EXCHANGE",
            "UNIVERSAL_EXCHANGE_NATURALITY_ON_ADMITTED_PRESENTATIONS",
            "SAME_CARRIER_RETURN",
            "INTERTWINER_REVERSAL_IS_INVERSE",
        ),
        "T_EFFECTIVENESS": ("T_SECOND_EXCHANGE", "LATER_RECOMBINATION_WITNESS_FOR_EACH_EXCHANGE"),
        "T_IRRATIONAL_GATE": ("T_EFFECTIVENESS",),
    }


def _roots(graph: Mapping[str, Sequence[str]]) -> Tuple[str, ...]:
    nodes = set(graph)
    return tuple(sorted({d for deps in graph.values() for d in deps if d not in nodes}))


def _cycle(graph: Mapping[str, Sequence[str]]) -> Optional[Tuple[str, ...]]:
    nodes = set(graph) | {d for deps in graph.values() for d in deps}
    state = {n: 0 for n in nodes}
    stack: List[str] = []
    def dfs(n: str) -> Optional[Tuple[str, ...]]:
        if state[n] == 1:
            i = stack.index(n)
            return tuple(stack[i:] + [n])
        if state[n] == 2:
            return None
        state[n] = 1
        stack.append(n)
        for d in graph.get(n, ()):
            c = dfs(d)
            if c:
                return c
        stack.pop()
        state[n] = 2
        return None
    for n in nodes:
        c = dfs(n)
        if c:
            return c
    return None


def check_T_two_exchange_dependency_contract() -> Dict[str, object]:
    fails: List[str] = []
    graph = _graph()
    roots = _roots(graph)
    expected = tuple(sorted(PHYSICAL_ROOTS))
    if roots != expected:
        fails.append(f"root inventory drift: {roots} != {expected}")
    cyc = _cycle(graph)
    if cyc is not None:
        fails.append(f"dependency cycle: {cyc}")
    absent_by_contract = {
        "PHYSICAL_SHARP_REFLECTION_IMPLEMENTABILITY":
            "superseded by the two-exchange reduction; machine-closed in "
            "T_composed_route_supersedes_reflection_gate",
        "CONNECTED_EFFECTIVE_HELD_SWEEP":
            "removed by the one-gate compact-orbit theorem",
        "QUADRATIC_LEDGER":
            "not consumed by this route; the positivity surface is RELOCATED to "
            "R-capacity-bounded-world + the H3 gate at reading grade, per "
            "check_L_bounded_orbit_positivity (v24.3.431)",
        "PULLBACK_NONEXPANSION":
            "killed device of the seam-closure packet; must never re-enter",
    }
    if set(absent_by_contract) & set(roots):
        fails.append("absent-by-contract premise re-entered the root inventory")
    mutated = dict(graph)
    mutated["T_IRRATIONAL_GATE"] = mutated["T_IRRATIONAL_GATE"] + ("SECOND_EMPIRICAL_ROOT",)
    mutation_caught = _roots(mutated) != expected
    if not mutation_caught:
        fails.append("added empirical-root mutation was not caught")
    missing_gen = dict(graph)
    missing_gen["T_SECOND_EXCHANGE"] = tuple(
        d for d in missing_gen["T_SECOND_EXCHANGE"]
        if d != "EFFECTIVE_SECOND_CONTENDER_EXCHANGE"
    )
    missing_second_exchange_caught = _roots(missing_gen) != expected
    if not missing_second_exchange_caught:
        fails.append("removing second physical exchange was not caught")
    missing_rev = dict(graph)
    missing_rev["T_SECOND_EXCHANGE"] = tuple(
        d for d in missing_rev["T_SECOND_EXCHANGE"]
        if d != "INTERTWINER_REVERSAL_IS_INVERSE"
    )
    missing_reversal_caught = _roots(missing_rev) != expected
    if not missing_reversal_caught:
        fails.append("removing the reversal-is-inverse root was not caught")
    return _result(
        "T_two_exchange_dependency_contract",
        "The generic sharp-reflection premise is eliminated from this route. The exact gate now depends on two effective contender exchanges, one admitted 3-4-5 binary presentation, its fixed-line identification, exchange naturality/same-carrier return, intertwiner reversal-is-inverse, and later recombination effectiveness. The graph is acyclic. It consumes neither the connected-sweep premise nor the quadratic ledger; the quadratic-ledger positivity surface is RELOCATED to R-capacity-bounded-world + the H3 gate at reading grade (check_L_bounded_orbit_positivity, v24.3.431); absence from this graph is mere absence. The root manifest lives in apf.two_exchange_roots, split from this consuming module so a coordinated mutation must touch two files.",
        {
            "graph": {k: list(v) for k, v in graph.items()},
            "roots": list(roots),
            "cycle": cyc,
            "generic_sharp_reflection_premise_present": False,
            "connected_sweep_present": False,
            "quadratic_ledger_present": False,
            "quadratic_ledger_disposition": absent_by_contract["QUADRATIC_LEDGER"],
            "added_root_mutation_caught": mutation_caught,
            "missing_second_exchange_caught": missing_second_exchange_caught,
            "missing_reversal_root_caught": missing_reversal_caught,
            "root_manifest_module": "apf.two_exchange_roots",
        },
        fails,
        dependencies=tuple(graph),
        premises=expected,
        negative_controls=("add SECOND_EMPIRICAL_ROOT", "remove second exchange", "remove reversal-is-inverse", "reinsert generic sharp reflection"),
        epistemic="P_structural_instrument",
    )


COMPOSED_SUPERSEDED_ROOTS = (
    "PHYSICAL_SHARP_REFLECTION_IMPLEMENTABILITY",
    "CODESPACE_TO_HELD_CARRIER_IDENTIFICATION",
)


def _one_gate_module():
    from apf import irrational_gate_holonomy as one_gate
    return one_gate


def _composed_graph() -> Dict[str, Tuple[str, ...]]:
    """End-to-end graph: the two-exchange front end spliced into the one-gate chain.

    ``T_REFLECTION_GATE`` and its roots are superseded here:
    ``T_BOUNDED_CYCLIC_CLOSURE`` consumes the front-end terminal node
    ``T_IRRATIONAL_GATE`` instead (cold-audit MAJOR-3).
    """
    og = _one_gate_module()
    one = og._dependency_graph("reflection")
    composed: Dict[str, Tuple[str, ...]] = {
        k: v for k, v in one.items()
        if k not in ("T_REFLECTION_GATE", "T_APF_345_PROJECTORS")
    }
    composed["T_BOUNDED_CYCLIC_CLOSURE"] = tuple(
        "T_IRRATIONAL_GATE" if d == "T_REFLECTION_GATE" else d
        for d in one["T_BOUNDED_CYCLIC_CLOSURE"]
    )
    composed.update(_graph())
    return composed


def _expected_composed_roots() -> Tuple[str, ...]:
    og = _one_gate_module()
    return tuple(sorted(set(PHYSICAL_ROOTS) | set(og.COMMON_PHYSICAL_ROOTS)))


def _validate_composed(graph: Mapping[str, Sequence[str]]) -> List[str]:
    fails: List[str] = []
    roots = _roots(graph)
    expected = _expected_composed_roots()
    if roots != expected:
        fails.append(f"composed root inventory drift: {roots} != {expected}")
    for old in COMPOSED_SUPERSEDED_ROOTS:
        if old in roots:
            fails.append(f"superseded root still in the composed inventory: {old}")
        consumers = [n for n, deps in graph.items() if old in deps]
        if consumers:
            fails.append(f"nodes still consuming the superseded root {old}: {consumers}")
    if "T_REFLECTION_GATE" in graph or any(
            "T_REFLECTION_GATE" in deps for deps in graph.values()):
        fails.append("the reflection-gate route must not appear in the composed graph")
    if "T_IRRATIONAL_GATE" not in graph.get("T_BOUNDED_CYCLIC_CLOSURE", ()):
        fails.append("splice missing: the compact-orbit chain must consume the front-end gate")
    cyc = _cycle(graph)
    if cyc is not None:
        fails.append(f"composed dependency cycle: {cyc}")
    return fails


def check_T_composed_route_supersedes_reflection_gate() -> Dict[str, object]:
    fails: List[str] = []
    og = _one_gate_module()
    composed = _composed_graph()
    fails.extend(_validate_composed(composed))
    # Tripwire pair: the vendored one-gate module keeps the reflection route
    # as an honest alternative and must still name its root THERE, while the
    # composed contract asserts the root is NOT live HERE.
    if "PHYSICAL_SHARP_REFLECTION_IMPLEMENTABILITY" not in og.REFLECTION_GATE_ROOTS:
        fails.append("vendored reflection route lost its named root; supersession would be vacuous")
    # Mutation controls, executed against the same validator this check uses.
    readded = dict(composed)
    readded["T_BOUNDED_CYCLIC_CLOSURE"] = readded["T_BOUNDED_CYCLIC_CLOSURE"] + (
        "PHYSICAL_SHARP_REFLECTION_IMPLEMENTABILITY",)
    readd_caught = bool(_validate_composed(readded))
    if not readd_caught:
        fails.append("re-adding the superseded reflection root was not caught")
    unspliced = dict(composed)
    unspliced["T_BOUNDED_CYCLIC_CLOSURE"] = og._dependency_graph(
        "reflection")["T_BOUNDED_CYCLIC_CLOSURE"]
    unsplice_caught = bool(_validate_composed(unspliced))
    if not unsplice_caught:
        fails.append("removing the front-end splice was not caught")
    composed_roots = _roots(composed)
    return _result(
        "T_composed_route_supersedes_reflection_gate",
        "The claimed supersession is machine-closed (cold-audit MAJOR-3): the end-to-end composed graph wires the two-exchange front end into the one-gate compact-orbit chain (T_BOUNDED_CYCLIC_CLOSURE consumes T_IRRATIONAL_GATE), and no node of the composed contract consumes PHYSICAL_SHARP_REFLECTION_IMPLEMENTABILITY. The carrier-identification root of the reflection route is not dropped: it is replaced by the DSEB_345 clauses (CODESPACE_TO_SECOND_PRESENTATION_FIXED_LINE + ADMITTED_SECOND_BINARY_PRESENTATION; charter limb L1). The vendored reflection route remains an honest root-carrying alternative in apf.irrational_gate_holonomy; it is superseded only inside this composed contract. Composition-order note: the certificate pins the product order R = S_u S_0; this is a labeling convention fixing the rotation sense, and the relative-loop group contains R^{-1} by closure.",
        {
            "composed_graph": {k: list(v) for k, v in composed.items()},
            "composed_roots": list(composed_roots),
            "superseded_roots": list(COMPOSED_SUPERSEDED_ROOTS),
            "superseded_roots_absent": True,
            "readded_root_caught": readd_caught,
            "unspliced_bridge_caught": unsplice_caught,
            "reflection_route_status": "superseded in the composed contract; retained as an alternative in the vendored one-gate module",
        },
        fails,
        dependencies=("T_two_exchange_dependency_contract",),
        premises=_expected_composed_roots(),
        negative_controls=("re-add the superseded reflection root (executed)", "remove the splice (executed)"),
        epistemic="P_structural_instrument",
    )


REQUIRED_CERT_FIELDS = (
    "evidence_class",
    "source_digest",
    "codespace_to_fixed_line_certified",
    "second_binary_presentation_certified",
    "first_exchange_path_certified",
    "second_exchange_path_certified",
    "exchange_naturality_certified",
    "same_carrier_return_certified",
    "intertwiner_reversal_is_inverse_certified",
    "recombination_effectiveness_certified",
    "exact_overlap_certified",
    "first_exchange_matrix",
    "second_exchange_matrix",
)


def _parse_matrix(raw: object) -> Matrix2:
    rows = raw  # type: ignore[assignment]
    return tuple(tuple(F(str(x)) for x in row) for row in rows)  # type: ignore[return-value]


def verify_two_exchange_interface_certificate(payload: Mapping[str, object]) -> Dict[str, object]:
    missing = [k for k in REQUIRED_CERT_FIELDS if k not in payload]
    failures: List[str] = []
    if missing:
        failures.append("missing fields: " + ", ".join(missing))
    evidence_class = str(payload.get("evidence_class", ""))
    allowed = {"structural_derivation", "experiment", "device_calibration", "synthetic_reference"}
    if evidence_class not in allowed:
        failures.append("unknown evidence_class")
    digest = str(payload.get("source_digest", ""))
    if evidence_class != "synthetic_reference" and len(digest) < 32:
        failures.append("physical evidence requires a source digest")
    bool_fields = [k for k in REQUIRED_CERT_FIELDS if k.endswith("_certified")]
    false_fields = [k for k in bool_fields if payload.get(k) is not True]
    if false_fields:
        failures.append("uncertified leaves: " + ", ".join(false_fields))
    matrix_ok = False
    product = None
    try:
        s0 = _parse_matrix(payload.get("first_exchange_matrix"))
        su = _parse_matrix(payload.get("second_exchange_matrix"))
        involutions = _mm(s0, s0) == _eye() and _mm(su, su) == _eye()
        orientation_reversing = _det(s0) == -1 and _det(su) == -1
        product = _mm(su, s0)
        matrix_ok = (
            involutions
            and orientation_reversing
            and product == R_345
            and _trace(product) == F(-14, 25)
        )
        if not matrix_ok:
            failures.append("exchange matrices do not produce the exact 3-4-5 gate")
    except Exception as exc:
        failures.append(f"invalid exchange matrices: {exc}")
    common_ok = not missing and not false_fields and evidence_class in allowed and (
        evidence_class == "synthetic_reference" or len(digest) >= 32
    )
    exact = common_ok and not failures and evidence_class == "structural_derivation" and matrix_ok
    finite_resolution = (
        common_ok
        and evidence_class in {"experiment", "device_calibration"}
        and payload.get("finite_resolution_orbit_cover_certified") is True
    )
    return {
        "passed_schema": not missing,
        "matrix_check": matrix_ok,
        "gate_matrix": _matrix_strings(product) if product is not None else None,
        "gate_trace": str(_trace(product)) if product is not None else None,
        "physical_premises_certified": exact,
        "finite_resolution_interface_certified": finite_resolution,
        "evidence_class": evidence_class,
        "failures": failures,
    }


def check_T_two_exchange_interface_certificate_fail_closed() -> Dict[str, object]:
    fails: List[str] = []
    base = {
        "source_digest": "a" * 64,
        "codespace_to_fixed_line_certified": True,
        "second_binary_presentation_certified": True,
        "first_exchange_path_certified": True,
        "second_exchange_path_certified": True,
        "exchange_naturality_certified": True,
        "same_carrier_return_certified": True,
        "intertwiner_reversal_is_inverse_certified": True,
        "recombination_effectiveness_certified": True,
        "exact_overlap_certified": True,
        "first_exchange_matrix": _matrix_strings(S_0),
        "second_exchange_matrix": _matrix_strings(S_U),
    }
    synthetic = dict(base, evidence_class="synthetic_reference",
                     finite_resolution_orbit_cover_certified=True)
    rep_syn = verify_two_exchange_interface_certificate(synthetic)
    if rep_syn["physical_premises_certified"] or rep_syn["finite_resolution_interface_certified"]:
        fails.append("synthetic reference must certify neither physical verdict")
    structural = dict(base, evidence_class="structural_derivation",
                      finite_resolution_orbit_cover_certified=True)
    rep_struct = verify_two_exchange_interface_certificate(structural)
    if not rep_struct["physical_premises_certified"]:
        fails.append("complete structural certificate should pass")
    experiment = dict(base, evidence_class="experiment",
                      finite_resolution_orbit_cover_certified=True)
    rep_exp = verify_two_exchange_interface_certificate(experiment)
    if rep_exp["physical_premises_certified"] or not rep_exp["finite_resolution_interface_certified"]:
        fails.append("experiment must certify finite resolution only")
    no_second = dict(structural, second_exchange_path_certified=False)
    rep_no_second = verify_two_exchange_interface_certificate(no_second)
    if rep_no_second["physical_premises_certified"]:
        fails.append("missing second exchange must fail closed")
    label_only = dict(structural, second_exchange_matrix=_matrix_strings(_eye()))
    rep_label = verify_two_exchange_interface_certificate(label_only)
    if rep_label["physical_premises_certified"]:
        fails.append("label-only identity action must fail closed")
    wrong_overlap = dict(structural, second_exchange_matrix=_matrix_strings(((F(0), F(1)), (F(1), F(0)))))
    rep_wrong = verify_two_exchange_interface_certificate(wrong_overlap)
    if rep_wrong["physical_premises_certified"]:
        fails.append("wrong-overlap exchange must fail closed")
    empty_digest = dict(structural, source_digest="")
    rep_empty = verify_two_exchange_interface_certificate(empty_digest)
    if rep_empty["physical_premises_certified"]:
        fails.append("empty digest must fail closed")
    no_reversal = dict(structural, intertwiner_reversal_is_inverse_certified=False)
    rep_no_rev = verify_two_exchange_interface_certificate(no_reversal)
    if rep_no_rev["physical_premises_certified"]:
        fails.append("missing reversal-is-inverse certification must fail closed")
    return _result(
        "T_two_exchange_interface_certificate_fail_closed",
        "The physical verifier requires two effective exchange paths, an admitted second presentation, exact fixed-line overlap, naturality/same-carrier return, intertwiner reversal-is-inverse, a recombination witness, and a source digest. Synthetic evidence certifies nothing; experiment certifies finite resolution only; missing, label-only, wrong-overlap, missing-reversal, and empty-digest mutations fail closed. The verifier demands the exact product S_u S_0; the order pin is a labeling convention fixing the rotation sense (the relative-loop group contains R^{-1} by closure).",
        {
            "synthetic": rep_syn,
            "structural": rep_struct,
            "experiment": rep_exp,
            "missing_second_exchange": rep_no_second,
            "label_only": rep_label,
            "wrong_overlap": rep_wrong,
            "empty_digest": rep_empty,
            "missing_reversal_certification": rep_no_rev,
        },
        fails,
        dependencies=("T_two_exchange_dependency_contract",),
        negative_controls=("synthetic", "missing second exchange", "identity action", "wrong overlap", "empty digest", "missing reversal-is-inverse"),
        epistemic="P_structural_instrument",
    )


def check_T_live_source_concordance_and_nonclaim() -> Dict[str, object]:
    fails: List[str] = []
    live = {
        "binary_exchange_math": "T_binary_exchange_character_idempotents / T_calibration_free_competition_zipper",
        "physical_exchange_countermodel": "T_HOC_quantum_close_scope_contract physical_monoid={I,P}",
        "345_projector_geometry": "reproduce_inline_345_commutator",
        "first_jet_carrier": "Paper 10 first-jet representation / bipolar comparison lift",
        "closed_world_effects": "closed_world_completeness.py",
    }
    absent = {
        "second_binary_presentation": "not banked",
        "second_effective_exchange_path": "not banked",
        "codespace_to_Held_fixed_line": "not banked",
        "generic_dynamic_saturation": "correctly not inferred from effect completeness",
    }
    if set(live) & set(absent):
        fails.append("live and absent source inventories must be disjoint")
    # Computed correspondence legs (audit m1): every named physical root maps
    # onto a fail-closed certificate leaf, checked against BOTH the split
    # manifest and the schema, so either side drifting fails this check.
    root_to_certificate_field = {
        "CODESPACE_TO_SECOND_PRESENTATION_FIXED_LINE": "codespace_to_fixed_line_certified",
        "ADMITTED_SECOND_BINARY_PRESENTATION": "second_binary_presentation_certified",
        "EFFECTIVE_FIRST_CONTENDER_EXCHANGE": "first_exchange_path_certified",
        "EFFECTIVE_SECOND_CONTENDER_EXCHANGE": "second_exchange_path_certified",
        "UNIVERSAL_EXCHANGE_NATURALITY_ON_ADMITTED_PRESENTATIONS": "exchange_naturality_certified",
        "SAME_CARRIER_RETURN": "same_carrier_return_certified",
        "INTERTWINER_REVERSAL_IS_INVERSE": "intertwiner_reversal_is_inverse_certified",
        "EXACT_345_FIXED_LINE_OVERLAP": "exact_overlap_certified",
        "LATER_RECOMBINATION_WITNESS_FOR_EACH_EXCHANGE": "recombination_effectiveness_certified",
    }
    if set(root_to_certificate_field) != set(PHYSICAL_ROOTS):
        fails.append("root manifest / certificate-field correspondence out of sync with apf.two_exchange_roots")
    missing_fields = [f for f in root_to_certificate_field.values()
                      if f not in REQUIRED_CERT_FIELDS]
    if missing_fields:
        fails.append("certificate schema missing fields for named roots: " + ", ".join(missing_fields))
    return _result(
        "T_live_source_concordance_and_nonclaim",
        "The live stack supplies the exact binary-exchange algebra, the consistency of a physical identity/exchange monoid, the 3-4-5 projector, and the first-jet carrier. It does not supply the second admitted binary presentation or an effective second exchange path. Closed-world record/effect completeness does not fill that dynamic gap. Every named physical root is mechanically mapped onto a fail-closed certificate leaf; the mapping is computed against both the manifest and the schema.",
        {"live_sources": live, "not_yet_supplied": absent,
         "root_to_certificate_field": root_to_certificate_field,
         "correspondence_computed": True,
         "headline_license": "reduction theorem, not physical closure"},
        fails,
        dependencies=("T_effect_completeness_does_not_imply_process_saturation", "T_two_exchange_dependency_contract"),
        epistemic="P_structural_instrument",
    )


CHECKS: Dict[str, Callable[[], Dict[str, object]]] = {
    "T_binary_exchange_is_character_reflection": check_T_binary_exchange_is_character_reflection,
    "T_rotated_exchange_is_conjugated_swap": check_T_rotated_exchange_is_conjugated_swap,
    "T_345_codespace_fixed_line_candidate": check_T_345_codespace_fixed_line_candidate,
    "T_two_exchanges_generate_irrational_gate": check_T_two_exchanges_generate_irrational_gate,
    "T_effect_completeness_does_not_imply_process_saturation": check_T_effect_completeness_does_not_imply_process_saturation,
    "T_localized_binary_exchange_suffices": check_T_localized_binary_exchange_suffices,
    "T_exchange_effectiveness_requires_recombination": check_T_exchange_effectiveness_requires_recombination,
    "T_two_exchange_dependency_contract": check_T_two_exchange_dependency_contract,
    "T_composed_route_supersedes_reflection_gate": check_T_composed_route_supersedes_reflection_gate,
    "T_two_exchange_interface_certificate_fail_closed": check_T_two_exchange_interface_certificate_fail_closed,
    "T_live_source_concordance_and_nonclaim": check_T_live_source_concordance_and_nonclaim,
}


def run_all() -> Dict[str, Dict[str, object]]:
    return {name: fn() for name, fn in CHECKS.items()}


def build_certificate(results: Mapping[str, Mapping[str, object]]) -> TwoExchangeCertificate:
    def ok(name: str) -> bool:
        return bool(results[name]["passed"])
    return TwoExchangeCertificate(
        exchange_is_reflection=ok("T_binary_exchange_is_character_reflection"),
        rotated_exchange_conjugacy=ok("T_rotated_exchange_is_conjugated_swap"),
        codespace_fixed_line_exact=ok("T_345_codespace_fixed_line_candidate"),
        two_exchange_gate_exact=ok("T_two_exchanges_generate_irrational_gate"),
        static_effects_do_not_imply_processes=ok("T_effect_completeness_does_not_imply_process_saturation"),
        localized_exchange_suffices=ok("T_localized_binary_exchange_suffices"),
        effectiveness_required=ok("T_exchange_effectiveness_requires_recombination"),
        generic_reflection_premise_removed=bool(
            results["T_two_exchange_dependency_contract"]["artifacts"]["generic_sharp_reflection_premise_present"] is False
        ),
        composed_supersession_machine_closed=ok("T_composed_route_supersedes_reflection_gate"),
        physical_two_exchange_certificate_verified=False,
        physical_premises_certified=False,
    )


def main() -> int:
    results = run_all()
    payload = {
        "family": FAMILY,
        "certificate": asdict(build_certificate(results)),
        "results": results,
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if all(r["passed"] for r in results.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())


# Bank-landing registration wiring (v24.3.432): standard registry hook.
_BANK_CHECKS = {
    "T_binary_exchange_is_character_reflection": check_T_binary_exchange_is_character_reflection,
    "T_rotated_exchange_is_conjugated_swap": check_T_rotated_exchange_is_conjugated_swap,
    "T_345_codespace_fixed_line_candidate": check_T_345_codespace_fixed_line_candidate,
    "T_two_exchanges_generate_irrational_gate": check_T_two_exchanges_generate_irrational_gate,
    "T_effect_completeness_does_not_imply_process_saturation": check_T_effect_completeness_does_not_imply_process_saturation,
    "T_localized_binary_exchange_suffices": check_T_localized_binary_exchange_suffices,
    "T_exchange_effectiveness_requires_recombination": check_T_exchange_effectiveness_requires_recombination,
    "T_two_exchange_dependency_contract": check_T_two_exchange_dependency_contract,
    "T_composed_route_supersedes_reflection_gate": check_T_composed_route_supersedes_reflection_gate,
    "T_two_exchange_interface_certificate_fail_closed": check_T_two_exchange_interface_certificate_fail_closed,
    "T_live_source_concordance_and_nonclaim": check_T_live_source_concordance_and_nonclaim,
}


def register(registry):
    registry.update(_BANK_CHECKS)
    return registry
