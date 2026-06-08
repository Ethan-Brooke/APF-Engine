"""APF v24.3.192 -- Admissibility Physics Framework.

3675 bank-registered checks. Zero free dimensionless parameters (one dimensional anchor: the Planck magnitude, equivalently the size of the de Sitter universe).

Current trace-sector status: APF_TRACE/W_TRACE closure is locally banked at [P_local]. Trace-to-scheme transport is bank-staged at [P_boundary] and the trace-to-scheme export iff theorem is banked at [P_transport_theorem]; the transport-ledger architecture is banked at [P_ledger]; route classification is banked at [P_route]; ordered route composition is banked at [P_composition]; the terminal physical-export gate is banked at [P_completion_gate]; the W_TRACE on-shell route contract is banked at [P_w_trace_contract]; the W input-basis ledger is banked at [P_w_input_basis_ledger]; the W constants-source ledger is banked at [P_w_constants_source_ledger]; the W Delta_r/finite-correction symbolic map is banked at [P_w_delta_r_symbolic_map]; the W finite-part component ledger is banked at [P_w_finite_part_ledger] with an APF-anchor Delta_r target; the W independent finite-part evaluator gate is banked at [P_w_finite_part_evaluator_gate]; the W finite-part symbolic component algebra is banked at [P_w_finite_part_skeleton]; the W numerical-source adapter is banked at [P_w_numeric_source_adapter]; the W payload fixture/table harness is banked at [P_w_payload_fixture]; and the W independent payload source-pack gate is banked at [P_w_payload_source_pack]; the W external finite-part source-pack adapter is banked at [P_w_external_source_adapter]; the W external ingestion dry-run/parser fixtures are banked at [P_w_external_ingestion_dryrun]; and the W real external source candidate gate is banked at [P_w_real_source_candidate_gate]. Actual numerical finite-part payloads, component-sum certification, covariance/uncertainty propagation, and physical W transport remain open. The W physical export lock/release predicate is banked at [P_w_physical_export_lock] and remains locked until all release certificates are supplied. The W on-shell counterterm-convention certificate is banked at [P_w_counterterm_convention_certificate]; numerical counterterm values, independent finite-part rows, component-sum certification, covariance/uncertainty propagation, and physical W export remain open. The W real finite-part row schema / counterterm-value adapter is banked at [P_w_row_schema_adapter]. The W real row-bundle admission report gate is banked at [P_w_real_row_bundle_admission]; the shipped bundle is empty by default, so real rows, component-sum certification, covariance/uncertainty propagation, and physical W export remain open. The W row-bundle-to-component-sum bridge is banked at [P_w_row_bundle_sum_bridge]. The W admitted-row covariance bridge is banked at [P_w_admitted_row_covariance_bridge]; the W final export readiness aggregator is banked at [P_w_final_export_readiness_aggregator]; the W payload import CLI loader, payload template pack, source-candidate registry, source-acquisition review packet, review-packet validator, reviewed-source import handoff, import-session log, import-session replay, E2E import pipeline manifest, and release runbook, release-packet validator, and signed-attestation / immutable-manifest digest layer are banked through [P_w_release_attestation_manifest_digest]. The W standard electroweak Delta_r source-mapping pivot is banked at [P_w_delta_r_source_mapping], shifting source acquisition to standard Delta_r total/decomposition payloads before any APF eight-slot refinement. The v13.2 standard Delta_r source-candidate registry is banked at [P_w_delta_r_source_candidate_registry], naming concrete precision-prediction, on-shell-renormalization, constants, and definition-lineage candidates while admitting no real payloads. The v13.3 standard Delta_r source-extraction protocol is banked at [P_w_delta_r_source_extraction_protocol], adding a concrete extraction worksheet/validator for source notation, input scheme, digests, and anti-smuggling attestations before any candidate can become a payload. Shipped state remains empty/unadmitted, so real covariance certification, uncertainty propagation, and physical W export remain open. The v14.1 physics-source acquisition sprint is banked across ACFW preflight, Denner/Sirlin notation mapping, standard Delta_r payload schema, independent comparison harness, no-more-scaffolding stop condition, and terminal sprint report. No additional W scaffold should be added before a real reviewed standard Delta_r payload or completed extraction worksheet is supplied, unless a blocker is found. The v14.2 physics validation sprint stress-tests ACFW input conventions, adds independent DGG/GFitter Standard-Model W/Delta_r cross-checks, and banks a multisource comparison: APF/W_TRACE lies a few MeV high relative to the independent SM source cluster, within declared source uncertainty scales; physical W export remains locked. The v14.3 deep physics validation sprint adds CMS/global-fit prediction context, quarantines observed CMS/CDF W measurements as context-only, banks a correlated/conservative source-uncertainty model, and propagates Delta-r pull diagnostics; APF/W_TRACE remains a few MeV high but GREEN under conservative source pulls, with physical export still locked. The v14.4 publication-grade physics validation sprint adds source authority grading, robust cluster stress tests, residual interpretation, paper-safe claim language, and a terminal publication-readiness report; APF/W_TRACE remains a few MeV high relative to independent Standard Model prediction sources under conservative pulls, with observed measurements quarantined and physical export still locked. The v15.0 W on-shell route terminal closure theorem is banked at [P_w_os_route_terminal_closure]: the route is closed as a theorem/obstruction certificate, while physical W export remains open until admitted real finite-part rows, component-sum certification, covariance certification, and uncertainty propagation are supplied.

v7.3 (2026-04-28 Phase 22b): codebase landing of Paper 5 Supplement v5.1
  quantum-structure framework.  New module apf/quantum_admissibility.py
  with six bank-registered checks: check_T_branch_taxonomy_inclusions
  (Lemmas 4.5/4.6 of Paper 5 v5.1 supplement -- the inclusions
  SepAdm => SepStr and IJCStr => IJCAdm forced by the branch-taxonomy
  split, with strict separation SepStr =/=> SepAdm certified on the
  capacity-limited witness so capacity-only failures are not mislabeled
  as standard quantumness); check_T_kappa_Bool_minimum (Lemma 1036,
  finite Boolean-defender minimum is attained on any finite candidate
  lattice); check_T_capacity_lower_bound_certificate (Corollary 1230,
  the universal infeasibility certificate -- kappa_Bool > C entails
  IJCPres branch / APF-infeasibility); check_T_quantum_admissibility_
  condition (Theorem 1518, IJC at a record-complete coherent interface
  produces a QAC witness with strictly positive Boolean record-locking
  preservation distortion); check_T_field_selection_complex (Theorem
  2907 + Lemma 2856, complex field selected uniquely among R/C/H by
  APF-complete composite accounting parameter-counting Delta_R > 0,
  Delta_C = 0, Delta_H < 0; verified on all (n, m) in [2, 5]^2);
  check_T_Born_trace_rule (Corollary 3053, every positive linear
  functional on M_n(C) effects is given by E |-> tr(rho E) for some
  density matrix rho).  Tier 4 [P_regime] (3 checks) and [P_regime
  + P_math] (3 checks).  EXPECTED_THEOREM_COUNT 434 -> 440;
  verify_all 451 -> 457; modules 24 -> 25.
  Source-of-record: Paper 5 Supplement v5.1 (field-selection scope and
  tau discipline pass, 2026-04-28), Sections 4-16.  Folder renamed
  APF_Codebase_v7.2 -> APF_Codebase_v7.3.

v7.2 (2026-04-28 Phase 22a): codebase landing of Paper 1 Supplement v7.1
  minimal-foundation framework -- the Admissible Possibility Space (APS)
  becomes the foundation object.  New module apf/aps.py with three
  bank-registered checks: check_T_APS_construction (Definition 4.1 of
  Paper 1 Supplement v7.1, structural invariants of the APS tuple);
  check_T_continuation_preorder (Definition 5.1 + Lemma 5.2, [x] preceq
  [y] iff Cont(y) subseteq Cont(x), reflexive/transitive on substrate,
  antisymmetric on quotient classes; formal root of the Paper 3
  thermodynamic arrow-of-time);
  check_T_state_distinction_ledger_induced (Lemma 4.2, physical states,
  distinctions, and ledgers all induced from APS data, not posited
  alongside it).  Tier 4 [P_structural].  EXPECTED_THEOREM_COUNT 431 ->
  434; verify_all 448 -> 451; modules 23 -> 24.
  Source-of-record: Paper 1 Supplement v7.1 (review-response edition,
  2026-04-28).  Folder renamed APF_Codebase_v7.1 -> APF_Codebase_v7.2.

The framework's referent -- admissibility as a physical quantity -- is named in
Paper 0 v4.0 Ch 1 (The Referent). The referent's finiteness clause (A1: at every
causally connected region, admissibility is finite) plus its three constitutive
coherence conditions (MD: positive cost floor; A2: argmin selection; BW: cost-
spectrum non-degeneracy), packaged variationally as the Principle of Least
Enforcement Cost (PLEC), generate the Standard Model and cosmological structure
with zero free dimensionless parameters (one dimensional anchor).

v7.1 (2026-04-26 Phase 21): inseparable-IJC bridge premise.
  Strengthened IJC Dichotomy at the substrate-factorizability level with paired
  witnesses (Sep / IJC). Branch (Sep): substrate factorizes S = Q x Pi with an
  admissible commuting d_Pi defending the joint threat; algebra commutative;
  classical/hidden-variable regime. Branch (IJC): no such factorization; the
  minimum-cost sharp B-orthogonal joint defender has codespace W_* = span(cos t
  e_1 + sin t e_3, e_2) not reducing for E_d1; [E_d1, pi_W*] != 0; algebra
  noncommutative. Bridge theorem: inseparable IJC -> noncommutativity, closed
  cleanly with rotated-graph defender at the 3-4-5 angle (cos^2 t = 9/25,
  sin^2 t = 16/25). Branch (IJC) classification at quantum-capable interfaces
  empirically inherited from Bell + Kochen-Specker (parallel to Planck/lattice/
  PDG external inputs). check_T_IJC_from_partition_structure (Phase 20) flagged
  as conditional form (substrate richness + no-extension premise).
  EXPECTED_THEOREM_COUNT 430 -> 431; verify_all 447 -> 448 PASS;
  setup.py 7.0.0 -> 7.1.0; folder renamed APF_Codebase_v7.0 -> v7.1.

v7.0 (2026-04-25 LATE evening, Phase 18): Paper 1 FD1 executable witness.
  apf/paper1_kernel.py -- instantiates Paper 1 Supplement v2 Definitions FD1-FD6
  on a finite 4-element substrate carrying three distinctions (d_1, d_2,
  d_pool) with capacity C = 5 and MD floor mu* = 1. Certifies seven bedrock
  properties: FD1 substrate is set-theoretic; distinctions are binary partitions
  with positive cost; FD1 capacity in R_{>0}; A1 budget bound holds on every
  admissible state; FD2 residual budget consistent; K1+K2+K3 (forced
  additivity on disjoint supports per Paper 1 Supplement Theorem K3); SP
  (substrate faithfulness). The pre-T_embed set-theoretic counterpart to Paper
  8's formal_kernel.py (V_61 representation-theoretic witness): paper1_kernel
  certifies the bedrock; formal_kernel certifies the SM-interface
  representation built on top.
  Registers check_T_FD1_substrate_distinctions_capacity [P_structural] tier 4.
  EXPECTED_THEOREM_COUNT 423 -> 424; verify_all 440 -> 441; modules 35 -> 36.

v7.0 (2026-04-25): Phase 16 codebase rev.
  apf/formal_kernel.py    -- Theorem 1.1 executable witness (V_61 + G_SM +
                             V_Lambda uniqueness via representative irrep model;
                             registers check_T_FormalKernel_VLambda_uniqueness
                             [P_structural], tier 4).
  apf/numeric_fallback.py -- scipy-optional fallback (Paper 8 + Paper 13).
  apf/test_no_smuggling.py -- anti-smuggling test suite (9/9 pass).
  EXPECTED_THEOREM_COUNT 422 -> 423; verify_all 439 -> 440 (assuming Phase 15
  fix from 2026-04-24 is in place); modules 34 -> 35.
  Folder renamed APF_Codebase_v6.9 -> APF_Codebase_v7.0.

v6.9 (2026-04-20 late evening): interface-sector bridge pass.
  New check_T_interface_sector_bridge (tier 4, [P]) and auxiliary
  check_L_global_interface_is_horizon (tier 3, [P]) in apf/gravity.py.
  The T12 interface partition V_61 = V_local (+) V_global governs the
  T_horizon_reciprocity second-epsilon sector decomposition:
    |Sector A| = |V_61 \\ {self}| = 60,
    |Sector B| = dim V_global    = 42,
    d_eff      = 60 + 42         = 102.
  Bank 345-loaded -> 347 (matches EXPECTED_THEOREM_COUNT = 347; absorbs
  pre-existing silent -2 drift); verify_all 360 -> 362.

v6.9 (2026-04-20 afternoon): T_ACC unification pass.
  New apf/unification.py module -- the Admissibility-Capacity Ledger.
  ACC record (two scalars K, ACC = K ln d_eff), six regime projections
  (pi_T, pi_G, pi_Q, pi_F, pi_C, pi_A), three canonical-interface factories
  (acc_SM, acc_horizon, acc_quantum), five bank-registered checks:
    I1_holographic           -- S_BH = ln(dim H_horizon) = ACC_horizon.
    I2_gauge_cosmological    -- K (pi_F at SM) = K (pi_C denominator at SM).
    I3_thermo_quantum        -- S_vN(rho_max) = ln dim H = ACC.
    I4_action_thermo         -- ln Z(beta) -> ACC as beta -> 0.
    T_ACC_unification        -- composed theorem re-running I1..I4.
  Bank 342 -> 347; verify_all 355 -> 360; modules 19 -> 20.

v6.9 (2026-04-18): PLEC formalization.
  New apf/plec.py module with Regime R + five-type regime-exit taxonomy:
    Regime_R                 -- R1..R4 joint validity; PLEC well-posedness.
    Regime_exit_Type_I       -- collapse of admissible variation (saturation).
    Regime_exit_Type_II      -- minimizer nonuniqueness (branching).
    Regime_exit_Type_III     -- change of admissible class (record locking).
    Regime_exit_Type_IV      -- loss of smooth / local structure.
    Regime_exit_Type_V       -- pure representational redundancy.
  New A9_closure in apf/gravity.py unifying the Lovelock prerequisites
  A9.1..A9.5 (locality, covariance, conservation, second-order, propagation).

For full per-version changelog, see CHANGELOG.md and apf/bank.py
EXPECTED_THEOREM_COUNT docstring.
"""

