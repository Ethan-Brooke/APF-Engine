"""Unbanked physical bridge from effective Held exchange to moving reflection.

Exact scope:
  tau0 = F P F^-1 on a completion-faithful binary Held zipper;
  tau = U tau0 U^-1;
  A = (1/2) tau_dot tau = (K - tau K tau)/2, K = U_dot U^-1;
  on the positive oriented rank-two holonomy branch, tau K tau = -K, so A=K.

The module certifies finite algebra and countermodels only.  Every physical
realisation premise remains named and uncertified.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Callable, Dict, Iterable, Mapping, Optional, Sequence, Tuple
import json

from apf import zipper_reduction as zr

F = zr.F
Matrix = zr.Matrix
Vector = Tuple[F, ...]
FAMILY = "quantum.zipper_reflection_bridge_candidate"


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


def _result(name: str, key_result: str, artifacts: Mapping[str, object], fails: Sequence[str], *,
            dependencies: Sequence[str] = (), premises: Sequence[str] = (),
            negative_controls: Sequence[str] = (), epistemic: str = "P_math") -> Dict[str, object]:
    passed = not fails
    return {
        "name": name, "family": FAMILY, "tier": 4, "epistemic": epistemic,
        "status": "PASS" if passed else "FAIL", "passed": passed,
        "scope": "exact operational-reflection / conjugation-orbit bridge audit candidate",
        "physical_premises_certified": False, "key_result": key_result,
        "dependencies": list(dependencies), "premises": list(premises),
        "negative_controls": list(negative_controls), "artifacts": dict(artifacts),
        "fail_reasons": list(fails),
    }


def _sub(a: Matrix, b: Matrix) -> Matrix:
    return zr._add(a, zr._scale(F(-1), b))


def _rank_rows(rows: Iterable[Iterable[F]]) -> int:
    work = [[F(x) for x in row] for row in rows]
    work = [row for row in work if any(row)]
    if not work:
        return 0
    r, ncols = 0, len(work[0])
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


def _normalized_j(a: Matrix) -> Tuple[F, Matrix]:
    rad = -F(1, 2) * zr._trace(zr._mm(a, a))
    omega = zr._sqrt_fraction_exact(rad)
    if omega <= 0:
        raise ValueError("nonpositive angular rate")
    return omega, zr._scale(F(1) / omega, a)


I2, J0, S0 = zr.I2, zr.J0, zr.S0
PORT_SWAP: Matrix = ((F(0), F(1)), (F(1), F(0)))
ZIPPER: Matrix = ((F(1), F(1)), (F(1), F(-1)))
ZIPPER_INV = zr._inv2(ZIPPER)
COMMON_DEFECT_METRIC = zr._mm(zr._transpose(ZIPPER_INV), ZIPPER_INV)


def check_T_effective_port_exchange_is_operational_reflection() -> Dict[str, object]:
    fails: list[str] = []
    tau0 = zr._mm(zr._mm(ZIPPER, PORT_SWAP), ZIPPER_INV)
    if tau0 != S0:
        fails.append("zipper transport of port exchange did not give diag(1,-1)")
    if zr._mm(tau0, tau0) != I2:
        fails.append("transported exchange is not an involution")
    if zr._mm(zr._mm(zr._transpose(tau0), COMMON_DEFECT_METRIC), tau0) != COMMON_DEFECT_METRIC:
        fails.append("transported exchange does not preserve the induced metric")
    if zr._b_adjoint(tau0, COMMON_DEFECT_METRIC) != tau0:
        fails.append("transported exchange is not metric-self-adjoint")
    if zr._mv(tau0, (F(1), F(0))) != (F(1), F(0)):
        fails.append("common line not fixed")
    if zr._mv(tau0, (F(0), F(1))) != (F(0), F(-1)):
        fails.append("defect line not reversed")

    total: Matrix = ((F(1), F(1)),)
    full_rank, total_rank = _rank_rows(ZIPPER), _rank_rows(total)
    total_invariant = zr._mm(total, PORT_SWAP) == total
    defect_killed = zr._mv(total, (F(1), F(-1))) == (F(0),)
    if (full_rank, total_rank, total_invariant, defect_killed) != (2, 1, True, True):
        fails.append("defect-killed quotient control failed")

    e_plus = zr._scale(F(1, 2), zr._add(I2, S0))
    e_minus = zr._scale(F(1, 2), _sub(I2, S0))
    static_effects = zr._mm(e_plus, e_plus) == e_plus and zr._mm(e_minus, e_minus) == e_minus
    exchange_absent = PORT_SWAP not in (I2,)
    if not static_effects or not exchange_absent:
        fails.append("effect/process separation control failed")

    return _result(
        "T_effective_port_exchange_is_operational_reflection",
        "An effective binary Held port exchange transported through a completion-faithful zipper is exactly the metric-self-adjoint common/defect reflection. Killing the defect makes the raw swap descend to identity; static effects alone do not supply the process.",
        {
            "port_swap": zr._matrix_strings(PORT_SWAP), "zipper": zr._matrix_strings(ZIPPER),
            "zipper_inverse": zr._matrix_strings(ZIPPER_INV),
            "induced_metric": zr._matrix_strings(COMMON_DEFECT_METRIC),
            "tau_0": zr._matrix_strings(tau0), "common_fixed": True, "defect_reversed": True,
            "completion_faithful_rank": full_rank, "total_only_rank": total_rank,
            "total_only_swap_descends_to_identity": total_invariant,
            "defect_killed_by_total_only_quotient": defect_killed,
            "static_effects_exist": static_effects, "static_effects_supply_exchange_process": False,
        },
        fails,
        premises=("BINARY_HELD_PRESENTATION_REALIZED", "EFFECTIVE_RECORD_NEUTRAL_PORT_EXCHANGE",
                  "COMPLETION_FAITHFUL_DEFECT_QUOTIENT", "EXCHANGE_LEDGER_NEUTRALITY", "SAME_TYPE_RETURN"),
        negative_controls=("label-only swap after defect-killing quotient",
                           "sharp common/defect effects with process set restricted to identity"),
    )


def check_T_conjugated_exchange_orbit_recovers_holonomy_generator() -> Dict[str, object]:
    fails: list[str] = []
    rows = []
    for t in (F(-1), F(-1, 3), F(0), F(1, 4), F(2, 3), F(1)):
        u, ud = zr._rotation_rational(t)
        ui, uid = zr._transpose(u), zr._transpose(ud)
        k = zr._mm(ud, ui)
        tau = zr._mm(zr._mm(u, S0), ui)
        td = zr._add(zr._mm(zr._mm(ud, S0), ui), zr._mm(zr._mm(u, S0), uid))
        a = zr._scale(F(1, 2), zr._mm(td, tau))
        anti = zr._scale(F(1, 2), _sub(k, zr._mm(zr._mm(tau, k), tau)))
        if a != anti or zr._mm(zr._mm(tau, k), tau) != zr._scale(F(-1), k) or a != k:
            fails.append(f"t={t}: conjugation-generator identity failed")
        if zr._transpose(k) != zr._scale(F(-1), k):
            fails.append(f"t={t}: K is not skew")
        omega, j = _normalized_j(a)
        if omega != F(2) / (F(1) + t * t) or j != J0:
            fails.append(f"t={t}: normalized J mismatch")

        tp = zr._mm(zr._mm(ui, S0), u)
        tdp = zr._add(zr._mm(zr._mm(uid, S0), u), zr._mm(zr._mm(ui, S0), ud))
        ap = zr._scale(F(1, 2), zr._mm(tdp, tp))
        if ap != zr._scale(F(-1), k):
            fails.append(f"t={t}: passive sign control failed")
        rows.append({
            "t": str(t), "U": zr._matrix_strings(u), "K=U_dot_U_inv": zr._matrix_strings(k),
            "tau": zr._matrix_strings(tau), "tau_dot": zr._matrix_strings(td),
            "A=(1/2)tau_dot_tau": zr._matrix_strings(a), "omega": str(omega),
            "J": zr._matrix_strings(j), "passive_A": zr._matrix_strings(ap),
        })

    k_commuting = S0
    td0 = _sub(zr._mm(k_commuting, S0), zr._mm(S0, k_commuting))
    a0 = zr._scale(F(1, 2), zr._mm(td0, S0))
    projected = a0 == zr._zero(2) and k_commuting != zr._zero(2)
    if not projected:
        fails.append("commuting-transport projection control failed")

    return _result(
        "T_conjugated_exchange_orbit_recovers_holonomy_generator",
        "For active tau=U tau0 U^-1, A=(tau_dot tau)/2 is the anti-commuting part (K-tau K tau)/2 of K=U_dot U^-1. On the positive oriented rank-two holonomy branch, tau K tau=-K, so A=K. Passive conjugation reverses the sign.",
        {
            "active_convention": "tau=U tau0 U^-1; K=U_dot U^-1",
            "generic_identity": "A=(K-tau K tau)/2",
            "rank_two_SO2_reduction": "tau K tau=-K => A=K",
            "sample_count": len(rows), "samples": rows,
            "commuting_generator": zr._matrix_strings(k_commuting),
            "commuting_transport_tau_dot": zr._matrix_strings(td0),
            "moving_exchange_recovers_commuting_component": False,
            "commuting_transport_projection_control": projected,
        },
        fails,
        dependencies=("T_effective_port_exchange_is_operational_reflection",),
        premises=("RECORD_NEUTRAL_EXPORT_FREE_HOLONOMY_PATH", "POSITIVE_LEDGER_ISOMETRY",
                  "FIRST_ORDER_FAITHFUL_ACTION", "NONTRIVIAL_CONJUGATION_ORBIT",
                  "FIXED_RANK_TWO_HELD_STRATUM"),
        negative_controls=("passive conjugation sign reversal",
                           "commuting/non-isometric transport leaves exchange frame stationary"),
    )


def check_T_live_345_zipper_transports_second_exchange() -> Dict[str, object]:
    fails: list[str] = []
    f345 = zr._scale(F(1, 5), ((F(-1), F(7)), (F(7), F(1))))
    su = zr._mm(zr._mm(f345, PORT_SWAP), zr._inv2(f345))
    expected_su = ((F(-7, 25), F(24, 25)), (F(24, 25), F(7, 25)))
    if su != expected_su or zr._mm(su, su) != I2 or zr._mm(zr._transpose(su), su) != I2:
        fails.append("transported 3-4-5 exchange mismatch")
    r = zr._mm(su, S0)
    expected_r = ((F(-7, 25), F(-24, 25)), (F(24, 25), F(-7, 25)))
    if r != expected_r or zr._det2(r) != 1 or zr._trace(r) != F(-14, 25):
        fails.append("two-exchange rotation mismatch")
    label_only = I2
    label_product = zr._mm(label_only, S0)
    if label_product != S0 or zr._det2(label_product) != -1:
        fails.append("label-only second-path control failed")
    return _result(
        "T_live_345_zipper_transports_second_exchange",
        "The exact live 3-4-5 zipper transports the effective binary port swap to Su=F345 P F345^-1; with S0 it yields the trace -14/25 rotation. If the second exchange dies as a label-only swap, the rotation disappears.",
        {
            "F345": zr._matrix_strings(f345), "det_F345": str(zr._det2(f345)),
            "Su": zr._matrix_strings(su), "R=Su_S0": zr._matrix_strings(r),
            "det_R": str(zr._det2(r)), "trace_R": str(zr._trace(r)),
            "label_only_second_exchange_image": zr._matrix_strings(label_only),
            "label_only_product": zr._matrix_strings(label_product),
            "effective_second_path_required": True,
        },
        fails,
        dependencies=("T_effective_port_exchange_is_operational_reflection",),
        premises=("LIVE_345_BINARY_HELD_PRESENTATION_REALIZED", "PHYSICAL_COMPLETE_ZIPPER_INTERTWINER",
                  "EFFECTIVE_SECOND_PORT_EXCHANGE", "SAME_CARRIER_RECORD_FREE_RETURN"),
        negative_controls=("label-only second exchange descends to identity",
                           "effect projector without effective exchange path"),
    )


PHYSICAL_PREMISES = (
    "BINARY_HELD_PRESENTATION_REALIZED", "EFFECTIVE_RECORD_NEUTRAL_PORT_EXCHANGE",
    "COMPLETION_FAITHFUL_DEFECT_QUOTIENT", "EXCHANGE_LEDGER_NEUTRALITY", "SAME_TYPE_RETURN",
    "RECORD_NEUTRAL_EXPORT_FREE_HOLONOMY_PATH", "POSITIVE_LEDGER_ISOMETRY",
    "FIRST_ORDER_FAITHFUL_ACTION", "NONTRIVIAL_CONJUGATION_ORBIT", "FIXED_RANK_TWO_HELD_STRATUM",
)
DEPENDENCY_GRAPH: Dict[str, Tuple[str, ...]] = {
    "T_OPERATIONAL_REFLECTION_REALIZATION": PHYSICAL_PREMISES[:5],
    "T_RECORD_NEUTRAL_CONJUGATION_ORBIT": (
        "T_OPERATIONAL_REFLECTION_REALIZATION", *PHYSICAL_PREMISES[5:]
    ),
    "T_MOVING_EXCHANGE_PHYSICAL_BRIDGE": ("T_RECORD_NEUTRAL_CONJUGATION_ORBIT",),
    "T_ZIPPER_LOCAL_J": ("T_MOVING_EXCHANGE_PHYSICAL_BRIDGE", "T_MOVING_EXCHANGE_FORMULA_EXACT"),
}
FORBIDDEN_UPSTREAM = (
    "HILBERT_SPACE", "BORN_RULE", "COMPLEX_SCALARS", "QUARTER_TURN_ASSUMED",
    "CONNECTED_SO2_IMAGE_ASSUMED", "EFFECT_SATURATION",
    "PHYSICAL_SHARP_REFLECTION_IMPLEMENTABILITY", "LABEL_SWAP_ONLY",
)


def _cycle(graph: Mapping[str, Sequence[str]]) -> Optional[Tuple[str, ...]]:
    nodes = set(graph)
    for deps in graph.values():
        nodes.update(deps)
    state: Dict[str, int] = {}
    stack: list[str] = []
    def dfs(n: str) -> Optional[Tuple[str, ...]]:
        state[n] = 1; stack.append(n)
        for d in graph.get(n, ()):
            if state.get(d, 0) == 0:
                c = dfs(d)
                if c is not None: return c
            elif state.get(d) == 1:
                i = stack.index(d); return tuple(stack[i:] + [d])
        stack.pop(); state[n] = 2; return None
    for n in sorted(nodes):
        if state.get(n, 0) == 0:
            c = dfs(n)
            if c is not None: return c
    return None


def _deps(graph: Mapping[str, Sequence[str]], node: str) -> set[str]:
    out, todo = set(), list(graph.get(node, ()))
    while todo:
        d = todo.pop()
        if d in out: continue
        out.add(d); todo.extend(graph.get(d, ()))
    return out


def _direct_drift(graph: Mapping[str, Sequence[str]]) -> bool:
    return set(graph.get("T_ZIPPER_LOCAL_J", ())) != {
        "T_MOVING_EXCHANGE_PHYSICAL_BRIDGE", "T_MOVING_EXCHANGE_FORMULA_EXACT"
    }


def check_T_operational_reflection_bridge_dependency_contract() -> Dict[str, object]:
    fails: list[str] = []
    cycle = _cycle(DEPENDENCY_GRAPH)
    if cycle is not None: fails.append(f"dependency cycle: {cycle}")
    upstream = _deps(DEPENDENCY_GRAPH, "T_ZIPPER_LOCAL_J")
    forbidden = sorted(set(FORBIDDEN_UPSTREAM) & upstream)
    if forbidden: fails.append(f"forbidden upstream dependencies: {forbidden}")
    if _direct_drift(DEPENDENCY_GRAPH): fails.append("direct antecedent drift")

    mc = dict(DEPENDENCY_GRAPH)
    mc["T_OPERATIONAL_REFLECTION_REALIZATION"] = (*mc["T_OPERATIONAL_REFLECTION_REALIZATION"], "T_ZIPPER_LOCAL_J")
    cycle_caught = _cycle(mc) is not None
    me = dict(DEPENDENCY_GRAPH)
    me["T_OPERATIONAL_REFLECTION_REALIZATION"] = (*me["T_OPERATIONAL_REFLECTION_REALIZATION"], "EFFECT_SATURATION")
    effect_caught = "EFFECT_SATURATION" in _deps(me, "T_ZIPPER_LOCAL_J")
    mq = dict(DEPENDENCY_GRAPH)
    mq["T_RECORD_NEUTRAL_CONJUGATION_ORBIT"] = (*mq["T_RECORD_NEUTRAL_CONJUGATION_ORBIT"], "QUARTER_TURN_ASSUMED")
    quarter_caught = "QUARTER_TURN_ASSUMED" in _deps(mq, "T_ZIPPER_LOCAL_J")
    deletion_caught = True
    for gate in DEPENDENCY_GRAPH["T_ZIPPER_LOCAL_J"]:
        md = dict(DEPENDENCY_GRAPH)
        md["T_ZIPPER_LOCAL_J"] = tuple(x for x in md["T_ZIPPER_LOCAL_J"] if x != gate)
        if not _direct_drift(md): deletion_caught = False
    if not all((cycle_caught, effect_caught, quarter_caught, deletion_caught)):
        fails.append("one or more dependency mutations escaped")

    return _result(
        "T_operational_reflection_bridge_dependency_contract",
        "The moving-exchange physical premise is decomposed into an effective binary Held exchange, completion-faithful defect quotient, exchange-neutral same-type return, and record-neutral positive-isometric conjugation path. Effect saturation, label-only swaps, assumed quarter-turn/SO(2), Hilbert, Born, and complex scalars are forbidden upstream.",
        {
            "graph": {k: list(v) for k, v in DEPENDENCY_GRAPH.items()}, "cycle": cycle,
            "upstream_of_local_J": sorted(upstream), "forbidden_upstream": list(FORBIDDEN_UPSTREAM),
            "physical_premises": list(PHYSICAL_PREMISES), "cycle_mutation_caught": cycle_caught,
            "effect_saturation_smuggling_caught": effect_caught,
            "quarter_turn_smuggling_caught": quarter_caught,
            "direct_gate_deletion_caught": deletion_caught,
            "bank_registration": False, "audit_status": "candidate_not_banked",
        },
        fails,
        dependencies=tuple(DEPENDENCY_GRAPH), premises=PHYSICAL_PREMISES,
        negative_controls=("effect saturation substituted for process realization",
                           "label-only swap substituted for effective quotient action",
                           "assumed quarter-turn/SO(2) inserted upstream", "bridge/formula cycle"),
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


def build_certificate(results: Optional[Mapping[str, Mapping[str, object]]] = None) -> ZipperReflectionBridgeCertificate:
    rows = dict(results or run_all())
    ok = lambda name: bool(rows[name]["passed"])
    refl = rows["T_effective_port_exchange_is_operational_reflection"]["artifacts"]
    orbit = rows["T_conjugated_exchange_orbit_recovers_holonomy_generator"]["artifacts"]
    return ZipperReflectionBridgeCertificate(
        ok("T_effective_port_exchange_is_operational_reflection"),
        ok("T_conjugated_exchange_orbit_recovers_holonomy_generator"),
        ok("T_live_345_zipper_transports_second_exchange"),
        bool(refl["defect_killed_by_total_only_quotient"]),
        not bool(refl["static_effects_supply_exchange_process"]),
        bool(orbit["commuting_transport_projection_control"]),
        ok("T_operational_reflection_bridge_dependency_contract"), False,
    )


def main() -> int:
    results = run_all(); cert = build_certificate(results)
    payload = {
        "name": "APF_Zipper_Operational_Reflection_Bridge_v0.1", "family": FAMILY,
        "passed": all(bool(r["passed"]) for r in results.values()),
        "n_checks": len(results), "n_passed": sum(bool(r["passed"]) for r in results.values()),
        "certificate": asdict(cert),
        "claim_boundary": {
            "operational_reflection_formula": "tau0=F P F^-1 on a physical completion-faithful binary zipper",
            "conjugation_orbit_formula": "tau=U tau0 U^-1; A=(tau_dot tau)/2=(K-tau K tau)/2",
            "rank_two_positive_holonomy_reduction": "tau K tau=-K => A=K=U_dot U^-1",
            "physical_premises_certified": False, "bank_registered": False,
        },
        "checks": list(results.values()),
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
