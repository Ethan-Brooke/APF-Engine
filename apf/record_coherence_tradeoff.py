# BANKED v24.3.477 (2026-08-15): built by a cold build seat to the frozen
# claim surface CLAIM_SURFACE_FROZEN_2026-08-15.md (Artifacts_2026-08-11_session/
# tradeoff_bank/), twice blind-audited (LAND-WITH-FIXES 0.86 / AFFIRM 0.90,
# ZERO arithmetic disagreement), fixes carried by a cold fix seat (7 fixed /
# 3 declined with reasons), LIFTED by Ethan 2026-08-15; registered with
# bare-name keys per D6@2026-08-03.
"""The record-coherence tradeoff: a theorem over the banked SR/PD/EE model.

BANKED v24.3.477 (2026-08-15).  Built by a cold build seat to the FROZEN
claim surface (binding; weakening with disclosure is the permitted direction,
strengthening is not; no check returns a sentence the surface does not
license):
  Artifacts_2026-08-11_session/tradeoff_bank/CLAIM_SURFACE_FROZEN_2026-08-15.md
  raw sha256 (verified by the build seat BEFORE reading; the constant below
  is the same value byte-for-byte):
  a2bb003c8001e9647c9d26ae4fefe302c9101caabf800c6f05f56c89574ca7f2
Pin at build: repo HEAD `6ffb4bd` (verified live by the build seat).
CONTAMINATION, DISCLOSED (from the surface): the surface was drafted by the
coordinator desk that ran the arc this module banks; this build seat is cold
and built from the surface plus the banked modules only.

WHAT THIS MODULE IS.  A theorem-over-the-banked-model module: every sentence
below is about the banked SR/PD/EE model objects of v24.3.476 --
stochastic_record (the record pair (p, q) over shared cells and
D := equal-prior record TV, consumed through SR's own module-level TV
function), record_partial_dephasing (the candidate x cell index set, the
record-cell dephasing, and the record-blind spanning set, consumed through
PD's own module-level machinery), and extended_carrier_elliptope (PSD
membership at fixed diagonal and principal minors, consumed through EE's own
module-level functions).  Two further consumptions, also by value and
disclosed at their sites: candidate_family_overlap (the banked family
the T5 capacity control executes on) and _module_manifest (the live
registration surface the T5 registration-shape control reads).
Nothing physical is claimed anywhere.

THE TWO QUANTITIES, defined here over that model and nowhere else:
  D  := the equal-prior record TV of the instance pair (p, q), computed by
        stochastic_record's own module-level function (the SR pin, consumed
        as a pin, never re-derived);
  V  := the matched-cell coherence magnitude of a carrier on PD's candidate
        x cell index set: twice the sum over cells of the absolute
        cross-candidate matched-cell entry.  V is a magnitude functional of
        THIS model object.  It is NOT Englert's visibility and is not any
        quantum-mechanical quantity (the may-not-cite list bars exactly
        that identification; the pair shares a GENRE, nothing more).
A carrier for an instance is a symmetric exact-rational matrix on PD's
index set whose diagonal is the instance pair laid out at half weight per
candidate; carrier admissibility is EE membership (symmetric PSD at that
fixed diagonal), decided through EE's own membership function.

THE FIVE CHECKS (registered under bare-name keys per D6@2026-08-03).

T1 (check_T_full_record_forces_matched_zero).  On the banked SR instances
with D = 1 (D computed via SR's own TV function; the D = 1 set computed
set-exactly; nonempty enforced): every matched-cell coherence entry is
FORCED to zero cell-by-cell -- each nonzero trial entry fails EE's own
PSD/minor membership, the zero entry passes -- hence V = 0 at D = 1,
forced, not merely bounded.  The per-cell universal rides EE's banked PSD
necessity (the 2x2 principal minor), consumed as banked and exercised
here on a trial grid and at the full-carrier level.

T2 (check_T_full_record_record_blind_invisibility).  At D = 1 on PD's own
index set: every record-blind spanning unit (count enforced equal to PD's
own span formula) returns the same value on the carrier, on its dephasing
(PD's own operator by value), and on the carrier with surviving coherence
zeroed -- no record-blind observable reads any entry of the surviving
mismatched-cell coherence.  A statement about the banked MODEL only.

T3 (check_T_tradeoff_envelope).  The two-step chain, decided EXACTLY on
the banked instances: (i) V bounded through per-cell 2x2 minors (EE by
value); (ii) BC^2 + D^2 <= 1 with the general-k step NAMED classical
content (Cauchy-Schwarz), computed exactly per-instance -- exactly where
EE's own certified sqrt certifies every per-cell product, and by a nested
squared decision on the two-cell residual; composed corollary
V^2 + D^2 <= 1.  A saturating family is exhibited with EXACT equality
(counts enforced): the Pythagorean-parametrized flipped pairs, whose
carriers are rational rank-one EE members.  No universal beyond the
computed instances plus the named import.

T4 (check_T_linear_law_definite_records).  On the definite-record
(disjoint-firing) family consumed from SR by value: V + D = 1 exactly at
every member (the bound from the per-cell minor necessity, the
achievement from an exhibited exact-rational carrier), strictly inside
the quadratic envelope except at the endpoints (both computed); plus the
partial-record readable survivor -- at a computed 0 < D < 1 point the
matched-cell coherence lies in the record-blind algebra's reach (its
unit a record-blind spanning element, checked through PD's own pair
census), reads nonzero, and survives full dephasing exactly (PD's own
operator by value), with V = 1 - D achieved and V <= sqrt(1 - D^2)
decided exactly (squared decision, no floats).

T5 (check_T_tradeoff_controls).  Permanent controls, each computed:
(a) the prior-inclusive D variant (SR's own module-level function at SR's
own NC4 point) breaks BOTH law shapes by value -- the equal-prior pin is
load-bearing in the composed chain, not only in SR; (b) fiber-sign
blindness, SCOPED: carrier membership is preserved under every diagonal
sign conjugation with principal minors tied by value (EE's own machinery),
and the banked capacity functional's domain carries no fiber sign
(signature read + executed on the banked family) -- scoped to these
banked objects, never bank-wide; (c) a registration-shape control,
executed in its BANKED form (landing rewire v24.3.477, disclosed at the
leg): this module supplies no tradeoff quantity to any other module at
the bank's registration surface (exactly one register() in this module's
own source, its AST equal to the house pattern that supplies only this
module's own check table; the landing name present in
BANK_REGISTRY_MODULES exactly once and in neither other manifest list;
positive controls executed), with the limitation stated.

LEG INVENTORY (D7@2026-08-08, APPEND-AND-RECORD): _result() compares the
executed leg set against EXPECTED_LEGS set-exactly on the path a bank run
would execute; a mismatch contributes a failure reason and does not raise.
STANDING LIMIT, disclosed: this certifies that a declared leg EXECUTED,
not that it COULD HAVE FAILED; a computed verdict replaced by a constant
escapes it, as it escapes the raising form equally.

DISCLOSED LIMITATIONS AND RESIDUALS (battery genre).
  (1) Identity-grade legs are DISCLOSED as identities where they occur:
      the min/max route to 1 - D^2 is finite arithmetic of min, max and
      abs (it pins agreement of two independently coded routes through
      SR's own TV, not a fact about nature); the 2x2-minor value tie is
      an algebraic identity of symmetric matrices (its role is a value
      tie on EE's determinant, the EE3 precedent); the Pythagorean
      equality is a polynomial identity of the construction (the
      falsifiable content of that leg is membership, the D tie, and the
      family gates); the sign-conjugation minor tie is an exercised
      identity (the sign factors square out of every principal minor,
      the EE5 precedent) whose falsifiable clauses are diagonal
      preservation, non-vacuity, and membership execution.
  (2) Two-cell SR records are embedded on PD's fixed three-cell index
      set by zero-mass padding; the embedding is a construction choice
      of this module, disclosed as authored.  Record-level legs use the
      instance's own cells; carrier-level legs use the embedded set.
  (3) The exhibited carriers are authored witnesses; existence claims
      ("achieved", "exhibited") are exactly as strong as the executed
      witness, and no uniqueness is computed or claimed.
  (4) A coordinated multi-site edit of the V convention (its factor at
      the definition site AND at every closed-form tie site) is the
      standing coordinated-edit residual (disclosed; single-site edits
      of the factor or the abs are caught by the closed-form and
      sign-conjugation value ties).  A TRANSPOSED matched-position rule
      is a true invariance of the symmetric exhibited carriers together
      with PD's two-sided pair census, not a caught edit (demonstrated
      in the build battery and recorded there).
  (5) The T5 registration-shape control reads this module's own source
      and the live manifest; a future consumer importing this module
      directly, outside the bank's registration surface, is outside its
      reach (stated limitation).

MAY-NOT-CITE (the frozen surface's list, verbatim, binding, returned in
every record): carried in MAY_NOT_CITE below.
"""

