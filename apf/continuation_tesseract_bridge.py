"""Continuation tesseract -- conditional physical bridge, v0.5.

This module is deliberately non-exporting.  It records the exact scope of the
finite quantum close without allowing the Interface Engine's module-level
closure census to mix the HOC-dependent bridge into the pure mathematical
export.

The named condition package is:

* binary Held Organizational Completeness (HOC);
* compatible joint realization of the two cargo ports;
* record-free common/defect isolation with neutral completion;
* naturality under admissible cargo substitution;
* record-free return to the source continuation type;
* dyadic classical positive control and null padding;
* typed reversal and nonnegative completed physical self-loops.

The identity/exchange-only countermodel proves that current A2 and continuation
preservation do not derive this package.  The downstream difference-completion
and positivity checks are theorem schemas conditional on it.
"""

from __future__ import annotations

from fractions import Fraction as F
from itertools import product
from typing import Callable, Dict, List, Mapping, Sequence, Tuple

Matrix = List[List[F]]
Vector = List[F]

HOC_PACKAGE = (
    "binary_HOC",
    "compatible_joint_realization",
    "record_free_factor_isolation_with_neutral_completion",
    "affine_cargo_naturality",
    "same_type_factor_return",
    "dyadic_classical_positive_control",
    "typed_reversal",
    "nonnegative_physical_completed_self_loops",
)


def _shape(a: Matrix) -> Tuple[int, int]:
    return len(a), len(a[0]) if a else 0

def _eye(n: int) -> Matrix:
    return [[F(1) if i == j else F(0) for j in range(n)] for i in range(n)]

def _add(a: Matrix, b: Matrix) -> Matrix:
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))]
            for i in range(len(a))]

def _sub(a: Matrix, b: Matrix) -> Matrix:
    return [[a[i][j] - b[i][j] for j in range(len(a[0]))]
            for i in range(len(a))]

def _scal(s: F, a: Matrix) -> Matrix:
    return [[s * x for x in row] for row in a]

def _mm(a: Matrix, b: Matrix) -> Matrix:
    ar, ac = _shape(a)
    br, bc = _shape(b)
    if ac != br:
        raise ValueError("matrix shape mismatch")
    return [[sum(a[i][k] * b[k][j] for k in range(ac))
             for j in range(bc)] for i in range(ar)]

def _transpose(a: Matrix) -> Matrix:
    return [[a[i][j] for i in range(len(a))] for j in range(len(a[0]))]

def _eq(a: Matrix, b: Matrix) -> bool:
    return _shape(a) == _shape(b) and all(
        a[i][j] == b[i][j]
        for i in range(len(a)) for j in range(len(a[0]))
    )

def _vec_eq(a: Vector, b: Vector) -> bool:
    return len(a) == len(b) and all(x == y for x, y in zip(a, b))

def _quadratic(g: Matrix, v: Vector) -> F:
    return sum(v[i] * g[i][j] * v[j]
               for i in range(len(v)) for j in range(len(v)))

def _principal_2(g: Matrix, i: int, j: int) -> Matrix:
    return [[g[i][i], g[i][j]], [g[j][i], g[j][j]]]

def _det2(a: Matrix) -> F:
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]

def _result(name: str, epistemic: str, key_result: str,
            dependencies: Sequence[str], artifacts: Mapping[str, object],
            fails: Sequence[str]) -> Dict[str, object]:
    return {
        "name": name,
        "epistemic": epistemic,
        "tier": 4,
        "passed": not fails,
        "key_result": key_result,
        "dependencies": list(dependencies),
        "cross_refs": [],
        "artifacts": dict(artifacts),
        "fail_reasons": list(fails),
    }



def check_T_HOC_quantum_close_scope_contract():
    fails: List[str] = []

    def ck(cond: bool, msg: str) -> None:
        if not cond:
            fails.append(msg)

    i2 = _eye(2)
    p = [[F(0), F(1)], [F(1), F(0)]]
    e_plus = _scal(F(1, 2), _add(i2, p))
    e_minus = _scal(F(1, 2), _sub(i2, p))
    physical_monoid = [i2, p]

    ck(_eq(_mm(p, p), i2), "record-free exchange is an involution")
    ck(not any(_eq(e_plus, m) for m in physical_monoid),
       "identity/exchange carrier lacks the common character idempotent")
    ck(not any(_eq(e_minus, m) for m in physical_monoid),
       "identity/exchange carrier lacks the defect character idempotent")
    ck(all(not _eq(_mm(m, m), m) or _eq(m, i2) for m in physical_monoid),
       "identity/exchange carrier has no nontrivial physical idempotent")
    ck(len(HOC_PACKAGE) == len(set(HOC_PACKAGE)) == 8,
       "the conditional close has eight distinct named obligations")

    return _result(
        "T_HOC_quantum_close_scope_contract",
        "P_structural_instrument",
        ("Scope contract: current continuation preservation may carry exchange "
         "without carrying its common/defect idempotents. The finite quantum "
         "close is therefore conditional on the named binary HOC package; this "
         "check records the package and proves the independence countermodel, "
         "but neither adopts nor derives the physical clause."),
        [],
        {
            "physical_monoid": ["I", "P"],
            "common_idempotent_present": False,
            "defect_idempotent_present": False,
            "conditional_on": list(HOC_PACKAGE),
            "HOC_adopted_by_this_check": False,
            "HOC_derived_by_this_check": False,
        },
        fails,
    )


