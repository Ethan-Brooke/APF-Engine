"""APF IE wall-shadow census -- the boundary map's cross-index, pinned.

v24.3.401 (2026-07-05). The third instrument of the census family
(export-core dependency census .390, full-surface input inventory .396):
the WALL-SHADOW cross-index. The verdict pin (apf/ie_atlas_verdict_pin.py)
records WHAT each atlas input delivers; this census records WHY the
held/obstructed rows stay held -- specifically, WHICH adjudicated wall
shadows each row whose hold is boundary-shaped, and which rows are
honestly UNSHADOWED because their hold is ordinary owed work.

THE OBJECT. Two pins and a partition:

  WALL_REGISTRY -- the adjudicated walls, typed. A wall is either
    CERTIFIED (its no-go / fence / grade-ceiling / constitutive content is
    carried by named registered bank checks, which this census RUNS) or a
    RULING (a standing principal decision -- NRDT / ICL_vac / LSC -- with
    certificate=() BY CONSTRUCTION and the decision record named as
    source; the census verifies only the ruling's SHADOW rows, it never
    adjudicates the ruling itself).

  SHADOW_MAP -- verdict-pin row -> wall id, for exactly the held/
    obstructed rows whose hold is boundary-shaped: the documented reason
    the row cannot advance IS the named wall (a banked no-go on the
    route, a banked fence on the stronger reading, a banked grade
    ceiling, a constitutive empirical bit, or a standing ruling).

  UNSHADOWED -- the honest remainder: held/obstructed rows whose hold is
    ordinary repair (owed derivation work, pending data admission, open
    computation lanes, engine-native probe design, delivered structural
    obstructions that ARE the certified content, self-certifying named
    closures not seeded as registry walls, substrate-revision pricing).
    Each row carries a reason-cluster id; the census asserts the
    PARTITION, not universal shadowing.

WHAT THE CHECK CERTIFIES (tier 4, [P_structural_instrument]) -- five legs:

  1. WALL INTEGRITY. Every certified wall's certificate checks are
     registered bank checks and PASS when run (executed live in this
     census); every ruling wall carries certificate=() by construction
     and names its decision record. W8's second certificate is the
     occupancy ROOT PIN itself: the census asserts "occupancy" is a
     pinned premise root of the banked export-core inventory (.390/.396).

  2. ROW REALITY. Every SHADOW_MAP key and every UNSHADOWED key is a
     real verdict-pin row whose verdict class is a held/obstructed class
     (the pinned HELD_CLASSES); no export row is mapped.

  3. SET-EXACT PARTITION. SHADOW_MAP keys and UNSHADOWED keys are
     disjoint and their union is EXACTLY the held/obstructed row set of
     the live verdict pin.

  4. TARGET VALIDITY. Every SHADOW_MAP value is a WALL_REGISTRY id;
     every UNSHADOWED value is a pinned reason-cluster id. Walls may
     carry ZERO current shadow rows (W7's rival kills and the NRDT door
     fence future lanes, not current rows) -- disclosed, not hidden.

  5. TRIPWIRE. Because the partition is set-exact against the live pin,
     any FUTURE verdict-pin row that lands in a held/obstructed class
     and is neither shadowed nor dispositioned UNSHADOWED fails the bank
     loudly -- the map cannot rot as the atlas grows.

SCOPE AND HONESTY. The wall ADJUDICATIONS (which wall shadows which row,
and which rows are ordinary repair) are recorded human judgment over the
rows' own documented dispositions (the reviewer-atlas notes, the banked
module docstrings, the decision records), exactly the disclaimer of the
.390/.392/.396 census family; what is machine-verified is the pins'
integrity, the certificates' live PASS, and the set-exact partition.
This census asserts nothing about the world: it is a bank-closed-world
instrument. It does NOT claim any wall is permanent, does NOT adjudicate
the NRDT/ICL_vac/LSC rulings, and does NOT promote any self-certifying
closure row into the registry by mapping it.

FALSIFIERS: a certificate check failing or unregistered; a mapped row
vanishing from the pin or flipping to export; a held row entering the
pin unmapped; a ruling wall acquiring a certificate without a deliberate
registry re-type; a SHADOW_MAP value naming no registered wall.

Dependencies: T_ie_atlas_verdict_tripwire (the pin this census
cross-indexes). Cross-refs: T_ie_export_core_dependency_census,
T_ie_full_surface_input_inventory.
"""

from __future__ import annotations

from typing import Dict, Tuple

from apf.apf_utils import check, _result

# ---------------------------------------------------------------------------
# Pin 0: the held/obstructed verdict classes (everything that is not an
# export verdict; the six classes live in the .398/.400 pin).
# ---------------------------------------------------------------------------

