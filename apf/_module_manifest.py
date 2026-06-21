"""APF module manifest — single source of truth for module lists.

Created 2026-05-18 as part of the MODULES unification refactor (v24.3.18 -> v24.3.19).

Replaces the previously-duplicate lists in ``apf/bank.py``'s ``_MODULE_PATHS``
(154 entries) and ``verify_all.py``'s ``MODULES`` (223 entries). The two lists
had drifted significantly; this manifest is the single source of truth both
files now import from.

Four categories
---------------

``BANK_REGISTRY_MODULES`` (233 modules)
    Modules with a ``register(registry)`` function that contributes checks to
    ``apf.bank.REGISTRY``. Loaded by ``bank._load()`` and enumerated by
    ``verify_all.MODULES``.

``ARCHITECTURE_ONLY_MODULES`` (29 modules)
    Architecture/engineering-only modules whose ``register()`` returns 0 checks
    BY DESIGN. Loaded by ``bank._load()`` for completeness; ``--bank-audit``
    Bucket B filters these so the warning surfaces only genuine misregistrations.
    Includes 12 v24.3.18 defect-calculus modules + 5 ISEE engineering modules
    + ``apf.ew_sector_closure``.

``STANDALONE_LEMMA_MODULES`` (4 modules)
    Standalone-lemma modules under ``apf/standalone/``. Have check_* defs but
    don't use the ``register(registry)`` contract. Listed in ``verify_all.MODULES``
    for scorecard enumeration; NOT loaded by ``bank._load()``.

``KNOWN_REGISTER_ANOMALIES`` (0 modules — cleaned up v24.3.20 2026-05-18)
    Modules with a non-standard ``register()`` signature (``register()`` with no
    argument). Their checks are NOT in ``REGISTRY`` because ``bank._load()``
    can't call ``register(REGISTRY)`` on them. Skipped silently via try/except
    TypeError in ``_load()``. Refactoring these to use the standard signature
    is deferred to a future cleanup pass.

Production-canonical REGISTRY size
----------------------------------

``EXPECTED_REGISTRY_SIZE = 3217`` (was 3193 pre-v24.3.22 dark-sector chain) re-derived from a clean load in a production
environment (scipy + numpy + full scientific stack). In a sandbox without
scipy, ``apf.cmb_finite_mode_covariance`` fails to import and the loaded
REGISTRY size drops by ~6 to ~3178. ``--bank-audit`` Bucket A surfaces this
as an environmental issue.

The previous narrative-incremented ``EXPECTED_THEOREM_COUNT = 3187`` over-counted
by 3; this re-derivation closes that gap.
"""
from __future__ import annotations


