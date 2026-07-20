"""Continuation tesseract -- exact finite symmetry mathematics, v0.5.

This module contains only the pure finite mathematics of the Continuation
Tesseract program.  It carries no HOC premise, no physical positivity bridge,
and no complex-orientation claim.

The module proves the binary exchange character algebra, the general
calibration-free zipper form, exact decoded projectors, the four-character
first-order carrier, an exact real root of contender exchange on that typed
carrier, and the integral parity shadow.

The physical admission of factor isolation, same-type return, the tie-through-
zero interpretation, and signed-loop positivity lives in
``apf.continuation_tesseract_bridge`` and remains explicitly conditional.
"""

from __future__ import annotations

from fractions import Fraction as F
from itertools import product
from typing import Callable, Dict, List, Mapping, Sequence, Tuple

Matrix = List[List[F]]
Vector = List[F]
Gaussian = Tuple[F, F]
GMatrix = List[List[Gaussian]]


def _zero(r: int, c: int) -> Matrix:
    return [[F(0) for _ in range(c)] for _ in range(r)]

def _eye(n: int) -> Matrix:
    return [[F(1) if i == j else F(0) for j in range(n)] for i in range(n)]

def _shape(a: Matrix) -> Tuple[int, int]:
    return len(a), len(a[0]) if a else 0

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

def _mv(a: Matrix, v: Vector) -> Vector:
    if len(a[0]) != len(v):
        raise ValueError("matrix/vector shape mismatch")
    return [sum(a[i][j] * v[j] for j in range(len(v)))
            for i in range(len(a))]

def _transpose(a: Matrix) -> Matrix:
    return [[a[i][j] for i in range(len(a))] for j in range(len(a[0]))]

def _eq(a: Matrix, b: Matrix) -> bool:
    return _shape(a) == _shape(b) and all(
        a[i][j] == b[i][j]
        for i in range(len(a)) for j in range(len(a[0]))
    )

def _vec_eq(a: Vector, b: Vector) -> bool:
    return len(a) == len(b) and all(x == y for x, y in zip(a, b))

def _block(a: Matrix, b: Matrix, c: Matrix, d: Matrix) -> Matrix:
    if len(a) != len(b) or len(c) != len(d):
        raise ValueError("block row mismatch")
    if len(a[0]) != len(c[0]) or len(b[0]) != len(d[0]):
        raise ValueError("block column mismatch")
    return [a[i] + b[i] for i in range(len(a))] + [
        c[i] + d[i] for i in range(len(c))
    ]

def _diag(entries: Sequence[F]) -> Matrix:
    n = len(entries)
    return [[entries[i] if i == j else F(0) for j in range(n)]
            for i in range(n)]

def _trace(a: Matrix) -> F:
    return sum(a[i][i] for i in range(min(len(a), len(a[0]))))

def _inverse(a: Matrix) -> Matrix:
    n, m = _shape(a)
    if n != m:
        raise ValueError("inverse requires square matrix")
    aug = [row[:] + eye_row[:] for row, eye_row in zip(a, _eye(n))]
    for col in range(n):
        pivot = next((r for r in range(col, n) if aug[r][col] != 0), None)
        if pivot is None:
            raise ValueError("singular matrix")
        if pivot != col:
            aug[col], aug[pivot] = aug[pivot], aug[col]
        p = aug[col][col]
        aug[col] = [x / p for x in aug[col]]
        for r in range(n):
            if r == col:
                continue
            q = aug[r][col]
            if q != 0:
                aug[r] = [aug[r][j] - q * aug[col][j]
                          for j in range(2 * n)]
    return [row[n:] for row in aug]

def _outer(v: Vector, w: Vector) -> Matrix:
    return [[x * y for y in w] for x in v]

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

def _zipper(a: Matrix, d: Matrix) -> Matrix:
    return _block(a, a, d, _scal(F(-1), d))

def _zipper_inverse(a: Matrix, d: Matrix) -> Matrix:
    ai = _inverse(a)
    di = _inverse(d)
    return _scal(F(1, 2), _block(ai, di, ai, _scal(F(-1), di)))

