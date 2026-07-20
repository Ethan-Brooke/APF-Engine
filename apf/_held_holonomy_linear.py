"""Private H4-H5 linear witnesses for :mod:`apf.held_holonomy`."""
from __future__ import annotations
from ._held_holonomy_common import *
def reversible_ledger_isometry_impl() -> Dict[str, object]:
    fails: List[str] = []

    def ck(cond: bool, msg: str) -> None:
        if not cond:
            fails.append(msg)

    # B=S^{-T}S^{-1}, T=S J S^{-1}; this is a rational, non-Euclidean
    # realization of a quarter-turn preserving B.
    b = [[F(1, 4), F(0)], [F(0), F(1, 9)]]
    t = [[F(0), F(-2, 3)], [F(3, 2), F(0)]]
    t_inv = _inverse(t)
    b_inv = _inverse(b)
    t_sharp = _mm(_mm(b_inv, _transpose(t)), b)

    ck(b[0][0] > 0 and _det2(b) > 0, "B must be positive definite")
    ck(_eq(_mm(t_inv, t), _eye(2)) and _eq(_mm(t, t_inv), _eye(2)),
       "reversed loop must represent the inverse")
    ck(_eq(t_sharp, t_inv), "represented reversal adjoint must equal inverse")
    ck(_eq(_mm(_mm(_transpose(t), b), t), b),
       "T^T B T must equal B")

    for v in product(range(-3, 4), repeat=2):
        vf = [F(v[0]), F(v[1])]
        ck(_quadratic(b, _mv(t, vf)) == _quadratic(b, vf),
           "exact ledger norm must be preserved on the rational grid")

    # Auxiliary monotonicity lemma and its sharp negative control.
    i2 = _eye(2)
    contraction = [[F(1, 2), F(0)], [F(0), F(1)]]
    forward_gap = _sub(i2, _mm(_mm(_transpose(contraction), i2), contraction))
    contraction_inv = _inverse(contraction)
    inverse_gap = _sub(i2, _mm(_mm(_transpose(contraction_inv), i2), contraction_inv))
    ck(_is_psd_2(forward_gap), "forward contraction must satisfy q(Cv)<=q(v)")
    ck(not _is_psd_2(inverse_gap),
       "inverse monotonicity must fail for a proper contraction")
    ck(not _eq(_mm(_transpose(contraction), contraction), i2),
       "forward contraction alone is not an isometry")

    return _result(
        "T_reversible_ledger_isometry",
        "P_math",
        ("For a represented record-free loop, Q2 identifies reversal with the "
         "ledger adjoint and reversible loop closure identifies reversal with "
         "the inverse.  Hence T^sharp=T^-1 and T^TBT=B exactly.  The rational "
         "non-Euclidean witness is certified.  A forward contraction shows why "
         "one-sided monotonicity alone is insufficient; no new monotonicity "
         "postulate is load-bearing."),
        [],
        {
            "B": _matrix_strings(b),
            "T": _matrix_strings(t),
            "T_inverse": _matrix_strings(t_inv),
            "T_sharp": _matrix_strings(t_sharp),
            "grid_vectors_checked": 49,
            "canonical_route": "T^sharp = T^-1",
            "two_sided_monotonicity_role": "auxiliary only",
            "forward_contraction_gap": _matrix_strings(forward_gap),
            "inverse_contraction_gap": _matrix_strings(inverse_gap),
        },
        fails,
        premises=(
            "positive_quadratic_ledger_form",
            "Q2_reversal_is_ledger_adjoint",
            "reversed_record_free_loop_is_inverse",
        ),
        negative_controls=(
            "diag(1/2,1) is forward-nonincreasing but not isometric",
        ),
        cross_refs=(
            "Paper 5 Mathematical Note v1.7 Lemma 5.2 and Corollary 5.3",
            "Paper 5 Technical Supplement v7.10 Q2 ledger adjoint",
        ),
    )