# 251 modules with register(registry) populating apf.bank.REGISTRY.
BANK_REGISTRY_MODULES: tuple[str, ...] = (
    "apf._optimize_vendored",  # v24.3.35 - Session 6 scipy-free bounded minimizer (closes sandbox scipy gap); 1 bank check
    "apf.acc_unification_all_p",
    "apf.acc_unification_no_imports",
    "apf.arch_defect_calculus_internal_identity_real_adapter",  # v24.3.43 - Step C arch internal-identity adapter; 3 bank checks
    "apf.arch_interface_engine_operational_internal_identity_real_adapter",  # v24.3.43 - Step C arch internal-identity adapter; 3 bank checks
    "apf.arch_rdfi_kernel_internal_identity_real_adapter",  # v24.3.43 - Step C arch internal-identity adapter; 3 bank checks
    "apf.admissible_representation_stack",
    "apf.anti_fitting_provenance_audit",
    "apf.aps",
    "apf.artifact_to_route_payload_adapter",
    "apf.base_fiber_allocation",
    "apf.bottom_msbar_export_candidate",
    "apf.bottom_msbar_rundec_real_adapter",
    "apf.bottom_msbar_transport",
    "apf.bottom_pole_obstruction_real_adapter",  # v24.3.42 - Mass-sector close R6; 3 bank checks
    "apf.capacity_coarse_grain_experiments",
    "apf.cfts_red_team_audit",
    "apf.charged_lepton_qed_real_adapter",
    "apf.delta_alpha_leptonic",  # v24.3.69 - leptonic running Delta alpha_lep(M_Z) first-principles from APF-banked charged-lepton pole masses (pure QED 1-loop); Delta alpha_had named data-bound external gate [C]; 4 bank checks
    "apf.delta_alpha_pqcd_m_z",  # v24.3.118 - Candidate A thresholded pQCD above Lambda_match = 2 m_c(m_c) = 2.558 GeV; first APF-banked first-principles slice of Delta alpha_had(M_Z); 1 check at [P_perturbative_QCD_M_Z_first_principles]
    "apf.delta_alpha_adler_m_z",  # v24.3.119 - Candidate B Euclidean Adler-function pQCD above Q^2_match = (2 m_c)^2 = 6.543 GeV^2; two-route corroboration vs v24.3.118 at 0.18% (< 1% gate); 1 check at [P_perturbative_QCD_M_Z_first_principles_Adler]
    "apf.charged_lepton_pole_real_adapter",  # v24.3.41 - Mass-sector Step D audit Finding 4 closer; 5 bank checks
    "apf.charged_trace_spectrum",
    "apf.charm_pole_obstruction_real_adapter",  # v24.3.42 - Mass-sector close R4; 3 bank checks
    "apf.charm_msbar_rundec_real_adapter",
    "apf.claim_dispatcher_multi_engine",  # v24.3.33 - Tier 3 multi-engine claim dispatcher (Session 4); 3 bank checks
    "apf.claim_to_interface_graph_compiler",
    "apf.class_transition",
    "apf.closed_world_completeness",
    "apf.cmb_finite_mode_covariance",
    "apf.codomain_transport_schema",
    "apf.codomain_selection_engine",  # v24.3.31 - Tier 2 IE family engine (codomain selection); 3 bank checks
    "apf.interface_engine_close_primitives",  # v24.3.248 - IE-family primitives distilled from the sin2thetaW close; 5 bank checks [P_structural]
    "apf.cosmogenesis_t1_t4_quartet_real_adapter",  # v24.3.44 - Step C Phase 2 cosmogenesis quartet; 3 bank checks
    "apf.core",
    "apf.cosmology",
    "apf.critical_slack",
    "apf.crystal",
    "apf.crystal_metrics",
    "apf.dark_apf2_real_adapter",
    "apf.dark_modified_gravity_obstruction_real_adapter",  # v24.3.43 - Step C dark-sector obstruction adapter; 3 bank checks
    "apf.dark_particle_id_obstruction_real_adapter",  # v24.3.43 - Step C dark-sector obstruction adapter; 3 bank checks
    "apf.defect_calculus_engine",  # v24.3.36 - Tier 2 IE family engine (defect calculus); 3 bank checks (Session 6 latent engine seed)
    "apf.dark_empirical_posterior_admission_contract",
    "apf.dark_mcmc_posterior_lane_admission",
    "apf.dark_posterior_certifier",
    "apf.dark_posterior_real_adapter",
    "apf.dark_profile_likelihood_lane_admission",
    "apf.dark_profile_mcmc_shared_contract",
    "apf.dark_w2_a_background_real_adapter",  # v24.3.45 - Step C Phase 3 dark-sector internal-identity adapter (APF2 w2(a) structural derivation per LATEST-62); 3 bank checks
    "apf.descent_exactness",
    "apf.descent_obstruction_calculus",
    "apf.down_lepton_trace",
    "apf.ew_counterterm_uncertainty_protocol",
    "apf.ew_dizet_real_adapter",
    "apf.ew_osw_reviewed_formula_evaluator_harness",  # v24.3.70 - reconciled architecture-only landing of the sibling OS-W reviewed-formula evaluator harness (fail-closed; wired to banked w_trace PV substrate + banked kernels, no duplication); value exports 0; 4 structural checks
    "apf.ew_osw_source_transcription_families",  # v24.3.80 - architecture-only certificate layer for the 6 SOURCE_TRANSCRIBE coefficient-map kernels installed verbatim under apf.ew_osw_source_families (W-transverse/gamma-Z/Z-transverse/vertex-box/gamma-gamma/counterterms; Dao-Gabelmann-Muehlleitner 2022 EPJC + Denner 1993); fail-closed, value exports 0; advances the harness pending count 14->8; 5 checks (4 P_structural + 1 C)
    "apf.ew_osw_numerical_assembly_harness",  # v24.3.81 - architecture-only certificate layer for the OS-W numerical assembly kernel (apf.ew_osw_numerical_assembly_kernel, installed verbatim): the slot-algebra wiring assemble_delta_r_one_loop + compute_delta_r_rem + solve_mw_from_delta_r ON TOP of the 6 source families; slot algebra proven == sum of the 6 banked family maps; fail-closed (9-entry nested guard), synthetic-test only, value exports 0; 5 checks (4 P_structural + 1 C)
    "apf.w_trace_pv_timelike_two_point",  # v24.3.84 - native PV two-point functions on the TIMELIKE/above-threshold branch (Re B0/B1/B11/B00 via principal value + absorptive Im B0); prerequisite for RePi_WW(M_W^2)/RePi_ZZ(M_Z^2). Validated by massless/equal/unequal closed forms + Im B0 + spacelike overlap (==banked where F>0) + real-part trace relation. 5 checks: b0_massless_closed [P], b0_threshold_closed [P], spacelike_overlap [P], trace_relation [P], subgate_partial [P_structural]
    "apf.w_trace_native_ew_self_energy",  # v24.3.83 - Stage 2 native fermionic EW self-energies SLOT-BY-SLOT (full SM couplings+colour) from native A0/B0/B1/B00: transverse A(p^2)=-(Nc/16pi^2){4(gL^2+gR^2)B00 - 2(gL^2+gR^2)[A0+m^2 B0+p^2 B1] + 4 gL gR m1 m2 B0}. Photon-transversality gate A_gamma(0)=0 (2 B00(0,m^2,m^2)=A0) + slot-by-slot Drho_top reproduces banked 0.008379 + agrees with v24.3.82 Veltman route. p^2=0 (no timelike branch). 4 checks: photon_transversality [P], drho_slot_by_slot [P], drho_routes_consistent [P], self_energy_scope_partial [P_structural]
    "apf.w_trace_native_drho_top",  # v24.3.82 - FIRST native-loop -> physical EW quantity rung (option-C native one-loop evaluator, Stage-2 fermionic gate). Native PV substrate (a0_fin/b0_fin) reproduces the Veltman rho-function F(m1^2,m2^2)=(m1^2+m2^2)(1+B0(0;m1^2,m2^2))-A0(m1^2)-A0(m2^2) (exact mu-independent identity, symbolically confirmed); fed APF inputs (m_t=163, sin2=3/13, alpha=1/128.21) the native Delta rho_top reproduces banked gauge.L_W_mass 0.008379 (m_b->0). p^2=0 so no timelike branch needed. Full Delta r_rem (timelike RePi, bosonic, delta_VB, UV cancellation) OPEN; no Delta r_rem/M_W; DIZET publishable. 4 checks: veltman_F_identity [P], drho_top_reproduces_banked [P], drho_top_mb_limit [P], drho_top_scope_partial [P_structural]
    "apf.w_trace_native_timelike_self_energy",  # v24.3.85 - Stage 2 timelike anchor: native fermionic photon VP -> Delta alpha_lep
    "apf.w_trace_native_uv_pole",  # v24.3.86 - Prereq B: UV-pole (Delta_eps) bookkeeping layer; fermionic photon-VP pole = QED beta-function
    "apf.w_trace_native_bosonic_scalar_vp",  # v24.3.87 - Stage 3 first bosonic piece: charged-scalar (Goldstone) photon VP (transverse; pole=1/4 fermion; 8/3 finite)
    "apf.w_trace_native_bosonic_photon_vp",  # v24.3.88 - Stage 3 FULL bosonic photon self-energy Sigma^AA_T from Denner App.B (arXiv:0709.1075) evaluated natively (re_b0_timelike + b0_pole): transversality + pole -3 [Goldstone +1/3, W+ghost -10/3; NOT the -7, which is the gamma-Z charge running] + finite<->pole + fermionic-norm anchor (sum N_c Q^2=8); 5 checks
    "apf.w_trace_native_charge_running",  # v24.3.89 - gauge-invariant one-loop charge running from Denner Sigma^AA_T + Sigma^AZ_T (App.B): bosonic -7 = -3 (photon SE) + -4 (gamma-Z mixing), s_W/c_W-independent; fermionic +(4/3) sum N_c Q^2 anchor (sum=8) calibrates the convention. 5 checks
    "apf.w_trace_native_gauge_boson_drho_uv",  # v24.3.90 - Denner Sigma^WW_T/Sigma^ZZ_T k^2=0 UV-pole structure + custodial Delta rho: fermionic Delta rho UV-FINITE (pole cancels ~1e-15, validates the full Sigma^WW/Sigma^ZZ transcription) + per-doublet custodial-symmetric pole; bosonic Delta rho bare pole = +4 universal (s2/MW/MH-independent), UV-divergent = Stage-4 counterterm target (renormalized bosonic Delta rho [C]). 4 checks
    "apf.w_trace_native_uv_cancellation_stage4",  # v24.3.91 - Stage-4 UV cancellation: bosonic gauge-boson self-energy poles linear in p^2 (renormalizable; (M^4/p^2) terms pole-free) + OS-renormalized Sigma_hat_VV UV-finite for AA(full ferm+bos, massless)/WW/ZZ(bosonic) + the v24.3.90 bosonic Delta rho +4 removed by OS mass renormalization (renormalized value [C]). 4 checks
    "apf.w_trace_native_fermionic_gauge_self_energy",  # v24.3.92 - fermionic gauge-boson self-energy p^2-pole coeffs (AA/AZ/ZZ/WW) from Denner + SM charges: P_AA=-(4/3) sum N_c Q^2 (=8, ties banked QED beta) + P_WW=-4/s^2 (g^2/s^2, 12 doublets) + Z/gZ couplings reproduce EW charge sum rules (Q I3=6, I3^2=6; Weinberg Q=I3+Y). Completes ferm+bos AA/AZ/ZZ/WW pole structure. 4 checks
    "apf.w_trace_native_timelike_gauge_width",  # v24.3.93 - timelike absorptive parts of Sigma^WW_T(M_W^2)/Sigma^ZZ_T(M_Z^2) via banked Im B0: optical theorem Im Sigma_VV(M_V^2)=M_V Gamma_V validated vs tree decay widths (ratio 1.0, M_V/alpha-independent, no measured input) + threshold gating (top excluded from Im Sigma_ZZ [2 m_t>M_Z] + Im Sigma_WW [m_t+m_b>M_W]). 4 checks
    "apf.w_trace_native_delta_r_uv_assembly",  # v24.3.94 - CAPSTONE: Denner master Delta r formula assembled from ALL native self-energy poles (Sigma^AA/AZ/WW/ZZ ferm+bos) -> full Delta r UV-FINITE (pole=0 to ~1e-15, cross-module integration test sensitive to cross-boson coeffs; requires OS c^2=M_W^2/M_Z^2), gauge-invariant (s2-independent); delta_VB Sirlin vertex+box closed form native. Finite Re Sigma(M^2) value [C] (external comparator) = only open Delta r_rem input. 4 checks
    "apf.w_trace_native_pv_massless_safe",  # v24.3.95 - massless/degenerate-safe two-point B0: analytic closed forms for exactly-massless lines (neutrino/photon/gluon), zero momentum, the scaleless point B0(0,0,0)=0, and the one-massless pseudo-threshold B0(m^2,0,m^2) (removable-singularity guard); reduces value-identically to the banked re_b0_timelike quadrature for all-massive p^2!=0 kinematics. Hardens the native PV substrate against the log(0) cases the SM self-energies need. 5 checks
    "apf.w_trace_native_os_renormalized_self_energy",  # v24.3.96 - OS-renormalized transverse self-energy Sigma_hat(p^2)=A(p^2)-A(M^2)-(p^2-M^2)A'(M^2) built native (timelike + massless-safe B-functions); OS conditions Sigma_hat(M^2)=Sigma_hat'(M^2)=0 + proven mu-independent (float floor ~5e-8 vs bare ~1e-3, >1e4x suppression) because the running is affine in p^2; bare mu-shift == analytic affine pole P(p^2) ln4 to ~1e-10. Closes the bare term-by-term scale-dependence that spoiled the precision attempt. 4 checks
    "apf.w_trace_native_fermion_sum_self_energy",  # v24.3.97 - native SM fermion-sum assembly of the transverse self-energies (3 gen quarks+leptons, colour, massless neutrinos via massless-safe B0), OS-renormalized per loop; total Sigma_hat_WW/ZZ mu-independent (~1e-8); registry sum N_c Q^2 = 8 + assembled photon-VP slope == QED beta; top-doublet Drho reproduces banked (m_b->0). 4 checks
    "apf.w_trace_native_bosonic_gauge_self_energy",  # v24.3.98 - native bosonic gauge-boson self-energies Sigma^AA/ZZ/W_T from Denner App.B (arXiv:0709.1075; W/Z/Higgs/Goldstone/ghost loops) on the PV toolkit; the v24.3.87-held W-sector piece done from the checked vertex algebra. Validated by banked poles: photon bosonic pole 3 k^2 (VP -3, dev 5e-10), bosonic Delta rho pole +4 M_H-independent (dev 8e-7), + k^2->0 regularity. Finite Re Sigma_bos(M^2) + Delta r_rem OPEN. 4 checks
    "apf.w_trace_native_delta_r_mw_assembly",  # v24.3.99 - CAPSTONE: native one-loop Delta r assembled from PV-evaluated self-energies (Denner GF1loop) -> M_W; reproduces Denner published one-loop M_W=80.23 to ~30 MeV (native 80.26), mu-independent (exact) + IR/lambda-finite. SM one-loop with native tools (inputs alpha/MZ/GF/mt/MH; Dalpha_had via effective masses); NOT parameter-free APF prediction. CLOSES native OS-W Delta r_rem/M_W (DIZET no longer needed for one-loop M_W). 4 checks
    "apf.w_trace_mw_from_effective_angle",  # v24.3.100 - the 3/13 -> M_W chain (FIRST time APF sin^2 theta_eff=3/13 drives the W mass): s2_OS=(3/13)/kappa_l -> M_W/M_Z=sqrt(1-s2_OS) -> M_W=80.40 GeV (M_Z-anchored), ~32 MeV from measured 80.369. Distinct from the v24.3.99 SM-loop evaluator (which never uses 3/13). Graded [C]: kappa_l 41% non-native + 3/13 candidate-for-effective-angle; M_Z scale anchor caps absolute M_W (sigma problem); only M_W/M_Z is [P]-reachable. 3 checks (chain [C], dimensionless [P_structural], open_gates [C])
    "apf.w_trace_native_zll_vertex_form_factors",  # v24.3.101 - native generic vertex form-factor layer (Denner App.C/haba3: V_a, V_b+- on the Denner-convention C0_D..C22_D wrapper over the native 3-point PV toolkit). Anchored by Denner OWN hab6 special-case closed forms (V_a mesh-converging 2.8e-3->6.4e-4; V_b- ~1e-4) + the QED Schwinger term F_2(0)=alpha/2pi (a_e). SUBSTRATE for Gate A Zll kappa_l; NOT yet kappa_l/Lambda_V/Lambda_S. 5 checks (4 [P] + subgate_partial [P_structural])
    "apf.w_trace_native_zll_kappa_l_oblique",
    "apf.w_trace_native_zll_R2_counterterm_pieces",  # v24.3.120 - R2 OS counterterm pieces wrapper for renormalized-vertex assembly; 1 check at [P_structural]  # v24.3.102 - Gate A rung 2a: native OBLIQUE leptonic effective-angle form factor kappa_l. Custodial (banked Xi_rho Drho, 59%) + native gamma-Z mixing (c/s)Sigma^gZ(M_Z^2)/M_Z^2 = +0.001483 [sign sourced from Dubovyk et al. arXiv:1906.08815 eq 1.1/1.2; Sigma^gZ from .99 Sig_AZ] -> oblique kappa_l = 0.023204 = 63% of banked Delta kappa_l=0.036808. Proper Zll vertex (non-oblique ~37%) OPEN [C], needs LEP YR hep-ph/9709229. 4 checks (custodial [P] + gamma-Z [P_structural] + oblique assembly [P_structural] + proper_vertex_open [C])
    "apf.ew_trace_scheme_transport_certifier",
    "apf.evaporation_e1_e4_quartet_real_adapter",  # v24.3.44 - Step C Phase 2 evaporation quartet; 3 bank checks
    "apf.evaporation_microtransport",  # v24.3.50 E1 (7 [P_structural]) + v24.3.51 E2 (2 [P|Schwarzschild ledger]) + v24.3.52 E3 import-certify (1 [P_structural] guard + 1 [P|island regime]) + E4 physical quotient (1 [P|APF physical quotient]); 12 checks total
    "apf.evaporation_quartet",
    "apf.ew_trace_to_scheme_real_adapter",
    "apf.extensions",
    "apf.fermion_normalizers",
    "apf.formal_kernel",
    "apf.foundation_inputs",
    "apf.fractional_reading",
    "apf.gauge",
    "apf.gauge_fiber_route_classifier",
    "apf.generations",
    "apf.globalization_promotion_gate",
    "apf.gravity",
    "apf.gravity_bianchi_rigidity_real_adapter",  # v24.3.44 - Step C Phase 2 gravity Bianchi rigidity; 3 bank checks
    "apf.gravity_gr_limit_full_close_real_adapter",  # v24.3.44 - Step C Phase 2 gravity GR-limit full close; 3 bank checks
    "apf.gravity_ringdown_capacity_schema_real_adapter",  # v24.3.44 - Step C Phase 2 gravity ringdown capacity schema; 3 bank checks
    "apf.horizon_fiber_cost_classifier",
    "apf.horizon_joint_bridge",
    "apf.horizon_ledger_reindexing",  # v24.3.48 - white-paper black-hole-entropy bank: 8 checks (4-commitment 1/4 structural derivation + horizon reindexing + no-bounded-remnant + evaporation [C] gate)
    "apf.i4_composition",
    "apf.initial_obstruction_classifier",
    "apf.interface_atlas",
    "apf.interface_dark_posterior_evidence_intake",
    "apf.interface_evidence_rerun_controller",
    "apf.interface_intelligence_CI_orchestrator",
    "apf.interface_intelligence_E2E_artifact_pipeline",
    "apf.interface_intelligence_engineering_command_center",
    "apf.interface_intelligence_failure_triage_assistant",
    "apf.interface_intelligence_live_smoke_harness",
    "apf.interface_intelligence_post_install_acceptance_auditor",
    "apf.interface_intelligence_registry_bridge",
    "apf.interface_intelligence_release_manifest",
    "apf.interface_intelligence_reviewer_reporter",
    "apf.interface_ew_counterterm_uncertainty_intake",
    "apf.interface_kinematic_holonomy_diagnostics",
    "apf.interface_kinematic_invariants",
    "apf.interface_kinematic_phase_space_atlas",
    "apf.interface_kinematic_solver",
    "apf.interface_kinematics_composition",
    "apf.interface_kinematics_engine",
    "apf.interface_kinematics_order_defects",
    "apf.interface_live_blocker_work_queue",
    "apf.interface_movement_graph_repair_planner",
    "apf.interface_repair_closure_simulator",
    "apf.interface_repair_frontier_explorer",
    "apf.interface_repair_obligation_compiler",
    "apf.interface_solver_descent_bridge",
    "apf.interface_solver_engineering_extensions",
    "apf.interface_structure_discovery_engine",
    "apf.interface_structure_movement_graph",
    "apf.interface_structure_transport_ledger",
    "apf.kinematics_adjudication_engine",  # v24.3.36 - Tier 2 IE family engine (kinematics adjudication); 3 bank checks (Session 6 latent engine seed)
    "apf.internalization",
    "apf.internalization_geo",
    "apf.kappa_int_bounds",
    "apf.killed_rivals",
    "apf.l_irr_induced_polarity",
    "apf.lambda_absolute",
    "apf.lambda_operator_derivation",
    "apf.light_quark_real_adapter",
    "apf.majorana",
    "apf.neutrino_mbb_reconciliation",
    "apf.neutrino_mbb_reconciliation_real_adapter",  # v24.3.44 - Step C Phase 2 neutrino m_bb reconciliation; 3 bank checks
    "apf.obstruction_dynamics",
    "apf.obstruction_repair_normal_form",
    "apf.paper1_kernel",
    "apf.obligation_packet_meta_schema",  # v24.3.34 - Tier 3 meta-schema (Session 5); 4 bank checks
    "apf.payload_batch_certification_runner",
    "apf.phase_14d3_completions",
    "apf.plec",
    "apf.quantum_admissibility",
    "apf.quantum_operator_derivation",
    "apf.recruitment",
    "apf.red_team",
    "apf.representation_descent_application_harness",
    "apf.representation_descent_full_integration",
    "apf.representation_descent_kernel",
    "apf.representation_descent_kernel_adversarial_audit",
    "apf.representation_descent_engine",  # v24.3.36 - Tier 2 IE family engine (representation descent); 3 bank checks (Session 6 latent engine seed)
    "apf.route_certification_starter_suite",
    "apf.route_certification_workbench",
    "apf.session_cosmo_update",
    "apf.session_delta_pmns",
    "apf.session_nnlo",
    "apf.session_qg",
    "apf.session_v63c",
    "apf.sin2theta_eff_bsy_real_adapter",
    "apf.sin2theta_eff_kappa_l_decomposition",  # v24.3.67 - Tier-4 leptonic form-factor (kappa_l) decomposition; leading custodial term APF-internal (reuses banked L_W_mass Delta rho + OS-codomain lever) + named remainder gate; 4 bank checks
    "apf.sin2theta_w_mass_ratio_identity_real_adapter",  # v24.3.42 - Mass-sector close R14 (internal identity); 3 bank checks
    "apf.sin2theta_w_source_identity_real_adapter",  # v24.3.42 - Mass-sector close R12 (internal identity); 3 bank checks
    "apf.spacetime",
    "apf.subspace_functors",
    "apf.superconductivity_codomain_adapter",  # v24.3.31 - Tier 4 SC codomain adapter under Codomain Selection Engine; 3 bank checks
    "apf.superfluidity_codomain_adapter",  # v24.3.62 - Tier 4 SF codomain adapter under Codomain Selection Engine (neutral coherent-phase sibling); 4 bank checks
    "apf.magnetism_codomain_adapter",  # v24.3.64 - Tier 4 Magnetism codomain adapter; 4 bank checks
    "apf.bec_codomain_adapter",  # v24.3.64 - Tier 4 Bose-Einstein condensation codomain adapter; 4 bank checks
    "apf.laser_coherence_codomain_adapter",  # v24.3.64 - Tier 4 Laser coherence codomain adapter; 4 bank checks
    "apf.synchronization_codomain_adapter",  # v24.3.64 - Tier 4 Synchronization codomain adapter; 4 bank checks
    "apf.topological_order_codomain_adapter",  # v24.3.65 - Tier 4 Topological order codomain adapter (completes the 7-regime coherent-phase family); 4 bank checks
    "apf.supplements",
    "apf.thermal_absolute",
    "apf.top_msr_R_star_real_adapter",  # v24.3.41 - Mass-sector Step D audit Finding 4 closer; 5 bank checks
    "apf.top_msr_r_evolution_real_adapter",
    "apf.top_pole_mc_obstruction_real_adapter",  # v24.3.42 - Mass-sector close R9; 3 bank checks
    "apf.trace_anchors",
    "apf.trace_scheme_transport",
    "apf.trace_sector_closure",
    "apf.trace_to_scheme_transport_theorem",
    "apf.trace_transport_completion",
    "apf.trace_transport_composition",
    "apf.trace_transport_ledger",
    "apf.trace_transport_routes",
    "apf.unification",
    "apf.unification_projection_essentiality",
    "apf.unification_three_levels",
    "apf.universality_forcing",
    "apf.up_family_trace",
    "apf.validation",
    "apf.w_os_route_terminal_closure",
    "apf.pi_gammagamma_2l_moment_native",  # v24.3.253 - native master-route 2-loop photon-VP reproduces Kallen-Sabry M(0)=82/81 [P]
    "apf.s_parameter_native",  # v24.3.255 - native EW oblique S (3 checks, scope-fenced reproductions): fermion-loop |S|=N_c/6pi + Higgs dS/dln(m_H^2)=1/12pi + oblique curvature 1/30 moment, all answer-free [P_S_oblique_native_reproduction]
    "apf.w_trace_native_bfm_photon_vp",  # v24.3.257 - native BFM photon VP: gauge-invariant bosonic charge-running |b|=7 answer-free from DDW vertices (route-strengthening of the banked Denner-import -7)
    "apf.s_parameter_pure_gauge_constant_native",  # v24.3.259 - gauge-invariant pure-gauge bosonic S constant -16.352 NATIVE [P] reproduction (BFM self-energies from DDW vertices via uniform projector; supersedes the same-session .258 [P+tool] import staging)
    "apf.s_higgs_finite_profile_native",  # v24.3.260 - native m_H-dependent finite Higgs profile of S (the last [P+tool] piece): D1(Z,h)+D2(h,G0) via two-mass native reducer; relative sign FORCED by executed i-count calibrated to native Goldstone(+1)/W-phi-mixed(-1) anchors (GLOO-independent); slope->+1/12pi, profile -0.13699 [P_S_higgs_finite_profile_native_reproduction]
    "apf.w_trace_acfw_candidate_preflight",
    "apf.w_trace_acfw_delta_r_extraction_attempt",
    "apf.w_trace_admitted_row_covariance_bridge",
    "apf.w_trace_apf_native_one_loop_evaluator",
    "apf.w_trace_candidate_payload_attempt",
    "apf.w_trace_cms_global_fit_context",
    "apf.w_trace_component_sum_certificate",
    "apf.w_trace_constants_source_ledger",
    "apf.w_trace_correlated_uncertainty_model",
    "apf.w_trace_counterterm_convention",
    "apf.w_trace_delta_r_comparison_harness",
    "apf.w_trace_delta_r_component_payload",
    "apf.w_trace_delta_r_finite_map",
    "apf.w_trace_delta_r_pull_diagnostics",
    "apf.w_trace_delta_r_remainder_resolution",
    "apf.w_trace_delta_r_route_input_evaluation",
    "apf.w_trace_delta_r_row_extraction_closeout",
    "apf.w_trace_delta_r_source_acquisition_matrix",
    "apf.w_trace_delta_r_source_candidate_registry",
    "apf.w_trace_delta_r_source_extraction_protocol",
    "apf.w_trace_delta_r_source_mapping",
    "apf.w_trace_delta_r_transport_buildout",
    "apf.w_trace_denner_diagram_coefficient_table_closeout",
    "apf.w_trace_denner_formula_import_native_assembly",
    "apf.w_trace_denner_sirlin_counterterm_functional",
    "apf.w_trace_denner_sirlin_notation_map",
    "apf.w_trace_denner_ward_identity_counterterm_import",
    "apf.w_trace_diagram_family_numeric_evaluator_import",
    "apf.w_trace_dizet_acquisition_instrumentation",
    "apf.w_trace_dizet_executable_run",
    "apf.w_trace_dizet_flag_sensitivity_covariance",
    "apf.w_trace_dizet_internal_dr_decomposition",
    "apf.w_trace_dizet_row_admission_covariance",
    "apf.w_trace_e2e_import_pipeline_manifest",
    "apf.w_trace_external_ingestion_dryrun",
    "apf.w_trace_external_source_adapter",
    "apf.w_trace_final_export_readiness",
    "apf.w_trace_finite_part_evaluator_gate",
    "apf.w_trace_finite_part_ledger",
    "apf.w_trace_finite_part_skeleton",
    "apf.w_trace_full_loop_derivation_closeout",
    "apf.w_trace_import_session_log",
    "apf.w_trace_import_session_replay",
    "apf.w_trace_independent_delta_r_crosscheck",
    "apf.w_trace_input_basis_ledger",
    "apf.w_trace_input_convention_stress_test",
    "apf.w_trace_measurement_quarantine_context",
    "apf.w_trace_multisource_delta_r_comparison",
    "apf.w_trace_native_finite_remainder_evaluator",
    "apf.w_trace_next_payload_requirements",
    "apf.w_trace_numeric_source_adapter",
    "apf.w_trace_onshell_transport",
    "apf.w_trace_payload_fixture",
    "apf.w_trace_payload_import_cli",
    "apf.w_trace_payload_source_pack",
    "apf.w_trace_payload_template_pack",
    "apf.w_trace_physical_export_lock",
    "apf.w_trace_physics_source_stop_condition",
    "apf.w_trace_prediction_cluster_robustness",
    "apf.w_trace_publication_claim_language",
    "apf.w_trace_pv_scalar_integral_substrate",
    "apf.w_trace_pv_tensor_reduction",  # v24.3.71 B1 + v24.3.72 B00/B11 - native PV two-point tensor reduction (rank-1 + rank-2) on the banked A0/B0 substrate (native rungs of the OPEN G2F gate; self-validating, no external input); 7 checks
    "apf.w_trace_pv_derivative_two_point",  # v24.3.73 - native PV two-point momentum derivatives B0\'/B1\' (for OS wave-function/mass renormalization); self-validating vs finite-difference + closed forms, no external input; 4 checks
    "apf.w_trace_pv_c0_general_momentum",  # v24.3.74 - native general-momentum spacelike scalar C0 (extends the banked zero-momentum-only C0; prerequisite for 3-point tensor reduction); self-validating via p->0 limit + S3 symmetry, no external input; 4 checks
    "apf.w_trace_pv_cij_three_point",  # v24.3.75 C1/C2 + v24.3.76 C00/C11/C12/C22 - native PV three-point tensor reduction (rank-1 + rank-2) on the general-momentum C0 + banked B0/B1; self-validating via contraction identities + metric-trace relation, no external input; 6 checks
    "apf.w_trace_pv_timelike_three_point",  # v24.3.103 - OS-W Gate A R0: native scalar C0 on the TIMELIKE/above-threshold branch (Re principal value + absorptive Im) via 1D-reduced Feynman integral + tanh-sinh per smooth piece; extends c0_general (spacelike-only) so the BHM Zll Lambda_2/Lambda_3 can be complex at s=M_Z^2. Self-validating: spacelike overlap (==banked c0_general, Im=0), Im two ways (analytic-inner vs delta root count), Im closed form (0,0,s;M,M,M), S3 permutation symmetry + below-threshold Im=0. 5 checks: spacelike_overlap [P], absorptive_two_ways [P], absorptive_closed_form [P], permutation_threshold [P], subgate_partial [P_structural]
    "apf.w_trace_pv_timelike_three_point_tensor",  # v24.3.104 - OS-W Gate A R0b: native rank-1 three-point tensor coefficients (C1,C2) on the TIMELIKE/above-threshold branch (Re principal value + absorptive Im) via the 1D-reduced Feynman integral with stable single-log inner I (avoids catastrophic cancellation at simplex corners; m1=0 nu/W/W case), tanh-sinh per smooth piece. Self-validating: spacelike overlap (==banked c1_c2_direct, Im=0), Im closed forms for (0,M,M,0,0,s) and (M,M,M,0,0,s) above threshold, Im two ways (analytic-inner vs delta root count), threshold (Im=0 below). 4 checks: spacelike_overlap [P], absorptive_closed_form [P], absorptive_two_ways [P], subgate_partial [P_structural]
    "apf.w_trace_pv_timelike_three_point_tensor_rank2",  # v24.3.105 - OS-W Gate A R0c: native rank-2 three-point tensor coefficients (C00, C11, C12, C22) on the TIMELIKE/above-threshold branch via closed-form K(x)=int y^2/(F-i eps)dy + L(x)=int ln(F-i eps)dy via integration-by-parts (single complex log of F(Y), no branch ambiguity), tanh-sinh per smooth piece. Self-validating: spacelike overlap (==banked cij_rank2_direct), metric-trace relation 4 C00 + s12 C11 + s23 C22 + 2 p1.p2 C12 - 1/2 = B0 + m1^2 C0 (complex on timelike, ties to banked B0 + native C0), Im=0 below threshold/spacelike. 4 checks: spacelike_overlap [P], trace_relation [P], threshold [P], subgate_partial [P_structural]
    "apf.w_trace_pv_lambda_bhm_vertex",  # v24.3.106 - OS-W Gate A R1: native BHM Z-vertex scalar functions Lambda_2(s,M^2) and Lambda_3(s,M^2) per EWWGR L6062 (CERN 95-03 / hep-ph/9709229) with Feynman iepsilon prescription w = M^2/(s + i eps). Pure-Python: self-contained Li_2 (series + reflection), closed forms threaded through cmath. Self-validating: Li_2 reference values (Li_2(1)=pi^2/6, Li_2(-1)=-pi^2/12, Li_2(1/2)=pi^2/12-(ln2)^2/2, Li_2(0)=0), Li_2 Abel identity off the cut, spacelike reality (Lambda real for s<0), physical-kinematics reference values matched against mpmath dps=40 (Lambda_2/Lambda_3 at MZ^2 with MW^2 or MZ^2, and spacelike) to ~1e-12. 5 checks: Li2_reference_values [P], Li2_abel_identity [P], spacelike_real [P], physical_values [P], subgate_partial [P_structural]
    "apf.w_trace_pv_ewwgr_bare_proper_vertex",  # v24.3.107 - OS-W Gate A R1b: native EWWGR §6 (L6005-6055) Zff/γff proper-vertex 3-pt form factors F_V^Zf, F_A^Zf, F_Zν, F_V^γf, F_A^γf, and channel-specific F_L^f, G_L^f for f∈{ℓ,u,d}, built as a thin layer on R1 BHM Λ_2/Λ_3 (v24.3.106). Tree EW couplings v_f = I3 - 2 Q sW², a_f = I3. Framing corrected 2026-05-27 (wiki/Log.md LATER-17 +4): these are the 3-pt function piece of the renormalized one-loop vertex correction in EWWGR's bookkeeping (Eqs 166/167), NOT "bare" form factors awaiting a separate counterterm — the renormalization of the W-triangle is structurally absorbed into the UV-finite Λ_2/Λ_3. They do NOT include external fermion wavefunction renormalization (composed at EWWGR Eqs 248-249 layer; the BSY recipe at Eq 175 consumes the 3-pt piece here with the wavefunction handled by the [(1-Δr)/(1+Π̂^Z)]^{1/2} common factor that cancels in g_V/g_A for sin²θ_eff). Self-validating: |F_L^ℓ|~17.77 at s=M_Z² with sin²θ_W=3/13 (working-doc "F_L~18" in-bracket kinematic target; α/(4π) prefactor makes F_V^Zell, F_A^Zell ~10⁻²), neutrino F_V^Zν=F_A^Zν, spacelike reality, all 11 form factors match mpmath dps=40 reference to ~1e-15. The earlier "WWZ-cancellation gate -> small Λ̂~1e-4" framing was a misreading retracted with this update; the "_bare_" infix in module/check names is retained for bank-registry stability. 5 checks: F_L_ell_target [P], neutrino_consistency [P], spacelike_real [P], reference_values [P], subgate_partial [P_structural]
    "apf.w_trace_BSY_one_loop_kappa_l_native_validator",  # v24.3.123 - OS-W Gate A R2b validator: composes v24.3.107 3-pt F_V/F_A + v24.3.106 BHM Lambda_2/Lambda_3 + v24.3.99 native self-energies via EWWGR Eq 175 (BSY recipe). Single check T_BSY_one_loop_kappa_l_assembly_consistency_at_Denner_validated_inputs at [P_one_loop_BSY_3pt_at_Denner_validated_inputs_assembly_consistency] (tier 4). Certifies, at Denner-validated inputs (sW²=0.223339, α(M_Z)=1/128.21, m_t=140, M_H=100 via v24.3.99 hardcoded globals): (a) BSY composition internally consistent (no NaN; |F_V|, Π̂^γZ_R, Δρ in physical one-loop bands); (b) Δρ_OS reproduces Denner-published 0.00780 to ~0.3%; (c) Δκ_ℓ lands at +0.0475 in the one-loop SM band. Bank-side capstone for the v24.3.81-.107 one-loop arc; cleanly separates one-loop closure (this check) from all-orders closure (open at two-loop EW gate, multi-session arc scoped at `APF Reference Docs/Reference - Native OS-W Two-Loop Close Scoping Brief (2026-05-26).md`). Today's session findings: Q2 mixed-conventions hypothesis FALSIFIED; §13's "0.053" reproduced as no-Π̂^γZ + mixed-denom artifact (retracted); the "+0.0084 honest-open R2" framing was a frame-comparison error (matched-inputs reading: +1.6×10⁻³ at Denner-set; +1.7×10⁻² at PDG canonical, the latter identified as the two-loop EW gate). v24.3.107 docstring corrected earlier today (3-pt function piece, not "BARE"; pre-edit snapshot at Codebase/Old/). HONEST NON-CLAIMS: Export_BSY_one_loop_assembly_consistency_at_Denner_set=1 (this check); Export_BSY_kappa_l_PDG_canonical_one_loop=0; Export_BSY_kappa_l_all_orders=0; Export_BSY_kappa_l_physical_final=0; Export_two_loop_EW_complete=0; target_consumed=0. Source findings: `APF Reference Docs/Reference - Q2 Empirical sW2 BSY Probe Findings (2026-05-27).md` (428 lines, three executable witnesses at `outputs/kappa_l_BSY_*.py`). 1 check: BSY_one_loop_kappa_l_assembly_consistency_at_Denner_validated_inputs [P_one_loop_BSY_3pt_at_Denner_validated_inputs_assembly_consistency].
    "apf.w_trace_native_two_loop_tadpole",  # v24.3.124 - Two-Loop Arc Phase-1 Tier-1: APF-native connected two-loop scalar tadpole master assembly at current scope (unit-power three-branch closure: all-massive source-brace + Chetyrkin two-massive/one-massless + one-massive/two-massless reduction gate). Single check T_two_loop_tadpole_connected_scalar_master_current_scope at [P_two_loop_tadpole_scalar_connected_master_current_scope] (tier 4). Kernel from sibling-AI delivery APF_NATIVE_TWO_LOOP_TADPOLE_CONNECTED_MASTER_ASSEMBLY_v1 + bank-protocol wrapper appended. Scope explicitly restricted: full arbitrary-power / tensor general-three-massive master NOT promoted (HF-pattern honest non-claim). MS-bar pole/mu-derivative identity c_{-1}\' = 2 c_{-2} verified; connected-vs-reducible guard ensures result is not just disconnected A_0^2 product; permutation symmetry of finite part verified at SM-realistic inputs. Five supporting closure packs at DOCTRINE_CONSEQUENCES_BUNDLE_LATEST_44/: TIER1_REFERENCE_INTAKE_AND_ROUTE_MAP_v1 (bibliography), TADPOLE_FORMULA_GATE_v1 (route adjudication), TADPOLE_GENERAL_MASS_SCALAR_MASTER_v1 (Davydychev-Tausk BFT source binding), TADPOLE_CHETYRKIN_SUBTOPOLOGY_v1 (Chetyrkin scalar gate), TADPOLE_MASSLESS_LIMIT_AND_MSBAR_NORMALIZATION_v1 (massless+MSbar). All six packs ship target_consumed=0, gdrive_write_performed=False, FORBIDDEN_INPUT_LEDGER, SHA256SUMS manifests. Sibling discipline strong: refused brief's aspirational [P_two_loop_master_integral] grade in favor of scope-restricted master_current_scope. Honest non-claims: Export_two_loop_master_integral_tadpole=0, Export_arbitrary_denominator_powers_general_three_massive=0, Export_arbitrary_tensor_numerators_general_three_massive=0. 1 check: T_two_loop_tadpole_connected_scalar_master_current_scope [P_two_loop_tadpole_scalar_connected_master_current_scope].
    "apf.w_trace_native_two_loop_two_point",  # v24.3.126 - Two-Loop Arc Phase-1 Tier-1 bubble source+DOUBLE_COUNT gate: APF-native two-loop two-point bubble — source-formula binding (Smirnov-Tausk leading-log) + DOUBLE_COUNT_LEDGER discipline (irreducible vs reducible topology classifier) + threshold kinematic classifier. Full numeric master NOT promoted at this gate; scheduled for next pack APF_NATIVE_TWO_LOOP_TWO_POINT_MASSLESS_HIGH_ENERGY_AND_THRESHOLD_ANCHOR_v1. Single check T_two_loop_two_point_bubble_source_and_double_count_gate at [P_source_formula_and_double_count_gate_two_loop_two_point_bubble; C_full_numeric_master_pending] (tier 4). Pattern parallel to v24.3.107 ('3-pt piece only, not full vertex') and v24.3.118 ('Δα_had pQCD above Λ_match, not full Δα') — scoped gate banked now, full closure scheduled. Sibling delivery APF_NATIVE_TWO_LOOP_TWO_POINT_BUBBLE_SOURCE_AND_DOUBLE_COUNT_GATE_v1 (verifier 18/18 PASS, staged at DOCTRINE_CONSEQUENCES_BUNDLE_LATEST_44/). Honest non-claims: Export_two_loop_master_integral_two_point_bubble=0 (next pack), Export_external_numeric_package_as_derivation=0 (pySecDec/FIESTA/LiteRed outputs forbidden as inputs per Phase-1 brief FORBIDDEN_INPUT_LEDGER), Export_native_two_loop_{M_W,delta_r,kappa_l}=0, target_consumed=0. 1 check: two_point_bubble_source_and_double_count_gate [P_source_formula_and_double_count_gate_two_loop_two_point_bubble].
    "apf.w_trace_native_two_loop_sunset",  # v24.3.130 - Two-Loop Arc Phase-1 Tier-1 SUNSET first gate: source differential-equation + threshold expansion gate. Four-region branch router (tadpole-boundary at p²=0 / threshold-timelike above (m1+m2+m3)² / euclidean-spacelike below 0 / intermediate between 0 and threshold), Caffo-Czyz-Laporta-Remiddi 1998 master basis F0/F1/F2/F3 schema, Davydychev-Tausk 1993 equal-mass closed-form source bound, Smirnov 1991 threshold expansion source bound, ε-pole coefficient schema declared, mass-permutation invariance verified across all 6 permutations of (m1,m2,m3). Single check T_two_loop_sunset_source_DE_and_threshold_gate at [P_source_gate_two_loop_sunset_DE_threshold; C_full_sunset_numeric_pending] (tier 4). Mirrors v24.3.126 (bubble source+DC gate) as first step of sunset ladder. With this push, Phase-1 Tier-1 sweep has structural gates for all three master integrals (tadpole Tier-1 P / bubble branch-assembly gate / sunset source-DE gate). Sibling delivery APF_NATIVE_TWO_LOOP_SUNSET_SOURCE_DE_AND_THRESHOLD_GATE_v1 (verifier 31/31 PASS, staged at DOCTRINE_CONSEQUENCES_BUNDLE_LATEST_44/). Honest non-claims: Export_two_loop_master_integral_sunset=0 (next pack), Export_external_numeric_package_as_derivation=0, Export_native_two_loop_{M_W,delta_r,kappa_l,M_W_physical_final}=0, target_consumed=0. 1 check: sunset_source_DE_and_threshold_gate [P_source_gate_two_loop_sunset_DE_threshold].
    "apf.w_trace_native_two_loop_tier1_status",  # v24.3.135 - Two-Loop Phase-1 Tier-1 single-swing capstone (cross-cutting meta-module). Records the Tier-1 sweep state across all 3 master integrals: tadpole at scoped Tier-1 master_integral grade (v24.3.125), two-point bubble at gate-ladder-complete grade (6 bank checks v24.3.126-.132), sunset at DE-solver-typed grade (3 bank checks v24.3.130, .133, .134). Phase-1 full completion EXPLICITLY NOT CLAIMED. Single check T_two_loop_tier1_single_swing_capstone at [P_tier1_single_swing_status; C_phase1_full_completion_pending_two_point_sunset_full_masters] (tier 4). Sibling delivery APF_NATIVE_TWO_LOOP_TIER1_SINGLE_SWING_CAPSTONE_v1 (verifier 22/22 PASS, staged at DOCTRINE_CONSEQUENCES_BUNDLE_LATEST_44/). 1 check.
    "apf.w_trace_native_two_loop_sunrise_de",  # v24.3.140 - APF-native sunrise/sunset DE matrix + 6-region branch router + guarded RK4 scaffold. Source-certified to Caffo-Czyz-Laporta-Remiddi 1998 (hep-th/9805118v2) Eq.(5),(7),(8),(12)-(20). Polynomial coefficients R²(a,b,c) and D(a,b,c,s) (expanded vs factored-over-threshold forms verified to agree at two test points); six-region branch router covering euclidean/tadpole/sub-thr/phys-thr/pseudo-thr/above-thr; RK4 scaffold validated on exp-decay ODE (multi-step h=0.1 accuracy 1e-6) with declared-singular-point abort. Full all-regions Tier-1 master STILL OPEN. Sibling APF_NATIVE_TWO_LOOP_SUNSET_DE_MATRIX_AND_ROUTER_v1 via APF_TWO_LOOP_PHASE1_PUSH_HARD_BUNDLE_v1. 1 check: T_two_loop_sunrise_DE_matrix_source_certified [P_source_certified_two_loop_sunrise_DE_matrix].
    "apf.w_trace_native_two_loop_two_point_bft_dst",  # v24.3.141 - APF-native two-loop two-point BFT one-mass + DST large-momentum coefficient family. Source-certified to BFT 1993 (hep-ph/9304303) for N_I1/N_I2/N_I4/N_Ie3 normalized hypergeometric branches and DST 1993 (hep-ph/9307371) Eq.(11)-(15),(30)-(33) for M0=6ζ(3) + M1 + M2 + vacuum F(m1²,m2²,m3²) symmetric function. M1 left-pair + right-pair symmetry verified to 1e-25; M2 left-right reflection + top-bottom reflection symmetries verified to 1e-20; vacuum F (a,b) and (b,c) permutation symmetries verified; BFT one-mass branches finite at small-q²; Padé bridge with Gaussian-elim Taylor-to-[L/M] converter validated on geometric series anchor; threshold catalog (4 named regions) + high-energy classifier. M3+ NotImplementedError guard enforced. Full Tier-1 master for unrestricted arbitrary-mass two-point STILL OPEN. Sibling APF_NATIVE_TWO_LOOP_TWO_POINT_COEFFICIENT_FAMILY_IMPLEMENTATION_v1 via APF_TWO_LOOP_PHASE1_PUSH_HARD_BUNDLE_v1. 1 check: T_two_loop_two_point_BFT_DST_coefficient_family_current_depth [P_two_point_BFT_DST_coefficient_family_current_depth].
    "apf.w_trace_native_two_loop_sunrise_2d_finite",  # v24.3.142 - APF-native two-loop sunrise 2D finite-core + p2=0 Clausen boundary evaluator. Source-certified to Adams-Bogner-Weinzierl 2014 (arXiv:1405.5640) Eq.(1)-(3), Eq.(17)-(20), Eq.(21)-(25). Composes with v24.3.140 CCLR DE matrix. Sibling APF_NATIVE_TWO_LOOP_SUNSET_FINITE_CORE_AND_BOUNDARY_v2 via CLOSURE_PUSH_BUNDLE_v2. 1 check: T_two_loop_sunrise_2d_finite_core_and_boundary [P_two_loop_sunrise_2d_finite_core_and_boundary].
    "apf.w_trace_native_two_loop_two_point_euclidean_master",  # v24.3.143 - APF-native two-loop two-point D=4 Euclidean 5-line scalar master evaluator, projective Feynman-parameter normalization. Genuine irreducible master (central-line m3 sensitivity falsifies B0xB0 product). Source-certified to DST 1993 + BFT 1993 + Berends-Davydychev-Smirnov 1996 + Bierenbaum-Weinzierl 2003. Composes with v24.3.141 BFT/DST coefficient family. Sibling APF_NATIVE_TWO_LOOP_TWO_POINT_EUCLIDEAN_MASTER_EVALUATOR_v2 via CLOSURE_PUSH_BUNDLE_v2. 1 check: T_two_loop_two_point_5line_euclidean_master_arbitrary_mass [P_two_loop_two_point_5line_euclidean_master_arbitrary_mass].
    "apf.w_trace_native_two_loop_phase2_master_interface_router",  # v24.3.144 - Phase-2 master-interface router consuming Phase-1 two-loop master substrate. Tadpole q=0 scalar → Chetyrkin scoped scalar bank PROMOTED; q≠0 / tensor → GUARDED. Sunset Euclidean → ABW 2D core + CCLR DE scaffold PROMOTED_CURRENT_DEPTH; p²=0 → ABW Clausen boundary PROMOTED; d=4 MSbar / timelike → GUARDED_BRANCH. Two-point Euclidean → 5-line projective evaluator PROMOTED; t>max(threshold) → DST M0/M1/M2 PROMOTED_CURRENT_DEPTH; threshold/between-threshold → GUARDED_BRANCH; BFT one-mass → PROMOTED. MB continuation guardrail (Czakon 2006): Euclidean comparator allowed, massive physical-region numeric guarded, full automation not claimed. Honest non-claims: Export_unrestricted_physical_sheet_master_router_P=0, Export_sunset_d4_all_sheets_MSbar_finite_part_P=0, Export_two_point_timelike_absorptive_all_thresholds_P=0, no EW self-energy / Δr / M_W value. Sibling APF_TWO_LOOP_PHASE2_MASTER_INTERFACE_AND_REGION_ROUTER_v1 via PHASE2_PUSH_BUNDLE_v1. 1 check: T_two_loop_phase2_master_interface_router_current_depth [P_two_loop_phase2_master_interface_router_current_depth].
    "apf.w_trace_native_two_loop_phase2_ew_self_energy_assembly_gate",  # v24.3.145 - Phase-2 EW self-energy assembly gate (TOY LEDGER ONLY). Runtime contract: PoleSeries Laurent record + RenormalizationContract schema (scheme, μ², finite-part convention, subtraction, gauge, tadpole convention, counterterm policy, source reference, Ward zero-momentum normalization, covariance ledger, coefficient_ledger_certified flag) + MasterTerm with irreducible flag for B0×B0 quarantine + ForbiddenInputLedger (measured_M_W/DIZET/ZFITTER/target_interval/fitted_counterterm refusal). 4-channel TOY pass (Σ_W, Σ_Z, Π_γγ, Π_γZ) + 8 negative-case refusals enforced. NO physical SM self-energy, Δr, or M_W value banked. Next gate explicitly named SOURCE_CERTIFIED_EW_TWO_LOOP_DIAGRAM_COEFFICIENT_LEDGER. Honest non-claims: Export_source_certified_EW_coefficient_ledger_P=0, Export_evaluated_Sigma_{W,Z}_2L_P=0, Export_evaluated_Pi_{γγ,γZ}_2L_P=0, Export_OSW_delta_r_rem_APF_internal_P=0. Sibling APF_TWO_LOOP_PHASE2_EW_SELF_ENERGY_ASSEMBLY_GATE_v1 via PHASE2_PUSH_BUNDLE_v1. 1 check: T_two_loop_phase2_ew_self_energy_assembly_gate_toy_ledger [P_two_loop_phase2_ew_self_energy_assembly_gate_toy_ledger; C_ew_two_loop_coefficient_ledger_pending].
    "apf.w_trace_native_two_loop_phase2_osw_deltar_connector_refusal",  # v24.3.146 - Phase-2 OS-W Δr connector + refusal gate (TOY LEDGER ONLY). Linear assembly map FiniteComponent × {4 self-energy channels + vertex/box + tadpole CT + charge/mixing CT} → Δr_rem candidate. Toy coefficients (+1, -0.75, +0.5, -0.25, +1, +1, +1) with Gaussian-propagated covariance. 9 negative-case refusals: missing physical certification, missing channel, missing component certification, convention mismatch, DIZET token, published_total_SM_M_W token, target_observable_consumed, fitted component, negative covariance. NO physical OS-W Δr_rem, no evaluated EW self-energy. Sibling APF_TWO_LOOP_PHASE2_OSW_DELTAR_CONNECTOR_AND_REFUSAL_v2 via PHASE2_PUSH_BUNDLE_v3. Honest non-claims: Export_OSW_delta_r_rem_APF_internal_P=0, Export_OSW_DeltaRhobarW_evaluated_P=0, Export_evaluated_EW_two_loop_self_energies_P=0, Export_vertex_box_two_loop_finite_remainder_P=0. 1 check: T_two_loop_phase2_osw_deltar_connector_refusal_toy [P_two_loop_phase2_osw_deltar_connector_refusal_toy; C_osw_deltar_physical_remainder_pending].
    "apf.w_trace_native_two_loop_phase2_ew_coefficient_ledger_audit",  # v24.3.147 - Phase-2 EW coefficient-ledger audit gate (SCAFFOLD ONLY). CoefficientRow schema (channel∈{Σ_W,Σ_Z,Π_γγ,Π_γZ}, diagram_class, topology∈7-element set, master_basis∈10-element set including T_tadpole_scalar_Tier1/S_sunset_DE_F0F1F2F3/S_sunset_2D_finite_core/B_two_point_5line_Euclidean/B_two_point_DST_high_energy_M0M1M2/B_two_point_BFT_one_mass/CT_local_counterterm/VB_vertex_box_family/WARD_photon_zero_momentum/MIX_gammaZ_renormalization, ConventionBlock, covariance_ledger, source_certified flag) + audit_ledger() 4-gate runner (schema/coverage/master-basis/source-cert). Placeholder scaffold passes schema+coverage but stays at PHYSICAL_SOURCE_OPEN. Toy-certified ledger passes physical promotion gate at TOY grade only. 10 refusal cases incl. reducible B0×B0 quarantine on two_point_5line. Forbidden-token scan extends OSW list with inverse_fit + posthoc_tuning. Sibling APF_TWO_LOOP_PHASE2_EW_COEFFICIENT_LEDGER_AUDIT_v2 via PHASE2_PUSH_BUNDLE_v3. Honest non-claims: Export_source_certified_EW_two_loop_coefficient_ledger_P=0, Export_evaluated_EW_two_loop_self_energies_P=0, Export_EW_physical_finite_part_values_P=0, Export_OSW_delta_r_rem_APF_internal_P=0. 1 check: T_two_loop_phase2_ew_coefficient_ledger_audit_scaffold [P_two_loop_phase2_ew_coefficient_ledger_audit_scaffold; C_source_certified_ew_coefficient_ledger_pending].
    "apf.w_trace_native_two_loop_phase2_ew_source_table_extraction_queue",  # v24.3.148 - Phase-2 EW source-table extraction queue (NO ROWS EXTRACTED). Five named literature source families: (1) Awramik-Czakon-Freitas-Weiglein 2004 W-mass hep-ph/0311148 aggregate-comparator + convention target (aggregate_only_guard=True); (2) Awramik-Czakon-Freitas 2006 complete sin²θ_eff hep-ph/0608099 — extractable; (3) ACFW 2004 fermionic hep-ph/0408207 — extractable; (4) CAF 2006 bosonic hep-ph/0602029 — extractable; (5) Denner 2007 0709.1075 one-loop conventions ONLY (aggregate_only_guard=True). Queue refuses pre-promoted targets, claims of extracted rows or promoted physical ledger, missing required sources, aggregate roles without guard, empty fields. CSV template physical_coefficient_ledger_template.csv ships in sibling pack. Sibling APF_TWO_LOOP_PHASE2_EW_SOURCE_TABLE_EXTRACTION_QUEUE_v1 via PHASE2_PUSH_BUNDLE_v3. Honest non-claims: Export_EW_source_table_rows_extracted_P=0, Export_source_certified_EW_two_loop_coefficient_ledger_P=0, Export_evaluated_EW_two_loop_self_energies_P=0. 1 check: T_two_loop_phase2_ew_source_table_extraction_queue [P_two_loop_phase2_ew_source_table_extraction_queue; C_ew_source_rows_not_extracted].
    "apf.w_trace_native_two_loop_phase2_ew_source_table_extraction",  # v24.3.149 - Phase-2 EW source-table extraction (AGGREGATE FORMULAS + CONVENTIONS). 29 source-local rows extracted from 5 EW two-loop papers: ACFW 2004 W-mass (hep-ph/0311148) Eqs.6-9 aggregate M_W parametrization c1..c11 in two variants — reproduces published shift table (M_H 100→200 = -41.4 MeV, mt+5.1 = +31 MeV, M_Z+2.1 = +2.6 MeV, Δα_had+3.6e-4 = -6.5 MeV, Δα_s+2.7e-3 = -1.7 MeV) to ≤0.4 MeV; ACF 2006 complete sin²θ_eff (hep-ph/0608099) Eqs.48-56 — 4-flavor sin²θ_eff^f fits (lepton=0.2312527, neutrino=0.2308772, up=0.2311395, down=0.2310286), Δκ^(α²)_rem k_0=-0.002711, Δr^(α²)_rem r_0=+0.003354; ACFW 2004 fermionic (hep-ph/0408207) methods + LF1 DE anchor; CAF 2006 bosonic (hep-ph/0602029) Eq.7 hard-region master expressions I4-I10 as source-local symbolic strings carrying explicit ε-poles + ζ(3) + π + S₂ + √3 structure; Denner 2007 (0709.1075) Eqs.3.32+3.35 δZ_e/δc_W/δs_W convention algebra. 29 rows tagged convention_anchor / aggregate_formula_evaluator / master_anchor — NONE promoted as physical diagram coefficient. Open-gap ledger 5 OPEN entries (Σ_W/Σ_Z/Π_γγ/Π_γZ coefficient ledgers + OS-W vertex/box remainder). Sibling APF_TWO_LOOP_PHASE2_EW_SOURCE_TABLE_EXTRACTION_v1 via PHASE2_PUSH_BUNDLE_v4. Honest non-claims: Export_source_certified_EW_two_loop_coefficient_ledger_P=0, Export_evaluated_EW_two_loop_self_energies_P=0, Export_row_level_diagram_coefficients_for_SigmaWZPi_channels_P=0, Export_DIZET_or_ZFITTER_aggregate_as_component_P=0, Export_OSW_delta_r_rem_APF_internal_P=0. 1 check: T_two_loop_phase2_ew_source_table_extraction_aggregate_and_convention [P_two_loop_phase2_ew_source_table_extraction_aggregate_and_convention; C_physical_coefficient_rows_pending].
    "apf.w_trace_native_two_loop_phase2_ew_tex_source_exact_extraction",  # v24.3.150 - Phase-2 EW TeX-source exact extraction (SOURCE WINDOWS ONLY). 23-row byte-level catalog across 5 EW two-loop families (ACFW W-mass:4 + ACF complete:5 + ACFW fermionic:4 + CAF bosonic:5 + Denner conventions:5). Every row at promotion_class=exact_source_window_not_coefficient_row with line ranges; full SHA256 manifest + byte-level snippets live at the bundle. Strictly stronger than v24.3.149 aggregate extraction; strictly weaker than row-local coefficient ledger. Sibling APF_TWO_LOOP_PHASE2_EW_TEX_SOURCE_EXACT_EXTRACTION_v2 via PHASE2_PUSH_BUNDLE_v5. Honest non-claims: Export_row_local_EW_2L_self_energy_coefficients_P=0, Export_evaluated_EW_2L_self_energies_P=0. 1 check: T_two_loop_phase2_ew_tex_source_exact_extraction_v2 [P_two_loop_phase2_ew_tex_source_exact_extraction_v2; C_row_local_ew_2l_coefficients_pending].
    "apf.w_trace_native_two_loop_phase2_zpole_form_factor_connector_dag",  # v24.3.151 - Phase-2 Z-pole form-factor connector DAG (CONNECTOR ONLY). ACF 2006 hep-ph/0608099 NNLO Z-pole 12-node/12-edge DAG: Σ'_ZZ^(2) + Σ_γZ → R_ZZ → R; ẑ_f^(2) + Σ'_γZ → Δκ̄; (R + Δκ̄) → sin²θ_eff^f. Phase-2 channel typing on Sigma_Z_2L and Pi_gammaZ_2L. Acyclicity guard via in-degree zero check. Sibling APF_TWO_LOOP_PHASE2_ZPOLE_FORM_FACTOR_CONNECTOR_DAG_v1 via PHASE2_PUSH_BUNDLE_v5. Honest non-claims: Export_Zpole_form_factor_coefficients_evaluated_P=0, Export_EW_2L_self_energy_coefficients_evaluated_P=0. 1 check: T_two_loop_phase2_zpole_form_factor_connector_dag [P_two_loop_phase2_zpole_form_factor_connector_dag; C_zpole_form_factor_coefficients_pending].
    "apf.w_trace_native_two_loop_phase2_bosonic_vertex_master_anchors",  # v24.3.152 - Phase-2 bosonic vertex master anchors I4-I10 (MASTERS ONLY). CAF 2006 hep-ph/0602029 Eq.7 hard-region masters with pole-order ledger (I4/I7 simple poles π²/9, π²/18; I5/I8 double poles 1/2; I6/I9/I10 finite). Symbolic + numeric finite parts via sandboxed eval using S₂≈0.260434 (Watson) + ζ(3)≈1.202057. Diagram coefficients multiplying masters NOT supplied. Sibling APF_TWO_LOOP_PHASE2_BOSONIC_VERTEX_MASTER_ANCHORS_v2 via PHASE2_PUSH_BUNDLE_v5. Honest non-claims: Export_bosonic_diagram_coefficient_rows_P=0, Export_evaluated_bosonic_Zll_2L_vertex_P=0. 1 check: T_two_loop_phase2_bosonic_vertex_master_anchors_I4_I10 [P_two_loop_phase2_bosonic_vertex_master_anchors_I4_I10; C_bosonic_diagram_coefficient_rows_pending].
    "apf.w_trace_native_two_loop_phase2_fermionic_vertex_reduction_ledger",  # v24.3.153 - Phase-2 fermionic vertex reduction method ledger (METHODS ONLY). ACFW 2004 hep-ph/0408207 banked as 5 named FermionicReductionRow records: top_large_mass (x=MZ²/mt² expansion), light_LF1_DE (Nielsen polylog finite part), idsolver_prototype (Prototype/PrototypeList + IBP/Lorentz identities), idsolver_integral (Integral linear combinations over masters), evaluation_homomorphism (projection to rationals). All status=coefficient_table_open. Full table requires DiaGen/IdSolver outputs or APF reproduction. Sibling APF_TWO_LOOP_PHASE2_FERMIONIC_VERTEX_REDUCTION_LEDGER_v1 via PHASE2_PUSH_BUNDLE_v5. Honest non-claims: Export_fermionic_full_coefficient_table_P=0, Export_evaluated_fermionic_Zll_2L_vertex_P=0. 1 check: T_two_loop_phase2_fermionic_vertex_reduction_ledger [P_two_loop_phase2_fermionic_vertex_reduction_ledger; C_fermionic_full_coefficient_table_pending].
    "apf.w_trace_native_two_loop_phase2_current_source_coefficient_no_go",  # v24.3.154 - Phase-2 CURRENT-SOURCE COEFFICIENT NO-GO (audit-first finding). Strongest audit-first content of the Phase-2 arc: declares the currently uploaded EW two-loop source set INSUFFICIENT for a row-local EW 2L diagram coefficient ledger. Decision matrix catalogues 5 row families with classifier: connector_relation→connector_only, aggregate_parametrization→comparator_only, convention_ledger→convention_only, method_row→method_only, master_anchor→master_anchor_only. Two next-gate paths explicitly named: (a) additional source coefficient tables/code outputs, (b) APF-internal derivation from Feynman rules + IBP + renormalization. Scope is current uploads, NOT physics impossibility. Sibling APF_TWO_LOOP_PHASE2_CURRENT_SOURCE_COEFFICIENT_NO_GO_v1 via PHASE2_PUSH_BUNDLE_v5. Honest non-claims: Export_source_certified_EW_2L_coefficient_ledger_from_current_uploads_P=0, Export_evaluated_EW_2L_self_energies_P=0, Export_OSW_delta_r_rem_APF_internal_P=0. 1 check: T_two_loop_phase2_current_source_coefficient_no_go [P_two_loop_phase2_current_source_coefficient_no_go; C_coefficient_ledger_requires_additional_sources_or_apf_derivation].
    "apf.w_trace_native_two_loop_phase2_missing_terms_source_and_derivation_plan",  # v24.3.155 - Phase-2 MISSING TERMS source map + derivation plan. Direct follow-on to v24.3.154 no-go: 14 acquisition targets (5 priority-1 Δr/muon-lifetime: FHW 2000 hep-ph/0007091, FHW 2002 hep-ph/0202131, AC 2002 muon-lifetime hep-ph/0208113, ACOv 2003 bosonic Δr hep-ph/0209084, AC 2003 complete muon-lifetime hep-ph/0305248; sin²θ_eff family ACFW 2004 fermionic PRL hep-ph/0407317 + ACF 2006 bosonic result hep-ph/0605339 + already-banked aggregates; Denner 2007 convention-only; ZFITTER/DIZET forbidden-as-component). 7 gap-to-source rows (Σ_W/Σ_Z/Π_γγ/Π_γZ + Zℓℓ form factors + muon-decay vertex/box remainder + OSW Δr_rem). 7-stage workplan A→G (freeze convention → generate diagram classes → project amplitudes → reduce to masters → evaluate rows → assemble+audit → validate vs aggregates). 4 Stage-F forbidden tokens (measured M_W, DIZET aggregate as component, published total SM M_W, fitted counterterm). 7-pack downstream sequence MISSING_SOURCE_ACQUISITION → DELTA_R_SOURCE_IMPORT → ZPOLE_DELTA_KAPPA_SOURCE_IMPORT → DIAGRAM_GENERATOR_AND_PROJECTORS → IBP_REDUCTION_LEDGER → COEFFICIENT_ROW_LEDGER → OSW_DELTAR_EVALUATOR. Allowed + 4 prohibited claim-language strings banked. Sibling APF_TWO_LOOP_PHASE2_MISSING_TERMS_SOURCE_AND_DERIVATION_PLAN_v1. Honest non-claims: Export_source_certified_EW_2L_diagram_coefficient_ledger_P=0, Export_evaluated_{Sigma_W,Sigma_Z,Pi_gammagamma,Pi_gammaZ}_2L_P=0, Export_vertex_box_2L_finite_remainder_P=0, Export_OSW_delta_r_rem_APF_internal_P=0, Export_DIZET_as_component_P=0. 1 check: T_two_loop_phase2_missing_terms_source_and_derivation_plan [P_two_loop_phase2_missing_terms_source_map_and_derivation_plan; C_seven_acquisition_packs_pending].
    "apf.w_trace_native_two_loop_phase2_delta_r_source_import",  # v24.3.156 - Phase-2 Δr SOURCE IMPORT. 10 source rows from 5 newly uploaded Δr/muon-lifetime papers (FHW 2000 hep-ph/0007091, FHW 2002 hep-ph/0202131, AC 2002 hep-ph/0208113, ACOv 2003 hep-ph/0209084, AC 2003 hep-ph/0305248) + 13 exact source MD windows. AC 2002 Eq.(11) bosonic ΔM_W = -(1.491 + 1.779·Δr̄)·1e4·Δr_bos banked as delta_mw_from_bosonic_delta_r() — reproduces -0.8946 MeV at Δr_bos=6e-5. Bosonic Δr range [+6e-5, -4e-5] → sub-MeV |ΔM_W|. No row_local_physical_coefficients. Sibling APF_TWO_LOOP_PHASE2_DELTA_R_SOURCE_IMPORT_v1 via PHASE2_PUSH_BUNDLE_v6. Honest non-claims: Export_source_certified_EW_two_loop_diagram_coefficient_ledger_P=0, Export_evaluated_{Sigma_W,Sigma_Z,Pi_gammagamma,Pi_gammaZ}_2L_P=0, Export_OSW_delta_r_rem_APF_internal_P=0. 1 check: T_two_loop_phase2_delta_r_source_import_v1 [P_two_loop_phase2_delta_r_source_import_v1; C_row_local_self_energy_coefficient_ledger_pending].
    "apf.w_trace_native_two_loop_phase2_zpole_bosonic_deltakappa_import",  # v24.3.157 - Phase-2 Z-pole bosonic Δκ source import. ACF 2006 hep-ph/0605339 bosonic Δκ_bos×10⁴ table for M_H∈{100,200,600,1000}={-0.74,-0.47,+0.17,+1.11} + sin²θ_eff^bos shift table {0.04,0.00,0.05,0.12}×10⁻⁴ (max ≤ 0.12 reproducing published "few×10⁻⁶") + Hollik cross-check sub-leading agreement to ≤ 0.002 in 10⁻⁴ units. Aggregate shift rows only; no row-local form-factor coefficients. Sibling APF_TWO_LOOP_PHASE2_ZPOLE_BOSONIC_DELTAKAPPA_IMPORT_v1 via PHASE2_PUSH_BUNDLE_v6. Honest non-claims: Export_Zpole_row_local_form_factor_coefficients_P=0, Export_complete_Zll_vertex_coefficient_ledger_P=0, Export_sin2eff_as_component_input_to_OSW_P=0. 1 check: T_two_loop_phase2_zpole_bosonic_deltakappa_import_v1 [P_two_loop_phase2_zpole_bosonic_deltakappa_import_v1; C_form_factor_coefficient_rows_pending].
    "apf.w_trace_native_two_loop_phase2_zfitter_comparator_guard",  # v24.3.158 - Phase-2 ZFITTER comparator guard. Formal role allowlist of 4 (comparator, same_input_total_evaluator_audit, implementation_context, regression_target) + 5 forbidden component tokens (DIZET_AGGREGATE_COMPONENT, ZFITTER_TOTAL_INPUT, PUBLISHED_TOTAL_SM_MW, FITTED_COUNTERTERM, MEASURED_MW). component_value role never allowed. Embedded-substring refusal. Forbidden tokens override allowed roles. Sibling APF_TWO_LOOP_PHASE2_ZFITTER_COMPARATOR_GUARD_v1 via PHASE2_PUSH_BUNDLE_v6. Honest non-claims: Export_ZFITTER_or_DIZET_component_consumed_P=0, Export_ZFITTER_row_local_coefficients_imported_P=0, Export_DIZET_row_covariance_imported_P=0. 1 check: T_two_loop_phase2_zfitter_comparator_guard_v1 [P_two_loop_phase2_zfitter_comparator_guard_v1; C_zfitter_component_consumption_permanently_refused].
    "apf.w_trace_native_two_loop_phase2_ew_diagram_coefficient_derivation_engine_scaffold",  # v24.3.159 - Phase-2 EW diagram-coefficient derivation engine SCAFFOLD. 8 REQUIRED_FAMILIES (4 EW self-energies Σ_W/Σ_Z/Π_γγ/Π_γZ + muon-decay vertex/box + Zℓℓ vertex + counterterm products + tadpole convention), 6 OPEN_PHYSICAL_FAMILIES (the 4 self-energies + 2 vertex/box), 6 FORBIDDEN_INPUTS (measured_MW, published_total_SM_MW, DIZET_aggregate_component, ZFITTER_total_input, target_interval, fitted_counterterm), 7-stage derivation matrix (diagram_inventory → projectors → algebra → IBP → master_eval → assembly → comparator). CoefficientRow validator refuses bad family/empty fields/target_consumed/fitted/source_certified=False. complete_physical_ledger([]) = False. NO physical rows. Sibling APF_TWO_LOOP_PHASE2_EW_DIAGRAM_COEFFICIENT_DERIVATION_ENGINE_SCAFFOLD_v1 via PHASE2_PUSH_BUNDLE_v6. Honest non-claims: Export_complete_physical_coefficient_ledger_P=0, Export_evaluated_{Sigma_W,Sigma_Z,Pi_gammagamma,Pi_gammaZ,vertex_box}_2L_P=0, Export_OSW_delta_r_rem_APF_internal_P=0. 1 check: T_two_loop_phase2_ew_diagram_coefficient_derivation_engine_scaffold_v1 [P_two_loop_phase2_ew_diagram_coefficient_derivation_engine_scaffold_v1; C_physical_coefficient_rows_pending].
    "apf.w_trace_native_two_loop_phase2_counterterm_residue_formula_ledger",  # v24.3.160 - Phase-2 push v7: renormalized counterterm + Z-pole NNLO residue formula ledger. Six required physical channels (Sigma_W/Sigma_Z/Pi_gammagamma/Pi_gammaZ/vertex_box/ZllR) seeded at physical_value=0; Delta_r/M_W aggregate grid comparator-only (published values held, never consumed as component, matching v24.3.158 ZFITTER role-typing); DIZET/ROKANC/RHOCC harness admits declared targets, refuses every component/aggregate token. AC 2002 bosonic Delta_M_W formula depended on from v24.3.156, not re-derived. Sibling APF_TWO_LOOP_PHASE2_PUSH_BUNDLE_v7 (5/5 PASS). Honest non-claims: Export_complete_EW_two_loop_diagram_coefficient_ledger_P=0, Export_evaluated_{Sigma_W,Sigma_Z,Pi_gammagamma,Pi_gammaZ,vertex_box}_2L_P=0, Export_OSW_delta_r_rem_APF_internal_P=0, Export_DIZET_or_published_MW_consumed_as_component_P=0. 1 check: T_two_loop_phase2_counterterm_residue_formula_ledger_current_depth [P_two_loop_phase2_counterterm_residue_formula_ledger_current_depth; C_physical_coefficient_values_pending].
    "apf.w_trace_native_two_loop_phase2_projectors_preibp_router",  # v24.3.161 - Phase-2 push v8: EW diagram projectors + pre-IBP scalar rows + master router + UV/IR/Ward cancellation testbench. Re-derives the exact-rational Laurent cancellation testbench (eps^-2/eps^-1 pole sums vanish per channel over fractions.Fraction; gauge-xi cancels; photon Ward Pi_gammagamma(0)=0); a control break row violates cancellation, proving the gate load-bearing. Five pre-IBP families + four projector families present. Sibling APF_TWO_LOOP_PHASE2_PUSH_BUNDLE_v8 (5/5 PASS). Honest non-claims: Export_IBP_reduced_rational_coefficient_rows_P=0, Export_complete_EW_two_loop_diagram_coefficient_ledger_P=0, Export_evaluated_{Sigma_W,Sigma_Z,Pi_gammagamma,Pi_gammaZ}_2L_P=0, Export_OSW_delta_r_rem_APF_internal_P=0. 1 check: T_two_loop_phase2_projectors_preibp_router_current_depth [P_two_loop_phase2_projectors_preibp_router_current_depth; C_ibp_reduced_coefficient_rows_pending].
    "apf.w_trace_native_two_loop_phase2_ibp_reduction_engine_tier0",  # v24.3.162 - Phase-2 push v9: IBP numerator-rewrite/linear-reduction engine + Tier-0 reduced rows + Laporta job specs + aggregate bridge. Re-derives the exact TP5 scalar-product -> inverse-propagator identities (p.k, q.k, p.q): restoring lowered propagators on each shifted integral and summing the engine coefficients recovers the scalar-product symbol exactly in sympy; each rewrite lowers exactly one denominator per shifted term; central-line (D3) contraction detected as one-loop product. Five Laporta job-spec families. Sibling APF_TWO_LOOP_PHASE2_PUSH_BUNDLE_v9 (5/5 PASS). Honest non-claims: Export_EW_complete_IBP_coefficient_output_P=0, Export_EW_complete_physical_self_energy_evaluator_P=0, Export_OSW_delta_r_rem_APF_internal_P=0. 1 check: T_two_loop_phase2_ibp_reduction_engine_tier0_current_depth [P_two_loop_phase2_ibp_reduction_engine_tier0_current_depth; C_complete_coefficient_output_pending].
    "apf.w_trace_native_two_loop_phase2_coefficient_output_slices",  # v24.3.163 - Phase-2 push v10: first actual coefficient-output slices (TP5 rational rows deg<=3 + SUN3 25 DE rows + ZFF_LIGHT LF1 + BOSONIC ultrasoft I1/I2->I3). Re-derives the TP5 numerator-expansion identity: each scalar-product monomial expands in the inverse-propagator basis and the emitted rational rows re-sum to the expansion exactly in sympy for all 10 test monomials through degree 3 (incl. degree-3 corners); every row physical_value=0, complete_family=0. Sibling APF_TWO_LOOP_PHASE2_PUSH_BUNDLE_v10 (7/7 PASS). Honest non-claims: Export_complete_EW_two_loop_physical_coefficient_ledger_P=0, Export_evaluated_self_energy_channels_P=0, Export_OSW_delta_r_rem_APF_internal_P=0, DIZET_ZFITTER_component_consumed=0. 1 check: T_two_loop_phase2_coefficient_output_slices_current_depth [P_two_loop_phase2_coefficient_output_slices_current_depth; C_complete_physical_coefficient_ledger_pending].
    "apf.w_trace_native_two_loop_phase2_coefficient_surface_no_smuggling",  # v24.3.164 - Phase-2 push v11: degree-5 TP5 coefficient surface + no-smuggling sector guard + SUN3 Taylor recurrence + muon hard-matching contract. Re-derives the TP5 expansion identity at degree 5 (corners + mixed reconstruct exactly in sympy) AND the no-smuggling guard: a genuine central-line-present five-line TP5 master may NOT be replaced by a B0xB0 one-loop product; product limit admitted only for central-line-removed sector classes. Four sector classes enumerated; classifier verified. Same irreducibility discipline as v24.3.143 central-line m3 falsifier. Sibling APF_TWO_LOOP_PHASE2_PUSH_BUNDLE_v11 (7/7 PASS). Honest non-claims: Export_complete_EW_two_loop_diagram_coefficient_ledger_P=0, Export_EW_physical_self_energy_evaluator_P=0, Export_OSW_delta_r_rem_APF_internal_P=0, Export_TP5_full_Laporta_reduction_P=0. 1 check: T_two_loop_phase2_coefficient_surface_no_smuggling_current_depth [P_two_loop_phase2_coefficient_surface_no_smuggling_current_depth; C_complete_physical_coefficient_ledger_pending].
    "apf.w_trace_native_two_loop_phase2_p_plus_ibp_tool_admission_policy",  # v24.3.165 - Phase-2 [P+IBP-tool] admission policy (principal decision, banked from v26 / APF_TWO_LOOP_PHASE2_EVALUATOR_REDIRECT_AND_PIBP_LEDGER_v1). Establishes [P+IBP-tool] as a framework epistemic grade analogous to [P+lattice]: a tool-computed IBP reduction coefficient (determined algebra, fixed by diagram topology) is admissible ONLY with an independent native spot-check (REFUSE_UNCHECKED_IBP_TOOL_ROW otherwise); all physical-result categories (measured/published M_W, DIZET/ZFITTER component, DFGRU fit, fitted counterterm, target observable) refused as smuggling; target consumption always refused; native IBP identities admitted as native algebra; comparator total evaluators comparator-only. Unblocks the post-redirect fast path (fixed-benchmark numeric IBP solve -> two-loop vacuum master Delta_rho -> master-DE numeric integration -> real Ward cancellation -> comparator-only audit) without banking any physical value. Symbolic track (v18-v23) re-tasked as the verifier layer supplying the spot-checks. Honest non-claims: Export_physical_two_loop_value_P=0, Export_tool_IBP_coefficient_admitted_without_spot_check_P=0, Export_physics_result_component_admitted_P=0. 1 check: T_two_loop_phase2_p_plus_ibp_tool_admission_policy [P_p_plus_ibp_tool_admission_policy].
    "apf.continuation_sum_measure",  # v24.3.166 - FIRST native bankable result of the EW->distinction-geometry pivot (2026-05-28). Continuation-sum measure: the universal one-loop factor is (4pi)^{-D/2}, = 1/(16pi^2) at native D=4 (T8 [P]). Two re-verified pillars: (1) measure theorem (angular continuation-direction volume Omega_{D-1}=2pi^{D/2}/Gamma(D/2) carries 1/Gamma(D/2); quadratic-cost radial Beta integral carries Gamma(D/2); they cancel -> (4pi)^{-D/2}); (2) A2 lemma (free cost kernel forced to k^2+m^2 by translation inv [Delta_continuum] + Lorentz [L_irr] + locality [L_loc] + bounded-below floor [L_epsilon_star] via no-ghost/Ostrogradsky exclusion of higher-derivative free kinetic terms -- verified at propagator-residue level: single pole +1, two-pole opposite-sign ghost). Math levers (Gaussian, Beta, Ostrogradsky) cited [P+math] on native premises. Honest non-claims: bare 1/(16pi^2) carries the (2pi)^D convention (Export_measure_value_convention_free_P=0); structure (4pi)^{-D/2} is the invariant claim, forced by native D=4; nothing tuned (check confirms measure tracks D, 1/(4pi) at D=2); Export_physical_final_P=0; Ostrogradsky flagged cited-math. Keystone: completes Delta_rho-from-distinction rung natively + leading EW radiative face native + seats into coherence frontier. Refs: APF Reference Docs continuation-sum-measure v0.2 + A2 closure (2026-05-28) + scripts. 1 check: T_continuation_sum_measure_native_from_D4 [P_structural_continuation_sum_measure_native_from_D4_modulo_convention].
    "apf.delta_rho_leading_distinction",  # v24.3.167 - FIRST physical EW observable derived end-to-end via the distinction picture (completes the Delta_rho rung the v24.3.166 keystone unlocked). Leading custodial response Delta_rho^(1)_leading = N_c * F(m_t^2,m_b^2) * [1/(16pi^2)] / v^2 = N_c m_t^2/(16pi^2 v^2) = N_c y_t^2/(32pi^2), equal to standard one-loop N_c x_t (comparator, not consumed). All factors native: N_c color distinction-count (gauge); custodial cost-asymmetry F symmetric under t<->b + F(m,m)=0 (rho=1 when held cost-equivalent) forcing leading scale = heavier cost m_t^2; continuation-sum measure 1/(16pi^2) (banked v24.3.166, forced by native D=4); EW interface cost v^2. Honest non-claims: Export_delta_rho_numerical_value_native_P=0 (value needs y_t = absolute top scale = OPEN sigma-derivation gap; only structure/ratio native), Export_full_delta_rho_MH_dependent_P=0 (leading M_H=0 slice only, subleading [P+tool]), Export_physical_final_P=0, (2pi)^D convention inherited. Deps: T_continuation_sum_measure_native_from_D4, Theorem_R, T_sin2theta. Refs: APF Reference Docs Delta-rho v0.1 + A2 closure (2026-05-28). 1 check: T_delta_rho_leading_custodial_from_distinction [P_structural_delta_rho_leading_custodial_from_distinction_modulo_scale_and_convention].
    "apf.mw_value_from_equilibrium_and_custodial",  # v24.3.168 - M_W value as {equilibrium angle sin2theta_W=3/13 + custodial Delta_rho family + native continuation-sum measure 1/(16pi^2)}, no loop construction. Composition/accounting theorem certifying the mechanistic decomposition of the banked L_W_mass M_W=80.3336 GeV (0.044%): the dominant SM Delta_alpha running is absorbed into the equilibrium angle (not summed); the only off-angle shift is custodial Delta_rho (= banked distinction-Delta_rho, measure 1/(16pi^2) = banked continuation-sum measure). Five native [P] pieces (angle, m_H, measure, custodial structure, N_c); exactly three non-native inputs (open absolute top scale m_t = sigma-gap; hadronic Delta_alpha_had [75.7% pQCD slice banked v24.3.118]; alpha_s) -- none a loop construction. No measured M_W consumed. Honest non-claims: Export_MW_value_fully_native_from_A1_P=0 (gated on absolute scale + Delta_alpha_had), Export_physical_final_P=0. Deps: L_W_mass, T_sin2theta, T_delta_rho_leading_custodial_from_distinction, T_continuation_sum_measure_native_from_D4, L_Higgs_2loop. 1 check: T_mw_value_equilibrium_plus_custodial_no_loop_construction [P_structural_mw_value_equilibrium_plus_custodial_modulo_absolute_scale_and_alpha_had].
    "apf.yt_absolute_scale_normalization_no_go",  # v24.3.169 - NO-GO (negative result, route a fenced off): the absolute top Yukawa y_t cannot be fixed by a normalization/unitarity principle on the Yukawa matrix. (1) rank-2 structure required for CKM + charm mass makes the top a two-channel sum c_B+c_H = x^3+1 = 9/8 > 1, breaking the single-correlation Cauchy-Schwarz ceiling; (2) all matrix norm-invariants (operator/Frobenius/a_Y-trace) are top-dominated (Frob/op-norm=1 to 1e-4) so fixing any IS fixing y_t (circular); (3) the only count handle (spectral a_Y) is N_c-color-convention-dependent (a_Y=N_c->y_t=1; a_Y=1->y_t=1 or 0.577), y_t moves by sqrt(N_c) under it -> non-physical by the invariance criterion (Paper 28 "needs a_Y=N_c, actual ~1" convention fork). Conclusion: absolute scale requires a dimensionful/cross-scale input (v_H-M_Pl hierarchy, route b), consistent with y_t being non-invariant (runs). Scope: fences the matrix-normalization / single-correlation-ceiling class; does not rule out a genuine dimensionful/dynamical derivation. No value banked. Deps: L_Yukawa_bilinear, L_mass_from_capacity, T_channels, T_capacity_ladder, T_q_Higgs. 1 check: T_yt_absolute_scale_not_fixable_by_normalization_no_go [P_structural_yt_absolute_scale_normalization_no_go].
    "apf.sigma_scale_capacity_formula_gate",  # v24.3.170 - GATE (disposition, route-b entry): the Paper-28 v_H capacity formula reproduces v_H=246.5 GeV from declared inputs but is HELD, not a native absolute-scale derivation. Prefactor a_total=a_Y+c_R with a_Y=N_c y_t^2, b=N_c y_t^4 carries the no-go-blocked top Yukawa; c_R (RH-neutrino/sigma0 term) is a SECOND load-bearing held input (~42% of a_total; without it v_H~144); color-counting convention moves v_H across 178-452 GeV (no-go corroboration). Absolute scale = one capacity relation among {M_Pl,v_H,y_t,c_R} needing one independent dimensionful input (route b). Measured v_H comparator only (residual 0.30 GeV). Faithful to audited-clean sibling pack APF_ABSOLUTE_MASS_SCALE_SIGMA_AUDIT_AND_REPAIR_v1 (12/12 asserts, no forbidden input, fail-closed gate) + c_R-second-input finding from the audit. No value banked. Deps: T_yt_absolute_scale_not_fixable_by_normalization_no_go, L_vev_threshold_matching, L_sigma_VEV. 1 check: T_sigma_scale_capacity_formula_held_pending_independent_scale [P_structural_sigma_scale_capacity_formula_held_pending_independent_scale].
    "apf.ew_branch_incidence_density",  # v24.3.174 - EW SSB branch incidence-density GEOMETRY [P_structural]: cone(dρ:H_R->g/k) node count N=7 (K3-additive over disjoint supports H_R(+)g/k), gauge-symmetric incidence S=12 (4 generators equal-weight x 3 broken), density 12/7. Capacity lift v_H=v_floor*12/7=246.21 GeV CONDITIONAL on single-currency canonical enforcement cost (f=k, A1+A2); cross-type f=k=1 needs a derived enforcement potential the bank lacks (PLEC has only kinetic realignment cost). vev value stays [C]; denominator+weights symmetry-forced (K3+gauge), the residue is A1+A2 single-currency. No measured target consumed. 1 check.
    "apf.ew_planck_hierarchy_mechanism",  # v24.3.176 - EW/Planck hierarchy as bosonic root-measure capacity suppression v/M_Pl ~ d_eff^(-C_boson/2) [P_structural mechanism modulo O(1); C_boson=16 vs C_total=61 mode-restriction OPEN; absolute value route-b]. 1 check. Arc v27..v33 converged 2026-05-29.
    "apf.ew_prefactor_invariance_no_go",  # v24.3.177 - EW vev O(1) prefactor invariance NO-GO [P_structural]: eta=sqrt(N_c)/(pi sqrt(C_boson)) has 3 independent carriers (color/measure/Planck); 1/pi is NOT the C_boson-mode determinant pi^-8; route fails under current stack, reduces to a missing static trace-measure invariance theorem. Absolute v_H blocked. 1 check.
    "apf.ew_static_well_factorization",  # v24.3.178 - static-well factorization principle [P_structural] (Paper-7 C_total=61 NOT auto-active for a local EW well; inactive complement cancels) + REJECTION of C_boson=16 direct route (color-singlet Higgs => gluons cancel with fermions => active sector 7-8, not 16; d_eff^-8 not native from direct restriction); revival = named bosonic-enforcement-reservoir theorem (not in corpus). 1 check.
    "apf.ew_bosonic_enforcement_reservoir",  # v24.3.179 - bosonic enforcement reservoir theorem [P_structural_under_reservoir_reading]: EW floor = pre-branch bosonic reservoir root-measure (C_boson=C_gauge+C_Higgs=12+4=16, gluons IN by capacity type, 45 fermions OUT as Grassmann); gives d_eff^-8. Disclaims local-Higgs-Hessian reading (7-8 => 16=0). Reading admissible+motivated but NOT proven forced (conditional). Prefactor + exact v_H still blocked. 1 check.
    "apf.ew_prefactor_axiom_independence",  # v24.3.180 - prefactor axiom-independence theorem [P_structural]: 4-model countermodel family (full/stripped/double-colored/reduced-Planck => v_H 246.21/142.15/426.45/49.11, all admissible under A1/A2/K3 + root-measure + 1/sqrtC + no-smuggling) proves the exact prefactor (hence exact v_H) is LOGICALLY INDEPENDENT of the current axioms; only 1/sqrt(C) is invariant; closing requires a NEW structural axiom (reservoir measure principle), not a derivation. Capstone of the prefactor line. 1 check.
    "apf.ew_floor_measure_continuation_root",  # v24.3.181 - AUDIT FINDING [P_structural]: the floor measure factor 1/(pi sqrt C_boson) = sqrt[(4pi)^-D/2] = root of the BANKED continuation-sum measure (v24.3.166, D=4-forced) at C_boson=16. Relocates the 1/pi clause from free-scalar to a banked measure (corrects v24.3.177 over-statement); residual = root-measure identification. sqrt(N_c) carrier + Planck anchor grep-audited GENUINELY ABSENT. Exact v_H still blocked. 1 check.
    "apf.ew_pre_branch_reservoir_ordering",  # v24.3.182 - order-of-operations theorem [P_structural]: the floor is the PRE-branch bosonic reservoir marginal (C_boson=16), the 12/7 lift is the POST-branch SSB cone; gluons are IN the floor because the color-singlet order parameter that would cancel them does not exist until the branch is selected (color cancellation is post-branch). Supplies the forcing MECHANISM v24.3.179 lacked; grounded in banked floor (v24.3.171) + SSB cone (v24.3.175). RESIDUAL sharpened: needs floor pre-gauge-SSB, but banked fact is y_t-free (W/Z are y_t-free yet post-SSB) -> the single remaining identification. Exponent conditional not unconditional. 1 check.
    "apf.ew_planck_anchor_gravity_consistency",  # v24.3.183 - Planck anchor FORCED by gravity-sector consistency [P_structural]: the banked Bekenstein S=A/4ell_P^2 with ell_P^2=G (T_Bek) fixes the unreduced Planck scale G^-1/2=1.22e19 = the floor anchor; the reduced-Planck countermodel D (2.4e18) is a 2nd incompatible Planck scale -> EXCLUDED by the gravity sector. The test v24.3.180 skipped. Closes the Planck clause (normalization, not magnitude=route-b); prefactor free factors 2->1; only sqrt(N_c) carrier remains. 1 check.
    "apf.ew_sqrtNc_carrier_color_triplet",  # v24.3.185 - sqrt(N_c) carrier FORCED by the physical color-triplet trace [P_structural], CLOSES the last prefactor clause. a_Y/sqrt(b)=sqrt(N_c) (y_t cancels) is the physical trace ratio: a2=Sum N_c*Tr exact over H_F=C^96 (L_normalization_coefficient [P]), SU(3)/N_c=3/triplet quarks (Theorem_R/T_gauge/T_field [P]). sqrt(N_c) is basis-invariant; color-strip (countermodel B) is a different trace functional (color-average), not a basis change -> EXCLUDED. No-go v24.3.169 preserved INVERSION-ONLY (absolute y_t still not derivable). EW floor now FULLY forced (exponent .184 + measure .181 + Planck-norm .183 + carrier this); only the absolute Planck magnitude = one external input (route-b). 1 check.
    "apf.delta_alpha_capacity_density",  # v24.3.186 - the running of alpha as capacity-counted distinction density [P_structural]: Delta-alpha = (alpha/3pi) sum N_c Q^2 [ln-window], R=N_c*sumQ^2 (colour capacity x charge-weighted distinction modes), VALIDATED EXACTLY on the leptonic sector (0.031421). Reframes the hadronic running into the EW-floor shape: native structure, one external scale (the confinement threshold, parallel to the Planck magnitude). NP residual VALUE held [C] (external threshold + nonperturbative duality violation; ~2 m_pi landing is a comparator, not target-matched). 1 check.
    "apf.planck_magnitude_single_anchor",  # v24.3.187 - the absolute Planck magnitude is the framework's ONE dimensional anchor [P_structural]. NO-GO: not derivable from dimensionless axioms (global rescaling M_Pl->lam*M_Pl leaves all dimensionless predictions invariant) -- same shape as the prefactor axiom-independence no-go (v24.3.180), one level deeper. POSITIVE: one anchor fixes BOTH the EW vev (v_H=M_Pl*sqrt(N_c)*(4pi)^-1*102^-8*(12/7)=246.22) and the cosmological constant (Lambda*G=3pi/102^61~10^-122, T10 [P]), zero free dimensionless params = the theoretical minimum; elevates T10's remark from limitation to unification. OPEN [C]: the strong-sector confinement scale (v24.3.186) is a 2nd apparent anchor -> at most TWO anchors, conjectured to collapse to ONE via dimensional transmutation Lambda_QCD=M_Pl*exp(-2pi/(b0 alpha_s(M_Pl))). Closes the gravity missing item at its honest max. v24.3.225: +T_fermion_strong_no_new_dimensional_anchor [P_structural] -- fermion+strong sectors add NO dimensional anchor (m_f=y_f*v_H, y_f dimensionless; Lambda_QCD by transmutation); SM mass spectrum rides the ONE anchor, only dimensionless mass ratios remain; dissolves 'top mass is a new scale'. 2 checks.
    "apf.confinement_scale_single_anchor",  # v24.3.188 - the confinement scale rides the SINGLE Planck anchor [P_structural], CLOSES the single-anchor [C] corollary. Lambda_QCD = M_Z*exp(-2pi/(b alpha_s)) with alpha_s(M_Z) native [P+alpha_EM] (L_alpha_s: Route A 0.1197/1.6%, Route B 0.1179/0.02%) and b native (L_beta_capacity), and M_Z = M_Pl*(native capacity number) (EW floor) -> Lambda_QCD = M_Pl*(pure number ~10^-20). The strong sector adds ZERO new dimensional anchors (alpha_s dimensionless whether [P] or [P+alpha_EM]). at-most-two-anchors -> EXACTLY ONE. nf=3 1-loop Lambda=244 MeV vs PDG ~332 (residual=known multi-loop+matching, [P+alpha_EM,+tool]); 2 m_pi=279 MeV running-floor comparator. NOT claimed: precise Lambda_QCD value, the 2 m_pi chiral-Goldstone floor. EW closed for real: one external dimensional input (absolute Planck magnitude, route-b). 1 check.
    "apf.a_mu_hvp_capacity_density",  # v24.3.189 - muon g-2 hadronic vacuum polarization as capacity-counted distinction density [P_structural]. a_mu^HVP,LO = (1/3)(alpha/pi)^2 int (ds/s) K(s) R(s) with K(s) the known QED g-2 kernel (Gourdin-de Rafael, K->m_mu^2/3s) and R=N_c*sumQ^2 the SAME source object as the hadronic running (v24.3.186). QED/EW determined; native perturbative slice ~345e-11 ~5% of a_mu^HVP,LO~6900e-11 (kernel low-energy-weighted, much thinner than Delta-alpha's ~76%) -- a reframing not a value derivation; NP bulk ~95% held [C] (universal QCD difficulty). 2025 anomaly DISSOLVED: a_mu^exp 116592070.5e-11 vs SM-lattice 116592033e-11 agree ~127 ppb; residual is ~3sigma INTERNAL dispersive-vs-lattice HVP. APF resolves no tension, claims no new physics, consumes no target. Closes RP-mu "upstream" -> source-codomain reading delivered. 1 check.
    "apf.gauge_beta_capacity_tiling",  # v24.3.190 - the abelian hypercharge beta is in the capacity ledger [P_structural]: 6|b_Y| = d_eff - C_total = 41 (SM norm, |b_Y|=41/6), a THIRD capacity-beta equation forcing N_gen=3 ((40/3)n+1=9n+14 -> n=3), independent of the SU(2)/SU(3) ones (abelian increases with n, non-abelian decrease, coincide only at n=3). Three gauge betas tile d_eff: 6(|b_3|+|b_2|+|b_Y|)=42+19+41=102. Extends L_beta_capacity to U(1). SCOPE: fixes the running RATE, NOT the absolute hypercharge coupling (the residual dimensionless input). The 1/alpha_Y(M_cross)=C_total closure (would predict alpha_s to 0.00%) is data-back-solved, held [C], NOT derived/banked. No measured coupling consumed. 1 check.
    "apf.abelian_coupling_capacity_count",  # v24.3.192 - the absolute U(1)_Y coupling is FIXED by the m=0 rank-1 collapse [P_structural], SUPERSEDING the v24.3.191 m=0 no-go. Competition matrix A=[[1,x],[x,x^2+m]] (det=m) is rank-2 for SU(3)/SU(2) (m=8/3, resolve sigma-entropy per mode -> 1/alpha_cross=(C_total/6)ln(d_eff)=S_dS/6) and RANK-1 for U(1) (m=0): a single undifferentiated mode counts capacity CHANNELS, 1/alpha_Y(M_cross)=S_dS/sigma=C_total=61 (a channel count, not a 2nd entropy scale -> respects L_sigma_intensive). With the derived crossing coupling + sin^2theta_W=3/13 this PREDICTS alpha_s(M_Z)=0.1179 to 0.00% from ZERO measured coupling (forward; alpha_s is the output, not back-solved). Gauge sector closes to ONE input (Planck magnitude); L_alpha_em "1 free param + 2 predictions" -> "0 free + 3 predictions". Same rigor level as L_coupling_capacity_id, validated by the 0.00% prediction. 1 check.
    "apf.acc_reading_selection",  # v24.3.193 - the ACC Reading-Selection Rule: one 61-slot ledger read four ways, selected by RANK (fixed-point dichotomy: rank-2 reads smeared S_dS/6, rank-1 reads bare count S_dS/sigma=C_total) + TYPE (which slots a structure supports). T_rank_field_selector (rank clause, composes T_ACC_unification + L_sigma_intensive + L_coupling_capacity_id + L_singlet_Gram + L_crossing_entropy, all [P]) + T_acc_reading_selection (top rule + four-instance table) + T_gauge_reading_dichotomy (v24.3.194 [P]: closes the abelian support-uniqueness via the channel-permutation-invariance lemma + the rank fixed-point dichotomy). Top rule [P_structural] (one open instance: EW-floor type clause); gauge arm closed to [P]; v24.3.195 +L_abelian_no_ledger_channel_structure tightens the dichotomy premise to [P]. 4 checks.
    "apf.ew_pre_branch_necessity",  # v24.3.184 - pre-branch NECESSITY theorem [P_structural]: {y_t-free floor AND C_boson=16 ledger AND separated 12/7 lift} => floor is pre-gauge-SSB reservoir, by exclusion (post-SSB+fermions y_t-dependent; post-SSB+bosonic gives 7-8!=16; exotic absolute escape killed by floor/lift staging). CLOSES the exponent d_eff^-8 unconditionally; upgrades v24.3.179 (reservoir forced) + v24.3.182 (typing forced). Only the sqrt(N_c) carrier remains open. 1 check.
    "apf.sigma_scale_yukawa_free_geometric_floor",  # v24.3.171 - the top Yukawa CANCELS in the capacity formula leading term (a_Y/sqrt(b)=sqrt(N_c), y_t-free), leaving a geometry-locked EW-scale component A*N_c ~ 144 GeV from {M_Pl,N_c,C_boson=16,d_eff=102} alone (A=M_Pl/[pi sqrt(C N_c) d_eff^(C/2)]); the only y_t-dependence is the c_R cross-term A*c_R/y_t^2 (~103 GeV at physical y_t, carries the RH-neutrino/sigma0 input). Survives the y_t no-go (leading piece never needed y_t), refines the held gate, factorizes the absolute-scale gap: 144 = geometry (open: hierarchy exponent why d_eff^C_boson) + 144->246 lift = c_R/sigma0 (open). Absolute v_H OPEN. Inputs are banked Paper-8 capacity numbers, not tuned; no measured target consumed. Value carries the unreduced-Planck convention (structure is the invariant claim). Faithful to audited-clean sibling bundle APF_ABSOLUTE_MASS_SCALE_PUSH_BUNDLE_v4. Deps: T_sigma_scale_capacity_formula_held_pending_independent_scale, T_yt_absolute_scale_not_fixable_by_normalization_no_go, L_vev_threshold_matching. 1 check: T_sigma_scale_yukawa_free_geometric_component [P_structural_sigma_scale_yukawa_free_geometric_component_modulo_planck_convention].
    "apf.sin2theta_w_OS_capacity_counting",  # v24.3.108 - APF-native sin²θ_W^OS = 2/9 via gauge+Higgs-only capacity counting (post-SSB W±+h on C_SU2H_OS = 7 modes; A_γ on C_U1_null_OS = 2 modes; canonical (7:2:9) unique among 3^8 = 6561 candidates under OSR1-OSR7). Composed with Paper 18 sin²θ_eff^ℓ = 3/13: κ_l = 27/26 = 1.038462 matches DFGRU (1906.08815) all-orders SM parametric fit to 3.2e-5 (below DFGRU's ~2e-5 noise floor). [P_structural | GH_OS_codomain] grade. Augments v5 sibling-pack derivation with 3 additional structural premises P12 (Higgs SU(2)-doublet member), P13 (charged-W SU(2)-adjoint member), P14 (charged-W counted) — gate-1 audit finding that closes v5's OSR4/OSR7 derivation gaps. Discrete Lyapunov analog: V(c) := # numeric premises violated has unique global min at canonical; k=2-swap strict descent from all 6561 starts; Boltzmann β→∞ concentration 99.4% at β=8. κ_b universality FALSIFIED (factor 1.65) — scope strictly gauge+Higgs OS sub-sector. Closure-pack lineage at bundles 203-210. 8 checks: sin2_theta_W_OS_value [P|GH_OS], MW2_over_MZ2_value [P|GH_OS], kappa_l_composed_with_paper_18 [P|GH_OS+Paper18], canonical_unique_under_OSR_enum [P_structural; actual 6561-candidate enumeration], OSR_premise_implications_mechanized [P_structural; all 6 OSR rules verify], lyapunov_V_unique_global_min [P_structural], lyapunov_k2_swap_strict_descent [P_structural], kappa_b_universality_falsified [C; scope-restriction guard]
    "apf.w_trace_pv_d0_general_momentum",  # v24.3.77 - native general-momentum spacelike box scalar D0 (completes the native scalar substrate A0/B0/C0/D0 at general momenta; prerequisite for 4-point tensor reduction); self-validating via p->0 limit + cyclic box symmetry, no external input; 4 checks
    "apf.w_trace_pv_dij_four_point",  # v24.3.78/.79 - native PV four-point (box) tensor reduction rank-1/2/3 (D1/D2/D3; D00/Dij; D00k/Dijk) on the general-momentum D0 + native triangle C0; self-validating via contraction identities (rank-1) + metric-trace relations (rank-2/3) in pure invariants, no external input; 7 checks
    "apf.w_trace_real_row_bundle_admission",
    "apf.w_trace_real_source_candidate",
    "apf.w_trace_release_attestation",
    "apf.w_trace_release_evidence_bundle",
    "apf.w_trace_release_packet_validator",
    "apf.w_trace_release_runbook",
    "apf.w_trace_residual_interpretation",
    "apf.w_trace_review_packet_validator",
    "apf.w_trace_reviewed_source_import_handoff",
    "apf.w_trace_row_bundle_to_component_sum",
    "apf.w_trace_row_schema_adapter",
    "apf.w_trace_same_input_evaluator_closeout",
    "apf.w_trace_signature_verification_adapter",
    "apf.w_trace_signed_release_replay",
    "apf.w_trace_source_acquisition_review_packet",
    "apf.w_trace_source_authority_grading",
    "apf.w_trace_source_candidate_registry",
    "apf.w_trace_standard_delta_r_extraction_worksheet",
    "apf.w_trace_standard_delta_r_payload_schema",
    "apf.w_trace_tensor_coefficient_map_scaffold",
    "apf.w_trace_terminal_state_report",
    "apf.w_trace_uncertainty_propagation",
    "apf.w_trace_v142_physics_validation_sprint_report",
    "apf.w_trace_v143_physics_deep_validation_report",
    "apf.w_trace_v144_publication_validation_report",
    "apf.w_trace_v14_physics_sprint_terminal_report",
    "apf.yang_mills_gap",
    "apf.yang_mills_md_bridge",
    "apf.photon_masslessness",  # v24.3.198 - the eps* bridge: YM gap positivity from the MD floor (1 check)
    "apf.photon_commitment_profile",  # v24.3.228 - photon slot-4 keystone: C_4 == L_irr permanent-ledger-lock [P_structural]
    "apf.ew_codomain_reading_contracts",  # v24.3.229 - EW codomain-reading contracts (4 domains, 6 forbidden swaps): guards reading a ledger quantity in the WRONG codomain (3/13 competition vs trace-route; v_H bosonic root-measure; abelian census 61 vs record 60.75; GH-OS 2/9 vs kappa_b fermion-channel). 3 checks [P_structural]: schema well-formed + home values from capacity + bank-scanning anchors-banked (9 anchors verified at grade). Cold-audited 2026-06-08. 3 checks.
    "apf.operational_completeness",  # v24.3.230 - access-partition arc: L_operational_completeness (sandwich, executable CM1/CM2 bodies at both halves) + L_local_removability (billing-locus converse of L_irr; floor == locked closure) [P_structural x2]
    "apf.gauge_quotient_ledger",  # v24.3.235-242 - quotient demand ledger arc (10 checks: 4 [P] + 6 [P_structural] incl. the UB adoption artifact) - quotient demand ledger: orbits unpinnable + record demand = quotient count + GQL-1 derived + GQL-1a reduced to GQL-1b via co-movement (4 checks, all [P_structural])
    "apf.cost_energy_identity",  # v24.3.199 - DERIVES the bridge dictionary: realignment cost = transition energy = n*eps (1 check)
    "apf.thermo_four_laws_synthesis",  # v24.3.219 - the four laws of thermodynamics as one [P] composition of 10 banked [P] lemmas (Paper 40) (1 check)
    "apf.fluctuation_response_two_faces",  # v24.3.220 - equilibrium fluctuation-response identity <dE^2>=-d<E>/dbeta on the bounded ledger [P] (1 check)
    "apf.negative_temperature_ceiling",  # v24.3.221 - FD4 ceiling creates the negative-temperature / population-inversion branch [P] (1 check)
    "apf.yang_mills_kappa3",
    "apf.ym_quotient_ledger",
    "apf.fibration_census",  # v24.3.245 - threat-emptiness + fibration census + record-term pincer (2026-06-12)
)


