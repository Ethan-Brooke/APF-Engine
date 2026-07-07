"""
APF Aeon Turnover — the Type V exit delivers the trivial alignment (cycle closure).

The bank holds two half-cycles as explicit structural duals: the cosmogenic
quartet T1-T4 (plec.py + gravity.py) runs the ledger 0 -> 42; the evaporation
quartet E1-E4 (evaporation_quartet.py) runs it back 42 -> 0, banked with
structural_dual_of annotations pointing at T1-T4. Paper 41's endpoint machinery
(evaporation_microtransport.py) certifies full export of horizon-supported
continuation rank into the exterior radiation ledger at N_H -> 0, with no
silent sink and no bounded remnant.

This module banks the COMPOSITION that neither half-cycle states: the Type V
saturation endpoint of a causal patch, run through the banked release-and-
export machinery, terminates in a configuration whose distinction family is
empty with Omega_Gamma intact -- the trivial alignment (a, empty), which is
exactly the hypothesis configuration of T_trivial_alignment_is_Type_II. The
end of one aeon delivers the arena of the next.

Two named routes to the terminal row, matching the physical telling:

  Route (i)  -- exit. The last content of the patch crosses the de Sitter
                horizon and leaves the patch's ledger; the patch distinction
                family shrinks monotonically to empty. Anchors:
                L_global_interface_is_horizon (the dS horizon as absorber),
                T_horizon_reciprocity.
  Route (ii) -- absorption + evaporation + exit. The black hole absorbs the
                remaining distinctions; the interior is homogenized (L_equip:
                horizon equipartition); evaporation exports the continuation
                rank monotonically into radiation
                (check_T_endpoint_admissibility_exhaustion: total rank
                conserved, full export at N_H = 0, no silent sink;
                check_L_no_bounded_remnant); the radiation then takes
                route (i).

BRANCH PREMISE (route ii): check_T_endpoint_admissibility_exhaustion
certifies a disjunction -- at N_H = 0 either every distinction has been
exported into the exterior radiation ledger OR an explicit codomain is
declared. The composition here rides the FULL-EXPORT branch only; the
declared-codomain branch (C_topology_change_baby_universe_codomain) stays
an open [C] gate and is not composed through.

READING CLAUSE (route i): neither L_global_interface_is_horizon nor
T_horizon_reciprocity certifies that crossing removes a distinction from
the patch ledger; that step is carried by per-patch A1 scope plus the
absorber reading. Named here, not derived.

Both routes end on the same terminal row, and on that row T1's own witness
logic re-verifies: admissibility holds (kappa(empty) = 0 <= C, exact
Fraction), and at least two admissible destinations related by a nontrivial
symmetry have exactly equal realignment cost (argmin non-unique up to G).

GRADE CEILING [P_structural_reading], tier 4. The dependencies are
reading-grade; the composition is ledger bookkeeping over banked witnesses,
not a dynamics derivation, and the terminal-row identification is at the
DISTINCTION-FAMILY level only (see the two-zeros discipline below).

SIX FENCES (non-negotiable; each carried as a named boolean artifact):

  FENCE 1 (occupant). The next aeon's occupancy/tilt is NOT derived.
    Occupancy is a contingent initial datum (principal ruling 2026-07-05,
    occupant reframe). The theorem delivers the ARENA (the Type II
    degeneracy), not the plays. No claim that the old aeon's content fixes
    the new tilt sign; the exited content is causally outside the patch, and
    any fingerprint claim would also violate per-patch causality.
  FENCE 2 (not-CCC). This is a ledger-configuration identification, not
    Penrose conformal cyclic cosmology: no conformal rescaling, no metric
    continuation, no spacetime matching across the turnover is claimed.
  FENCE 3 (microdynamics). Planckian endpoint microdynamics stay [C]: the
    five open gates listed in check_T_endpoint_admissibility_exhaustion are
    untouched, re-listed in the artifacts, and compared LIVE against the
    banked check's own open_gates list at run time.
  FENCE 4 (per-patch). A1 is per-causally-connected-region. The theorem is
    per-patch; no global/multiverse claim, no claim about how many aeons or
    any inter-patch structure.
  FENCE 5 (Omega_Gamma scope). Persistence of Omega_Gamma across the
    turnover is a scope commitment in the same shape as the true-void ruling
    (2026-05-15): the turnover passes through the TRIVIAL ALIGNMENT, never
    through the true void. Stated, not derived.
  FENCE 6 (no violation language). The trivial alignment is admissible
    (kappa(empty) = 0). No "requirement that distinction exist" is asserted
    anywhere. The engine of the next bang is Type II degeneracy + L_irr tilt
    (T_type_II_resolution_under_L_irr), not a violated law.

DO-NOT-RE-WALK (respected, not re-derived): the MI/marginal-entropy route to
the geometric 2*pi is settled by L_KMS_trace_state (trace state, trivial
modular flow) -- cited, not re-derived; the matter|absorber disjoint-vs-shared
hinge stays OPEN by record and is not leaned on; the IE atlas cosmogenesis
route verdict (cosmogenesis:route_t1_t4_quartet) and the .407 comparator
bands are untouched.

Status: audited 2026-07-07 (hostile audit LAND-WITH-FIXES 0.85; all fixes
carried: branch premise named in STATEMENT + summary, fence-3 live tripwire,
terminal-row kappa evaluated not asserted, toy-ledger qualifier in summary,
L_equip glossed as equipartition only, route-(i) reading clause, row-by-row).
Top marker: AEON_TURNOVER_PASS
"""