import ast
import inspect
import os
from fractions import Fraction as F
from itertools import product

from apf import stochastic_record as _sr
from apf import record_partial_dephasing as _pd
from apf import extended_carrier_elliptope as _ee
from apf import hold_cost_dominance as _hcd
from apf import candidate_family_overlap as _cfo
from apf import _module_manifest as _mm

HELD_OUT_OF_THE_BANK = False  # BANKED v24.3.477 (2026-08-15); lifted by Ethan; register() below

CLAIM_SURFACE_SHA256 = (
    "a2bb003c8001e9647c9d26ae4fefe302c9101caabf800c6f05f56c89574ca7f2")

# The frozen surface's may-not-cite list, verbatim (the surface's own
# numbered clauses).
MAY_NOT_CITE = (
    "1. Any identification of V or D with Englert's visibility/"
    "distinguishability or any quantum-mechanical quantity -- the pair "
    "shares a GENRE, nothing more.",
    "2. \"Born is derived\", in any form.",
    "3. Any supply claim, read-channel claim, or formation-map claim.",
    "4. Anything for or against situational-S.",
    "5. Any unconditional physical collapse/measurement claim -- every "
    "sentence is about the banked SR/PD/EE model.",
    "6. Any claim that A1 forces or prices record fullness -- D = 1 is "
    "only ever the hypothesis of a conditional here.",
    "7. The close of the Situational Sign program, as if derived from "
    "this module.",
    "8. Any bank-wide universal without attribution scope.",
)

# ---------------------------------------------------------------------------
# authored inputs (disclosed, not discharged)
# ---------------------------------------------------------------------------

# The T1 trial grid: nonzero coherence trials, both signs (authored; the
# leg enforces non-emptiness and two-sidedness by computation).
T1_TRIALS = (F(1), F(-1), F(1, 2), F(-1, 2), F(1, 3), F(-1, 3))

# Carrier-level injection trials (authored; both signs).
INJECT_TRIALS = (F(1, 3), F(-1, 3))

# The D = 1 instance names this build expects SR's inventory to compute to
# (an authored expectation compared set-exactly against the computed set).
EXPECTED_D1_NAMES = ("disjoint_two_cell", "flipped_0", "firing_4")

# The subset of SR instances on which every per-cell product has an
# EE-certified exact square root (authored expectation; membership is
# COMPUTED via EE's own certified sqrt and compared set-exactly).
EXPECTED_EXACT_BC_NAMES = (
    "disjoint_two_cell", "firing_0", "firing_1", "firing_2", "firing_3",
    "firing_4", "flipped_0", "flipped_4", "identical_two_cell")

# The Pythagorean saturating family: authored integer parameter pairs
# (a, b).  Records p = (a^2, b^2)/g, q flipped, g = a^2 + b^2; the family
# gates (distinct D values, strictly interior D) are enforced in-leg.
PY_PARAMS = ((1, 2), (2, 3), (1, 3), (3, 4), (2, 5))

# The T4 survivor point: the median authored firing parameter (an authored
# choice; the leg enforces 0 < D < 1 by computation).
SURVIVOR_NAME = "firing_2"

# The registration-shape control checks both manifest spellings of the
# name this file takes at landing (D6@2026-08-03 both-spellings rule).
LANDING_MODULE_NAMES = ("record_coherence_tradeoff",
                        "apf.record_coherence_tradeoff")

EXPECTED_LEGS = {
    "check_T_full_record_forces_matched_zero": [
        "carrier_level_forcing_and_v_zero",
        "d1_set_computed_via_sr_tv_set_exact_nonempty",
        "matched_products_vanish_at_d1",
        "nonzero_trials_fail_ee_membership",
        "zero_entry_passes_and_minor_tied_by_value",
    ],
    "check_T_full_record_record_blind_invisibility": [
        "d1_carriers_valid_with_mismatched_coherence",
        "mismatched_unit_positive_control",
        "scope_of_the_statement_recorded",
        "span_count_enforced_equals_pd_formula",
        "three_way_agreement_on_every_spanning_unit",
    ],
    "check_T_tradeoff_envelope": [
        "cauchy_schwarz_named_bc_exact_where_certified",
        "composed_envelope_on_exhibited_carriers",
        "min_max_route_ties_sr_tv_identity_disclosed",
        "per_cell_minor_bound_ties_ee_by_value",
        "saturating_family_exact_equality",
        "two_cell_residual_nested_squared_decision",
    ],
    "check_T_linear_law_definite_records": [
        "achieving_carrier_v_plus_d_equals_one_exact",
        "firing_family_consumed_by_value",
        "matched_zeros_and_bound_give_v_le_one_minus_d",
        "partial_record_readable_survivor",
        "strictly_inside_envelope_except_endpoints",
    ],
    "check_T_tradeoff_controls": [
        "capacity_domain_carries_no_fiber_sign_scoped",
        "fiber_sign_membership_preserved_minors_tied_scoped",
        "prior_inclusive_breaks_both_law_shapes_at_nc4",
        "registration_shape_no_supply_executed_scoped",
    ],
}


# ---------------------------------------------------------------------------
# result plumbing (append-and-record leg inventory, sited in the per-check
# result assembly a bank run would execute -- D7@2026-08-08)
# ---------------------------------------------------------------------------

def _result(name, legs, key_result, dependencies=(), cross_refs=(),
            disclosures=(), named_imports=()):
    fails = []
    have = tuple(sorted(legs))
    want = tuple(EXPECTED_LEGS[name])
    if have != want:
        missing = sorted(set(want) - set(have))
        extra = sorted(set(have) - set(want))
        fails.append(
            "leg inventory mismatch: missing=%r extra=%r" % (missing, extra))
    for label in sorted(legs):
        ok, ev = legs[label]
        if not ok:
            fails.append("%s: %s" % (label, ev))
    return {
        "name": name,
        "passed": not fails,
        "tier": 3,
        "epistemic": "P_math",
        "genre_note": (
            "theorem over the banked SR/PD/EE model: every sentence is "
            "about those model objects; V and D are quantities of this "
            "model, not physical or quantum-mechanical quantities; no "
            "physics claimed"),
        "legs": {k: {"passed": bool(v[0]), "evidence": v[1]}
                 for k, v in legs.items()},
        "leg_count": len(legs),
        "fail_reasons": fails,
        "key_result": key_result,
        "conditional_on": [
            "the banked SR/PD/EE model objects (stochastic_record, "
            "record_partial_dephasing, extended_carrier_elliptope), "
            "consumed by value; their premises and authored inputs are "
            "inherited, not discharged",
        ] + list(named_imports),
        "authored_inputs": [
            "the trial grids", "the D=1 and exact-BC name expectations",
            "the Pythagorean family parameters", "the survivor point",
            "the zero-mass embedding of two-cell records on PD's index set",
            "every exhibited carrier",
        ],
        "dependencies": list(dependencies),
        "cross_refs": list(cross_refs),
        "disclosures": list(disclosures),
        "may_not_cite": list(MAY_NOT_CITE),
        "held_out_of_the_bank": HELD_OUT_OF_THE_BANK,
        "frozen_claim_surface_sha256": CLAIM_SURFACE_SHA256,
        "inventory_note": (
            "append-and-record (D7@2026-08-08): certifies a declared leg "
            "EXECUTED, not that it could have failed"),
    }


def _no_float(values):
    return all(isinstance(v, F) for v in values)


# ---------------------------------------------------------------------------
# model glue: thin compositions of the consumed modules' own machinery
# (nothing banked is re-implemented; EE/PD/SR functions are the routes)
# ---------------------------------------------------------------------------

def _D_of(p, q):
    """D of a record pair: the equal-prior record TV, consumed from
    stochastic_record's own module-level function BY VALUE (the SR pin,
    consumed as a pin)."""
    return _sr._tv(p, q)


def _embed(w):
    """Zero-mass padding of a record onto PD's fixed cell count (authored
    construction choice, disclosed)."""
    w = tuple(w)
    assert len(w) <= _pd.N_CELL
    return w + (F(0),) * (_pd.N_CELL - len(w))


def _carrier_diag(p, q):
    """The carrier diagonal for an instance pair: each candidate's record
    at half weight, laid out by PD's own index map."""
    p3, q3 = _embed(p), _embed(q)
    d = [F(0)] * _pd.DIM
    for k in range(_pd.N_CELL):
        d[_pd._flat(0, k)] = p3[k] / 2
        d[_pd._flat(1, k)] = q3[k] / 2
    return tuple(d)


