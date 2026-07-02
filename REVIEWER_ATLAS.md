# APF Reviewer Atlas -- what the framework claims, machine-checked

Generated 2026-07-02 against verdict pin v24.3.323. Every row below is produced by running the banked engine, not written by hand; the committed copy is certified current against the verdict pin by `check_T_ie_reviewer_manifest_current` (a failing bank run means this file is stale).

**How to reproduce**: clone the repo, `python3 verify_all.py --bank-audit` (the full theorem bank, 3805 checks), then `PYTHONPATH=. python3 scripts/gen_reviewer_manifest.py`.

**Reading a verdict**: `EXPORT` = the route exports a global section in the engine's own currency. `held/obstructed` = the route holds with a NAMED obstruction or an honest open disposition -- in this framework obstructions are results (e.g. a Bell/noncontextuality certificate, a no-go, an honest OPEN statement), not defects. Verdicts inherit the grades of the banked theorems they route through; routing confers nothing.

**Coverage**: 113 of 446 loaded modules onboarded (71 directly), 73 of 245 on the physics target surface. Modules not onboarded are honestly so (pipeline stages of banked programs, or abstract interfaces with no payload data).

## Paper 0 + Paper 13 (foundations)

| input | axis | verdict | note |
|---|---|---|---|
| `foundation:acc_ledger_identities` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 4 probe |
| `foundation:base_fiber_allocation` | ROUTE | BLOCKED_SUBSTRATE_REVISION_REQUIRED | Wave 4 probe; the no-B row's OPEN status stated honestly |
| `foundation:d4_unique` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 5 probe; all-[P] verified per epistemic fields |
| `foundation:four_input_declaration` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 4 probe; grades letter-checked (the clause is adopted; see the 2026-06-25 canonical-definition note) |
| `foundation:regime_r_exit_taxonomy` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 4 probe |
| `foundation:single_dimensional_anchor` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 4 probe; the name-vs-grade trap defused explicitly |
| `foundation:sixteen_case_unification` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 5 probe; grade read from the epistemic field, not prose |

## Paper 5 (quantum structure) + the FeasBool lane