def check_L_tie_through_zero_defect_germ():
    fails: List[str] = []

    def ck(cond: bool, msg: str) -> None:
        if not cond:
            fails.append(msg)

    # gamma_+(t)=t and gamma_-(t)=-t.
    value_plus = F(0)
    value_minus = F(0)
    deriv_plus = F(1)
    deriv_minus = F(-1)
    later_t = F(1, 3)
    later_plus = later_t
    later_minus = -later_t

    ck(value_plus == value_minus == 0, "exact present tie")
    ck(deriv_plus != deriv_minus, "opposite continuation direction")
    ck(later_plus != later_minus, "later non-null continuation witness")

    # Higher-order fence: h_+(t)=t^2, h_-(t)=-t^2 share value and first
    # derivative but differ later.
    h_value_plus = h_value_minus = F(0)
    h_deriv_plus = h_deriv_minus = F(0)
    h_later_plus = later_t * later_t
    h_later_minus = -h_later_plus
    ck(h_value_plus == h_value_minus and h_deriv_plus == h_deriv_minus,
       "higher-order pair shares first jet")
    ck(h_later_plus != h_later_minus,
       "higher-order pair remains continuation-distinct")

    return _result(
        "L_tie_through_zero_defect_germ",
        "P_math",
        ("An exact present tie d=0 can retain a non-null continuation defect "
         "d_dot!=0. The t^2/-t^2 control shows that rank four is sufficient only "
         "in an operationally first-order complete regime."),
        [],
        {
            "first_order_witness": ["t", "-t"],
            "higher_order_fence": ["t^2", "-t^2"],
            "coherence_reading": "conditional on operational first-order completeness",
            "named_condition": "operational_first_order_completeness",
        },
        fails,
    )


def _dyadic_mixture_decomposition(v: Vector) -> Tuple[F, Vector, Vector]:
    positive = [max(x, F(0)) for x in v]
    negative = [max(-x, F(0)) for x in v]
    s_pos = sum(positive)
    s_neg = sum(negative)
    bound = max(s_pos, s_neg)
    if bound == 0:
        return F(1), [F(0) for _ in v], [F(0) for _ in v]
    # Choose a power-of-two normalization.  For dyadic v this keeps every
    # mixture weight dyadic and makes it realizable by repeated fair binary
    # classical control plus null padding.
    lam = F(1)
    while lam < bound:
        lam *= 2
    x = [a / lam for a in positive]
    y = [a / lam for a in negative]
    # The missing weight 1-sum(x) or 1-sum(y) is assigned to the physical null
    # branch and therefore does not appear in the represented vector.
    return lam, x, y


def check_T_dyadic_defect_difference_completion():
    fails: List[str] = []

    def ck(cond: bool, msg: str) -> None:
        if not cond:
            fails.append(msg)

    tested = 0
    for nums in product(range(-2, 3), repeat=4):
        for den in (1, 2, 4, 8):
            v = [F(n, den) for n in nums]
            lam, x, y = _dyadic_mixture_decomposition(v)
            ck(all(a >= 0 for a in x+y), "mixture weights nonnegative")
            ck(sum(x) <= 1 and sum(y) <= 1,
               "null-padded inputs are convex mixtures")
            # Decoded defect first port is (x-y)/2.
            out = [(a-b)/2 for a, b in zip(x, y)]
            target = [a / (2*lam) if any(v) else F(0) for a in v]
            ck(_vec_eq(out, target), "decoded defect realizes dyadic ray")
            tested += 1

    # Loud no-smuggling control: x and y are individually positive mixtures;
    # their signed difference appears only after applying E_defect.
    v = [F(2, 3), F(-1, 5), F(0), F(7, 11)]
    lam, x, y = _dyadic_mixture_decomposition(v)
    ck(all(a >= 0 for a in x+y), "control inputs are ordinary positive mixtures")
    ck(_vec_eq([(a-b)/2 for a, b in zip(x, y)],
               [a/(2*lam) for a in v]),
       "the only signed step is the physical defect projector")

    return _result(
        "T_dyadic_defect_difference_completion",
        "P_math",
        ("Every dyadic represented ray is obtained from two ordinary dyadic "
         "convex mixtures x,y and one decoded physical defect projector: the "
         "first return port is (x-y)/2. Classical control supplies only x and y; "
         "the zipper supplies the sign. Unknown A,D calibrations cancel."),
        ["T_HOC_quantum_close_scope_contract", "T_decoded_common_defect_projectors"],
        {
            "vectors_tested": tested,
            "coefficient_range": "numerators -2..2, denominators 1,2,4,8, dimension 4",
            "arbitrary_signed_classical_control_assumed": False,
            "balanced_splitter_assumed": False,
            "conditional_on": list(HOC_PACKAGE),
        },
        fails,
    )