def _exchange(n: int) -> Matrix:
    i = _eye(n)
    z = _zero(n, n)
    return _block(z, i, i, z)

def _factor_parity(n: int) -> Matrix:
    i = _eye(n)
    z = _zero(n, n)
    return _block(i, z, z, _scal(F(-1), i))


def _det3(a: Matrix) -> F:
    return (
        a[0][0] * (a[1][1] * a[2][2] - a[1][2] * a[2][1])
        - a[0][1] * (a[1][0] * a[2][2] - a[1][2] * a[2][0])
        + a[0][2] * (a[1][0] * a[2][1] - a[1][1] * a[2][0])
    )

def _gadd(x: Gaussian, y: Gaussian) -> Gaussian:
    return x[0] + y[0], x[1] + y[1]

def _gmul(x: Gaussian, y: Gaussian) -> Gaussian:
    return x[0] * y[0] - x[1] * y[1], x[0] * y[1] + x[1] * y[0]

def _gconj(x: Gaussian) -> Gaussian:
    return x[0], -x[1]

def _gmm(a: GMatrix, b: GMatrix) -> GMatrix:
    return [[
        _gadd(_gmul(a[i][0], b[0][j]), _gmul(a[i][1], b[1][j]))
        for j in range(2)
    ] for i in range(2)]

def _gdag(a: GMatrix) -> GMatrix:
    return [[_gconj(a[j][i]) for j in range(2)] for i in range(2)]


def check_T_binary_exchange_character_idempotents():
    fails: List[str] = []

    def ck(cond: bool, msg: str) -> None:
        if not cond:
            fails.append(msg)

    i2 = _eye(2)
    z2 = _zero(2, 2)
    p = [[F(0), F(1)], [F(1), F(0)]]
    e_plus = _scal(F(1, 2), _add(i2, p))
    e_minus = _scal(F(1, 2), _sub(i2, p))

    ck(_eq(_mm(e_plus, e_plus), e_plus), "E+ idempotent")
    ck(_eq(_mm(e_minus, e_minus), e_minus), "E- idempotent")
    ck(_eq(_mm(e_plus, e_minus), z2), "E+E-=0")
    ck(_eq(_mm(e_minus, e_plus), z2), "E-E+=0")
    ck(_eq(_add(e_plus, e_minus), i2), "E++E-=I")
    ck(_vec_eq(_mv(e_plus, [F(3), F(1)]), [F(2), F(2)]),
       "E+ extracts half-sum pair")
    ck(_vec_eq(_mv(e_minus, [F(3), F(1)]), [F(1), F(-1)]),
       "E- extracts half-difference pair")

    return _result(
        "T_binary_exchange_character_idempotents",
        "P_math",
        ("The exchange involution has the complementary central idempotents "
         "E+=(I+P)/2 and E-=(I-P)/2. Their images are the common and defect "
         "roles. The theorem is algebraic; HOC is the physical splitting claim."),
        [],
        {
            "E_common": [[str(x) for x in row] for row in e_plus],
            "E_defect": [[str(x) for x in row] for row in e_minus],
            "metric_used": False,
        },
        fails,
    )