def _matched_positions():
    """The cross-candidate matched-cell positions, via PD's own index map."""
    return [(_pd._flat(0, k), _pd._flat(1, k)) for k in range(_pd.N_CELL)]


def _V(rho):
    """V of a carrier: twice the sum over cells of the absolute
    cross-candidate matched-cell entry.  A magnitude functional of this
    model object (not Englert's visibility; the may-not-cite list bars
    that identification)."""
    return 2 * sum(abs(rho[i][j]) for (i, j) in _matched_positions())


def _zero_mismatched(rho):
    """The carrier with every cell-mismatched entry zeroed (an independent
    entrywise second route beside PD's dephasing, so the T2 agreement is
    a tie of two code paths plus PD's own operator)."""
    return [[rho[i][j]
             if _pd._cell_of(i) == _pd._cell_of(j) else F(0)
             for j in range(_pd.DIM)] for i in range(_pd.DIM)]


def _pure_carrier(n_vec):
    """A rank-one carrier from an integer amplitude vector, normalized by
    its own squared length: exact rationals via EE's own rank-one
    constructor and PD's own scaling."""
    n_vec = tuple(F(x) for x in n_vec)
    norm = sum(x * x for x in n_vec)
    return _pd._scal(F(1) / norm, _ee.rank_one(n_vec))


def _d1_carrier(name, ins):
    """The exhibited D = 1 carrier for a named SR instance: a rank-one
    member whose diagonal is the instance pair and whose only coherence
    is cell-mismatched (the amplitude vector puts the two candidates'
    unit masses at their own -- disjoint -- cells)."""
    p3, q3 = _embed(ins[name]["p"]), _embed(ins[name]["q"])
    ku = next(k for k in range(_pd.N_CELL) if p3[k] == F(1))
    kv = next(k for k in range(_pd.N_CELL) if q3[k] == F(1))
    n_vec = [0] * _pd.DIM
    n_vec[_pd._flat(0, ku)] = 1
    n_vec[_pd._flat(1, kv)] = 1
    return _pure_carrier(n_vec)


def _py_record(a, b):
    """The Pythagorean record pair for authored integers (a, b)."""
    g = F(a * a + b * b)
    p = (F(a * a) / g, F(b * b) / g)
    q = (F(b * b) / g, F(a * a) / g)
    return p, q, g


def _py_carrier(a, b):
    """The Pythagorean rank-one carrier: amplitudes (a, b) for candidate
    u and (b, a) for candidate v on the first two cells."""
    n_vec = [0] * _pd.DIM
    n_vec[_pd._flat(0, 0)] = a
    n_vec[_pd._flat(0, 1)] = b
    n_vec[_pd._flat(1, 0)] = b
    n_vec[_pd._flat(1, 1)] = a
    return _pure_carrier(n_vec)


def _half_coherence(rho):
    """The entrywise half-coherence of a carrier: off-diagonal entries
    halved, diagonal kept (authored non-saturating tie witness for T3's
    minor-tie loop; EE membership is decided in-leg, not assumed)."""
    return [[rho[i][j] if i == j else rho[i][j] / 2
             for j in range(_pd.DIM)] for i in range(_pd.DIM)]


def _firing_carrier(s):
    """The exhibited disjoint-firing carrier at parameter s: each
    candidate's firing mass on its own cell, the shared no-fire mass in
    a rank-one cross-candidate block on the shared cell."""
    rho = _pd._zeros(_pd.DIM)
    i00, i11 = _pd._flat(0, 0), _pd._flat(1, 1)
    i02, i12 = _pd._flat(0, 2), _pd._flat(1, 2)
    rho[i00][i00] = s / 2
    rho[i11][i11] = s / 2
    rho[i02][i02] = (1 - s) / 2
    rho[i12][i12] = (1 - s) / 2
    rho[i02][i12] = (1 - s) / 2
    rho[i12][i02] = (1 - s) / 2
    return rho


def _own_tree():
    path = os.path.abspath(__file__)
    with open(path, "r", encoding="utf-8") as fh:
        src = fh.read()
    return ast.parse(src), path


# ---------------------------------------------------------------------------
# T1 -- full record forces matched-cell zero
# ---------------------------------------------------------------------------

def check_T_full_record_forces_matched_zero():
    legs = {}
    ins = _sr._instances()

    d1 = sorted(n for n in ins
                if _D_of(ins[n]["p"], ins[n]["q"]) == F(1))
    want = sorted(EXPECTED_D1_NAMES)
    inv_ok = sorted(ins) == sorted(_sr.EXPECTED_INSTANCE_NAMES)
    ok = (d1 == want and len(d1) > 0 and inv_ok)
    legs["d1_set_computed_via_sr_tv_set_exact_nonempty"] = (ok, (
        "the D = 1 instance set is computed over SR's own full inventory "
        "(inventory recount set-exact against SR's declared names, %d "
        "members) with D through SR's own module-level TV function by "
        "value; the computed set (%r, %d members, nonempty enforced) "
        "equals the authored expectation set-exactly, compared as sorted "
        "lists in both directions" % (len(ins), d1, len(d1))))

    n_cells = 0
    ok = True
    for name in d1:
        rec = ins[name]
        for k in range(len(rec["cells"])):
            if rec["p"][k] * rec["q"][k] != F(0):
                ok = False
            n_cells += 1
    ok = ok and n_cells == sum(len(ins[n]["cells"]) for n in d1) > 0
    legs["matched_products_vanish_at_d1"] = (ok, (
        "at every matched cell of every D = 1 instance (the instance's "
        "own cells; %d cells total, count enforced against the summed "
        "inventory and nonzero), the per-cell product p_k * q_k computes "
        "to zero exactly -- disjoint support cell-by-cell, the hypothesis "
        "the forcing below consumes; DISCLOSED: for normalized record "
        "pairs D = 1 forces disjoint supports, so given the previous leg "
        "this one is near-implied -- its executed value re-verifies the "
        "classification, the identity-leg genre" % n_cells))

    two_sided = (any(t > 0 for t in T1_TRIALS)
                 and any(t < 0 for t in T1_TRIALS))
    n_fail = 0
    ok = len(T1_TRIALS) > 0 and two_sided and all(t != 0 for t in T1_TRIALS)
    for name in d1:
        rec = ins[name]
        for k in range(len(rec["cells"])):
            dk = (rec["p"][k], rec["q"][k])
            for t in T1_TRIALS:
                W = _ee.ext_matrix(dk, {(0, 1): t})
                if _ee.in_extended_elliptope(W, dk):
                    ok = False
                n_fail += 1
    ok = ok and n_fail == n_cells * len(T1_TRIALS)
    legs["nonzero_trials_fail_ee_membership"] = (ok, (
        "every nonzero trial coherence entry at every matched cell of "
        "every D = 1 instance fails EE's own PSD/minor membership at the "
        "fixed two-cell diagonal (p_k, q_k): %d rejections (count "
        "enforced == cells x trials), trial grid nonempty with both "
        "signs present (computed); membership decided through EE's own "
        "in_extended_elliptope, nothing re-implemented" % n_fail))

    n_pass = 0
    n_tie = 0
    ok = True
    for name in d1:
        rec = ins[name]
        for k in range(len(rec["cells"])):
            dk = (rec["p"][k], rec["q"][k])
            W0 = _ee.ext_matrix(dk, {(0, 1): F(0)})
            if not _ee.in_extended_elliptope(W0, dk):
                ok = False
            n_pass += 1
            for t in T1_TRIALS + (F(0),):
                W = _ee.ext_matrix(dk, {(0, 1): t})
                m2 = _ee.det(_ee.submatrix(W, (0, 1)))
                if m2 != dk[0] * dk[1] - t * t:
                    ok = False
                n_tie += 1
    ok = (ok and n_pass == n_cells
          and n_tie == n_cells * (len(T1_TRIALS) + 1))
    legs["zero_entry_passes_and_minor_tied_by_value"] = (ok, (
        "the zero entry passes EE membership at every matched cell (%d "
        "passes, count enforced), so zero is forced rather than the set "
        "being empty; and at every trial (including zero; %d ties, count "
        "enforced) the deciding 2x2 principal minor computed through EE's "
        "own det/submatrix equals p_k q_k - t^2 by value -- DISCLOSED: "
        "that equality is an algebraic identity of symmetric matrices "
        "(the EE3 precedent); its role here is a value tie on EE's "
        "determinant route, and the falsifiable content of this leg is "
        "the membership verdict pattern" % (n_pass, n_tie)))

    n_car = 0
    n_inj = 0
    ok = True
    for name in d1:
        rho = _d1_carrier(name, ins)
        diag = _carrier_diag(ins[name]["p"], ins[name]["q"])
        if not _ee.in_extended_elliptope(rho, diag):
            ok = False
        if _V(rho) != F(0):
            ok = False
        n_car += 1
        for (i, j) in _matched_positions():
            for t in INJECT_TRIALS:
                Wt = [row[:] for row in rho]
                Wt[i][j] = t
                Wt[j][i] = t
                if _ee.in_extended_elliptope(Wt, diag):
                    ok = False
                n_inj += 1
    ok = (ok and n_car == len(d1)
          and n_inj == len(d1) * len(_matched_positions())
          * len(INJECT_TRIALS)
          and len(INJECT_TRIALS) > 0
          and any(t > 0 for t in INJECT_TRIALS)
          and any(t < 0 for t in INJECT_TRIALS))
    legs["carrier_level_forcing_and_v_zero"] = (ok, (
        "the forcing exercised at the full-carrier level: for each D = 1 "
        "instance (%d carriers) an exhibited mismatched-coherence "
        "carrier IS an EE member at the instance diagonal with V "
        "computed exactly zero, and injecting any nonzero trial at any "
        "matched position (%d injections, count enforced == carriers x "
        "matched positions x trials, both signs) breaks EE membership -- "
        "so V = 0 at D = 1 is forced, not merely bounded: the per-cell "
        "universal rides EE's banked PSD necessity (the 2x2 principal "
        "minor), consumed as banked and exercised here on the trial "
        "grids; no claim beyond the banked model is made" % (n_car, n_inj)))

    return _result(
        "check_T_full_record_forces_matched_zero", legs,
        key_result=(
            "on the banked SR instances with D = 1 (D through SR's own TV "
            "function; the D = 1 set computed set-exactly, %d members, "
            "nonempty), every matched-cell coherence entry is forced to "
            "zero cell-by-cell: each nonzero trial entry fails EE's own "
            "PSD/minor membership and the zero entry passes, at the "
            "two-cell level and at the full-carrier level -- hence V = 0 "
            "at D = 1, forced, not merely bounded, on this model; D = 1 "
            "is the HYPOTHESIS of this conditional, never a forced or "
            "priced state of affairs" % len(d1)),
        dependencies=["T_stochastic_record_construction",
                      "L_record_endpoint_families",
                      "T_extended_carrier_elliptope",
                      "L_per_cell_minor_bound"],
        cross_refs=["L_record_distinguishability_equal_prior_TV"],
        disclosures=[
            "the trial grids are authored inputs (non-emptiness and "
            "two-sidedness enforced by computation)",
            "the 2x2 minor equality is a disclosed identity; the "
            "membership verdicts are the falsifiable content",
            "two-cell records are embedded on PD's index set by zero-mass "
            "padding at the carrier level (authored, disclosed)"])


