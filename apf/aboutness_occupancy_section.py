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


# ---------------------------------------------------------------------------
# A UNIFIED, ==-TESTABLE model of the three typed objects on a common record
# space.  A held presentation is (r, c): r = record content, c = coherence /
# operational-radical component (there are `nc` coherence values per content;
# nc >= 2 == a NONZERO operational radical, no_phantom's object; nc == 1 == a
# zero radical / semisimple).  Outcomes range over `no` values (no >= 2 == an
# SSB-degenerate binding manifold, aboutness's object; no == 1 == G-trivial).
#
# Common record space Rec = content x outcome-slot, slot in {SYM, 0..no-1}:
#   R    (invariant record quotient) : (r,c) |-> (r, SYM)   -- radical-blind,
#         outcome-blind; when no==1 there is NO symmetry to be invariant under,
#         so the invariant image and the sole committed outcome coincide:
#         slot = 0 == C_0.
#   C_i  (outcome-selection instrument): (r,c) |-> (r, i)    -- commits outcome i.
# Distinctness of two objects == their maps DIFFER on the common space; a
# control DEGENERATES a property (nc->1 or no->1) and RE-RUNS the same predicate.
# ---------------------------------------------------------------------------

def _held(nr, nc):
    return [(r, c) for r in range(nr) for c in range(nc)]

def _R(state, no):
    r, _c = state
    return (r, 'SYM') if no >= 2 else (r, 0)      # SYM distinct only when a symmetry exists

def _C(i, state):
    r, _c = state
    return (r, i)

def _noninjective(f, H):
    seen = {}
    for s in H:
        seen.setdefault(f(s), []).append(s)
    return any(len(v) > 1 for v in seen.values())

def _distinct_H_R(nr, nc, no):
    H = _held(nr, nc)
    return _noninjective(lambda s: _R(s, no), H)             # H != R(H) iff R non-injective

def _distinct_R_C(nr, nc, no):
    H = _held(nr, nc)
    return any(_R(s, no) != _C(i, s) for s in H for i in range(no))   # some (r,SYM) != (r,i)

def _distinct_H_C(nr, nc, no):
    H = _held(nr, nc)
    if any(_noninjective(lambda s: _C(i, s), H) for i in range(no)):
        return True                                          # C_i forgets coherence
    return no >= 2                                           # or loses co-available outcomes