def check_T_calibration_free_competition_zipper():
    fails: List[str] = []

    def ck(cond: bool, msg: str) -> None:
        if not cond:
            fails.append(msg)

    calibrations = [
        (
            [[F(1), F(1)], [F(0), F(1)]],
            [[F(2), F(0)], [F(1), F(1)]],
        ),
        (
            [[F(3), F(-1)], [F(1), F(1)]],
            [[F(1), F(2)], [F(-1), F(3)]],
        ),
    ]
    p = _exchange(2)
    s = _factor_parity(2)
    i4 = _eye(4)

    for idx, (a, d) in enumerate(calibrations):
        xi = _zipper(a, d)
        xi_inv = _zipper_inverse(a, d)
        ck(_eq(_mm(xi, p), _mm(s, xi)), f"zipper {idx}: XiP=SXi")
        ck(_eq(_mm(xi_inv, xi), i4), f"zipper {idx}: left inverse")
        ck(_eq(_mm(xi, xi_inv), i4), f"zipper {idx}: right inverse")

    # Exact block-equation identity for symbolic blocks represented by distinct
    # scalar placeholders r,t,u,w.
    r, t, u, w = F(2), F(3), F(5), F(7)
    x = [[r, t], [u, w]]
    p1 = [[F(0), F(1)], [F(1), F(0)]]
    s1 = [[F(1), F(0)], [F(0), F(-1)]]
    residual = _sub(_mm(x, p1), _mm(s1, x))
    expected = [[t-r, r-t], [w+u, u+w]]
    ck(_eq(residual, expected), "general block residual exact")
    ck(not _eq(residual, _zero(2, 2)),
       "generic non-zipped block must fail covariance")

    return _result(
        "T_calibration_free_competition_zipper",
        "P_math",
        ("Exchange covariance forces Xi(a,b)=(A(a+b),D(a-b)). If Xi is "
         "lossless, A and D are invertible. Exchange fixes signs but not equal "
         "calibration, orthogonality, a norm, or reciprocity."),
        [],
        {
            "calibration_pairs_checked": len(calibrations),
            "equal_calibration_required": False,
            "metric_used": False,
        },
        fails,
    )


def check_T_decoded_common_defect_projectors():
    fails: List[str] = []

    def ck(cond: bool, msg: str) -> None:
        if not cond:
            fails.append(msg)

    n = 2
    i = _eye(n)
    z = _zero(n, n)
    p = _exchange(n)
    e_plus = _scal(F(1, 2), _add(_eye(2*n), p))
    e_minus = _scal(F(1, 2), _sub(_eye(2*n), p))
    q_common = _block(i, z, z, z)
    q_defect = _block(z, z, z, i)

    calibrations = [
        (
            [[F(1), F(1)], [F(0), F(1)]],
            [[F(2), F(0)], [F(1), F(1)]],
        ),
        (
            [[F(3), F(-1)], [F(1), F(1)]],
            [[F(1), F(2)], [F(-1), F(3)]],
        ),
        (
            [[F(2), F(1)], [F(1), F(2)]],
            [[F(4), F(-1)], [F(1), F(1)]],
        ),
    ]

    decoded = []
    for idx, (a, d) in enumerate(calibrations):
        xi = _zipper(a, d)
        xi_inv = _zipper_inverse(a, d)
        ec = _mm(_mm(xi_inv, q_common), xi)
        ed = _mm(_mm(xi_inv, q_defect), xi)
        ck(_eq(ec, e_plus), f"calibration {idx}: decoded common is E+")
        ck(_eq(ed, e_minus), f"calibration {idx}: decoded defect is E-")
        decoded.append((ec, ed))

        for a0, b0 in [
            ([F(1), F(0)], [F(0), F(1)]),
            ([F(3), F(-2)], [F(1), F(4)]),
            ([F(-5), F(7)], [F(2), F(-3)]),
        ]:
            inp = a0 + b0
            common = _mv(ec, inp)
            defect = _mv(ed, inp)
            half_sum = [(x+y)/2 for x, y in zip(a0, b0)]
            half_diff = [(x-y)/2 for x, y in zip(a0, b0)]
            ck(_vec_eq(common, half_sum + half_sum),
               "decoded common output is two copies of half-sum")
            ck(_vec_eq(defect, half_diff + [-x for x in half_diff]),
               "decoded defect output is half-difference and its reverse")

    return _result(
        "T_decoded_common_defect_projectors",
        "P_math",
        ("For every invertible exchange-natural zipper, physical factor-port "
         "selection followed by unzipping cancels A and D exactly: "
         "Xi^-1 Q_common Xi=(I+P)/2 and Xi^-1 Q_defect Xi=(I-P)/2. "
         "The common and defect projectors are therefore calibration-free."),
        [],
        {
            "calibration_pairs_checked": len(decoded),
            "decoded_common": "(a+b)/2 in both return ports",
            "decoded_defect": "(a-b)/2 and (b-a)/2",
            "balanced_splitter_assumed": False,
        },
        fails,
    )


