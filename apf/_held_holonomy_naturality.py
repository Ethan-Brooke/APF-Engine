"""Private orientation/classification witnesses for :mod:`apf.held_holonomy`."""
from __future__ import annotations
from ._held_holonomy_common import *
def held_circle_quarter_turn_impl() -> Dict[str, object]:
    fails: List[str] = []

    def ck(cond: bool, msg: str) -> None:
        if not cond:
            fails.append(msg)

    i2 = _eye(2)
    minus_i = _scal(F(-1), i2)
    j = [[F(0), F(-1)], [F(1), F(0)]]
    r_pi = minus_i

    ck(_eq(_mm(j, j), minus_i), "J^2=-I")
    ck(_eq(_mm(_transpose(j), j), i2), "J is orthogonal")
    ck(_eq(_transpose(j), _scal(F(-1), j)), "J^T=-J")
    ck(_det2(j) == 1, "J is orientation preserving")
    ck(_eq(_mm(r_pi, r_pi), i2) and not _eq(r_pi, i2),
       "-I is the nonidentity order-two half-turn")
    ck(_eq(_mm(_mm(j, j), j), _scal(F(-1), j)), "J^3=-J")
    ck(_eq(_mm(_mm(j, j), _mm(j, j)), i2), "J has order four")

    return _result(
        "T_held_circle_quarter_turn",
        "P_math",
        ("Once the effective image is the full SO(2) circle, its unique "
         "nonidentity order-two element is R(pi)=-I and its quarter-turn "
         "J=R(pi/2) obeys J^2=-I, J^T=-J, J^TJ=I, and det J=1.  This is the "
         "canonical local complex orientation, conditional on the Held-circle "
         "premises rather than assumed as a scalar field."),
        ["T_held_connected_subgroup_so2", "T_reversible_ledger_isometry",
         "T_bipolar_first_jet_rank_two"],
        {
            "R_pi": _matrix_strings(r_pi),
            "J": _matrix_strings(j),
            "relations": ["J^2=-I", "J^T=-J", "J^T J=I", "det(J)=1"],
            "half_turn_is_derived": True,
        },
        fails,
        premises=(
            "nontrivial_connected_effective_image",
            "faithful_isometric_action_on_the_bipolar_plane",
            "positive_quadratic_ledger_form",
        ),
        negative_controls=(
            "the disconnected C2 subgroup contains -I but no quarter-turn",
        ),
        cross_refs=(
            "T_quantum_zipper_root_of_exchange",
            "Paper 5 Mathematical Note v1.7 Theorem 6.6",
        ),
    )


# ---------------------------------------------------------------------------
# H7: naturality on first jets
# ---------------------------------------------------------------------------


def held_jet_naturality_impl() -> Dict[str, object]:
    fails: List[str] = []

    def ck(cond: bool, msg: str) -> None:
        if not cond:
            fails.append(msg)

    j = [[F(0), F(-1)], [F(1), F(0)]]
    scalars = [F(-3), F(-1), F(0), F(1, 2), F(1), F(2), F(7, 3)]
    for a in scalars:
        lift = _scal(a, _eye(2))
        ck(_eq(_mm(lift, j), _mm(j, lift)),
           "scalar first-jet lift must commute with J")

    # The full real commutant of J has the complex-linear form [[a,-b],[b,a]].
    commutant_samples = 0
    for a, b in product(range(-2, 3), repeat=2):
        c = [[F(a), F(-b)], [F(b), F(a)]]
        ck(_eq(_mm(c, j), _mm(j, c)),
           "complex-linear commutant form must commute with J")
        commutant_samples += 1

    anisotropic = [[F(2), F(0)], [F(0), F(1)]]
    ck(not _eq(_mm(anisotropic, j), _mm(j, anisotropic)),
       "general anisotropic map need not be J-natural")

    return _result(
        "T_held_jet_naturality",
        "P_math",
        ("A typed morphism of one-dimensional elementary comparison quotients "
         "has scalar derivative a_f; its first-jet lift is a_f I and commutes "
         "with the quarter-turn.  The exact commutant is the complex-linear "
         "form [[a,-b],[b,a]].  An anisotropic map is the negative control: "
         "local J does not become natural without the scalar/functorial premise."),
        ["T_held_circle_quarter_turn"],
        {
            "scalar_derivatives_checked": [str(x) for x in scalars],
            "commutant_samples_checked": commutant_samples,
            "anisotropic_control": _matrix_strings(anisotropic),
            "naturality_scope": "typed elementary first-jet morphisms",
        },
        fails,
        premises=(
            "jet_functoriality",
            "one_dimensional_comparison_derivative_is_scalar",
            "orientation_synchronization_across_typed_sectors",
            "continuous_conjugation_orientation_transport",
            "closed_world_record_completeness",
        ),
        negative_controls=(
            "diag(2,1) does not commute with J",
        ),
        cross_refs=(
            "Paper 5 Technical Supplement v7.11 section 23.3-23.4",
        ),
    )


# ---------------------------------------------------------------------------
# Central square-minus-one and the real C*-block menu
# ---------------------------------------------------------------------------


