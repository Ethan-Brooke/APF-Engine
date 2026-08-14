"""The record-subsystem partial dephasing: a conditional expectation onto
record-blind observables when the record is a subsystem of a candidate x cell
index set.

BUILT 2026-08-14 by a cold build seat under the Supplier Search charter
(Phase 2, prerequisite 2 of 3; the object M2 names as absence C2), to the
FROZEN claim surface (binding; weaken with disclosure, strengthen nothing):
  Artifacts_2026-08-11_session/phase2_prereqs/
    CLAIM_SURFACE_PD_record_partial_dephasing_2026-08-14.md
  raw sha256: 8ed073de36fb1c5a938a1818faeead7ee9eba8ebc1909861a48ffcd3b6e7083b
The module may state nothing beyond that surface.  The Situational Sign
program fences (its section 4) bind in full.

WHAT THIS MODULE IS.  The banked lemma (the leg-(ii) dephasing of
L_commutative_no_unresolved_hold) covers the full-algebra case: the
conditional expectation D(rho) = sum_pi Q_pi rho Q_pi over a spectral
projection family, with the off-diagonal content invisible to the whole
algebra.  This module constructs the same mathematics when the record is a
SUBSYSTEM: on a candidate x cell index set, a record subsystem is a
resolution of the cell index set into record cells, and the partial
dephasing is D_R(rho) = sum_k (I (x) Q_k) rho (I (x) Q_k) over the
record-cell projections {Q_k} -- exact rational matrices throughout.
DEFINITIONAL: it supplies a map and its characterization and claims no
physics.

THE SUBSUMPTION QUESTION, asked first (build standard) and answered in
writing: the bank's nearest neighbors are the full-algebra dephasing
(L_commutative_no_unresolved_hold, leg (ii)), the sector-separation
re-derivation of that same full conditional expectation
(coherence_sector_separation), the restricted DIAGONAL conditional
expectation of the one-context one-transport criterion, and the
conditional-expectation chain-rule dichotomy of the delta calculus (which
takes conditional expectations as PRESENTATION inputs to a billing
question).  None constructs the record-SUBSYSTEM partial dephasing on a
candidate x cell index set, none states its fixed-point characterization,
endpoints, or refinement controls.  This is the chartered absence.

CHECKS (bare-name keys per D6@2026-08-03; tier 3; [P_math]; non-exporting):

  PD1  T_record_subsystem_partial_dephasing -- the construction on the
       candidate x cell index set; linearity / trace preservation /
       idempotence / unitality / positivity-on-instances legged BY VALUE;
       the conditional-expectation property computed (projection, algebra
       membership and multiplicative closure of the span; the module
       property over the full spanning-unit pair set at the exhibited
       state, middle-slot scope named in-leg); structural complete
       positivity NAMED as the [P_math] Kraus-form genre, not
       sampled-and-overclaimed.
  PD2  L_full_algebra_recovers_banked_dephasing -- when the record
       resolves the whole index set, D_R agrees with the banked leg-(ii)
       dephasing, tied through the sibling module's own module-level
       machinery BY VALUE.  DISCLOSED LIMITATION (per the frozen surface):
       the sibling's dephasing operator is defined INSIDE its check
       function and is not reachable module-level (computed in-leg), so
       the tie is (a) through the sibling's module-level matrix machinery
       on shared instances, and (b) to the sibling's executed record
       values recomputed on its own instance, reconstructed verbatim
       through its own module-level constructors.  Wrong-convention rivals
       fail the tie BY VALUE, not by verdict.
  PD3  L_record_blind_invisibility -- the fixed-point characterization
       (invariant iff cell-block-diagonal at the record-cell resolution)
       and the invisibility read (Tr(rho A) reads only matched-cell
       entries; mismatched-cell coherence contributes zero), computed over
       an EXACT SPANNING SET of the record-blind algebra, not sampled.
       This discharges the M2 audit's P2 finding, SCOPED to this index-set
       model -- never a bank-wide or physical universal.
  PD4  L_partial_dephasing_endpoints -- trivial record subsystem gives the
       identity (computed); full record gives the matched-cell restriction
       (computed, with within-cell candidate coherence surviving -- the
       subsystem point); a strictly partial record exhibited with
       surviving off-diagonal coherence, exactly.  No V law is stated.
  PD5  T_partial_dephasing_controls -- (a) the decoherence-control
       direction BY VALUE in both directions (refining strictly shrinks
       the surviving record-blind coherence functional; coarsening
       restores it exactly); (b) rival maps fail idempotence or the tie by
       value; (c) the no-sign-read scan and the form-(b) non-consumption
       scan, both executed and both SCOPED TO THIS MODULE.

LEG INVENTORY (D7@2026-08-08, APPEND-AND-RECORD): _result() compares the
executed leg set against EXPECTED_LEGS set-exactly on the path the bank
would execute; a mismatch contributes a failure reason and does not raise.
STANDING LIMIT, disclosed: this certifies that a declared leg EXECUTED,
not that it COULD HAVE FAILED.

MAY-NOT-CITE (binding; the frozen surface's list, carried):
- never a physical collapse or measurement claim;
- never anything for or against situational-S;
- never a formation-map or supplier claim;
- never a consumer claim on the form-(b) slot (the R-event-model's
  declared per-pair field): this module consumes nothing there;
- never the V^2+D^2 or V+D law (downstream, C8 chain);
- never a bank-wide universal (every statement is scoped to this
  index-set model);
- never an identification of the record subsystem with an environment;
- never "decoherence" as a physical process claim (the word names the
  control genre only).

This module describes what it COMPUTES.  Exact Fraction arithmetic only.
"""
from __future__ import annotations

import ast
import inspect
import os
from fractions import Fraction as F

from apf import commutative_no_unresolved_hold as _cnuh

# BANKED v24.3.476 (2026-08-14): built and held under the Supplier Search
# charter Phase 2, twice blind-audited, fixes carried, LIFTED by Ethan
# 2026-08-14; registered with bare-name keys per D6@2026-08-03.

HELD_OUT_OF_THE_BANK = False  # flipped at the 2026-08-14 lift; wiring edit

CLAIM_SURFACE_SHA256 = (
    "8ed073de36fb1c5a938a1818faeead7ee9eba8ebc1909861a48ffcd3b6e7083b")

MAY_NOT_CITE = (
    "any physical collapse or measurement claim",
    "anything for or against situational-S",
    "any formation-map or supplier claim",
    "any consumer claim on the form-(b) slot (the R-event-model's declared "
    "per-pair field): this module consumes nothing there",
    "the V^2+D^2 or V+D law (downstream, C8 chain): no V law is stated here",
    "any bank-wide universal (every statement is scoped to this index-set "
    "model)",
    "any identification of the record subsystem with an environment",
    "'decoherence' as a physical process claim (the word names the control "
    "genre only)",
)

# ---------------------------------------------------------------------------
# the exhibited index set (authored data, not derived figures)
# ---------------------------------------------------------------------------

N_CAND = 2                    # candidate-factor dimension (authored)
N_CELL = 3                    # cell-factor dimension (authored)
DIM = N_CAND * N_CELL

# record subsystems exhibited: resolutions of the cell index set into record
# cells (genre: the endpoint chain plus the strictly partial middle case)
P_TRIVIAL = (frozenset({0, 1, 2}),)
P_MID = (frozenset({0, 1}), frozenset({2}))
P_FINE = (frozenset({0}), frozenset({1}), frozenset({2}))


# ---------------------------------------------------------------------------
# exact matrix helpers (Fraction only; an independent code path from the
# sibling's helpers, so the PD2 tie compares two executions, not one)
# ---------------------------------------------------------------------------

def _mat(rows):
    return [[F(x) for x in r] for r in rows]