def check_T_klein_four_continuation_tesseract():
    fails: List[str] = []

    def ck(cond: bool, msg: str) -> None:
        if not cond:
            fails.append(msg)

    i4 = _eye(4)
    z4 = _zero(4, 4)
    sigma = _diag([F(1), F(-1), F(1), F(-1)])
    tau = _diag([F(1), F(1), F(-1), F(-1)])
    ck(_eq(_mm(sigma, sigma), i4), "sigma involution")
    ck(_eq(_mm(tau, tau), i4), "tau involution")
    ck(_eq(_mm(sigma, tau), _mm(tau, sigma)), "sigma,tau commute")

    projectors: Dict[str, Matrix] = {}
    for eps, eta in product((F(1), F(-1)), repeat=2):
        e = _scal(F(1, 4), _mm(_add(i4, _scal(eps, sigma)),
                                 _add(i4, _scal(eta, tau))))
        key = f"({int(eps):+d},{int(eta):+d})"
        projectors[key] = e
        ck(_eq(_mm(e, e), e), f"{key} idempotent")
        ck(_trace(e) == 1, f"{key} scalar rank-one trace")

    total = z4
    keys = list(projectors)
    for key in keys:
        total = _add(total, projectors[key])
    ck(_eq(total, i4), "four projectors sum to identity")
    for i, key_i in enumerate(keys):
        for j, key_j in enumerate(keys):
            if i != j:
                ck(_eq(_mm(projectors[key_i], projectors[key_j]), z4),
                   f"{key_i}{key_j}=0")

    # Metric non-uniqueness control. The same involutions preserve many positive
    # diagonal forms and are also compatible with an indefinite diagonal form.
    g1 = _diag([F(1), F(2), F(3), F(4)])
    g2 = _diag([F(4), F(3), F(2), F(1)])
    g_bad = _diag([F(1), F(1), F(1), F(-1)])
    for g, label in ((g1, "g1"), (g2, "g2"), (g_bad, "g_bad")):
        ck(_eq(_mm(_mm(_transpose(sigma), g), sigma), g),
           f"sigma preserves {label}")
        ck(_eq(_mm(_mm(_transpose(tau), g), tau), g),
           f"tau preserves {label}")
    ck(g_bad[3][3] < 0, "indefinite compatible form control")

    return _result(
        "T_klein_four_continuation_tesseract",
        "P_math",
        ("Contender exchange and germ reversal generate Z2 x Z2. Their four "
         "joint character projectors are (I+/-sigma)(I+/-tau)/4, corresponding "
         "to c, d, c_dot, d_dot. For scalar cargo the local real rank is four. "
         "The symmetry algebra does not choose a positive metric."),
        [],
        {
            "coordinate_order": ["c", "d", "c_dot", "d_dot"],
            "character_projectors": list(projectors),
            "real_rank_scalar": 4,
            "metric_nonuniqueness_control": True,
        },
        fails,
    )