# ---------------------------------------------------------------------------
# H5: the elementary bipolar first-jet plane
# ---------------------------------------------------------------------------


def bipolar_first_jet_rank_two_impl() -> Dict[str, object]:
    fails: List[str] = []

    def ck(cond: bool, msg: str) -> None:
        if not cond:
            fails.append(msg)

    # q_+(t)=t and q_-(t)=-t at t=0.
    q_plus_jet = [F(0), F(1)]
    q_minus_jet = [F(0), F(-1)]
    value_only = [[F(1), F(0)]]
    derivative_only = [[F(0), F(1)]]

    ck(_mv(value_only, q_plus_jet) == _mv(value_only, q_minus_jet),
       "value-only carrier must identify opposite germs at the tie")
    ck(_mv(derivative_only, q_plus_jet) != _mv(derivative_only, q_minus_jet),
       "derivative-only carrier separates the example germs")
    ck(_mv(derivative_only, [F(1), F(0)]) == [F(0)],
       "derivative-only carrier loses present-value data")

    # Any one-dimensional linear carrier L=[a b] has nonzero kernel vector
    # (b,-a), so it cannot faithfully carry arbitrary first-jet data (q,q_dot).
    rank_one_rows_checked = 0
    for a, b in product(range(-4, 5), repeat=2):
        if a == 0 and b == 0:
            continue
        row = [[F(a), F(b)]]
        kernel = [F(b), F(-a)]
        ck(kernel != [F(0), F(0)], "rank-one kernel witness must be nonzero")
        ck(_mv(row, kernel) == [F(0)], "(b,-a) is the exact rank-one kernel")
        rank_one_rows_checked += 1

    first_jet_identity = _eye(2)
    ck(_det2(first_jet_identity) == 1, "rank-two first-jet carrier is faithful")
    ck(_mv(first_jet_identity, q_plus_jet) !=
       _mv(first_jet_identity, q_minus_jet),
       "rank-two carrier separates opposite germs")

    # Higher-order fence: t^2 and -t^2 have identical first jets at zero.
    h_plus_first_jet = [F(0), F(0)]
    h_minus_first_jet = [F(0), F(0)]
    later = F(1, 3)
    ck(h_plus_first_jet == h_minus_first_jet,
       "higher-order pair shares the first jet")
    ck(later * later != -(later * later),
       "higher-order pair remains distinct later")

    return _result(
        "T_bipolar_first_jet_rank_two",
        "P_math",
        ("After common displacement and independently recordable coordinates "
         "are split off, an elementary bipolar comparison has first-jet data "
         "(q,q_dot).  Every rank-one linear carrier has the exact kernel "
         "(b,-a), while the rank-two first-jet carrier is faithful.  The "
         "t^2/-t^2 control keeps the claim restricted to a first-order-complete "
         "regime; this is not a Bloch-plane or complex-scalar assumption."),
        [],
        {
            "q_plus_jet": [str(x) for x in q_plus_jet],
            "q_minus_jet": [str(x) for x in q_minus_jet],
            "rank_one_rows_checked": rank_one_rows_checked,
            "minimum_complete_rank": 2,
            "higher_order_control": ["t^2", "-t^2"],
            "scope": "one elementary bipolar quotient after common/record coordinates split off",
            "not_the_tesseract_rank_four_claim": True,
        },
        fails,
        premises=(
            "elementary_bipolar_support",
            "first_order_local_continuation_completeness",
            "minimum_complete_carrier",
        ),
        negative_controls=(
            "value-only carrier",
            "derivative-only carrier",
            "t^2/-t^2 higher-order pair",
        ),
        cross_refs=(
            "L_tie_through_zero_defect_germ",
            "T_klein_four_continuation_tesseract",
            "Paper 10 universal local continuation lift",
        ),
    )


# ---------------------------------------------------------------------------
# H6: full circle -> half-turn and quarter-turn
# ---------------------------------------------------------------------------