# 35 architecture/engineering-only modules: register() contributes
# 0 checks BY DESIGN. Loaded by bank._load() for completeness; --bank-audit
# Bucket B filters them out so the warning surfaces only genuine misregistrations.
# v24.3.30 (2026-05-19) added 4 IE coherent-phase-regime utility modules
# (superconductivity_ie + codomain_{competition,transition_dynamics,hysteresis}).
# v24.3.37 (2026-05-19) added 6 Coherent Materials Audit Layer utility modules:
# sc_material_ledger + correlated_layer_competition + sc_material_evidence +
# coherent_materials_{discriminator,intervention_selector,protocol_compiler}.
# v24.3.38 (2026-05-19) added 2 CMAL Tier-4 sector adapter utility modules:
# coherent_materials_functional_codomain_registry (functional codomain card
# registry: 2 active cards SC + RARE_EARTH_QUANTUM_MEMORY, 5 stub-only-not-
# exported future slots) + coherent_materials_obligation_packet_adapter
# (compiles CMAL protocol cards into existing obligation_packet_meta_schema
# bound to evidence_required, target_engine CODOMAIN_SELECTION).
# v24.3.39 (2026-05-19) added 1 CMAL receipt-update-loop utility module:
# coherent_materials_receipt_update_loop closes the obligation -> receipt ->
# ledger -> discriminator -> next-obligation loop. Consumes typed receipts +
# current ledger + current obligation packet; returns updated ledger +
# reclassification + next obligation packet + preserved non-claims.
# Architecture-only; no new bank checks; depends on v24.3.37 discriminator +
# v24.3.38 obligation_packet_adapter; 8 update statuses including
# PROMOTE/HOLD_PARTIAL/DEMOTE/QUARANTINE/REQUEST_NEXT_RECEIPT.
# v24.3.40 (2026-05-19) added 2 CMAL user-facing + boundary-formalization utility modules:
# coherent_materials_casebook (10 case cards: 7 active + 3 future stubs; the
# user-facing demonstration layer translating ledger -> classification -> protocol
# -> required receipts -> promotion/demotion/quarantine into one-page cards) +
# coherent_materials_ingestion_contract (formalizes v24.3.37's "ingestion outside
# core" commitment as a typed JSON schema; defines what external tools must
# emit as APFMaterialReceipt; explicitly NOT an OPTIMADE/MaterialsProject/GNoME/
# SuperCon connector implementation).
ARCHITECTURE_ONLY_MODULES: tuple[str, ...] = (
    "apf.w_trace_native_lepton_self_energy",  # v24.3.121 - lepton chiral self-energy wrapper for R2.b; ARCHITECTURE-ONLY (no register; sibling-validation pending via R2 v3)
    "apf.coherent_materials_partner_pilot_lifecycle",  # v24.3.66 - CMAL collapse (kit+feedback+review_board+readiness+governance)
    "apf.coherent_materials_rc_certification",  # v24.3.66 - CMAL collapse (acceptance_test_harness+release_candidate_certifier)
    "apf.coherent_materials_red_team",  # v24.3.66 - CMAL collapse (adversarial+claim_fence+provenance_conflict_auditor)
    "apf.interaction_pattern_schema",  # v24.3.66 - architecture-only Pattern schema (6-field tau-tuple; Integrator Response Q4)
    "apf.codomain_competition",  # v24.3.30 - IE coherent-phase-regime; codomain competition selector
    "apf.codomain_hysteresis",  # v24.3.30 - IE coherent-phase-regime; history-state + barrier-gated transitions
    "apf.codomain_transition_dynamics",  # v24.3.30 - IE coherent-phase-regime; phase-boundary detection + transition barriers
    "apf.coherent_materials_batch_triage_runner",  # v24.3.46 - CMAL end-to-end runner composing validator + ledger-update + triage + obligation-packet emission over receipt batches
    "apf.coherent_materials_candidate_triage_kernel",  # v24.3.46 - CMAL claim-admissibility priority queue (front gate triage classifier)
    "apf.coherent_materials_casebook",  # v24.3.40 - CMAL user-facing demonstration layer; 10 case cards (7 active + 3 stub-only) translating ledger -> classification -> protocol -> receipts -> promotion-rule into one-page cards
    "apf.coherent_materials_discriminator",  # v24.3.37 - Coherent Materials Audit Layer; runtime classifier over SC + non-SC coherent-material ledgers
    "apf.coherent_materials_functional_codomain_registry",  # v24.3.38 - CMAL Tier-4 adapter; functional codomain card registry (SC + RARE_EARTH_QUANTUM_MEMORY active + 5 stub-only)
    "apf.coherent_materials_golden_receipt_benchmark",  # v24.3.46 - CMAL benchmark fixture pack (10 golden receipts covering bulk SC / resistive-only / hydride / nickelate / Pearson QM / smuggling attempts)
    "apf.coherent_materials_ingestion_contract",  # v24.3.40 - CMAL boundary-formalization; typed APFMaterialReceipt JSON schema for external tools; formalizes v24.3.37 "ingestion outside APF core" commitment without implementing connectors
    "apf.coherent_materials_intervention_selector",  # v24.3.37 - Coherent Materials Audit Layer; ranks next admissible interventions
    "apf.coherent_materials_manual_dry_run_pilot",  # v24.3.46 - CMAL human-driven pilot dry-run harness
    "apf.coherent_materials_manual_external_dry_run",  # v24.3.46 - CMAL hand-curated APFMaterialReceipt batch runner through validator + update-loop + triage + obligation-packet + trace certificates
    "apf.coherent_materials_obligation_packet_adapter",  # v24.3.38 - CMAL Tier-4 adapter; compiles protocol cards into obligation_packet_meta_schema bound to evidence_required
    "apf.coherent_materials_pilot_telemetry_schema",  # v24.3.46 - CMAL pilot pipeline; typed telemetry schema for pilot reporting
    "apf.coherent_materials_portfolio_planner",  # v24.3.46 - CMAL portfolio planning utility across active CMAL pilot lanes
    "apf.coherent_materials_protocol_compiler",  # v24.3.37 - Coherent Materials Audit Layer; compiles intervention into receipt-bearing protocol card
    "apf.coherent_materials_receipt_contract_validator",  # v24.3.46 - CMAL receipt-contract validator (external-receipt admissibility front gate)
    "apf.coherent_materials_receipt_trace_certificates",  # v24.3.46 - CMAL deterministic receipt-trace certificates binding case/result to receipt IDs + source anchors + outcomes + obligation packet IDs + non-claim guards + audit hash
    "apf.coherent_materials_receipt_update_loop",  # v24.3.39 - CMAL Tier-4 adapter; receipt-update loop (obligation -> receipt -> ledger -> discriminator -> next-obligation; 8 update statuses)
    "apf.correlated_layer_competition",  # v24.3.37 - Coherent Materials Audit Layer; correlated-layer SC codomain competition
    "apf.continuability_preservation_resolution",
    "apf.defect_composition_calculus",
    "apf.defect_domain_applications",
    "apf.defect_falsifier_gate_logic",
    "apf.defect_functorial_transport",
    "apf.defect_global_descent_kernel",
    "apf.defect_master_integration",
    "apf.defect_observable_signatures",
    "apf.defect_obstruction_cohomology",
    "apf.defect_scale_flow",
    "apf.defect_transition_dynamics",
    "apf.defect_variational_principle",
    "apf.engine_dag_priming",  # v24.3.41 - Fourth Law Step D audit Finding 2 closer; DAG-priming helper
    "apf.ew_sector_closure",
    "apf.interface_solver_batch",
    "apf.interface_solver_ci_policy",
    "apf.interface_solver_contracts",
    "apf.interface_solver_report",
    "apf.interface_solver_route_adapters",
    "apf.perturbative_refinability",  # v24.3.21 - defect-calculus extension; utility module, no register()
    "apf.sc_material_evidence",  # v24.3.37 - Coherent Materials Audit Layer; SC evidence audit ladder
    "apf.sc_material_ledger",  # v24.3.37 - Coherent Materials Audit Layer; material ledger schema validator
    "apf.superconductivity_ie",  # v24.3.30 - IE coherent-phase-regime; SC admissibility margin + audit ladder evaluator
)


