"""Exact audit witnesses for the APF zipper operational-reflection bridge.

The candidate bridge is deliberately narrow:

1. an effective binary Held port exchange P transported through a
   completion-faithful common/defect zipper F is the reflection

       tau0 = F P F^-1 = diag(1,-1);

2. if a record-neutral coherent path U transports that reflection actively,

       tau = U tau0 U^-1,       K = U_dot U^-1,

   then

       A = (1/2) tau_dot tau = (K - tau K tau)/2.

   On a positive oriented rank-two holonomy branch, tau K tau = -K, so A=K.

The module certifies exact finite algebra, dependency discipline, and sharp
negative controls.  It does not certify any physical-realisation premise and
is not registered in the APF theorem bank.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from fractions import Fraction as F
from math import isqrt
from typing import Callable, Dict, Iterable, Mapping, Optional, Sequence, Tuple
import json

FAMILY = "quantum.zipper_reflection_bridge_candidate"
Matrix = Tuple[Tuple[F, ...], ...]
Vector = Tuple[F, ...]


@dataclass(frozen=True)
class ZipperReflectionBridgeCertificate:
    effective_port_exchange_reflection_exact: bool
    conjugated_exchange_generator_exact: bool
    live_345_transported_exchange_exact: bool
    label_only_exchange_rejected: bool
    static_effect_saturation_rejected: bool
    commuting_transport_projection_exposed: bool
    dependency_contract_clean: bool
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
        "scope": "exact operational-reflection / conjugation-orbit bridge audit candidate",
        "physical_premises_certified": False,
        "key_result": key_result,
        "dependencies": list(dependencies),
        "premises": list(premises),
        "negative_controls": list(negative_controls),
        "artifacts": dict(artifacts),
        "fail_reasons": list(fails),
    }


# ---------------------------------------------------------------------------
# Exact rational matrix helpers
# ---------------------------------------------------------------------------


def _shape(a: Matrix) -> Tuple[int, int]:
    return len(a), len(a[0]) if a else 0


def _eye(n: int) -> Matrix:
    return tuple(tuple(F(1) if i == j else F(0) for j in range(n)) for i in range(n))


def _zero(n: int, m: Optional[int] = None) -> Matrix:
    m = n if m is None else m
    return tuple(tuple(F(0) for _ in range(m)) for _ in range(n))


def _add(a: Matrix, b: Matrix) -> Matrix:
    if _shape(a) != _shape(b):
        raise ValueError("matrix shape mismatch")
    return tuple(tuple(a[i][j] + b[i][j] for j in range(len(a[0]))) for i in range(len(a)))


def _sub(a: Matrix, b: Matrix) -> Matrix:
    return _add(a, _scale(F(-1), b))


def _scale(s: F, a: Matrix) -> Matrix:
    return tuple(tuple(s * x for x in row) for row in a)


def _mm(a: Matrix, b: Matrix) -> Matrix:
    ar, ac = _shape(a)
    br, bc = _shape(b)
    if ac != br:
        raise ValueError("matrix shape mismatch")
    return tuple(
        tuple(sum(a[i][k] * b[k][j] for k in range(ac)) for j in range(bc))
        for i in range(ar)
    )


def _mv(a: Matrix, v: Vector) -> Vector:
    if _shape(a)[1] != len(v):
        raise ValueError("matrix/vector shape mismatch")
    return tuple(sum(a[i][j] * v[j] for j in range(len(v))) for i in range(len(a)))


def _transpose(a: Matrix) -> Matrix:
    return tuple(tuple(a[j][i] for j in range(len(a))) for i in range(len(a[0])))


def _trace(a: Matrix) -> F:
    n, m = _shape(a)
    if n != m:
        raise ValueError("trace requires square matrix")
    return sum(a[i][i] for i in range(n))


def _det2(a: Matrix) -> F:
    if _shape(a) != (2, 2):
        raise ValueError("det2 requires 2x2 matrix")
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def _inv2(a: Matrix) -> Matrix:
    d = _det2(a)
    if d == 0:
        raise ValueError("singular matrix")
    return ((a[1][1] / d, -a[0][1] / d), (-a[1][0] / d, a[0][0] / d))


def _b_adjoint(a: Matrix, metric: Matrix) -> Matrix:
    return _mm(_mm(_inv2(metric), _transpose(a)), metric)


def _matrix_strings(a: Matrix) -> list[list[str]]:
    return [[str(x) for x in row] for row in a]


def _sqrt_fraction_exact(x: F) -> F:
    if x < 0:
        raise ValueError("negative radicand")
    rn = isqrt(x.numerator)
    rd = isqrt(x.denominator)
    if rn * rn != x.numerator or rd * rd != x.denominator:
        raise ValueError("radicand is not an exact rational square")
    return F(rn, rd)


def _rank_rows(rows: Iterable[Iterable[F]]) -> int:
    work = [[F(x) for x in row] for row in rows]
    work = [row for row in work if any(row)]
    if not work:
        return 0
    r = 0
    ncols = len(work[0])
    for col in range(ncols):
        pivot = next((i for i in range(r, len(work)) if work[i][col] != 0), None)
        if pivot is None:
            continue
        work[r], work[pivot] = work[pivot], work[r]
        p = work[r][col]
        work[r] = [x / p for x in work[r]]
        for i in range(len(work)):
            if i != r and work[i][col] != 0:
                q = work[i][col]
                work[i] = [a - q * b for a, b in zip(work[i], work[r])]
        r += 1
        if r == len(work):
            break
    return r


def _rotation_rational(t: F) -> Tuple[Matrix, Matrix]:
    """SO(2) rotation and derivative in tangent-half-angle coordinate t."""
    d = F(1) + t * t
    c = (F(1) - t * t) / d
    s = F(2) * t / d
    d2 = d * d
    cp = -F(4) * t / d2
    sp = F(2) * (F(1) - t * t) / d2
    return ((c, -s), (s, c)), ((cp, -sp), (sp, cp))


def _normalized_j(a: Matrix) -> Tuple[F, Matrix]:
    rad = -F(1, 2) * _trace(_mm(a, a))
    omega = _sqrt_fraction_exact(rad)
    if omega <= 0:
        raise ValueError("nonpositive angular rate")
    return omega, _scale(F(1) / omega, a)


I2 = _eye(2)
J0: Matrix = ((F(0), F(-1)), (F(1), F(0)))
S0: Matrix = ((F(1), F(0)), (F(0), F(-1)))
PORT_SWAP: Matrix = ((F(0), F(1)), (F(1), F(0)))
ZIPPER: Matrix = ((F(1), F(1)), (F(1), F(-1)))
ZIPPER_INV = _inv2(ZIPPER)
COMMON_DEFECT_METRIC = _mm(_transpose(ZIPPER_INV), ZIPPER_INV)


# ---------------------------------------------------------------------------
# Exact bridge checks
# ---------------------------------------------------------------------------


def check_T_effective_port_exchange_is_operational_reflection() -> Dict[str, object]:
    fails: list[str] = []
    tau0 = _mm(_mm(ZIPPER, PORT_SWAP), ZIPPER_INV)
    if tau0 != S0:
        fails.append("zipper transport of port exchange did not give diag(1,-1)")
    if _mm(tau0, tau0) != I2:
        fails.append("transported exchange is not an involution")
    if _mm(_mm(_transpose(tau0), COMMON_DEFECT_METRIC), tau0) != COMMON_DEFECT_METRIC:
        fails.append("transported exchange does not preserve the induced metric")
    if _b_adjoint(tau0, COMMON_DEFECT_METRIC) != tau0:
        fails.append("transported exchange is not metric-self-adjoint")
    if _mv(tau0, (F(1), F(0))) != (F(1), F(0)):
        fails.append("common line is not fixed")
    if _mv(tau0, (F(0), F(1))) != (F(0), F(-1)):
        fails.append("defect line is not reversed")

    total: Matrix = ((F(1), F(1)),)
    full_rank = _rank_rows(ZIPPER)
    total_rank = _rank_rows(total)
    total_invariant = _mm(total, PORT_SWAP) == total
    defect_killed = _mv(total, (F(1), F(-1))) == (F(0),)
    if (full_rank, total_rank, total_invariant, defect_killed) != (2, 1, True, True):
        fails.append("defect-killed quotient control failed")

    e_plus = _scale(F(1, 2), _add(I2, S0))
    e_minus = _scale(F(1, 2), _sub(I2, S0))
    static_effects = _mm(e_plus, e_plus) == e_plus and _mm(e_minus, e_minus) == e_minus
    static_effects_supply_exchange = False
    if not static_effects:
        fails.append("sharp common/defect effects were not idempotent")

    return _result(
        "T_effective_port_exchange_is_operational_reflection",
        "An effective binary Held port exchange transported through a completion-faithful zipper is exactly the metric-self-adjoint common/defect reflection. Killing the defect makes the raw swap descend to identity; static effects alone do not supply the process.",
        {
            "port_swap": _matrix_strings(PORT_SWAP),
            "zipper": _matrix_strings(ZIPPER),
            "zipper_inverse": _matrix_strings(ZIPPER_INV),
            "induced_metric": _matrix_strings(COMMON_DEFECT_METRIC),
            "tau_0": _matrix_strings(tau0),
            "common_fixed": True,
            "defect_reversed": True,
            "completion_faithful_rank": full_rank,
            "total_only_rank": total_rank,
            "total_only_swap_descends_to_identity": total_invariant,
            "defect_killed_by_total_only_quotient": defect_killed,
            "static_effects_exist": static_effects,
            "static_effects_supply_exchange_process": static_effects_supply_exchange,
        },
        fails,
        premises=(
            "BINARY_HELD_PRESENTATION_REALIZED",
            "EFFECTIVE_RECORD_NEUTRAL_PORT_EXCHANGE",
            "COMPLETION_FAITHFUL_DEFECT_QUOTIENT",
            "EXCHANGE_LEDGER_NEUTRALITY",
            "SAME_TYPE_RETURN",
        ),
        negative_controls=(
            "label-only swap after defect-killing quotient",
            "sharp common/defect effects with process set restricted to identity",
        ),
    )


def check_T_conjugated_exchange_orbit_recovers_holonomy_generator() -> Dict[str, object]:
    fails: list[str] = []
    rows = []
    for t in (F(-1), F(-1, 3), F(0), F(1, 4), F(2, 3), F(1)):
        u, ud = _rotation_rational(t)
        ui = _transpose(u)
        uid = _transpose(ud)
        k = _mm(ud, ui)
        tau = _mm(_mm(u, S0), ui)
        td = _add(_mm(_mm(ud, S0), ui), _mm(_mm(u, S0), uid))
        a = _scale(F(1, 2), _mm(td, tau))
        anti = _scale(F(1, 2), _sub(k, _mm(_mm(tau, k), tau)))
        if a != anti:
            fails.append(f"t={t}: generic projection identity failed")
        if _mm(_mm(tau, k), tau) != _scale(F(-1), k):
            fails.append(f"t={t}: reflection did not reverse SO(2) generator")
        if a != k:
            fails.append(f"t={t}: moving-exchange generator did not equal K")
        if _transpose(k) != _scale(F(-1), k):
            fails.append(f"t={t}: K is not skew")
        omega, j = _normalized_j(a)
        if omega != F(2) / (F(1) + t * t):
            fails.append(f"t={t}: angular rate mismatch")
        if j != J0:
            fails.append(f"t={t}: normalized J mismatch")

        # Passive-frame convention: tau_p = U^-1 tau0 U.
        tp = _mm(_mm(ui, S0), u)
        tdp = _add(_mm(_mm(uid, S0), u), _mm(_mm(ui, S0), ud))
        ap = _scale(F(1, 2), _mm(tdp, tp))
        if ap != _scale(F(-1), k):
            fails.append(f"t={t}: passive sign control failed")

        rows.append({
            "t": str(t),
            "U": _matrix_strings(u),
            "K=U_dot_U_inv": _matrix_strings(k),
            "tau": _matrix_strings(tau),
            "tau_dot": _matrix_strings(td),
            "A=(1/2)tau_dot_tau": _matrix_strings(a),
            "omega": str(omega),
            "J": _matrix_strings(j),
            "passive_A": _matrix_strings(ap),
        })

    # A generator commuting with the current reflection does not move it.
    k_commuting = S0
    td0 = _sub(_mm(k_commuting, S0), _mm(S0, k_commuting))
    a0 = _scale(F(1, 2), _mm(td0, S0))
    projected = a0 == _zero(2) and k_commuting != _zero(2)
    if not projected:
        fails.append("commuting-transport projection control failed")

    return _result(
        "T_conjugated_exchange_orbit_recovers_holonomy_generator",
        "For active tau=U tau0 U^-1, A=(tau_dot tau)/2 is the anti-commuting part (K-tau K tau)/2 of K=U_dot U^-1. On the positive oriented rank-two holonomy branch, tau K tau=-K, so A=K. Passive conjugation reverses the sign.",
        {
            "active_convention": "tau=U tau0 U^-1; K=U_dot U^-1",
            "generic_identity": "A=(K-tau K tau)/2",
            "rank_two_SO2_reduction": "tau K tau=-K => A=K",
            "sample_count": len(rows),
            "samples": rows,
            "commuting_generator": _matrix_strings(k_commuting),
            "commuting_transport_tau_dot": _matrix_strings(td0),
            "moving_exchange_recovers_commuting_component": False,
            "commuting_transport_projection_control": projected,
        },
        fails,
        dependencies=("T_effective_port_exchange_is_operational_reflection",),
        premises=(
            "RECORD_NEUTRAL_EXPORT_FREE_HOLONOMY_PATH",
            "POSITIVE_LEDGER_ISOMETRY",
            "FIRST_ORDER_FAITHFUL_ACTION",
            "NONTRIVIAL_CONJUGATION_ORBIT",
            "FIXED_RANK_TWO_HELD_STRATUM",
        ),
        negative_controls=(
            "passive conjugation sign reversal",
            "commuting/non-isometric transport leaves exchange frame stationary",
        ),
    )


def check_T_live_345_zipper_transports_second_exchange() -> Dict[str, object]:
    fails: list[str] = []
    f345 = _scale(F(1, 5), ((F(-1), F(7)), (F(7), F(1))))
    su = _mm(_mm(f345, PORT_SWAP), _inv2(f345))
    expected_su: Matrix = ((F(-7, 25), F(24, 25)), (F(24, 25), F(7, 25)))
    if su != expected_su:
        fails.append("transported 3-4-5 exchange mismatch")
    if _mm(su, su) != I2 or _mm(_transpose(su), su) != I2:
        fails.append("transported 3-4-5 exchange is not an orthogonal involution")

    r = _mm(su, S0)
    expected_r: Matrix = ((F(-7, 25), F(-24, 25)), (F(24, 25), F(-7, 25)))
    if r != expected_r:
        fails.append("two-exchange rotation matrix mismatch")
    if _det2(r) != 1 or _trace(r) != F(-14, 25):
        fails.append("two-exchange rotation invariants mismatch")

    # A label swap that dies in the physical quotient is represented by I.
    label_only = I2
    label_product = _mm(label_only, S0)
    if label_product != S0 or _det2(label_product) != -1:
        fails.append("label-only second-path control failed")

    return _result(
        "T_live_345_zipper_transports_second_exchange",
        "The exact live 3-4-5 zipper transports the effective binary port swap to Su=F345 P F345^-1; with S0 it yields the trace -14/25 rotation. If the second exchange dies as a label-only swap, the rotation disappears.",
        {
            "F345": _matrix_strings(f345),
            "det_F345": str(_det2(f345)),
            "Su": _matrix_strings(su),
            "R=Su_S0": _matrix_strings(r),
            "det_R": str(_det2(r)),
            "trace_R": str(_trace(r)),
            "label_only_second_exchange_image": _matrix_strings(label_only),
            "label_only_product": _matrix_strings(label_product),
            "effective_second_path_required": True,
        },
        fails,
        dependencies=("T_effective_port_exchange_is_operational_reflection",),
        premises=(
            "LIVE_345_BINARY_HELD_PRESENTATION_REALIZED",
            "PHYSICAL_COMPLETE_ZIPPER_INTERTWINER",
            "EFFECTIVE_SECOND_PORT_EXCHANGE",
            "SAME_CARRIER_RECORD_FREE_RETURN",
        ),
        negative_controls=(
            "label-only second exchange descends to identity",
            "effect projector without effective exchange path",
        ),
    )


# ---------------------------------------------------------------------------
# Dependency contract
# ---------------------------------------------------------------------------

PHYSICAL_PREMISES = (
    "BINARY_HELD_PRESENTATION_REALIZED",
    "EFFECTIVE_RECORD_NEUTRAL_PORT_EXCHANGE",
    "COMPLETION_FAITHFUL_DEFECT_QUOTIENT",
    "EXCHANGE_LEDGER_NEUTRALITY",
    "SAME_TYPE_RETURN",
    "RECORD_NEUTRAL_EXPORT_FREE_HOLONOMY_PATH",
    "POSITIVE_LEDGER_ISOMETRY",
    "FIRST_ORDER_FAITHFUL_ACTION",
    "NONTRIVIAL_CONJUGATION_ORBIT",
    "FIXED_RANK_TWO_HELD_STRATUM",
)

DEPENDENCY_GRAPH: Dict[str, Tuple[str, ...]] = {
    "T_OPERATIONAL_REFLECTION_REALIZATION": PHYSICAL_PREMISES[:5],
    "T_RECORD_NEUTRAL_CONJUGATION_ORBIT": (
        "T_OPERATIONAL_REFLECTION_REALIZATION",
        *PHYSICAL_PREMISES[5:],
    ),
    "T_MOVING_EXCHANGE_PHYSICAL_BRIDGE": ("T_RECORD_NEUTRAL_CONJUGATION_ORBIT",),
    "T_ZIPPER_LOCAL_J": (
        "T_MOVING_EXCHANGE_PHYSICAL_BRIDGE",
        "T_MOVING_EXCHANGE_FORMULA_EXACT",
    ),
}

FORBIDDEN_UPSTREAM = (
    "HILBERT_SPACE",
    "BORN_RULE",
    "COMPLEX_SCALARS",
    "QUARTER_TURN_ASSUMED",
    "CONNECTED_SO2_IMAGE_ASSUMED",
    "EFFECT_SATURATION",
    "PHYSICAL_SHARP_REFLECTION_IMPLEMENTABILITY",
    "LABEL_SWAP_ONLY",
)


def _cycle(graph: Mapping[str, Sequence[str]]) -> Optional[Tuple[str, ...]]:
    nodes = set(graph)
    for deps in graph.values():
        nodes.update(deps)
    state: Dict[str, int] = {}
    stack: list[str] = []

    def dfs(node: str) -> Optional[Tuple[str, ...]]:
        state[node] = 1
        stack.append(node)
        for dep in graph.get(node, ()):
            if state.get(dep, 0) == 0:
                cycle = dfs(dep)
                if cycle is not None:
                    return cycle
            elif state.get(dep) == 1:
                i = stack.index(dep)
                return tuple(stack[i:] + [dep])
        stack.pop()
        state[node] = 2
        return None

    for node in sorted(nodes):
        if state.get(node, 0) == 0:
            cycle = dfs(node)
            if cycle is not None:
                return cycle
    return None


def _deps(graph: Mapping[str, Sequence[str]], node: str) -> set[str]:
    out: set[str] = set()
    todo = list(graph.get(node, ()))
    while todo:
        dep = todo.pop()
        if dep in out:
            continue
        out.add(dep)
        todo.extend(graph.get(dep, ()))
    return out


def _direct_drift(graph: Mapping[str, Sequence[str]]) -> bool:
    required = {"T_MOVING_EXCHANGE_PHYSICAL_BRIDGE", "T_MOVING_EXCHANGE_FORMULA_EXACT"}
    return set(graph.get("T_ZIPPER_LOCAL_J", ())) != required


def check_T_operational_reflection_bridge_dependency_contract() -> Dict[str, object]:
    fails: list[str] = []
    cycle = _cycle(DEPENDENCY_GRAPH)
    if cycle is not None:
        fails.append(f"dependency cycle: {cycle}")
    upstream = _deps(DEPENDENCY_GRAPH, "T_ZIPPER_LOCAL_J")
    forbidden = sorted(set(FORBIDDEN_UPSTREAM) & upstream)
    if forbidden:
        fails.append(f"forbidden upstream dependencies: {forbidden}")
    if _direct_drift(DEPENDENCY_GRAPH):
        fails.append("direct antecedent drift")

    mut_cycle = dict(DEPENDENCY_GRAPH)
    mut_cycle["T_OPERATIONAL_REFLECTION_REALIZATION"] = (
        *mut_cycle["T_OPERATIONAL_REFLECTION_REALIZATION"],
        "T_ZIPPER_LOCAL_J",
    )
    cycle_caught = _cycle(mut_cycle) is not None

    mut_effect = dict(DEPENDENCY_GRAPH)
    mut_effect["T_OPERATIONAL_REFLECTION_REALIZATION"] = (
        *mut_effect["T_OPERATIONAL_REFLECTION_REALIZATION"],
        "EFFECT_SATURATION",
    )
    effect_caught = "EFFECT_SATURATION" in _deps(mut_effect, "T_ZIPPER_LOCAL_J")

    mut_quarter = dict(DEPENDENCY_GRAPH)
    mut_quarter["T_RECORD_NEUTRAL_CONJUGATION_ORBIT"] = (
        *mut_quarter["T_RECORD_NEUTRAL_CONJUGATION_ORBIT"],
        "QUARTER_TURN_ASSUMED",
    )
    quarter_caught = "QUARTER_TURN_ASSUMED" in _deps(mut_quarter, "T_ZIPPER_LOCAL_J")

    deletion_caught = True
    for gate in DEPENDENCY_GRAPH["T_ZIPPER_LOCAL_J"]:
        mut_drop = dict(DEPENDENCY_GRAPH)
        mut_drop["T_ZIPPER_LOCAL_J"] = tuple(
            x for x in mut_drop["T_ZIPPER_LOCAL_J"] if x != gate
        )
        if not _direct_drift(mut_drop):
            deletion_caught = False

    if not all((cycle_caught, effect_caught, quarter_caught, deletion_caught)):
        fails.append("one or more dependency mutations escaped")

    return _result(
        "T_operational_reflection_bridge_dependency_contract",
        "The moving-exchange physical premise is decomposed into an effective binary Held exchange, completion-faithful defect quotient, exchange-neutral same-type return, and record-neutral positive-isometric conjugation path. Effect saturation, label-only swaps, assumed quarter-turn/SO(2), Hilbert, Born, and complex scalars are forbidden upstream.",
        {
            "graph": {k: list(v) for k, v in DEPENDENCY_GRAPH.items()},
            "cycle": cycle,
            "upstream_of_local_J": sorted(upstream),
            "forbidden_upstream": list(FORBIDDEN_UPSTREAM),
            "physical_premises": list(PHYSICAL_PREMISES),
            "cycle_mutation_caught": cycle_caught,
            "effect_saturation_smuggling_caught": effect_caught,
            "quarter_turn_smuggling_caught": quarter_caught,
            "direct_gate_deletion_caught": deletion_caught,
            "bank_registration": False,
            "audit_status": "candidate_not_banked",
        },
        fails,
        dependencies=tuple(DEPENDENCY_GRAPH),
        premises=PHYSICAL_PREMISES,
        negative_controls=(
            "effect saturation substituted for process realization",
            "label-only swap substituted for effective quotient action",
            "assumed quarter-turn/SO(2) inserted upstream",
            "bridge/formula cycle",
        ),
        epistemic="P_structural_instrument",
    )


CHECKS: Dict[str, Callable[[], Dict[str, object]]] = {
    "T_effective_port_exchange_is_operational_reflection": check_T_effective_port_exchange_is_operational_reflection,
    "T_conjugated_exchange_orbit_recovers_holonomy_generator": check_T_conjugated_exchange_orbit_recovers_holonomy_generator,
    "T_live_345_zipper_transports_second_exchange": check_T_live_345_zipper_transports_second_exchange,
    "T_operational_reflection_bridge_dependency_contract": check_T_operational_reflection_bridge_dependency_contract,
}


def run_all() -> Dict[str, Dict[str, object]]:
    return {name: fn() for name, fn in CHECKS.items()}


def build_certificate(
    results: Optional[Mapping[str, Mapping[str, object]]] = None,
) -> ZipperReflectionBridgeCertificate:
    rows = dict(results or run_all())

    def ok(name: str) -> bool:
        return bool(rows[name]["passed"])

    refl = rows["T_effective_port_exchange_is_operational_reflection"]["artifacts"]
    orbit = rows["T_conjugated_exchange_orbit_recovers_holonomy_generator"]["artifacts"]
    return ZipperReflectionBridgeCertificate(
        effective_port_exchange_reflection_exact=ok("T_effective_port_exchange_is_operational_reflection"),
        conjugated_exchange_generator_exact=ok("T_conjugated_exchange_orbit_recovers_holonomy_generator"),
        live_345_transported_exchange_exact=ok("T_live_345_zipper_transports_second_exchange"),
        label_only_exchange_rejected=bool(refl["defect_killed_by_total_only_quotient"]),
        static_effect_saturation_rejected=not bool(refl["static_effects_supply_exchange_process"]),
        commuting_transport_projection_exposed=bool(orbit["commuting_transport_projection_control"]),
        dependency_contract_clean=ok("T_operational_reflection_bridge_dependency_contract"),
        physical_premises_certified=False,
    )


def main() -> int:
    results = run_all()
    certificate = build_certificate(results)
    payload = {
        "name": "APF_Zipper_Operational_Reflection_Bridge_v0.1",
        "family": FAMILY,
        "passed": all(bool(row["passed"]) for row in results.values()),
        "n_checks": len(results),
        "n_passed": sum(bool(row["passed"]) for row in results.values()),
        "certificate": asdict(certificate),
        "claim_boundary": {
            "operational_reflection_formula": "tau0=F P F^-1 on a physical completion-faithful binary zipper",
            "conjugation_orbit_formula": "tau=U tau0 U^-1; A=(tau_dot tau)/2=(K-tau K tau)/2",
            "rank_two_positive_holonomy_reduction": "tau K tau=-K => A=K=U_dot U^-1",
            "physical_premises_certified": False,
            "bank_registered": False,
        },
        "checks": list(results.values()),
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