HELD_CLASSES = frozenset({
    "SOLVED_LOCAL_HELD_FOR_REPAIR",
    "OBSTRUCTION_NAMED_CLOSURE",
    "BLOCKED_SUBSTRATE_REVISION_REQUIRED",
    "READOUT_OBSTRUCTION",
    "IJC_OBSTRUCTION",
    "FAIL_CLOSED_PROVENANCE",
})

#: Valid wall types. "ruling" walls carry certificate=() by construction.
WALL_TYPES = ("no_go", "fence", "grade_ceiling", "constitutive", "ruling")

# ---------------------------------------------------------------------------
# Pin 1: the wall registry. Certificate names are REGISTRY KEYS (the .391
# convention: some carry the check_ prefix in the registry, some do not --
# the resolver below tries both). NB two W2 certificates circulate in prose
# with a _P suffix (check_T_ew_prefactor_invariance_no_go_P /
# check_T_yt_absolute_scale_not_fixable_by_normalization_no_go_P); the
# registered keys carry NO suffix -- pinned here as registered.
# ---------------------------------------------------------------------------

WALL_REGISTRY: Dict[str, dict] = {
    "W1_wg2_dictionary": {
        "type": "no_go",
        "module": "apf.wg2_dictionary_typing_no_go",
        "certificates": (
            "L_wg2_dictionary_index_content_blind_native",
            "T_wg2_dictionary_index_no_native_consumer_census",
        ),
        "source": ("the .364 dictionary fence + the .394 C(n) constructor "
                   "census: no banked constructor consumes the measured "
                   "weak-mixing exponent; the EW export gate's one-wall "
                   "story (Paper 42), NRDT the one named door"),
    },
    "W2_absolute_scale_triptych": {
        "type": "no_go",
        "module": "apf.ew_scale_functional_independence",
        "certificates": (
            "T_ew_prefactor_invariance_no_go",
            "T_ew_scale_functional_independence_no_go",
            "T_yt_absolute_scale_not_fixable_by_normalization_no_go",
        ),
        "source": ("the absolute-scale no-go triptych (magnitude / "
                   "prefactor / form, terminated v24.3.314): the "
                   "dimensional hierarchy v_H/M_Pl is the one open ratio; "
                   "identification (B) proven irreducible"),
    },
    "W3_bell_ceiling_calibration": {
        "type": "grade_ceiling",
        "module": "apf.fencea_hinge_trichotomy",
        "certificates": (
            "T_ladder_ceiling_calibration_from_saturation",
        ),
        "source": ("the Bell-ceiling calibration (.389): 2*sqrt(2)*102/103 "
                   "framework-anchored at [P_structural_reading]; the "
                   "discharge to [P] is a principled wall (saturation "
                   "never forced) -- adjudicated 2026-07-04, do-not-re-walk"),
    },
    "W4_strong_cp_transport": {
        "type": "no_go",
        "module": "apf.strong_cp_completion_no_go",
        "certificates": (
            "L_completion_angle_content_blind_native",
        ),
        "source": ("the .359 transport-half content-blindness no-go: the "
                   "alpha-completion is content-blind on theta-bar; the "
                   "transport half is unreachable-by-[P] (Paper 46 anchors "
                   "the ceiling); NRDT the one named door"),
    },
    "W5_solder_slot_record": {
        "type": "no_go",
        "module": "apf.colour_solder_form_no_go",
        "certificates": (
            "T_colour_solder_form_no_go",
            "T_vglobal_slot_identification_no_go",
            "check_T_matter_free_colour_record_deep_superselection_no_go",
        ),
        "source": ("the solder/slot/record family: canonical-B neither "
                   "storable nor constructible (.367); slot-level "
                   "global-stratum identification impossible unbroken (.326); matter-free "
                   "colour records deeply superselected -- adoption (the "
                   "named ICL conjecture) is the only door"),
    },
    "W6_over_reading_fences": {
        "type": "fence",
        "module": "(cross-module fence family)",
        "certificates": (
            "T_ledger_rent_excluded",
            "check_T_delta_not_an_information_functional",
            "check_T_colour_contextuality_is_kstring_spectrum_blind",
            "T_banked_registration_coherent_recovery_no_go",
            "L_RT_two_sided_reading_no_go",
            "T_w_observed_MW_excluded_from_input_basis",
        ),
        "source": ("the banked over-reading fences: rent exclusion, Delta "
                   "is not an information functional, contextuality is "
                   "k-string-spectrum-blind, no coherent recovery from "
                   "banked registration, no two-sided RT reading, measured "
                   "M_W excluded from the input basis"),
    },
    "W7_rival_kills": {
        "type": "no_go",
        "module": "apf.killed_rivals",
        "certificates": (
            "R_SU_Nc_neq_3_killed",
            "R_Ngen_neq_3_killed",
            "R_extra_axiom_NT_killed",
            "R_Born_axiomatic_killed",
            "T_killed_rivals_v0",
        ),
        "source": ("the structural rival kills: these fence RIVAL lanes, "
                   "not current atlas rows -- the shadow set is empty by "
                   "honest measurement, disclosed in leg 4"),
    },
    "W8_occupancy_constitutive": {
        "type": "constitutive",
        "module": "apf.quantum_admissibility",
        "certificates": (
            "T_quantum_admissibility_condition",
        ),
        "source": ("the constitutive empirical bit: occupancy (QAC), "
                   "co-equal with A1 per the 2026-07-01 ruling; the second "
                   "certificate is the occupancy ROOT PIN itself "
                   "(EXPORT_ROOT_INVENTORY / FULL_SURFACE_TYPED_ROOTS, "
                   "asserted in leg 1) -- a declared root, not a defect"),
    },
    # -- ruling walls: standing principal decisions. certificate=() BY
    #    CONSTRUCTION; the census verifies their shadow rows only and
    #    NEVER adjudicates the rulings.
    "R_NRDT": {
        "type": "ruling",
        "module": None,
        "certificates": (),
        "source": ("NRDT RULED HOLD 2026-07-03 (named, not adopted -- the "
                   "ICL_vac/LSC pattern); the one named door through W1/W4; "
                   "record: the 2026-07-03 decision notes (wiki Log + "
                   "Reference decision records)"),
    },
    "R_ICL_vac": {
        "type": "ruling",
        "module": None,
        "certificates": (),
        "source": ("ICL_vac adoption ruling pending (route-(b) witness "
                   "family banked .352/.356/.357; adoption is "
                   "principal-ruling-shaped); record: Reference - Decisions "
                   "List - Consolidation of the 2026-07-02 Threads.md"),
    },
    "R_LSC": {
        "type": "ruling",
        "module": None,
        "certificates": (),
        "source": ("LSC RULED HOLD 2026-07-02 (no axiom promotion; the H0 "
                   "fork deliberately preserved per the principal's "
                   "charter); record: Reference - Decisions List - "
                   "Consolidation of the 2026-07-02 Threads.md"),
    },
}