# ---------------------------------------------------------------------------
# T2 -- record-blind invisibility of the surviving coherence at D = 1
# ---------------------------------------------------------------------------

def check_T_full_record_record_blind_invisibility():
    legs = {}
    ins = _sr._instances()
    d1 = sorted(n for n in ins
                if _D_of(ins[n]["p"], ins[n]["q"]) == F(1))

    carriers = {}
    n_car = 0
    ok = len(d1) > 0
    for name in d1:
        rho = _d1_carrier(name, ins)
        diag = _carrier_diag(ins[name]["p"], ins[name]["q"])
        mism = [(i, j) for i in range(_pd.DIM) for j in range(_pd.DIM)
                if _pd._cell_of(i) != _pd._cell_of(j)
                and rho[i][j] != F(0)]
        ok = (ok and _pd._tr(rho) == F(1)
              and tuple(rho[i][i] for i in range(_pd.DIM)) == diag
              and _ee.in_extended_elliptope(rho, diag)
              and len(mism) > 0
              and all(rho[i][j] == F(0)
                      for (i, j) in _matched_positions()))
        carriers[name] = (rho, mism)
        n_car += 1
    ok = ok and n_car == len(d1)
    legs["d1_carriers_valid_with_mismatched_coherence"] = (ok, (
        "for every D = 1 instance (%d carriers, count enforced): the "
        "exhibited carrier has trace one, its diagonal ties the instance "
        "pair by value entry-by-entry (each candidate's record at half "
        "weight via PD's own index map), it is an EE member at that "
        "diagonal (EE's own membership function), its matched-cell "
        "coherence is exactly zero, and its MISMATCHED-cell coherence is "
        "enforced nonzero -- the invisibility below is non-vacuous"
        % n_car))

    blind = _pd._record_blind_pairs(_pd.P_FINE)
    span = _pd._span_formula(_pd.P_FINE)
    ok = (len(blind) == span and span > 0)
    legs["span_count_enforced_equals_pd_formula"] = (ok, (
        "the record-blind spanning set at the full record resolution is "
        "PD's own pair census (%d units), and its count is enforced "
        "equal to PD's own span formula (%d) -- two PD routes, one "
        "value, both consumed" % (len(blind), span)))

    n_reads = 0
    ok = True
    for name in d1:
        rho, _mism = carriers[name]
        Drho = _pd._D(rho, _pd.P_FINE)
        rho_z = _zero_mismatched(rho)
        for (pp, qq) in sorted(blind):
            A = _pd._unit(pp, qq, _pd.DIM)
            t1 = _pd._tr(_pd._mm(rho, A))
            t2 = _pd._tr(_pd._mm(Drho, A))
            t3 = _pd._tr(_pd._mm(rho_z, A))
            if not (t1 == t2 == t3 and _no_float([t1, t2, t3])):
                ok = False
            n_reads += 1
    ok = ok and n_reads == len(d1) * span
    legs["three_way_agreement_on_every_spanning_unit"] = (ok, (
        "every record-blind spanning unit returns the same value on the "
        "carrier, on its dephasing computed through PD's own operator at "
        "the full record resolution, and on the carrier with all "
        "mismatched-cell coherence zeroed by an independent entrywise "
        "rule: %d three-way reads (count enforced == carriers x span "
        "formula), every value an exact Fraction -- so no spanning unit "
        "reads any entry of the surviving mismatched-cell coherence, and "
        "the extension from the executed spanning set to the full "
        "record-blind algebra is by linearity: that span-to-algebra step "
        "is the content of the banked L_record_blind_invisibility, named "
        "in this check's dependencies; on this model" % n_reads))

    n_pos = 0
    ok = True
    for name in d1:
        rho, mism = carriers[name]
        (i, j) = mism[0]
        A = _pd._unit(i, j, _pd.DIM)
        t_car = _pd._tr(_pd._mm(rho, A))
        t_zed = _pd._tr(_pd._mm(_zero_mismatched(rho), A))
        t_dep = _pd._tr(_pd._mm(_pd._D(rho, _pd.P_FINE), A))
        if not (t_car != F(0) and t_zed == F(0) and t_dep == F(0)):
            ok = False
        n_pos += 1
    ok = ok and n_pos == len(d1)
    legs["mismatched_unit_positive_control"] = (ok, (
        "positive control on every carrier (%d, count enforced): a "
        "mismatched-cell unit at an exhibited nonzero coherence position "
        "reads a nonzero value on the carrier and zero on both the "
        "dephasing and the zeroed carrier -- the surviving coherence is "
        "really present, and it is exactly the record-blind reads that "
        "cannot see it" % n_pos))

    span_recount = len(_pd._record_blind_pairs(_pd.P_FINE))
    ok = (span_recount == span and n_reads == n_car * span_recount
          and n_pos == n_car)
    legs["scope_of_the_statement_recorded"] = (ok, (
        "scope, recorded on recomputed counts (span recount %d ties the "
        "executed read counts, enforced): this is a statement about the "
        "banked SR/PD/EE MODEL only -- carriers on PD's index set, PD's "
        "dephasing, PD's record-blind span; it is not a physical, "
        "measurement, or collapse claim, and it is not a bank-wide "
        "universal" % span_recount))

    return _result(
        "check_T_full_record_record_blind_invisibility", legs,
        key_result=(
            "at D = 1 on PD's own index set, every record-blind spanning "
            "unit (count enforced equal to PD's own span formula, %d) "
            "returns the same value on the carrier, on its dephasing "
            "through PD's own operator, and on the carrier with the "
            "surviving mismatched-cell coherence zeroed -- %d three-way "
            "reads with a per-carrier positive control; a statement "
            "about the banked model only" % (span, n_reads)),
        dependencies=["T_stochastic_record_construction",
                      "T_record_subsystem_partial_dephasing",
                      "L_record_blind_invisibility",
                      "T_extended_carrier_elliptope"],
        cross_refs=["T_full_record_forces_matched_zero",
                    "L_partial_dephasing_endpoints"],
        disclosures=[
            "the zeroed-carrier route is this module's independent "
            "entrywise second code path; PD's operator is the consumed "
            "machinery, so the agreement is a tie of two code paths "
            "plus the banked operator",
            "the exhibited carriers are authored witnesses (non-vacuity "
            "enforced in-leg)"])