def check_T_quantum_zipper_root_of_exchange():
    fails: List[str] = []

    def ck(cond: bool, msg: str) -> None:
        if not cond:
            fails.append(msg)

    p = [[F(0), F(1)], [F(1), F(0)]]
    ck(_det2(p) == F(-1), 'scalar branch exchange has determinant -1')
    # If R^2=P over R, det(R)^2=-1. No real R exists.

    sigma = _diag([F(1), F(-1), F(1), F(-1)])
    tau = _diag([F(1), F(1), F(-1), F(-1)])
    z = [
        [F(1), F(0), F(0), F(0)],
        [F(0), F(0), F(0), F(-1)],
        [F(0), F(0), F(1), F(0)],
        [F(0), F(1), F(0), F(0)],
    ]
    i4 = _eye(4)
    z2 = _mm(z, z)
    z3 = _mm(z2, z)
    z4 = _mm(z2, z2)
    ck(_eq(z2, sigma), 'typed zipper squares to contender exchange')
    ck(_eq(z4, i4), 'typed zipper has order four')
    ck(_eq(_mm(_mm(tau, z), tau), z3), 'germ reversal conjugates Z to Z^-1')

    j_cont = [
        [F(0), F(0), F(-1), F(0)],
        [F(0), F(0), F(0), F(-1)],
        [F(1), F(0), F(0), F(0)],
        [F(0), F(1), F(0), F(0)],
    ]
    ck(_eq(_mm(j_cont, j_cont), _scal(F(-1), i4)), 'J_cont^2=-I')
    ck(_eq(_mm(z, j_cont), _mm(j_cont, z)), 'Z commutes with continuation orientation')

    # A rank-three untyped extension also admits a real root. Rank four is a
    # typed first-order completeness statement, not abstract minimality.
    sigma3 = _diag([F(1), F(-1), F(-1)])
    z_rank3 = [
        [F(1), F(0), F(0)],
        [F(0), F(0), F(-1)],
        [F(0), F(1), F(0)],
    ]
    ck(_eq(_mm(z_rank3, z_rank3), sigma3), 'rank-three untyped control exists')
    ck(_det3(sigma3) == F(1), 'paired negative directions remove determinant obstruction')

    # The defect moves through an exact present tie.
    for c, d in ((F(2), F(3)), (F(-5), F(7)), (F(1, 3), F(-2, 5))):
        x = [c, d, F(0), F(0)]
        zx = _mv(z, x)
        z2x = _mv(z2, x)
        ck(_vec_eq(zx, [c, F(0), F(0), d]), 'one root step moves d to d_dot')
        ck(_vec_eq(z2x, [c, -d, F(0), F(0)]), 'two root steps exchange contenders')

    # Exact Gaussian-rational branch representation after complex orientation.
    one = F(1)
    half = F(1, 2)
    zero_g: Gaussian = (F(0), F(0))
    one_g: Gaussian = (one, F(0))
    r_branch: GMatrix = [
        [(half, half), (half, -half)],
        [(half, -half), (half, half)],
    ]
    p_g: GMatrix = [[zero_g, one_g], [one_g, zero_g]]
    i_g: GMatrix = [[one_g, zero_g], [zero_g, one_g]]
    ck(_gmm(r_branch, r_branch) == p_g, 'complex branch root squares to exchange')
    ck(_gmm(_gdag(r_branch), r_branch) == i_g,
       'after positive orientation the canonical branch root is unitary')

    return _result(
        'T_quantum_zipper_root_of_exchange',
        'P_math',
        ('Scalar real branch exchange has no real square root because det(P)=-1. '
         'The typed four-character carrier pairs the two exchange-odd sectors and '
         'admits the exact real root Z with Z^2=sigma, Z^4=I, and tau Z tau=Z^-1. '
         'One step sends present defect into continuation defect. This root is not '
         'used in the positivity proof; its physical admission needs a Held '
         'defect-to-direction midpoint gate or the downstream coherent orientation.'),
        ['T_klein_four_continuation_tesseract'],
        {
            'det_scalar_exchange': '-1',
            'relations': ['Z^2=sigma', 'Z^4=I', 'tau Z tau=Z^-1', '[Z,J_cont]=0'],
            'rank3_untyped_control': True,
            'typed_rank_claim': 'four only when c,d,c_dot,d_dot are consequential',
            'branch_root_after_orientation': '1/2[[1+i,1-i],[1-i,1+i]]',
            'physicality_gate': 'Held defect-to-direction midpoint or downstream coherent orientation',
            'consumed_by_positivity': False,
        },
        fails,
    )