def _zeros(n):
    return [[F(0)] * n for _ in range(n)]


def _eye(n):
    return [[F(1) if i == j else F(0) for j in range(n)] for i in range(n)]


def _mm(A, B):
    n, m, p = len(A), len(B), len(B[0])
    return [[sum(A[i][k] * B[k][j] for k in range(m)) for j in range(p)]
            for i in range(n)]


def _add(A, B):
    return [[A[i][j] + B[i][j] for j in range(len(A[0]))]
            for i in range(len(A))]


def _sub(A, B):
    return [[A[i][j] - B[i][j] for j in range(len(A[0]))]
            for i in range(len(A))]


def _scal(c, A):
    return [[c * A[i][j] for j in range(len(A[0]))] for i in range(len(A))]


def _tr(A):
    return sum(A[i][i] for i in range(len(A)))


def _eq(A, B):
    return all(A[i][j] == B[i][j]
               for i in range(len(A)) for j in range(len(A[0])))


def _T(A):
    return [[A[j][i] for j in range(len(A))] for i in range(len(A[0]))]


def _is0(A):
    return all(A[i][j] == 0 for i in range(len(A)) for j in range(len(A[0])))


def _kron(A, B):
    na, nb = len(A), len(B)
    out = _zeros(na * nb)
    for i in range(na):
        for j in range(na):
            for k in range(nb):
                for l in range(nb):
                    out[i * nb + k][j * nb + l] = A[i][j] * B[k][l]
    return out


def _rank1(v):
    n = len(v)
    vv = sum(F(x) * F(x) for x in v)
    return [[F(v[i]) * F(v[j]) / vv for j in range(n)] for i in range(n)]


def _unit(p, q, n):
    M = _zeros(n)
    M[p][q] = F(1)
    return M


def _flat(c, k):
    return c * N_CELL + k


def _cell_of(p):
    return p % N_CELL


def _charpoly(A):
    """Exact characteristic polynomial coefficients (Faddeev-LeVerrier;
    genre: exact PSD certification for symmetric rational matrices)."""
    n = len(A)
    cs = [F(1)]
    Mk = None
    for k in range(1, n + 1):
        if Mk is None:
            Mk = [row[:] for row in A]
        else:
            Mk = _mm(A, _add(Mk, _scal(cs[-1], _eye(n))))
        cs.append(F(-1, k) * _tr(Mk))
    return cs


def _is_psd(A):
    """Symmetric exact PSD: the spectrum is real by symmetry, and PSD holds
    iff every elementary symmetric function of the eigenvalues is
    nonnegative -- read off the characteristic polynomial exactly."""
    n = len(A)
    if not _eq(_T(A), A):
        return False
    cs = _charpoly(A)
    return all((F(-1) ** k) * cs[k] >= 0 for k in range(1, n + 1))


# ---------------------------------------------------------------------------
# the record subsystem and its partial dephasing
# ---------------------------------------------------------------------------

def _cell_proj(block):
    E = _zeros(N_CELL)
    for k in block:
        E[k][k] = F(1)
    return E


def _record_projs(partition):
    """The record-cell projections {I (x) Q_k}: one per record cell."""
    return [_kron(_eye(N_CAND), _cell_proj(B)) for B in partition]


def _dephase_family(rho, projs):
    """The dephasing sum over an arbitrary projection family (the leg-(ii)
    form; PD2 ties this to the banked sibling by value)."""
    out = _zeros(len(rho))
    for Q in projs:
        out = _add(out, _mm(_mm(Q, rho), Q))
    return out


def _D(rho, partition):
    return _dephase_family(rho, _record_projs(partition))


def _record_blind_pairs(partition):
    """Index pairs whose cell indices share a record cell: the matrix units
    at exactly these positions span the record-blind algebra."""
    pairs = []
    for p in range(DIM):
        for q in range(DIM):
            if any(_cell_of(p) in B and _cell_of(q) in B for B in partition):
                pairs.append((p, q))
    return pairs


def _span_formula(partition):
    return sum((N_CAND * len(B)) ** 2 for B in partition)


def _cell_offdiag_weight(M):
    """The surviving record-blind coherence functional: total squared weight
    on cell-mismatched positions.  The positions are partition-independent
    so values compare exactly across record resolutions (control genre)."""
    return sum(M[p][q] ** 2 for p in range(DIM) for q in range(DIM)
               if _cell_of(p) != _cell_of(q))


# ---------------------------------------------------------------------------
# partition operations and predicates (for the PD5 control directions)
# ---------------------------------------------------------------------------

def _is_partition(parts, ground):
    blocks = [set(b) for b in parts]
    if not blocks or any(not b for b in blocks):
        return False
    union = set()
    total = 0
    for b in blocks:
        union |= b
        total += len(b)
    return union == set(ground) and total == len(ground)


def _refines(finer, coarser):
    return all(any(set(b) <= set(c) for c in coarser) for b in finer)


def _same_partition(p, q):
    return {frozenset(b) for b in p} == {frozenset(b) for b in q}


def _split(partition, block, part1, part2):
    """Refine: replace one record cell by two (adding a recording cell that
    distinguishes)."""
    assert frozenset(part1) | frozenset(part2) == frozenset(block)
    assert not (frozenset(part1) & frozenset(part2))
    out = [frozenset(b) for b in partition if frozenset(b) != frozenset(block)]
    out.extend([frozenset(part1), frozenset(part2)])
    return tuple(out)


def _merge(partition, b1, b2):
    """Coarsen: replace two record cells by their union."""
    out = [frozenset(b) for b in partition
           if frozenset(b) not in (frozenset(b1), frozenset(b2))]
    out.append(frozenset(b1) | frozenset(b2))
    return tuple(out)


# ---------------------------------------------------------------------------
# exhibited instances (authored rational data with genuine coherence in
# every sector the legs interrogate; non-vacuity is ENFORCED at the legs)
# ---------------------------------------------------------------------------

# NOTE (value coincidences, authored-data genre): in rho_a the executed
# evidence values at positions (1,1)/(0,1) and at (2,2)/(0,3) coincide
# pairwise.  Both coincidences are properties of the authored vectors
# below; editing _V1.._V3 moves all four evidence sites that quote those
# values at once.
_V1 = (1, 1, 1, 1, 1, 1)
_V2 = (2, 1, 0, 1, 0, 1)
_V3 = (1, -1, 2, 0, 1, 0)
_V4 = (0, 1, -1, 1, 2, 1)


def _instance_states():
    r1, r2, r3, r4 = (_rank1(v) for v in (_V1, _V2, _V3, _V4))
    rho_a = _add(_add(_scal(F(1, 2), r1), _scal(F(1, 3), r2)),
                 _scal(F(1, 6), r3))
    rho_b = _add(_scal(F(3, 5), r2), _scal(F(2, 5), r4))
    rho_c = r3
    return [rho_a, rho_b, rho_c]


def _general_mats():
    A = _mat([[1, 2, 3, 4, 5, 6],
              [6, 5, 4, 3, 2, 1],
              [0, 1, 0, 2, 0, 3],
              [1, 0, -1, 0, 1, 0],
              [2, -2, 3, -3, 4, -4],
              [0, 0, 1, 1, 2, 2]])
    B = [[F(i + 1, 2) - F(j, 3) for j in range(DIM)] for i in range(DIM)]
    return [A, B]


# ---------------------------------------------------------------------------
# leg inventory (append-and-record, on the bank path)
# ---------------------------------------------------------------------------