# ---------------------------------------------------------------------------
# T3 -- the tradeoff envelope
# ---------------------------------------------------------------------------

def check_T_tradeoff_envelope():
    legs = {}
    ins = _sr._instances()

    # exhibited carriers: the Pythagorean family (records, carriers)
    py = []
    for (a, b) in PY_PARAMS:
        p, q, g = _py_record(a, b)
        py.append((a, b, p, q, g, _py_carrier(a, b)))

    (_a0, _b0, p0, q0, _g0, rho0) = py[0]
    tie_pool = [(p, q, rho, "sat") for (a, b, p, q, g, rho) in py]
    tie_pool.append((p0, q0, _half_coherence(rho0), "half"))
    n_tie = 0
    n_eq = 0
    n_eq_sat = 0
    n_strict = 0
    n_strict_half = 0
    ok = (len(py) == len(PY_PARAMS) > 0
          and len(tie_pool) == len(py) + 1)
    for (p, q, rho, tag) in tie_pool:
        diag = _carrier_diag(p, q)
        if not _ee.in_extended_elliptope(rho, diag):
            ok = False
        p3, q3 = _embed(p), _embed(q)
        for k, (i, j) in enumerate(_matched_positions()):
            x = rho[i][j]
            m2 = _ee.det(_ee.submatrix(rho, (i, j)))
            if m2 != p3[k] * q3[k] / 4 - x * x:
                ok = False
            if m2 < 0 or 4 * x * x > p3[k] * q3[k]:
                ok = False
            if m2 == 0:
                n_eq += 1
                if tag == "sat":
                    n_eq_sat += 1
            elif m2 > 0:
                n_strict += 1
                if tag == "half":
                    n_strict_half += 1
            n_tie += 1
    ok = (ok and n_tie == len(tie_pool) * len(_matched_positions())
          and n_eq + n_strict == n_tie
          and n_eq_sat == len(py) * len(_matched_positions())
          and n_strict == n_strict_half >= 1)
    legs["per_cell_minor_bound_ties_ee_by_value"] = (ok, (
        "V bounded through per-cell 2x2 minors on the exhibited carriers "
        "(%d matched-cell ties, count enforced == carriers x matched "
        "positions; the pool is the saturating family plus one authored "
        "non-saturating half-coherence carrier): each carrier is an EE "
        "member (EE's own membership function), the deciding minor "
        "computed through EE's own det/submatrix equals p_k q_k / 4 - "
        "x^2 by value (DISCLOSED identity of symmetric matrices; the "
        "tie is on EE's determinant route), and the squared per-cell "
        "bound 4 x^2 <= p_k q_k holds exactly at every cell; DISCLOSED, "
        "computed: the equality/strict partition of the tie sites is "
        "exhaustive (enforced): %d sites sit at exact equality, "
        "including every saturating-family site (%d, deciding minor "
        "identically zero there, enforced), and %d minors are strictly "
        "positive, every one on the authored half-coherence carrier "
        "(enforced >= 1) -- summing the "
        "certified per-cell bounds bounds V by BC on the exhibited "
        "carriers; the per-cell universal beyond them rides EE's banked "
        "PSD necessity, consumed as banked"
        % (n_tie, n_eq, n_eq_sat, n_strict)))

    n_seen = 0
    ok = True
    for name in sorted(ins):
        rec = ins[name]
        d = _D_of(rec["p"], rec["q"])
        s_min = sum(min(x, y) for x, y in zip(rec["p"], rec["q"]))
        s_max = sum(max(x, y) for x, y in zip(rec["p"], rec["q"]))
        if not (s_min + s_max == F(2)
                and s_min == 1 - d
                and s_min * s_max == 1 - d * d
                and _no_float([d, s_min, s_max])):
            ok = False
        n_seen += 1
    ok = ok and n_seen == len(_sr.EXPECTED_INSTANCE_NAMES)
    legs["min_max_route_ties_sr_tv_identity_disclosed"] = (ok, (
        "on all %d banked SR instances (count enforced against SR's "
        "inventory): the min/max route computes sum-min + sum-max = 2, "
        "sum-min = 1 - D and (sum-min)(sum-max) = 1 - D^2 exactly, with "
        "D through SR's own TV function by value -- DISCLOSED as an "
        "arithmetic identity: this pins agreement of two independently "
        "coded routes (the min/max sums against SR's abs-route TV), not "
        "a fact about nature; it is the exact rational form the named "
        "Cauchy-Schwarz step below bounds BC against" % n_seen))

    exact_names = sorted(
        n for n in ins
        if all(_ee.certified_sqrt(x * y) is not None
               for x, y in zip(ins[n]["p"], ins[n]["q"])))
    want_exact = sorted(EXPECTED_EXACT_BC_NAMES)
    n_dec = 0
    ok = (exact_names == want_exact and len(exact_names) > 0
          and len(exact_names) < len(ins))
    for name in exact_names:
        rec = ins[name]
        d = _D_of(rec["p"], rec["q"])
        bc = sum(_ee.certified_sqrt(x * y)
                 for x, y in zip(rec["p"], rec["q"]))
        if not (F(0) <= bc <= F(1) and bc * bc + d * d <= F(1)
                and _no_float([bc, d])):
            ok = False
        n_dec += 1
    ok = ok and n_dec == len(exact_names)
    legs["cauchy_schwarz_named_bc_exact_where_certified"] = (ok, (
        "the general-k step BC^2 <= (sum-min)(sum-max) is NAMED classical "
        "content -- Cauchy-Schwarz, a named import at this site, not "
        "re-proved here; on the computed subset of instances where EE's "
        "own certified sqrt certifies every per-cell product (%d of %d, "
        "set-exact against the authored expectation in both directions, "
        "nonempty and proper), "
        "BC is computed exactly and BC^2 + D^2 <= 1 is decided by value "
        "per instance (%d decisions, count enforced)"
        % (len(exact_names), len(ins), n_dec)))

    residual = sorted(set(ins) - set(exact_names))
    n_res = 0
    n_res_strict = 0
    ok = all(len(ins[n]["cells"]) == 2 for n in residual) and len(residual) > 0
    for name in residual:
        rec = ins[name]
        d = _D_of(rec["p"], rec["q"])
        x0 = rec["p"][0] * rec["q"][0]
        x1 = rec["p"][1] * rec["q"][1]
        r_slack = (1 - d * d) - (x0 + x1)
        if not (r_slack >= 0 and 4 * x0 * x1 <= r_slack * r_slack
                and _no_float([d, x0, x1, r_slack])):
            ok = False
        if 4 * x0 * x1 < r_slack * r_slack:
            n_res_strict += 1
        n_res += 1
    ok = ok and n_res == len(residual) and n_res_strict >= 1
    legs["two_cell_residual_nested_squared_decision"] = (ok, (
        "the residual instances (%d, all two-cell, enforced) are decided "
        "exactly without floats by a nested squared decision: BC^2 <= "
        "1 - D^2 there is equivalent to the slack (1 - D^2) - (x0 + x1) "
        "being nonnegative with 4 x0 x1 <= slack^2 (x_k the per-cell "
        "products), both decided as exact Fractions, with at least one "
        "residual member decided STRICTLY (%d strict, enforced "
        "nonzero) -- so BC^2 + D^2 <= 1 is decided exactly on EVERY "
        "banked instance, the certified subset by exact BC and the "
        "residual by squared decision; the general-k universal beyond "
        "these computed instances is the named import and nothing "
        "more" % (n_res, n_res_strict)))

    env = []
    for (a, b, p, q, g, rho) in py:
        env.append((rho, _D_of(p, q), "py"))
    for i, s in enumerate(_sr.FIRE_PARAMS):
        rec = ins["firing_%d" % i]
        env.append((_firing_carrier(s), _D_of(rec["p"], rec["q"]), "fire"))
    sig_flip = tuple(F(-1) if r == _pd._flat(1, 1) else F(1)
                     for r in range(_pd.DIM))
    base_rho, base_d, _ = env[0]
    rho_neg = _ee.conj_by_signs(base_rho, sig_flip)
    neg_entry = rho_neg[_pd._flat(0, 1)][_pd._flat(1, 1)]
    n_env = 0
    ok = (neg_entry < 0 and _V(rho_neg) == _V(base_rho))
    env.append((rho_neg, base_d, "py_conj"))
    for (rho, d, _tag) in env:
        v = _V(rho)
        if not (v >= 0 and v * v + d * d <= F(1) and _no_float([v, d])):
            ok = False
        n_env += 1
    ok = ok and n_env == len(PY_PARAMS) + len(_sr.FIRE_PARAMS) + 1
    legs["composed_envelope_on_exhibited_carriers"] = (ok, (
        "the composed corollary V^2 + D^2 <= 1 decided exactly on every "
        "exhibited carrier (%d carriers, count enforced: the Pythagorean "
        "family, the firing family, and a sign-conjugated Pythagorean "
        "member): V computed by the definition, D through SR's own TV; "
        "the conjugated member carries an exhibited NEGATIVE matched "
        "entry (%s, computed negative) and V ties the base carrier's V "
        "by value -- the abs in V is load-bearing and exercised; no "
        "universal over carriers beyond the per-cell minor route is "
        "claimed" % (n_env, neg_entry)))

    n_sat = 0
    d_vals = []
    ok = len(py) == len(PY_PARAMS)
    for (a, b, p, q, g, rho) in py:
        d = _D_of(p, q)
        v = _V(rho)
        bc = sum(_ee.certified_sqrt(x * y)
                 for x, y in zip(_embed(p), _embed(q)))
        closed_d = abs(F(a * a) - F(b * b)) / g
        closed_v = 2 * F(a * b) / g
        norm_ok = (sum(p) == F(1) and sum(q) == F(1)
                   and all(x >= 0 for x in p + q))
        if not (norm_ok and d == closed_d and v == closed_v == bc
                and v * v + d * d == F(1)
                and bc * bc + d * d == F(1)
                and F(0) < d < F(1)):
            ok = False
        d_vals.append(d)
        n_sat += 1
    ok = (ok and n_sat == len(PY_PARAMS)
          and len(set(d_vals)) == len(PY_PARAMS))
    legs["saturating_family_exact_equality"] = (ok, (
        "the saturating family, exhibited with EXACT equality: %d "
        "Pythagorean members (count enforced; D values %r pairwise "
        "distinct and strictly interior, enforced -- the family "
        "exercises the envelope's interior, not an endpoint), each a "
        "valid record pair (normalization and nonnegativity gated) with "
        "D through SR's own TV tied to the closed form from the authored "
        "integers, V computed equal to BC computed through EE's own "
        "certified sqrt, and V^2 + D^2 == 1 == BC^2 + D^2 exactly; "
        "DISCLOSED: the equality is a polynomial identity of the "
        "Pythagorean construction -- the falsifiable content is EE "
        "membership of each carrier (legged above), the SR TV ties, and "
        "the family gates" % (n_sat, [str(x) for x in d_vals])))

    return _result(
        "check_T_tradeoff_envelope", legs,
        key_result=(
            "the two-step chain, decided exactly on the banked "
            "instances: (i) V is bounded through per-cell 2x2 minors, EE "
            "by value, on the exhibited carriers; (ii) BC^2 + D^2 <= 1 "
            "with the general-k step named classical content "
            "(Cauchy-Schwarz), decided exactly on every banked instance "
            "(certified-sqrt subset by exact BC, two-cell residual by "
            "nested squared decision); composed corollary V^2 + D^2 <= 1 "
            "on every exhibited carrier; a saturating family exhibited "
            "with exact equality (%d members, counts enforced) -- all on "
            "the banked SR/PD/EE model, no universal beyond the computed "
            "instances plus the named import" % n_sat),
        dependencies=["T_stochastic_record_construction",
                      "L_record_distinguishability_equal_prior_TV",
                      "T_extended_carrier_elliptope",
                      "L_per_cell_minor_bound",
                      "L_rank_one_achievement"],
        cross_refs=["T_full_record_forces_matched_zero",
                    "T_linear_law_definite_records"],
        disclosures=[
            "the min/max identity leg and the 2x2 minor tie are "
            "disclosed identities (route agreement, not nature)",
            "the Pythagorean equality is a polynomial identity of the "
            "construction; membership, the TV ties, and the family "
            "gates are the falsifiable content",
            "Cauchy-Schwarz is a NAMED classical import at its one site "
            "of use; nothing beyond the computed instances rides it "
            "unattributed"],
        named_imports=[
            "Cauchy-Schwarz (classical), the general-k step of the "
            "BC-D inequality, NAMED at its site of use"])