# 4 standalone-lemma modules under apf/standalone/.
# Don't use register(registry) contract; enumerated by verify_all for scorecard
# but NOT in bank._MODULE_PATHS.
STANDALONE_LEMMA_MODULES: tuple[str, ...] = (
    "apf.standalone.L_Cauchy_uniqueness",
    "apf.standalone.L_CKM_resolution_limit",
    "apf.standalone.phase1_seesaw_closure",
    "apf.standalone.phase5_theorem_R_audit",
)


# 2 modules with non-standard register() signature.
# bank._load() silently skips these via try/except TypeError; their checks
# are NOT in REGISTRY. Cleanup deferred to a future refactor pass.
KNOWN_REGISTER_ANOMALIES: tuple[str, ...] = (
    # Empty as of v24.3.20 (2026-05-18) — the 2 previous anomaly entries
    # (apf.evaporation_quartet + apf.l_irr_induced_polarity) were refactored
    # to use the standard register(registry) contract and moved into
    # BANK_REGISTRY_MODULES. Their 9 checks now load into REGISTRY.
)


# Production-canonical REGISTRY size after clean load. Re-derived 2026-05-18
# by simulating a full load of BANK_REGISTRY_MODULES + ARCHITECTURE_ONLY_MODULES.
# Sandbox typically returns ~6 fewer due to scipy-blocked
# apf.cmb_finite_mode_covariance; --bank-audit Bucket A surfaces this.
# v24.3.243 (2026-06-11): +1 check_T_ledger_rent_excluded [P] (operational_completeness.py)
# -- the rent exclusion / cost-kind dichotomy, consuming Paper 0 v6.2.29 loads-table row 9
# (no standing rent; falsifier (vi)); sealed-cycle derivation + cold audit 2026-06-11;
# license-class guard + placement-blindness recorded in-check. EXPECTED 3725 -> 3726.
# v24.3.245 (2026-06-12): +3 from NEW apf.fibration_census (T_b_pin_threat_empty +
# T_saturation_fibration_census + T_record_term_pincer, all [P_structural], each from a
# cold-audited 2026-06-12 reference-note cycle; named consumptions carried in-module;
# orphan-flagged with the v24.3.244 eight pending the Paper 18/42 row). EXPECTED 3734 -> 3737.
# v24.3.246 (2026-06-12): +1 from apf.operational_completeness (check_T_transition_log_residue_readable [P] -- the transition log observable at residue
# grade, consuming Paper 0 v6.2.30 loads-table row 10 (observer-reading, falsifier (vii));
# OR landed row-first per the principal's L2-observability ruling (option 2); canonical pass
# + cold audit REDUCES 2026-06-12; billing-placement-blind, join split pin/pool recorded
# in-check). EXPECTED 3737 -> 3738.
# v24.3.249 (2026-06-13, INFRA — no check delta, EXPECTED unchanged): added MODULE_TYPES
# (first-class spine/sector/extension/engineering/infra/standalone classification of all 422
# loaded modules) + modules_of_type(); crystal.py MODULE_PRESETS now DERIVE from it
# (CORE=spine, EXTENDED=+sector+extension, FULL=all, plus typed single-layer views).
EXPECTED_REGISTRY_SIZE: int = 3758  # v24.3.260 (native [P] gauge-invariant pure-gauge bosonic S constant -16.352, apf/s_parameter_pure_gauge_constant_native.py check_T_S_pure_gauge_constant_native_P [P_S_pure_gauge_constant_native_reproduction]: BFM self-energies AA/AZ/ZZ derived from DDW vertices via one uniform transverse projector, gates cross-check only; SUPERSEDES the same-session .258 [P+tool] import check, net +0). v24.3.260 +1: native m_H-dependent finite Higgs profile of S (apf/s_higgs_finite_profile_native.py check_T_S_higgs_finite_profile_native_P [P_S_higgs_finite_profile_native_reproduction]); closes the last [P+tool] piece of the EW oblique S; relative D1:D2 sign forced by an executed i-count calibrated to the native Goldstone(+1)/W-phi-mixed(-1) bubble anchors (GLOO-independent)