EXPECTED_LEGS = {
    "check_T_record_subsystem_partial_dephasing": (
        "kraus_family_is_a_record_projection_resolution",
        "linearity_by_value_on_instances_and_basis_expansion",
        "trace_preservation_by_value",
        "idempotence_on_full_basis_by_value",
        "unitality_by_value",
        "positivity_on_exhibited_instances_with_tester_controls",
        "structural_cp_named_as_kraus_form_genre",
        "conditional_expectation_module_property_by_value",
        "projection_property_and_membership_computed",
    ),
    "check_L_full_algebra_recovers_banked_dephasing": (
        "sibling_helper_surface_reachable_and_limitation_computed",
        "full_record_tie_via_sibling_machinery_by_value",
        "sibling_instance_reconstruction_tie_by_value",
        "wrong_convention_rivals_fail_by_value",
    ),
    "check_L_record_blind_invisibility": (
        "fixed_points_are_exactly_cell_block_diagonal_units",
        "general_fixed_point_iff_via_perturbation_family",
        "record_blind_reads_only_matched_cell_entries",
        "mismatched_coherence_contributes_zero_over_spanning_set",
        "scope_of_the_discharge_recorded",
    ),
    "check_L_partial_dephasing_endpoints": (
        "partition_chain_well_formed",
        "trivial_record_is_identity",
        "full_record_is_matched_cell_restriction",
        "strictly_partial_record_survivor_exhibited",
    ),
    "check_T_partial_dephasing_controls": (
        "refinement_strictly_shrinks_by_value",
        "coarsening_restores_by_value",
        "rival_fails_idempotence_by_value",
        "rival_fails_tie_and_unitality_by_value",
        "no_sign_read_scan_scoped",
        "form_b_slot_not_consumed_scoped",
    ),
}


def _result(name, legs, key_result, dependencies=(), cross_refs=(),
            disclosures=()):
    have = tuple(sorted(legs))
    want = tuple(sorted(EXPECTED_LEGS[name]))
    fail_reasons = []
    if have != want:
        missing = sorted(set(want) - set(have))
        extra = sorted(set(have) - set(want))
        fail_reasons.append(
            f"leg inventory mismatch: missing={missing} extra={extra}")
    for label in sorted(legs):
        ok, _ev = legs[label]
        if not ok:
            fail_reasons.append(f"leg failed: {label}")
    return {
        "name": name,
        "passed": not fail_reasons,
        "fail_reasons": fail_reasons,
        "legs": {k: {"passed": bool(v[0]), "evidence": v[1]}
                 for k, v in legs.items()},
        "leg_count": len(legs),
        "key_result": key_result,
        "dependencies": list(dependencies),
        "cross_refs": list(cross_refs),
        "disclosures": list(disclosures),
        "may_not_cite": list(MAY_NOT_CITE),
        "held_out_of_the_bank": HELD_OUT_OF_THE_BANK,
        "claim_surface_sha256": CLAIM_SURFACE_SHA256,
        "tier": 3,
        "epistemic_tag": "[P_math]",
        "physical_premises_certified": False,
        "leg_inventory_contract": (
            "append-and-record (D7@2026-08-08): certifies a declared leg "
            "EXECUTED, not that it could have failed"),
    }


# ---------------------------------------------------------------------------
# PD1 -- the construction
# ---------------------------------------------------------------------------