# ---------------------------------------------------------------------------
# T4 -- the linear law on the definite-record (disjoint-firing) family
# ---------------------------------------------------------------------------

def check_T_linear_law_definite_records():
    legs = {}
    ins = _sr._instances()
    fire_names = ["firing_%d" % i for i in range(len(_sr.FIRE_PARAMS))]

    n_mem = 0
    ok = sorted(fire_names) == sorted(
        n for n in ins if n.startswith("firing_"))
    for i, s in enumerate(_sr.FIRE_PARAMS):
        rec = ins[fire_names[i]]
        d = _D_of(rec["p"], rec["q"])
        if not (d == s == rec["param"]
                and rec["cells"] == _sr.CELLS_FIRE
                and _no_float([d, s])):
            ok = False
        n_mem += 1
    ok = ok and n_mem == len(_sr.FIRE_PARAMS) > 0
    legs["firing_family_consumed_by_value"] = (ok, (
        "the disjoint-firing family consumed from SR by value: %d "
        "members (count enforced against SR's parameter tuple and "
        "against SR's inventory by name), each member's D computed "
        "through SR's own TV function equal to its own authored "
        "parameter, on SR's own firing cells -- SR's definite-record "
        "genre (each candidate's firing cell disjoint, the no-fire cell "
        "shared), nothing re-authored here" % n_mem))

    n_bound = 0
    n_rej = 0
    ok = True
    for i, s in enumerate(_sr.FIRE_PARAMS):
        rec = ins[fire_names[i]]
        p, q = rec["p"], rec["q"]
        s2 = _ee.certified_sqrt(p[2] * q[2])
        if not (p[0] * q[0] == F(0) and p[1] * q[1] == F(0)
                and s2 == 1 - s):
            ok = False
        n_bound += 1
        dk = (p[0], q[0])
        for t in INJECT_TRIALS:
            W = _ee.ext_matrix(dk, {(0, 1): t})
            if _ee.in_extended_elliptope(W, dk):
                ok = False
            n_rej += 1
    ok = (ok and n_bound == len(_sr.FIRE_PARAMS)
          and n_rej == len(_sr.FIRE_PARAMS) * len(INJECT_TRIALS))
    legs["matched_zeros_and_bound_give_v_le_one_minus_d"] = (ok, (
        "the bound side, per member (%d members): the firing-cell "
        "products compute to zero exactly and the no-fire-cell product's "
        "EE-certified sqrt computes to 1 - s exactly, so the per-cell "
        "minor necessity (EE, consumed as banked; exercised here by %d "
        "trial rejections at a firing cell, count enforced) gives "
        "V <= (1 - s) = 1 - D for every EE-member carrier at the member "
        "diagonal -- the same banked necessity T1 rides, composed with "
        "the exact per-cell sqrt certificates" % (n_bound, n_rej)))

    n_ach = 0
    ok = True
    for i, s in enumerate(_sr.FIRE_PARAMS):
        rec = ins[fire_names[i]]
        rho = _firing_carrier(s)
        diag = _carrier_diag(rec["p"], rec["q"])
        d = _D_of(rec["p"], rec["q"])
        v = _V(rho)
        if not (_pd._tr(rho) == F(1)
                and tuple(rho[r][r] for r in range(_pd.DIM)) == diag
                and _ee.in_extended_elliptope(rho, diag)
                and v == 1 - s
                and v + d == F(1)
                and _no_float([v, d])):
            ok = False
        n_ach += 1
    ok = ok and n_ach == len(_sr.FIRE_PARAMS)
    legs["achieving_carrier_v_plus_d_equals_one_exact"] = (ok, (
        "the achievement side, per member (%d carriers, count enforced): "
        "an exhibited exact-rational carrier with trace one, diagonal "
        "tied to the member pair by value, EE membership through EE's "
        "own function, and V computed equal to 1 - s exactly -- so "
        "V + D = 1 EXACTLY at every member of the definite-record "
        "family, bound and achievement both computed" % n_ach))

    interior = sorted(fire_names[i]
                      for i, s in enumerate(_sr.FIRE_PARAMS)
                      if F(0) < s < F(1))
    endpoints = sorted(fire_names[i]
                       for i, s in enumerate(_sr.FIRE_PARAMS)
                       if s == F(0) or s == F(1))
    n_env = 0
    ok = (len(interior) > 0 and len(endpoints) > 0
          and sorted(interior + endpoints) == sorted(fire_names))
    for i, s in enumerate(_sr.FIRE_PARAMS):
        name = fire_names[i]
        rec = ins[name]
        d = _D_of(rec["p"], rec["q"])
        v = _V(_firing_carrier(s))
        lhs = v * v + d * d
        if name in interior and not lhs < F(1):
            ok = False
        if name in endpoints and lhs != F(1):
            ok = False
        n_env += 1
    ok = ok and n_env == len(_sr.FIRE_PARAMS)
    legs["strictly_inside_envelope_except_endpoints"] = (ok, (
        "the linear law sits strictly inside the quadratic envelope "
        "except at the endpoints, both computed: on the %d interior "
        "members (%r; both partitions computed from the parameter "
        "values, jointly exhaustive enforced) V^2 + D^2 < 1 strictly, "
        "and on the %d endpoint members (%r) V^2 + D^2 == 1 exactly"
        % (len(interior), interior, len(endpoints), endpoints)))

    rec = ins[SURVIVOR_NAME]
    s = rec["param"]
    rho = _firing_carrier(s)
    d = _D_of(rec["p"], rec["q"])
    v = _V(rho)
    (i2, j2) = _matched_positions()[2]
    blind = _pd._record_blind_pairs(_pd.P_FINE)
    A = _pd._unit(i2, j2, _pd.DIM)
    read_val = _pd._tr(_pd._mm(rho, A))
    Drho = _pd._D(rho, _pd.P_FINE)
    read_dep = _pd._tr(_pd._mm(Drho, A))
    ok = (F(0) < d < F(1)
          and (i2, j2) in blind
          and read_val == rho[j2][i2] != F(0)
          and Drho[i2][j2] == rho[i2][j2]
          and read_dep == read_val
          and v == 1 - d
          and v >= 0 and v * v <= 1 - d * d
          and v * v < 1 - d * d
          and _no_float([d, v, read_val]))
    legs["partial_record_readable_survivor"] = (ok, (
        "the partial-record readable survivor at the authored member "
        "(D = %s computed, strictly interior enforced): the matched-cell "
        "coherence unit at the shared no-fire cell IS a record-blind "
        "spanning element (membership checked in PD's own pair census by "
        "value), it reads the value %s on the carrier -- nonzero -- the "
        "entry survives PD's full dephasing exactly (PD's own operator, "
        "entry and read both tied by value), V = 1 - D = %s is achieved, "
        "and V <= sqrt(1 - D^2) is decided exactly by squared decision "
        "(V >= 0 and V^2 <= 1 - D^2, here strict), no floats anywhere"
        % (d, read_val, v)))

    return _result(
        "check_T_linear_law_definite_records", legs,
        key_result=(
            "on the definite-record (disjoint-firing) family consumed "
            "from SR by value (%d members): V + D = 1 exactly at every "
            "member -- the bound from the per-cell minor necessity (EE "
            "by value) and the achievement from exhibited exact-rational "
            "carriers -- strictly inside the quadratic envelope except "
            "at the endpoints, both computed; and at a computed "
            "0 < D < 1 point the matched-cell coherence lies in the "
            "record-blind algebra's reach, reads nonzero, and survives "
            "full dephasing exactly, with V = 1 - D achieved and "
            "V <= sqrt(1 - D^2) decided by squared decision; all on the "
            "banked model" % n_mem),
        dependencies=["T_stochastic_record_construction",
                      "L_record_endpoint_families",
                      "T_record_subsystem_partial_dephasing",
                      "L_partial_dephasing_endpoints",
                      "T_extended_carrier_elliptope",
                      "L_per_cell_minor_bound"],
        cross_refs=["T_tradeoff_envelope",
                    "L_record_blind_invisibility"],
        disclosures=[
            "the survivor point is an authored choice among the interior "
            "members (interiority enforced by computation)",
            "the achieving carriers are authored witnesses; no "
            "uniqueness is computed or claimed",
            "'definite record' names SR's disjoint-firing genre on this "
            "model; no physical measurement claim is made"])