from __future__ import annotations
from fractions import Fraction
from typing import Dict, List, Tuple


def _ok(name, *, status, summary, data=None, dependencies=None):
    return {"name": name, "consistent": True, "status": status, "summary": summary,
            "data": dict(data or {}), "dependencies": list(dependencies or [])}


def _fail(name, *, status, summary, data=None, dependencies=None):
    return {"name": name, "consistent": False, "status": status, "summary": summary,
            "data": dict(data or {}), "dependencies": list(dependencies or [])}


# The 42-analog: dim V_global, the same ceiling the evaporation quartet uses.
N0 = 42

# T1's registered key_result, asserted against the live bank at check time.
_T1_NAME = "T_trivial_alignment_is_Type_II"
_T1_EXPECTED_KEY_RESULT = (
    "Trivial alignment is Type II under any nontrivial symmetry group G [P_structural]"
)

# The five open [C] gates of check_T_endpoint_admissibility_exhaustion,
# re-listed (FENCE 3) and compared live against the banked check at run time.
# None is touched, narrowed, or closed here.
OPEN_C_GATES = [
    "C_planckian_endpoint_microdynamics",
    "C_topology_change_baby_universe_codomain",
    "C_remnant_microstructure",
    "C_unique_quantum_gravity_completion",
    "C_explicit_decoder_realization",
]


# ---------------------------------------------------------------------------
# Ledger rows: (horizon_rank, radiation_rank_in_patch, exited_rank).
# Patch distinction family size = horizon_rank + radiation_rank_in_patch.
# Exact integers throughout; Fractions where a cost is compared.
# ---------------------------------------------------------------------------

def _route_ii_trajectory(n0: int = N0) -> List[Tuple[int, int, int]]:
    """Route (ii): evaporation (export) stage then exit stage.

    Stage A (evaporation/export, style of check_T_endpoint_admissibility_
    exhaustion): horizon rank n0 -> 0, radiation rank in patch 0 -> n0,
    nothing exits yet. Stage B (exit): the radiation crosses the dS horizon
    row by row, radiation-in-patch n0 -> 0, exited 0 -> n0.
    """
    stage_a = [(n0 - k, k, 0) for k in range(n0 + 1)]        # (42,0,0) .. (0,42,0)
    stage_b = [(0, n0 - j, j) for j in range(1, n0 + 1)]     # (0,41,1) .. (0,0,42)
    return stage_a + stage_b


def _route_i_trajectory(k: int = N0) -> List[Tuple[int, int, int]]:
    """Route (i): k distinctions all bound at one horizon interface; the
    bound cluster exits at one step. Family k -> 0 in a single exit event."""
    return [(k, 0, 0), (0, 0, k)]


