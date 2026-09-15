"""Audit-candidate exact witnesses for the APF zipper-reduction formula.

The candidate local theorem is deliberately narrow.  On a realised positive
rank-two Held event plane, let ``tau(s)`` be a differentiable family of
metric-self-adjoint involutions representing the operational comparison frame.
For a non-stationary frame define

    A = (1/2) * tau_dot * tau,
    omega = sqrt(-(1/2) * tr(A^2)),
    J = A / omega.

Differentiating tau^2 = I makes A skew-adjoint.  In positive real rank two a
nonzero skew-adjoint endomorphism squares to a negative scalar multiple of the
identity, so the normalization gives J^2 = -I.

This packet certifies exact finite mathematics, covariance, and sharp negative
controls.  It does NOT certify that an active record-kernel, positive event
metric, differentiable non-stationary operational exchange frame, or
record-neutral completion path is physically realised.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from fractions import Fraction as F
from math import isqrt
from typing import Callable, Dict, Iterable, Mapping, MutableMapping, Optional, Sequence, Tuple
import json

FAMILY = "quantum.zipper_reduction_candidate"
Matrix = Tuple[Tuple[F, ...], ...]


@dataclass(frozen=True)
class ZipperReductionCertificate:
    moving_exchange_formula_exact: bool
    metric_covariance_exact: bool
    orientation_sign_exact: bool
    reflection_product_holonomy_exact: bool
    stationary_frame_rejected: bool
    derivative_incompatibility_rejected: bool
    indefinite_signature_rejected: bool
    rank_two_scope_fenced: bool
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
        "scope": "exact rank-two moving-exchange mathematics / audit candidate",
        "physical_premises_certified": False,
        "key_result": key_result,
        "dependencies": list(dependencies),
        "premises": list(premises),
        "negative_controls": list(negative_controls),
        "artifacts": dict(artifacts),
        "fail_reasons": list(fails),
    }


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


def _block_diag(*blocks: Matrix) -> Matrix:
    sizes = [len(b) for b in blocks]
    total = sum(sizes)
    out = [[F(0) for _ in range(total)] for _ in range(total)]
    offset = 0
    for block in blocks:
        n, m = _shape(block)
        if n != m:
            raise ValueError("block diagonal requires square blocks")
        for i in range(n):
            for j in range(n):
                out[offset + i][offset + j] = block[i][j]
        offset += n
    return tuple(tuple(row) for row in out)


def _matrix_strings(a: Matrix) -> list[list[str]]:
    return [[str(x) for x in row] for row in a]


def _sqrt_fraction_exact(x: F) -> F:
    if x < 0:
        raise ValueError("normalization radicand is negative")
    rn = isqrt(x.numerator)
    rd = isqrt(x.denominator)
    if rn * rn != x.numerator or rd * rd != x.denominator:
        raise ValueError("normalization radicand is not an exact rational square")
    return F(rn, rd)


def _is_positive_definite_2(metric: Matrix) -> bool:
    return _shape(metric) == (2, 2) and metric == _transpose(metric) and metric[0][0] > 0 and _det2(metric) > 0


def _b_adjoint(a: Matrix, metric: Matrix) -> Matrix:
    return _mm(_mm(_inv2(metric), _transpose(a)), metric)


I2 = _eye(2)
J0: Matrix = ((F(0), F(-1)), (F(1), F(0)))
S0: Matrix = ((F(1), F(0)), (F(0), F(-1)))


def _rotation_rational(t: F) -> Tuple[Matrix, Matrix]:
    """R(t) and dR/dt for tangent-half-angle parameter t."""
    d = F(1) + t * t
    c = (F(1) - t * t) / d
    s = F(2) * t / d
    d2 = d * d
    cp = -F(4) * t / d2
    sp = F(2) * (F(1) - t * t) / d2
    r = ((c, -s), (s, c))
    rp = ((cp, -sp), (sp, cp))
    return r, rp


def _moving_reflection(t: F) -> Tuple[Matrix, Matrix]:
    r, rp = _rotation_rational(t)
    rt = _transpose(r)
    rpt = _transpose(rp)
    tau = _mm(_mm(r, S0), rt)
    tau_dot = _add(_mm(_mm(rp, S0), rt), _mm(_mm(r, S0), rpt))
    return tau, tau_dot


def _boost_rational(u: F) -> Tuple[Matrix, Matrix, Matrix, Matrix]:
    """O(1,1) boost B(u), inverse, and derivatives for |u|<1."""
    d = F(1) - u * u
    c = (F(1) + u * u) / d
    s = F(2) * u / d
    d2 = d * d
    cp = F(4) * u / d2
    sp = F(2) * (F(1) + u * u) / d2
    b = ((c, s), (s, c))
    bi = ((c, -s), (-s, c))
    bp = ((cp, sp), (sp, cp))
    bip = ((cp, -sp), (-sp, cp))
    return b, bi, bp, bip


def _moving_indefinite_reflection(u: F) -> Tuple[Matrix, Matrix]:
    b, bi, bp, bip = _boost_rational(u)
    tau = _mm(_mm(b, S0), bi)
    tau_dot = _add(_mm(_mm(bp, S0), bi), _mm(_mm(b, S0), bip))
    return tau, tau_dot


def derive_complex_structure(tau: Matrix, tau_dot: Matrix, metric: Matrix = I2) -> Dict[str, object]:
    """Validate the moving-exchange hypotheses and return the normalized J.

    The function fails closed outside a positive rank-two metric plane, for a
    stationary frame, or when ``tau_dot`` is not tangent to the involution
    manifold at ``tau``.
    """
    if _shape(tau) != (2, 2) or _shape(tau_dot) != (2, 2):
        raise ValueError("zipper formula is scoped to an elementary rank-two carrier")
    if not _is_positive_definite_2(metric):
        raise ValueError("positive-definite rank-two event metric required")
    if _mm(tau, tau) != I2:
        raise ValueError("tau must be an involution")
    if _mm(_mm(_transpose(tau), metric), tau) != metric:
        raise ValueError("tau must preserve the event metric")
    if _b_adjoint(tau, metric) != tau:
        raise ValueError("tau must be metric-self-adjoint")
    compatibility = _add(_mm(tau_dot, tau), _mm(tau, tau_dot))
    if compatibility != _zero(2):
        raise ValueError("tau_dot must satisfy the differentiated involution identity")

    a = _scale(F(1, 2), _mm(tau_dot, tau))
    if a == _zero(2):
        raise ValueError("stationary exchange frame has no normalized complex generator")
    if _b_adjoint(a, metric) != _scale(F(-1), a):
        raise ValueError("moving-exchange generator must be metric-skew")

    a2 = _mm(a, a)
    radicand = -F(1, 2) * _trace(a2)
    omega = _sqrt_fraction_exact(radicand)
    if omega <= 0:
        raise ValueError("moving exchange frame must have positive angular rate")
    j = _scale(F(1, 1) / omega, a)
    if _mm(j, j) != _scale(F(-1), I2):
        raise ValueError("normalized generator does not square to -I")
    if _b_adjoint(j, metric) != _scale(F(-1), j):
        raise ValueError("normalized generator must be metric-skew")
    if _mm(_mm(_transpose(j), metric), j) != metric:
        raise ValueError("normalized generator must preserve the event metric")

    return {
        "A": a,
        "A2": a2,
        "omega": omega,
        "J": j,
        "radicand": radicand,
        "metric": metric,
    }


def check_T_moving_exchange_formula_exact() -> Dict[str, object]:
    fails: list[str] = []
    samples = (F(-2), F(-1), F(-1, 2), F(0), F(1, 3), F(1), F(2))
    rows = []
    for t in samples:
        tau, tau_dot = _moving_reflection(t)
        try:
            cert = derive_complex_structure(tau, tau_dot)
        except ValueError as exc:
            fails.append(f"t={t}: {exc}")
            continue
        expected_omega = F(2) / (F(1) + t * t)
        if cert["omega"] != expected_omega:
            fails.append(f"t={t}: omega mismatch")
        if cert["J"] != J0:
            fails.append(f"t={t}: normalized J is not the canonical orientation")
        rows.append({
            "t": str(t),
            "tau": _matrix_strings(tau),
            "tau_dot": _matrix_strings(tau_dot),
            "omega": str(cert["omega"]),
            "J": _matrix_strings(cert["J"]),
        })
    return _result(
        "T_moving_exchange_formula_exact",
        "For the exact rational tangent-half-angle family tau(t)=R(t)S0R(t)^T, A=(1/2)tau_dot tau is nonzero skew, omega=sqrt(-(1/2)tr(A^2))=2/(1+t^2), and J=A/omega is exactly the canonical quarter-turn with J^2=-I on every tested rational frame.",
        {
            "formula": "A=(1/2) tau_dot tau; omega=sqrt(-(1/2)tr(A^2)); J=A/omega",
            "sample_count": len(rows),
            "samples": rows,
            "J_squared": _matrix_strings(_mm(J0, J0)),
        },
        fails,
        premises=(
            "positive_rank_two_event_metric",
            "differentiable_nonstationary_operational_exchange",
            "record_neutral_completion_path",
        ),
        negative_controls=(
            "stationary exchange frame",
            "derivative not tangent to tau^2=I",
            "indefinite event metric",
            "higher-rank unequal-frequency frame",
        ),
    )


def check_T_moving_exchange_metric_covariance() -> Dict[str, object]:
    fails: list[str] = []
    t = F(2, 3)
    tau, tau_dot = _moving_reflection(t)
    q: Matrix = ((F(2), F(1)), (F(0), F(3)))
    qi = _inv2(q)
    metric = _mm(_transpose(qi), qi)
    tau_q = _mm(_mm(q, tau), qi)
    tau_dot_q = _mm(_mm(q, tau_dot), qi)
    try:
        cert = derive_complex_structure(tau_q, tau_dot_q, metric)
    except ValueError as exc:
        fails.append(str(exc))
        cert = {"J": _zero(2), "omega": F(0)}
    expected_j = _mm(_mm(q, J0), qi)
    if cert["J"] != expected_j:
        fails.append("conjugated J does not transform covariantly")
    if cert["omega"] != F(18, 13):
        fails.append("omega changed under basis conjugation")
    if not _is_positive_definite_2(metric):
        fails.append("conjugated metric is not positive definite")
    return _result(
        "T_moving_exchange_metric_covariance",
        "The zipper formula is basis-covariant on a non-Euclidean positive plane: simultaneous conjugation of tau and tau_dot with the induced metric sends J to QJQ^{-1} while leaving omega invariant.",
        {
            "Q": _matrix_strings(q),
            "metric": _matrix_strings(metric),
            "tau": _matrix_strings(tau_q),
            "tau_dot": _matrix_strings(tau_dot_q),
            "J": _matrix_strings(cert["J"]),
            "expected_J": _matrix_strings(expected_j),
            "omega": str(cert["omega"]),
        },
        fails,
        dependencies=("T_moving_exchange_formula_exact",),
        premises=("positive_event_metric",),
        negative_controls=("Euclidean-coordinate-only formula",),
    )


def check_T_moving_exchange_orientation_sign() -> Dict[str, object]:
    fails: list[str] = []
    tau, tau_dot = _moving_reflection(F(1, 4))
    pos = derive_complex_structure(tau, _scale(F(7, 3), tau_dot))
    neg = derive_complex_structure(tau, _scale(F(-5, 2), tau_dot))
    if pos["J"] != J0:
        fails.append("positive reparameterization changed orientation")
    if neg["J"] != _scale(F(-1), J0):
        fails.append("negative reparameterization did not reverse orientation")
    if pos["omega"] <= 0 or neg["omega"] <= 0:
        fails.append("omega must be a positive magnitude")
    return _result(
        "T_moving_exchange_orientation_sign",
        "The normalized J is invariant under positive reparameterization speed and flips sign under reversal of the completion-context orientation. The construction therefore fixes complex structure only up to the expected J<->-J orientation choice.",
        {
            "positive_speed_J": _matrix_strings(pos["J"]),
            "negative_speed_J": _matrix_strings(neg["J"]),
            "positive_omega": str(pos["omega"]),
            "negative_omega": str(neg["omega"]),
            "orientation_ambiguity": "J <-> -J",
        },
        fails,
        dependencies=("T_moving_exchange_formula_exact",),
        premises=("oriented_completion_context_parameter",),
        negative_controls=("claim of globally fixed orientation sign",),
    )


def check_T_two_exchange_product_holonomy() -> Dict[str, object]:
    fails: list[str] = []
    t1, t2 = F(0), F(1, 2)
    tau1, _ = _moving_reflection(t1)
    tau2, _ = _moving_reflection(t2)
    hol = _mm(tau2, tau1)
    if _mm(_transpose(hol), hol) != I2:
        fails.append("product of exchanges is not orthogonal")
    if _det2(hol) != 1:
        fails.append("product of exchanges is not orientation preserving")
    if hol == I2:
        fails.append("distinct exchange frames produced trivial holonomy")
    if _mm(hol, J0) != _mm(J0, hol):
        fails.append("orientation-preserving holonomy must commute with J")
    if _mm(tau1, J0) != _scale(F(-1), _mm(J0, tau1)):
        fails.append("first exchange must reverse J")
    if _mm(tau2, J0) != _scale(F(-1), _mm(J0, tau2)):
        fails.append("second exchange must reverse J")
    return _result(
        "T_two_exchange_product_holonomy",
        "Two distinct operational exchange frames are reflections; their product is a nontrivial orientation-preserving rotation that commutes with the normalized J, while each individual exchange anticommutes with J.",
        {
            "tau_1": _matrix_strings(tau1),
            "tau_2": _matrix_strings(tau2),
            "holonomy": _matrix_strings(hol),
            "det_holonomy": str(_det2(hol)),
            "individual_exchanges_reverse_J": True,
            "product_commutes_with_J": True,
        },
        fails,
        dependencies=("T_moving_exchange_formula_exact",),
        premises=("two_distinct_operational_exchange_frames",),
        negative_controls=("fixed exchange frame gives identity holonomy",),
    )


def check_T_zipper_formula_negative_controls() -> Dict[str, object]:
    fails: list[str] = []
    controls: Dict[str, object] = {}

    stationary_rejected = False
    try:
        derive_complex_structure(S0, _zero(2))
    except ValueError as exc:
        stationary_rejected = "stationary" in str(exc)
        controls["stationary_error"] = str(exc)
    if not stationary_rejected:
        fails.append("stationary exchange frame was not rejected")

    bad_derivative_rejected = False
    try:
        derive_complex_structure(S0, I2)
    except ValueError as exc:
        bad_derivative_rejected = "differentiated involution" in str(exc)
        controls["bad_derivative_error"] = str(exc)
    if not bad_derivative_rejected:
        fails.append("incompatible derivative was not rejected")

    tau_ind, td_ind = _moving_indefinite_reflection(F(1, 3))
    a_ind = _scale(F(1, 2), _mm(td_ind, tau_ind))
    rad_ind = -F(1, 2) * _trace(_mm(a_ind, a_ind))
    if rad_ind >= 0:
        fails.append("indefinite control did not produce negative normalization radicand")
    indefinite_rejected = False
    try:
        derive_complex_structure(tau_ind, td_ind, ((F(1), F(0)), (F(0), F(-1))))
    except ValueError as exc:
        indefinite_rejected = "positive-definite" in str(exc)
        controls["indefinite_error"] = str(exc)
    if not indefinite_rejected:
        fails.append("indefinite metric was not rejected")
    controls["indefinite_radicand"] = str(rad_ind)
    controls["indefinite_A_squared"] = _matrix_strings(_mm(a_ind, a_ind))

    a4 = _block_diag(J0, _scale(F(2), J0))
    a4sq = _mm(a4, a4)
    rad4 = -F(1, 2) * _trace(a4sq)
    scalar_identity = _scale(-rad4, _eye(4))
    unequal_frequency_detected = a4sq != scalar_identity
    if not unequal_frequency_detected:
        fails.append("rank-four unequal-frequency scope control did not fire")
    rank_rejected = False
    try:
        derive_complex_structure(_block_diag(S0, S0), _block_diag(_scale(F(2), _mm(J0, S0)), _scale(F(4), _mm(J0, S0))))
    except ValueError as exc:
        rank_rejected = "rank-two" in str(exc)
        controls["rank_four_error"] = str(exc)
    if not rank_rejected:
        fails.append("rank-four carrier was not rejected by scoped constructor")
    controls["rank_four_A_squared"] = _matrix_strings(a4sq)
    controls["rank_four_trace_radicand"] = str(rad4)
    controls["rank_four_A2_not_single_frequency"] = unequal_frequency_detected

    return _result(
        "T_zipper_formula_negative_controls",
        "The formula fails closed for a stationary frame, a derivative not tangent to the involution manifold, an indefinite event metric (boost branch), and a higher-rank unequal-frequency carrier. Positivity, nonstationarity, differentiated involution compatibility, and elementary rank two are all load-bearing.",
        controls,
        fails,
        dependencies=("T_moving_exchange_formula_exact",),
        negative_controls=(
            "stationary tau",
            "tau_dot violating d(tau^2)=0",
            "O(1,1) boost-like moving reflection",
            "rank-four unequal-frequency skew generator",
        ),
    )


PHYSICAL_PREMISES = (
    "ACTIVE_RECORD_KERNEL_REALIZED",
    "COMPLETION_FAITHFUL_RANK_TWO_QUOTIENT",
    "POSITIVE_EVENT_METRIC_REALIZED",
    "SMOOTH_NONSTATIONARY_OPERATIONAL_EXCHANGE_REALIZED",
    "RECORD_NEUTRAL_EXPORT_FREE_COMPLETION_PATH",
)

DEPENDENCY_GRAPH: Dict[str, Tuple[str, ...]] = {
    "ACTIVE_RECORD_KERNEL": (
        "CONTEXT_SENSITIVE_ADMISSIBILITY_EVENT",
        "BOUNDARY_MEDIATED_ENFORCEABILITY",
        "POSITIVE_IRREVERSIBLE_COMMITMENT",
    ),
    "RANK_TWO_EVENT_PLANE": (
        "ACTIVE_RECORD_KERNEL",
        "COMPLETION_FAITHFUL_FIRST_ORDER_QUOTIENT",
    ),
    "POSITIVE_EVENT_METRIC": (
        "CLOSED_LOOP_NONNEGATIVITY",
        "OPERATIONAL_NULL_QUOTIENT",
        "NO_SILENT_LOSS",
    ),
    "MOVING_OPERATIONAL_EXCHANGE": (
        "RANK_TWO_EVENT_PLANE",
        "RELATIONAL_FRAME_VARIABILITY",
        "RECORD_NEUTRAL_EXPORT_FREE_COMPLETION_PATH",
    ),
    "T_ZIPPER_LOCAL_J": (
        "POSITIVE_EVENT_METRIC",
        "MOVING_OPERATIONAL_EXCHANGE",
    ),
}

FORBIDDEN_UPSTREAM = (
    "HILBERT_SPACE",
    "BORN_RULE",
    "COMPLEX_SCALARS",
    "OPERATOR_POSITIVITY",
    "CONNECTED_SO2_IMAGE",
    "QUARTER_TURN_ASSUMED",
)


def _cycle(graph: Mapping[str, Sequence[str]]) -> Optional[Tuple[str, ...]]:
    nodes = set(graph)
    for deps in graph.values():
        nodes.update(deps)
    state: Dict[str, int] = {}
    stack: list[str] = []

    def dfs(n: str) -> Optional[Tuple[str, ...]]:
        state[n] = 1
        stack.append(n)
        for d in graph.get(n, ()):
            if state.get(d, 0) == 0:
                c = dfs(d)
                if c is not None:
                    return c
            elif state.get(d) == 1:
                i = stack.index(d)
                return tuple(stack[i:] + [d])
        stack.pop()
        state[n] = 2
        return None

    for n in sorted(nodes):
        if state.get(n, 0) == 0:
            c = dfs(n)
            if c is not None:
                return c
    return None


def _deps(graph: Mapping[str, Sequence[str]], node: str) -> set[str]:
    out: set[str] = set()
    todo = list(graph.get(node, ()))
    while todo:
        d = todo.pop()
        if d in out:
            continue
        out.add(d)
        todo.extend(graph.get(d, ()))
    return out


def _direct_gate_drift(graph: Mapping[str, Sequence[str]]) -> bool:
    required = {"POSITIVE_EVENT_METRIC", "MOVING_OPERATIONAL_EXCHANGE"}
    return set(graph.get("T_ZIPPER_LOCAL_J", ())) != required


def check_T_zipper_reduction_dependency_contract() -> Dict[str, object]:
    fails: list[str] = []
    cyc = _cycle(DEPENDENCY_GRAPH)
    if cyc is not None:
        fails.append(f"dependency cycle: {cyc}")
    upstream = _deps(DEPENDENCY_GRAPH, "T_ZIPPER_LOCAL_J")
    forbidden_present = sorted(set(FORBIDDEN_UPSTREAM) & upstream)
    if forbidden_present:
        fails.append(f"zipper J illegally consumes downstream structure: {forbidden_present}")
    required_direct = {"POSITIVE_EVENT_METRIC", "MOVING_OPERATIONAL_EXCHANGE"}
    if _direct_gate_drift(DEPENDENCY_GRAPH):
        fails.append("T_ZIPPER_LOCAL_J direct antecedent drift")

    mut_cycle = dict(DEPENDENCY_GRAPH)
    mut_cycle["ACTIVE_RECORD_KERNEL"] = (*mut_cycle["ACTIVE_RECORD_KERNEL"], "T_ZIPPER_LOCAL_J")
    cycle_mutation_caught = _cycle(mut_cycle) is not None
    if not cycle_mutation_caught:
        fails.append("cycle mutation was not caught")

    mut_hilbert = dict(DEPENDENCY_GRAPH)
    mut_hilbert["POSITIVE_EVENT_METRIC"] = (*mut_hilbert["POSITIVE_EVENT_METRIC"], "HILBERT_SPACE")
    hilbert_mutation_caught = "HILBERT_SPACE" in _deps(mut_hilbert, "T_ZIPPER_LOCAL_J")
    if not hilbert_mutation_caught:
        fails.append("Hilbert-smuggling mutation was not caught")

    gate_deletion_caught = True
    for gate in required_direct:
        mut_drop = dict(DEPENDENCY_GRAPH)
        mut_drop["T_ZIPPER_LOCAL_J"] = tuple(
            x for x in mut_drop["T_ZIPPER_LOCAL_J"] if x != gate
        )
        if not _direct_gate_drift(mut_drop):
            gate_deletion_caught = False
            fails.append(f"deletion of {gate} from T_ZIPPER_LOCAL_J not caught")

    mut_extra = dict(DEPENDENCY_GRAPH)
    mut_extra["T_ZIPPER_LOCAL_J"] = (
        *mut_extra["T_ZIPPER_LOCAL_J"],
        "QUARTER_TURN_ASSUMED",
    )
    extra_gate_mutation_caught = _direct_gate_drift(mut_extra)
    if not extra_gate_mutation_caught:
        fails.append("addition of QUARTER_TURN_ASSUMED direct gate not caught")

    return _result(
        "T_zipper_reduction_dependency_contract",
        "The audit-candidate dependency graph is acyclic and keeps the local complex structure downstream only of a positive event metric and a moving operational exchange frame. Hilbert space, Born weighting, complex scalars, operator positivity, a connected SO(2) image, and an assumed quarter-turn are explicitly forbidden upstream.",
        {
            "graph": {k: list(v) for k, v in DEPENDENCY_GRAPH.items()},
            "cycle": cyc,
            "upstream_of_local_J": sorted(upstream),
            "forbidden_upstream": list(FORBIDDEN_UPSTREAM),
            "physical_premises": list(PHYSICAL_PREMISES),
            "cycle_mutation_caught": cycle_mutation_caught,
            "hilbert_smuggling_mutation_caught": hilbert_mutation_caught,
            "direct_gate_deletion_caught": gate_deletion_caught,
            "extra_gate_mutation_caught": extra_gate_mutation_caught,
            "bank_registration": False,
            "audit_status": "candidate_not_banked",
        },
        fails,
        dependencies=tuple(DEPENDENCY_GRAPH),
        premises=PHYSICAL_PREMISES,
        negative_controls=(
            "positivity-orientation dependency cycle",
            "Hilbert-space smuggling",
            "assumed quarter-turn",
            "deleted positive-metric or moving-exchange gate",
        ),
        epistemic="P_structural_instrument",
    )


CHECKS: Dict[str, Callable[[], Dict[str, object]]] = {
    "T_moving_exchange_formula_exact": check_T_moving_exchange_formula_exact,
    "T_moving_exchange_metric_covariance": check_T_moving_exchange_metric_covariance,
    "T_moving_exchange_orientation_sign": check_T_moving_exchange_orientation_sign,
    "T_two_exchange_product_holonomy": check_T_two_exchange_product_holonomy,
    "T_zipper_formula_negative_controls": check_T_zipper_formula_negative_controls,
    "T_zipper_reduction_dependency_contract": check_T_zipper_reduction_dependency_contract,
}


def run_all() -> Dict[str, Dict[str, object]]:
    return {name: fn() for name, fn in CHECKS.items()}


def build_certificate(results: Optional[Mapping[str, Mapping[str, object]]] = None) -> ZipperReductionCertificate:
    rows = dict(results or run_all())

    def ok(name: str) -> bool:
        return bool(rows[name]["passed"])

    controls = rows["T_zipper_formula_negative_controls"]["artifacts"]
    return ZipperReductionCertificate(
        moving_exchange_formula_exact=ok("T_moving_exchange_formula_exact"),
        metric_covariance_exact=ok("T_moving_exchange_metric_covariance"),
        orientation_sign_exact=ok("T_moving_exchange_orientation_sign"),
        reflection_product_holonomy_exact=ok("T_two_exchange_product_holonomy"),
        stationary_frame_rejected="stationary" in str(controls.get("stationary_error", "")),
        derivative_incompatibility_rejected="differentiated involution" in str(controls.get("bad_derivative_error", "")),
        indefinite_signature_rejected="positive-definite" in str(controls.get("indefinite_error", "")),
        rank_two_scope_fenced="rank-two" in str(controls.get("rank_four_error", "")),
        dependency_contract_clean=ok("T_zipper_reduction_dependency_contract"),
        physical_premises_certified=False,
    )


def main() -> int:
    results = run_all()
    certificate = build_certificate(results)
    payload = {
        "name": "APF_Zipper_Reduction_Audit_Candidate_v0.1",
        "family": FAMILY,
        "passed": all(bool(row["passed"]) for row in results.values()),
        "n_checks": len(results),
        "n_passed": sum(bool(row["passed"]) for row in results.values()),
        "certificate": asdict(certificate),
        "claim_boundary": {
            "derived_formula": "J=((1/2) tau_dot tau)/sqrt(-(1/2) tr[((1/2) tau_dot tau)^2])",
            "rank_two_only": True,
            "positive_metric_required": True,
            "stationary_frame_excluded": True,
            "orientation_sign_globalized": False,
            "physical_premises_certified": False,
            "bank_registered": False,
        },
        "checks": list(results.values()),
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