__version__ = '24.3.192'

# v15.1 status: standard-Delta-r extraction worksheet banked at
# [P_w_standard_delta_r_extraction_worksheet]. The ACFW standard-total
# Delta-r source payload is reproducibly extracted and valid for comparison,
# but it is not an APF finite-part component-row bundle and cannot unlock
# physical W export.

# v15.2 status: Delta-r transport buildout banked at
# [P_w_delta_r_transport_buildout]. Closed: on-shell Delta-r <-> M_W
# calculator, analytic push-forward sensitivity, source-scale uncertainty
# translation, component-slot contract, dry covariance mechanics, and terminal
# physical-export blocker. Still open: real APF finite-part component rows,
# real component-sum certificate, real covariance, and export uncertainty.


# v15.3 status: Delta-r component-payload worksheet banked at
# [P_w_delta_r_component_payload_worksheet]. Closed: dominant standard
# decomposition proxies for Delta alpha and top/rho, source-total remainder
# isolation, row-level obstruction, and paper-ready component ledger. Still
# open: reviewed APF finite-part bundle, covariance, export uncertainty, and
# physical W export.

# v15.4 status: Delta-r remainder-resolution worksheet banked at
# [P_w_delta_r_remainder_resolution]. The source/APF Delta-r gap is localized
# to the unresolved finite-remainder sector after the same Delta-alpha and
# top-rho source proxies are removed. Named acquisition buckets are closed;
# physical W export remains locked pending reviewed numerical bucket rows,
# component-sum certification, covariance, and uncertainty pushforward.