def check_T_record_subsystem_partial_dephasing():
    legs = {}
    part = P_MID              # a genuinely partial record: the general case
    projs = _record_projs(part)
    states = _instance_states()
    gens = _general_mats()

    # -- Kraus family: exact record-cell projection resolution ------------
    ok = len(projs) == len(part)
    S = _zeros(DIM)
    for i, Q in enumerate(projs):
        ok = ok and _eq(_mm(Q, Q), Q) and _eq(_T(Q), Q)
        for j, R in enumerate(projs):
            if i != j:
                ok = ok and _is0(_mm(Q, R))
        S = _add(S, Q)
    ok = ok and _eq(S, _eye(DIM))
    legs["kraus_family_is_a_record_projection_resolution"] = (ok, (
        f"the record-cell projections I(x)Q_k on the candidate x cell index "
        f"set (dim {DIM} = {N_CAND} x {N_CELL}) at the partial resolution "
        f"{[sorted(B) for B in part]}: each an exact projection, "
        f"self-adjoint, pairwise orthogonal, and the family sums to the "
        f"identity; family size {len(projs)} == record-cell count "
        f"{len(part)} (enforced)"))

    # -- linearity BY VALUE: exhibited combinations + the full basis
    #    expansion (the universal rides the Kraus-form genre; the leg
    #    computes) --------------------------------------------------------
    combos = [(F(2, 3), F(-1, 5), gens[0], gens[1]),
              (F(7), F(1, 2), states[0], gens[0]),
              (F(-3, 4), F(5, 6), states[1], states[2])]
    n_run = 0
    ok = True
    for a, b, X, Y in combos:
        lhs = _D(_add(_scal(a, X), _scal(b, Y)), part)
        rhs = _add(_scal(a, _D(X, part)), _scal(b, _D(Y, part)))
        ok = ok and _eq(lhs, rhs)
        n_run += 1
    ok = ok and n_run == len(combos)
    X = gens[0]
    recon = _zeros(DIM)
    n_units = 0
    for p in range(DIM):
        for q in range(DIM):
            recon = _add(recon, _scal(X[p][q], _D(_unit(p, q, DIM), part)))
            n_units += 1
    ok = ok and n_units == DIM * DIM and _eq(recon, _D(X, part))
    legs["linearity_by_value_on_instances_and_basis_expansion"] = (ok, (
        f"D_R(aX+bY) == a D_R(X) + b D_R(Y) entrywise on {n_run} exhibited "
        f"rational combinations (enforced == authored count), and D_R of a "
        f"general instance equals its expansion sum_pq X_pq D_R(e_pq) over "
        f"all {n_units} basis units (enforced == dim^2); linearity as a "
        f"universal is the [P_math] Kraus-form genre named in the "
        f"structural-CP leg -- this leg computes"))

    # -- trace preservation BY VALUE (instances + the full basis) ----------
    n_run = 0
    ok = True
    for M in states + gens:
        ok = ok and _tr(_D(M, part)) == _tr(M)
        n_run += 1
    ok = ok and n_run == len(states) + len(gens)
    n_units = 0
    for p in range(DIM):
        for q in range(DIM):
            e = _unit(p, q, DIM)
            ok = ok and _tr(_D(e, part)) == _tr(e)
            n_units += 1
    ok = ok and n_units == DIM * DIM
    legs["trace_preservation_by_value"] = (ok, (
        f"Tr D_R(X) == Tr X on {n_run} instances (states and general "
        f"matrices; enforced count) and on all {n_units} matrix units "
        f"(enforced == dim^2)"))

    # -- idempotence BY VALUE on the full matrix-unit basis ----------------
    n_run = 0
    ok = True
    for p in range(DIM):
        for q in range(DIM):
            e = _unit(p, q, DIM)
            De = _D(e, part)
            ok = ok and _eq(_D(De, part), De)
            n_run += 1
    ok = ok and n_run == DIM * DIM
    n_states = 0
    for rho in states:
        Dr = _D(rho, part)
        ok = ok and _eq(_D(Dr, part), Dr)
        n_states += 1
    ok = ok and n_states == len(states)
    legs["idempotence_on_full_basis_by_value"] = (ok, (
        f"D_R(D_R(e)) == D_R(e) entrywise on all {n_run} matrix units "
        f"(enforced == dim^2) and on all {n_states} exhibited states "
        f"(enforced count)"))

    # -- unitality BY VALUE ------------------------------------------------
    ok = _eq(_D(_eye(DIM), part), _eye(DIM))
    legs["unitality_by_value"] = (ok, "D_R(I) == I entrywise")

    # -- positivity on the exhibited instance set, with tester controls ----
    n_run = 0
    ok = True
    for rho in states:
        ok = ok and _eq(_T(rho), rho) and _tr(rho) == 1 and _is_psd(rho)
        ok = ok and _is_psd(_D(rho, part))
        n_run += 1
    ok = ok and n_run == len(states)
    indef = _add(_unit(0, 1, DIM), _unit(1, 0, DIM))
    ok = ok and not _is_psd(indef)               # tester negative control
    ok = ok and _is_psd(_rank1(_V1))             # tester boundary control
    legs["positivity_on_exhibited_instances_with_tester_controls"] = (ok, (
        f"D_R(rho) is symmetric, trace-one and exactly PSD (characteristic-"
        f"polynomial sign pattern, exact) on all {n_run} exhibited states "
        f"(enforced count); the PSD tester itself is exercised: it rejects "
        f"an exhibited indefinite symmetric matrix and accepts an exhibited "
        f"boundary rank-one projector"))

    # -- structural CP: the Kraus-form genre, NAMED -----------------------
    n_parts = 0
    ok = True
    for pt in (P_TRIVIAL, P_MID, P_FINE):
        fam = _record_projs(pt)
        Ssum = _zeros(DIM)
        for Q in fam:
            ok = ok and _eq(_mm(Q, Q), Q) and _eq(_T(Q), Q)
            Ssum = _add(Ssum, Q)
        ok = ok and _eq(Ssum, _eye(DIM))
        n_parts += 1
    ok = ok and n_parts == 3
    legs["structural_cp_named_as_kraus_form_genre"] = (ok, (
        f"structural complete positivity and positivity on ALL inputs are "
        f"the [P_math] Kraus-form genre, NAMED: D_R is a finite sum of "
        f"congruences X -> Q X Q with Q == Q^T == Q^2 and sum_k Q_k == I -- "
        f"the executed content is exactly those family facts, verified here "
        f"on all {n_parts} exhibited record resolutions (enforced count); "
        f"the universal is named, not sampled-and-overclaimed"))

    # -- the conditional-expectation MODULE property BY VALUE --------------
    sp_pairs = _record_blind_pairs(part)
    span_units = [_unit(p, q, DIM) for (p, q) in sp_pairs]
    rho = states[0]
    Drho = _D(rho, part)
    n_pairs = 0
    n_nonzero = 0
    ok = len(span_units) == _span_formula(part)
    for A in span_units:
        for B in span_units:
            lhs = _D(_mm(_mm(A, rho), B), part)
            rhs = _mm(_mm(A, Drho), B)
            ok = ok and _eq(lhs, rhs)
            if not _is0(lhs):
                n_nonzero += 1
            n_pairs += 1
    ok = ok and n_pairs == _span_formula(part) ** 2 and n_nonzero > 0
    legs["conditional_expectation_module_property_by_value"] = (ok, (
        f"D_R(A rho B) == A D_R(rho) B entrywise for ALL ordered pairs "
        f"(A, B) from the exact spanning set of the record-blind algebra "
        f"({n_pairs} pairs, enforced == span^2 with span == "
        f"sum_k (n_cand * |cell_k|)^2 == {_span_formula(part)}); "
        f"{n_nonzero} pairs give a nonzero product (anti-vacuity "
        f"enforced).  MIDDLE-SLOT SCOPE, named: this sweep computes the "
        f"property at the single exhibited state rho only; the universal "
        f"in the middle slot is not computed here -- it rides the "
        f"separately-legged full-basis linearity and basis determination "
        f"of D_R, named per the [P_math] genre"))

    # -- projection property + algebra membership --------------------------
    n_proj = 0
    ok = True
    for A in span_units:
        ok = ok and _eq(_D(A, part), A)
        n_proj += 1
    ok = ok and n_proj == _span_formula(part)
    cross = [(p, q) for p in range(DIM) for q in range(DIM)
             if (p, q) not in set(sp_pairs)]
    n_mem = 0
    for p in range(DIM):
        for q in range(DIM):
            Du = _D(_unit(p, q, DIM), part)
            ok = ok and all(Du[r][s] == 0 for (r, s) in cross)
            n_mem += 1
    ok = ok and n_mem == DIM * DIM
    ok = ok and all(Drho[r][s] == 0 for (r, s) in cross)
    n_prod = 0
    for A in span_units:
        for B in span_units:
            AB = _mm(A, B)
            ok = ok and all(AB[r][s] == 0 for (r, s) in cross)
            n_prod += 1
    ok = ok and n_prod == _span_formula(part) ** 2
    legs["projection_property_and_membership_computed"] = (ok, (
        f"D_R restricts to the identity on all {n_proj} spanning units of "
        f"the record-blind algebra (enforced == span formula); the span "
        f"is closed under products (every one of the {n_prod} ordered "
        f"spanning-unit products, enforced == span^2, has all "
        f"cross-record-cell entries exactly zero -- the 'algebra' in "
        f"'record-blind algebra' computed, with linearity separately "
        f"legged); and D_R of every one of the {n_mem} basis units "
        f"(enforced == dim^2) and of the exhibited state lies IN that "
        f"algebra (every cross-record-cell entry exactly zero): with the "
        f"module property (middle-slot scope named in-leg) and "
        f"idempotence, D_R is A conditional expectation onto the "
        f"record-blind algebra -- uniqueness is not computed and not "
        f"claimed"))

    return _result(
        "check_T_record_subsystem_partial_dephasing", legs,
        key_result=(
            "On the candidate x cell index set, the record-subsystem "
            "partial dephasing D_R(rho) = sum_k (I (x) Q_k) rho (I (x) Q_k) "
            "over the record-cell projections is constructed in exact "
            "rational matrices; linearity, trace preservation, idempotence, "
            "unitality, and positivity on the exhibited instance set are "
            "legged by value; D_R is a conditional expectation onto the "
            "record-blind algebra (projection property, algebra membership, "
            "multiplicative closure of the span, and the module property "
            "computed over the full spanning-unit pair set at the "
            "exhibited state, middle-slot scope named in-leg; uniqueness "
            "is not computed and not claimed); structural complete "
            "positivity is NAMED as the "
            "[P_math] Kraus-form genre, not sampled-and-overclaimed. "
            "DEFINITIONAL: a map and its characterization; no physics "
            "claimed."),
        cross_refs=["L_commutative_no_unresolved_hold"],
        disclosures=[
            "the universal linearity / trace-preservation / idempotence / "
            "unitality / CP statements ride the [P_math] Kraus-form genre "
            "named in-leg; the legs compute instances, full-basis sweeps, "
            "and full spanning-pair sweeps",
        ])


# ---------------------------------------------------------------------------
# PD2 -- the full-algebra tie to the banked leg-(ii) dephasing
# ---------------------------------------------------------------------------

