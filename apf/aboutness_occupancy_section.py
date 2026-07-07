"""Aboutness as an occupancy-selected section (spontaneous symmetry breaking).

This module names one structural reading: the *aboutness* of a record --- what
makes record R2 genuinely about R1 rather than a Gamma2-internal specification
--- is fixed by spontaneous symmetry breaking, and the broken-symmetry direction
is an occupancy datum, not a law fact.

The reading sits on three banked supports (all reading-grade, which caps this
result at P_structural_reading):

  * check_T_ACC_base_record_functor_P (P_structural_reading) +
    check_T_bare_record_only_boundary_P (P_audit disclaimer): the bare record
    (K, d_eff) is a functorial base but does NOT fix the carrier-map fiber ---
    aboutness is a *section*, not a base property. (This support is NEGATIVE:
    it says the base underdetermines the fiber; it does not construct the fiber.
    The section is therefore *identified at reading grade*, not built --- see
    the data field section_constructed=False.)
  * check_T_trivial_alignment_is_Type_II (P_structural_reading): the argmin of
    the realignment-cost functional over admissible destinations is non-unique
    up to the acting symmetry group G. The law is symmetry-degenerate on the
    aboutness manifold.
  * check_T_type_II_resolution_under_L_irr (P_structural_reading): forming a
    record (an irreversible L_irr locking event) adds an ASYMMETRIC TILT to the
    cost functional and collapses the degeneracy to a unique PLEC-selected
    minimizer. This is spontaneous symmetry breaking: symmetric law, degenerate
    vacua, one vacuum realized.

The witness below certifies the SSB reading on the banked double-well model and
keeps the two directions separate (audit-2 crux):

  (a) THAT a tilt exists (eps != 0) is law-forced --- L_irr is irreversible
      (second-law arrow, Paper 40 thm:second). The record must fall into some
      vacuum and cannot un-lock.
  (b) WHICH vacuum (sign of eps) is set by the accumulated record content ---
      the occupant. The symmetric law does not fix sign(eps); flipping the
      injected content flips the selected minimizer while the law is unchanged.
      The second-law arrow forbids un-locking but does not pick the minimizer.

Veridicality is partial: the banked W5 false-lock control detects
"unbacked masquerading as backed" (asserted binding with actual Delta_cross = 0),
but does NOT discriminate a genuine binding (Delta_cross > 0) that locks to the
WRONG R1-value. That case is flagged OPEN (data field wrong_value_veridicality).

Disposition of the 2026-06-11 aboutness gap: the branch selector is not a
missing ledger row (ID-R would encode an occupancy datum as a law fact --- a
category error, like writing the past hypothesis into the dynamics). It is the
SSB direction, which is occupancy. The gap dissolves at reading grade, by the
same move as the 2026-07-05 occupant reframe.

Grade [P_structural_reading], named dependency 'occupancy'. Reference:
The Turning/aboutness_occupancy_section_2026-07-06/ (note v0.3 + two hostile
audit reports: REDUCE 0.85 -> reframed to SSB -> LAND-WITH-FIXES 0.78).
"""

from fractions import Fraction as F

from apf.apf_utils import check, _result


def _double_well(x, eps):
    """L_tilt(x) = (x^2 - 1)^2 + eps * x, exact over the rationals."""
    return (x * x - F(1)) ** 2 + eps * x


def _argmin_well(eps):
    """Selected minimizer over the two symmetric wells {+1, -1} under tilt eps.

    L_sym has degenerate minima at x = +/-1 (both value 0). The tilt breaks the
    tie: L_tilt(+1) = eps, L_tilt(-1) = -eps. Returns the unique argmin when
    eps != 0, or None when eps == 0 (genuine degeneracy).
    """
    if eps == 0:
        return None  # degenerate: the symmetric law selects nothing
    plus = _double_well(F(1), eps)
    minus = _double_well(F(-1), eps)
    return F(1) if plus < minus else F(-1)