# ---------------------------------------------------------------------------
# Pin 2: the shadow map -- held/obstructed verdict-pin row -> wall id.
# Adjudicated row-by-row from the rows' own documented dispositions
# (reviewer-atlas notes, module docstrings, decision records); recorded
# human judgment, tripwired by the set-exact partition below.
# ---------------------------------------------------------------------------

SHADOW_MAP: Dict[str, str] = {
    # -- W1: the wg2 dictionary wall (the EW export gate).
    "ew:wg2_dictionary_typing_no_go": "W1_wg2_dictionary",
    #    ^ the wall's own atlas row (.364 closure-by-design obstruction).
    "claim:ew_global_export": "W1_wg2_dictionary",
    #    ^ the EW global-export claim probe: the .394 census closed the
    #      gate lane (no banked constructor consumes the measured index);
    #      the one-wall story of Paper 42, NRDT the sole named door.

    # -- W2: the absolute-scale triptych.
    "ew:absolute_scale_frontier_terminated": "W2_absolute_scale_triptych",
    #    ^ the triptych terminus head row itself (v24.3.314).
    "flavour:yt_normalization_no_go": "W2_absolute_scale_triptych",
    #    ^ the triptych's yt leg (its own obstruction-result row).
    "ew:sigma_scale_formula_held": "W2_absolute_scale_triptych",
    #    ^ the v_H capacity formula: reproduced-but-held; the absolute
    #      scale is exactly the triptych-walled quantity.
    #      (.401 audit m4 rider, 2026-07-05: the W2 mapping is defensible
    #      via the absolute-scale family, but this row's atlas note cites
    #      a bespoke held-gate token, not the triptych by name.)
    "ew:sigma_scale_yukawa_free_floor": "W2_absolute_scale_triptych",
    #    ^ the Yukawa-free geometric floor component of the same lane.
    "ew:mcross_planck_ratio_reading": "W2_absolute_scale_triptych",
    #    ^ M_cross/M_Pl at [P_structural_reading] under the never-promote
    #      discipline (.365); what blocks [P] is the scale-functional
    #      independence no-go (identification irreducible).
    "ew:planck_anchor_bekenstein_forced": "W2_absolute_scale_triptych",
    #    ^ the Planck-anchor route's sibling probe (SSU route refuted,
    #      frontier terminated .314).
    "foundation:single_dimensional_anchor": "W2_absolute_scale_triptych",
    #    ^ the single-dimensional-anchor billing row: the anchor's
    #      magnitude is what the triptych proves underivable (v_H/M_Pl
    #      the one open ratio).

    # -- W3: the Bell-ceiling calibration grade ceiling.
    "foundation:fencea_hinge_trichotomy_ladder": "W3_bell_ceiling_calibration",
    #    ^ the ladder module's held row: the ceiling calibration is
    #      reading-conditional; the [P] discharge is the adjudicated
    #      principled wall (saturation never forced).

    # -- W4: the strong-CP transport wall.
    "strong:strong_cp_transport_content_blind": "W4_strong_cp_transport",
    #    ^ the wall's own atlas row (.359 closure-by-design obstruction).

    # -- W5: the solder/slot/record family.
    "gauge:colour_solder_form_no_go": "W5_solder_slot_record",
    #    ^ the wall's own atlas row (.367 closure-by-design obstruction).
    "foundation:formal_kernel_theorem11_and_slot_no_go": "W5_solder_slot_record",
    #    ^ the slot no-go row ("never cite the slot-level global-stratum
    #      identification as an open lead").
    "foundation:base_fiber_allocation": "W5_solder_slot_record",
    #    ^ the no-B substrate row: its boundary is the solder/record
    #      family (matter-free deep-superselection no-go); closure beyond
    #      it needs the named ICL conjecture -- a second commitment, not
    #      repair work.
    "claim:gauge_fiber": "W5_solder_slot_record",
    #    ^ the gauge-fiber claim probe: canonical-B storage/construction
    #      routes are closed by the solder-form no-go; adoption is the
    #      only door (.367).

    # -- W6: the over-reading fences.
    "strong:lattice_gap_candidate": "W6_over_reading_fences",
    #    ^ contextuality certifies gap EXISTENCE only; the route from the
    #      banked obstruction to the tension/spectrum law is fenced
    #      spectrum-blind (.299/.300) -- the candidate framing is the
    #      banked framing.

    # -- W8: the constitutive empirical bit.
    "foundation:four_input_declaration": "W8_occupancy_constitutive",
    #    ^ the framework's input billing row: held because the empirical
    #      bit (occupancy/QAC) is a DECLARED constitutive input -- a
    #      profile fact, not a repairable defect.

    # -- ruling shadows.
    "quantum:vacuum_label_code_p1_witness": "R_ICL_vac",
    #    ^ the row's own note names the hold: the ICL_vac route-(b)
    #      witness family, adoption ruling pending.
    "quantum:vacuum_scheme_covariance_split": "R_ICL_vac",
    #    ^ the .373 covariance split: residue = S_42-covariant open + the
    #      ICL_vac adoption ruling.
    "strong:vacuum_realization_triptych": "R_ICL_vac",
    #    ^ the vacuum-realization arc: residue = identification (B) + the
    #      ICL_vac adoption, both principal-ruling-shaped.
    "gravity:vacuum_o1_h0_fork": "R_LSC",
    #    ^ the H0 fork row: deliberately preserved per the principal's
    #      charter (the 2026-07-02 consolidation record) -- a
    #      ruling-shaped hold, not a defect.
}

