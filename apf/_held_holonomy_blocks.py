"""Private block-classification/SAT witnesses for :mod:`apf.held_holonomy`."""
from __future__ import annotations
from ._held_holonomy_common import *
def _realify_complex(x: Matrix, y: Matrix) -> Matrix:
    """Realification of X+iY in Re/Im block ordering."""

    if _shape(x) != _shape(y) or _shape(x)[0] != _shape(x)[1]:
        raise ValueError("complex realification requires equal square blocks")
    n = len(x)
    top = [x[i] + [-v for v in y[i]] for i in range(n)]
    bottom = [y[i] + x[i] for i in range(n)]
    return top + bottom


def _qmul(a: Tuple[F, F, F, F],
          b: Tuple[F, F, F, F]) -> Tuple[F, F, F, F]:
    a0, a1, a2, a3 = a
    b0, b1, b2, b3 = b
    return (
        a0*b0 - a1*b1 - a2*b2 - a3*b3,
        a0*b1 + a1*b0 + a2*b3 - a3*b2,
        a0*b2 - a1*b3 + a2*b0 + a3*b1,
        a0*b3 + a1*b2 - a2*b1 + a3*b0,
    )


def central_complex_block_exclusion_impl() -> Dict[str, object]:
    fails: List[str] = []

    def ck(cond: bool, msg: str) -> None:
        if not cond:
            fails.append(msg)

    # Center of M2(R): exact commutant dimension one.
    real_basis = _matrix_units(2)
    real_constraints = _commutant_constraint_matrix(real_basis, 2)
    real_center_dim = 4 - _rank(real_constraints)
    ck(real_center_dim == 1, "center of M2(R) must be one-dimensional real scalars")

    # Center of H: exact commutant of i and j has dimension one.
    q_basis = (
        (F(1), F(0), F(0), F(0)),
        (F(0), F(1), F(0), F(0)),
        (F(0), F(0), F(1), F(0)),
        (F(0), F(0), F(0), F(1)),
    )
    qi, qj = q_basis[1], q_basis[2]
    q_constraint_rows: Matrix = []
    for generator in (qi, qj):
        columns: List[Tuple[F, F, F, F]] = []
        for basis_element in q_basis:
            left = _qmul(basis_element, generator)
            right = _qmul(generator, basis_element)
            columns.append(tuple(left[k] - right[k] for k in range(4)))
        for output_coordinate in range(4):
            q_constraint_rows.append([columns[k][output_coordinate]
                                      for k in range(4)])
    quaternion_center_dim = 4 - _rank(q_constraint_rows)
    ck(quaternion_center_dim == 1, "center of H must be real scalars")
    qk = q_basis[3]
    ck(_qmul(qi, qi) == (F(-1), F(0), F(0), F(0)), "i^2=-1 in H")
    ck(_qmul(qi, qj) == qk and _qmul(qj, qi) == tuple(-x for x in qk),
       "quaternionic square root i is not central")

    # Realified M2(C): commutant is two-dimensional, spanned by I and J.
    e2 = _matrix_units(2)
    z2 = _zero(2, 2)
    complex_real_basis = [_realify_complex(e, z2) for e in e2]
    complex_imag_basis = [_realify_complex(z2, e) for e in e2]
    complex_algebra_basis = complex_real_basis + complex_imag_basis
    complex_constraints = _commutant_constraint_matrix(complex_algebra_basis, 4)
    complex_center_dim = 16 - _rank(complex_constraints)
    ck(complex_center_dim == 2,
       "real commutant of realified M2(C) must be span_R{I,J}")

    j4 = _realify_complex(z2, _eye(2))
    i4 = _eye(4)
    ck(_eq(_mm(j4, j4), _scal(F(-1), i4)), "central complex unit squares to -I")
    ck(all(_eq(_mm(j4, a), _mm(a, j4)) for a in complex_algebra_basis),
       "J must commute with the whole realified complex matrix algebra")

    # A real scalar cannot square to -1: x^2+1 has negative discriminant.
    discriminant = F(-4)
    ck(discriminant < 0, "x^2+1 has no real root")

    return _result(
        "T_central_complex_block_exclusion",
        "P_math",
        ("The exact commutant calculations give center dimension one for "
         "M2(R) and for H, but dimension two for realified M2(C).  Quaternionic "
         "i squares to -1 yet fails centrality (ij=-ji); the realified complex "
         "J is central and squares to -I.  Therefore a central square-minus-one "
         "excludes real and quaternionic simple blocks and selects complex blocks, "
         "conditional on the finite real C*-classification and prior centrality."),
        ["T_held_jet_naturality"],
        {
            "center_dimensions": {
                "M2(R)": real_center_dim,
                "H": quaternion_center_dim,
                "realified_M2(C)": complex_center_dim,
            },
            "real_polynomial_discriminant_x2_plus_1": str(discriminant),
            "quaternion_i_central": False,
            "complex_J_central": True,
            "complex_J": _matrix_strings(j4),
        },
        fails,
        premises=(
            "finite_real_Cstar_completion",
            "J_is_central_in_the_completed_represented_algebra",
        ),
        negative_controls=(
            "quaternionic i has i^2=-1 but ij=-ji",
            "real scalar equation x^2=-1 has no solution",
        ),
        cross_refs=(
            "Paper 2 Technical Supplement II: complex-type classification",
            "Paper 5 Technical Supplement v7.10 Q4",
        ),
    )


# ---------------------------------------------------------------------------
# SAT disposition: bypassed, never contradicted
# ---------------------------------------------------------------------------


def sat_countermodel_bypassed_not_refuted_impl() -> Dict[str, object]:
    fails: List[str] = []

    def ck(cond: bool, msg: str) -> None:
        if not cond:
            fails.append(msg)

    i2 = _eye(2)
    p = [[F(0), F(1)], [F(1), F(0)]]
    e_minus = _scal(F(1, 2), _sub(i2, p))
    physical_monoid = (i2, p)

    ck(_eq(_mm(p, p), i2), "static exchange countermodel must be consistent")
    ck(not any(_eq(e_minus, m) for m in physical_monoid),
       "physical odd projector must be absent")
    ck(all(not _eq(_mm(m, m), m) or _eq(m, i2) for m in physical_monoid),
       "no nontrivial physical idempotent exists")
    ck(len(physical_monoid) == 2, "effective symmetry is discrete C2")
    connected = len(physical_monoid) == 1
    ck(not connected, "C2 must fail the connectedness hypothesis")

    return _result(
        "T_SAT_countermodel_is_bypassed_not_refuted",
        "P_structural_instrument",
        ("The old identity/exchange carrier {I,P} is mathematically consistent: "
         "it retains static exchange but contains neither the odd character "
         "projector nor a connected nontrivial holonomy.  The Held route therefore "
         "bypasses SAT by adding different hypotheses; it does not refute the old "
         "countermodel or pretend static exchange already contains a circle."),
        ["T_HOC_quantum_close_scope_contract", "T_held_connected_subgroup_so2"],
        {
            "physical_monoid": ["I", "P"],
            "static_exchange_present": True,
            "physical_odd_projector_present": False,
            "nontrivial_connected_holonomy_present": False,
            "SAT_status": "retired_as_unnecessary_not_refuted",
        },
        fails,
        premises=(),
        negative_controls=(
            "identity/exchange-only C2 carrier",
        ),
        cross_refs=(
            "T_HOC_quantum_close_scope_contract",
            "Paper 5 Held-holonomy replacement of SAT",
        ),
    )


# ---------------------------------------------------------------------------
# Dependency contract and no-positivity-cycle tripwire
# ---------------------------------------------------------------------------


