"""Exact finite witnesses for the HFC-to-DSEB_345 reduction.

The module proves a narrower and stronger result than the earlier two-exchange
packet.  The live 3-4-5 active plane need not be identified with Paper 10's
value/tangent first-jet plane.  Under Held Fair Commoning (HFC) and the existing
finite compatible-realization leaves, it is instead a common/defect *character
carrier*.  The conservative dilation of fair commoning then supplies the exact
second binary presentation and its exchange.  The two exchanges generate an
exact gate R, and the local square-minus-one operator is recovered algebraically
from R itself:

    J = (25 R + 7 I) / 24,      J^2 = -I.

No connected sweep, physical quarter-turn limit, quadratic ledger, or generic
"sharp effect => reflection process" rule is consumed.  The module certifies
finite mathematics and a fail-closed certificate schema.  It does not adopt or
empirically certify HFC or the other physical leaves.

Provenance (fortification 2026-07-20, cold-audit MAJOR-4): the
conservative-dilation lemma and the HFC-to-HOC reduction used here are NEW
constructions of this packet; neither is a pre-existing APF result.  The
actual banked neighbors are ``continuation_tesseract_math`` (the
exchange-natural competition zipper: check_T_calibration_free_competition_zipper,
check_T_quantum_zipper_root_of_exchange) and ``continuation_tesseract_bridge``
(the eight-leg HOC_PACKAGE, including ``affine_cargo_naturality``).  The 2x2
zipper F_345 below is a divergent re-implementation of that banked machinery:
the banked module checks the exchange-naturality leg in-code, this packet's
first cut dropped it, and the fortified packet consumes it instead as the
named physical leaf EXCHANGE_CARGO_NATURALITY.

Reduction typing (cold-audit statement-level finding): the DSEB_345
dissolution is a RE-TYPING of the physical inventory, not a shrink.  The
two-exchange packet's nine roots become thirteen typed leaves plus the new
HFC availability gate, itself proven underivable from the minimal base by
this module's own countermodel.  What genuinely shrinks is the mathematical
scaffolding: the connected sweep, the physical quarter-turn limit, and the
quadratic ledger exit the local-J antecedent.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
from typing import Callable, Dict, Iterable, List, Mapping, MutableMapping, Optional, Sequence, Tuple

FAMILY = "quantum.hfc_345_algebraic_orientation"
Matrix2 = Tuple[Tuple[F, F], Tuple[F, F]]
Matrix3 = Tuple[Tuple[F, F, F], Tuple[F, F, F], Tuple[F, F, F]]
Vector2 = Tuple[F, F]
Vector3 = Tuple[F, F, F]

from apf._hfc_345_contracts import CENTRAL_J_REQUIRED_GATES

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
LEAF_MANIFEST_PATH = PACKAGE_ROOT / "DATA" / "physical_leaf_manifest.json"


@dataclass(frozen=True)
class HFC345Certificate:
    neutral_spectator_split: bool
    character_carrier_type_safe: bool
    conservative_dilation_exact: bool
    dseb_345_discharged_relative_to_hfc: bool
    two_exchange_gate_exact: bool
    algebraic_J_exact: bool
    optional_dense_circle_corollary: bool
    effectiveness_from_complete_defect: bool
    hfc_independence_countermodel: bool
    parallel_no_cycle: bool
    central_j_gate_contract: bool
    physical_interface_certificate_verified: bool
    physical_premises_certified: bool = False


def _result(
    name: str,
    key_result: str,
    artifacts: Mapping[str, object],
    fails: Sequence[str],
    *,
    dependencies: Sequence[str] = (),
    premises: Sequence[str] = (),
    negative_controls: Sequence[str] = (),
    epistemic: str = "P_math",
) -> Dict[str, object]:
    passed = not fails
    return {
        "name": name,
        "family": FAMILY,
        "tier": 4,
        "epistemic": epistemic,
        "status": "PASS" if passed else "FAIL",
        "passed": passed,
        "scope": "finite exact mathematics / fail-closed physical-leaf reduction",
        "physical_premises_certified": False,
        "key_result": key_result,
        "dependencies": list(dependencies),
        "premises": list(premises),
        "negative_controls": list(negative_controls),
        "artifacts": dict(artifacts),
        "fail_reasons": list(fails),
    }


# ---------------------------------------------------------------------------
# Exact linear algebra
# ---------------------------------------------------------------------------


def _eye2() -> Matrix2:
    return ((F(1), F(0)), (F(0), F(1)))


def _zero2() -> Matrix2:
    return ((F(0), F(0)), (F(0), F(0)))


def _neg2(a: Matrix2) -> Matrix2:
    return tuple(tuple(-a[i][j] for j in range(2)) for i in range(2))  # type: ignore[return-value]


def _mm2(a: Matrix2, b: Matrix2) -> Matrix2:
    return tuple(
        tuple(sum(a[i][k] * b[k][j] for k in range(2)) for j in range(2))
        for i in range(2)
    )  # type: ignore[return-value]


def _mv2(a: Matrix2, v: Vector2) -> Vector2:
    return tuple(sum(a[i][k] * v[k] for k in range(2)) for i in range(2))  # type: ignore[return-value]


def _mt2(a: Matrix2) -> Matrix2:
    return ((a[0][0], a[1][0]), (a[0][1], a[1][1]))


def _add2(a: Matrix2, b: Matrix2) -> Matrix2:
    return tuple(tuple(a[i][j] + b[i][j] for j in range(2)) for i in range(2))  # type: ignore[return-value]


def _sub2(a: Matrix2, b: Matrix2) -> Matrix2:
    return tuple(tuple(a[i][j] - b[i][j] for j in range(2)) for i in range(2))  # type: ignore[return-value]


def _scale2(s: F, a: Matrix2) -> Matrix2:
    return tuple(tuple(s * a[i][j] for j in range(2)) for i in range(2))  # type: ignore[return-value]


def _det2(a: Matrix2) -> F:
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def _trace2(a: Matrix2) -> F:
    return a[0][0] + a[1][1]


def _inv2(a: Matrix2) -> Matrix2:
    d = _det2(a)
    if d == 0:
        raise ValueError("singular 2x2 matrix")
    return ((a[1][1] / d, -a[0][1] / d), (-a[1][0] / d, a[0][0] / d))


def _pow2(a: Matrix2, n: int) -> Matrix2:
    if n < 0:
        return _pow2(_inv2(a), -n)
    out = _eye2()
    base = a
    k = n
    while k:
        if k & 1:
            out = _mm2(out, base)
        base = _mm2(base, base)
        k >>= 1
    return out


def _dot2(u: Vector2, v: Vector2) -> F:
    return u[0] * v[0] + u[1] * v[1]


def _outer2(v: Vector2) -> Matrix2:
    return ((v[0] * v[0], v[0] * v[1]), (v[1] * v[0], v[1] * v[1]))


def _mm3(a: Matrix3, b: Matrix3) -> Matrix3:
    return tuple(
        tuple(sum(a[i][k] * b[k][j] for k in range(3)) for j in range(3))
        for i in range(3)
    )  # type: ignore[return-value]


def _mv3(a: Matrix3, v: Vector3) -> Vector3:
    return tuple(sum(a[i][k] * v[k] for k in range(3)) for i in range(3))  # type: ignore[return-value]


def _matrix_strings(a: Sequence[Sequence[F]]) -> List[List[str]]:
    return [[str(x) for x in row] for row in a]


def _vector_strings(v: Sequence[F]) -> List[str]:
    return [str(x) for x in v]


def _parse_matrix2(raw: object) -> Matrix2:
    if not isinstance(raw, list) or len(raw) != 2:
        raise ValueError("matrix must have two rows")
    rows: List[Tuple[F, F]] = []
    for row in raw:
        if not isinstance(row, list) or len(row) != 2:
            raise ValueError("matrix rows must have length two")
        rows.append((F(str(row[0])), F(str(row[1]))))
    return (rows[0], rows[1])


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


# ---------------------------------------------------------------------------
# Exact witness data
# ---------------------------------------------------------------------------

P_SWAP: Matrix2 = ((F(0), F(1)), (F(1), F(0)))
S_0: Matrix2 = ((F(1), F(0)), (F(0), F(-1)))
U_345: Vector2 = (F(3, 5), F(4, 5))
V_345: Vector2 = (F(-4, 5), F(3, 5))
P_U: Matrix2 = _outer2(U_345)
S_U: Matrix2 = _sub2(_scale2(F(2), P_U), _eye2())

# Minimum complete HFC dilation with common factor embedded along u and defect
# factor embedded along v:
# F(alpha,beta) = (alpha+beta)u + (alpha-beta)v.
F_345: Matrix2 = (
    (U_345[0] + V_345[0], U_345[0] - V_345[0]),
    (U_345[1] + V_345[1], U_345[1] - V_345[1]),
)
C_345: Matrix2 = _scale2(F(5), F_345)
R_345: Matrix2 = _mm2(S_U, S_0)
J_345: Matrix2 = _scale2(F(1, 24), _add2(_scale2(F(25), R_345), _scale2(F(7), _eye2())))

PI_W_3: Matrix3 = (
    (F(9, 25), F(0), F(12, 25)),
    (F(0), F(1), F(0)),
    (F(12, 25), F(0), F(16, 25)),
)
E1_3: Matrix3 = ((F(1), F(0), F(0)), (F(0), F(0), F(0)), (F(0), F(0), F(0)))
E2_3: Matrix3 = ((F(0), F(0), F(0)), (F(0), F(1), F(0)), (F(0), F(0), F(0)))
E3_3: Matrix3 = ((F(0), F(0), F(0)), (F(0), F(0), F(0)), (F(0), F(0), F(1)))


def _active_restrict(a: Matrix3) -> Matrix2:
    """Restrict a 3x3 map to span(e1,e3), in the ordered basis (e1,e3)."""
    return ((a[0][0], a[0][2]), (a[2][0], a[2][2]))


# ---------------------------------------------------------------------------
# Theorem checks
# ---------------------------------------------------------------------------


def check_T_345_neutral_spectator_restriction() -> Dict[str, object]:
    fails: List[str] = []
    e2: Vector3 = (F(0), F(1), F(0))
    e1: Vector3 = (F(1), F(0), F(0))
    e3: Vector3 = (F(0), F(0), F(1))
    active = _active_restrict(PI_W_3)
    if _mv3(PI_W_3, e2) != e2:
        fails.append("e2 must be fixed by the live defender")
    if _mv3(PI_W_3, e1)[1] != 0 or _mv3(PI_W_3, e3)[1] != 0:
        fails.append("span(e1,e3) must be invariant")
    if active != P_U:
        fails.append("active restriction must equal u u^T")
    if _mm2(active, active) != active:
        fails.append("active restriction must be idempotent")
    if _mv2(active, U_345) != U_345:
        fails.append("u must be the active range line")
    if _mv2(active, V_345) != (F(0), F(0)):
        fails.append("v must be the active kernel line")
    return _result(
        "T_345_neutral_spectator_restriction",
        "The live 3-4-5 defender splits exactly as an invariant e2 summand plus an active two-dimensional carrier. On the neutral e2 completion, the active restriction is u u^T with range u=(3/5,4/5) and kernel v=(-4/5,3/5). The e2 direction is fixed, not globally null; using the active plane therefore requires an explicit neutral-spectator completion.",
        {
            "pi_W": _matrix_strings(PI_W_3),
            "active_restriction": _matrix_strings(active),
            "range_u": _vector_strings(U_345),
            "kernel_v": _vector_strings(V_345),
            "e2_fixed": True,
            "e2_globally_null": False,
            "neutral_completion_required": True,
        },
        fails,
        premises=("EXACT_345_DEFENDER_GEOMETRY", "NEUTRAL_E2_COMPLETION"),
        negative_controls=("calling e2 quotient-null", "using the active plane without a neutral completion"),
    )


def check_T_character_carrier_not_first_jet() -> Dict[str, object]:
    fails: List[str] = []
    # Both carriers have dimension two, but their axis roles are not the same.
    character_roles = ("common_present", "defect_present")
    first_jet_roles = ("signed_value", "continuation_direction")
    if set(character_roles) & set(first_jet_roles):
        fails.append("typed role vocabularies must be disjoint")
    if character_roles == first_jet_roles:
        fails.append("dimension equality must not collapse the types")
    # The first-order lift of the character plane is rank four.  Fortification
    # (cold-audit minors 5 and 7): the rank is now COMPUTED from an explicit
    # jet matrix, not asserted as 2*len(roles).  Four exact curves
    # gamma(t) = p + t q in the (c,d) character plane have first-order jets
    # (c(0), d(0), c'(0), d'(0)); their jet matrix must have exact rank four,
    # while the zero-velocity control curves span only rank two.
    def _rank(rows: List[List[F]]) -> int:
        m = [row[:] for row in rows]
        rank = 0
        n_cols = len(m[0]) if m else 0
        for col in range(n_cols):
            pivot = next((r for r in range(rank, len(m)) if m[r][col] != 0), None)
            if pivot is None:
                continue
            m[rank], m[pivot] = m[pivot], m[rank]
            pv = m[rank][col]
            m[rank] = [x / pv for x in m[rank]]
            for r in range(len(m)):
                if r != rank and m[r][col] != 0:
                    factor = m[r][col]
                    m[r] = [a - factor * b for a, b in zip(m[r], m[rank])]
            rank += 1
        return rank

    def _jet(p: Vector2, q: Vector2) -> List[F]:
        return [p[0], p[1], q[0], q[1]]

    jet_matrix = [
        _jet((F(1), F(0)), (F(0), F(0))),
        _jet((F(0), F(1)), (F(0), F(0))),
        _jet((F(0), F(0)), (F(1), F(0))),
        _jet((F(0), F(0)), (F(0), F(1))),
    ]
    first_order_character_rank = _rank(jet_matrix)
    if first_order_character_rank != 4:
        fails.append("character-plane first-order jet matrix must have exact rank four")
    zero_velocity_rank = _rank([
        _jet((F(1), F(0)), (F(0), F(0))),
        _jet((F(0), F(1)), (F(0), F(0))),
        _jet((F(1), F(1)), (F(0), F(0))),
        _jet((F(2), F(-3)), (F(0), F(0))),
    ])
    if zero_velocity_rank != 2:
        fails.append("zero-velocity control curves must span exactly rank two")
    return _result(
        "T_character_carrier_not_first_jet",
        "The 3-4-5 active plane is used as the present common/defect character carrier supplied by conservative Held dilation. It is not identified with Paper 10's signed-value/continuation-direction first-jet plane merely because both are real two-planes. The first-order lift of the character carrier is rank four, computed exactly from the jet matrix of four curves (the zero-velocity control spans rank two). The rank-four vocabulary echoes the banked continuation_tesseract_math carrier; the link is nominal and the computation is packet-local. The role-vocabulary legs are declaratory fences, billed as such.",
        {
            "active_carrier_roles": list(character_roles),
            "paper10_first_jet_roles": list(first_jet_roles),
            "role_vocabulary_legs_class": "declaratory_fence_not_test",
            "active_rank": 2,
            "first_jet_rank": 2,
            "first_order_character_lift_rank": first_order_character_rank,
            "first_order_lift_rank_computed_from_jet_matrix": True,
            "zero_velocity_control_rank": zero_velocity_rank,
            "rank_four_link_to_banked_tesseract": "nominal vocabulary link only; the rank is computed in-packet, the banked module is continuation_tesseract_math",
            "canonical_identification_claimed": False,
            "retired_claim": "ACTIVE_345_PLANE_IS_PAPER10_FIRST_JET",
        },
        fails,
        dependencies=("T_345_neutral_spectator_restriction",),
        negative_controls=("dimension-only type identification", "clock-ruler or spacetime tangent conflation"),
        epistemic="P_structural_instrument",
    )


def check_T_hfc_345_conservative_dilation() -> Dict[str, object]:
    fails: List[str] = []
    a = (F_345[0][0], F_345[1][0])
    b = (F_345[0][1], F_345[1][1])
    common = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
    defect = ((a[0] - b[0]) / 2, (a[1] - b[1]) / 2)
    if common != U_345:
        fails.append("port average must be u")
    if defect != V_345:
        fails.append("port half-difference must be v")
    if _det2(F_345) == 0:
        fails.append("minimum complete dilation must be invertible")
    visible_commoning = _mm2(P_U, F_345)
    retained_defect = _mm2(_sub2(_eye2(), P_U), F_345)
    expected_visible = ((U_345[0], U_345[0]), (U_345[1], U_345[1]))
    expected_defect = ((V_345[0], -V_345[0]), (V_345[1], -V_345[1]))
    if visible_commoning != expected_visible:
        fails.append("pi_W|act must map both candidate ports to the same common vector u")
    if retained_defect != expected_defect:
        fails.append("the complementary active factor must retain v and -v")
    # Direct formula checks on exact sample inputs.
    for alpha, beta in ((F(1), F(0)), (F(0), F(1)), (F(2), F(-3)), (F(1, 7), F(5, 9))):
        lhs = _mv2(F_345, (alpha, beta))
        rhs = (
            (alpha + beta) * U_345[0] + (alpha - beta) * V_345[0],
            (alpha + beta) * U_345[1] + (alpha - beta) * V_345[1],
        )
        if lhs != rhs:
            fails.append(f"dilation formula failed at {(alpha, beta)}")
    return _result(
        "T_hfc_345_conservative_dilation",
        "Once the live candidate ports a=u+v and b=u-v are certified as one equal unresolved Held competition and pi_W|act is certified as their contender-blind Held commoning, Paper 10 completeness retains the consequential relative kernel. The minimum scalar dilation embeds the common factor on the live range line u and the defect factor on the live kernel line v. The exact map F_345(alpha,beta)=(alpha+beta)u+(alpha-beta)v has columns u+v and u-v, hence 5F_345=[[-1,7],[7,1]]. It is an invertible Held zipper, not a coordinate-only relabeling.",
        {
            "F_345": _matrix_strings(F_345),
            "scaled_C_345": _matrix_strings(C_345),
            "port_a": _vector_strings(a),
            "port_b": _vector_strings(b),
            "common_axis": _vector_strings(common),
            "defect_axis": _vector_strings(defect),
            "det_F_345": str(_det2(F_345)),
            "visible_commoning_Pu_F345": _matrix_strings(visible_commoning),
            "retained_defect_(I-Pu)_F345": _matrix_strings(retained_defect),
            "both_ports_have_same_visible_output_u": True,
            "equal_calibration_required": False,
        },
        fails,
        dependencies=("T_345_neutral_spectator_restriction", "T_character_carrier_not_first_jet"),
        premises=(
            "LIVE_345_HELD_FAIR_COMMONING",
            "COMPLETE_HELD_PROFILE",
            "A2_NO_WASTE_MINIMUM",
            "FINITE_COMPATIBLE_JOINT_REALIZATION",
            "FACTOR_ISOLATION_NEUTRAL_COMPLETION",
            "SAME_TYPE_RETURN",
        ),
        negative_controls=("destructive classical commoning", "formal linear combination with no Held total realization"),
        epistemic="P_structural",
    )


def check_T_DSEB_345_discharged_from_HFC() -> Dict[str, object]:
    fails: List[str] = []
    # Fortification (cold-audit MAJOR-2): the transport S_u = F_345 P F_345^{-1}
    # consumes two leaves the pre-fortification manifest had dropped.  The
    # arithmetic shadows are checked here; the physical claims stay leaves.
    finv = _inv2(F_345)
    if _mm2(F_345, finv) != _eye2() or _mm2(finv, F_345) != _eye2():
        fails.append(
            "F_345^{-1} must be an exact two-sided inverse "
            "(arithmetic shadow of ZIPPER_REVERSAL_IS_INVERSE)"
        )
    if _mm2(F_345, P_SWAP) != _mm2(S_U, F_345):
        fails.append(
            "zipper must intertwine the exchanges, F P = S_u F "
            "(arithmetic shadow of EXCHANGE_CARGO_NATURALITY)"
        )
    transported = _mm2(_mm2(F_345, P_SWAP), _inv2(F_345))
    if transported != S_U:
        fails.append("HFC transport of source exchange must equal S_u")
    if _mv2(transported, U_345) != U_345:
        fails.append("S_u must fix the HFC common factor")
    if _mv2(transported, V_345) != (-V_345[0], -V_345[1]):
        fails.append("S_u must reverse the retained defect factor")
    if _mm2(transported, transported) != _eye2():
        fails.append("transported exchange must be involutive")
    return _result(
        "T_DSEB_345_discharged_from_HFC",
        "DSEB_345 is not an additional root once a live-interface HFC certificate and the conservative Held-dilation package are present. The physical HFC zipper F_345 and its record-free return transport the source contender exchange to S_u=F_345 P F_345^{-1}. The transport consumes ZIPPER_REVERSAL_IS_INVERSE (the reversed zipper path is represented by F_345^{-1}; reversal admission alone yields only a monoid -- the .429 H1-genre gate) and EXCHANGE_CARGO_NATURALITY (the represented action is linear on Held cargo; the banked affine_cargo_naturality leg of continuation_tesseract_bridge.HOC_PACKAGE is the fallback-route consumer). The live range/kernel factors are therefore a second effective binary Held presentation on the same character carrier. No sharp-projector-to-process rule and no first-jet identification is used. Conditional physical discharge claim, billed P_structural.",
        {
            "source_exchange": _matrix_strings(P_SWAP),
            "physical_intertwiner": _matrix_strings(F_345),
            "transported_exchange": _matrix_strings(transported),
            "target_S_u": _matrix_strings(S_U),
            "DSEB_345_independent_root": False,
            "first_jet_identification_consumed": False,
            "generic_reflection_saturation_consumed": False,
            "premise_consumption": {
                "ZIPPER_REVERSAL_IS_INVERSE": "F_345^{-1} as the represented reversed zipper path in S_u = F_345 P F_345^{-1}",
                "EXCHANGE_CARGO_NATURALITY": "linearity of the represented action; intertwining identity F P = S_u F",
                "LIVE_345_RECORD_FREE_PORT_EXCHANGE": "the physical port swap P on the admitted ports",
                "SAME_TYPE_RETURN": "same-carrier return of the transported loop",
            },
        },
        fails,
        dependencies=("T_hfc_345_conservative_dilation",),
        premises=(
            "LIVE_345_RECORD_FREE_PORT_EXCHANGE",
            "SAME_TYPE_RETURN",
            "ZIPPER_REVERSAL_IS_INVERSE",
            "EXCHANGE_CARGO_NATURALITY",
        ),
        negative_controls=("coordinate conjugacy without a physical zipper", "label swap represented trivially", "reversal admitted but represented by a non-inverse"),
        epistemic="P_structural",
    )


def check_T_two_exchange_gate_and_algebraic_J() -> Dict[str, object]:
    fails: List[str] = []
    if _mm2(S_0, S_0) != _eye2() or _mm2(S_U, S_U) != _eye2():
        fails.append("both exchanges must be involutions")
    if R_345 != ((F(-7, 25), F(-24, 25)), (F(24, 25), F(-7, 25))):
        fails.append("two-exchange product matrix incorrect")
    if _det2(R_345) != F(1) or _trace2(R_345) != F(-14, 25):
        fails.append("gate determinant/trace incorrect")
    if J_345 != ((F(0), F(-1)), (F(1), F(0))):
        fails.append("algebraic J extraction incorrect")
    if _mm2(J_345, J_345) != _neg2(_eye2()):
        fails.append("J^2 must equal -I")
    if _mm2(R_345, J_345) != _mm2(J_345, R_345):
        fails.append("J must commute with R")
    reconstructed = _add2(_scale2(F(-7, 25), _eye2()), _scale2(F(24, 25), J_345))
    if reconstructed != R_345:
        fails.append("R must equal (-7/25)I+(24/25)J")
    return _result(
        "T_two_exchange_gate_and_algebraic_J",
        "The two physical exchanges give R=S_u S_0=[[-7,-24],[24,-7]]/25. The local complex orientation is then an exact element of the real algebra generated by I and R: J=(25R+7I)/24. It satisfies J^2=-I and R=(-7/25)I+(24/25)J. A physical continuous sweep, operational limit admitting a quarter-turn, and quadratic-ledger isometry are unnecessary for the algebraic complex structure.",
        {
            "S_0": _matrix_strings(S_0),
            "S_u": _matrix_strings(S_U),
            "R": _matrix_strings(R_345),
            "det_R": str(_det2(R_345)),
            "trace_R": str(_trace2(R_345)),
            "J_formula": "(25 R + 7 I)/24",
            "J": _matrix_strings(J_345),
            "J_square": _matrix_strings(_mm2(J_345, J_345)),
            "physical_J_process_claimed": False,
            "J_in_real_generated_algebra": True,
        },
        fails,
        dependencies=("T_DSEB_345_discharged_from_HFC",),
        negative_controls=("connected sweep", "physical quarter-turn saturation", "quadratic-ledger derivation", "generic 2P-I process rule"),
    )


def check_T_optional_dense_circle_corollary() -> Dict[str, object]:
    fails: List[str] = []
    # Exact orthogonality is an auxiliary representation identity. It proves
    # boundedness; it is not installed as a physical cost ledger.
    if _mm2(_mt2(R_345), R_345) != _eye2():
        fails.append("R must be exactly orthogonal in the displayed representation")
    finite_order_hit: Optional[int] = None
    for n in range(1, 65):
        if _pow2(R_345, n) == _eye2():
            finite_order_hit = n
            break
    if finite_order_hit is not None:
        fails.append(f"unexpected finite order {finite_order_hit}")
    rational_finite_order_traces = (F(-2), F(-1), F(0), F(1), F(2))
    if _trace2(R_345) in rational_finite_order_traces:
        fails.append("nonintegral trace control failed")
    return _result(
        "T_optional_dense_circle_corollary",
        "The exact gate is also an irrational rotation. Its determinant is one, its auxiliary-coordinate orbit is bounded, and its rational trace -14/25 is not a rational algebraic integer. It therefore has infinite order. The closure of its cyclic subgroup in the displayed SO(2) representation is the full circle. This strengthens the holonomy interpretation, but it is not load-bearing for J because J is already a polynomial in R.",
        {
            "orthogonal_exact": True,
            "powers_checked_nonidentity": 64,
            "finite_order_hit": finite_order_hit,
            "rational_finite_order_trace_controls": [str(x) for x in rational_finite_order_traces],
            "trace_R": str(_trace2(R_345)),
            "circle_load_bearing_for_J": False,
        },
        fails,
        dependencies=("T_two_exchange_gate_and_algebraic_J",),
        negative_controls=("order-four 90-degree rotation", "order-three 120-degree rotation", "SO(1,1) boost"),
    )


def check_T_effectiveness_from_complete_defect() -> Dict[str, object]:
    fails: List[str] = []
    # The dual residual coordinate in the physical HFC factorization is the
    # second coordinate after applying F^{-1}.  It is a later-completion witness,
    # not a present contender record.
    residual_row = _inv2(F_345)[1]
    defect = V_345
    flipped = _mv2(S_U, defect)
    before = residual_row[0] * defect[0] + residual_row[1] * defect[1]
    after = residual_row[0] * flipped[0] + residual_row[1] * flipped[1]
    if before == 0:
        fails.append("defect witness must be nonzero")
    if after != -before:
        fails.append("exchange must reverse the residual completion signature")
    identity_action = _eye2()
    identity_after = _mv2(identity_action, defect)
    identity_signature = residual_row[0] * identity_after[0] + residual_row[1] * identity_after[1]
    if identity_signature != before:
        fails.append("identity kernel-death control malformed")
    return _result(
        "T_effectiveness_from_complete_defect",
        "HFC retains the relative kernel because it is future-consequential. In the exact F_345 factorization, the residual dual coordinate changes sign under S_u. A later completion reading that coordinate distinguishes the exchanged and unexchanged continuations. The exchange therefore survives the complete operational quotient; no separately postulated recombination leaf is needed beyond future-consequential defect completeness.",
        {
            "defect_vector": _vector_strings(defect),
            "flipped_defect": _vector_strings(flipped),
            "residual_dual_row": _vector_strings(residual_row),
            "signature_before": str(before),
            "signature_after": str(after),
            "identity_signature": str(identity_signature),
            "present_contender_record_formed": False,
        },
        fails,
        dependencies=("T_DSEB_345_discharged_from_HFC",),
        premises=("FUTURE_CONSEQUENTIAL_DEFECT",),
        negative_controls=("label-only exchange represented by identity", "residual kernel declared null"),
    )


def check_T_HFC_independence_countermodel() -> Dict[str, object]:
    fails: List[str] = []
    # The convex identity/exchange world contains the fair visible commoning E+.
    E_plus = _scale2(F(1, 2), _add2(_eye2(), P_SWAP))
    E_minus = _scale2(F(1, 2), _sub2(_eye2(), P_SWAP))
    if _mm2(E_plus, E_plus) != E_plus:
        fails.append("fair common quotient must be idempotent")
    # E_minus maps e1 to (1/2,-1/2), so it is not positive on the pointed
    # nonnegative record cone.  Any positive exchange-odd channel must vanish.
    odd_on_e1 = _mv2(E_minus, (F(1), F(0)))
    if all(x >= 0 for x in odd_on_e1):
        fails.append("defect control must leave the pointed record cone")
    # Exact bounded coefficient grid over the exchange-odd condition D P = -D
    # (fortification, cold-audit minor 5: the previous grid enumerated a
    # trivially true entrywise property and could not fail).  Pointed-cone leg:
    # positive exchange-odd survivors must be exactly {0}.  Non-pointed
    # control: dropping the positivity filter recovers eight nonzero odd maps,
    # so the pointedness premise is load-bearing and this grid can fail.
    pointed_survivors: List[Matrix2] = []
    odd_survivors: List[Matrix2] = []
    vals = (F(-1), F(0), F(1))
    for a in vals:
        for b in vals:
            for c in vals:
                for d in vals:
                    D = ((a, b), (c, d))
                    if _mm2(D, P_SWAP) != _neg2(D):
                        continue
                    odd_survivors.append(D)
                    if all(x >= 0 for row in D for x in row):
                        pointed_survivors.append(D)
    if pointed_survivors != [_zero2()]:
        fails.append("pointed-cone positive exchange-odd survivor set must be {0}")
    if len(odd_survivors) != 9 or sum(1 for D in odd_survivors if D != _zero2()) != 8:
        fails.append("non-pointed control must recover exactly eight nonzero exchange-odd maps")
    nonzero_positive_exchange_odd_exists = any(D != _zero2() for D in pointed_survivors)
    return _result(
        "T_HFC_independence_countermodel",
        "The current minimal APF base does not force HFC. A convex identity/exchange world has the fair common quotient (I+P)/2 but no nonzero positive exchange-odd residual on a pointed committed-record cone. It may erase the defect, hide it in an oriented record, or cross an irreversible boundary. Therefore HFC is an independent quantum-branch availability condition, not unfinished linear algebra.",
        {
            "fair_commoning": _matrix_strings(E_plus),
            "defect_map": _matrix_strings(E_minus),
            "defect_on_positive_seed": _vector_strings(odd_on_e1),
            "nonzero_positive_exchange_odd_exists": nonzero_positive_exchange_odd_exists,
            "coefficient_grid_survivors": len(pointed_survivors),
            "unique_survivor": _matrix_strings(pointed_survivors[0]),
            "nonpointed_odd_survivors": len(odd_survivors),
            "nonpointed_nonzero_odd_survivors": sum(1 for D in odd_survivors if D != _zero2()),
            "pointedness_is_load_bearing": True,
            "HFC_derived_from_A1_MD_A2_BW": False,
        },
        fails,
        negative_controls=("convex identity/exchange world", "destructive fair commoning"),
        epistemic="P_structural_instrument",
    )


DSEB_GRAPH: Dict[str, Tuple[str, ...]] = {
    "T_P10_RELATIVE_KERNEL_RETENTION": (
        "LIVE_345_HELD_FAIR_COMMONING",
        "COMPLETE_HELD_PROFILE",
        "A2_NO_WASTE_MINIMUM",
    ),
    "T_HOC_FACTOR_PACKAGE": (
        "T_P10_RELATIVE_KERNEL_RETENTION",
        "FINITE_COMPATIBLE_JOINT_REALIZATION",
        "FACTOR_ISOLATION_NEUTRAL_COMPLETION",
        "SAME_TYPE_RETURN",
    ),
    "T_345_ACTIVE_CHARACTER_CARRIER": (
        "T_HOC_FACTOR_PACKAGE",
        "EXACT_345_DEFENDER_GEOMETRY",
        "NEUTRAL_E2_COMPLETION",
    ),
    "T_FIRST_EXCHANGE": ("EFFECTIVE_BASELINE_BINARY_EXCHANGE",),
    "T_SECOND_EXCHANGE": (
        "T_345_ACTIVE_CHARACTER_CARRIER",
        "LIVE_345_RECORD_FREE_PORT_EXCHANGE",
        "ZIPPER_REVERSAL_IS_INVERSE",
        "EXCHANGE_CARGO_NATURALITY",
        "FUTURE_CONSEQUENTIAL_DEFECT",
    ),
    "T_DSEB_345": ("T_SECOND_EXCHANGE",),
    "T_R_345": ("T_FIRST_EXCHANGE", "T_DSEB_345"),
    "T_LOCAL_J": ("T_R_345",),
}

FULL_PARALLEL_GRAPH: Dict[str, Tuple[str, ...]] = {
    **DSEB_GRAPH,
    "T_DEFECT_CHANNEL": ("T_HOC_FACTOR_PACKAGE",),
    "T_SIGNED_LOOP_POSITIVITY": (
        "T_DEFECT_CHANNEL",
        "DYADIC_EXTENSION_STABILITY",
        "NONNEGATIVE_PHYSICAL_SELF_LOOPS",
    ),
    "T_POSITIVE_REAL_CSTAR": ("T_SIGNED_LOOP_POSITIVITY",),
    "T_CENTRAL_J": (
        "T_LOCAL_J",
        "NATURALITY",
        "ORIENTATION_SYNCHRONIZATION",
        "GENERATOR_COMPLETENESS",
    ),
    "T_COMPLEX_CSTAR": ("T_POSITIVE_REAL_CSTAR", "T_CENTRAL_J"),
    "T_DENSITY_BORN_CP": (
        "T_COMPLEX_CSTAR",
        "POSITIVE_STATE_SOUNDNESS",
        "EFFECT_SOUNDNESS",
        "COMPOSITE_EXTENSION_SOUNDNESS",
    ),
}


def _all_nodes(graph: Mapping[str, Sequence[str]]) -> set[str]:
    return set(graph) | {d for deps in graph.values() for d in deps}


def _roots(graph: Mapping[str, Sequence[str]]) -> Tuple[str, ...]:
    nodes = set(graph)
    return tuple(sorted({d for deps in graph.values() for d in deps if d not in nodes}))


def _cycle(graph: Mapping[str, Sequence[str]]) -> Optional[Tuple[str, ...]]:
    nodes = _all_nodes(graph)
    state: Dict[str, int] = {n: 0 for n in nodes}
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
            if c is not None:
                return c
        stack.pop()
        state[n] = 2
        return None

    for n in sorted(nodes):
        c = dfs(n)
        if c is not None:
            return c
    return None


def _transitive_dependencies(graph: Mapping[str, Sequence[str]], node: str) -> set[str]:
    out: set[str] = set()
    todo = list(graph.get(node, ()))
    while todo:
        d = todo.pop()
        if d in out:
            continue
        out.add(d)
        todo.extend(graph.get(d, ()))
    return out


def _load_leaf_manifest(path: Path = LEAF_MANIFEST_PATH) -> Dict[str, object]:
    # Bank landing (v24.3.432): the manifest is embedded in the split contract
    # module (two-file discipline preserved); the packet JSON is the fallback so
    # the standalone packet layout still works unchanged.
    if not path.exists():
        from apf._hfc_345_contracts import LEAF_MANIFEST
        data = LEAF_MANIFEST
    else:
        data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("leaves"), dict):
        raise ValueError("invalid leaf manifest")
    return data


def check_T_parallel_orientation_positivity_no_cycle() -> Dict[str, object]:
    fails: List[str] = []
    graph = FULL_PARALLEL_GRAPH
    cyc = _cycle(graph)
    if cyc is not None:
        fails.append(f"dependency cycle: {cyc}")
    deps_J = _transitive_dependencies(graph, "T_LOCAL_J")
    deps_pos = _transitive_dependencies(graph, "T_POSITIVE_REAL_CSTAR")
    if "T_SIGNED_LOOP_POSITIVITY" in deps_J or "T_POSITIVE_REAL_CSTAR" in deps_J:
        fails.append("local J branch must not consume positivity")
    if "T_LOCAL_J" in deps_pos or "T_R_345" in deps_pos:
        fails.append("positivity branch must not consume the orientation branch")
    if graph["T_COMPLEX_CSTAR"] != ("T_POSITIVE_REAL_CSTAR", "T_CENTRAL_J"):
        fails.append("parallel branches must meet only at complex C*-selection")

    # Adversarial cycle mutation: make retention depend on final complex closure.
    mutated = dict(graph)
    mutated["T_P10_RELATIVE_KERNEL_RETENTION"] = (
        *mutated["T_P10_RELATIVE_KERNEL_RETENTION"],
        "T_COMPLEX_CSTAR",
    )
    cycle_mutation_caught = _cycle(mutated) is not None
    if not cycle_mutation_caught:
        fails.append("positivity/orientation cycle mutation not caught")

    return _result(
        "T_parallel_orientation_positivity_no_cycle",
        "HFC is a common upstream availability condition, but its two consequences are parallel. Conservative defect completion supplies signed-loop positivity. The exact two-exchange gate supplies J algebraically. Neither branch derives the other. They meet only when a prior positive real C*-algebra and a central synchronized J select complex blocks.",
        {
            "graph": {k: list(v) for k, v in graph.items()},
            "cycle": cyc,
            "local_J_consumes_positivity": False,
            "positivity_consumes_local_J": False,
            "branches_meet_at": "T_COMPLEX_CSTAR",
            "cycle_mutation_caught": cycle_mutation_caught,
        },
        fails,
        dependencies=tuple(graph),
        negative_controls=("use J to derive the positivity it later consumes", "use positivity to manufacture the exact gate"),
        epistemic="P_structural_instrument",
    )


def check_T_hfc_345_dependency_contract() -> Dict[str, object]:
    fails: List[str] = []
    manifest = _load_leaf_manifest()
    manifest_leaves = tuple(sorted(manifest["leaves"].keys()))  # type: ignore[index,union-attr]
    graph_roots = _roots(DSEB_GRAPH)
    if graph_roots != manifest_leaves:
        fails.append(f"DSEB root inventory drift: {graph_roots} != {manifest_leaves}")
    if _cycle(DSEB_GRAPH) is not None:
        fails.append("DSEB graph must be acyclic")
    forbidden = set(manifest.get("forbidden_substitutions", []))
    graph_tokens = _all_nodes(DSEB_GRAPH)
    leaked = sorted(forbidden & graph_tokens)
    if leaked:
        fails.append(f"forbidden substitutions leaked into graph: {leaked}")

    # Mutations must be caught against the independently stored manifest.
    added = dict(DSEB_GRAPH)
    added["T_LOCAL_J"] = (*added["T_LOCAL_J"], "SECOND_EMPIRICAL_ROOT")
    added_root_caught = _roots(added) != manifest_leaves
    if not added_root_caught:
        fails.append("added-root mutation not caught")

    removed = dict(DSEB_GRAPH)
    for node in ("T_FIRST_EXCHANGE", "T_SECOND_EXCHANGE"):
        removed[node] = tuple(
            d for d in removed[node] if d != "FUTURE_CONSEQUENTIAL_DEFECT"
        )
    removed_leaf_caught = _roots(removed) != manifest_leaves
    if not removed_leaf_caught:
        fails.append("removed-leaf mutation not caught")

    dropped_te_gates = dict(DSEB_GRAPH)
    dropped_te_gates["T_SECOND_EXCHANGE"] = tuple(
        d for d in dropped_te_gates["T_SECOND_EXCHANGE"]
        if d not in ("ZIPPER_REVERSAL_IS_INVERSE", "EXCHANGE_CARGO_NATURALITY")
    )
    te_gate_removal_caught = _roots(dropped_te_gates) != manifest_leaves
    if not te_gate_removal_caught:
        fails.append("TE-fortification gate removal mutation not caught")

    first_jet_mutation = dict(DSEB_GRAPH)
    first_jet_mutation["T_345_ACTIVE_CHARACTER_CARRIER"] = (
        *first_jet_mutation["T_345_ACTIVE_CHARACTER_CARRIER"],
        "ACTIVE_345_PLANE_IS_PAPER10_FIRST_JET",
    )
    first_jet_conflation_caught = bool(forbidden & _all_nodes(first_jet_mutation))
    if not first_jet_conflation_caught:
        fails.append("first-jet conflation mutation not caught")

    return _result(
        "T_hfc_345_dependency_contract",
        "The DSEB_345 node is derived, not a leaf. The fail-closed graph consumes a localized live-345 HFC certificate, a separately effective baseline exchange, the independently manifested completeness/joint-realization leaves, the restored TE-fortification gates (zipper reversal represented by the inverse; exchange-cargo naturality), and exact 3-4-5 geometry. It excludes the rejected first-jet identification, generic sharp-reflection saturation, connected sweep, quadratic-ledger route, pullback nonexpansion, SAT, and G-hold-exact.",
        {
            "graph": {k: list(v) for k, v in DSEB_GRAPH.items()},
            "roots": list(graph_roots),
            "manifest_sha256": (_sha256(LEAF_MANIFEST_PATH) if LEAF_MANIFEST_PATH.exists() else "embedded:apf._hfc_345_contracts.LEAF_MANIFEST"),
            "forbidden_substitutions": sorted(forbidden),
            "forbidden_leaks": leaked,
            "added_root_mutation_caught": added_root_caught,
            "removed_leaf_mutation_caught": removed_leaf_caught,
            "te_gate_removal_mutation_caught": te_gate_removal_caught,
            "first_jet_conflation_caught": first_jet_conflation_caught,
            "DSEB_345_is_root": "T_DSEB_345" in graph_roots,
        },
        fails,
        dependencies=tuple(DSEB_GRAPH),
        premises=manifest_leaves,
        negative_controls=("add SECOND_EMPIRICAL_ROOT", "remove future-consequential defect", "remove the restored TE-fortification gates", "reinsert first-jet conflation"),
        epistemic="P_structural_instrument",
    )


def check_T_central_j_gate_contract() -> Dict[str, object]:
    """Machine-enforced Ruling-3 gate list for T_CENTRAL_J (cold-audit MAJOR-1).

    Ruling 3 of record (2026-07-20): LOCAL_J + NATURALITY +
    ORIENTATION_SYNCHRONIZATION + GENERATOR_COMPLETENESS => CENTRAL_J, never
    less.  The expected antecedent inventory is stored in the separate module
    :mod:`apf._hfc_345_contracts` (pattern: the .429
    ``_held_holonomy_contract.py``), so a silent gate deletion must touch two
    files to pass.  The pre-fortification packet asserted the gate list only
    as prose; the audited M6 mutation (delete GENERATOR_COMPLETENESS) passed
    10/10 checks.  It now fails this check and its test.
    """
    fails: List[str] = []
    live = tuple(sorted(FULL_PARALLEL_GRAPH["T_CENTRAL_J"]))
    expected = tuple(sorted(CENTRAL_J_REQUIRED_GATES))
    if live != expected:
        fails.append(f"central-J antecedent drift: {live} != {expected}")

    deletion_caught: Dict[str, bool] = {}
    for gate in expected:
        mutated_gates = tuple(sorted(g for g in FULL_PARALLEL_GRAPH["T_CENTRAL_J"] if g != gate))
        deletion_caught[gate] = mutated_gates != expected
        if not deletion_caught[gate]:
            fails.append(f"deletion of {gate} from T_CENTRAL_J not caught set-exactly")

    m6 = dict(FULL_PARALLEL_GRAPH)
    m6["T_CENTRAL_J"] = tuple(g for g in m6["T_CENTRAL_J"] if g != "GENERATOR_COMPLETENESS")
    m6_caught = tuple(sorted(m6["T_CENTRAL_J"])) != expected
    if not m6_caught:
        fails.append("audited M6 mutation (drop GENERATOR_COMPLETENESS) not caught")

    deps_local = _transitive_dependencies(FULL_PARALLEL_GRAPH, "T_LOCAL_J")
    for gate in ("NATURALITY", "ORIENTATION_SYNCHRONIZATION", "GENERATOR_COMPLETENESS"):
        if gate in deps_local:
            fails.append(f"T_LOCAL_J must not silently contain the global gate {gate}")

    deps_central = set(FULL_PARALLEL_GRAPH["T_CENTRAL_J"]) | _transitive_dependencies(
        FULL_PARALLEL_GRAPH, "T_CENTRAL_J"
    )
    for gate in expected:
        if gate not in deps_central:
            fails.append(f"T_CENTRAL_J must consume {gate}")

    return _result(
        "T_central_j_gate_contract",
        "Central J stays four-gated per Ruling 3 of record: T_LOCAL_J + NATURALITY + ORIENTATION_SYNCHRONIZATION + GENERATOR_COMPLETENESS => T_CENTRAL_J, never less. The antecedent set is pinned set-exactly against the separately stored inventory in apf._hfc_345_contracts, so deleting any one gate fails this check. The local branch contains none of the three global gates. J is not claimed as central, physical, or implementable by this packet; this check only enforces the gate list on the citable graph instrument.",
        {
            "ruling": "Ruling 3 (2026-07-20): LOCAL_J + NATURALITY + ORIENTATION_SYNCHRONIZATION + GENERATOR_COMPLETENESS => CENTRAL_J",
            "live_gates": list(live),
            "required_gates": list(expected),
            "contract_module": "apf/_hfc_345_contracts.py",
            "single_gate_deletion_caught": dict(deletion_caught),
            "m6_mutation_caught": m6_caught,
            "local_branch_contains_global_gates": False,
        },
        fails,
        dependencies=("T_parallel_orientation_positivity_no_cycle",),
        negative_controls=(
            "M6: delete GENERATOR_COMPLETENESS from T_CENTRAL_J",
            "delete NATURALITY from T_CENTRAL_J",
            "delete ORIENTATION_SYNCHRONIZATION from T_CENTRAL_J",
            "globalize local J without the three gates",
        ),
        epistemic="P_structural_instrument",
    )


# ---------------------------------------------------------------------------
# Fail-closed external certificate verifier
# ---------------------------------------------------------------------------


def verify_physical_interface_certificate(
    payload: Mapping[str, object],
    *,
    manifest_path: Path = LEAF_MANIFEST_PATH,
    source_root: Optional[Path] = None,
) -> Dict[str, object]:
    """Fail-closed certificate verifier.

    Fortification (cold-audit MAJOR-3): the verifier now consults the
    packet's own executable dependency graph.  The certified leaf set is
    computed set-exactly against the root inventory of ``DSEB_GRAPH``, and a
    supplied ``--manifest`` override is REFUSED unless it is byte-identical
    (SHA-256) to the packet-pinned manifest.  The audit's V2 probe (a
    substituted one-leaf manifest with a matching one-leaf payload) is
    therefore rejected in both directions.

    Evidence billing (honest, per the audit): the evidence legs certify
    DIGEST RESOLUTION ONLY -- that each leaf's declared local file exists and
    its bytes hash to the declared SHA-256, i.e. that a signing authority has
    attached that exact file to that leaf.  The verifier does not read or
    judge evidence content; semantic localization (the charter's demand that
    the HFC evidence certify the live candidate ports specifically) remains a
    prose obligation on the certifying authority, not a schema gate.
    """
    manifest = _load_leaf_manifest(manifest_path)
    leaves: Mapping[str, object] = manifest["leaves"]  # type: ignore[assignment]
    failures: List[str] = []

    packet_manifest_sha = _sha256(LEAF_MANIFEST_PATH)
    supplied_manifest_sha = _sha256(manifest_path)
    manifest_is_packet_pinned = supplied_manifest_sha == packet_manifest_sha
    if not manifest_is_packet_pinned:
        failures.append(
            "manifest override rejected: supplied manifest sha256 "
            f"{supplied_manifest_sha} != packet-pinned {packet_manifest_sha}"
        )

    graph_roots = set(_roots(DSEB_GRAPH))
    if set(leaves) != graph_roots:
        failures.append(
            "manifest does not match DSEB_GRAPH root inventory: "
            f"missing={sorted(graph_roots - set(leaves))}, "
            f"extra={sorted(set(leaves) - graph_roots)}"
        )

    if payload.get("schema_version") != manifest.get("schema_version"):
        failures.append("schema_version mismatch")
    if payload.get("claim") != manifest.get("claim"):
        failures.append("claim mismatch")

    evidence = payload.get("evidence")
    if not isinstance(evidence, Mapping):
        failures.append("evidence must be an object")
        evidence = {}
    payload_leaf_names = set(evidence)
    manifest_leaf_names = set(leaves)
    if payload_leaf_names != manifest_leaf_names:
        failures.append(
            "leaf inventory mismatch: "
            f"missing={sorted(manifest_leaf_names-payload_leaf_names)}, "
            f"extra={sorted(payload_leaf_names-manifest_leaf_names)}"
        )

    allowed_classes = {
        "source_theorem",
        "structural_derivation",
        "experiment",
        "device_calibration",
        "principal_adoption",
    }
    exact_structural_leaves = {"EXACT_345_DEFENDER_GEOMETRY"}
    for name in sorted(manifest_leaf_names):
        row = evidence.get(name)
        if not isinstance(row, Mapping):
            failures.append(f"{name}: evidence row missing/malformed")
            continue
        if row.get("certified") is not True:
            failures.append(f"{name}: not certified")
        cls = row.get("evidence_class")
        if cls not in allowed_classes:
            failures.append(f"{name}: unsupported evidence_class {cls!r}")
        digest = row.get("source_digest")
        digest_well_formed = (
            isinstance(digest, str)
            and len(digest) == 64
            and not any(ch not in "0123456789abcdef" for ch in digest.lower())
        )
        if not digest_well_formed:
            failures.append(f"{name}: source_digest must be a 64-character hex SHA-256")

        source_path_raw = row.get("source_path")
        if not isinstance(source_path_raw, str) or not source_path_raw.strip():
            failures.append(f"{name}: source_path must identify a local evidence file")
        else:
            source_path = Path(source_path_raw).expanduser()
            if not source_path.is_absolute():
                source_path = (source_root or PACKAGE_ROOT) / source_path
            try:
                source_path = source_path.resolve(strict=True)
            except FileNotFoundError:
                failures.append(f"{name}: source_path does not exist")
            else:
                if not source_path.is_file():
                    failures.append(f"{name}: source_path is not a file")
                elif digest_well_formed and _sha256(source_path).lower() != str(digest).lower():
                    failures.append(f"{name}: source_digest does not match source bytes")
        if name in exact_structural_leaves and cls not in {"source_theorem", "structural_derivation"}:
            failures.append(f"{name}: exact geometry cannot be certified by finite-precision calibration alone")

    matrices = payload.get("claimed_matrices")
    if not isinstance(matrices, Mapping):
        failures.append("claimed_matrices must be an object")
        matrices = {}
    expected_matrices = {
        "first_exchange": S_0,
        "second_exchange": S_U,
        "product_gate": R_345,
        "derived_J": J_345,
    }
    for key, expected in expected_matrices.items():
        try:
            got = _parse_matrix2(matrices.get(key))
        except Exception as exc:  # noqa: BLE001 - fail-closed report
            failures.append(f"{key}: malformed matrix ({exc})")
            continue
        if got != expected:
            failures.append(f"{key}: matrix mismatch")

    # The payload cannot declare success independently of the verifier.
    if payload.get("physical_premises_certified") is True:
        failures.append("payload may not self-declare physical_premises_certified")

    physical_premises_certified = not failures
    return {
        "claim": manifest.get("claim"),
        "schema_version": manifest.get("schema_version"),
        "manifest_sha256": supplied_manifest_sha,
        "packet_manifest_sha256": packet_manifest_sha,
        "manifest_is_packet_pinned": manifest_is_packet_pinned,
        "dseb_graph_root_count": len(graph_roots),
        "evidence_semantics_verified": False,
        "evidence_billing": (
            "digest resolution only: each leaf's declared local evidence file "
            "exists and its bytes hash to the declared SHA-256; the verifier "
            "does not read or judge evidence content"
        ),
        "leaf_count": len(manifest_leaf_names),
        "physical_premises_certified": physical_premises_certified,
        "DSEB_345_certified": physical_premises_certified,
        "local_J_certified": physical_premises_certified,
        "failures": failures,
        "gate_trace": str(_trace2(R_345)),
        "J": _matrix_strings(J_345),
    }


CHECKS: Dict[str, Callable[[], Dict[str, object]]] = {
    "T_345_neutral_spectator_restriction": check_T_345_neutral_spectator_restriction,
    "T_character_carrier_not_first_jet": check_T_character_carrier_not_first_jet,
    "T_hfc_345_conservative_dilation": check_T_hfc_345_conservative_dilation,
    "T_DSEB_345_discharged_from_HFC": check_T_DSEB_345_discharged_from_HFC,
    "T_two_exchange_gate_and_algebraic_J": check_T_two_exchange_gate_and_algebraic_J,
    "T_optional_dense_circle_corollary": check_T_optional_dense_circle_corollary,
    "T_effectiveness_from_complete_defect": check_T_effectiveness_from_complete_defect,
    "T_HFC_independence_countermodel": check_T_HFC_independence_countermodel,
    "T_parallel_orientation_positivity_no_cycle": check_T_parallel_orientation_positivity_no_cycle,
    "T_hfc_345_dependency_contract": check_T_hfc_345_dependency_contract,
    "T_central_j_gate_contract": check_T_central_j_gate_contract,
}


def run_all() -> Dict[str, Dict[str, object]]:
    return {name: fn() for name, fn in CHECKS.items()}


def build_certificate(results: Optional[Mapping[str, Mapping[str, object]]] = None) -> HFC345Certificate:
    rows = dict(results or run_all())

    def ok(name: str) -> bool:
        return bool(rows[name]["passed"])

    return HFC345Certificate(
        neutral_spectator_split=ok("T_345_neutral_spectator_restriction"),
        character_carrier_type_safe=ok("T_character_carrier_not_first_jet"),
        conservative_dilation_exact=ok("T_hfc_345_conservative_dilation"),
        dseb_345_discharged_relative_to_hfc=ok("T_DSEB_345_discharged_from_HFC"),
        two_exchange_gate_exact=ok("T_two_exchange_gate_and_algebraic_J"),
        algebraic_J_exact=ok("T_two_exchange_gate_and_algebraic_J"),
        optional_dense_circle_corollary=ok("T_optional_dense_circle_corollary"),
        effectiveness_from_complete_defect=ok("T_effectiveness_from_complete_defect"),
        hfc_independence_countermodel=ok("T_HFC_independence_countermodel"),
        parallel_no_cycle=ok("T_parallel_orientation_positivity_no_cycle") and ok("T_hfc_345_dependency_contract"),
        central_j_gate_contract=ok("T_central_j_gate_contract"),
        physical_interface_certificate_verified=False,
        physical_premises_certified=False,
    )


def register(registry: MutableMapping[str, Callable[[], Dict[str, object]]]) -> None:
    registry.update(CHECKS)


def main() -> int:
    results = run_all()
    certificate = build_certificate(results)
    report = {
        "name": "APF_HFC_345_Closure_v0.4",
        "passed": all(bool(r["passed"]) for r in results.values()),
        "n_checks": len(results),
        "n_passed": sum(bool(r["passed"]) for r in results.values()),
        "certificate": asdict(certificate),
        "claim_boundary": {
            "DSEB_345_independent_premise": False,
            "DSEB_345_derived_relative_to_HFC_package": True,
            "local_J_requires_connected_sweep": False,
            "local_J_requires_quadratic_ledger": False,
            "HFC_derived_from_minimal_base": False,
            "physical_inventory_re_typed_not_reduced": True,
            "two_exchange_root_count": 9,
            "hfc_leaf_count": 13,
            "central_J_gates": sorted(CENTRAL_J_REQUIRED_GATES),
            "physical_premises_certified": False,
        },
        "checks": list(results.values()),
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