# ---------------------------------------------------------------------------
# Pin 3: the honest remainder -- held/obstructed rows whose hold is
# ordinary owed work, dispositioned into reason clusters. The census
# asserts the PARTITION (pin 2 + pin 3 == the held rows, set-exact).
# ---------------------------------------------------------------------------

UNSHADOWED_REASONS: Dict[str, str] = {
    "grade_mirror": (
        "held because the banked content carries non-[P] structural/"
        "reading/seam/instrument/bespoke grades (or claim-level scope "
        "riders); the hold mirrors the grade, repair is the lane's own "
        "owed derivation work -- no single adjudicated wall names it"),
    "open_computation_lane": (
        "open computation lane (the W-trace/EW transport family): the "
        "v15.1 [P_boundary] adjudication + admitted-row / remainder debt; "
        "repair is admission and component certification, deliberately "
        "not registered as a wall here"),
    "data_admission": (
        "pending external-data admission or a signed WATCH (the dark "
        "route / evaporation-gate / neutrino-hierarchy / Cassini family: "
        "Gates 3/4-shaped, data-side, not boundary-shaped)"),
    "engine_native_probe": (
        "engine-native claim/payload probe held or fail-closed BY LANE "
        "DESIGN (incl. the provenance-smuggling guard, which fail-closes "
        "on purpose); no bank home, nothing to shadow"),
    "delivered_obstruction": (
        "the obstruction IS the certified content (IJC contextuality "
        "witnesses; readout multiplicity/no-record verdicts): a delivered "
        "structural verdict, not a hold awaiting repair"),
    "self_certifying_closure": (
        "closure-by-design row carrying its OWN banked certificate "
        "(pole-scheme obstructions, dark modified-gravity/particle-id "
        "closures, the AGT encoding wall, the saturation guard): a "
        "candidate for a future WALL_REGISTRY row, deliberately not "
        "silently promoted by this census"),
    "substrate_revision": (
        "BLOCKED_SUBSTRATE_REVISION_REQUIRED priced by the claim "
        "compiler: repair is a substrate revision (external-Hamiltonian "
        "pricing, *-algebra closure, composition tokens), not a named "
        "wall"),
}