# v15.5 status: Delta-r source-acquisition matrix banked at
# [P_w_delta_r_source_acquisition_matrix]. Reviewed electroweak source
# families are mapped to every unresolved finite-remainder bucket, but no
# numerical APF finite-part row bundle, component-sum certificate, covariance,
# or export uncertainty certificate is admitted. Physical W export remains
# locked.

# v15.7 status: Delta-r route-input evaluation with covariance propagation banked after
# v15.6 status: Delta-r row-extraction closeout banked at
# [P_w_delta_r_row_extraction_closeout]. ACFW Table 1 has been extracted as
# an eight-row reviewed source-local Delta-r component table. This moves the
# W route past pure source-location, but physical export remains locked because
# the rows are evaluated at the ACFW source point, not the APF_TRACE route input
# point, and no APF same-input row admission, covariance, or export uncertainty
# certificate is supplied.


# v15.8 status: same-input evaluator terminal closeout banked at
# [P_w_same_input_evaluator_terminal_closeout]. The W route is closed as a
# terminal publication-safe route closeout: source-local rows, model-limited
# APF-route row-shape transfer, and covariance propagation are banked; physical
# W export remains locked behind REVIEWED_PER_ROW_SAME_INPUT_EVALUATOR_WITH_COVARIANCE.

# v16.2 status: DIZET flag-sensitivity and covariance worksheet banked at
# [P_w_trace_dizet_flag_sensitivity_covariance]. Reviewed same-input total
# evaluator remains closed; broad DIZET flag/input scan and covariance
# pushforward are closed; APF row-decomposition/covariance protocol and
# physical W export remain blocked.