| input | axis | verdict | note |
|---|---|---|---|
| `contextuality:chsh_local` | CONTEXTUALITY | **EXPORT** | local interior point (all CHSH sign choices /S/=6/5<=2) -> SepStr export |
| `contextuality:consistent_cycle` | CONTEXTUALITY | **EXPORT** | even 4-cycle (consistent GF(2) system) -> SepStr export |
| `contextuality:magic_square_parity` | CONTEXTUALITY | IJC_OBSTRUCTION | Mermin-Peres magic square (GF(2) 0=1) -> IJCStr named obstruction |
| `contextuality:pr_box` | CONTEXTUALITY | IJC_OBSTRUCTION | PR box (S=4) -> IJCStr named obstruction (CHSH/Fine separator) |
| `quantum:ghz_mermin_state_independent` | CONTEXTUALITY | IJC_OBSTRUCTION | the GHZ/Mermin state-independent scenario (empty global-section support, brute-forced 0/64 -- six observables, 2^6 global sections -- in ... |
| `quantum:magic_square_threshold_robust` | CONTEXTUALITY | IJC_OBSTRUCTION | sign-equivalent textbook encoding of the v24.3.297 scenario (the banked check uses column parities (1,1,1); flipping two row signs gives ... |
| `quantum:qutrit_noncontextual_control` | CONTEXTUALITY | **EXPORT** | the qutrit noncontextual control scenario -> SepStr export (a faithful global hidden-variable section exists) |
| `quantum:symmetry_contextuality_orthogonal` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 4 probe; the four-cell witness content stays with the banked check |
| `spine:inseparable_ijc_345_witness` | CONTEXTUALITY | IJC_OBSTRUCTION | the v24.3.288 exact singlet realization of the 3-4-5 geometry (constructive companion to T_inseparable_IJC's inline +-12/25 codespace wit... |

## Paper 18 + Paper 42 + Paper 28 (EW sector)

| input | axis | verdict | note |
|---|---|---|---|
| `claim:ew_global_export` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR |  |
| `claim:ew_local_trace` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR |  |
| `ew:absolute_scale_frontier_terminated` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 5 Group A head: the no-go triptych terminus (v24.3.314); covers = the prefactor chain (invariance_no_go + hierarchy_mechanism enter ... |
| `ew:mw_distinction_decomposition` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 4 head 4: the distinction-picture M_W head; no in-family covers |
| `ew:native_oblique_close` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 4 head 5: the oblique family head; covers = the cross-composed native oblique modules |
| `ew:photon_massless_reversibility` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 4 probe; grade stated at the banked [P_structural_reading] |
| `ew:planck_anchor_bekenstein_forced` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 5 Group A sibling probe; covers = its genuine floor-measure dependency |
| `ew:pre_branch_joint_necessity` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 5 Group B head; covers = the four named dependencies of the head check |
| `ew:sqrtNc_carrier_forced` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 5 Group B leaf probe |
| `ew_eigenscreen:coupled_channel_disposition` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | provenance: APF_INTERFACE_ENGINE_EW_COUPLED_CHANNEL_EIGENSCREEN_SYMBOLIC_GATE_v1 + EW_PARTIAL_WAVE_ANALYTIC_SCREEN_v1 (held, not banked);... |
| `ew_eigenscreen:goldstone_boundary_disposition` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | provenance: APF_INTERFACE_ENGINE_GOLDSTONE_EQUIVALENCE_BOUNDARY_v1 + EW_SCATTERING_UNITARITY_SYMBOLIC_GATE_v1 + EW_TREE_AMPLITUDE_CUSTODI... |
| `payload:ew_dizet_real_adapter_live` | ROUTE | **EXPORT** | live adapter payload (swap of mass:route11_mw_on_shell_dizet); imported/banked content and grades per its adapter module |
| `payload:ew_transport_open` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR |  |
| `wtrace:native_one_loop_mw_close` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 4 head 1: the one-loop native close; covers = the dependency-verified composition fan |
| `wtrace:os_route_terminal_closure_open_export` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 4 head 2: the export-status head -- the honest OPEN statement; covers = the import-verified closure surface |
| `wtrace:two_loop_phase2_router` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 4 head 3: the two-loop program head; covers = its promoted-lane composition only |

## Papers 29/30/31 (YM trilogy) + the gauge sector

| input | axis | verdict | note |
|---|---|---|---|
| `claim:gauge_fiber` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR |  |
| `gauge:quotient_pinned_demand` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 4 probe |
| `gauge:spine_disposition` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 3 spine probe; dispositions per the banked checks (Theorem_R, L_count, T_ew_load_placement_P, T_abelian_coupling_fixed_by_rank1_capa... |
| `readout:su2_diquark` | READOUT | **EXPORT** | m=1 -> canonical record EXPORTED |
| `readout:su2_fund4` | READOUT | READOUT_OBSTRUCTION | m=2 -> named obstruction: multiplicity-frame required |
| `readout:su3_baryon` | READOUT | **EXPORT** | m=1 -> canonical record EXPORTED (the epsilon baryon) |
| `readout:su3_meson` | READOUT | **EXPORT** | m=1 -> canonical frame-free record EXPORTED (the entangled singlet) |
| `readout:su3_quark_pair` | READOUT | READOUT_OBSTRUCTION | m=0 -> named obstruction: no sharp gauge-invariant record |
| `readout:su3_single_quark` | READOUT | READOUT_OBSTRUCTION | m=0 -> named obstruction: no sharp gauge-invariant record |
| `readout:su3_tetraquark` | READOUT | READOUT_OBSTRUCTION | m=2 -> named obstruction: multiplicity-frame required |
| `strong:ladder_classical_correlation_control` | CONTEXTUALITY | **EXPORT** | v24.3.298 corrected ladder, rung 1: perfectly-correlated classical table has a global Boolean section -> SepStr (subadditive control) |
| `strong:lattice_gap_candidate` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 4 probe; the candidate framing is the banked framing |
| `strong:pentaquark_magic_square` | CONTEXTUALITY | IJC_OBSTRUCTION | v24.3.295 banked scenario: SU(2) pentaquark M4 hosts the Mermin-Peres magic square (empty global-section support) -> IJCStr; the physical... |
| `strong:tetraquark_kcbs` | CONTEXTUALITY | IJC_OBSTRUCTION | v24.3.293 banked scenario: gauge-invariant tetraquark M3 KCBS -> IJCStr |
| `strong:tetraquark_yuoh_state_independent` | CONTEXTUALITY | IJC_OBSTRUCTION | v24.3.294 banked scenario: Yu-Oh 13-ray on the tetraquark M3, state-independent -> IJCStr |

## Paper 35 (dark sector)

| input | axis | verdict | note |
|---|---|---|---|
| `claim:dark_runtime` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR |  |
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
| `gravity:evaporation_quartet_page_derived` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 5 probe; grade lives in the status field in this module |
| `gravity:observable_transport_gr_nonclaims` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Phase 2 disposition gravity residue; pack transport-ledger rows consolidated |
| `payload:cosmogenesis_t1_t4_quartet_real_adapter_live` | ROUTE | **EXPORT** | live adapter payload (swap of cosmogenesis:route_t1_t4_quartet); imported/banked content and grades per its adapter module |
| `payload:evaporation_e1_e4_quartet_real_adapter_live` | ROUTE | **EXPORT** | live adapter payload (swap of evaporation:route_e1_e4_quartet); imported/banked content and grades per its adapter module |
| `payload:gravity_bianchi_rigidity_real_adapter_live` | ROUTE | **EXPORT** | live adapter payload (swap of gravity:route_bianchi_rigidity); imported/banked content and grades per its adapter module |
| `payload:gravity_gr_limit_full_close_real_adapter_live` | ROUTE | **EXPORT** | live adapter payload (swap of gravity:route_gr_limit_full_close); imported/banked content and grades per its adapter module |
| `payload:gravity_ringdown_capacity_schema_real_adapter_live` | ROUTE | **EXPORT** | live adapter payload (swap of gravity:route_ringdown_capacity_schema); imported/banked content and grades per its adapter module |

## Paper 33 (trace-to-scheme) + the mass sector

| input | axis | verdict | note |
|---|---|---|---|
| `flavour:chiral_condensate_yuoh` | CONTEXTUALITY | IJC_OBSTRUCTION | v24.3.296 banked scenario: Yu-Oh on the N_f=3 flavour qutrit at the chiral condensate single density -> IJCStr |
| `flavour:ckm_two_mass_bases` | CONTEXTUALITY | **EXPORT** | v24.3.303 banked scenario: the CKM-forced up/down mass bases as two disjoint triads -> SepStr export (forced flavour dynamics buy noncomm... |
| `flavour:seesaw_from_a1` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 5 probe; the uniform-[P] letter is the banked state, cited as such |
| `flavour:three_generations_forced` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 4 probe; survey-verified against the module's banked checks |
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
| `claim:generic` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR |  |
| `claim:provenance_smuggling` | ROUTE | FAIL_CLOSED_PROVENANCE |  |
| `coherent_phase:bec` | CODOMAIN | **EXPORT** | live adapter payload (swap of (none; new codomain-axis input)); imported/banked content and grades per its adapter module |
| `coherent_phase:laser_coherence` | CODOMAIN | **EXPORT** | live adapter payload (swap of (none; new codomain-axis input)); imported/banked content and grades per its adapter module |
| `coherent_phase:magnetism` | CODOMAIN | **EXPORT** | live adapter payload (swap of (none; new codomain-axis input)); imported/banked content and grades per its adapter module |
| `coherent_phase:superconductivity` | CODOMAIN | **EXPORT** | live adapter payload (swap of (none; new codomain-axis input)); imported/banked content and grades per its adapter module |
| `coherent_phase:superfluidity` | CODOMAIN | **EXPORT** | live adapter payload (swap of (none; new codomain-axis input)); imported/banked content and grades per its adapter module |
| `coherent_phase:synchronization` | CODOMAIN | **EXPORT** | live adapter payload (swap of (none; new codomain-axis input)); imported/banked content and grades per its adapter module |
| `coherent_phase:topological_order` | CODOMAIN | **EXPORT** | live adapter payload (swap of (none; new codomain-axis input)); imported/banked content and grades per its adapter module |
| `instrument:crystal_attribution` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 5 probe; instrument grade per the corpus grade-split |
| `payload:arch_defect_calculus_internal_identity_real_adapter_live` | ROUTE | **EXPORT** | live adapter payload (swap of arch:route_defect_calculus_architecture); imported/banked content and grades per its adapter module |
| `payload:arch_interface_engine_operational_internal_identity_real_adapter_live` | ROUTE | **EXPORT** | live adapter payload (swap of arch:route_interface_engine_operational); imported/banked content and grades per its adapter module |
| `payload:arch_rdfi_kernel_internal_identity_real_adapter_live` | ROUTE | **EXPORT** | live adapter payload (swap of arch:route_rdfi_global_descent_kernel); imported/banked content and grades per its adapter module |
| `payload:capacity_overspend` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR |  |
| `payload:neutrino_mbb_reconciliation_real_adapter_live` | ROUTE | **EXPORT** | live adapter payload (swap of neutrino:route_mbb_reconciliation); imported/banked content and grades per its adapter module |
| `payload:sin2theta_eff_bsy_real_adapter_live` | ROUTE | **EXPORT** | live adapter payload (swap of mass:route13_sin2_theta_eff_bsy_four_channel); imported/banked content and grades per its adapter module |
| `payload:sin2theta_w_mass_ratio_identity_real_adapter_live` | ROUTE | **EXPORT** | live adapter payload (swap of mass:route14_sin2_theta_w_mass_ratio_identity); imported/banked content and grades per its adapter module |
| `payload:sin2theta_w_source_identity_real_adapter_live` | ROUTE | **EXPORT** | live adapter payload (swap of mass:route12_sin2_theta_w_source_identity); imported/banked content and grades per its adapter module |
| `thermo:four_laws_composed` | ROUTE | SOLVED_LOCAL_HELD_FOR_REPAIR | Wave 4 probe |

---
*The paper cross-index is a curated coverage map, not a completeness claim. Concept DOIs for all deposited papers: see the repo README / the Zenodo community `admissibility_physics`.*