UNSHADOWED: Dict[str, str] = {
    # engine-native probes (no bank home; lane-design holds)
    "claim:capacity_overspend": "engine_native_probe",
    "claim:generic": "engine_native_probe",
    "claim:horizon_cost": "engine_native_probe",
    "claim:provenance_smuggling": "engine_native_probe",
    "payload:capacity_overspend": "engine_native_probe",
    # substrate-revision pricing
    "claim:cstar_substrate": "substrate_revision",
    "foundation:l_irr_induced_polarity": "substrate_revision",
    "thermo:cost_energy_identity": "substrate_revision",
    "thermo:i4_operator_self_identification": "substrate_revision",
    # data-admission / WATCH rows
    "claim:dark_runtime": "data_admission",
    "payload:dark_runtime_open": "data_admission",
    "dark:phase_space_persistence_kernel": "data_admission",
    "dark:route_cross_sn_profile_probe": "data_admission",
    "dark:route_desi_full_shape_exact": "data_admission",
    "dark:route_full_growth_likelihood": "data_admission",
    "gravity:evaporation_microtransport_gates": "data_admission",
    "gravity:gammaC_carrier_watch": "data_admission",
    "neutrino:route_dune_juno_hierarchy": "data_admission",
    # open computation lanes (v15.1 boundary + remainder debt)
    "claim:ew_local_trace": "open_computation_lane",
    "payload:ew_transport_open": "open_computation_lane",
    "ew:mw_distinction_decomposition": "open_computation_lane",
    "ew:mw_from_3_13_effective_angle": "open_computation_lane",
    "ew:native_oblique_close": "open_computation_lane",
    "ew:osw_source_transcription_families": "open_computation_lane",
    "ew:sin2theta_eff_kappa_l_decomposition": "open_computation_lane",
    "flavour:bottom_msbar_export_candidate": "open_computation_lane",
    "flavour:bottom_msbar_transport_route": "open_computation_lane",
    "flavour:neutrino_mbb_transport": "open_computation_lane",
    "flavour:trace_sector_closure": "open_computation_lane",
    "wtrace:bsy_one_loop_kappa_l_assembly_consistency": "open_computation_lane",
    "wtrace:native_one_loop_mw_close": "open_computation_lane",
    "wtrace:os_route_terminal_closure_open_export": "open_computation_lane",
    "wtrace:two_loop_phase2_router": "open_computation_lane",
    "wtrace:zll_kappa_l_oblique": "open_computation_lane",
    "wtrace:zll_r2_counterterm_pieces": "open_computation_lane",
    # delivered structural obstructions (the content, not a hold)
    "contextuality:magic_square_parity": "delivered_obstruction",
    "contextuality:native_ladder_chsh_violation": "delivered_obstruction",
    "contextuality:pr_box": "delivered_obstruction",
    "flavour:chiral_condensate_yuoh": "delivered_obstruction",
    "quantum:ghz_mermin_state_independent": "delivered_obstruction",
    "quantum:magic_square_threshold_robust": "delivered_obstruction",
    "readout:su2_fund4": "delivered_obstruction",
    "readout:su3_quark_pair": "delivered_obstruction",
    "readout:su3_single_quark": "delivered_obstruction",
    "readout:su3_tetraquark": "delivered_obstruction",
    "spine:inseparable_ijc_345_witness": "delivered_obstruction",
    "strong:pentaquark_magic_square": "delivered_obstruction",
    "strong:tetraquark_kcbs": "delivered_obstruction",
    "strong:tetraquark_yuoh_state_independent": "delivered_obstruction",
    # self-certifying named closures (candidate future walls)
    "foundation:agt_encoding_wall": "self_certifying_closure",
    "dark:saturation_no_go_guard": "self_certifying_closure",
    "payload:bottom_pole_obstruction_real_adapter_live": "self_certifying_closure",
    "payload:charm_pole_obstruction_real_adapter_live": "self_certifying_closure",
    "payload:top_pole_mc_obstruction_real_adapter_live": "self_certifying_closure",
    "payload:dark_modified_gravity_obstruction_real_adapter_live": "self_certifying_closure",
    "payload:dark_particle_id_obstruction_real_adapter_live": "self_certifying_closure",
    # grade-mirror holds (the bulk: held at banked non-[P] grades/scopes)
    # .401 audit m4 (2026-07-05): rows in this cluster whose atlas notes
    # claim all-[P] content are PROMOTION CANDIDATES (.398-style export
    # re-declarations), not grade holds; this census's next version should
    # surface them MECHANICALLY rather than by hand-tag (see the
    # foundation:d4_unique tag below for the one caught by the .401 audit).
    "claim:drawn_content_readings_functional": "grade_mirror",
    "claim:magic_square_4n_rigidity": "grade_mirror",
    "dark:cmb_finite_mode_covariance_prototype": "grade_mirror",
    "dark:lambda_absolute_mixed_grades": "grade_mirror",
    "ew:a_mu_hvp_capacity_density": "grade_mirror",
    "ew:delta_alpha_adler_pqcd_m_z": "grade_mirror",
    "ew:delta_alpha_capacity_density": "grade_mirror",
    "ew:delta_alpha_leptonic": "grade_mirror",
    "ew:delta_alpha_pqcd_m_z": "grade_mirror",
    "ew:delta_rho_leading_distinction": "grade_mirror",
    "ew:orientation_ew_route_priced": "grade_mirror",
    "ew:photon_massless_reversibility": "grade_mirror",
    "ew:pi_gammagamma_2l_moment_native": "grade_mirror",
    "ew:pre_branch_joint_necessity": "grade_mirror",
    "ew:sin2theta_w_os_capacity_counting_gh_codomain": "grade_mirror",
    "ew:sqrtNc_carrier_forced": "grade_mirror",
    "ew:u1y_landau_pole_trans_planckian": "grade_mirror",
    "ew_eigenscreen:coupled_channel_disposition": "grade_mirror",
    "ew_eigenscreen:goldstone_boundary_disposition": "grade_mirror",
    "flavour:charged_fermion_trace_spectrum": "grade_mirror",
    "flavour:down_lepton_trace_vector": "grade_mirror",
    "flavour:quark_trace_anchors": "grade_mirror",
    "flavour:seesaw_from_a1": "grade_mirror",
    "flavour:three_generations_forced": "grade_mirror",
    "flavour:up_family_trace_bridge": "grade_mirror",
    "flavour:up_normalizer_local": "grade_mirror",
    "foundation:acc_ledger_identities": "grade_mirror",
    "foundation:acc_projection_essentiality": "grade_mirror",
    "foundation:acc_three_level_identities": "grade_mirror",
    "foundation:acc_unification_all_p_categorical_closure": "grade_mirror",
    "foundation:acc_unification_no_imports_provenance_gate": "grade_mirror",
    "foundation:billed_vs_derived_register_criterion": "grade_mirror",
    "foundation:class_transition_primitive": "grade_mirror",
    "foundation:closed_world_regime_gates": "grade_mirror",
    "foundation:d4_unique": "grade_mirror",  # .401 audit m4 (2026-07-05): PROMOTION CANDIDATE -- the atlas note says all-[P]; a .398-style export re-declaration candidate, not a grade hold (kept in this pin this leg by design)
    "foundation:forced_universality_classes": "grade_mirror",
    "foundation:geometric_symmetry_internalization": "grade_mirror",
    "foundation:import_internalization_extensions": "grade_mirror",
    "foundation:interface_factoriality_native": "grade_mirror",
    "foundation:itpfi_tail_scalar_on_omega": "grade_mirror",
    "foundation:kappa_int_two_sided_rigidity": "grade_mirror",
    "foundation:mean_field_slack_equation": "grade_mirror",
    "foundation:one_loop_measure_from_d4": "grade_mirror",
    "foundation:operational_completeness_sandwich": "grade_mirror",
    "foundation:paper1_fd1_executable_witness": "grade_mirror",
    "foundation:regime_r_exit_taxonomy": "grade_mirror",
    "foundation:representation_descent_stack": "grade_mirror",
    "foundation:sixteen_case_unification": "grade_mirror",
    "foundation:spectral_action_internalization": "grade_mirror",
    "foundation:subspace_functors_i1_i3_i4": "grade_mirror",
    "foundation:tail_center_trivial_f1": "grade_mirror",
    "gauge:abelian_rank1_capacity_count": "grade_mirror",
    "gauge:acc_reading_selection_map": "grade_mirror",
    "gauge:anchor_electric_center_correspondence": "grade_mirror",
    "gauge:beta_capacity_tiling": "grade_mirror",
    "gauge:photon_slot4_c4_keystone": "grade_mirror",
    "gauge:quotient_pinned_demand": "grade_mirror",
    "gauge:spine_disposition": "grade_mirror",
    "gauge:su2_string_cut_four_clause_verdict": "grade_mirror",
    "gravity:bekenstein_quarter_structural": "grade_mirror",
    "gravity:evaporation_quartet_page_derived": "grade_mirror",
    "gravity:fre_and_lambda_absolute": "grade_mirror",
    "gravity:i1_bridge_at_joint_k42": "grade_mirror",
    "gravity:lambda_operator_level_derivation": "grade_mirror",
    "gravity:observable_transport_gr_nonclaims": "grade_mirror",
    "gravity:phase_14d3_completions": "grade_mirror",
    "gravity:singlet_gram_exchangeable_form": "grade_mirror",
    "instrument:crystal_attribution": "grade_mirror",
    "instrument:enforcement_crystal_walker": "grade_mirror",
    "quantum:i3_operator_self_identification": "grade_mirror",
    "quantum:symmetry_contextuality_orthogonal": "grade_mirror",
    "strong:confinement_single_anchor": "grade_mirror",
    "strong:pi0_anomaly_width_row": "grade_mirror",
    "strong:ym_kappa3_negative": "grade_mirror",
    "strong:ym_quotient_ledger": "grade_mirror",
    "thermo:fluctuation_response_equilibrium": "grade_mirror",
    "thermo:four_laws_composed": "grade_mirror",
    "thermo:negative_temperature_ceiling": "grade_mirror",
    "thermo:thermal_absolute_scope": "grade_mirror",
}