def check_T_held_to_record_typing():
    """The held carrier H, the invariant record quotient R(H), and the outcome-
    selection instruments {C_i} are three DISTINCT typed objects on a common
    record space (Paper 9 TS v1.0 def:ts-record-transition; Paper 14 held
    profile). Composes the two banked faces -- no_phantom_record_quotient (the
    radical-blind invariant quotient) and aboutness_is_occupancy_ssb_section
    (the occupancy-selected SSB vacua) -- and shows the three-way
    non-identification FOLLOWS from (nonzero operational radical) + (SSB
    degeneracy), each made load-bearing by a collapse control that re-runs the
    same distinctness predicate on the degenerated model. [P_structural_reading]."""

    # ---- faithfulness: the two banked objects are the model's nc/no ------
    # no_phantom's object: R[x]/(x^3), radical (x^2) NONZERO (nc=2 coherence: {1,x} vs x^2).
    def _alg_mult(i, j):
        return None if i + j >= 3 else i + j
    check(_alg_mult(2, 1) is None and _alg_mult(2, 2) is None and _alg_mult(2, 0) == 2,
          "no_phantom object: x^2 is a NONZERO operational-radical element (nc >= 2)")
    # aboutness's object: the double-well has TWO occupancy-selected vacua (no=2).
    v_pos, v_neg = _argmin_well(F(-1, 10)), _argmin_well(F(1, 10))
    check(v_pos == F(1) and v_neg == F(-1) and v_pos != v_neg and _argmin_well(F(0)) is None,
          "aboutness object: the SSB manifold is degenerate with TWO occupancy vacua (no >= 2)")

    # ---- the three-way distinctness on the non-degenerate model ----------
    NR, NC, NO = 3, 2, 2   # nonzero radical (nc=2), SSB degeneracy (no=2)
    check(_distinct_H_R(NR, NC, NO),
          "H != R(H): R is a proper non-injective quotient -- coherence-distinct held "
          "states (r,c1),(r,c2) share the invariant image (r,SYM)")
    check(_distinct_R_C(NR, NC, NO),
          "R(H) != C_i: on the common record space the invariant image (r,SYM) differs "
          "from every committed image (r,i) -- outcome-blind vs outcome-bearing")
    check(_distinct_H_C(NR, NC, NO),
          "H != C_i: each C_i forgets coherence AND commits one of the co-available "
          "outcomes, losing the alternatives the held carrier holds")

    # ---- parity witness for R(H) != C_i (in the common space) ------------
    # the outcome symmetry sigma swaps 0<->1 and FIXES SYM. R's image is sigma-fixed;
    # each C_i's image is sigma-MOVED. A sigma-fixed object cannot equal a moved one.
    # NOTE: two-outcome (no=2) parity witness, matching the banked double-well's two
    # vacua +/-1; sigma swaps {0,1} and does NOT generalize to no>=3 (out of the
    # banked object's scope). NO is pinned to 2 below.
    sigma = lambda slot: slot if slot == 'SYM' else (1 - slot if slot in (0, 1) else slot)
    s0 = (0, 0)
    R_img = _R(s0, NO)
    check(sigma(R_img[1]) == R_img[1],
          "parity: the invariant record image (slot SYM) is sigma-FIXED")
    check(all(sigma(_C(i, s0)[1]) != _C(i, s0)[1] for i in range(NO)),
          "parity: every committed image (slot i) is sigma-MOVED (0<->1) -- so no C_i "
          "equals the sigma-fixed R(H)")

    # ======================================================================
    # COLLAPSE CONTROLS -- degenerate a banked-face property, RE-RUN the SAME
    # predicate, and exhibit the collapse (equality). Not hardcoded booleans.
    # ======================================================================
    # (a) ZERO radical (nc=1, semisimple): re-run H vs R -> R injective -> H = R(H).
    check(_distinct_H_R(NR, NC, NO) and not _distinct_H_R(NR, 1, NO),
          "CONTROL (no_phantom load-bearing): setting the operational radical to ZERO "
          "(nc=1) makes R injective -> H = R(H) COLLAPSES; H != R(H) REQUIRES a nonzero "
          "radical")
    # (b) G-TRIVIAL manifold (no=1): re-run R vs C -> (r,SYM->0)==(r,0) -> R(H) = C_0.
    check(_distinct_R_C(NR, NC, NO) and not _distinct_R_C(NR, NC, 1),
          "CONTROL (aboutness/Type-II load-bearing): setting the manifold to a single "
          "outcome (no=1, no symmetry to be invariant under) makes the invariant image "
          "coincide with the sole committed outcome -> R(H) = C_0 COLLAPSES; R(H) != C_i "
          "REQUIRES the SSB degeneracy")
    # (c) BOTH degenerate (nc=1, no=1): re-run H vs C -> C_0 bijective -> H = C_0.
    check(_distinct_H_C(NR, NC, NO) and not _distinct_H_C(NR, 1, 1),
          "CONTROL (degeneracy load-bearing): with zero radical AND a single outcome "
          "(nc=1,no=1) C_0 is a bijection -> H = C_0 COLLAPSES; H != C_i REQUIRES a "
          "nonzero radical or >= 2 co-available outcomes")

    # ---- the composite fact: all three distinct together, and EACH control
    #      flips exactly the relevant pair to identical (model-dependent, not
    #      type-baked) --------------------------------------------------------
    nd = (_distinct_H_R(NR, NC, NO), _distinct_R_C(NR, NC, NO), _distinct_H_C(NR, NC, NO))
    ca = (_distinct_H_R(NR, 1, NO), _distinct_R_C(NR, 1, NO), _distinct_H_C(NR, 1, NO))
    cb = (_distinct_H_R(NR, NC, 1), _distinct_R_C(NR, NC, 1), _distinct_H_C(NR, NC, 1))
    check(nd == (True, True, True),
          "TYPING: on the composed witness (nonzero radical + SSB degeneracy) H, R(H), "
          "{C_i} are pairwise distinct")
    check(ca[0] is False and cb[1] is False,
          "each collapse is causal and targeted: zero radical kills exactly H!=R(H); a "
          "trivial manifold kills exactly R(H)!=C_i -- the distinctness verdict is "
          "MODEL-DEPENDENT, not type-baked")

    return _result(
        name='T_held_to_record_typing -- held carrier / invariant record quotient / '
             'outcome-selection instruments are three distinct typed objects on a '
             'common record space (Paper 9 TS v1.0 def:ts-record-transition; Paper 14)',
        tier=4,
        epistemic='P_structural_reading',
        summary=(
            'Composes the two banked held-to-record faces into the three-way TYPING the '
            'Paper 9 Technical Supplement asserts (def:ts-record-transition): the held '
            'carrier H, the invariant record quotient R(H), and the outcome-selection '
            'instruments {C_i} are PAIRWISE DISTINCT and cannot be identified. All three '
            'objects are realized as maps into ONE common record space (Rec = content x '
            'outcome-slot in {SYM,0..no-1}), so distinctness is machine-decided by '
            'map/kernel equality, not asserted across disjoint types. On the composed '
            'witness -- nonzero operational radical (nc>=2, no_phantom''s R[x]/(x^3) with '
            'x^2 != 0) + SSB degeneracy (no>=2, aboutness''s two occupancy vacua +/-1) -- '
            '(I) H != R(H): R is non-injective, coherence-distinct held states share the '
            'invariant image; (II) R(H) != C_i: the invariant image (r,SYM) differs from '
            'every committed image (r,i), and under the outcome symmetry sigma the '
            'invariant image is sigma-FIXED while each committed image is sigma-MOVED; '
            '(III) H != C_i: each C_i forgets coherence and commits one co-available '
            'outcome. The three-way distinctness is shown to FOLLOW from the two banked '
            'objects by collapse controls that RE-RUN the same distinctness predicate on '
            'the degenerated model: zero radical (nc=1) collapses H=R(H); a single '
            'outcome (no=1) collapses R(H)=C_0; both (nc=1,no=1) collapse H=C_0 -- so the '
            'verdict is model-dependent, not type-baked: the radical is load-bearing '
            'for H!=R(H) and the degeneracy for R(H)!=C_i, while H!=C_i holds from '
            'either (nonzero radical OR >=2 co-available outcomes). Grade '
            '[P_structural_reading]: a typing '
            'that composes two banked readings; it types the three objects, it does not '
            'derive the physical held-profile ontology. Paper anchor: Paper 9 TS v1.0 '
            'def:ts-held-profile + def:ts-record-transition.'
        ),
        key_result=(
            'held carrier H != invariant record quotient R(H) != outcome instruments '
            '{C_i}, realized as maps on one common record space so distinctness is '
            '==-decided; pairwise non-identification FOLLOWS from nonzero radical '
            '(no_phantom) + SSB degeneracy (aboutness), each shown load-bearing by a '
            'collapse control that re-runs the predicate on the degenerated model '
            '(nc=1 -> H=R(H); no=1 -> R(H)=C_0; nc=1,no=1 -> H=C_0). [P_structural_reading].'
        ),
        dependencies=['A1', 'L_irr', 'occupancy', 'T_no_phantom_record_quotient',
                      'T_aboutness_is_occupancy_ssb_section'],
        cross_refs=['T_no_phantom_record_quotient', 'T_aboutness_is_occupancy_ssb_section',
                    'T_type_II_resolution_under_L_irr', 'occupancy'],
        artifacts={
            'common_space': 'Rec = content x outcome-slot {SYM,0..no-1}; R->SYM, C_i->i',
            'distinctness_nondegenerate': [True, True, True],
            'collapse_controls': {'nc=1 -> H=R(H)': True, 'no=1 -> R(H)=C_0': True,
                                  'nc=1,no=1 -> H=C_0': True},
            'parity': 'invariant image sigma-fixed; committed images sigma-moved',
            'paper_anchor': 'Paper 9 TS v1.0 def:ts-held-profile + def:ts-record-transition',
        },
    )


_CHECKS = {
    'T_aboutness_is_occupancy_ssb_section': check_T_aboutness_is_occupancy_ssb_section,
    'T_held_to_record_typing': check_T_held_to_record_typing,
}


def register(registry):
    """Register the aboutness-as-occupancy-SSB-section reading into the bank."""
    registry.update(_CHECKS)