def check_L_full_algebra_recovers_banked_dephasing():
    legs = {}
    states = _instance_states()

    # -- the sibling's reachable machinery, and the disclosed limitation --
    helper_names = ("_mat", "_mm", "_add", "_sub", "_scal", "_eye", "_tr",
                    "_eq", "_rank1")
    have_helpers = all(callable(getattr(_cnuh, h, None))
                       for h in helper_names)
    dephase_is_check_local = not hasattr(_cnuh, "dephase")
    try:
        sib_src = inspect.getsource(_cnuh)
    except (OSError, TypeError):
        sib_src = None
    module_level_dephase = True
    dephase_hosts = []
    if sib_src is not None:
        sib_tree = ast.parse(sib_src)
        module_level_dephase = any(
            isinstance(node, ast.FunctionDef) and node.name == "dephase"
            for node in sib_tree.body)
        for outer in ast.walk(sib_tree):
            if isinstance(outer, ast.FunctionDef):
                for inner in ast.walk(outer):
                    if (isinstance(inner, ast.FunctionDef)
                            and inner is not outer
                            and inner.name == "dephase"):
                        dephase_hosts.append(outer.name)
    ok = (have_helpers and dephase_is_check_local
          and sib_src is not None
          and not module_level_dephase
          and dephase_hosts == ["check_L_commutative_no_unresolved_hold"])
    legs["sibling_helper_surface_reachable_and_limitation_computed"] = (ok, (
        f"the banked sibling's module-level matrix machinery "
        f"{list(helper_names)} is reachable and callable; its dephasing "
        f"operator is NOT module-level (computed two ways: no module "
        f"attribute 'dephase', and an AST walk of the sibling's source "
        f"finds no module-level def of that name and exactly one nested "
        f"def, hosted inside {dephase_hosts} -- the positive locational "
        f"fact computed, not inferred from an absence alone), so the tie "
        f"below runs through the sibling's module-level machinery and "
        f"through its executed instance reconstructed via its own "
        f"module-level constructors -- the limitation the frozen surface "
        f"disclosed, computed rather than assumed"))

    # -- full-record ties through the sibling's machinery BY VALUE ---------
    # two families: the whole index set resolved (every index its own
    # record), and the full cell record I (x) e_kk (the sibling's
    # rank>1-projection genre)
    fam_whole = [_unit(p, p, DIM) for p in range(DIM)]
    fam_cells = _record_projs(P_FINE)
    n_run = 0
    ok = True
    tied_matrices = {}
    basis = ([_unit(p, q, DIM) for p in range(DIM) for q in range(DIM)])
    for fam_name, fam in (("whole-index", fam_whole), ("cell", fam_cells)):
        for idx, rho in enumerate(states):
            theirs = _cnuh._scal(F(0), rho)
            for Q in fam:
                theirs = _cnuh._add(theirs,
                                    _cnuh._mm(_cnuh._mm(Q, rho), Q))
            ours = _dephase_family(rho, fam)
            ok = ok and _cnuh._eq(theirs, ours) and _eq(theirs, ours)
            ok = ok and _cnuh._tr(theirs) == _tr(ours)
            n_run += 1
            if fam_name == "cell" and idx == 0:
                tied_matrices["cell_rho0"] = ours
    ok = ok and n_run == 2 * len(states)
    n_basis = 0
    for fam in (fam_whole, fam_cells):
        for e in basis:
            theirs = _cnuh._scal(F(0), e)
            for Q in fam:
                theirs = _cnuh._add(theirs, _cnuh._mm(_cnuh._mm(Q, e), Q))
            ok = ok and _cnuh._eq(theirs, _dephase_family(e, fam))
            n_basis += 1
    ok = ok and n_basis == 2 * DIM * DIM
    ok = ok and _eq(tied_matrices["cell_rho0"], _D(states[0], P_FINE))
    legs["full_record_tie_via_sibling_machinery_by_value"] = (ok, (
        f"on {n_run} (family, state) instances (enforced == families x "
        f"states) AND on the full matrix-unit basis for both families "
        f"({n_basis} units, enforced == families x dim^2 -- both "
        f"expressions are finite sums of congruences, so basis agreement "
        f"determines the map-level tie, the [P_math] linearity genre "
        f"named) the leg-(ii) sum computed ENTIRELY through the sibling's "
        f"module-level machinery equals, entrywise under BOTH modules' "
        f"equality functions and by trace value, the same sum computed "
        f"through this module's independent code path; the cell-family tie "
        f"instance also equals D_R at the full record resolution entrywise "
        f"(the record subsystem resolving the whole index set recovers the "
        f"banked dephasing form by value)"))

    # -- the sibling's own executed instance, reconstructed ----------------
    P1 = _cnuh._rank1([1, 1, 0])
    P2 = _cnuh._rank1([1, -1, 0])
    P0 = _cnuh._sub(_cnuh._sub(_cnuh._eye(3), P1), P2)
    spec3 = [P1, P2, P0]
    rho3 = _cnuh._add(_cnuh._scal(F(2, 3), _cnuh._rank1([2, 1, 1])),
                      _cnuh._scal(F(1, 3), _cnuh._rank1([1, 0, 1])))
    theirs3 = _cnuh._scal(F(0), rho3)
    for Q in spec3:
        theirs3 = _cnuh._add(theirs3, _cnuh._mm(_cnuh._mm(Q, rho3), Q))
    ours3 = _dephase_family(rho3, spec3)
    ok = _cnuh._eq(theirs3, ours3) and _eq(theirs3, ours3)
    ok = ok and _cnuh._tr(rho3) == 1 and _tr(rho3) == 1
    ok = ok and not _cnuh._eq(rho3, theirs3)   # genuine off-diagonal content
    n_inv = 0
    for A in spec3:
        t_sib = _cnuh._tr(_cnuh._mm(rho3, A))
        t_our = _tr(_mm(rho3, A))
        t_dep = _cnuh._tr(_cnuh._mm(theirs3, A))
        ok = ok and t_sib == t_our == t_dep
        n_inv += 1
    ok = ok and n_inv == len(spec3)
    legs["sibling_instance_reconstruction_tie_by_value"] = (ok, (
        f"the sibling's executed dim-3 MASA instance (its spectral family "
        f"and its state), reconstructed verbatim through the sibling's own "
        f"module-level constructors: the leg-(ii) sum via the sibling's "
        f"machinery equals this module's dephasing on the same matrices "
        f"entrywise; the sibling's executed record values are recomputed "
        f"and tied by value across both code paths -- state trace one, "
        f"genuine off-diagonal content present, and Tr(rho A) == "
        f"Tr(D(rho) A) for all {n_inv} family members (enforced), with the "
        f"two modules' trace functions agreeing on every value"))

    # -- wrong-convention rivals fail the tie BY VALUE ---------------------
    rho = states[0]
    tied = tied_matrices["cell_rho0"]
    q0 = fam_cells[0]
    denom = _tr(_mm(q0, rho))
    ok = denom != 0
    rival_sel = _scal(F(1) / denom, _mm(_mm(q0, rho), q0))
    p_probe = _flat(0, 1)      # a diagonal position outside record cell 0
    v_tied = tied[p_probe][p_probe]
    v_sel = rival_sel[p_probe][p_probe]
    ok = ok and v_tied != 0 and v_sel == 0 and v_tied != v_sel
    m = len(fam_cells)
    rival_shift = _zeros(DIM)
    for k in range(m):
        rival_shift = _add(rival_shift,
                           _mm(_mm(fam_cells[k], rho),
                               fam_cells[(k + 1) % m]))
    t_shift = _tr(rival_shift)
    t_tied = _tr(tied)
    ok = ok and t_shift != t_tied
    ok = ok and not _eq(rival_shift, tied)
    legs["wrong_convention_rivals_fail_by_value"] = (ok, (
        f"two wrong-convention rivals fail by VALUE, not by verdict: the "
        f"un-normalized (selective) rival Q_0 rho Q_0 / Tr(Q_0 rho) "
        f"disagrees with the tied dephasing at an exhibited diagonal entry "
        f"(tied value {v_tied}, rival value {v_sel}, computed unequal with "
        f"the tied value enforced nonzero), and the index-shifted Kraus "
        f"pairing sum_k Q_k rho Q_(k+1) disagrees by trace value (rival "
        f"trace {t_shift}, tied trace {t_tied}) and entrywise"))

    return _result(
        "check_L_full_algebra_recovers_banked_dephasing", legs,
        key_result=(
            "When the record subsystem resolves the whole index set, D_R "
            "agrees with the banked leg-(ii) dephasing of "
            "L_commutative_no_unresolved_hold: tied through the sibling's "
            "own module-level machinery by value on shared instances, and "
            "tied to the sibling's executed record values on its own "
            "instance reconstructed through its own constructors (the "
            "sibling's dephasing operator is check-local -- limitation "
            "disclosed and computed).  Wrong-convention rivals fail the "
            "tie by value."),
        dependencies=["L_commutative_no_unresolved_hold"],
        disclosures=[
            "the sibling's dephasing operator is defined inside its check "
            "function; the tie is to (a) the sibling's module-level matrix "
            "machinery executed on shared instances and (b) the sibling's "
            "executed record values recomputed on its reconstructed "
            "instance -- exactly the limitation the frozen surface states",
            "the literal transposed-Kraus rival coincides with D_R for a "
            "self-adjoint projection family (an identity, so it cannot "
            "fail); the exhibited failing rivals are the index-shifted "
            "Kraus pairing and the selective normalized projection, per "
            "the surface's 'e.g.' license",
        ])