# ---------------------------------------------------------------------------
# T5 -- permanent controls
# ---------------------------------------------------------------------------

def check_T_tradeoff_controls():
    legs = {}

    # (a) the prior-inclusive variant breaks BOTH law shapes at SR's own
    # NC4 point (control genre: wrong-definition break, computed)
    d_w = _sr._dw(_sr.NC4_PRIOR_U, _sr.NC4_PRIOR_V, _sr.NC4_P, _sr.NC4_Q)
    d_true = _D_of(_sr.NC4_P, _sr.NC4_Q)
    n_vec = [0] * _pd.DIM
    n_vec[_pd._flat(0, 0)] = 1
    n_vec[_pd._flat(0, 1)] = 1
    n_vec[_pd._flat(1, 0)] = 1
    n_vec[_pd._flat(1, 1)] = 1
    rho = _pure_carrier(n_vec)
    diag = _carrier_diag(_sr.NC4_P, _sr.NC4_Q)
    v = _V(rho)
    ok = (d_true == F(0) and d_w != F(0) and d_w != d_true
          and tuple(rho[r][r] for r in range(_pd.DIM)) == diag
          and _ee.in_extended_elliptope(rho, diag)
          and v * v + d_true * d_true <= F(1)
          and v + d_true == F(1)
          and v * v + d_w * d_w > F(1)
          and v + d_w != F(1)
          and _no_float([d_w, d_true, v]))
    legs["prior_inclusive_breaks_both_law_shapes_at_nc4"] = (ok, (
        "at SR's own NC4 point (priors %s and %s, identical records; "
        "constants and both D routes consumed from SR's own module "
        "level): the pinned D computes to %s and the prior-inclusive "
        "variant to %s; on the exhibited maximal-coherence carrier "
        "(V = %s, an EE member at the NC4 diagonal) BOTH composed law "
        "shapes hold with the pinned D (V^2 + D^2 <= 1 and V + D == 1, "
        "computed) and BOTH break with the variant in D's slot "
        "(V^2 + D_w^2 = %s > 1 and V + D_w = %s != 1, computed) -- the "
        "equal-prior pin is load-bearing in the composed chain, not "
        "only in SR" % (_sr.NC4_PRIOR_U, _sr.NC4_PRIOR_V, d_true, d_w,
                        v, v * v + d_w * d_w, v + d_w)))

    # (b) fiber-sign blindness, SCOPED to these banked objects
    a, b = PY_PARAMS[0]
    p, q, g = _py_record(a, b)
    W = _py_carrier(a, b)
    diag_w = _carrier_diag(p, q)
    base_minors = _ee.principal_minor_list(W)
    sigmas = list(product((F(1), F(-1)), repeat=_pd.DIM))
    n_ties = 0
    n_mem = 0
    ok = len(sigmas) == 2 ** _pd.DIM
    for sigma in sigmas:
        WC = _ee.conj_by_signs(W, sigma)
        if tuple(WC[r][r] for r in range(_pd.DIM)) != diag_w:
            ok = False
        if not _ee.in_extended_elliptope(WC, diag_w):
            ok = False
        n_mem += 1
        for (S1, v1), (S2, v2) in zip(base_minors,
                                      _ee.principal_minor_list(WC)):
            if S1 != S2 or v1 != v2:
                ok = False
            n_ties += 1
    sig_mix = tuple(F(-1) if r == _pd._flat(0, 1) else F(1)
                    for r in range(_pd.DIM))
    WM = _ee.conj_by_signs(W, sig_mix)
    moved = [(r, c) for r in range(_pd.DIM) for c in range(_pd.DIM)
             if sig_mix[r] * sig_mix[c] == F(-1) and W[r][c] != F(0)]
    ok = (ok and n_mem == 2 ** _pd.DIM
          and n_ties == 2 ** _pd.DIM * len(base_minors)
          and len(moved) > 0
          and all(WM[r][c] == sig_mix[r] * sig_mix[c] * W[r][c]
                  for r in range(_pd.DIM) for c in range(_pd.DIM))
          and all(WM[r][c] != W[r][c] for (r, c) in moved))
    legs["fiber_sign_membership_preserved_minors_tied_scoped"] = (ok, (
        "fiber-sign blindness, SCOPED: on the exhibited carrier, "
        "membership at the fixed diagonal is preserved under every "
        "diagonal sign conjugation (%d conjugations through EE's own "
        "conjugation function, each membership through EE's own "
        "membership function; diagonal preservation computed) with "
        "every principal minor tied by value against the base (%d "
        "ties through EE's own minor list); DISCLOSED identity: the "
        "minor equality is an exercised identity (the sign factors "
        "square out of every principal minor, the EE5 precedent) -- "
        "the falsifiable clauses are diagonal preservation, membership "
        "execution, and NON-VACUITY, pinned here: a mixed sign vector "
        "moves %d nonzero cells with every conjugated entry equal to "
        "its predicted multiple by value; scoped to these banked "
        "objects, never bank-wide" % (n_mem, n_ties, len(moved))))

    # (b') the banked capacity functional's domain carries no fiber sign
    sig = inspect.signature(_hcd._cost)
    params = tuple(sig.parameters)
    members, _nulls, _inadm = _cfo.build_family()
    n_fam = 0
    n_elem = 0
    ok = (params == ("S",) and len(members) > 0)
    for anchor in sorted(members):
        cfg = members[anchor]
        c1 = _hcd._cost(cfg)
        c2 = _hcd._cost(cfg)
        if not (isinstance(c1, F) and c1 == c2
                and c1 <= _cfo.CAPACITY_C
                and isinstance(cfg, frozenset)):
            ok = False
        for e in cfg:
            if not (isinstance(e, tuple) and len(e) == 2
                    and isinstance(e[0], str)
                    and isinstance(e[1], int) and e[1] >= 0):
                ok = False
            n_elem += 1
        n_fam += 1
    ok = ok and n_fam == len(members) and n_elem > 0
    two_anchor = frozenset(_cfo.BASE_S) | {("c", 0), ("c", 1)}
    ok = ok and _hcd._cost(two_anchor) > _cfo.CAPACITY_C
    legs["capacity_domain_carries_no_fiber_sign_scoped"] = (ok, (
        "the banked capacity functional's domain carries no fiber sign, "
        "SCOPED: its signature reads a single parameter %r (read via "
        "inspect, not asserted), and it is EXECUTED on the banked "
        "family by value (%d members, count enforced; each cost an "
        "exact Fraction of the anchor-support frozenset alone, "
        "re-executed equal, admissible against the family's own "
        "capacity; a two-anchor rejection control computed); the "
        "domain datum is the support set, INSPECTED at the element "
        "level rather than read off the container type: every element "
        "of every executed support set (%d elements, nonzero enforced) "
        "computes to a (str label, nonnegative int index) pair -- no "
        "sign-typed datum among the executed elements; the carrier "
        "fiber signs of leg (b), which preserve every diagonal, never "
        "reach it; scoped to these banked objects, never bank-wide"
        % (list(params), n_fam, n_elem)))

    # (c) registration-shape: this module supplies no tradeoff quantity
    # to any other module at the bank's registration surface.
    # LANDING REWIRE (v24.3.477, 2026-08-15, disclosed; the v24.3.474
    # named-absence precedent): the held form of this leg asserted the
    # hold state itself (no module-level register(); the landing name
    # absent from the live manifest; the held flag True), and
    # registration inverts all three by construction.  The banked form
    # asserts the BANKED registration shape instead: exactly one
    # module-level register() whose AST equals the house pattern
    # (update the registry with this module's own check table and
    # return it -- check records, never a tradeoff quantity), the
    # landing name present in BANK_REGISTRY_MODULES exactly once and
    # in neither other manifest list, and the held flag False.  No
    # other executable content moved at landing.
    tree, _path = _own_tree()
    own_register_defs = [node for node in tree.body
                         if isinstance(node, ast.FunctionDef)
                         and node.name == "register"]
    synthetic = ast.parse("def register(registry):\n    return registry\n")
    synth_defs = [node for node in synthetic.body
                  if isinstance(node, ast.FunctionDef)
                  and node.name == "register"]
    house = ast.parse("def register(registry):\n"
                      "    registry.update(_CHECKS)\n"
                      "    return registry\n")
    house_shape = (len(own_register_defs) == 1
                   and ast.dump(own_register_defs[0])
                   == ast.dump(house.body[0])
                   and ast.dump(own_register_defs[0])
                   != ast.dump(synth_defs[0]))
    bank_list = tuple(_mm.BANK_REGISTRY_MODULES)
    other_lists = (tuple(_mm.ARCHITECTURE_ONLY_MODULES)
                   + tuple(_mm.STANDALONE_LEMMA_MODULES))
    present_once = (bank_list.count("apf.record_coherence_tradeoff") == 1
                    and "record_coherence_tradeoff" not in bank_list
                    and all(nm not in other_lists
                            for nm in LANDING_MODULE_NAMES))
    pos_control = "apf.stochastic_record" in bank_list
    ok = (house_shape and len(synth_defs) == 1
          and present_once and pos_control
          and len(bank_list) + len(other_lists) > 0
          and HELD_OUT_OF_THE_BANK is False)
    legs["registration_shape_no_supply_executed_scoped"] = (ok, (
        "registration-shape, executed in its BANKED form (landing "
        "rewire v24.3.477, disclosed above at the leg; no other "
        "executable content moved at landing): this module's own "
        "parsed source carries exactly one module-level register "
        "function and its AST equals the house pattern -- update the "
        "registry with this module's own check table and return it, "
        "so it supplies check records, never a tradeoff quantity "
        "(positive controls: the same collector finds a register in a "
        "synthetic source, and the synthetic body does NOT match the "
        "house pattern); the landing name is present in "
        "BANK_REGISTRY_MODULES exactly once under the dotted spelling "
        "and absent under the bare spelling, and absent from the "
        "architecture-only and standalone lists under both spellings "
        "(checked against %d manifest entries by value; positive "
        "control: a banked sibling IS present), and the held flag "
        "reads %r -- so this module supplies no tradeoff quantity to "
        "any other module at the bank's registration surface.  STATED "
        "LIMITATION: this control covers the registration surface and "
        "this file; a future consumer importing this module directly "
        "is outside its reach"
        % (len(bank_list) + len(other_lists), HELD_OUT_OF_THE_BANK)))

    return _result(
        "check_T_tradeoff_controls", legs,
        key_result=(
            "permanent controls, each computed: (a) the prior-inclusive "
            "D variant breaks BOTH composed law shapes at SR's own NC4 "
            "point by value while both hold with the pinned D -- the "
            "equal-prior pin is load-bearing in the composed chain; "
            "(b) fiber-sign blindness, scoped: carrier membership "
            "preserved under every diagonal sign conjugation with "
            "principal minors tied by value, and the banked capacity "
            "functional's domain (signature read, executed on the "
            "banked family) carries no fiber sign -- scoped to these "
            "banked objects; (c) registration-shape: this module "
            "supplies no tradeoff quantity to any other module at the "
            "bank's registration surface, executed with positive "
            "controls and a stated limitation"),
        dependencies=["L_record_distinguishability_equal_prior_TV",
                      "T_extended_elliptope_controls",
                      "T_hold_cost_dominance_split",
                      "CF1_candidate_family_construction"],
        cross_refs=["T_tradeoff_envelope",
                    "T_linear_law_definite_records",
                    "T_stochastic_record_controls"],
        disclosures=[
            "the sign-conjugation minor tie is a disclosed exercised "
            "identity; diagonal preservation, membership execution and "
            "non-vacuity are its falsifiable clauses",
            "the registration-shape control reads this file and the "
            "live manifest only; direct imports elsewhere are outside "
            "its reach (stated limitation)",
            "the registration-shape leg carries a disclosed landing "
            "rewire (v24.3.477): its held-state assertions inverted "
            "by construction at registration and the banked "
            "registration shape is asserted instead; no other "
            "executable content moved at landing",
            "the broken variant is computed only to be broken; it is "
            "not defined into this module's vocabulary"])