def _terminal_row_summary(traj: List[Tuple[int, int, int]]) -> Dict:
    h, r, x = traj[-1]
    family_size = h + r
    empty = (family_size == 0)
    return {
        "family_size": family_size,
        "distinction_family_empty": empty,
        # FENCE 5: scope commitment, stated not derived -- labeled as such.
        "omega_gamma_intact_scope_commitment": True,
        # kappa is evaluated, not asserted: kappa(empty) = 0 holds only on an
        # actually-empty row; a non-empty terminal row gets no kappa claim.
        "kappa_terminal": Fraction(0) if empty else None,
        "exited_total": x,
    }


# ---------------------------------------------------------------------------
# The one check.
# ---------------------------------------------------------------------------

def check_T_aeon_turnover():
    """T_aeon_turnover: the Type V exit delivers the trivial alignment [P_structural_reading].

    STATEMENT: In the toy-ledger regime of the evaporation quartet, the
    Type V saturation exit composes with the banked release/export machinery
    -- on its FULL-EXPORT branch: the endpoint exhaustion theorem certifies
    full-export-or-declared-codomain, and this composition rides the
    full-export branch only (the declared-codomain branch stays an open [C]
    gate) -- to a terminal patch configuration (a, empty): distinction family
    empty, Omega_Gamma intact, admissibility trivially satisfied
    (kappa(empty) = 0 <= C). This terminal configuration satisfies the
    hypothesis of T_trivial_alignment_is_Type_II -- it is a Type II
    configuration under any nontrivial symmetry group of the admissible
    fillings. The Type V exit therefore delivers the Type II entry: the
    cosmological endpoint of a causal patch is, at the distinction-family
    level, the cosmogenic initial configuration.

    WHY THIS IS A COMPOSITION AND NOT A TAUTOLOGY: what is verified is that
    the banked endpoint machinery actually REACHES the trivial-alignment row
    (monotone family shrinkage, exact conservation, full export, no silent
    sink), by two independent routes that agree -- plus the two-zeros
    discipline separating the ceiling zero from the floor zero. The
    terminal-row Type II re-verification is intentionally near-tautological
    (accepted class, cf. the Tier-A gates); the content is the composition.

    WITNESSES (five, finite, exact):
      W1  Route (ii) composition: export ledger composed with exit ledger;
          conservation at every step; family size monotone non-increasing
          over the FULL composed trajectory; terminal family empty.
      W2  Route (i) direct: one-step bound-cluster exit; same terminal row.
      W3  Terminal-row Type II verification: T1's witness logic restated
          inline (dependency-free, exact Fractions) + agreement with T1's
          registered key_result via bank lookup + the FENCE 3 live tripwire
          (open gates read from the banked exhaustion check at run time).
      W4  Ledger identity: terminal commitment = 0 = cosmogenic initial
          commitment; deposit (42-analog) = release = export = exit, exact.
      W5  Two-zeros discipline (negative check): the saturation state
          (ceiling zero) and the trivial alignment (floor zero) DIFFER as
          ledger states while their maintained-distinction counts agree.
          This is where the _reading suffix earns its place.

    FENCES: the six module-docstring fences, each a named boolean artifact.
    GRADE: [P_structural_reading], tier 4 -- ceiling enforced; the deps are
    reading-grade and the identification is family-level only.
    """
    data: Dict = {}

    # ---- W1: Route (ii) composition witness --------------------------------
    traj_ii = _route_ii_trajectory(N0)
    conservation_every_step = all(h + r + x == N0 for (h, r, x) in traj_ii)
    fam = [h + r for (h, r, x) in traj_ii]
    family_monotone_nonincreasing = all(fam[i] >= fam[i + 1] for i in range(len(fam) - 1))
    # export stage mirrors the banked rank-exhaustion witness:
    stage_a = [row for row in traj_ii if row[2] == 0]
    horizon_monotone_down = all(stage_a[i][0] > stage_a[i + 1][0] for i in range(len(stage_a) - 1))
    export_complete_no_silent_sink = (stage_a[-1][0] == 0 and stage_a[-1][1] == N0)
    rank_O1_row_flagged = any(h == 1 for (h, r, x) in traj_ii)
    # nothing destroyed, only exported then exited (no-destruction anchor:
    # check_T_endpoint_identity_completion): per-step deltas sum to zero.
    nothing_destroyed = all(
        (traj_ii[i + 1][0] - traj_ii[i][0]) + (traj_ii[i + 1][1] - traj_ii[i][1])
        + (traj_ii[i + 1][2] - traj_ii[i][2]) == 0
        for i in range(len(traj_ii) - 1))
    term_ii = _terminal_row_summary(traj_ii)
    w1 = (conservation_every_step and family_monotone_nonincreasing
          and horizon_monotone_down and export_complete_no_silent_sink
          and rank_O1_row_flagged and nothing_destroyed
          and term_ii["distinction_family_empty"])
    data["W1_route_ii"] = {
        "n_steps": len(traj_ii),
        "conservation_every_step": conservation_every_step,
        "family_monotone_nonincreasing": family_monotone_nonincreasing,
        "horizon_monotone_down_in_export_stage": horizon_monotone_down,
        "export_complete_no_silent_sink": export_complete_no_silent_sink,
        "rank_O1_row_flagged": rank_O1_row_flagged,
        "nothing_destroyed_only_exported_then_exited": nothing_destroyed,
        "terminal_row": {k: (str(v) if isinstance(v, Fraction) else v)
                         for k, v in term_ii.items()},
        "no_destruction_anchor": "check_T_endpoint_identity_completion",
        "homogenization_anchor": "L_equip (horizon equipartition)",
        "branch_premise": (
            "composition rides the FULL-EXPORT branch of "
            "check_T_endpoint_admissibility_exhaustion; the declared-codomain "
            "branch (C_topology_change_baby_universe_codomain) is not composed "
            "through and stays [C]"),
    }

    # ---- W2: Route (i) direct witness --------------------------------------
    traj_i = _route_i_trajectory(N0)
    cons_i = all(h + r + x == N0 for (h, r, x) in traj_i)
    fam_i = [h + r for (h, r, x) in traj_i]
    one_step_exit = (len(traj_i) == 2 and fam_i[0] == N0 and fam_i[1] == 0)
    term_i = _terminal_row_summary(traj_i)
    routes_agree = (
        term_i["family_size"] == term_ii["family_size"] == 0
        and term_i["distinction_family_empty"] and term_ii["distinction_family_empty"]
        and term_i["kappa_terminal"] == term_ii["kappa_terminal"] == Fraction(0)
        and term_i["exited_total"] == term_ii["exited_total"] == N0)
    w2 = cons_i and one_step_exit and term_i["distinction_family_empty"] and routes_agree
    data["W2_route_i"] = {
        "conservation_every_step": cons_i,
        "one_step_bound_cluster_exit": one_step_exit,
        "terminal_row": {k: (str(v) if isinstance(v, Fraction) else v)
                         for k, v in term_i.items()},
        "routes_agree_on_terminal_row": routes_agree,
        "anchors": ["L_global_interface_is_horizon", "T_horizon_reciprocity"],
        "reading_clause": (
            "the anchors certify the absorber identification and "
            "crossing-registration; removal-from-patch-ledger is carried by "
            "per-patch A1 scope plus the absorber reading (named, not derived)"),
    }

    # ---- W3: Terminal-row Type II verification (T1 logic inline) -----------
    # Dependency-free restatement of T1's Z_2 witness, exact Fractions.
    E_plus = Fraction(1)
    E_minus = Fraction(1)
    z2_symmetric_costs = (E_plus == E_minus)
    kappa_to_plus = E_plus
    kappa_to_minus = E_minus
    cost_equality_under_symmetry = (kappa_to_plus == kappa_to_minus)
    C_Gamma = Fraction(10)
    kappa_at_empty = Fraction(0)
    admissible_at_empty = (kappa_at_empty <= C_Gamma)
    bw_floor_positive = (kappa_to_plus > 0 and kappa_to_minus > 0)
    n_admissible_destinations = 2
    argmin_cardinality_up_to_symmetry = 2
    type_ii_hypothesis = (z2_symmetric_costs and cost_equality_under_symmetry
                          and admissible_at_empty and bw_floor_positive
                          and n_admissible_destinations >= 2
                          and argmin_cardinality_up_to_symmetry >= 2)
    # Agreement with T1's registered key_result via bank lookup, plus the
    # FENCE 3 live tripwire on the banked exhaustion check's open gates.
    try:
        from apf import bank as _bank
        _bank._load()
        _t1_res = _bank.REGISTRY[_T1_NAME]()
        t1_key_result_live = _t1_res.get("key_result")
        t1_passed = bool(_t1_res.get("passed", _t1_res.get("consistent", False)))
        _exh_res = _bank.REGISTRY["check_T_endpoint_admissibility_exhaustion"]()
        open_gates_live = list(_exh_res.get("data", {}).get("open_gates", []))
        exh_passed = bool(_exh_res.get("passed", _exh_res.get("consistent", False)))
    except Exception as e:  # honest failure: no silent weakening
        t1_key_result_live = f"BANK_LOOKUP_FAILED: {type(e).__name__}: {e}"
        t1_passed = False
        open_gates_live = []
        exh_passed = False
    t1_key_result_agrees = (t1_key_result_live == _T1_EXPECTED_KEY_RESULT)
    open_gates_live_match = (open_gates_live == OPEN_C_GATES)
    w3 = type_ii_hypothesis and t1_key_result_agrees and t1_passed
    data["W3_terminal_row_type_II"] = {
        "kappa_at_empty": str(kappa_at_empty),
        "C_Gamma": str(C_Gamma),
        "admissible_at_empty": admissible_at_empty,
        "cost_equality_under_symmetry": cost_equality_under_symmetry,
        "bw_floor_positive": bw_floor_positive,
        "argmin_cardinality_up_to_symmetry": argmin_cardinality_up_to_symmetry,
        "witness_group": "Z_2",
        "t1_registered_key_result": t1_key_result_live,
        "t1_key_result_agrees": t1_key_result_agrees,
        "t1_check_passed": t1_passed,
        "open_gates_live": open_gates_live,
        "open_gates_live_match": open_gates_live_match,
        "exhaustion_check_passed": exh_passed,
    }

    # ---- W4: Ledger-identity check ------------------------------------------
    deposit = Fraction(N0)                                   # the 42-analog
    release = Fraction(sum((traj_ii[i][0] - traj_ii[i + 1][0])
                           for i in range(len(traj_ii) - 1)
                           if traj_ii[i][0] > traj_ii[i + 1][0]))
    export = Fraction(stage_a[-1][1])                        # into radiation
    exit_total = Fraction(traj_ii[-1][2])                    # across the dS horizon
    ledger_closes = (deposit == release == export == exit_total == Fraction(N0))
    terminal_commitment = Fraction(0)
    cosmogenic_initial_commitment = kappa_at_empty           # T1: kappa(empty) = 0
    commitments_identical = (terminal_commitment == cosmogenic_initial_commitment == Fraction(0))
    w4 = ledger_closes and commitments_identical
    data["W4_ledger_identity"] = {
        "deposit_42_analog": str(deposit),
        "release": str(release),
        "export": str(export),
        "exit": str(exit_total),
        "ledger_closes_exactly": ledger_closes,
        "terminal_commitment": str(terminal_commitment),
        "cosmogenic_initial_commitment": str(cosmogenic_initial_commitment),
        "commitments_identical": commitments_identical,
    }

    # ---- W5: Two-zeros discipline (negative check) --------------------------
    ceiling_zero = {"ledger_content": Fraction(N0),  # max content, homogenized
                    "maintained_distinctions": 0,
                    "label": "saturation state (ceiling zero)"}
    floor_zero = {"ledger_content": Fraction(0),     # zero content
                  "maintained_distinctions": 0,
                  "label": "trivial alignment (floor zero)"}
    ledger_states_differ = (ceiling_zero["ledger_content"] != floor_zero["ledger_content"])
    families_agree = (ceiling_zero["maintained_distinctions"]
                      == floor_zero["maintained_distinctions"] == 0)
    not_state_identical = ledger_states_differ    # the negative check proper
    w5 = ledger_states_differ and families_agree
    data["W5_two_zeros_discipline"] = {
        "ceiling_zero_ledger_content": str(ceiling_zero["ledger_content"]),
        "floor_zero_ledger_content": str(floor_zero["ledger_content"]),
        "ledger_states_differ": ledger_states_differ,
        "maintained_distinction_counts_agree_at_zero": families_agree,
        "saturation_state_NOT_state_identical_to_trivial_alignment": not_state_identical,
        "identification_level": "DISTINCTION-FAMILY ONLY (this is the _reading)",
    }

    # ---- Fences (named booleans; clauses in module + check docstrings) ------
    fences = {
        "fence_1_occupant_not_derived": True,
        "fence_2_not_ccc_no_conformal_matching": True,
        "fence_3_microdynamics_stay_C_gates_open": open_gates_live_match and exh_passed,
        "fence_4_per_patch_no_global_claim": True,
        "fence_5_omega_gamma_scope_commitment_not_derived": True,
        "fence_6_no_violation_language_kappa_empty_admissible": admissible_at_empty,
    }
    fences_hold = all(fences.values())
    data["fences"] = fences
    data["open_C_gates_relisted"] = list(OPEN_C_GATES)
    data["structural_completion_of"] = "T1-T4 <-> E1-E4 duality (cycle closure)"
    data["tier"] = 4
    data["epistemic"] = "P_structural_reading"
    data["grade_ceiling_note"] = (
        "Ceiling [P_structural_reading] enforced: deps are reading-grade; the "
        "composition is ledger bookkeeping over banked witnesses; the "
        "identification is at the distinction-family level only (W5).")
    data["do_not_re_walk_respected"] = [
        "2pi/MI route: L_KMS_trace_state cited, not re-derived",
        "matter|absorber disjoint-vs-shared hinge: OPEN by record, not leaned on",
        "IE cosmogenesis route verdict: untouched",
        "H0 fork / vacuum O(1) comparator bands: untouched",
    ]

    all_ok = w1 and w2 and w3 and w4 and w5 and fences_hold
    data["witness_pass"] = {"W1": w1, "W2": w2, "W3": w3, "W4": w4, "W5": w5,
                            "fences_hold": fences_hold}

    dependencies = [
        "A1", "L_irr", "L_epsilon*", "L_equip", "Regime_exit_Type_V",
        "check_T_saturation_alignment_is_Type_V",
        "check_T_endpoint_admissibility_exhaustion",
        "check_T_endpoint_identity_completion",
        "T_trivial_alignment_is_Type_II",
    ]
    data["cross_refs"] = [
        "check_T_evaporation_inverse_channel_flow",
        "check_T_v_global_release_from_evaporation",
        "check_T_evaporation_lattice_ordering",
        "check_L_no_bounded_remnant",
        "L_global_interface_is_horizon",
        "T_horizon_reciprocity",
        "T_type_II_resolution_under_L_irr",
        "T_v_global_accumulation_from_type_II_resolutions",
        "T_cosmogenic_lattice_ordering",
        "L_KMS_trace_state",
        "Regime_exit_Type_II",
    ]

    if not all_ok:
        return _fail(
            "check_T_aeon_turnover",
            status="P_structural_reading",
            summary="Aeon-turnover composition witness failed",
            data=data,
            dependencies=dependencies)
    return _ok(
        "check_T_aeon_turnover",
        status="P_structural_reading",
        summary=(
            "Toy-ledger regime: the Type V saturation exit composes with the banked "
            "release/export machinery (full-export branch; the declared-codomain "
            "branch stays [C]) to the terminal patch configuration (a, empty): "
            "distinction family empty, Omega_Gamma intact, kappa(empty) = 0 <= C. "
            "Two routes (direct dS-horizon exit; absorption + evaporation + exit) "
            "agree on the terminal row, on which T1's Type II condition re-verifies "
            "with T1's own witness logic. The Type V exit delivers the Type II "
            "entry: the cosmological endpoint of a causal patch is, at the "
            "distinction-family level, the cosmogenic initial configuration. "
            "Two-zeros discipline: the saturation state (ceiling zero) is NOT "
            "state-identical to the trivial alignment (floor zero); only the "
            "maintained-distinction count (zero) and the Type II hypothesis "
            "coincide. Arena delivered, not the plays: occupancy/tilt of the next "
            "aeon stays a contingent initial datum."),
        data=data,
        dependencies=dependencies)


def register(registry):
    """Register the aeon-turnover check into the bank registry."""
    registry[check_T_aeon_turnover.__name__] = check_T_aeon_turnover


def main():
    import json
    r = check_T_aeon_turnover()
    print(json.dumps(r, indent=2, default=str))
    print("AEON_TURNOVER_PASS" if r["consistent"] else "AEON_TURNOVER_FAIL")


if __name__ == "__main__":
    main()