# ---------------------------------------------------------------------------
# PD3 -- record-blind invisibility, LEGGED
# ---------------------------------------------------------------------------

def check_L_record_blind_invisibility():
    legs = {}
    states = _instance_states()
    parts = (P_MID, P_FINE)

    # -- fixed points on the full basis: exactly the cell-block-diagonal
    #    units ------------------------------------------------------------
    ok = True
    n_parts = 0
    ev_counts = []
    for part in parts:
        blind = set(_record_blind_pairs(part))
        n_in = n_cross = 0
        for p in range(DIM):
            for q in range(DIM):
                e = _unit(p, q, DIM)
                De = _D(e, part)
                if (p, q) in blind:
                    ok = ok and _eq(De, e)
                    n_in += 1
                else:
                    ok = ok and _is0(De) and not _eq(De, e)
                    n_cross += 1
        ok = ok and n_in == _span_formula(part)
        ok = ok and n_in + n_cross == DIM * DIM
        ev_counts.append((sorted(sorted(B) for B in part), n_in, n_cross))
        n_parts += 1
    ok = ok and n_parts == len(parts)
    legs["fixed_points_are_exactly_cell_block_diagonal_units"] = (ok, (
        f"over the full matrix-unit basis at each exhibited record "
        f"resolution: every cell-block-diagonal unit is D_R-invariant and "
        f"every cross-record-cell unit is annihilated (hence not "
        f"invariant); per-resolution (blocks, invariant, annihilated) = "
        f"{ev_counts}, with invariant count enforced == the span formula "
        f"and the two classes enforced to partition dim^2"))

    # -- the iff at the entry level, via a perturbation family -------------
    part = P_MID
    blind = set(_record_blind_pairs(part))
    a0 = _zeros(DIM)
    for (p, q) in blind:
        a0[p][q] = F(1 + p + 2 * q, 3)
    ok = _eq(_D(a0, part), a0)
    n_pert = 0
    for p in range(DIM):
        for q in range(DIM):
            if (p, q) in blind:
                continue
            pert = _add(a0, _unit(p, q, DIM))
            ok = ok and not _eq(_D(pert, part), pert)
            n_pert += 1
    ok = ok and n_pert == DIM * DIM - _span_formula(part)
    legs["general_fixed_point_iff_via_perturbation_family"] = (ok, (
        f"a general cell-block-diagonal matrix is D_R-invariant, and "
        f"adding any single cross-record-cell entry breaks invariance -- "
        f"executed for all {n_pert} cross positions (enforced == dim^2 "
        f"minus the span formula): an observable is D_R-invariant iff "
        f"cell-block-diagonal, at this resolution, computed"))

    # -- Tr(rho A) reads only matched-cell entries -------------------------
    n_run = 0
    ok = True
    for rho in states:
        Drho = _D(rho, part)
        for (p, q) in sorted(blind):
            A = _unit(p, q, DIM)
            t = _tr(_mm(rho, A))
            ok = ok and t == rho[q][p]
            ok = ok and t == _tr(_mm(Drho, A))
            n_run += 1
    ok = ok and n_run == len(states) * _span_formula(part)
    legs["record_blind_reads_only_matched_cell_entries"] = (ok, (
        f"for every element of the exact spanning set of the record-blind "
        f"algebra and every exhibited state ({n_run} pairs, enforced == "
        f"states x span formula): Tr(rho A) equals the single matched-cell "
        f"entry of rho the unit addresses, and equals Tr(D_R(rho) A) -- "
        f"the record-blind algebra reads only matched-cell entries, "
        f"computed over the spanning set, not sampled"))

    # -- mismatched-cell coherence contributes zero, over the whole
    #    spanning set ------------------------------------------------------
    cross_pairs = [(p, q) for p in range(DIM) for q in range(DIM)
                   if (p, q) not in blind]
    n_pairs = 0
    ok = True
    for (r, s) in cross_pairs:
        delta_u = _unit(r, s, DIM)
        for (p, q) in sorted(blind):
            A = _unit(p, q, DIM)
            ok = ok and _tr(_mm(delta_u, A)) == 0
            n_pairs += 1
    ok = ok and n_pairs == len(cross_pairs) * _span_formula(part)
    rho = states[0]
    delta = _add(_unit(_flat(0, 0), _flat(1, 2), DIM),
                 _unit(_flat(1, 2), _flat(0, 0), DIM))
    n_reads = 0
    for (p, q) in sorted(blind):
        A = _unit(p, q, DIM)
        ok = ok and _tr(_mm(_add(rho, delta), A)) == _tr(_mm(rho, A))
        n_reads += 1
    ok = ok and n_reads == _span_formula(part)
    legs["mismatched_coherence_contributes_zero_over_spanning_set"] = (ok, (
        f"every cross-record-cell coherence unit is traceless against "
        f"EVERY element of the exact spanning set ({n_pairs} pairs, "
        f"enforced == cross count x span formula), and adding an exhibited "
        f"symmetric mismatched-cell coherence to a state changes no "
        f"record-blind read ({n_reads} reads, enforced == span formula): "
        f"mismatched-cell coherence contributes zero to Tr(rho A) for "
        f"every A in the record-blind algebra, at this resolution"))

    # -- the scope of the discharge, recorded on recomputed facts ----------
    span_recount = len(_record_blind_pairs(part))
    ok = (span_recount == _span_formula(part)
          and n_pairs == (DIM * DIM - span_recount) * span_recount
          and n_run == len(states) * span_recount)
    legs["scope_of_the_discharge_recorded"] = (ok, (
        f"the invisibility sentence the M2 audit's P2 finding flagged as "
        f"asserted-not-legged is legged above (spanning-set recount "
        f"{span_recount} ties the executed pair counts, enforced); the "
        f"discharge is SCOPED to this candidate x cell index-set model -- "
        f"it is not a bank-wide universal and not a physical claim"))

    return _result(
        "check_L_record_blind_invisibility", legs,
        key_result=(
            "Fixed-point characterization: an observable is D_R-invariant "
            "iff cell-block-diagonal at the record-cell resolution "
            "(computed over the full basis and a full perturbation "
            "family); consequently Tr(rho A) for every A in the "
            "record-blind algebra reads only the matched-cell entries of "
            "rho, and mismatched-cell coherence contributes zero -- "
            "computed over an exact spanning set, not sampled.  This "
            "discharges the M2 audit's P2 finding, scoped to this "
            "index-set model."),
        cross_refs=["L_commutative_no_unresolved_hold"],
        disclosures=[
            "the discharge is scoped to this index-set model; no bank-wide "
            "or physical universal is stated",
            "the traceless-pair sweep is, mathematically, an identity of "
            "disjointly supported matrix units; its executed value is a "
            "check on the blind/cross classification, and the "
            "state-plus-coherence read sweep is the leg's discriminating "
            "half (disclosed per the identity-leg genre)",
        ])