# v16.3 status: DIZET internal Delta-r decomposition instrumentation banked at
# [P_w_trace_dizet_internal_dr_decomposition]. SEARCH/NEWDR internals expose
# DR, DRBIG, DRREM, DR1FER/DR1BOS, Delta-alpha, QCD, rho, and NEWDR remainder
# variables at the APF same-input deck. This upgrades the W route with a real
# implementation-local decomposition snapshot, but physical W export remains
# blocked because these variables are not reviewed APF finite-part component
# rows with row covariance and an export uncertainty protocol.

# v16.5 status: full electroweak-loop derivation closeout banked at
# [P_w_trace_full_loop_derivation_closeout]. W remains an export candidate by
# reviewed same-input DIZET transport plus admitted row covariance; APF-native
# full loop derivation remains open behind APF_NATIVE_COUNTERTERM_AND_LOOP_INTEGRAL_EVALUATOR.

# v16.6 status: APF-native one-loop Delta-r evaluator scaffold banked at
# [P_w_trace_apf_native_one_loop_evaluator_scaffold]. Closed: on-shell
# algebra, leading top-rho analytic branch, finite-remainder gap accounting,
# and preservation of W export-candidate status. Still open: APF-native finite
# remainder/counterterm evaluator and two-loop/higher-order stack.

# v16.7 status: native finite-remainder evaluator target banked at
# [P_w_trace_native_finite_remainder_evaluator_target]. The exact same-input
# finite/counterterm target is closed as a reviewed-code realization and APF
# target functional; APF-native Denner/Sirlin counterterm functions remain open.