def check_T_minimal_competition_signed_loop_positivity():
    fails: List[str] = []

    def ck(cond: bool, msg: str) -> None:
        if not cond:
            fails.append(msg)

    # Pairwise insufficiency: every 2x2 principal block is positive definite,
    # while the global all-ones direction is negative.
    g_bad = [
        [F(1), F(-3, 4), F(-3, 4)],
        [F(-3, 4), F(1), F(-3, 4)],
        [F(-3, 4), F(-3, 4), F(1)],
    ]
    for i, j in ((0, 1), (0, 2), (1, 2)):
        block = _principal_2(g_bad, i, j)
        ck(block[0][0] > 0 and _det2(block) > 0,
           "each binary principal restriction positive definite")
    one = [F(1), F(1), F(1)]
    q_bad = _quadratic(g_bad, one)
    ck(q_bad == F(-3, 2), "global three-way loop score negative")

    lam, x, y = _dyadic_mixture_decomposition(one)
    synthesized = [(a-b)/2 for a, b in zip(x, y)]
    scale = F(1, 2) / lam
    ck(_vec_eq(synthesized, [scale*a for a in one]),
       "negative eigendirection is physically synthesized up to nonzero scale")
    ck(_quadratic(g_bad, synthesized) == scale*scale*q_bad < 0,
       "non-PSD Gram form violates physical LOOP+ on the synthesized ray")

    # Positive control with exact L^T L certificate.
    l = [
        [F(1), F(0), F(0)],
        [F(1), F(1), F(0)],
        [F(0), F(1), F(1)],
    ]
    g_pos = _mm(_transpose(l), l)
    for v in product(range(-2, 3), repeat=3):
        vf = [F(a) for a in v]
        ck(_quadratic(g_pos, vf) >= 0, "L^T L positive control")

    return _result(
        "T_minimal_competition_signed_loop_positivity",
        "P_structural_reading",
        ("HOC plus decoded dyadic difference completion makes every dyadic "
         "represented ray physical. LOOP+ then gives q(v)>=0 on a dense dyadic "
         "set; finite-dimensional bilinearity supplies continuity, so every "
         "completed Gram form is PSD. The 3x3 pairwise-positive counterexample "
         "is caught on (1,1,1)."),
        ["T_HOC_quantum_close_scope_contract",
         "T_dyadic_defect_difference_completion"],
        {
            "pairwise_counterexample_q_111": str(q_bad),
            "pairwise_principal_determinant": str(F(7, 16)),
            "positive_control": "G=L^T L exact Fraction certificate",
            "continuity_source": "finite-dimensional bilinear loop form",
            "conditional_on": list(HOC_PACKAGE),
        },
        fails,
    )


_CHECKS: Dict[str, Callable[[], Dict[str, object]]] = {
    "T_HOC_quantum_close_scope_contract": check_T_HOC_quantum_close_scope_contract,
    "L_tie_through_zero_defect_germ": check_L_tie_through_zero_defect_germ,
    "T_dyadic_defect_difference_completion": check_T_dyadic_defect_difference_completion,
    "T_minimal_competition_signed_loop_positivity": check_T_minimal_competition_signed_loop_positivity,
}


def register(registry: Dict[str, object]) -> Dict[str, object]:
    registry.update(_CHECKS)
    return registry


def run_all() -> Dict[str, Dict[str, object]]:
    return {name: fn() for name, fn in _CHECKS.items()}


IE_DECLARATIONS = (
    {
        "input_id": "quantum:held_organizational_completeness_bridge",
        "axis": "ROUTE",
        "route": "held_organizational_completeness",
        "expect_export": False,
        "payload": {
            "name": "HOC_quantum_close_scope_contract",
            "closure_kind": "obstruction_named",
            "obstruction_class": "HOC_REQUIRED_FOR_PHYSICAL_IDEMPOTENT_SPLITTING",
            "source_check": "T_HOC_quantum_close_scope_contract",
            "conditional_close_checks": [
                "T_dyadic_defect_difference_completion",
                "T_minimal_competition_signed_loop_positivity",
            ],
            "open_obligations": list(HOC_PACKAGE),
            "knockout_summary": (
                "Current continuation preservation can carry exchange P without "
                "physically carrying its character idempotents. The signed-loop "
                "and finite-quantum close therefore remain conditional on the "
                "binary HOC package recorded by the scope contract."
            ),
            "target_value_consumed": False,
        },
        "note": (
            "Self-certifying closure row: the identity/exchange-only countermodel "
            "proves the physical bridge is additional content."
        ),
    },
)


if __name__ == "__main__":
    import json
    results = run_all()
    print(json.dumps({
        "module": "continuation_tesseract_bridge_v0_5",
        "check_count": len(results),
        "checks": {name: ("PASS" if r["passed"] else "FAIL")
                   for name, r in results.items()},
        "all_pass": all(r["passed"] for r in results.values()),
        "conditional_on": list(HOC_PACKAGE),
    }, indent=2, sort_keys=True))