# Full module list for verify_all enumeration order. Order matters for
# DAG-cache populating modules (see verify_all.PRELUDE_MODULES).
# Includes KNOWN_REGISTER_ANOMALIES so verify_all can enumerate their check_*
# functions even though bank._load() can't add them to REGISTRY.

ALL_MODULES_VERIFY_ORDER: tuple[str, ...] = (
    BANK_REGISTRY_MODULES
    + ARCHITECTURE_ONLY_MODULES
    + KNOWN_REGISTER_ANOMALIES
    + STANDALONE_LEMMA_MODULES
)


# Modules that bank._load() should attempt to call register() on.
# Includes ANOMALIES so bank.py's try/except TypeError can handle them quietly
# (their checks won't enter REGISTRY but at least they're attempted).
# Restored 2026-06-07: recurring Drive-truncation of this file's derived tail.
BANK_LOAD_MODULES: tuple[str, ...] = (
    BANK_REGISTRY_MODULES
    + ARCHITECTURE_ONLY_MODULES
    + KNOWN_REGISTER_ANOMALIES
)


# =============================================================================
# MODULE_TYPES  --  first-class semantic classification of every loaded module
# (v1 heuristic classification, 2026-06-13; reviewable). Lets tooling --- the
# Enforcement Crystal presets above all --- filter by ROLE instead of by
# hand-maintained module lists, so the analysis stays interpretable as the bank
# scales. Six types:
#   spine        -- the A1 -> SM -> gravity derivation core (the CORE crystal view)
#   sector       -- quantitative physics closures (EW, YM/QCD, mass, dark, thermo, neutrino, hadronic, W-trace)
#   extension    -- recruitment / internalization / universality / crystal / quantum-structure extensions
#   engineering  -- interface-engine, defect/descent calculus, codomain transport, materials/CMAL, external-tool adapters
#   infra        -- sessions, audits, orchestration, intake/admission, vendored utilities
#   standalone   -- the standalone lemma sub-package
# Sum across types == total loaded modules (369 bank + 49 architecture + 4 standalone = 422).
# =============================================================================
VALID_MODULE_TYPES: tuple[str, ...] = ("spine", "sector", "extension", "engineering", "infra", "standalone")