# ---------------------------------------------------------------------------
# check table + register() (bare-name keys per D6@2026-08-03) +
# standalone execution.  Registered at landing v24.3.477 (2026-08-15).
# ---------------------------------------------------------------------------

_CHECKS = {
    "T_full_record_forces_matched_zero":
        check_T_full_record_forces_matched_zero,
    "T_full_record_record_blind_invisibility":
        check_T_full_record_record_blind_invisibility,
    "T_tradeoff_envelope":
        check_T_tradeoff_envelope,
    "T_linear_law_definite_records":
        check_T_linear_law_definite_records,
    "T_tradeoff_controls":
        check_T_tradeoff_controls,
}


def run_all():
    return {name: fn() for name, fn in _CHECKS.items()}


def register(registry):
    registry.update(_CHECKS)
    return registry


if __name__ == "__main__":
    import sys
    results = run_all()
    n_pass = sum(1 for r in results.values() if r["passed"])
    n_legs = sum(r["leg_count"] for r in results.values())
    print("record_coherence_tradeoff: BANKED v24.3.477 "
          "(bare-name keys per D6@2026-08-03)")
    for name, r in results.items():
        status = "PASS" if r["passed"] else "FAIL"
        print("  [%s] %s (%d legs)" % (status, name, r["leg_count"]))
        for reason in r["fail_reasons"]:
            print("      FAIL: %s" % reason)
    print("%d/%d checks pass; %d legs" % (n_pass, len(results), n_legs))
    sys.exit(0 if n_pass == len(results) else 1)