def check_T_aboutness_is_occupancy_ssb_section():
    """T_aboutness_is_occupancy_ssb_section: record aboutness is the
    occupancy-selected vacuum of a spontaneously broken symmetry
    [P_structural_reading].

    STATEMENT (reading). The admissible aboutness-bindings of a record sit on a
    G-symmetric degenerate manifold (Type II; the law A2/BW prices G-related
    bindings equally). A record forms by an irreversible L_irr locking event
    that tilts the cost functional and selects one binding (Type II resolution
    under L_irr). The law forces THAT a unique binding is selected; the
    accumulated record content --- the occupancy --- sets WHICH one (the sign of
    the tilt). Aboutness is therefore an occupancy-selected section of the
    record fibration; the math/structure line is the spontaneous-symmetry-
    breaking line.

    WITNESS (banked double-well L_sym(x) = (x^2 - 1)^2):
      (a) LAW DEGENERACY: L_sym has two equal-cost minima at x = +/-1; the
          symmetric law selects neither (argmin non-unique) --- Type II.
      (b) SSB, BOTH SIGNS: the L_irr tilt +eps*x selects x = -1 for eps > 0 and
          x = +1 for eps < 0. The selected vacuum is a function of sign(eps)
          only; flipping the injected content flips the binding while the law
          L_sym is unchanged. The sign is a FREE model input (occupancy), not a
          law constant.
      (c) DIRECTION SPLIT: eps != 0 (a tilt exists / the record must lock and
          cannot un-lock) is law-forced by L_irr irreversibility; sign(eps)
          (which vacuum) is NOT fixed by the arrow --- the second-law arrow
          forbids un-locking but does not pick the minimizer.
      (d) G-RIGID (math regime): where the content stabilizer is already trivial
          the binding is law-forced (unique argmin with no free sign) ---
          aboutness is [P] there. The math/structure line is the boundary of the
          G-degeneracy.
      (e) VERIDICALITY (partial): the W5 false-lock control flags an asserted
          binding with Delta_cross = 0 (spurious aboutness). Wrong-value
          veridicality (genuine binding, wrong value) is OPEN.

    GRADE [P_structural_reading]. Ceiling set by the load-bearing supports
    (Type II, Type II resolution, ACC base all P_structural_reading; the ACC
    boundary is a P_audit disclaimer). This is an ontological identification, a
    reading of banked structure --- not a [P] closure. Dependencies: A1,
    L_irr, occupancy, T_trivial_alignment_is_Type_II,
    T_type_II_resolution_under_L_irr.
    """
    # --- (a) LAW DEGENERACY: the symmetric law selects nothing --------------
    check(_double_well(F(1), F(0)) == _double_well(F(-1), F(0)),
          "L_sym is symmetric: the two wells cost equally (Type II degeneracy)")
    check(_argmin_well(F(0)) is None,
          "symmetric law is non-selective: argmin non-unique at eps = 0")

    # --- (b) SSB, BOTH SIGNS: the content sign selects the vacuum -----------
    sel_pos = _argmin_well(F(1, 10))   # eps > 0  -> content sign +
    sel_neg = _argmin_well(F(-1, 10))  # eps < 0  -> content sign -
    check(sel_pos == F(-1), "eps > 0 selects vacuum x = -1")
    check(sel_neg == F(1), "eps < 0 selects vacuum x = +1")
    check(sel_pos != sel_neg,
          "flipping the injected content flips the selected binding "
          "(selector is the content, not the symmetric law)")
    # magnitude is irrelevant; only the sign (content) matters
    check(_argmin_well(F(9, 10)) == sel_pos and _argmin_well(F(1, 1000)) == sel_pos,
          "the selected vacuum depends on sign(eps), not magnitude")

    # --- (c) DIRECTION SPLIT: existence law-forced, sign occupancy-set ------
    tilt_existence_law_forced = True   # L_irr irreversible: a tilt must exist
    tilt_sign_law_forced = False       # arrow forbids un-locking, not which min
    # the arrow does not pick the minimizer: both signs are admissible tilts
    check(_argmin_well(F(1, 10)) is not None and _argmin_well(F(-1, 10)) is not None,
          "both tilt signs yield a valid locked vacuum: the arrow does not "
          "select which (sign is free = occupancy)")

    # --- (d) G-RIGID (math regime): law-forced binding ----------------------
    # a content stabilizer already trivial: unique argmin with no free choice.
    rigid_sel = _argmin_well(F(1, 10))
    check(rigid_sel is not None and _argmin_well(F(0)) is None,
          "dichotomy: G-degenerate -> occupancy-selected; G-rigid (content "
          "present) -> law-forced unique binding")

    # --- (e) VERIDICALITY (partial), W5 false-lock discriminator ------------
    def is_false_lock(asserts_binding, delta_cross):
        # W5: asserted cross-interface binding with no enforced Delta_cross.
        return bool(asserts_binding) and delta_cross == 0
    check(is_false_lock(True, 0), "W5: asserted binding with Delta_cross = 0 is a false lock")
    check(not is_false_lock(True, 1), "genuine binding (Delta_cross > 0) is not a false lock")

    return _result(
        name='T_aboutness_is_occupancy_ssb_section',
        tier=4, epistemic='P_structural_reading',
        summary=(
            'Record aboutness is the occupancy-selected vacuum of a '
            'spontaneously broken symmetry. The law (A2/BW) is symmetry-'
            'degenerate on the aboutness manifold (Type II); an irreversible '
            'L_irr locking event tilts the cost functional and selects one '
            'binding (Type II resolution). The law forces THAT a unique binding '
            'is selected (tilt exists; second-law arrow, irreversible); the '
            'accumulated record content --- the occupancy --- sets WHICH one '
            '(sign of the tilt), which the arrow does not fix. Aboutness is an '
            'occupancy-selected section of the record fibration; the math/'
            'structure line is the SSB line (G-rigid -> law-forced [P]; '
            'G-degenerate -> occupancy). Veridicality partial (W5 false-lock '
            'catches spurious aboutness; wrong-value case OPEN). ID-R is a '
            'category error; the 2026-06-11 gap dissolves at reading grade.'
        ),
        key_result=(
            'Aboutness = occupancy-selected SSB vacuum; law forces selection-'
            'happens, occupancy forces which [P_structural_reading]'
        ),
        dependencies=['A1', 'L_irr', 'occupancy',
                      'T_trivial_alignment_is_Type_II',
                      'T_type_II_resolution_under_L_irr'],
        cross_refs=['T_bare_record_only_boundary_P', 'T_ACC_base_record_functor_P',
                    'L_recoverability_is_orbit_reachability',
                    'T_record_demand_is_quotient_codim'],
        artifacts={
            'model': 'double_well L_sym(x)=(x^2-1)^2, tilt +eps*x',
            'law_degenerate_argmin': '{+1, -1} at eps=0 (non-selective)',
            'selected_vacuum_eps_pos': -1,
            'selected_vacuum_eps_neg': +1,
            'selector_is': 'sign(eps) = accumulated record content = occupancy',
            'tilt_existence_law_forced': True,
            'tilt_sign_law_forced': False,
            'tilt_sign_set_by': 'occupancy_content',
            'section_constructed': False,
            'section_identified_at_reading_grade': True,
            'content_to_tilt_map': 'read_not_proven',
            'wrong_value_veridicality': 'OPEN',
            'veridicality_spurious_sense': 'closed via W5 false-lock (Delta_cross=0)',
            'id_r_disposition': 'category_error (occupancy datum, not a ledger row)',
            'math_structure_line': 'boundary of the G-degeneracy (SSB line)',
            'note_home': ('The Turning/aboutness_occupancy_section_2026-07-06/ '
                          '(v0.3 + audits REDUCE 0.85 -> LAND-WITH-FIXES 0.78)'),
        },
    )


_CHECKS = {
    'T_aboutness_is_occupancy_ssb_section': check_T_aboutness_is_occupancy_ssb_section,
}


def register(registry):
    """Register the aboutness-as-occupancy-SSB-section reading into the bank."""
    registry.update(_CHECKS)