# ---------------------------------------------------------------------------
# PD4 -- endpoints
# ---------------------------------------------------------------------------

def check_L_partial_dephasing_endpoints():
    legs = {}
    states = _instance_states()
    rho = states[0]

    # -- the endpoint chain is well-formed ---------------------------------
    ground = range(N_CELL)
    ok = all(_is_partition(pt, ground)
             for pt in (P_TRIVIAL, P_MID, P_FINE))
    ok = ok and _refines(P_FINE, P_MID) and _refines(P_MID, P_TRIVIAL)
    ok = ok and not _same_partition(P_FINE, P_MID)
    ok = ok and not _same_partition(P_MID, P_TRIVIAL)
    ok = ok and len(P_TRIVIAL) < len(P_MID) < len(P_FINE)
    legs["partition_chain_well_formed"] = (ok, (
        f"the exhibited record resolutions are partitions of the cell "
        f"index set, strictly ordered by refinement: "
        f"{[sorted(sorted(B) for B in pt) for pt in (P_TRIVIAL, P_MID, P_FINE)]} "
        f"(each checked as a partition; refinement and strictness "
        f"computed)"))

    # -- trivial record subsystem: the identity ----------------------------
    n_run = 0
    ok = True
    for p in range(DIM):
        for q in range(DIM):
            e = _unit(p, q, DIM)
            ok = ok and _eq(_D(e, P_TRIVIAL), e)
            n_run += 1
    ok = ok and n_run == DIM * DIM
    n_states = 0
    for r_s in states:
        ok = ok and _eq(_D(r_s, P_TRIVIAL), r_s)
        n_states += 1
    ok = ok and n_states == len(states)
    legs["trivial_record_is_identity"] = (ok, (
        f"at the trivial record subsystem (one record cell) D_R is the "
        f"identity on all {n_run} basis units (enforced == dim^2) and on "
        f"all {n_states} exhibited states (enforced count), computed "
        f"entrywise"))

    # -- full record: the matched-cell restriction -------------------------
    def _matched_cell_mask(M):
        # the independent entrywise rule the leg compares against (genre:
        # a second code path so the equality is a tie, not a restatement)
        return [[M[p][q] if _cell_of(p) == _cell_of(q) else F(0)
                 for q in range(DIM)] for p in range(DIM)]

    n_run = 0
    ok = True
    for p in range(DIM):
        for q in range(DIM):
            e = _unit(p, q, DIM)
            ok = ok and _eq(_D(e, P_FINE), _matched_cell_mask(e))
            n_run += 1
    ok = ok and n_run == DIM * DIM
    n_states = 0
    for r_s in states:
        ok = ok and _eq(_D(r_s, P_FINE), _matched_cell_mask(r_s))
        n_states += 1
    ok = ok and n_states == len(states)
    Dr = _D(rho, P_FINE)
    p_c, q_c = _flat(0, 0), _flat(1, 0)   # cross-candidate, matched cell
    ok = ok and rho[p_c][q_c] != 0 and Dr[p_c][q_c] == rho[p_c][q_c]
    legs["full_record_is_matched_cell_restriction"] = (ok, (
        f"at the full record D_R equals the matched-cell restriction, "
        f"computed against an independent entrywise rule on all {n_run} "
        f"basis units (enforced == dim^2) and on all {n_states} exhibited "
        f"states (enforced count); the "
        f"subsystem point exhibited by value: the cross-candidate "
        f"matched-cell coherence survives exactly "
        f"(entry value {rho[p_c][q_c]}, enforced nonzero, preserved)"))

    # -- a strictly partial record: survivor exhibited exactly -------------
    Dm = _D(rho, P_MID)
    p1, q1 = _flat(0, 0), _flat(0, 1)     # within one record cell
    p2, q2 = _flat(0, 0), _flat(0, 2)     # across record cells
    ok = (rho[p1][q1] != 0 and Dm[p1][q1] == rho[p1][q1]
          and rho[p2][q2] != 0 and Dm[p2][q2] == 0)
    legs["strictly_partial_record_survivor_exhibited"] = (ok, (
        f"at the strictly partial record the off-diagonal coherence "
        f"WITHIN a record cell survives exactly (value {rho[p1][q1]}, "
        f"enforced nonzero, preserved) while the coherence ACROSS record "
        f"cells is annihilated exactly (state value {rho[p2][q2]}, "
        f"enforced nonzero; dephased value {Dm[p2][q2]}): the surviving "
        f"sector is the within-record-cell off-diagonal -- exhibited; no "
        f"V law is stated here"))

    return _result(
        "check_L_partial_dephasing_endpoints", legs,
        key_result=(
            "Endpoints, computed: the trivial record subsystem gives "
            "D_R = identity; the full record gives the matched-cell "
            "restriction (with within-cell candidate coherence surviving "
            "-- the subsystem point); a strictly partial record is "
            "exhibited with off-diagonal coherence surviving within a "
            "record cell and annihilated across record cells, exactly.  "
            "No V law is stated."),
        cross_refs=["L_commutative_no_unresolved_hold"],
        disclosures=[
            "the surviving-sector sentence exhibits values on this model "
            "and states no law for them",
            "at the one-block partition most wrong conventions collapse "
            "to the identity map too, so the trivial-endpoint leg "
            "discriminates only against normalization-genre rivals",
        ])


# ---------------------------------------------------------------------------
# PD5 -- permanent controls
# ---------------------------------------------------------------------------