def check_T_quantum_zipper_parity_shadow():
    fails: List[str] = []

    def ck(cond: bool, msg: str) -> None:
        if not cond:
            fails.append(msg)

    tested = 0
    for d in range(-9, 10):
        for d_dot in range(-9, 10):
            z_d, z_d_dot = -d_dot, d
            before = (d % 2, d_dot % 2)
            after = (z_d % 2, z_d_dot % 2)
            ck(after == (before[1], before[0]), 'Z swaps parity coordinates')
            ck((sum(before) % 2) == (sum(after) % 2),
               'total defect parity is conserved')
            tested += 1

    cycle = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    for d, d_dot in cycle:
        ck((d % 2) + (d_dot % 2) == 1,
           'cardinal zipper cycle carries one odd defect unit')
    for d_dot in range(-9, 10):
        if d_dot % 2 == 1:
            ck((0 % 2) + (d_dot % 2) == 1,
               'at a tie, odd total parity sits in continuation defect')

    return _result(
        'T_quantum_zipper_parity_shadow',
        'P_math',
        ('On the integral defect lattice Z(d,d_dot)=(-d_dot,d). Modulo two the '
         'sign disappears, so Z swaps present-defect and continuation-defect '
         'parity while conserving their sum. In the odd sector, d=0 forces the '
         'parity defect into d_dot. Identifying a physical residual ledger sector '
         'with d_dot remains a separate residual-direction premise.'),
        ['T_quantum_zipper_root_of_exchange'],
        {
            'lattice_points_tested': tested,
            'cardinal_cycle': cycle,
            'conserved_mod2_quantity': '[d]_2 + [d_dot]_2',
            'physical_identification_gate': 'residual_direction_identification',
            'winner_selected': False,
        },
        fails,
    )


_CHECKS: Dict[str, Callable[[], Dict[str, object]]] = {
    "T_binary_exchange_character_idempotents": check_T_binary_exchange_character_idempotents,
    "T_calibration_free_competition_zipper": check_T_calibration_free_competition_zipper,
    "T_decoded_common_defect_projectors": check_T_decoded_common_defect_projectors,
    "T_klein_four_continuation_tesseract": check_T_klein_four_continuation_tesseract,
    "T_quantum_zipper_root_of_exchange": check_T_quantum_zipper_root_of_exchange,
    "T_quantum_zipper_parity_shadow": check_T_quantum_zipper_parity_shadow,
}


def register(registry: Dict[str, object]) -> Dict[str, object]:
    registry.update(_CHECKS)
    return registry


def run_all() -> Dict[str, Dict[str, object]]:
    return {name: fn() for name, fn in _CHECKS.items()}


IE_DECLARATIONS = (
    {
        "input_id": "quantum:continuation_tesseract_exact_math_v0_5",
        "axis": "ROUTE",
        "route": "continuation_tesseract_exact_math",
        "expect_export": True,
        "payload": {
            "name": "continuation_tesseract_exact_math_v0_5",
            "closure_kind": "internal_identity",
            "source_checks": list(_CHECKS),
            "identity_summary": (
                "Exact Z2 character idempotents; calibration-free zipper and "
                "decoded projectors; Klein-four first-order carrier; exact real "
                "root of exchange; and the integral parity shadow."
            ),
        },
        "note": (
            "Pure finite mathematics. The HOC and physical midpoint bridges live "
            "in a separate non-exporting module."
        ),
    },
    {
        "input_id": "quantum:zipper_root_physicality_gate",
        "axis": "ROUTE",
        "route": "zipper_root_of_exchange",
        "expect_export": False,
        "payload": {
            "name": "zipper_root_physicality_gate",
            "closure_kind": "obstruction_named",
            "obstruction_class": "HELD_DEFECT_TO_DIRECTION_MIDPOINT_REQUIRED",
            "source_check": "T_quantum_zipper_root_of_exchange",
            "open_obligations": [
                "admitted_record_free_defect_to_direction_continuation",
                "or_downstream_coherent_orientation",
                "residual_direction_identification_for_physical_parity_reading",
            ],
            "knockout_summary": (
                "The rank-four carrier admits an exact real square root of "
                "exchange, but the mathematics does not make that root a "
                "physical Held continuation."
            ),
            "target_value_consumed": False,
        },
        "note": "The exact zipper-root geometry is not consumed by the positivity proof.",
    },
)


if __name__ == "__main__":
    import json
    results = run_all()
    print(json.dumps({
        "module": "continuation_tesseract_math_v0_5",
        "check_count": len(results),
        "checks": {name: ("PASS" if r["passed"] else "FAIL")
                   for name, r in results.items()},
        "all_pass": all(r["passed"] for r in results.values()),
    }, indent=2, sort_keys=True))