MODULE_TYPES: dict[str, str] = {
    # --- spine (12) ---
    'apf.core': 'spine',
    'apf.cosmology': 'spine',
    'apf.formal_kernel': 'spine',
    'apf.foundation_inputs': 'spine',
    'apf.gauge': 'spine',
    'apf.generations': 'spine',
    'apf.gravity': 'spine',
    'apf.paper1_kernel': 'spine',
    'apf.plec': 'spine',
    'apf.spacetime': 'spine',
    'apf.unification': 'spine',
    'apf.unification_three_levels': 'spine',
    # --- sector (193) ---
    'apf.a_mu_hvp_capacity_density': 'sector',
    'apf.abelian_coupling_capacity_count': 'sector',
    'apf.acc_reading_selection': 'sector',
    'apf.acc_unification_all_p': 'sector',
    'apf.acc_unification_no_imports': 'sector',
    'apf.base_fiber_allocation': 'sector',
    'apf.bottom_msbar_export_candidate': 'sector',
    'apf.bottom_msbar_transport': 'sector',
    'apf.charged_trace_spectrum': 'sector',
    'apf.cmb_finite_mode_covariance': 'sector',
    'apf.confinement_scale_single_anchor': 'sector',
    'apf.cost_energy_identity': 'sector',
    'apf.delta_alpha_adler_m_z': 'sector',
    'apf.delta_alpha_capacity_density': 'sector',
    'apf.delta_alpha_leptonic': 'sector',
    'apf.delta_alpha_pqcd_m_z': 'sector',
    'apf.delta_rho_leading_distinction': 'sector',
    'apf.down_lepton_trace': 'sector',
    'apf.evaporation_microtransport': 'sector',
    'apf.evaporation_quartet': 'sector',
    'apf.ew_bosonic_enforcement_reservoir': 'sector',
    'apf.ew_branch_incidence_density': 'sector',
    'apf.ew_floor_measure_continuation_root': 'sector',
    'apf.ew_osw_source_transcription_families': 'sector',
    'apf.ew_planck_anchor_gravity_consistency': 'sector',
    'apf.ew_planck_hierarchy_mechanism': 'sector',
    'apf.ew_pre_branch_necessity': 'sector',
    'apf.ew_pre_branch_reservoir_ordering': 'sector',
    'apf.ew_prefactor_axiom_independence': 'sector',
    'apf.ew_prefactor_invariance_no_go': 'sector',
    'apf.ew_sector_closure': 'sector',
    'apf.ew_sqrtNc_carrier_color_triplet': 'sector',
    'apf.ew_static_well_factorization': 'sector',
    'apf.fermion_normalizers': 'sector',
    'apf.fluctuation_response_two_faces': 'sector',
    'apf.gauge_beta_capacity_tiling': 'sector',
    'apf.gauge_quotient_ledger': 'sector',
    'apf.horizon_ledger_reindexing': 'sector',
    'apf.l_irr_induced_polarity': 'sector',
    'apf.lambda_absolute': 'sector',
    'apf.mw_value_from_equilibrium_and_custodial': 'sector',
    'apf.negative_temperature_ceiling': 'sector',
    'apf.neutrino_mbb_reconciliation': 'sector',
    'apf.operational_completeness': 'sector',
    'apf.photon_commitment_profile': 'sector',
    'apf.photon_masslessness': 'sector',
    'apf.planck_magnitude_single_anchor': 'sector',
    'apf.sigma_scale_capacity_formula_gate': 'sector',
    'apf.sigma_scale_yukawa_free_geometric_floor': 'sector',
    'apf.sin2theta_eff_kappa_l_decomposition': 'sector',
    'apf.sin2theta_w_OS_capacity_counting': 'sector',
    'apf.thermal_absolute': 'sector',
    'apf.thermo_four_laws_synthesis': 'sector',
    'apf.trace_anchors': 'sector',
    'apf.trace_sector_closure': 'sector',
    'apf.up_family_trace': 'sector',
    'apf.w_os_route_terminal_closure': 'sector',
    'apf.pi_gammagamma_2l_moment_native': 'extension',
    'apf.s_parameter_native': 'extension',
    'apf.w_trace_native_bfm_photon_vp': 'extension',
    'apf.s_parameter_pure_gauge_constant_native': 'extension',
    'apf.s_higgs_finite_profile_native': 'extension',
    'apf.w_trace_BSY_one_loop_kappa_l_native_validator': 'sector',
    'apf.w_trace_acfw_candidate_preflight': 'sector',
    'apf.w_trace_acfw_delta_r_extraction_attempt': 'sector',
    'apf.w_trace_admitted_row_covariance_bridge': 'sector',
    'apf.w_trace_apf_native_one_loop_evaluator': 'sector',
    'apf.w_trace_cms_global_fit_context': 'sector',
    'apf.w_trace_component_sum_certificate': 'sector',
    'apf.w_trace_constants_source_ledger': 'sector',
    'apf.w_trace_correlated_uncertainty_model': 'sector',
    'apf.w_trace_counterterm_convention': 'sector',
    'apf.w_trace_delta_r_finite_map': 'sector',
    'apf.w_trace_delta_r_pull_diagnostics': 'sector',
    'apf.w_trace_delta_r_remainder_resolution': 'sector',
    'apf.w_trace_delta_r_route_input_evaluation': 'sector',
    'apf.w_trace_delta_r_row_extraction_closeout': 'sector',
    'apf.w_trace_delta_r_source_acquisition_matrix': 'sector',
    'apf.w_trace_delta_r_source_candidate_registry': 'sector',
    'apf.w_trace_delta_r_source_mapping': 'sector',
    'apf.w_trace_delta_r_transport_buildout': 'sector',
    'apf.w_trace_denner_diagram_coefficient_table_closeout': 'sector',
    'apf.w_trace_denner_formula_import_native_assembly': 'sector',
    'apf.w_trace_denner_sirlin_counterterm_functional': 'sector',
    'apf.w_trace_denner_sirlin_notation_map': 'sector',
    'apf.w_trace_denner_ward_identity_counterterm_import': 'sector',
    'apf.w_trace_diagram_family_numeric_evaluator_import': 'sector',
    'apf.w_trace_dizet_acquisition_instrumentation': 'sector',
    'apf.w_trace_dizet_executable_run': 'sector',
    'apf.w_trace_dizet_flag_sensitivity_covariance': 'sector',
    'apf.w_trace_dizet_internal_dr_decomposition': 'sector',
    'apf.w_trace_external_ingestion_dryrun': 'sector',
    'apf.w_trace_final_export_readiness': 'sector',
    'apf.w_trace_finite_part_evaluator_gate': 'sector',
    'apf.w_trace_finite_part_ledger': 'sector',
    'apf.w_trace_finite_part_skeleton': 'sector',
    'apf.w_trace_full_loop_derivation_closeout': 'sector',
    'apf.w_trace_import_session_log': 'sector',
    'apf.w_trace_import_session_replay': 'sector',
    'apf.w_trace_independent_delta_r_crosscheck': 'sector',
    'apf.w_trace_input_basis_ledger': 'sector',
    'apf.w_trace_input_convention_stress_test': 'sector',
    'apf.w_trace_measurement_quarantine_context': 'sector',
    'apf.w_trace_multisource_delta_r_comparison': 'sector',
    'apf.w_trace_mw_from_effective_angle': 'sector',
    'apf.w_trace_native_bosonic_gauge_self_energy': 'sector',
    'apf.w_trace_native_bosonic_photon_vp': 'sector',
    'apf.w_trace_native_bosonic_scalar_vp': 'sector',
    'apf.w_trace_native_charge_running': 'sector',
    'apf.w_trace_native_delta_r_mw_assembly': 'sector',
    'apf.w_trace_native_delta_r_uv_assembly': 'sector',
    'apf.w_trace_native_drho_top': 'sector',
    'apf.w_trace_native_ew_self_energy': 'sector',
    'apf.w_trace_native_fermion_sum_self_energy': 'sector',
    'apf.w_trace_native_fermionic_gauge_self_energy': 'sector',
    'apf.w_trace_native_finite_remainder_evaluator': 'sector',
    'apf.w_trace_native_gauge_boson_drho_uv': 'sector',
    'apf.w_trace_native_lepton_self_energy': 'sector',
    'apf.w_trace_native_os_renormalized_self_energy': 'sector',
    'apf.w_trace_native_pv_massless_safe': 'sector',
    'apf.w_trace_native_timelike_gauge_width': 'sector',
    'apf.w_trace_native_timelike_self_energy': 'sector',
    'apf.w_trace_native_two_loop_phase2_bosonic_vertex_master_anchors': 'sector',
    'apf.w_trace_native_two_loop_phase2_coefficient_output_slices': 'sector',
    'apf.w_trace_native_two_loop_phase2_coefficient_surface_no_smuggling': 'sector',
    'apf.w_trace_native_two_loop_phase2_counterterm_residue_formula_ledger': 'sector',
    'apf.w_trace_native_two_loop_phase2_current_source_coefficient_no_go': 'sector',
    'apf.w_trace_native_two_loop_phase2_delta_r_source_import': 'sector',
    'apf.w_trace_native_two_loop_phase2_ew_self_energy_assembly_gate': 'sector',
    'apf.w_trace_native_two_loop_phase2_ew_source_table_extraction': 'sector',
    'apf.w_trace_native_two_loop_phase2_ew_source_table_extraction_queue': 'sector',
    'apf.w_trace_native_two_loop_phase2_ew_tex_source_exact_extraction': 'sector',
    'apf.w_trace_native_two_loop_phase2_fermionic_vertex_reduction_ledger': 'sector',
    'apf.w_trace_native_two_loop_phase2_master_interface_router': 'sector',
    'apf.w_trace_native_two_loop_phase2_missing_terms_source_and_derivation_plan': 'sector',
    'apf.w_trace_native_two_loop_phase2_osw_deltar_connector_refusal': 'sector',
    'apf.w_trace_native_two_loop_phase2_projectors_preibp_router': 'sector',
    'apf.w_trace_native_two_loop_phase2_zfitter_comparator_guard': 'sector',
    'apf.w_trace_native_two_loop_phase2_zpole_bosonic_deltakappa_import': 'sector',
    'apf.w_trace_native_two_loop_phase2_zpole_form_factor_connector_dag': 'sector',
    'apf.w_trace_native_two_loop_sunrise_2d_finite': 'sector',
    'apf.w_trace_native_two_loop_sunrise_de': 'sector',
    'apf.w_trace_native_two_loop_sunset': 'sector',
    'apf.w_trace_native_two_loop_tadpole': 'sector',
    'apf.w_trace_native_two_loop_tier1_status': 'sector',
    'apf.w_trace_native_two_loop_two_point': 'sector',
    'apf.w_trace_native_two_loop_two_point_bft_dst': 'sector',
    'apf.w_trace_native_two_loop_two_point_euclidean_master': 'sector',
    'apf.w_trace_native_uv_cancellation_stage4': 'sector',
    'apf.w_trace_native_uv_pole': 'sector',
    'apf.w_trace_native_zll_R2_counterterm_pieces': 'sector',
    'apf.w_trace_native_zll_kappa_l_oblique': 'sector',
    'apf.w_trace_native_zll_vertex_form_factors': 'sector',
    'apf.w_trace_onshell_transport': 'sector',
    'apf.w_trace_physical_export_lock': 'sector',
    'apf.w_trace_physics_source_stop_condition': 'sector',
    'apf.w_trace_prediction_cluster_robustness': 'sector',
    'apf.w_trace_publication_claim_language': 'sector',
    'apf.w_trace_pv_c0_general_momentum': 'sector',
    'apf.w_trace_pv_cij_three_point': 'sector',
    'apf.w_trace_pv_d0_general_momentum': 'sector',
    'apf.w_trace_pv_derivative_two_point': 'sector',
    'apf.w_trace_pv_dij_four_point': 'sector',
    'apf.w_trace_pv_ewwgr_bare_proper_vertex': 'sector',
    'apf.w_trace_pv_lambda_bhm_vertex': 'sector',
    'apf.w_trace_pv_scalar_integral_substrate': 'sector',
    'apf.w_trace_pv_tensor_reduction': 'sector',
    'apf.w_trace_pv_timelike_three_point': 'sector',
    'apf.w_trace_pv_timelike_three_point_tensor': 'sector',
    'apf.w_trace_pv_timelike_three_point_tensor_rank2': 'sector',
    'apf.w_trace_pv_timelike_two_point': 'sector',
    'apf.w_trace_real_source_candidate': 'sector',
    'apf.w_trace_release_attestation': 'sector',
    'apf.w_trace_release_evidence_bundle': 'sector',
    'apf.w_trace_release_packet_validator': 'sector',
    'apf.w_trace_release_runbook': 'sector',
    'apf.w_trace_residual_interpretation': 'sector',
    'apf.w_trace_review_packet_validator': 'sector',
    'apf.w_trace_reviewed_source_import_handoff': 'sector',
    'apf.w_trace_row_bundle_to_component_sum': 'sector',
    'apf.w_trace_same_input_evaluator_closeout': 'sector',
    'apf.w_trace_signed_release_replay': 'sector',
    'apf.w_trace_source_acquisition_review_packet': 'sector',
    'apf.w_trace_source_authority_grading': 'sector',
    'apf.w_trace_source_candidate_registry': 'sector',
    'apf.w_trace_standard_delta_r_extraction_worksheet': 'sector',
    'apf.w_trace_tensor_coefficient_map_scaffold': 'sector',
    'apf.w_trace_terminal_state_report': 'sector',
    'apf.w_trace_uncertainty_propagation': 'sector',
    'apf.w_trace_v142_physics_validation_sprint_report': 'sector',
    'apf.w_trace_v143_physics_deep_validation_report': 'sector',
    'apf.w_trace_v144_publication_validation_report': 'sector',
    'apf.w_trace_v14_physics_sprint_terminal_report': 'sector',
    'apf.yang_mills_gap': 'sector',
    'apf.yang_mills_kappa3': 'sector',
    'apf.yang_mills_md_bridge': 'sector',
    'apf.ym_quotient_ledger': 'sector',
    'apf.yt_absolute_scale_normalization_no_go': 'sector',
    # --- extension (25) ---
    'apf.admissible_representation_stack': 'extension',
    'apf.class_transition': 'extension',
    'apf.closed_world_completeness': 'extension',
    'apf.continuability_preservation_resolution': 'extension',
    'apf.continuation_sum_measure': 'extension',
    'apf.critical_slack': 'extension',
    'apf.crystal': 'extension',
    'apf.crystal_metrics': 'extension',
    'apf.extensions': 'extension',
    'apf.fractional_reading': 'extension',
    'apf.horizon_joint_bridge': 'extension',
    'apf.i4_composition': 'extension',
    'apf.internalization': 'extension',
    'apf.internalization_geo': 'extension',
    'apf.kappa_int_bounds': 'extension',
    'apf.lambda_operator_derivation': 'extension',
    'apf.majorana': 'extension',
    'apf.perturbative_refinability': 'extension',
    'apf.phase_14d3_completions': 'extension',
    'apf.quantum_admissibility': 'extension',
    'apf.quantum_operator_derivation': 'extension',
    'apf.recruitment': 'extension',
    'apf.subspace_functors': 'extension',
    'apf.unification_projection_essentiality': 'extension',
    'apf.universality_forcing': 'extension',
    # --- engineering (137) ---
    'apf.arch_defect_calculus_internal_identity_real_adapter': 'engineering',
    'apf.arch_interface_engine_operational_internal_identity_real_adapter': 'engineering',
    'apf.arch_rdfi_kernel_internal_identity_real_adapter': 'engineering',
    'apf.artifact_to_route_payload_adapter': 'engineering',
    'apf.bec_codomain_adapter': 'engineering',
    'apf.bottom_msbar_rundec_real_adapter': 'engineering',
    'apf.bottom_pole_obstruction_real_adapter': 'engineering',
    'apf.charged_lepton_pole_real_adapter': 'engineering',
    'apf.charged_lepton_qed_real_adapter': 'engineering',
    'apf.charm_msbar_rundec_real_adapter': 'engineering',
    'apf.charm_pole_obstruction_real_adapter': 'engineering',
    'apf.claim_dispatcher_multi_engine': 'engineering',
    'apf.claim_to_interface_graph_compiler': 'engineering',
    'apf.codomain_competition': 'engineering',
    'apf.codomain_hysteresis': 'engineering',
    'apf.codomain_selection_engine': 'engineering',
    'apf.codomain_transition_dynamics': 'engineering',
    'apf.codomain_transport_schema': 'engineering',
    'apf.coherent_materials_casebook': 'engineering',
    'apf.coherent_materials_discriminator': 'engineering',
    'apf.coherent_materials_functional_codomain_registry': 'engineering',
    'apf.coherent_materials_golden_receipt_benchmark': 'engineering',
    'apf.coherent_materials_intervention_selector': 'engineering',
    'apf.coherent_materials_manual_dry_run_pilot': 'engineering',
    'apf.coherent_materials_manual_external_dry_run': 'engineering',
    'apf.coherent_materials_obligation_packet_adapter': 'engineering',
    'apf.coherent_materials_partner_pilot_lifecycle': 'engineering',
    'apf.coherent_materials_pilot_telemetry_schema': 'engineering',
    'apf.coherent_materials_portfolio_planner': 'engineering',
    'apf.coherent_materials_protocol_compiler': 'engineering',
    'apf.coherent_materials_rc_certification': 'engineering',
    'apf.coherent_materials_receipt_trace_certificates': 'engineering',
    'apf.coherent_materials_receipt_update_loop': 'engineering',
    'apf.correlated_layer_competition': 'engineering',
    'apf.cosmogenesis_t1_t4_quartet_real_adapter': 'engineering',
    'apf.dark_apf2_real_adapter': 'engineering',
    'apf.dark_modified_gravity_obstruction_real_adapter': 'engineering',
    'apf.dark_particle_id_obstruction_real_adapter': 'engineering',
    'apf.dark_posterior_certifier': 'engineering',
    'apf.dark_posterior_real_adapter': 'engineering',
    'apf.dark_w2_a_background_real_adapter': 'engineering',
    'apf.defect_calculus_engine': 'engineering',
    'apf.defect_composition_calculus': 'engineering',
    'apf.defect_domain_applications': 'engineering',
    'apf.defect_falsifier_gate_logic': 'engineering',
    'apf.defect_functorial_transport': 'engineering',
    'apf.defect_global_descent_kernel': 'engineering',
    'apf.defect_master_integration': 'engineering',
    'apf.defect_observable_signatures': 'engineering',
    'apf.defect_obstruction_cohomology': 'engineering',
    'apf.defect_scale_flow': 'engineering',
    'apf.defect_transition_dynamics': 'engineering',
    'apf.defect_variational_principle': 'engineering',
    'apf.descent_exactness': 'engineering',
    'apf.descent_obstruction_calculus': 'engineering',
    'apf.evaporation_e1_e4_quartet_real_adapter': 'engineering',
    'apf.ew_counterterm_uncertainty_protocol': 'engineering',
    'apf.ew_dizet_real_adapter': 'engineering',
    'apf.ew_trace_scheme_transport_certifier': 'engineering',
    'apf.ew_trace_to_scheme_real_adapter': 'engineering',
    'apf.gauge_fiber_route_classifier': 'engineering',
    'apf.gravity_bianchi_rigidity_real_adapter': 'engineering',
    'apf.gravity_gr_limit_full_close_real_adapter': 'engineering',
    'apf.gravity_ringdown_capacity_schema_real_adapter': 'engineering',
    'apf.horizon_fiber_cost_classifier': 'engineering',
    'apf.initial_obstruction_classifier': 'engineering',
    'apf.interaction_pattern_schema': 'engineering',
    'apf.interface_atlas': 'engineering',
    'apf.interface_engine_close_primitives': 'engineering',
    'apf.interface_kinematic_holonomy_diagnostics': 'engineering',
    'apf.interface_kinematic_invariants': 'engineering',
    'apf.interface_kinematic_phase_space_atlas': 'engineering',
    'apf.interface_kinematic_solver': 'engineering',
    'apf.interface_kinematics_composition': 'engineering',
    'apf.interface_kinematics_engine': 'engineering',
    'apf.interface_kinematics_order_defects': 'engineering',
    'apf.interface_movement_graph_repair_planner': 'engineering',
    'apf.interface_repair_closure_simulator': 'engineering',
    'apf.interface_repair_frontier_explorer': 'engineering',
    'apf.interface_repair_obligation_compiler': 'engineering',
    'apf.interface_solver_batch': 'engineering',
    'apf.interface_solver_ci_policy': 'engineering',
    'apf.interface_solver_descent_bridge': 'engineering',
    'apf.interface_solver_engineering_extensions': 'engineering',
    'apf.interface_solver_report': 'engineering',
    'apf.interface_solver_route_adapters': 'engineering',
    'apf.interface_structure_discovery_engine': 'engineering',
    'apf.interface_structure_movement_graph': 'engineering',
    'apf.interface_structure_transport_ledger': 'engineering',
    'apf.kinematics_adjudication_engine': 'engineering',
    'apf.laser_coherence_codomain_adapter': 'engineering',
    'apf.light_quark_real_adapter': 'engineering',
    'apf.magnetism_codomain_adapter': 'engineering',
    'apf.neutrino_mbb_reconciliation_real_adapter': 'engineering',
    'apf.obligation_packet_meta_schema': 'engineering',
    'apf.obstruction_dynamics': 'engineering',
    'apf.obstruction_repair_normal_form': 'engineering',
    'apf.payload_batch_certification_runner': 'engineering',
    'apf.representation_descent_engine': 'engineering',
    'apf.representation_descent_full_integration': 'engineering',
    'apf.representation_descent_kernel': 'engineering',
    'apf.route_certification_starter_suite': 'engineering',
    'apf.route_certification_workbench': 'engineering',
    'apf.sc_material_evidence': 'engineering',
    'apf.sc_material_ledger': 'engineering',
    'apf.sin2theta_eff_bsy_real_adapter': 'engineering',
    'apf.sin2theta_w_mass_ratio_identity_real_adapter': 'engineering',
    'apf.sin2theta_w_source_identity_real_adapter': 'engineering',
    'apf.superconductivity_codomain_adapter': 'engineering',
    'apf.superconductivity_ie': 'engineering',
    'apf.superfluidity_codomain_adapter': 'engineering',
    'apf.synchronization_codomain_adapter': 'engineering',
    'apf.top_msr_R_star_real_adapter': 'engineering',
    'apf.top_msr_r_evolution_real_adapter': 'engineering',
    'apf.top_pole_mc_obstruction_real_adapter': 'engineering',
    'apf.topological_order_codomain_adapter': 'engineering',
    'apf.trace_scheme_transport': 'engineering',
    'apf.trace_to_scheme_transport_theorem': 'engineering',
    'apf.trace_transport_completion': 'engineering',
    'apf.trace_transport_composition': 'engineering',
    'apf.trace_transport_ledger': 'engineering',
    'apf.trace_transport_routes': 'engineering',
    'apf.w_trace_candidate_payload_attempt': 'engineering',
    'apf.w_trace_delta_r_component_payload': 'engineering',
    'apf.w_trace_delta_r_source_extraction_protocol': 'engineering',
    'apf.w_trace_external_source_adapter': 'engineering',
    'apf.w_trace_native_two_loop_phase2_ew_diagram_coefficient_derivation_engine_scaffold': 'engineering',
    'apf.w_trace_native_two_loop_phase2_ibp_reduction_engine_tier0': 'engineering',
    'apf.w_trace_next_payload_requirements': 'engineering',
    'apf.w_trace_numeric_source_adapter': 'engineering',
    'apf.w_trace_payload_fixture': 'engineering',
    'apf.w_trace_payload_import_cli': 'engineering',
    'apf.w_trace_payload_source_pack': 'engineering',
    'apf.w_trace_payload_template_pack': 'engineering',
    'apf.w_trace_row_schema_adapter': 'engineering',
    'apf.w_trace_signature_verification_adapter': 'engineering',
    'apf.w_trace_standard_delta_r_payload_schema': 'engineering',
    # --- infra (51) ---
    'apf._optimize_vendored': 'infra',
    'apf.anti_fitting_provenance_audit': 'infra',
    'apf.aps': 'infra',
    'apf.capacity_coarse_grain_experiments': 'infra',
    'apf.cfts_red_team_audit': 'infra',
    'apf.coherent_materials_batch_triage_runner': 'infra',
    'apf.coherent_materials_candidate_triage_kernel': 'infra',
    'apf.coherent_materials_ingestion_contract': 'infra',
    'apf.coherent_materials_receipt_contract_validator': 'infra',
    'apf.coherent_materials_red_team': 'infra',
    'apf.dark_empirical_posterior_admission_contract': 'infra',
    'apf.dark_mcmc_posterior_lane_admission': 'infra',
    'apf.dark_profile_likelihood_lane_admission': 'infra',
    'apf.dark_profile_mcmc_shared_contract': 'infra',
    'apf.engine_dag_priming': 'infra',
    'apf.ew_codomain_reading_contracts': 'infra',
    'apf.ew_osw_numerical_assembly_harness': 'infra',
    'apf.ew_osw_reviewed_formula_evaluator_harness': 'infra',
    'apf.fibration_census': 'infra',
    'apf.globalization_promotion_gate': 'infra',
    'apf.interface_dark_posterior_evidence_intake': 'infra',
    'apf.interface_evidence_rerun_controller': 'infra',
    'apf.interface_ew_counterterm_uncertainty_intake': 'infra',
    'apf.interface_intelligence_CI_orchestrator': 'infra',
    'apf.interface_intelligence_E2E_artifact_pipeline': 'infra',
    'apf.interface_intelligence_engineering_command_center': 'infra',
    'apf.interface_intelligence_failure_triage_assistant': 'infra',
    'apf.interface_intelligence_live_smoke_harness': 'infra',
    'apf.interface_intelligence_post_install_acceptance_auditor': 'infra',
    'apf.interface_intelligence_registry_bridge': 'infra',
    'apf.interface_intelligence_release_manifest': 'infra',
    'apf.interface_intelligence_reviewer_reporter': 'infra',
    'apf.interface_live_blocker_work_queue': 'infra',
    'apf.interface_solver_contracts': 'infra',
    'apf.killed_rivals': 'infra',
    'apf.red_team': 'infra',
    'apf.representation_descent_application_harness': 'infra',
    'apf.representation_descent_kernel_adversarial_audit': 'infra',
    'apf.session_cosmo_update': 'infra',
    'apf.session_delta_pmns': 'infra',
    'apf.session_nnlo': 'infra',
    'apf.session_qg': 'infra',
    'apf.session_v63c': 'infra',
    'apf.supplements': 'infra',
    'apf.validation': 'infra',
    'apf.w_trace_delta_r_comparison_harness': 'infra',
    'apf.w_trace_dizet_row_admission_covariance': 'infra',
    'apf.w_trace_e2e_import_pipeline_manifest': 'infra',
    'apf.w_trace_native_two_loop_phase2_ew_coefficient_ledger_audit': 'infra',
    'apf.w_trace_native_two_loop_phase2_p_plus_ibp_tool_admission_policy': 'infra',
    'apf.w_trace_real_row_bundle_admission': 'infra',
    # --- standalone (4) ---
    'apf.standalone.L_CKM_resolution_limit': 'standalone',
    'apf.standalone.L_Cauchy_uniqueness': 'standalone',
    'apf.standalone.phase1_seesaw_closure': 'standalone',
    'apf.standalone.phase5_theorem_R_audit': 'standalone',
}

def modules_of_type(*kinds: str) -> tuple[str, ...]:
    """Return the loaded modules whose MODULE_TYPES classification is in ``kinds``."""
    return tuple(m for m, t in MODULE_TYPES.items() if t in kinds)
