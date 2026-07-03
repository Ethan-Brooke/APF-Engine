# APF Reviewer Atlas -- what the framework claims, machine-checked

Generated 2026-07-02 against verdict pin v24.3.348. Every row below is produced by running the banked engine, not written by hand; the committed copy is certified current against the verdict pin by `check_T_ie_reviewer_manifest_current` (a failing bank run means this file is stale).

**How to reproduce**: clone the repo, `python3 verify_all.py --bank-audit` (the full theorem bank, 3824 checks), then `PYTHONPATH=. python3 scripts/gen_reviewer_manifest.py`.

**Reading a verdict**: `EXPORT` = the route exports a global section in the engine's own currency. `held/obstructed` = the route holds with a NAMED obstruction or an honest open disposition -- in this framework obstructions are results (e.g. a Bell/noncontextuality certificate, a no-go, an honest OPEN statement), not defects. Verdicts inherit the grades of the banked theorems they route through; routing confers nothing.

**Coverage**: 203 of 449 loaded modules onboarded (144 directly), 162 of 247 on the physics target surface. Modules not onboarded are honestly so (pipeline stages of banked programs, or abstract interfaces with no payload data).

## Paper 0 + Paper 13 (foundations)

| input | axis | verdict | note |
|---|---|---|---|
| `foundation:acc_ledger_identities` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 4 probe |
| `foundation:acc_projection_essentiality` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 7; flag: docstring prose says 'all [P_structural]' while the machine field is the finer 'P_structural_exhaustive' -- field wins. |
| `foundation:acc_three_level_identities` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 7; grades from the epistemic fields (17 x 'P'); the promotion history is stated, not laundered |
| `foundation:acc_unification_all_p_categorical_closure` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 7; flag: header docstring advertises plain 'P' per piece and check names end in _P, but the machine status tokens are the bespoke P_... |
| `foundation:acc_unification_no_imports_provenance_gate` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 7; grades are the bespoke P_provenance/P_audit/P_cat_fully_closed_no_imports tokens read from the status= fields. |
| `foundation:base_fiber_allocation` | ROUTE | BLOCKED_SUBSTRATE_REVISION_REQUIRED | Wave 4 probe; the no-B row's OPEN status stated honestly |
| `foundation:billed_vs_derived_register_criterion` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 6 depth; the B5 close (.332) |
| `foundation:class_transition_primitive` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 7; flag: the four checks carry NO machine epistemic field (return dicts have only name/passed/key_result/theorem_refs) -- grade live... |
| `foundation:closed_world_regime_gates` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 7; flag: the header docstring grade table is STALE vs the machine fields -- it lists gates (4)-(7) as [P_regime + accounting] and (2... |
| `foundation:d4_unique` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 5 probe; all-[P] verified per epistemic fields |
| `foundation:fencea_hinge_trichotomy_ladder` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 6; the .340/.341 landings; profile clause [P+IJC] stands untouched |
| `foundation:forced_universality_classes` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 7; grade uniform across all 7 checks, matches docstring ('all tier-4 [P_structural]'); C3 conditionality carried as a rider. |
| `foundation:formal_kernel_theorem11_and_slot_no_go` | ROUTE | BLOCKED_SUBSTRATE_REVISION_REQUIRED | Wave 6; spine; never cite slot-level V_global identification as an open lead |
| `foundation:four_input_declaration` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 4 probe; grades letter-checked (the clause is adopted; see the 2026-06-25 canonical-definition note) |
| `foundation:geometric_symmetry_internalization` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 7; fields match docstring. |
| `foundation:import_internalization_extensions` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 7; minor prose drift: header docstring says 'six new theorems' but the module registers seven (check_L_Tannaka_Krein added after the... |
| `foundation:interface_factoriality_native` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 7; current field confirmed 'P' per the v24.3.271 corner-argument regrade; III_lambda type explicitly stays [P_structural] |
| `foundation:itpfi_tail_scalar_on_omega` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 7; native-fragment-only lemma, non-native step (iv) explicitly fenced in-module |
| `foundation:kappa_int_two_sided_rigidity` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 7; module docstring line 34 says all checks are [P_structural] but the sixth carries the narrower regime-restricted token (field wins) |
| `foundation:l_irr_induced_polarity` | ROUTE | BLOCKED_SUBSTRATE_REVISION_REQUIRED | Wave 7 substrate *-algebra closure; docstring 'P_structural' vs machine P_structural_reading/P_audit flagged |
| `foundation:mean_field_slack_equation` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 7; grade read from the epistemic field, matches docstring. |
| `foundation:one_loop_measure_from_d4` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 7; the bespoke epistemic token carries its own rider (modulo_convention) -- quoted verbatim, not shortened to [P]. |
| `foundation:operational_completeness_sandwich` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 7; flag: the _module_manifest.py:438 comment (v24.3.230 stamp) still reads '[P_structural] x2' for the first two checks, but the in-... |
| `foundation:paper1_fd1_executable_witness` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 7; the Paper 1 analog of formal_kernel's Theorem 1.1 witness |
| `foundation:regime_r_exit_taxonomy` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 4 probe |
| `foundation:representation_descent_stack` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 7; grades are the bespoke P_descent/P_obstruction/P_schema/P_audit/P_cat_finite_descent tokens read from status= fields. |
| `foundation:single_dimensional_anchor` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 4 probe; the name-vs-grade trap defused explicitly |
| `foundation:sixteen_case_unification` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 5 probe; grade read from the epistemic field, not prose |
| `foundation:spectral_action_internalization` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 7; fields match docstring. |
| `foundation:subspace_functors_i1_i3_i4` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 7; fields match docstring intent (module exists precisely to earn the [P] the three-level module had parked). |
| `foundation:tail_center_trivial_f1` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 7; native F1 half only, factoriality export explicitly disclaimed by in-module flags |

## Paper 5 (quantum structure) + the FeasBool lane

| input | axis | verdict | note |
|---|---|---|---|
| `contextuality:chsh_local` | CONTEXTUALITY | **EXPORT** | local interior point (all CHSH sign choices /S/=6/5<=2) -> SepStr export |
| `contextuality:consistent_cycle` | CONTEXTUALITY | **EXPORT** | even 4-cycle (consistent GF(2) system) -> SepStr export |
| `contextuality:magic_square_parity` | CONTEXTUALITY | IJC_OBSTRUCTION | Mermin-Peres magic square (GF(2) 0=1) -> IJCStr named obstruction |
| `contextuality:pr_box` | CONTEXTUALITY | IJC_OBSTRUCTION | PR box (S=4) -> IJCStr named obstruction (CHSH/Fine separator) |
| `quantum:ghz_mermin_state_independent` | CONTEXTUALITY | IJC_OBSTRUCTION | the GHZ/Mermin state-independent scenario (empty global-section support, brute-forced 0/64 -- six observables, 2^6 global sections -- in ... |
| `quantum:i3_operator_self_identification` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 7; P_comp on the top check quoted as-is (composed status, distinct from plain P). |
| `quantum:magic_square_threshold_robust` | CONTEXTUALITY | IJC_OBSTRUCTION | sign-equivalent textbook encoding of the v24.3.297 scenario (the banked check uses column parities (1,1,1); flipping two row signs gives ... |
| `quantum:qutrit_noncontextual_control` | CONTEXTUALITY | **EXPORT** | the qutrit noncontextual control scenario -> SepStr export (a faithful global hidden-variable section exists) |
| `quantum:symmetry_contextuality_orthogonal` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 4 probe; the four-cell witness content stays with the banked check |
| `spine:inseparable_ijc_345_witness` | CONTEXTUALITY | IJC_OBSTRUCTION | the v24.3.288 exact singlet realization of the 3-4-5 geometry (constructive companion to T_inseparable_IJC's inline +-12/25 codespace wit... |

## Paper 18 + Paper 42 + Paper 28 (EW sector)

| input | axis | verdict | note |
|---|---|---|---|
| `claim:ew_global_export` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR |  |
| `claim:ew_local_trace` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR |  |
| `ew:a_mu_hvp_capacity_density` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 7; docstring [P_structural] vs machine epistemic=P_structural_seam flagged, field wins |
| `ew:absolute_scale_frontier_terminated` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 5 Group A head: the no-go triptych terminus (v24.3.314); covers = the prefactor chain (invariance_no_go + hierarchy_mechanism enter ... |
| `ew:delta_alpha_adler_pqcd_m_z` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 7; bespoke grade token quoted verbatim from the machine field |
| `ew:delta_alpha_capacity_density` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 7; docstring [P_structural] vs machine epistemic=P_structural_seam on both checks flagged, field wins |
| `ew:delta_alpha_leptonic` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 7; mixed-grade module, per-check grades listed from machine fields |
| `ew:delta_alpha_pqcd_m_z` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 7; bespoke grade token quoted verbatim from the machine field |
| `ew:delta_rho_leading_distinction` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 7; grade rider (modulo scale and convention) carried in the bespoke token |
| `ew:mw_distinction_decomposition` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 4 head 4: the distinction-picture M_W head; no in-family covers |
| `ew:mw_from_3_13_effective_angle` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 8; classified physics_claim in the plumbing pass (the only one in the 86-module pool); absolute-scale discipline: M_Z anchor named, ... |
| `ew:native_oblique_close` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 4 head 5: the oblique family head; covers = the cross-composed native oblique modules |
| `ew:orientation_ew_route_priced` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 6 depth; the B3 close (.327) |
| `ew:osw_source_transcription_families` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 7; architecture-only instrument layer; W-export language aligned to the v15.1 adjudication |
| `ew:photon_massless_reversibility` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 4 probe; grade stated at the banked [P_structural_reading] |
| `ew:pi_gammagamma_2l_moment_native` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 7; scope fence (reproduction, not A1-derivation) is part of the banked grade token |
| `ew:planck_anchor_bekenstein_forced` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 5 Group A sibling probe; covers = its genuine floor-measure dependency |
| `ew:pre_branch_joint_necessity` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 5 Group B head; covers = the four named dependencies of the head check |
| `ew:sigma_scale_formula_held` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 7 v_H capacity-formula held-gate; bespoke P_structural_* token, reproduced-but-held disposition |
| `ew:sigma_scale_yukawa_free_floor` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 7 Yukawa-free geometric component of v_H; bespoke P_structural_* token with Planck-convention rider |
| `ew:sin2theta_eff_kappa_l_decomposition` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 7; mixed-grade module, per-check grades listed from machine fields |
| `ew:sin2theta_w_os_capacity_counting_gh_codomain` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 7; docstring headline P_full_structural vs value-check machine fields P_attractor_structural_GH_OS_codomain flagged, fields quoted |
| `ew:sqrtNc_carrier_forced` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 5 Group B leaf probe |
| `ew:u1y_landau_pole_trans_planckian` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 6 |
| `ew_eigenscreen:coupled_channel_disposition` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | provenance: APF_INTERFACE_ENGINE_EW_COUPLED_CHANNEL_EIGENSCREEN_SYMBOLIC_GATE_v1 + EW_PARTIAL_WAVE_ANALYTIC_SCREEN_v1 (held, not banked);... |
| `ew_eigenscreen:goldstone_boundary_disposition` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | provenance: APF_INTERFACE_ENGINE_GOLDSTONE_EQUIVALENCE_BOUNDARY_v1 + EW_SCATTERING_UNITARITY_SYMBOLIC_GATE_v1 + EW_TREE_AMPLITUDE_CUSTODI... |
| `payload:ew_dizet_real_adapter_live` | ROUTE | **EXPORT** | live adapter payload (swap of mass:route11_mw_on_shell_dizet); imported/banked content and grades per its adapter module |
| `payload:ew_transport_open` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR |  |
| `wtrace:bsy_one_loop_kappa_l_assembly_consistency` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 7; bespoke grade token quoted verbatim; opens stated as banked |
| `wtrace:native_one_loop_mw_close` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 4 head 1: the one-loop native close; covers = the dependency-verified composition fan; Wave 7 covers extension: +11 stages, criterio... |
| `wtrace:os_route_terminal_closure_open_export` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 4 head 2: the export-status head -- the honest OPEN statement; covers = the import-verified closure surface; Wave 7 covers extension... |
| `wtrace:two_loop_phase2_router` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 4 head 3: the two-loop program head; covers = its promoted-lane composition only |
| `wtrace:zll_kappa_l_oblique` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 7; mixed-grade module, per-check grades listed from machine fields |
| `wtrace:zll_r2_counterterm_pieces` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 7; plumbing-with-a-theorem: banked content = finiteness + the delta_Z2_gamma = -Pi_AA(0) identity + delta_Z_AZ self-consistency + st... |

## Papers 29/30/31 (YM trilogy) + the gauge sector

| input | axis | verdict | note |
|---|---|---|---|
| `claim:gauge_fiber` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR |  |
| `gauge:abelian_rank1_capacity_count` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 6 item (a); the check name's _P suffix is historical -- the operative grade is the declared [P_structural_reading] |
| `gauge:acc_reading_selection_map` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 6 |
| `gauge:beta_capacity_tiling` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 7 abelian beta-tiling + leading-log identity; field P_structural_seam vs docstring [P_structural] flagged |
| `gauge:photon_slot4_c4_keystone` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 7; docstring [P_structural] vs machine epistemic=P_structural_reading flagged, field wins |
| `gauge:quotient_pinned_demand` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 4 probe |
| `gauge:spine_disposition` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 3 spine probe; dispositions per the banked checks (Theorem_R, L_count, T_ew_load_placement_P, T_abelian_coupling_fixed_by_rank1_capa... |
| `readout:su2_diquark` | READOUT | **EXPORT** | m=1 -> canonical record EXPORTED |
| `readout:su2_fund4` | READOUT | READOUT_OBSTRUCTION | m=2 -> named obstruction: multiplicity-frame required |
| `readout:su3_baryon` | READOUT | **EXPORT** | m=1 -> canonical record EXPORTED (the epsilon baryon) |
| `readout:su3_meson` | READOUT | **EXPORT** | m=1 -> canonical frame-free record EXPORTED (the entangled singlet) |
| `readout:su3_quark_pair` | READOUT | READOUT_OBSTRUCTION | m=0 -> named obstruction: no sharp gauge-invariant record |
| `readout:su3_single_quark` | READOUT | READOUT_OBSTRUCTION | m=0 -> named obstruction: no sharp gauge-invariant record |
| `readout:su3_tetraquark` | READOUT | READOUT_OBSTRUCTION | m=2 -> named obstruction: multiplicity-frame required |
| `strong:confinement_single_anchor` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 7 single-anchor collapse for the strong sector; field P_structural_seam vs docstring [P_structural] flagged |
| `strong:ladder_classical_correlation_control` | CONTEXTUALITY | **EXPORT** | v24.3.298 corrected ladder, rung 1: perfectly-correlated classical table has a global Boolean section -> SepStr (subadditive control) |
| `strong:lattice_gap_candidate` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 4 probe; the candidate framing is the banked framing |
| `strong:pentaquark_magic_square` | CONTEXTUALITY | IJC_OBSTRUCTION | v24.3.295 banked scenario: SU(2) pentaquark M4 hosts the Mermin-Peres magic square (empty global-section support) -> IJCStr; the physical... |
| `strong:pi0_anomaly_width_row` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 6; scorecard row 49 (49 total / 40 tested / 33 consistent at the .341 landing) |
| `strong:tetraquark_kcbs` | CONTEXTUALITY | IJC_OBSTRUCTION | v24.3.293 banked scenario: gauge-invariant tetraquark M3 KCBS -> IJCStr |
| `strong:tetraquark_yuoh_state_independent` | CONTEXTUALITY | IJC_OBSTRUCTION | v24.3.294 banked scenario: Yu-Oh 13-ray on the tetraquark M3, state-independent -> IJCStr |
| `strong:vacuum_realization_triptych` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 6: the 2026-07-02 vacuum-realization arc (.335/.337/.341-.343); no [P] claimed anywhere in this row |
| `strong:ym_kappa3_negative` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 7 Paper 30 kappa_3 negativity witness; [P_structural] field, full interval certificate lives off-bank |
| `strong:ym_quotient_ledger` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 7 YM quotient ledger; 6x P_structural_instrument + 2x P machine fields, no spectral/value claim |

## Paper 35 (dark sector)

| input | axis | verdict | note |
|---|---|---|---|
| `claim:dark_runtime` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR |  |
| `dark:cmb_finite_mode_covariance_prototype` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 7; scipy-blocked module read statically; docstring [P_structural] vs field P_structural_reading flagged on all six checks |
| `dark:lambda_absolute_mixed_grades` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 5 probe; mixed grades enumerated, no blanket bracket |
| `dark:phase_space_persistence_kernel` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Phase 2 disposition item (b); pack PHASE_SPACE_CLUSTERING_KERNEL.md wording |
| `dark:route_cross_sn_profile_probe` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR |  |
| `dark:route_desi_full_shape_exact` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR |  |
| `dark:route_full_growth_likelihood` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR |  |
| `dark:saturation_no_go_guard` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Phase 2 disposition item (a); pack SATURATION_NO_GO_GUARD.md wording |
| `payload:dark_modified_gravity_obstruction_real_adapter_live` | ROUTE | OBSTRUCTION_NAMED_CLOSURE | live adapter payload (swap of dark:route_modified_gravity); imported/banked content and grades per its adapter module |
| `payload:dark_particle_id_obstruction_real_adapter_live` | ROUTE | OBSTRUCTION_NAMED_CLOSURE | live adapter payload (swap of dark:route_dark_particle_id); imported/banked content and grades per its adapter module |
| `payload:dark_runtime_open` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR |  |
| `payload:dark_w2_a_background_real_adapter_live` | ROUTE | **EXPORT** | live adapter payload (swap of dark:route_w2_a_background); imported/banked content and grades per its adapter module |

## Paper 41 + Paper 8 (horizon / ledger)

| input | axis | verdict | note |
|---|---|---|---|
| `claim:horizon_cost` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR |  |
| `gravity:bekenstein_quarter_structural` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 4 probe; the one-logarithm displacement stated per the corrigendum |
| `gravity:evaporation_microtransport_gates` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 7; data-field 'P / regime' prose vs status='P_conditional' token flagged (token wins) |
| `gravity:evaporation_quartet_page_derived` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 5 probe; grade lives in the status field in this module |
| `gravity:fre_and_lambda_absolute` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 7; fork-conformed surfaces (v24.3.320) respected, row is branch-neutral; the L_Lambda [P] is gate-passage-only by its own corrected ... |
| `gravity:i1_bridge_at_joint_k42` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 7; single-check module, bridge grade is joint-point-only per its own artifacts |
| `gravity:lambda_operator_level_derivation` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 7; composed check field 'P' is over-[C]-ansatz per its own docstring (flagged); row is fork-branch-neutral |
| `gravity:observable_transport_gr_nonclaims` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Phase 2 disposition gravity residue; pack transport-ledger rows consolidated |
| `gravity:phase_14d3_completions` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 7; 42/102-uniqueness demotion (v24.3.320) and stale-broken scan flag surfaced; row is fork-branch-neutral |
| `gravity:singlet_gram_exchangeable_form` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 6 depth; the B4 close (.330); the a=b identity is a named open kernel |
| `gravity:vacuum_o1_h0_fork` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 6; the fork is deliberately preserved (principal's charter: preserve the tension), not a defect |
| `payload:cosmogenesis_t1_t4_quartet_real_adapter_live` | ROUTE | **EXPORT** | live adapter payload (swap of cosmogenesis:route_t1_t4_quartet); imported/banked content and grades per its adapter module |
| `payload:evaporation_e1_e4_quartet_real_adapter_live` | ROUTE | **EXPORT** | live adapter payload (swap of evaporation:route_e1_e4_quartet); imported/banked content and grades per its adapter module |
| `payload:gravity_bianchi_rigidity_real_adapter_live` | ROUTE | **EXPORT** | live adapter payload (swap of gravity:route_bianchi_rigidity); imported/banked content and grades per its adapter module |
| `payload:gravity_gr_limit_full_close_real_adapter_live` | ROUTE | **EXPORT** | live adapter payload (swap of gravity:route_gr_limit_full_close); imported/banked content and grades per its adapter module |
| `payload:gravity_ringdown_capacity_schema_real_adapter_live` | ROUTE | **EXPORT** | live adapter payload (swap of gravity:route_ringdown_capacity_schema); imported/banked content and grades per its adapter module |

## Paper 33 (trace-to-scheme) + the mass sector

| input | axis | verdict | note |
|---|---|---|---|
| `flavour:bottom_msbar_export_candidate` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 7 bottom export-candidate closure; grade in module status tokens (export candidate, not physical-final) |
| `flavour:bottom_msbar_transport_route` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 7 bottom trace-to-scheme validation lane; grade lives in module status tokens, no per-check epistemic field |
| `flavour:charged_fermion_trace_spectrum` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 7 charged trace spectrum aggregator; P_local grade with named yellow rung (upstream-banking of the up bridge) |
| `flavour:chiral_condensate_yuoh` | CONTEXTUALITY | IJC_OBSTRUCTION | v24.3.296 banked scenario: Yu-Oh on the N_f=3 flavour qutrit at the chiral condensate single density -> IJCStr |
| `flavour:ckm_two_mass_bases` | CONTEXTUALITY | **EXPORT** | v24.3.303 banked scenario: the CKM-forced up/down mass bases as two disjoint triads -> SepStr export (forced flavour dynamics buy noncomm... |
| `flavour:down_lepton_trace_vector` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 7 down/lepton trace vector; all grades P_local machine fields |
| `flavour:neutrino_mbb_transport` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 7 mbb transport certificate; [P] machine field with the Delta m^2_31 anchor named as the sole external input |
| `flavour:quark_trace_anchors` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 7 top/bottom trace anchors; P_local machine fields, top anchor is an inherited constant |
| `flavour:seesaw_from_a1` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 5 probe; the uniform-[P] letter is the banked state, cited as such |
| `flavour:three_generations_forced` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 4 probe; survey-verified against the module's banked checks |
| `flavour:trace_sector_closure` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 7 trace-sector master closure; P_local/P_local_boundary, physical transport explicitly open here |
| `flavour:up_family_trace_bridge` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 7 up-family Gram-to-Trace bridge; P_local with named upstream-banking promotion condition |
| `flavour:up_normalizer_local` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 7; local theorem + guard pair; conditional gates named as banked |
| `flavour:yt_normalization_no_go` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 7 absolute-top-Yukawa normalization no-go; bespoke P_structural_* token, obstruction result |
| `neutrino:route_dune_juno_hierarchy` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR |  |
| `payload:bottom_msbar_rundec_real_adapter_live` | ROUTE | **EXPORT** | live adapter payload (swap of mass:route05_bottom_msbar_self_scale); imported/banked content and grades per its adapter module |
| `payload:bottom_pole_obstruction_real_adapter_live` | ROUTE | OBSTRUCTION_NAMED_CLOSURE | live adapter payload (swap of mass:route06_bottom_pole); imported/banked content and grades per its adapter module |
| `payload:charged_lepton_pole_real_adapter_live` | ROUTE | **EXPORT** | live adapter payload (swap of mass:route01_charged_lepton_pole); imported/banked content and grades per its adapter module |
| `payload:charged_lepton_qed_real_adapter_live` | ROUTE | **EXPORT** | live adapter payload (swap of mass:route02_charged_lepton_qed_running); imported/banked content and grades per its adapter module |
| `payload:charm_msbar_rundec_real_adapter_live` | ROUTE | **EXPORT** | live adapter payload (swap of mass:route03_charm_msbar_self_scale); imported/banked content and grades per its adapter module |
| `payload:charm_pole_obstruction_real_adapter_live` | ROUTE | OBSTRUCTION_NAMED_CLOSURE | live adapter payload (swap of mass:route04_charm_pole); imported/banked content and grades per its adapter module |
| `payload:light_quark_real_adapter_live` | ROUTE | **EXPORT** | live adapter payload (swap of mass:route10_light_quark_flag_external_kernel); imported/banked content and grades per its adapter module |
| `payload:top_msr_R_star_real_adapter_live` | ROUTE | **EXPORT** | live adapter payload (swap of mass:route07_top_external_msr); imported/banked content and grades per its adapter module |
| `payload:top_msr_r_evolution_real_adapter_live` | ROUTE | **EXPORT** | live adapter payload (swap of mass:route08_top_msr_ew_transport); imported/banked content and grades per its adapter module |
| `payload:top_pole_mc_obstruction_real_adapter_live` | ROUTE | OBSTRUCTION_NAMED_CLOSURE | live adapter payload (swap of mass:route09_top_pole_mc); imported/banked content and grades per its adapter module |

## Paper 21 / the Engine (everything; the atlas itself is its artifact)

| input | axis | verdict | note |
|---|---|---|---|
| `claim:capacity_overspend` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR |  |
| `claim:cstar_substrate` | ROUTE | BLOCKED_SUBSTRATE_REVISION_REQUIRED |  |
| `claim:drawn_content_readings_functional` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | the .306 open object closed at v0.2 strength (banked v24.3.328/.329); scenario payloads live with their home modules -- this claim onboar... |
| `claim:generic` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR |  |
| `claim:magic_square_4n_rigidity` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | upgrades the ladder's parity column from constructive to characterized: a parity off-cell is an invariant absence |
| `claim:provenance_smuggling` | ROUTE | FAIL_CLOSED_PROVENANCE |  |
| `coherent_phase:bec` | CODOMAIN | **EXPORT** | live adapter payload (swap of (none; new codomain-axis input)); imported/banked content and grades per its adapter module |
| `coherent_phase:laser_coherence` | CODOMAIN | **EXPORT** | live adapter payload (swap of (none; new codomain-axis input)); imported/banked content and grades per its adapter module |
| `coherent_phase:magnetism` | CODOMAIN | **EXPORT** | live adapter payload (swap of (none; new codomain-axis input)); imported/banked content and grades per its adapter module |
| `coherent_phase:superconductivity` | CODOMAIN | **EXPORT** | live adapter payload (swap of (none; new codomain-axis input)); imported/banked content and grades per its adapter module |
| `coherent_phase:superfluidity` | CODOMAIN | **EXPORT** | live adapter payload (swap of (none; new codomain-axis input)); imported/banked content and grades per its adapter module |
| `coherent_phase:synchronization` | CODOMAIN | **EXPORT** | live adapter payload (swap of (none; new codomain-axis input)); imported/banked content and grades per its adapter module |
| `coherent_phase:topological_order` | CODOMAIN | **EXPORT** | live adapter payload (swap of (none; new codomain-axis input)); imported/banked content and grades per its adapter module |
| `instrument:crystal_attribution` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 5 probe; instrument grade per the corpus grade-split |
| `instrument:enforcement_crystal_walker` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 7; instrument coherence certificate only |
| `payload:arch_defect_calculus_internal_identity_real_adapter_live` | ROUTE | **EXPORT** | live adapter payload (swap of arch:route_defect_calculus_architecture); imported/banked content and grades per its adapter module |
| `payload:arch_interface_engine_operational_internal_identity_real_adapter_live` | ROUTE | **EXPORT** | live adapter payload (swap of arch:route_interface_engine_operational); imported/banked content and grades per its adapter module |
| `payload:arch_rdfi_kernel_internal_identity_real_adapter_live` | ROUTE | **EXPORT** | live adapter payload (swap of arch:route_rdfi_global_descent_kernel); imported/banked content and grades per its adapter module |
| `payload:capacity_overspend` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR |  |
| `payload:neutrino_mbb_reconciliation_real_adapter_live` | ROUTE | **EXPORT** | live adapter payload (swap of neutrino:route_mbb_reconciliation); imported/banked content and grades per its adapter module |
| `payload:sin2theta_eff_bsy_real_adapter_live` | ROUTE | **EXPORT** | live adapter payload (swap of mass:route13_sin2_theta_eff_bsy_four_channel); imported/banked content and grades per its adapter module |
| `payload:sin2theta_w_mass_ratio_identity_real_adapter_live` | ROUTE | **EXPORT** | live adapter payload (swap of mass:route14_sin2_theta_w_mass_ratio_identity); imported/banked content and grades per its adapter module |
| `payload:sin2theta_w_source_identity_real_adapter_live` | ROUTE | **EXPORT** | live adapter payload (swap of mass:route12_sin2_theta_w_source_identity); imported/banked content and grades per its adapter module |
| `thermo:cost_energy_identity` | ROUTE | BLOCKED_SUBSTRATE_REVISION_REQUIRED | Wave 7; single [P] derivation check. Verdict-class adjudication (post-audit 2026-07-02): the claim compiler prices the named external-Ham... |
| `thermo:fluctuation_response_equilibrium` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 7; equilibrium-only, dynamical FDT explicitly not claimed |
| `thermo:four_laws_composed` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 4 probe |
| `thermo:i4_operator_self_identification` | ROUTE | BLOCKED_SUBSTRATE_REVISION_REQUIRED | Wave 7; P_comp composition token, regime-local self-identification distinguished from bridge closure |
| `thermo:negative_temperature_ceiling` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 7; single [P] check with explicit microcanonical-dispute fence |
| `thermo:thermal_absolute_scope` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 7; 2 [P] numerical/scope checks over a 3-check [C] interpretive layer |

---
*The paper cross-index is a curated coverage map, not a completeness claim. Concept DOIs for all deposited papers: see the repo README / the Zenodo community `admissibility_physics`.*