def check_T_partial_dephasing_controls():
    legs = {}
    states = _instance_states()

    # -- (a) refinement strictly shrinks the surviving coherence
    #    functional, BY VALUE (control genre; no supplier claim) -----------
    mid_built = _split(P_TRIVIAL, {0, 1, 2}, {0, 1}, {2})
    fine_built = _split(mid_built, {0, 1}, {0}, {1})
    ok = _same_partition(mid_built, P_MID)
    ok = ok and _same_partition(fine_built, P_FINE)
    forward = []
    n_states = 0
    for rho in (states[0], states[1]):
        has_cross = any(rho[p][q] != 0
                        for p in range(DIM) for q in range(DIM)
                        if {_cell_of(p), _cell_of(q)} == {0, 2}
                        or {_cell_of(p), _cell_of(q)} == {1, 2})
        has_within = any(rho[p][q] != 0
                         for p in range(DIM) for q in range(DIM)
                         if {_cell_of(p), _cell_of(q)} == {0, 1})
        ok = ok and has_cross and has_within        # non-vacuity enforced
        w0 = _cell_offdiag_weight(_D(rho, P_TRIVIAL))
        w1 = _cell_offdiag_weight(_D(rho, mid_built))
        w2 = _cell_offdiag_weight(_D(rho, fine_built))
        ok = ok and w0 > w1 > w2 and w2 == 0
        forward.append((w0, w1, w2))
        n_states += 1
    ok = ok and n_states == 2
    legs["refinement_strictly_shrinks_by_value"] = (ok, (
        f"refining the record by SPLIT operations (adding a recording cell "
        f"that distinguishes; the built partitions tie the authored chain "
        f"by partition equality) strictly shrinks the surviving "
        f"record-blind coherence functional on {n_states} exhibited states "
        f"(enforced count) whose relevant coherence is enforced nonzero: "
        f"exact values per state {[[str(w) for w in ws] for ws in forward]} "
        f"-- the decoherence-CONTROL direction (control genre only; no "
        f"supplier claim)"))

    # -- (a') coarsening restores the value exactly ------------------------
    mid_merged = _merge(P_FINE, {0}, {1})
    triv_merged = _merge(mid_merged, {0, 1}, {2})
    ok = _same_partition(mid_merged, P_MID)
    ok = ok and _same_partition(triv_merged, P_TRIVIAL)
    n_states = 0
    restored = []
    for i, rho in enumerate((states[0], states[1])):
        w1_back = _cell_offdiag_weight(_D(rho, mid_merged))
        w0_back = _cell_offdiag_weight(_D(rho, triv_merged))
        ok = ok and w1_back == forward[i][1] and w0_back == forward[i][0]
        restored.append((w0_back, w1_back))
        n_states += 1
    ok = ok and n_states == 2
    legs["coarsening_restores_by_value"] = (ok, (
        f"coarsening the record by MERGE operations (the merged partitions "
        f"tie the authored chain by partition equality) restores the "
        f"functional to its exact forward values on the same {n_states} "
        f"states (enforced count): restored values per state "
        f"{[[str(w) for w in ws] for ws in restored]} equal the "
        f"forward-computed values as Fractions -- both directions computed"))

    # -- (b) a rival non-conditional-expectation map fails idempotence
    #    BY VALUE ----------------------------------------------------------
    rho = states[0]

    def rival_avg(X):
        # the averaging rival: linear, trace-preserving, unital -- and not
        # idempotent (genre: the failure must be exhibited by value)
        return _scal(F(1, 2), _add(X, _D(X, P_MID)))

    m1 = rival_avg(rho)
    m2 = rival_avg(m1)
    p2, q2 = _flat(0, 0), _flat(0, 2)
    ok = rho[p2][q2] != 0
    v_once, v_twice = m1[p2][q2], m2[p2][q2]
    ok = ok and v_once != v_twice and not _eq(m1, m2)
    ok = ok and _tr(m1) == _tr(rho) and _eq(rival_avg(_eye(DIM)), _eye(DIM))
    legs["rival_fails_idempotence_by_value"] = (ok, (
        f"the averaging rival (X + D_R(X))/2 is trace-preserving and "
        f"unital yet fails idempotence BY VALUE: at an exhibited "
        f"cross-record-cell entry (state value enforced nonzero) one "
        f"application gives {v_once} and two give {v_twice}, computed "
        f"unequal -- so it is not a conditional expectation"))

    # -- (b') a rival fails the tie and unitality BY VALUE -----------------
    q0 = _record_projs(P_MID)[0]
    denom = _tr(_mm(q0, rho))
    ok = denom != 0

    def rival_sel(X):
        return _scal(F(1) / _tr(_mm(q0, X)), _mm(_mm(q0, X), q0))

    tied = _D(rho, P_MID)
    r_out = rival_sel(rho)
    p3 = _flat(0, 2)          # a diagonal position outside record cell 0
    v_tied, v_riv = tied[p3][p3], r_out[p3][p3]
    ok = ok and v_tied != 0 and v_riv == 0 and v_tied != v_riv
    u_out = rival_sel(_eye(DIM))
    ok = ok and u_out[p3][p3] != _eye(DIM)[p3][p3]
    legs["rival_fails_tie_and_unitality_by_value"] = (ok, (
        f"the normalized-projection rival Q_0 X Q_0 / Tr(Q_0 X) fails the "
        f"tie to D_R BY VALUE at an exhibited diagonal entry (tied value "
        f"{v_tied}, enforced nonzero; rival value {v_riv}) and fails "
        f"unitality by value at the same position ({u_out[p3][p3]} against "
        f"the identity's {_eye(DIM)[p3][p3]})"))

    # -- (c) the no-sign-read scan, scoped to this module ------------------
    path = os.path.abspath(__file__)
    src = None
    try:
        with open(path, "r", encoding="utf-8") as fh:
            src = fh.read()
    except OSError:
        pass
    tok_sign = "sign" + "_class"
    tok_sgn = "sign" + "("
    tok_switch = "switching" + "_class"
    control_tok = "record_blind"
    ok = (src is not None
          and tok_sign not in src
          and tok_sgn not in src
          and tok_switch not in src
          and control_tok in src)
    legs["no_sign_read_scan_scoped"] = (ok, (
        f"executed exact-token scan of THIS module's own source (scope: "
        f"this module only): the per-pair sign-class tokens (assembled by "
        f"concatenation so the scan cannot self-match) are absent, and the "
        f"positive-control token '{control_tok}' is present, so the "
        f"scanner reads the source and can report presence; no per-pair "
        f"sign-class datum is read by this module.  STATED LIMITATION: an "
        f"exact-token scan of one file; a read under a different name is "
        f"outside its reach"))

    # -- (c') the form-(b) slot is not consumed, scoped to this module -----
    tok_bat = "born" + "_at_ties"
    tok_rev = "R_EVENT" + "_MODEL"
    apf_imports = set()
    if src is not None:
        tree = ast.parse(src)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for a in node.names:
                    if a.name == "apf" or a.name.startswith("apf."):
                        apf_imports.add(a.name)
            elif isinstance(node, ast.ImportFrom):
                mod = node.module or ""
                if mod == "apf":
                    for a in node.names:
                        apf_imports.add("apf." + a.name)
                elif mod.startswith("apf."):
                    apf_imports.add(mod)
    ok = (src is not None
          and tok_bat not in src
          and tok_rev not in src
          and apf_imports == {"apf.commutative_no_unresolved_hold"})
    legs["form_b_slot_not_consumed_scoped"] = (ok, (
        f"executed scan, scope: this module only.  The declaring module's "
        f"name token and the R-event-model token (assembled by "
        f"concatenation) are absent from this module's source, and the AST "
        f"import census of this module's own source finds its apf imports "
        f"set-exactly equal to the one banked sibling it ties to "
        f"({sorted(apf_imports)}): the form-(b) slot is not consumed by "
        f"this module.  STATED LIMITATION: a census of this file, not of "
        f"any consumer elsewhere"))

    return _result(
        "check_T_partial_dephasing_controls", legs,
        key_result=(
            "Permanent controls, computed: refining the record strictly "
            "shrinks the surviving record-blind coherence functional and "
            "coarsening restores it exactly (both directions by value; the "
            "decoherence-control direction, control genre only, no "
            "supplier claim); rival non-conditional-expectation maps fail "
            "idempotence or the tie by value; the no-sign-read scan and "
            "the form-(b) non-consumption scan are executed, both scoped "
            "to this module."),
        cross_refs=["L_commutative_no_unresolved_hold"],
        disclosures=[
            "both scans are exact-token / AST censuses of this module's "
            "own source only; consumers elsewhere are outside their reach",
            "'decoherence' names the control genre only; no physical "
            "process claim is made",
        ])


# ---------------------------------------------------------------------------
# bare-name check table + registration (D6@2026-08-03)
# ---------------------------------------------------------------------------

_CHECKS = {
    "T_record_subsystem_partial_dephasing":
        check_T_record_subsystem_partial_dephasing,
    "L_full_algebra_recovers_banked_dephasing":
        check_L_full_algebra_recovers_banked_dephasing,
    "L_record_blind_invisibility":
        check_L_record_blind_invisibility,
    "L_partial_dephasing_endpoints":
        check_L_partial_dephasing_endpoints,
    "T_partial_dephasing_controls":
        check_T_partial_dephasing_controls,
}


def register(registry):
    registry.update(_CHECKS)
    return registry


def run_all():
    return {name: fn() for name, fn in _CHECKS.items()}


if __name__ == "__main__":
    import sys
    results = run_all()
    total_legs = 0
    all_green = True
    for name, r in results.items():
        total_legs += r["leg_count"]
        status = "PASS" if r["passed"] else "FAIL"
        print(f"{status}  {name}  legs={r['leg_count']}")
        for reason in r["fail_reasons"]:
            print(f"    - {reason}")
        all_green = all_green and r["passed"]
    print(f"checks={len(results)} legs={total_legs} "
          f"{'ALL GREEN' if all_green else 'RED'}")
    sys.exit(0 if all_green else 1)