# ---------------------------------------------------------------------------
# The check
# ---------------------------------------------------------------------------

def _resolve_certificate(registry: dict, name: str):
    """Resolve a certificate name against the bank registry (the census
    convention: registry keys sometimes carry the check_ prefix)."""
    for cand in (name, "check_" + name,
                 name[len("check_"):] if name.startswith("check_") else None):
        if cand and cand in registry:
            return cand, registry[cand]
    return None, None


def check_T_ie_wall_shadow_census():
    """T_ie_wall_shadow_census: the boundary map's wall-shadow cross-index
    [P_structural_instrument] -- see the module docstring for the contract."""
    from apf import bank
    bank._load()
    registry = bank.REGISTRY

    # Leg 1a: wall integrity -- types, ruling construction.
    for wid, w in WALL_REGISTRY.items():
        check(w["type"] in WALL_TYPES,
              f"wall {wid}: type {w['type']!r} is a pinned wall type")
        if w["type"] == "ruling":
            check(w["certificates"] == (),
                  f"ruling wall {wid} carries certificate=() BY CONSTRUCTION "
                  "(the census never adjudicates a ruling)")
            check(bool(w["source"]),
                  f"ruling wall {wid} names its decision record")
        else:
            check(len(w["certificates"]) >= 1,
                  f"certified wall {wid} names at least one certificate check")

    # Leg 1b: every certificate is registered and PASSES when run live.
    cert_runs = 0
    for wid, w in WALL_REGISTRY.items():
        for cname in w["certificates"]:
            rkey, fn = _resolve_certificate(registry, cname)
            check(fn is not None,
                  f"wall {wid}: certificate {cname} resolves to a registered "
                  "bank check")
            try:
                r = fn()
            except Exception as exc:  # noqa: BLE001 -- a raise is a FAIL
                check(False,
                      f"wall {wid}: certificate {rkey} raised "
                      f"{type(exc).__name__}: {str(exc)[:120]}")
                continue
            ok = (r is None) or (isinstance(r, dict)
                                 and r.get("passed", True) is not False)
            check(ok, f"wall {wid}: certificate {rkey} PASSES live")
            cert_runs += 1

    # Leg 1c: W8's root-pin contact -- occupancy is a pinned premise root
    # of the banked census inventories (the constitutive certificate).
    from apf.ie_export_core_census import (EXPORT_ROOT_INVENTORY,
                                           FULL_SURFACE_TYPED_ROOTS)
    check("occupancy" in EXPORT_ROOT_INVENTORY,
          "W8 root-pin contact: 'occupancy' is a pinned export-core root")
    check(FULL_SURFACE_TYPED_ROOTS.get("occupancy") == "premise",
          "W8 root-pin contact: 'occupancy' is genre-typed premise on the "
          "full surface")

    # Leg 2: row reality -- every mapped row is a real pin row in a
    # held/obstructed class; no export row is mapped.
    from apf.ie_atlas_verdict_pin import PINNED_VERDICTS
    held = {k for k, v in PINNED_VERDICTS.items()
            if (not v[1]) and v[0] in HELD_CLASSES}
    stray_classes = {v[0] for k, v in PINNED_VERDICTS.items()
                     if (not v[1]) and v[0] not in HELD_CLASSES}
    check(not stray_classes,
          "HELD_CLASSES pin covers every non-export verdict class in the pin "
          f"(unpinned classes: {sorted(stray_classes)[:4]})")
    for m, kind in ((SHADOW_MAP, "SHADOW_MAP"), (UNSHADOWED, "UNSHADOWED")):
        bad = [k for k in m if k not in held]
        check(not bad,
              f"{kind} keys are real held/obstructed pin rows "
              f"(violations: {bad[:4]})")

    # Leg 3: set-exact partition.
    overlap = set(SHADOW_MAP) & set(UNSHADOWED)
    check(not overlap,
          f"partition disjointness: no row is both shadowed and unshadowed "
          f"(overlap: {sorted(overlap)[:4]})")
    mapped = set(SHADOW_MAP) | set(UNSHADOWED)
    missing = held - mapped
    extra = mapped - held
    check(not missing and not extra,
          "SET-EXACT partition / TRIPWIRE: shadowed + unshadowed rows are "
          "exactly the held/obstructed pin rows -- a future held row landing "
          "unmapped fails the bank here "
          f"(unmapped: {sorted(missing)[:5]}; stale: {sorted(extra)[:5]})")

    # Leg 4: target validity (walls may have zero shadow rows -- disclosed).
    bad_targets = sorted({w for w in SHADOW_MAP.values()
                          if w not in WALL_REGISTRY})
    check(not bad_targets,
          f"every SHADOW_MAP value is a registered wall (bad: {bad_targets[:4]})")
    bad_reasons = sorted({r for r in UNSHADOWED.values()
                          if r not in UNSHADOWED_REASONS})
    check(not bad_reasons,
          f"every UNSHADOWED value is a pinned reason cluster (bad: {bad_reasons[:4]})")
    shadowless = sorted(w for w in WALL_REGISTRY
                        if w not in set(SHADOW_MAP.values()))

    n_by_wall: Dict[str, int] = {}
    for w in SHADOW_MAP.values():
        n_by_wall[w] = n_by_wall.get(w, 0) + 1
    n_by_reason: Dict[str, int] = {}
    for r in UNSHADOWED.values():
        n_by_reason[r] = n_by_reason.get(r, 0) + 1

    return _result(
        name="T_ie_wall_shadow_census",
        tier=4,
        epistemic="P_structural_instrument",
        summary=(
            "The wall-shadow cross-index over the verdict pin: "
            f"{len(WALL_REGISTRY)} adjudicated walls (8 certified, 3 "
            f"rulings), {len(SHADOW_MAP)} held/obstructed rows shadowed, "
            f"{len(UNSHADOWED)} pinned UNSHADOWED in "
            f"{len(UNSHADOWED_REASONS)} reason clusters; partition "
            "set-exact against the live pin (the tripwire); every "
            "certificate check run live and PASSING; ruling walls carry "
            "no certificate by construction. Adjudications are recorded "
            "human judgment; the machine verifies the pins, the "
            "certificates, and the partition."
        ),
        key_result=(
            f"Every one of the {len(SHADOW_MAP) + len(UNSHADOWED)} "
            "held/obstructed verdict-pin rows is dispositioned: "
            f"{len(SHADOW_MAP)} boundary-shaped holds name their shadowing "
            f"wall ({', '.join(sorted(n_by_wall))}), {len(UNSHADOWED)} are "
            "honestly UNSHADOWED (ordinary repair / data admission / open "
            "lanes / probes / delivered obstructions / self-certifying "
            f"closures / substrate pricing); {cert_runs} certificate "
            "checks run live, all PASS; shadowless walls disclosed "
            f"({', '.join(shadowless)}). An instrument; asserts no physics."
        ),
        dependencies=["T_ie_atlas_verdict_tripwire"],
        cross_refs=["T_ie_export_core_dependency_census",
                    "T_ie_full_surface_input_inventory"],
        artifacts={
            "wall_registry": {k: {"type": v["type"],
                                  "certificates": list(v["certificates"])}
                              for k, v in WALL_REGISTRY.items()},
            "shadow_counts_by_wall": n_by_wall,
            "unshadowed_counts_by_reason": n_by_reason,
            "shadowless_walls": shadowless,
            "n_held_rows": len(SHADOW_MAP) + len(UNSHADOWED),
        },
    )


_CHECKS = {
    "T_ie_wall_shadow_census": check_T_ie_wall_shadow_census,
}


def register(registry):
    """Register the wall-shadow census into the bank."""
    registry.update(_CHECKS)


def run_all():
    return {name: fn() for name, fn in _CHECKS.items()}


if __name__ == "__main__":
    for _n, _r in run_all().items():
        print(("PASS" if _r.get("passed", True) else "FAIL"), _n)
        print("  ", _r["key_result"])
