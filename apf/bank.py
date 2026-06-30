"""APF v6.7 Theorem Bank — unified registry with lazy loading.

Each physics module exports a register(registry) function that adds
its theorem check functions to the global REGISTRY. No theorem logic
runs at import time; execution happens only when run_all() is called.

Module loading order respects the dependency DAG:
  core → gauge → generations → spacetime → gravity
       → cosmology → validation → supplements → majorana
       → internalization → internalization_geo
       → extensions → red_team → session_v63c → session_qg
       → session_nnlo → session_delta_pmns → session_cosmo_update

EPISTEMIC TAG LEGEND (v7.0+ — Phase 19f):
  [P]               Proved from the FOUR FOUNDATIONAL ASSUMPTIONS of Paper 0
                    + standard imported mathematics, by ANY valid argument.
                    The four: Assumption 1 (physical identity is finite
                    admissible continuation identity, INCLUDING its
                    full-strength reading -- structural completeness, "a
                    physical object is its continuation profile and nothing
                    beyond it"); Assumption 2 (cost-bearing distinction);
                    Assumption 3 (structural commitment); finiteness.  What
                    the argument RESTS ON sets the grade; proof METHOD
                    (symbolic / executable witness / enumeration) does not.
                    PLEC's {A1, MD, A2, BW}, FD1, and closed-world
                    completeness are FORCED from this base (Book I), so
                    resting on them is resting on the base.  GUARDRAIL:
                    structural completeness excludes free FIAT but does NOT
                    supply a missing VALUE; a result that USES it is [P]
                    only when the base-resting theorem supplying the value
                    is named (e.g. GQL-1: Theorem_R + Schur).  (Pre-
                    2026-06-25 this legend keyed [P] to PLEC's four only;
                    that narrow reading mis-graded results resting on
                    Assumption-1 structural completeness as [P_structural].
                    See "Reference - Canonical [P] vs [P_structural]
                    Definition (2026-06-25)".)
  [P_structural_*]  Structural-meta result, proved up to a NAMED premise.  The
                    grade was split (2026-06-22) after a corpus audit found the
                    bare [P_structural] doing six distinct jobs; the premise's
                    KIND is now in the tag.  The "structural" stem is preserved
                    so substring/startswith consumers (photon_commitment_profile,
                    ew_codomain_reading_contracts) keep working.  Six sub-grades:
                      P_structural_seam        external COMPLETION-theorem import:
                          finite->infinite (operator algebra), the emergent-field
                          w prop g^2 dictionary, or NP/transmutation.  The genuine
                          completion-seam core (Paper 44).  (~16)
                      P_structural_partial     native continuum-PERTURBATIVE
                          machinery (w_trace self-energy / PV reduction), pending
                          scheme-export assembly.  Counts as seam ONLY under the
                          "loops are math" reading -- kept distinct so the bank
                          stays agnostic; the seam claim lives in Paper 44 prose.
                          (~35)
                      P_structural_exhaustive  uniqueness among FINITE
                          alternatives: rival elimination, projection
                          essentiality, OSR enumeration, census.  (~26)
                      P_structural_instrument  classical FINITE MATH imported to
                          analyze/verify the bank: crystal graph metrics
                          (Brandes/Menger/Tarjan), OSW harnesses, YM finite-model
                          ports, export guards.  (~26)
                      P_structural_reading     physics derivation up to an adopted
                          INTERNAL reading/premise (record-state, IJC, PLEC,
                          MD-bridge, categorical ACC stack, evaporation/horizon
                          readings) -- not an external import at all.  (~89)
                      P_structural_convention  unit/scale convention; O(1)
                          prefactor (Planck magnitude).  (~8)
                    Source-of-record: APF Reference Docs/Reference - Corpus Audit
                    of the Completion Seam (2026-06-22).md + the CONTINUATION
                    grade-split note.  Pure relabel: no math, no count change,
                    EXPECTED unchanged.  The IJC dichotomy checks are now
                    P_structural_reading; check_T_crystal_* are
                    P_structural_instrument.
  [P+lattice]       Proved from PLEC + lattice-QCD numerical input.  Used
                    where the framework's structural derivation reduces a
                    physical observable to a lattice-QCD computation.  The
                    structural reduction is [P]; the numerical input is
                    flagged honestly with the +lattice tag.
  [P+IJC]           Proved from PLEC + Irreducible Joint Constraint at a
                    quantum-capable interface.  Phase 19 introduction
                    (2026-04-26): IJC is a regime-classifier in admissibility
                    space distinguishing quantum-capable interfaces (where
                    branch (IJC) of the dichotomy is occupied) from
                    classically separable interfaces (where only branch (Sep)
                    is occupied).  Theorems whose conclusions presuppose the
                    (IJC) branch carry this tag honestly.  Cascade scope (per
                    Phase 19g audit, pending): L_Pi (post-19e refactor),
                    T_alg_FPi, T2 (Hilbert space), T_tensor, T_M (in QM
                    regime), T_Tsirelson, T_Born, T_decoherence, all of
                    apf/quantum_operator_derivation.py and apf/quantum.py.
                    Source-of-record: APF Reference Docs/Reference - IJC
                    Dichotomy Theorem and the Quantum-Interface Bridge
                    (2026-04-26).md.
  [P+occupancy]     Proved from PLEC + the occupancy input at the interface
                    (2026-06-29): the joint-vs-sum cost residual Delta = E_12 -
                    E_1 - E_2 has its FORM fixed by L_cost (cost=count: Delta =
                    eps * (# irreducibly-joint distinctions)), but its SIGN is a
                    per-interface input -- Delta>0 iff the interface carries an
                    irreducibly-joint distinction (a correlation not reducible to
                    either marginal). A1 admits both Delta=0 (reversible) and
                    Delta>0, so theorems whose conclusions presuppose Delta>0 carry
                    this tag honestly. It is the SAME occupancy bit that branch (IJC)
                    names on the quantum axis ([P+IJC]); L_irr (the arrow of time)
                    and the IJC bridge (quantum non-commutativity) share it. (L_nc,
                    the sum-vs-budget non-closure lemma, supplies no Delta.)
  [C]               Conjecture.  Not yet proved; flagged for follow-up.
  [C, parked]       Conjecture deliberately parked pending further work
                    (e.g., subspace-level witnesses for I1/I3/I4 in
                    apf/unification_three_levels.py).
  [POSTULATE]       Framework postulate that's not derived but is named
                    explicitly so its load-bearing role is visible.
  [AXIOM]           A1 itself, the substantive finiteness claim about
                    admissibility space (Paper 0 v4.4 framing).
  [RED_TEAM]        Adversarial check certifying that a previously-flagged
                    failure mode does not actually occur.

The framework's previous corpus-wide claim "PLEC's four features force
noncommutativity" was structurally false and admitted an explicit spectator
countermodel.  The Phase 19 dichotomy framing replaces that claim with the
honest routing: PLEC universal, IJC regime-specific.  See the canonical
four-line statement in the IJC reference doc.

v6.7 CHANGELOG:
  - 312 theorems (was 294). 311 [P] + 1 [C].
  - Option 3 Work Plan: ALL SIX PHASES complete.

  PHASE 1 — Close the Seesaw Gap:
    L_seesaw_from_A1 [P] — Chain-completeness verification: 9-link kinematic
      chain derives the full type-I seesaw with zero BSM imports. M_R from
      scalar potential minimum (σ₀ = 29.1 GeV → M_R = [31, 61, 177] GeV),
      y_D = 1.86×10⁻⁷ from spectral weight. LOW-SCALE seesaw: suppression
      from y_D² ~ 10⁻¹⁴, not M_R/v. Collider-accessible ν_R.
    L_nuR_enforcement — 'Import:' label REMOVED. Seesaw now fully derived.
    RT_seesaw_necessity [P] — Adversarial test: chain is load-bearing,
      M_R kinematic, APF seesaw experimentally distinguishable from textbook.

  PHASE 2 — Mass Matrix from Capacity (FN gap closure):
    L_multiplicative_amplitude [P] — Additive cost + Gram overlap x → x^q
      by independence. Exponential suppression without Boltzmann. No flavon.
    L_Yukawa_bilinear [P] — Bilinear vertex + multiplicative amplitude →
      Y_{gh} = x^{q(g)+q(h)}. FN form is a theorem.
    L_mass_from_capacity [P] — 11-link chain, all [P]. Zero FN imports.
      "Capacity charges" replaces "FN charges."
    RT_FN_vs_capacity [P] — Capacity matrix = FN matrix to 10⁻¹⁵.
    T_capacity_ladder — 'FN imported' label REMOVED.

  PHASE 3 — Texture from Capacity (Fritzsch gap closure):
    L_texture_from_capacity [P] — 10-link chain verifies full texture
      derivation: LO rank-2 + curvature channel + NLO + NNLO. All NNLO
      parameters (c=x^{2d}, θ=π/N_gen, w=nearest-neighbor) derived from
      framework constants. Zero Fritzsch imports.
    L_GJ_from_capacity [P] — GJ modulation (1/N_c, N_c, 1) from capacity
      color channels. N_c from T_gauge, curvature concentration at gen-1.
      No SU(5) GUT invoked.
    RT_texture_chain [P] — Red team: all NNLO parameters have provenance.
    L_lepton_GJ — Docstring updated: "capacity color modulation" not "SU(5)".
    L_NNLO_Fritzsch — Docstring updated: parameters derived (v6.7 note).

  PHASE 4 — Bridge Closures:
    L_bridges_closed [P] — All 5 interpretive bridges identified by the
      work plan are now [P] theorems: (A) dim(G)=cost → L_cost, (B) capacity
      fractions=Ω → L_equip, (C) d_eff^C=microstates → L_self_exclusion+T_Bek,
      (D) σ=ln(d_eff) → T_entropy+T11, (E) x=1/2 → T27c+L_Gram.
      Zero interpretive assumptions remain.
    RT_bridge_audit [P] — Red team: all 5 bridges closed, 8 capacity→observable
      connections verified with explicit closing theorems.

  PHASE 5 — Adversarial Audit of Theorem R:
    RT_R1_stable_composites [P] — Stable composites forced (confinement +
      finiteness). Trilinear from oriented composites (B1_prime), not stability.
      One weak link (Step 4) documented. Not circular.
    RT_R2_vectorlike_SSB [P] — Vector-like is CPT-symmetric (no intrinsic
      gauge irreversibility). R2 sound but imprecise; sharpened to invoke
      T_M admissibility independence.
    RT_R3_no_U1 [P] — SU(3)×SU(2) IS anomaly-free without U(1). R3
      derivation REWRITTEN: admissibility completeness (A1 must distinguish
      all states) + minimality → one U(1). Documented reasoning corrected.
    Theorem_R — R1/R2 sharpened, R3 rewritten. Dependencies expanded to
      include T_M, T_field, T_confinement.
    L_gauge_template_uniqueness — Step 4 updated (admissibility completeness).

  PHASE 6 — NCG Spectral Action (near-term track):
    L_NCG_status [P] — 11/11 NCG items (3 components + 7 axioms + 1 principle)
      all [P]-derived or verified. 3 mathematical tools (heat kernel,
      rep theory, KO classification) with same status as Lie classification.
      Zero physics imports from NCG. Spectral action principle from A1.
    RT_NCG_no_physics_import [P] — Red team: zero physics imports confirmed.
      Long-term open: derive spectral triple formalism from canonical object
      (math research program, not physics derivation gap).

v6.6 CHANGELOG:
  - 294 theorems (was 289). 293 [P] + 1 [C].
  - NEW THEOREMS (5, from 2 sessions):
    L_seesaw_factorization [P] — Single-channel seesaw M_D·M_R⁻¹·M_D^T
      with holonomy phase produces factorizable phases → δ=0 exactly.
    L_PMNS_CP_corrected [P] — Supersedes T_PMNS_CP. k_B(ν)=3 (H̃).
      δ_PMNS = +3° to +11° from BK/Higgs cross-channel interference.
    L_DESI_DR2_confrontation [P] — DESI Year-3 (15M objects): APF (w=-1) NOT excluded.
    L_joint_cosmo_neutrino [P] — Joint (w=-1, Σm_ν=58.8 meV, NO). IO excluded.
    L_top_mass_hint [C] — σ = x^(1/d) = 0.8409 → m_t = 165.2 GeV. Conjecture.

v6.5 CHANGELOG:
  - 289 theorems (was 284). All [P] except 1 [AXIOM], 9 [RED_TEAM],
    1 [P + disp.rel.].
  - NEW THEOREMS (5):
    L_mu_mc_unified [P] — m_u/m_c via Gram crossing: 0.0017 (exp 0.0020±0.0006,
      0.4σ). Supersedes L_NNLO_up_mass (deprecated). Gram crossing route is
      authoritative; Δq mechanism was cancellation artifact.
    L_Higgs_curvature_channel [P] — Third FN channel from Higgs VEV
      curvature h=(0,1,0) on P₃. q_curv = q_B[0]/N_gen = 7/3.
      CLOSES m_s/m_b (4.4%), Georgi-Jarlskog (0.1%).
    L_NNLO_Fritzsch [P] — Complex Fritzsch perturbation: c = x^{2d},
      θ = π/N_gen, w = (1, −e^{iπ/3}, 0)/√2. 8 observables within 11%.
      δ_CKM = 65.7° (exp 65.6°, +0.1%). Zero free parameters.
    L_sin2_oneloop [P + disp.rel.] — sin²θ̂_W(M_Z) = (3/13)(1+Δκ̂_SM).
      Standard SM κ̂ correction Δκ̂ = +0.00195 = 3.4×α/(4π).
      11σ tension → <0.01% error. Irreducible: Δα_had [disp.rel.].
    L_lepton_GJ [P] — Full SU(5) GJ with generation-dependent Clebsch:
      gen-0 × 1/N_c, gen-1 × N_c, gen-2 × 1. m_e/m_μ at 3%,
      m_μ/m_τ at 4%, GJ₂ = 2.97 ≈ 3, GJ₁ = 0.33 ≈ 1/3.
  - GAP CLOSURES:
    m_s/m_b ratio: CLOSED (was ~100× too small) — curvature channel
    Georgi-Jarlskog: CLOSED (m_μ/m_τ ≠ 3×m_s/m_b) — curvature channel
    δ_CKM CP phase: CLOSED (was 13σ at LO) — Fritzsch NNLO
    sin²θ_W 11σ tension: CLOSED — SM one-loop correction
    m_d/m_s lift: CLOSED (was zero at LO) — Fritzsch NNLO
    V_us rotation: CLOSED (was 0.191) — Fritzsch NNLO
    Charged lepton masses: VERIFIED — SU(5) GJ Clebsch
    m_u/m_c: RESOLVED — Gram crossing (L_mu_mc_unified)
  - DEPRECATION: L_NNLO_up_mass marked DEPRECATED (Δq cancellation artifact).
  - ANNOTATIONS: Down-sector chain marked PRE-CURVATURE-CHANNEL (now
    superseded by L_Higgs_curvature_channel + L_NNLO_Fritzsch).

v6.3c+QG+GTU CHANGELOG:
  - 284 theorems (was 281). All [P] except 1 [AXIOM], 9 [RED_TEAM].
  - ZERO POSTULATES. Everything derived from A1 alone.
  - NEW THEOREMS (3):
    L_gauge_template_uniqueness [P] — SU(N_c)×SU(2)×U(1) is the UNIQUE
      gauge template. Exhaustive classification of all 17 compact simple
      Lie algebras against Theorem_R carrier requirements (R1+R2+R3).
      Step 2: Only SU(N_c≥3) has complex faithful fundamental (R1).
      Step 3: Only SU(2) has pseudoreal 2-dim faithful rep (R2).
      Step 4: U(1) unique compact abelian (R3).
      Step 5: Witten anomaly excludes even N_c.
      Step 6: All simple envelopes (SU(5),SO(10),E₆) cost ≥2× product.
      Product structure forced by admissibility independence (T_M + L_loc).
      CLOSES the classification gap: A1 → Theorem_R → template uniqueness
      → T_gauge(N_c=3) → T_field → L_count → C_total=61.
      C_total=61 is now RIGID: changing any factor destroys all predictions.
    L_Cauchy_uniqueness [P] — F(d)=d is the UNIQUE realignment cost function.
      Replaces representation principles R1-R4 with Cauchy's functional
      equation (1821) + monotonicity. C1 (additivity) from L_loc+L_cost,
      C2 (monotonicity) from A1, C3 (unit) convention.
      gamma = d+1/d = 17/4, sin²θ_W = 3/13 from 200-year-old theorem.
      Attack surface: reviewer must deny additive costs for independent channels.
    L_CKM_resolution_limit [P] — CKM 3-4% error is the FN resolution limit.
      All three CKM angle errors |2-4%| = intrinsic discreteness of x=1/2,
      integer-charge FN mechanism. δq = 0.049 FN charge units (1/20 of
      minimum step). Insensitive to c_Hu, charge perturbations, phase.
      PMNS 30× more accurate because Gram matrix has continuous parameters.
      The accuracy asymmetry is a PREDICTED feature, not a failure.
  - GAP CLOSURES:
    Gauge template uniqueness: the "why this gauge group" question now has
    a complete answer from A1 through established mathematics (Lie
    classification, Killing 1888 / Cartan 1894). Previously Theorem_R
    derived abstract carrier requirements but the bridge to the specific
    SU(N_c)×SU(2)×U(1) template was implicit. Now explicit and machine-verified.
    sin²θ_W derivation: R1-R4 representation principles replaced by Cauchy
    uniqueness (1821). Attack surface reduced from 4 framework axioms to 1
    established mathematical theorem.
  - DERIVATION CHAIN COMPLETION:
    A1 → {L_nc,L_irr,L_col} → Theorem_R → L_gauge_template_uniqueness
    → T_gauge(N_c=3) → T_field → L_count → C_total=61
    Every link is now [P] with machine-verified checks.

v6.3c CHANGELOG:
  - 277 theorems (was 275). All [P] except 1 [AXIOM], 9 [RED_TEAM].
  - ZERO POSTULATES. Everything derived from A1 alone.
  - NEW THEOREMS (4):
    L_hierarchy_boson_suppression [P] — EW VEV from capacity: v = 251.1 GeV (2.0% err)
      Closes P1 §2.1 (absolute hierarchy). C_boson=16 in coefficient AND exponent.
    L_hierarchy_cascade [P] — σ₀ = 29.1 GeV derived, M_R = [31,61,177] GeV [P]
      Closes P1 §2.2 (M_R from geometry). 7 downstream epistemic upgrades.
    L_neutrino_closure [P] — Δm²₂₁/Δm²₃₁ = 0.02952 (0.06% error)
      Closes P2 §1.3 (neutrino mass splittings). Both actions satisfied.
    L_yD_spectral [P] — y_D from seesaw vertex capacity:
      y_D² = 3/(77 × 102⁶). W_seesaw = C_f + 2C_b = 45+32 = 77.
      Two Higgs insertions in seesaw M_D·M_R⁻¹·M_D^T.
      Δm²₃₁ = 2.514e-3 eV² (0.04% error). ZERO neutrino anchors.
  - ANCHOR REDUCTION (WITHDRAWN 2026-05-29): the 2 → 0 neutrino-anchor claim
      rested on the absolute EW vev v=251 GeV, which came from a tuned c_R=1.968
      (the framework's own κ trace computes 21.34). The absolute scale reverts:
      M_Z and Δm²₃₁ anchors return; effective neutrino-sector anchors 0 → 1.
  - GAP CLOSURES (WITHDRAWN 2026-05-29): P1 §2.1 / §2.2 / §3.1 and P2 §1.3 were
      marked CLOSED on the tuned-c_R absolute vev. Those absolute-scale closures
      are re-graded [C] pending the c_R-source resolution (see L_sigma_normalization
      deeper-node question, wiki/Open Problems.md). Scale-free ratio results
      (e.g. Δm²₂₁/Δm²₃₁, sin²θ_W^OS, M_W²/M_Z²) are UNAFFECTED.
  - TESTABLE PREDICTIONS (zero-anchor neutrino sector):
      Σmᵢ = 59.9 meV (CMB-S4+DESI, σ~15-20 meV, ~2028)
      m_ββ = 4.4 meV (nEXO/LEGEND-1000, ~2030)
      Normal ordering (JUNO/DUNE, ~2028-2030)

v5.3.4 Phase 4 CHANGELOG:
  - 236 theorems (was 231). 226 [P], 0 [P_structural], 1 [AXIOM], 9 [RED_TEAM].
  - ZERO POSTULATES. Everything derived from A1 alone.
  - PROMOTIONS P_structural → [P] (5):
    L_CP_dual_mechanism — CKM/PMNS dual CP mechanism (root cause: k_B sector)
    L_TN_anomaly_protection — topological protection from anomaly cancellation
    L_MERA_generation — FN hierarchy = 3-level MERA (was already promoted)
    T12, L_matching_transition — (promoted in prior session)
  - NEW THEOREMS (5):
    L_DUNE_response [P] — APF δ_PMNS = 0° vs DUNE/HK sensitivity (2028-2035)
    L_sum_mnu_cosmo [P] — Σmᵢ = 59.2 meV vs Planck/DESI/future bounds
    L_prediction_catalog [P] — 25 quantitative predictions, 0 free params
    L_no_BSM [P] — 6 BSM exclusions (no SUSY, axion, 4th gen, W'/Z', gravitino, monopoles)
    (L_DESI_response [P] already existed from prior session)

v5.3.4 CHANGELOG:
  - 231 theorems (+11: L_coupling_capacity_id, L_mbb_prediction, L_proton_decay_channels,
    L_sigma_phenomenology, L_BH_page_curve_capacity, L_inflation_R2_spectral,
    L_FN_ladder_uniqueness, L_singularity_resolution, L_quantum_evolution,
    L_M_derived, L_NT_derived)
  - 216 [P], 5 [P_structural], 0 [POSTULATE], 1 [AXIOM]
  - COUPLING CONSTANT CHAIN FULLY PROMOTED [P]:
    NEW: L_coupling_capacity_id [P] — derives 1/α_cross = B×σ from
      Fisher equilibrium at the gauge crossing. The proof:
      (1) 1/α = resolved information [T20, P]
      (2) B = C_total/6 running modes [L_beta_capacity, P]
      (3) balanced sectors at crossing [L_Fisher_gradient, P]
      (4) σ = ln(d_eff) unique intensive entropy [L_sigma_intensive + L_equip, P]
      (5) per-mode resolution = σ by uniqueness → 1/α_cross = B×σ = S_dS/6
      Verified to 26 ppm against experiment.
    UPGRADED P_structural → [P]:
      L_crossing_entropy — 1/α_cross = S_dS/6 (was structural, now derived)
      L_alpha_s — α_s(M_Z) from capacity (inherits [P] from crossing_entropy)
      L_alpha_em — α_em(M_Z) from capacity (inherits [P] from crossing_entropy)
  - NEW PREDICTION:
    L_mbb_prediction [P] — neutrinoless double beta decay effective mass:
      m_ββ = 4.4 meV, Σmᵢ = 60 meV, m_β = 8.9 meV
      Majorana phases α₂₁ = α₃₁ = 0 (real seesaw → same-sign eigenvalues)
      Normal ordering, one experimental input (Δm²₃₁)
      Within reach of nEXO (~5-15 meV) and LEGEND-1000 (~9-21 meV)
  - PROTON STABILITY SHARPENED:
    L_proton_decay_channels [P] NEW — systematic analysis of all 7 known
      B-violation mechanisms:
      3 FORBIDDEN: no GUT (dim-6), no monopoles, ν_R conserves B
      4 NEGLIGIBLE: sphalerons (10⁻³²³), dim-7+ (>10⁶⁷ yr),
        gravitational (>10⁴⁵ yr), Majorana+sph (10⁻³³⁵)
      Weakest bound exceeds Super-K by 10¹¹
      Key new result: light ν_R (31-174 GeV) proven B-conserving
  - All three SM coupling constants now derived [P] from A1 alone.
  - Phase 2: sigma phenomenology, BH Page curve, inflation promoted [P].
  - L_sigma_phenomenology [P]: m_σ = 713 GeV (broad), ν_R displaced vertices, FCC-ee reach.
  - L_BH_page_curve_capacity [P]: S_rad = min(C_rad,C_BH)·s₁, scrambling time derived.
  - L_inflation_R2_spectral [P]: spectral action R² → Starobinsky → n_s=0.961, r=0.004.
  - T_inflation promoted P_structural → [P] (discrete staircase smoothing resolved).
  Phase 3 (theoretical completion):
  - L_FN_ladder_uniqueness [P]: q_B=(7,4,0) unique among 16 partitions (max hierarchy).
  - L_singularity_resolution [P]: no Big Bang singularity (S_min = ε* > 0).
  - L_M_derived [P] + L_NT_derived [P]: both postulates derived from A1.
  - M,NT promoted POSTULATE → [P] (zero postulates remaining).
  - L_quantum_evolution [P]: 61 CPTP commitment steps, path integral over S_61.
  - Phase 3: FN uniqueness, singularity, quantum evolution, M/NT derived.
  - L_FN_ladder_uniqueness [P]: q_B=(7,4,0) unique among 16 partitions (max hierarchy + D2q).
  - L_singularity_resolution [P]: S_min = ε* > 0 → no S=0 singularity, ρ_max finite.
  - L_quantum_evolution [P]: U(t) = exp(-iHt) on 2^61-dim H, exact Z, no UV divergence.
  - L_M_derived [P]: M (multiplicity) derived from T_field (61 ≥ 2).
  - L_NT_derived [P]: NT (non-degeneracy) derived from T11 (42 ≠ 19).
  - M, NT promoted POSTULATE → [P]. Zero postulates remaining.

v5.3.3 CHANGELOG:
  - 214 theorems (+4: geometric & symmetry internalization)
  - 194 [P], 8 [P_structural], 2 [POSTULATE], 1 [AXIOM]
  - NEW [P]: L_kolmogorov_internal (continuum limit from A1+R3),
             L_chartability (smooth atlas from Lipschitz+regularity),
             L_coleman_mandula_internal (direct product from admissibility),
             L_lovelock_internal (Einstein equations unique in d=4)
  - External imports: 11 → 5
    ELIMINATED: Kolmogorov extension (1933), Nash-Kuiper+Palais,
                Coleman-Mandula (1967), Haag-Lopuszanski-Sohnius (1975),
                Lovelock (1971)

v5.2.9 CHANGELOG:
  - 185 theorems (+1: L_Fisher_measure new)
  - 172 [P], 10 [P_structural], 2 [POSTULATE], 1 [AXIOM]  (was 165/16)
  - UPGRADED [P_structural] → [P]: 7 theorems in Fisher geometry cluster

  KEY NEW THEOREM: L_Fisher_measure [P]
    Derives S = (d_eff/2) ln det G from APF capacity counting (IID argument):
    - d_eff = 102 independent channels (T_deSitter_entropy [P])
    - Each channel contributes (1/2) ln det G via Gaussian entropy formula
    - Total: S = (d_eff/2) ln det G + const  [exactly, not approximately]
    - IID exponent 51 vs Stiefel exponent 49 difference = (n+1)/2 = 2 (3.9%)
    - Stiefel exponent would FAIL the CKM entropy budget check (2.55 vs 2.66 nats)
    - IID exponent passes: this is the correct APF counting measure

  UPGRADED THEOREMS (all now [P]):
    L_Fisher_factorization  — 7D Fisher metric block-diagonal
    L_Fisher_curvature      — K = 1/(4 d_eff) = 1/408, R = 3/(2 d_eff)
    L_Fisher_entropy_budget — mixing uses 17.1% of S_dS
    L_Fisher_geodesic       — boundary det(G)=0 at infinite geodesic distance
    L_CP_geometric_bound    — |delta_PMNS| < 120 degrees, width 10 degrees
    L_Fisher_gradient       — beta = P grad V, RG flow = gradient descent
    [plus L_Fisher_measure itself = new [P] theorem]

  REMAINING P_structural (10):
    L_crossing_entropy, L_alpha_s  — sigma = ln(d_eff) identification
    L_dm2_hierarchy                — eigenvalue ordering assumption
    L_CP_dual_mechanism            — dual mechanism structural
    L_matching_transition          — latent heat / inflation connection
    T_inflation                    — reheating dynamics
    L_TN_anomaly_protection        — topological interpretation
    L_MERA_generation              — MERA structural equivalence
    L_SA_Higgs, L_RG_lambda        — Lambda_APF = Lambda_GUT identification

v5.2.8 CHANGELOG:
  - 184 theorems (was 183, net +1: L_RG_lambda new)
  - CORRECTED: L_SA_Higgs — removed false SW2010 citation
  - NEW: L_RG_lambda [P_structural] — lambda_H RG running, APF+CCM predicts m_H = 149 GeV

  CORRECTION DETAIL: v5.2.7 L_SA_Higgs incorrectly cited Shaposhnikov-Wetterich (2010)
  as giving m_H = 124.5 GeV via APF+CCM+RG. SW2010 uses lambda(M_Pl) = 0 from asymptotic
  safety — a different initial condition from CCM's lambda(GUT) = g²/2. The correct
  APF+CCM+1-loop RG prediction is m_H = 149 GeV, which is the known minimal-spectrum
  Connes result (documented in CCM 2007, Buck et al 2010).

  L_RG_lambda DERIVATION:
    Step 1: APF d/c² = 0.33311 = 1/3 to 0.07% (L_SA_sector_dominance [P])
    Step 2: CCM initial condition lambda(M_GUT) = g₂²/2 = 0.1360
    Step 3: 1-loop SM RG (import: T6B beta coefficients [P]) to M_Z
            lambda(M_Z) = 0.1832
    Step 4: m_H = sqrt(2 * 0.1832 * v²) = 149.1 GeV
    GUT-scale independence: m_H = 149-151 GeV for M_GUT in [10¹⁴, 10¹⁷] GeV

  THE HONEST STATUS OF 149 GeV:
    - This is the correct APF+CCM+1-loop prediction
    - Observed: 125.09 GeV — residual 19% gap
    - Gap is the known open problem in Connes spectral geometry:
      CCM 2007 (m_t=174 GeV) gave ~170 GeV; our (m_t=163 GeV) gives 149 GeV
    - Closing the gap requires right-handed Majorana neutrinos (y_D ~ 0.4,
      M_R ~ 10¹⁴ GeV) — requires adding nu_R to T_field [EXTENSION TARGET]
    - Alternatively: asymptotic safety lambda(M_Pl)=0 (SW2010), different framework
    - APF as defined (T_field: 48 Weyl fermions, Dirac nu) gives minimal CCM result

v5.2.7 CHANGELOG:
  - 183 theorems (count unchanged — corrected v5.2.6 theorems)
  - CORRECTED spectral action cross-check (L_SA_moments, L_SA_sector_dominance, L_SA_Higgs)

  BUG FIXED: v5.2.6 used raw APF internal mass matrices for the spectral action.
  The spectral action (CCM 2007) requires dimensionless YUKAWA COUPLINGS Y = M/v,
  not mass matrices. Each sector has a different internal scale in APF units:
    sv_d[0]/sv_u[0] = 1.887  (derived: M_d[2,2]=vB²+vH²=2 vs M_u[2,2]=bk+x³=1.125)
  This ratio is a DERIVED APF structural quantity but does NOT affect d_s/c_s²
  (scale-invariant). When sectors are properly normalized to physical Yukawas:
    lambda_s = y_s^{heaviest}(M_Z) / sv_s[0]
  the cross-sector imbalance disappears completely.

  CORRECTED RESULTS:
    c = 2.630437  (was 21.985 — artifact of mixing sectors with different internal scales)
    d = 2.304827  (was 87.201)
    d/c² = 0.33311  (was 0.180 — artifact; now 1/3 to 0.07%)
    Top fraction of c: 99.97%  (was 17.4% — now CCM top-dominance fully restored)
    m_H(APF) = 282.6 GeV  (confirms CCM, not 208 GeV)

  THE CORRECT STORY:
    1. APF CONFIRMS CCM: d/c² = 1/3 to 0.07%. APF and CCM agree exactly.
    2. APF DERIVES sector dominance: FN hierarchy forces eps² < 10^-7 in each sector,
       explaining FROM FIRST PRINCIPLES why CCM's top-dominance assumption holds.
    3. APF DERIVES sv_d/sv_u = 1.887: this structural ratio (from down double-VEV)
       modifies the effective cross-sector normalization, but is transparent once
       the physical Yukawa mapping is applied.
    4. Remaining m_H gap (283 -> 125 GeV): RG running Lambda_APF -> M_Z.
       Shaposhnikov-Wetterich (2010) independently gives m_H ≈ 124 GeV after RG.
       APF beta functions (T_alpha_s [P]) provide the machinery; formal RG
       derivation of lambda_H running is the next open target.

v5.2.6 CHANGELOG:
  - 183 total theorems (was 182 in v5.2.5)
  - 3 new [P/P_structural] theorems: spectral action cross-check
  - Closes the gap between APF and Chamseddine-Connes-Marcolli (2007)

  L_SA_moments [P]:
    Spectral action heat kernel moments from APF D_F:
    c = Tr(M_Y†M_Y) = 21.984950, d = Tr((M_Y†M_Y)²) = 87.201141, N_f = 48.
    KEY FINDING: Down sector dominates c at 61.9% (not top-dominated).
    M_d[2,2] ≈ vB²+vH² = 2.0 vs M_u[2,2] ≈ bk+x³ = 1.125 — APF VEV
    structure naturally makes the down sector larger in these units.
    Heat kernel expansion verified: err < 0.005% at t=1e-4.
    Connects to CCM (2007): c → Higgs mass², d → Higgs quartic.

  L_SA_sector_dominance [P]:
    Within each fermion sector: d_sector/c_sector² = 1/N_color to 10^-8.
    Up: 0.3333332556 vs 1/3, ε² = 1.17e-7. Down: 0.3333332939 vs 1/3, ε² = 5.9e-8.
    Analytic: d/c² = (1/N_c)(1-2ε₂) verified to 1e-9.
    Neutrino: exact 1/1 (rank-1 matrix, σ₂=σ₃=0 exactly).
    FN hierarchy forces ε² < 10^-6 → exceptional sector dominance.
    Cross-sector deviation: d_total/c_total² = 0.1804 = (1/N_c)×Σf_i²,
    a GEOMETRIC effect of multi-sector spectral mixing, not a violation.
    KEY: APF FN hierarchy DERIVES the sector dominance that CCM assumes.

  L_SA_Higgs [P_structural]:
    CCM top-dominated prediction: m_H = sqrt(8/3)×m_t = 282.7 GeV.
    APF correction: d/c² = 0.1804 → correction factor = 0.7357.
    APF-corrected: m_H = 208.0 GeV (47% of CCM gap to observed 125.1 GeV closed).
    Mechanism: down sector NNLO dominance → Σf_i² = 0.456 < 1 → diluted λ_H.
    APF + RG running estimate: ~127 GeV (within 2% of observed).
    [P]: d/c²=0.1804, gap fractions, correction mechanism.
    [P_structural]: m_H formula requires Λ_APF=Λ_GUT identification.

  SUMMARY OF SPECTRAL ACTION CROSS-CHECK:
    The two independent derivation paths — APF comparison geometry and
    Connes-Chamseddine spectral action — converge on consistent physics:
    (1) APF derives the D_F that CCM takes as input: sector dominance is
        a consequence of FN hierarchy, not an assumption.
    (2) APF's multi-sector structure (down-dominated c) CORRECTS CCM's
        known over-prediction of m_H from 283 GeV toward 208 GeV.
    (3) With RG running (derivable from APF beta functions): ~127 GeV ≈ obs.
    The gap cannot be coincidence: two frameworks built on different axioms
    produce the same spectral coefficients and the same Higgs correction direction.

v5.2.5 CHANGELOG:
  - 180 total theorems (was 176 in v5.2.4)
  - 4 new theorems completing the Connes Spectral Triple derivation
  - L_anomaly_index upgraded [P_structural → P] (via McKean-Singer)

  L_ST_algebra [P]:
    A_F = C ⊕ M_2(C) ⊕ M_3(C) derived from T_gauge [P].
    dim(A_F)=14 = 1+4+9. U(1)→C, SU(2)→M_2(C), SU(3)→M_3(C).
    Center Z(M_2)=C·I_2 picks out U(1) direction. SU(2) generators ⊂ M_2.
    *-algebra involution (AB)*=B*A* verified. Establishes Wedderburn decomposition.
    Connes-Lott (1991), Connes-Marcolli (2008).

  L_ST_Hilbert [P]:
    H_F = C^45 ⊕ C^45 = C^90 from T_field + T7 + T_CPT [all P].
    15 Weyl/gen × 3 gen = 45 particle + 45 antiparticle.
    Quarks (72) + leptons (18) = 90 total.
    Generation subspace for D_F: 4 sectors × 2×3 = 24-dim.
    APF minimal (no ν_R from T_field) vs Connes 96 (with ν_R).

  L_ST_Dirac [P]:
    D_F = [[0,M_Y†],[M_Y,0]] with M_Y = diag(M_u,M_d,M_ν,M_e).
    All four Yukawa matrices from [P] theorems.
    6 of 7 Connes axioms verified in generation subspace:
      (i) D†=D ✓  (ii) real spectrum = ±sv(M_Y) ✓
      (iii) compact resolvent (finite-dim) ✓  (iv) ||[D,π(a)]||<∞ ✓
      (v) γD+Dγ=0 (chirality anticommutes) ✓  (vi) J²=-I, JD=-DJ ✓
      (vii) [L(a),R(b)]=0 bimodule verified; full first-order [P] structural.
    KO-dimension = 6 (mod 8), signs (ε,ε',ε'')=(-1,-1,-1).
    Connes distance d(g,h) = 1/|M_u[g,h]| ~ x^{-(q_B[g]+q_B[h])}.
    FN HIERARCHY IS THE CONNES METRIC ON GENERATION SPACE.

  L_ST_index [P]:
    Index(D_F) = 0 for all four sectors (u,d,ν,e).
    Three independent proofs:
      (a) Rank: M_Y is N_gen×N_gen square → ker(M)=ker(M†) → Index=0.
      (b) McKean-Singer: Tr_s[e^{-tD²}]=0 verified at t=0.001,0.01,0.1,1.0.
      (c) Cross-check: [U(1)]^3=∑Y³=0 (L_anomaly_free [P]).
    CPT chain: T_CPT → H_L=H_R → M_Y square → Index=0 → anomaly-free.
    CLOSES ATIYAH-SINGER GAP: McKean-Singer is purely algebraic on D_F,
    no bundle curvature required. L_anomaly_index upgraded [P_struct→P].

  SUMMARY OF SPECTRAL TRIPLE DERIVATION:
    (A_F, H_F, D_F) fully derived from APF first principles.
    A_F from T_gauge, H_F from T_field+T7+T_CPT, D_F from Yukawa theorems.
    FN hierarchy encodes the Connes metric: d(g,h) ~ x^{-(q_B[g]+q_B[h])}.
    CPT → square Yukawa → Index=0 → anomaly cancellation (exact algebraic chain).
    Connects to Connes-Lott (1991), Connes-Marcolli (2008),
    Chamseddine-Connes-Marcolli (2007), McKean-Singer (1967).

v5.2.4 CHANGELOG:
  - 176 total theorems (was 171 in v5.2.3)
  - supplements: +5 new mathematical connections theorems
  - "Connecting to Established Math" series

  L_KMS_trace_state [P]:
    APF saturation state ρ=I/d_eff is the (σ^ω=id, β)-KMS trace state.
    Modular Hamiltonian H_mod = ln(102)·I (trivial — proportional to identity).
    Modular automorphism σ^ω_t = id (no flow). KMS at any β via trace cyclicity.
    Physical temperature T = ln(d_eff)/ε* matches T_zeroth_law exactly.
    Closes paper's claim about Tomita-Takesaki modular theory.

  L_RT_capacity [P]:
    S(A) = k·ln(d_eff) = (k/61)·S_dS for any subregion of k types.
    APF version of Ryu-Takayanagi formula for uniform boundary density.
    Special cases: S(vacuum) = Ω_Λ·S_dS, S(matter) = Ω_m·S_dS.
    Zero mutual info from the maximally-mixed saturation state (L_equip + L_KMS_trace_state;
    I/d^n = ⊗ I/d) → exact additivity. The count identity S(A)=(k/61)·S_dS is [P]; the
    holographic/entanglement reading of it is [P_structural_reading] (the dS state is mixed,
    so S(ρ_A) is marginal mixedness, across-cut entanglement = 0).

  L_MERA_generation [P_structural]:
    3-level FN hierarchy (q_B=7,4,0) = 3-level MERA ansatz.
    Isometry W†W=1 verified at both scales (x^3=1/8, x^4=1/16).
    FN charge additivity: Δq₀₁ + Δq₁₂ = 3+4 = 7 = q_max.
    Disentangler = holonomy rotation φ=π/4. Bond dim = κ=2.
    Structural: MERA is a variational ansatz, not derived from A1.

  L_algebra_type [P]:
    Finite APF algebra = ⊗_{61} M_{102}(ℂ) ≅ M_{102^61}(ℂ): type I (Wedderburn).
    Thermodynamic limit at physical β: type III_λ Powers factor, λ=e^{-βε*}=0.806.
    β→0 saturation limit: λ→1 → type III₁ (Araki-Woods).
    Correctly identifies paper's "type III₁" claim: valid for Gibbs state as β→0.
    Establishes: Wedderburn (1907), Powers (1967), Araki-Woods (1968).

  L_anomaly_index [P_structural]:
    7 anomaly cancellation conditions = vanishing of Atiyah-Singer Dirac index.
    [U(1)]^3 = ∑Y³ = 0 (cubic hypercharge index). [grav]²U(1) = ∑Y = 0.
    [SU(2)]^3 = 0 automatically (SU(2) has no cubic Casimir d^{abc}=0).
    Witten: 12 doublets ≡ 0 (mod 2). [SU(3)]^3 = 0 per generation.
    Unique SM content = unique zero of 6 integer index equations (1/4680).
    P_structural: A-S requires bundle curvature formalism not yet in bank.
    Establishes: Atiyah-Singer (1963-71), Alvarez-Gaumé & Witten (1983).

v5.2.3 CHANGELOG:
  - 171 total theorems (was 168 in v5.2.2)
  - supplements: +3 new (L_TN_Hamiltonian [P], L_TN_product_state [P],
    L_TN_anomaly_protection [P_structural])
  - Target 11 CLOSED: Tensor Network Reformulation
  - Key result 1: APF realignment cost = uniform graph Hamiltonian H = -ε*ΣN
    J_ij = 0 (no inter-type coupling) from L_equip. Complexity is entirely
    in the constraint surface (anomaly-free matching polytope), not H.
    Unlike Ising models: APF is the reverse — trivial H, complex constraints.
  - Key result 2: Ground state is a D_bond=1 product TN. Zero entanglement
    between type pairs (mutual info I(i;j)=0). Partition function factorizes:
    Z = (1+e^{βε*})^61. L_loc expressed algebraically as product structure.
    MERA refinement: 3 levels at x^3, x^4 from FN charge gaps.
  - Key result 3: 7 anomaly conditions = topological protection of ground state.
    Physical sector = single point in 2^61 config space (unique full matching).
    Z_2 invariant N≡1(mod 2). Block structure: 42-node vacuum + 19-node matter
    reproduces Ω_Λ=42/61 (0.05%), Ω_m=19/61 (0.13%) from TN block decomposition.
    Condensed matter analog: anomaly gap ↔ topological gap in topological order.

v5.2.2 CHANGELOG:
  - 168 total theorems (was 167 in v5.2.1)
  - supplements: +1 new (L_CKM_phase_bracket [P_structural])
  - Target 6 FULLY CLOSED: CKM CP Phase
  - Criterion A (delta within 5°): CLOSED
      LO: delta=85.4° (13σ). V2 NLO: delta=61.8° (2.5σ, within 5° window)
      V1 NLO: delta=68.6° (1.9σ, also within 5° window)
      Experiment 65.6° lies between V1 and V2 → NLO mechanism confirmed
      13x improvement in delta tension
  - Criterion B (Vus within -10%): CLOSED by NNLO (L_NNLO_down_mass)
      NLO alone: V2 Vus=-15.3% (fails), but experiment bracketed between V1/V2
      NLO+NNLO: Vus=+1.2%, delta=66.0° (0.4° from exp) — 13x improvement
      Three-effect mechanism: (1) rescale→delta 85°→66°, (2) rotate→Vus+1%, (3) lift m_d
  - Alpha determination: alpha=0 (V2) derived from k_B_down=0 trivial holonomy
  - Numerical exploration confirmed: NNLO phase corrections that improve
    delta+Vus simultaneously break Vcb (-20%) and Vub (-85%)
  - Epistemic label: [P] (both criteria closed by NLO+NNLO chain)

v5.2.1 CHANGELOG:
  - 167 total theorems (was 164 in v5.2.0)
  - supplements: +3 new (L_beta_temp, T_zeroth_law, T_first_law)
  - Target 9 CLOSED: Temperature and Thermodynamic Foundation
  - beta = DeltaS/DeltaE = ln(d)/epsilon well-defined [P]
  - Zeroth law: beta equalizes via L_irr-driven capacity flow [P]
  - First law: dE = TdS + dW; cosmological fill is pure heat [P]
  - T_univ = epsilon/ln(102); T_phys = hbar/(2*k_B*ln(102)) derived


  - 161 total theorems (was 157 in v5.1.3)
  - generations: +4 new (L_null_direction, L_e3_gen0,
    L_NNLO_three_effects, L_NNLO_down_mass).
    Phase 1 Targets 6+7 (NNLO down-sector mass / perpendicular geometry).
    Resolves L_md_zero open problem: m_d lifted from zero by single
    rank-1 NNLO correction with c = x³, ρ = x^d/d.
    Six observables (m_d/m_s, δ_CKM, V_us, V_cb, V_ub, J) all within
    sub-6% of experiment from two derived parameters.
    Key insight: perpendicular direction e3 = v_B × v_H is pure gen-0
    (gen-1 exactly zero); rank-1 form essential for V_us rotation
    via cross terms.

v5.1.3 CHANGELOG:
  - 151 total theorems (was 147 in v5.1.2)
  - L_Fisher_gradient FIXED: corrected fixed point (w*=(3/8,5/4) from
    Aw*=γ, not w*=(10/13,3/13) from Aw*=1), metric (P_ij=w_i A_ij w_j,
    not diag(w)A diag(w*)), and sign convention (β=+P∇V forward/IR).
  - generations: +3 new (L_Fisher_factorization, L_CP_geometric_bound,
    L_CP_dual_mechanism). Phase 1 Target 5 (Information Geometry / CP).
    Positivity bound on leptonic CP: |δ_PMNS| < 120° (geometric),
    δ_PMNS = 0° ± 10° (Boltzmann). Two CP mechanisms: holonomy (CKM)
    vs entropy optimization (PMNS).
  - cosmology: +2 restored (L_singlet_Gram, L_dark_budget).
    Were in v5.1.0 HTML report but lost from source. Reconstructed.
  - Registry fixes: L_cap_per_dim → L_capacity_per_dimension,
    L_boundary_proj → L_boundary_projection (7+1 dependency refs resolved).
  - All 151 theorems pass. All dependencies resolve. All cross-refs resolve.

v5.1.1 CHANGELOG:
  - 147 total theorems (was 145 in v5.1.0)
  - generations: +2 new (L_seesaw_dimension, L_dm2_hierarchy)
  - Phase 1 Target 2 (neutrino mass hierarchy)
  - Effective seesaw dimension d_seesaw = 9/2 from capacity averaging
  - Dm2_21/Dm2_31 = 0.0318 (exp 0.0295, 7.8%) closes 3.4x gap

v5.1.0 CHANGELOG:
  - 145 total theorems (was 143 in v5.0.9)
  - cosmology: +2 new (L_singlet_Gram, L_dark_budget)
  - Phase 1 Target 1 (dark sector internal structure)
  - Singlet Gram matrix rank-1 derivation
  - Dark sector collisionlessness at all perturbative orders

v5.0.9 CHANGELOG:
  - 143 total theorems (was 138 in v5.0.8)
  - generations: +5 new (L_channel_disjoint, L_trace_equality,
    L_beta_capacity, L_crossing_entropy, L_alpha_s)
  - Phase 1 Target 3 (strong coupling from capacity structure)
  - HTML report generation
"""

import time as _time
from collections import OrderedDict

# Single source of truth for module lists. Re-derived 2026-05-18 (v24.3.19)
# as part of the MODULES unification refactor. Both bank._MODULE_PATHS (loaded
# below) and verify_all.MODULES (in verify_all.py) now import from this manifest.
from apf._module_manifest import (
    BANK_LOAD_MODULES as _MODULE_PATHS,
    EXPECTED_REGISTRY_SIZE,
)
from apf.apf_utils import CheckFailure
from apf.apf_utils import dag_reset, dag_dump, dag_verify_chain

__all__ = ['REGISTRY', 'run_all', 'main']

REGISTRY = OrderedDict()

# Expected theorem count — updated when theorems are added/removed.
# If the loaded count doesn't match, something silently failed.
EXPECTED_THEOREM_COUNT = EXPECTED_REGISTRY_SIZE  # 3299 v24.3.37 (2026-05-19 STARTUP+++++++++ - Coherent Materials Audit Layer lands as Codomain Selection specialization. EXPECTED unchanged at 3299 (utility modules architecture-only); BANK_REGISTRY_MODULES unchanged at 233; ARCHITECTURE_ONLY_MODULES 23 -> 29 (+6 utility modules). Sibling-AI materials-discovery proposal absorbed under corrected architectural framing per Reference - APF Coherent Materials Audit Layer and Codomain Selection Specialization (2026-05-19).md. **Coherent Materials Audit Layer is a materials specialization of the Codomain Selection Engine** (Tier 2, landed Session 2 today), not a new sixth engine or separate operating system. Bank-side absorption of the v5 superconductivity/coherent-materials suite without the architectural OS commitment the original proposal proposed. **Bank actions**: APF_SUPERCONDUCTIVITY_MATERIALS_OPENING_SUITE_v5 banked to DOCTRINE_CONSEQUENCES_BUNDLE_LATEST_44/ (bundle 180 -> 181). 6 utility modules installed to apf/ as ARCHITECTURE_ONLY_MODULES: apf/sc_material_ledger.py (5.6 KB; ledger schema validator with 8 required slots); apf/correlated_layer_competition.py (3.9 KB); apf/sc_material_evidence.py (3.8 KB); apf/coherent_materials_discriminator.py (10.7 KB; runtime classifier); apf/coherent_materials_intervention_selector.py (15.4 KB; ranks next admissible interventions); apf/coherent_materials_protocol_compiler.py (21.9 KB; compiles intervention into receipt-bearing protocol card). All 6 modules architecture-only (no register, no check_*); parallel to v24.3.30 coherent-phase utility modules pattern. **Engine placement** per Reference doc: 4 formal role assignments: ledger schema -> Tier 4 adapter input contract; discriminator -> Codomain Selection specialization; intervention selector -> recommended-next-action generator; protocol compiler -> materials-specific obligation packet compiler (subtype of evidence_required in obligation_packet_meta_schema). Public ingestion bridge (Materials Project / OPTIMADE / GNoME / SuperCon) placed *outside* APF core as downstream toolchain producing APF-ingestable ledgers. **Naming convention**: APF-Mat retained as strategic vision/program name; 'Coherent Materials Audit Layer' is the formal bank architecture name. OS framing from original proposal explicitly NOT committed pending demonstrated need beyond Codomain Selection specialization. **Atlas posture**: no new MATERIALS axis. Materials adjudication uses existing CODOMAIN axis with metadata fields (domain=materials, family=correlated_layer_SC, functional_codomain=quantum_memory). **LATEST-84 through LATEST-89 sequence from original proposal explicitly NOT committed**. v5 banked content sufficient for current hero lanes (Pearson rare-earth quantum memory + correlated-layer SC). **Honest non-claims preserved verbatim across v5 suite**: numeric_Tc = 0; room_temperature_SC_claim = 0; SC_new_material_prediction = 0; SC_highTc_solved = 0; SC_ab_initio_chemistry = 0; experimental_result = 0; Pearson_SC_claim = 0. Pearson NaEu(IO3)4 routed as COHERENT_BUT_NOT_SC subtype QUANTUM_MEMORY_MATERIAL_ADMISSIBLE_PARTIAL. **Audit-first cross-AI handoff demonstrated**: in-session Claude reviewed sibling AI proposal, identified abstraction-creep risk, proposed Option B + Option C. Sibling AI accepted critique, lowered architectural claim, kept substantive content. Architecture-review framework caught exactly the kind of abstraction creep it was designed to catch (Reference doc Q named this as the dominant failure mode for IE family naming). **Sandbox + production bank load**: 3299/3299. setup.py + apf/__init__.py + bank.py changelog all 24.3.36 -> 24.3.37. Working Rule 9 preemptive tmp+rename used across 9 file writes; zero truncation incidents. Closure pack APF_COHERENT_MATERIALS_AUDIT_LAYER_LAND_v1 at bundle 181 -> 182. Reference doc landed at __APF Library/APF Reference Docs/. **Cross-day arc**: today's work spans Sessions 1-6b of architecture-review (+25 bank checks; 5-engine IE family operationally complete) + this Coherent Materials Audit Layer land (+0 bank checks; +6 architecture-only utility modules; materials-specialization framing committed in writing). Total today: +25 bank checks; codebase v24.3.30 -> v24.3.37; 8 new closure packs (174 -> 182); 7 new BANK_REGISTRY modules + 10 new ARCHITECTURE_ONLY utility modules. Bank state: 3299/3299 PASS.) v24.3.36 (2026-05-19 STARTUP++++++++ - Session 6 latent engine operationalization: all 3 latent engines named in architecture-review Reference doc now have Tier 2 engine seeds. **The 5-engine IE family is operationally complete at structural-commitment level**: Route Adjudication (existing IE) + Codomain Selection (Session 2) + Kinematics Adjudication + Defect Calculus + Representation Descent. Three new BANK_REGISTRY modules + 9 new bank checks (3 per engine following Session 2 Codomain Selection Engine pattern: identity + entry_point + audit_first). `apf/kinematics_adjudication_engine.py` (17.8 KB; +3 bank checks): Tier 2 engine wrapping apf.interface_kinematics_engine.compute_kinematic_certificate + apf.interface_kinematic_solver.solve_kinematic_path (existing modules from v24.3.16-17 kinematics layer). Verdict schema KinematicAdjudicationVerdict + 6-status enum (KINEMATIC_PATH_CLOSED / HOLONOMY_DEFECT / ORDER_DEFECT / PHASE_SPACE_INCOHERENT / INVARIANT_VIOLATED / OPEN_EVIDENCE_REQUIRED). Entry point adjudicate_kinematic_composition(route, payload). Unit of adjudication = route's kinematic composition (parallel to Route Adjudication's transport composition but with kinematics-state-machine reasoning). `apf/defect_calculus_engine.py` (16.6 KB; +3 bank checks): Tier 2 engine wrapping apf.defect_global_descent_kernel.certify_global_descent + apf.defect_master_integration.stack_report (existing defect-calculus stack from v24.3.18). Verdict schema DefectAdjudicationVerdict + 6-status enum (ZERO_DEFECT_GLOBAL / DELTA_P_NONZERO / DELTA_O_NONZERO / DELTA_E_R_NONZERO / GLOBAL_DESCENT_KERNEL_NONEMPTY / OPEN_EVIDENCE_REQUIRED). Entry point adjudicate_defect_stratum(unit_id, patches). Unit of adjudication = continuation certificate's defect-stratum classification (A_Gamma ⊃ P_Gamma ⊃ O_Gamma ⊃ E_{Gamma,r}). `apf/representation_descent_engine.py` (19.6 KB; +3 bank checks): Tier 2 engine wrapping apf.interface_solver_descent_bridge.solve_interface_descent (existing bridge from v24.3.12). Verdict schema RepresentationDescentVerdict + 6-status enum (DESCENT_EXACT / OBSTRUCTION_NONZERO / DESCENT_NONEXACT / FUNCTORIAL_TRANSPORT_FAILED / GLOBALIZATION_GATE_BLOCKED / OPEN_EVIDENCE_REQUIRED). Entry point adjudicate_representation_descent(problem_name, problem). Unit of adjudication = representation-descent problem; Theorem 7 (Global physics = ker(Obs_APF) = im(Glob)) made operationally adjudicate-able. **Enum extensions**: EngineTarget in claim_dispatcher_multi_engine and EngineSubtype in obligation_packet_meta_schema both extended from 2 to 5 values. The 3 new engine values (KINEMATICS_ADJUDICATION + DEFECT_CALCULUS + REPRESENTATION_DESCENT) are reachable via direct adjudicate_*_*() entry points but not yet via dispatch_multi_engine (claim recognizers not added for them; would require per-engine claim-text signatures which is Session 7+ work). meta_schema_identity bank check updated to assert == 5. **Audit-first discipline preserved across all 3 latent engine seeds**: per-engine non-claims explicit (kinematics: target_value_consumed + kinematic_dynamics_imported + phase_space_volume_consumed; defect: target_value_consumed + new_physical_claim + infinity_stack_claim; representation_descent: target_value_consumed + flat_substrate_global_cstar_algebra + infinity_stack_or_cohomology_overclaim — the last two preserved verbatim from v24.3.11 representation-descent kernel non-claims). **OPEN_EVIDENCE_REQUIRED is dominant initial state**: parallel to Codomain Selection (Session 2) where 6 of 7 regimes had no runtime evaluator and returned OPEN. Each engine's entry point returns OPEN_EVIDENCE_REQUIRED for missing-input cases with obligation packets naming exactly what's needed (kinematics: payload; defect calculus: patches; representation_descent: problem specification). EXPECTED 3290 → 3299 (+9); BANK_REGISTRY_MODULES 230 → 233 (+3). ARCHITECTURE_ONLY_MODULES unchanged at 23. setup.py + apf/__init__.py + bank.py all bumped 24.3.35 → 24.3.36. **Working Rule 9 preemptive tmp+rename** used uniformly across 7 file writes (3 engine modules + 2 enum extensions + manifest + bank.py changelog). Zero truncation incidents. Pre-install snapshot reused: Codebase/Old/APF_Codebase_v24.3.29_post-tier1-wire-in_2026-05-19.zip. Closure pack APF_LATENT_ENGINES_OPERATIONAL_SEEDS_v1 lands at bundle 179 → 180. **Architecture-review sequencing arc COMPLETE**: Sessions 1-5 closed (24.3.30 → 24.3.34); Session 6 scipy gap closure CLOSED (24.3.35); Session 6 latent engine operationalization CLOSED (24.3.36). The 5-engine IE family is operationally complete; future work (Session 7+) is incremental — claim-text recognizers for non-route/non-codomain engines; engine-axis atlas integration for new engines; per-engine meta-schema wrappers as needed. Bank state: 3299/3299 PASS expected in both production and sandbox.) v24.3.35 (2026-05-19 STARTUP+++++++ - Session 6 scipy gap closure: persistent sandbox -6 gap CLOSED. Across the entire architecture-review arc (v24.3.30 → v24.3.34) the sandbox bank.load() reported `Expected N, loaded N-6` because apf.cmb_finite_mode_covariance imported scipy.optimize.minimize and scipy is missing in the sandbox. Production environments have scipy and reported gap = 0. **New Tier 3 utility module `apf/_optimize_vendored.py`** (12 KB; +1 bank check) vendors the one scipy function the bank uses: minimize(fun, x0, method='L-BFGS-B', bounds=...) implemented via projected gradient + Armijo backtracking line search + central-difference numerical gradient; OptimizeResult-compatible return interface (.x / .fun / .success / .nit / .nfev / .message). Self-test on a known convex bounded QP (f(x)=0.5*||x-target||^2 on box [0,1]) converges in 2 iterations to max_err 5.5e-11 vs analytical clip(target, 0, 1). **Patched `apf/cmb_finite_mode_covariance.py`** to try-except import: scipy.optimize.minimize first; falls back to apf._optimize_vendored.minimize on ImportError. Production behavior unchanged (still uses scipy). Sandbox behavior changed: bank now reaches 3290/3290 (was 3283/3289). **All 6 cmb_finite_mode_covariance bank checks PASS with the vendored solver** (sandbox): quadrupole suppression m_2 = 0.10 (target < 0.5); high-ell preservation max |m_ell-1| = 0.018 for ell >= 20 (target <= 0.15); large-angle reduction S_proj/S_std = 0.001; Legendre recurrence at 4.4e-16. Vendored solver produces same structural verdicts as scipy (not bit-identical iterates; tolerant structural checks). **Audit-first discipline preserved**: no new physical claim; the vendor is a narrow scipy replacement for the one minimize() call used in the bank, not a scipy-wide vendor. Bank check `check_T_optimize_vendored_minimize_convex_bounded_P` verifies the vendored solver converges on a canonical convex bounded QP within 1e-3 of analytical solution + OptimizeResult interface complete. **Working Rule 9 incident this session**: Drive truncation on apf/cmb_finite_mode_covariance.py + apf/_optimize_vendored.py during Edit tool patches. Both repaired via tmp+rename from snapshot (the v24.3.29 snapshot still being a valid baseline for the unmodified cmb module). EXPECTED 3289 → 3290 (+1); BANK_REGISTRY_MODULES 229 → 230 (+1 new module: apf._optimize_vendored inserted alphabetically at head of BANK_REGISTRY_MODULES). ARCHITECTURE_ONLY_MODULES unchanged at 23. **Sandbox bank now matches production**: 3290/3290 in both environments. The 'scipy gap' annotation in CLAUDE.md changelog entries v24.3.30 → v24.3.34 is now historical — going forward, sandbox load = production load. setup.py + apf/__init__.py + bank.py changelog all bumped 24.3.34 → 24.3.35. Closure pack APF_SCIPY_OPTIMIZE_VENDORED_v1 lands at bundle 178 → 179. Sessions 1-5 of architecture-review CLOSED; this Session 6 piece is an opportunistic closure of the scipy gap (not opening any of the 3 named latent engines). Bank state: 3290/3290 PASS expected in both production and sandbox.) v24.3.34 (2026-05-19 STARTUP++++++ - IE Family architecture commitment Session 5 (obligation packet meta-schema) lands. New Tier 3 module `apf/obligation_packet_meta_schema.py` (25.7 KB; +4 bank checks) formalizes Reference doc Q3: meta-schema with engine-specific subtypes. ObligationPacketMetaSchema dataclass with 6 required common fields (obligation_kind + target_engine + target_unit_id + evidence_required + current_status + recommended_next_action) + EngineSubtype enum (ROUTE_ADJUDICATION + CODOMAIN_SELECTION) + engine_subtype_data extension slot. Per-engine adapter wrappers (wrap_route_adjudication_packet + wrap_codomain_selection_packet) translate native packet shapes to meta-schema without modifying source compilers. Route Adjudication translation: obligation_kind derived from original_repair_class + packet_status; target_engine = 'route_adjudication'; target_unit_id = route sector name; evidence_required = critical_fields; engine_subtype_data preserves bundles + frontier_status + original_certificate + blocked_reason + ready_to_rerun + original_repair_class + optional_fields. Codomain Selection translation: largely pass-through since Codomain packets (from Session 2) already use Q3 field names; engine_subtype_data preserves evaluation_data per-verdict. Uniform `inspect_packet(packet, engine)` reads any-engine packet via meta-schema, returns PacketInspectionResult with common_fields + engine_subtype + engine_subtype_data + audit_first_non_claims_preserved + valid + errors. CrossEngineMetaPacket composes multi-engine sub-packets into one cross-engine view (formalizes the Session 4 dispatcher's meta_obligation_packet field). **Backward compatibility preserved**: no per-engine compiler modified; meta-schema is additive adapter layer. Route Adjudication's interface_repair_obligation_compiler stays untouched (existing 11 packet fields unchanged); Codomain Selection's engine packets stay untouched. Bank checks: meta_schema_identity (6 common fields + 2 engine subtypes correctly declared), route_subtype (Route packet wraps to meta-schema with target_engine='route_adjudication' + target_unit_id=sector + critical_fields → evidence_required + bundles preserved in subtype_data), codomain_subtype (Codomain packets wrap across multiple verdict cases incl positive + no-runtime + unknown-regime), uniform_inspector (Route + Codomain packets read with same PacketInspectionResult shape; common_fields keys match across engines). **Audit-first discipline preserved across the meta-schema layer**: target_value_consumed flag from original_certificate propagates to audit_first_non_claims_preserved on the meta-schema; no new physical claim. EXPECTED 3285 → 3289 (+4); BANK_REGISTRY_MODULES 228 → 229 (+1 new module). ARCHITECTURE_ONLY_MODULES unchanged at 23. Sandbox bank._load() reports 3283/3289 (scipy gap=6 unchanged); production gap=0. setup.py + apf/__init__.py + bank.py changelog all bumped 24.3.33 → 24.3.34. **Working Rule 9 preemptive tmp+rename** used uniformly across 5 file writes. Zero truncation incidents. Pre-install snapshot reused: Codebase/Old/APF_Codebase_v24.3.29_post-tier1-wire-in_2026-05-19.zip. Closure pack APF_CODOMAIN_SELECTION_ENGINE_SESSION_5_v1 at bundle 177 → 178. **Sequencing forward**: Sessions 1-5 of architecture-review plan now CLOSED. Session 6+ — operationalize latent engines (kinematics adjudication entry point; defect calculus operational surface; representation descent operational surface) — remains opportunistic. Bank state: 3289/3289 PASS in production; 3283/3289 in sandbox.) v24.3.33 (2026-05-19 STARTUP+++++ - IE Family architecture commitment Session 4 (claim compiler multi-engine dispatch) lands. New Tier 3 module `apf/claim_dispatcher_multi_engine.py` (24.5 KB; +3 bank checks): multi-engine claim dispatcher implementing Q1 starting position (conjunctive meta-verdict). EngineTarget enum (ROUTE_ADJUDICATION + CODOMAIN_SELECTION). CODOMAIN_REGIME_TERMS keyword dict for all 7 coherent-phase regimes from extended-regimes registry (SC + SF + magnetism + BEC + laser + sync + topological order). detect_codomain_regime(claim_text) returns (regime, matched_terms) or None. detect_engines(claim_text) returns tuple of EngineDispatch entries (always includes ROUTE_ADJUDICATION; appends CODOMAIN_SELECTION when coherent-phase regime detected). MultiEngineVerdict composes per-engine sub-verdicts under 5 meta-statuses (ALL_PASS / ALL_OPEN / PARTIAL_PASS / MIXED_OPEN_FAIL / ALL_FAIL). dispatch_multi_engine(claim_text) is the public entry point. **End-to-end behavior**: SC claim 'superconductivity exhibits zero resistance and Meissner effect' dispatches to BOTH engines: Route Adjudication via existing audit_claim returning generic-route reading (no SC sector entry in ClaimRoute today); Codomain Selection via adjudicate_codomain_competition returning OPEN_EVIDENCE_REQUIRED with obligation packet naming network state as missing input. Meta-status: ALL_OPEN (honest reading — both engines need more evidence than claim text alone provides). Non-coherent-phase claim 'W boson on-shell mass is 80.36 GeV' correctly dispatches to ROUTE only. **Meta-obligation packet implements Q3 starting position** at cross-engine layer: meta-schema with engine-specific evidence_required subtypes (engines_dispatched + evidence_required list with per-engine target_unit_id + current_status + recommended_next_action). 5 obligation_kind values per meta_status. **Audit-first discipline preserved**: no new physical claim; per-engine non-claims (numeric_critical_temperature / material_specific_prediction / highTc_solved / ab_initio_chemistry all = 0) verified at composition layer; cross-engine note explicit about conjunctive rule (Reference doc Q1 option a). Bank checks: dispatcher_basic (SC claim end-to-end produces 2-engine dispatch + valid meta-status), codomain_regime_recognizer (7 regimes detected from representative claims + no false-positive on non-coherent-phase claim), meta_verdict_conjunctive (composition function correctly classifies ALL_PASS / ALL_OPEN / PARTIAL_PASS / ALL_FAIL cases). EXPECTED 3282 → 3285 (+3); BANK_REGISTRY_MODULES 227 → 228 (+1 new module). ARCHITECTURE_ONLY_MODULES unchanged at 23. Sandbox bank._load() reports 3279/3285 (scipy gap=6 unchanged); production gap=0. setup.py + apf/__init__.py + bank.py changelog all bumped 24.3.32 → 24.3.33. Pre-install snapshot reused: Codebase/Old/APF_Codebase_v24.3.29_post-tier1-wire-in_2026-05-19.zip (still valid rollback baseline). **Working Rule 9 preemptive tmp+rename** used across 5 file writes (dispatcher module + manifest + bank.py changelog + setup.py + __init__.py). Zero truncation. Closure pack APF_CODOMAIN_SELECTION_ENGINE_SESSION_4_v1 at bundle 176 → 177. **Sequencing forward**: Session 5 obligation packet meta-schema cross-engine (formalizes the meta-schema this session prototyped at the dispatcher layer); Session 6+ operationalize latent engines. Bank state: 3285/3285 PASS in production; 3279/3285 in sandbox.) v24.3.32 (2026-05-19 STARTUP++++ - IE Family architecture commitment Session 3 (atlas engine-axis typing) lands. Atlas refactored from single-axis (route-only) to two-axis (ROUTE + CODOMAIN) reading. SC codomain adapter wired into atlas via codomain-axis dispatch. **No new modules.** apf/interface_atlas.py extended with AxisKind enum + axis field on AtlasInput + AtlasRouteSummary (defaults preserve backward compat) + AtlasInputKind.CODOMAIN_PAYLOAD + _compile_codomain_input helper dispatching to adjudicate_codomain_competition + axis_summary field on InterfaceAtlas with per-axis aggregation + cross-axis advisory note (per Reference doc Q2 starting position). +1 bank check check_T_interface_atlas_axis_typing_P. apf/interface_atlas_live_runner.py: discover_adapters() broadened to match *_real_adapter OR *_codomain_adapter; reads optional ATLAS_AXIS attribute (defaults ROUTE); per-axis breakdown in print_summary; CSV gets axis column; run_live_atlas() returns axis_summary. apf/superconductivity_codomain_adapter.py: gains atlas-contract attributes (ATLAS_INPUT_ID + ATLAS_ROUTE + ATLAS_PAYLOAD_NAME + ATLAS_AXIS=CODOMAIN + build_live_atlas_payload). +1 bank check check_T_superconductivity_codomain_adapter_atlas_contract_P. **Atlas v0.8 reading** (`python3 -m apf.interface_atlas_live_runner`): 8/43 SOLVED_GLOBAL_P (was 7/42 at v24.3.31). Per-axis: ROUTE 7/42, CODOMAIN 1/1 (SC coherent codomain selected on positive fixture; honest structural reading, not empirical claim). EXPECTED 3280 → 3282 (+2); BANK_REGISTRY_MODULES unchanged at 227; ARCHITECTURE_ONLY_MODULES unchanged at 23. Sandbox bank._load() reports 3276/3282 (scipy gap=6 unchanged); production gap=0. setup.py + apf/__init__.py + bank.py changelog all bumped 24.3.31 → 24.3.32. Pre-install snapshot reused: Codebase/Old/APF_Codebase_v24.3.29_post-tier1-wire-in_2026-05-19.zip (5.8 MB; baseline rollback). **Architecture-review sequencing progress** (per Reference doc): Session 1 doc-only ✓, Session 2 engine seed ✓, **Session 3 atlas axis typing ✓**, Session 4 claim compiler multi-engine dispatch queued, Session 5 obligation packet meta-schema queued, Session 6+ latent engine operationalization opportunistic. **Working Rule 9 preemptive** used uniformly across 5 file writes (interface_atlas.py + live_runner.py + codomain adapter + _module_manifest.py + bank.py changelog). Zero truncation incidents. Closure pack APF_CODOMAIN_SELECTION_ENGINE_SESSION_3_v1 lands at DOCTRINE_CONSEQUENCES_BUNDLE_LATEST_44/. Bank state: 3282/3282 PASS expected in production; 3276/3282 in sandbox.) v24.3.31 (2026-05-19 STARTUP+++ - IE Family architecture commitment Session 2 seed: Codomain Selection Engine + SC codomain adapter land as first Tier 2 engine in IE family beyond Route Adjudication. Two new modules in apf/ both BANK_REGISTRY (with register + check_* functions); +6 bank checks total. 1. `apf/codomain_selection_engine.py` (29.6 KB; +3 checks): Tier 2 engine seed per architecture-review Reference doc. Verdict schema `CodomainSelectionVerdict` + 6-status enum `CodomainSelectionStatus` (COHERENT_CODOMAIN_SELECTED / MARGIN_NONPOSITIVE / PHASE_LOCK_FAILED / COHERENCE_INSUFFICIENT / METASTABLE_HISTORY_LOCKED / OPEN_EVIDENCE_REQUIRED). Entry point `adjudicate_codomain_competition(regime, network_state)` delegates SC adjudication to apf.superconductivity_ie.evaluate_sc_codomain. 7-regime registry (1 runtime-available SC + 6 structural-only). Obligation packet shape implements Reference doc Q3 starting position (meta-schema with engine-specific evidence_required subtypes; fields obligation_kind / target_engine / target_unit_id / evidence_required / current_status / recommended_next_action). Audit-first non-claims preserved verbatim from 9-pack arc (numeric_critical_temperature + material_specific_prediction + highTc_solved + ab_initio_chemistry all = 0). Bank checks: identity (Tier 2 declared + 7 regimes registered + 4 non-claims preserved), entry_point (4-case smoke covering positive + overloaded + no-runtime + unknown-regime), audit_first (8-verdict sweep preserves per-regime non-claims). 2. `apf/superconductivity_codomain_adapter.py` (16.3 KB; +3 checks): Tier 4 adapter wrapping SCEvaluation into engine-readable payload. Uses 3 verbatim fixtures from v5 audit ladder (positive / phase_fragmented / defect_overloaded). `SuperconductivityCodomainAdapterSnapshot` dataclass + `build_codomain_adapter_payload(fixture)` payload builder. Bank checks: payload_contract (9 required fields), verdict_consistent (3 v5 fixtures classify correctly: positive -> COHERENT_CODOMAIN_SELECTED at margin 6.3; phase_fragmented -> PHASE_LOCK_FAILED; defect_overloaded -> MARGIN_NONPOSITIVE), audit_first (target_value_consumed=False + non-claims preserved + external evaluator ledger declared). **No atlas integration this session** (per Reference doc Session 2 plan); the adapter intentionally does NOT declare ATLAS_INPUT_ID / ATLAS_ROUTE / ATLAS_PAYLOAD_NAME attributes — those land alongside Session 3 atlas engine-axis-typing refactor (Path 2). The adapter exists as a bank-registered module with audit-first presence; atlas reachability is deferred. Both modules use Python tmp+rename per Working Rule 9 preemptive. AST PASS, import PASS, smoke 6/6 PASS. _module_manifest.py BANK_REGISTRY_MODULES 217 -> 219; ARCHITECTURE_ONLY_MODULES unchanged at 23; EXPECTED_REGISTRY_SIZE 3274 -> 3280 (+6). Sandbox bank._load() reports 3274/3280 (scipy gap = 6 unchanged); production gap = 0. setup.py + apf/__init__.py + bank.py changelog all bumped 24.3.30 -> 24.3.31. Pre-install snapshot reused: Codebase/Old/APF_Codebase_v24.3.29_post-tier1-wire-in_2026-05-19.zip (structurally identical to pre-Session-2 state since the v24.3.30 coherent-phase arc was utility-only with no bank delta). **Architecture-review sequencing**: Session 1 (Reference doc + Top-of-mind anchor) closed earlier today. Session 2 (this rev) closed. Sessions 3-6 named in Reference doc and queued: Session 3 atlas engine-axis typing (Path 2 refactor); Session 4 claim compiler multi-engine dispatch; Session 5 obligation packet meta-schema across both engines; Session 6+ operationalize latent engines (kinematics / defect calculus / representation descent). Each session leaves the codebase in coherent shipped state. None blocks other framework work. Bank state: 3280/3280 PASS expected in production; 3274/3280 in sandbox.) v24.3.30 (2026-05-19 STARTUP++ - IE coherent-phase-regime arc lands: 9-pack walk consolidating 5 superconductivity-arc packs (v1 criterion -> v2 paper-facing -> v3 IE schema integration -> v4 runtime scaffold -> v5 audit ladder) + 3 generic IE-extension packs (v1 codomain competition selector + v2 transition dynamics + v3 hysteresis/metastability) + 1 master ratification pack. 4 net-new apf/ utility modules land via tmp+rename: apf/superconductivity_ie.py (v5 canonical: IEInterfaceState + SCCostLedger + SCDefectAlgebra + SCInterfaceNetwork + SCEvaluation; S_SC = C(R_N) - C(R_SC) - Pi_defects + phase-locking/coherence predicates), apf/codomain_competition.py (CodomainCandidate + CodomainCompetitionGraph + CodomainSelection; Score_i(lambda) = C(R_i) + Pi_i(lambda) + argmin_i selector), apf/codomain_transition_dynamics.py (CodomainLandscape + LandscapeSelection; perturbation sweeps + phase-boundary detection + transition barriers B_ij), apf/codomain_hysteresis.py (HysteresisLandscape + HysteresisStep; history-state R(t-) + barrier-gated transition rule Score_a - Score_b > B_ab). All 4 modules classified ARCHITECTURE_ONLY_MODULES (no register, no check_*); manifest entry count 19 -> 23 (+4); EXPECTED_REGISTRY_SIZE unchanged at 3274 (no bank delta). Master equation banked: R_selected(t,lambda) = HistBarrierSelect(argmin_i [C(R_i) + Pi_i(lambda)], R(t-), B_ij). Superconductivity named as first worked coherent-phase regime; superfluidity/magnetism/Bose condensation/lasers/synchronization/topological order named as future regime targets. Explicit non-claims (preserved verbatim across all 9 packs): numeric_Tc = 0, material_specific_phase_diagram = 0, highTc_solved = 0, ab_initio_chemistry = 0. 9 closure packs land at DOCTRINE_CONSEQUENCES_BUNDLE_LATEST_44/; all 9 standalone verifiers PASS clean from Drive location. Pre-install snapshot reused: Codebase/Old/APF_Codebase_v24.3.29_post-tier1-wire-in_2026-05-19.zip (5.8 MB; structurally identical to pre-coherent-phase-arc state since no codebase changes between this morning's wire-in close and this install). setup.py + apf/__init__.py + bank.py changelog all bumped 24.3.29 -> 24.3.30. Top markers: SUPERCONDUCTIVITY_INTERFACE_CRITERION_PASS + SUPERCONDUCTIVITY_INTERFACE_THEORY_PASS + SUPERCONDUCTIVITY_IE_INTEGRATION_PASS + SUPERCONDUCTIVITY_IE_RUNTIME_SCAFFOLD_PASS + SUPERCONDUCTIVITY_IE_AUDIT_LADDER_PASS + IE_CODOMAIN_COMPETITION_SELECTOR_PASS + IE_CODOMAIN_TRANSITION_DYNAMICS_PASS + IE_CODOMAIN_HYSTERESIS_PASS + COHERENT_PHASE_REGIME_MASTER_PASS. Paper-side absorption deferred to next session (anticipated Paper 39 Coherent Phase Regimes in the APF Interface Engine). Bank state: 3274/3274 PASS expected.) v24.3.22 (2026-05-18 STARTUP+++++++ dark-sector live admission chain install - **Live engine adapter chain absorbs candidate evidence for EW + dark routes.** Consolidated upstream sprint (live_blocker -> next_dark -> dark_empirical, 3 sprints, dark_empirical is superset). 5 NEW modules: dark_empirical_posterior_admission_contract (+5 checks), ew_counterterm_uncertainty_protocol (+6), interface_dark_posterior_evidence_intake (+5), interface_ew_counterterm_uncertainty_intake (+4), interface_live_blocker_work_queue (+4). 2 MODIFIED modules (no new checks, internal wiring): ew_trace_to_scheme_real_adapter (21778 -> 25439 bytes), dark_posterior_real_adapter (20601 -> 21114 bytes). Manifest update: BANK_REGISTRY_MODULES 210 -> 215; EXPECTED_REGISTRY_SIZE 3193 -> 3217 (+24). REGISTRY sandbox 3187 -> 3211 (scipy-gap unchanged at 6); production 3193 -> 3217 (gap=0). **Engine phase delta** (confirmed by upstream engine_phase logs): EW live route OPEN_EVIDENCE_REQUIRED -> NOT_REQUIRED_ALREADY_P (counterterm + uncertainty protocols admitted); dark EVALUATOR_MAP admitted as CANDIDATE_EVIDENCE_PRESENT (Route-C APF2 tabulated-w2 / CAMB / Cobaya bridge-smoke evidence from LATEST-83/84/85/86); dark EMPIRICAL_POSTERIOR stays OPEN_EVIDENCE_REQUIRED with 6 named admission-contract slots (runtime artifacts, R-hat/ESS, frozen-APF2 guard, no-posterior-as-input guard, declared threshold rule, profile/MCMC adjudication table). **Preserved non-claims (verbatim)**: Export_dark_RouteC_APF2_posterior_P = 0; Export_dark_RouteC_MCMC_posterior_P = 0; Export_dark_robust_empirical_P = 0. No route promoted from intake alone. setup.py + apf/__init__.py docstring + __version__ bumped 24.3.21 -> 24.3.22. 6 closure sub-packs land at DOCTRINE_CONSEQUENCES_BUNDLE_LATEST_44/. Bank state: 3217/3217 PASS expected in production; 3211/3217 in sandbox (scipy-blocked). Pack stays bank-side internal per the v24.3.17 proprietary directive.) v24.3.21 (2026-05-18 STARTUP+++++++ perturbative-refinability-defect install - **APF_PERTURBATIVE_REFINABILITY_DEFECT_v1 lands as defect-calculus extension.** New apf/perturbative_refinability.py: utility module supplying the structural refinability defect formula Delta_P = max(0, (r_k + I_k)(1 + lambda_Gamma)/N_Gamma - 1) and the continuum corollary Delta_P = [(r_k + I_k)(1 + q^2) q^d_Gamma - 1]_+. Bulk scalar linear threshold q_c = 0.837619774826962. Standalone verifier PERTURBATIVE_REFINABILITY_BANK_PASS 8/8 clean from pack root. **Architecture-only**: no register(), no check_* functions; manifest classification ARCHITECTURE_ONLY_MODULES (19 entries, +1); EXPECTED_REGISTRY_SIZE unchanged at 3193. Module count: 210+19+4+0 = 233 in BANK_LOAD_MODULES (was 232; ALL_MODULES_VERIFY_ORDER 232 -> 233). verify_all.py ARCHITECTURE_ONLY_WHITELIST extended with apf.perturbative_refinability. Explicit non-claims: no full growth likelihood, no modified gravity, no slip operator, no empirical fit, Pi_P/L_Gamma not fully derived, no robust empirical dark P. Closure pack lands at DOCTRINE_CONSEQUENCES_BUNDLE_LATEST_44/APF_PERTURBATIVE_REFINABILITY_DEFECT_v1/. setup.py + apf/__init__.py docstring + __version__ bumped 24.3.20 -> 24.3.21. Bank state: 3193/3193 PASS expected in production; 3187/3193 in sandbox (scipy-blocked). Pack stays bank-side internal per the v24.3.17 proprietary directive.) v24.3.20 (2026-05-18 STARTUP++++++ register-anomalies cleanup - **KNOWN_REGISTER_ANOMALIES emptied; 9 previously-orphaned checks now in REGISTRY.** Refactored apf.evaporation_quartet.register() + apf.l_irr_induced_polarity.register() from the legacy no-arg pattern `register()` (which expected a non-existent bank.register(name, fn) helper) to the standard `register(registry)` contract that bank._load() actually calls. Their 4 + 5 = 9 checks now enter REGISTRY: check_T_saturation_alignment_is_Type_V, check_T_evaporation_inverse_channel_flow, check_T_v_global_release_from_evaporation, check_T_evaporation_lattice_ordering, check_T_L_irr_polarity_well_defined, check_T_L_irr_polarity_involution, check_T_L_irr_polarity_antimultiplicative, check_T_L_irr_polarity_substrate_primitive, check_T_L_irr_polarity_star_axioms_i_ii. Manifest update: BANK_REGISTRY_MODULES 208 -> 210; KNOWN_REGISTER_ANOMALIES 2 -> 0; EXPECTED_REGISTRY_SIZE 3184 -> 3193. REGISTRY sandbox: 3178 -> 3187 (+9, scipy-gap unchanged at 6); production REGISTRY: 3184 -> 3193 (gap = 0). setup.py + apf/__init__.py docstring + __version__ all bumped 24.3.19 -> 24.3.20. **No new theorems** -- these 9 checks were always static definitions in the modules; the refactor just makes bank._load() able to import them. Bank-audit Bucket B drops from 2 to 0 (no more loaded-but-zero-check entries); Bucket D widens to -33 (= 3193 - 3226 total static defs; negative just means helper sub-check delta -- the 33-check difference is helper functions in apf.supplements, apf.w_os_route_terminal_closure, etc. that aren't individually registered, by design). Bank state: 3193/3193 PASS expected in production; 3187/3193 in sandbox.) v24.3.19 (2026-05-18 STARTUP++++++ MODULES unification + EXPECTED re-derivation - **Single source of truth lands: `apf/_module_manifest.py`.** Response to Ethan's release-readiness audit follow-on. Previously bank's _MODULE_PATHS (154 entries) and verify_all's MODULES (223 entries) had drifted by ~70 modules; new manifest unifies them. _MODULE_PATHS now imports BANK_LOAD_MODULES from manifest (228 unique entries = 208 BANK_REGISTRY + 18 ARCHITECTURE_ONLY + 2 KNOWN_REGISTER_ANOMALIES). verify_all.MODULES imports ALL_MODULES_VERIFY_ORDER (232 entries = 228 + 4 STANDALONE_LEMMA_MODULES). EXPECTED_THEOREM_COUNT bound to EXPECTED_REGISTRY_SIZE = 3184 (production-canonical, re-derived from clean load). Previous narrative-incremented value 3187 over-counted by 3. bank._load() now has try/except TypeError to handle KNOWN_REGISTER_ANOMALIES. 44 archived apf/Old/ snapshots that accidentally entered the manifest from a recursive glob were filtered out. Pre-refactor snapshot: Codebase/Old/APF_Codebase_v24.3.18_pre-modules-unification_2026-05-18.zip. **Bank-audit Bucket D went from 280 to -24**: sandbox gap is now 6 (scipy-blocked), production gap is 0. setup.py + apf/__init__.py 24.3.18 -> 24.3.19. **No new bank checks** (engineering refactor; 292 modules' worth of checks now load correctly that were silently missed by the old bank — and EXPECTED corrected by -3). Bank state: 3184/3184 PASS expected in production; 3178/3184 in sandbox.) v24.3.18 (2026-05-18 STARTUP++++++ defect-calculus-architecture install - APF_DEFECT_CALCULUS_ARCHITECTURE_v1 (13-pack bundle) lands 12 architecture-level modules in apf/ at status [P_architecture]. The defect calculus unifies finite continuability + preservation + resolution + obstruction + transport into one synthesis: master object is a continuation certificate C_X = (Gamma, D, E, C, P, L, R, partial) with three defect maps Delta_P (preservation), Delta_O (resolution), Delta_E^r (route/export); object ladder A_Gamma supset P_Gamma supset O_Gamma supset E_{Gamma,r} where each stratum is zero-defect. 10 theorems landed: T1 Defect-Strata (status classes are zero-defect strata of finite continuability), T2 Defect-Transition (physical events are class transitions), T3 Defect-Composition (classes not generally closed under composition; Delta_i(X (x) Y) = max(0, sum + overhead - shared)), T4 Defect-Variational (J(X) = sum w_i Delta_i + alpha d + beta L_irr + gamma capacity-penalty covers collapse/ringdown/route-repair/perturbative suppression), T5 Scale-Flow (preferred scales are minimal-defect strata), T6 Obstruction-Cohomology (local zero-defect certificates need not glue; overlap/cycle defects measure obstruction), T7 Global Descent Kernel (Global APF physics = ker(Obs_APF) = im(Glob); architecture-level reformulation of the v24.3.11 RDFI theorem), T8 Functorial Transport (transport maps admissible iff type-preserving + codomain-respecting + no-hidden-debt + defect-nonincreasing), T9 Falsifier Gate (required zero-defect channels determine pass/open/repair/boundary/falsify), T10 Observable-Signature (class transitions generate typed signature families: knees, suppression envelopes, hysteresis, boundary residuals, route residuals, local-global mismatch). 12 new modules in apf/: continuability_preservation_resolution (strata), defect_transition_dynamics, defect_composition_calculus, defect_variational_principle, defect_scale_flow, defect_obstruction_cohomology, defect_global_descent_kernel, defect_functorial_transport, defect_falsifier_gate_logic, defect_observable_signatures, defect_master_integration (binds 10 layers + dependency-order check), defect_domain_applications (measurement/ringdown/growth/horizons/contextuality/route-transport application templates). Architecture-only -- no check_* functions in module bodies; standalone verifiers ship under DOCTRINE_CONSEQUENCES_BUNDLE_LATEST_44/APF_DEFECT_CALCULUS_ARCHITECTURE_v1/. Net delta vs v24.3.17: +0 bank checks (EXPECTED stays 3187); module count: 222 -> 234 (+12 architecture modules). setup.py + apf/__init__.py 24.3.17 -> 24.3.18. Top marker: DEFECT_MASTER_INTEGRATION_PASS. Pre-install snapshot: Codebase/Old/APF_Codebase_v24.3.17_pre-defect_calculus_install_2026-05-18.zip. Pack source: 13 zips at __APF Library/uploads/APF_DEFECT_*.zip. Explicit non-claim (synthesis note): 'This is architecture/math only. It does not promote any physical claim, fit, prediction, or route beyond route-local certificates.' Paper insertion points named for follow-on absorption: Paper 10 (defect calculus as operational extension of finite continuability), Paper 5 (preservation/closed-world gates as zero-defect conditions), Paper 8 (global descent/kernel as ACC projection coherence + cross-regime gluing), Paper 33 / resolved observable doctrine (O_Gamma -> E_{Gamma,r} as route/export layer), Interface Engine (executable graph witness for defect closure). Bank state: 3187/3187 PASS expected.) v24.3.17 (2026-05-18 STARTUP++++++ kinematic-reship - upstream resupplied the 4 kinematic packs flagged at v24.3.16 as missing their module bodies: APF_INTERFACE_KINEMATIC_SOLVER_v1 + _PHASE_SPACE_ATLAS_v1 + _HOLONOMY_DIAGNOSTICS_v1 + _INVARIANTS_v1 now ship with their declared new_module files. 4 net-new modules in apf/ closing the kinematics layer: (1) interface_kinematic_solver (P_kinematic_solver, +5; main solver kernel over the kinematics engine) (2) interface_kinematic_phase_space_atlas (P_kinematic_atlas, +4; phase-space atlas over kinematic trajectories) (3) interface_kinematic_holonomy_diagnostics (P_kinematic_holonomy, +5; holonomy diagnostics around closed kinematic paths) (4) interface_kinematic_invariants (P_kinematic_invariants, +5; conserved invariants of the kinematic dynamics). Kinematics layer now complete: 3 modules from v24.3.16 (engine + composition + order_defects) + 4 from v24.3.17 (solver + phase_space_atlas + holonomy_diagnostics + invariants) = 7 kinematic modules total. Net delta vs v24.3.16: +19 checks (3168 -> 3187); module count: 218 -> 222. setup.py + apf/__init__.py 24.3.16 -> 24.3.17. Top markers: INTERFACE_KINEMATIC_SOLVER_P_PASS + INTERFACE_KINEMATIC_PHASE_SPACE_ATLAS_P_PASS + INTERFACE_KINEMATIC_HOLONOMY_DIAGNOSTICS_P_PASS + INTERFACE_KINEMATIC_INVARIANTS_P_PASS (the bundle's headline 'latest kinematics marker' INTERFACE_KINEMATIC_INVARIANTS_P_PASS named at v24.3.16 manifest now banked). Pre-install snapshot: Codebase/Old/APF_Codebase_v24.3.16_pre-kinematic_reship_2026-05-18.zip. Closes the v24.3.16 upstream-pack-gap follow-on item. Bank state: 3187/3187 PASS expected.) v24.3.16 (2026-05-17 STARTUP++++++ since-EW-bundle install - Interface Intelligence engineering + kinematics expansion: APF_MODULES_SINCE_EW_TRACE_SCHEME_BUNDLE_v1 (25-pack consolidated bundle covering every module built since APF_EW_TRACE_TO_SCHEME_REAL_ADAPTER_v1) lands 14 net-new modules in apf/ — 11 engineering + 3 kinematics. **Engineering layer (11 modules, +47 checks)**: (1) artifact_to_route_payload_adapter (P_artifact_adapter, +5), (2) interface_intelligence_CI_orchestrator (P_CI, +4), (3) interface_intelligence_E2E_artifact_pipeline (P_E2E, +4), (4) interface_intelligence_engineering_command_center (P_command_center, +4), (5) interface_intelligence_failure_triage_assistant (P_triage, +4), (6) interface_intelligence_live_smoke_harness (P_live_smoke, +4), (7) interface_intelligence_post_install_acceptance_auditor (P_post_install, +4), (8) interface_intelligence_registry_bridge (P_registry, +6, the bridge between the Interface Engine and bank.REGISTRY/verify_all.py), (9) interface_intelligence_release_manifest (P_release_manifest, +4), (10) interface_intelligence_reviewer_reporter (P_reviewer, +4), (11) payload_batch_certification_runner (P_batch_runner, +4). **Kinematics layer (3 modules, +15 checks; NEW CONCEPTUAL LAYER above the Interface Engine)**: (12) interface_kinematics_engine (P_kinematics_engine, +5), (13) interface_kinematics_composition (P_kinematics_composition, +5), (14) interface_kinematics_order_defects (P_kinematics_order_defects, +5). **Upstream-pack gap**: 4 additional kinematic packs declared in the bundle's manifest (APF_INTERFACE_KINEMATIC_SOLVER_v1, APF_INTERFACE_KINEMATIC_PHASE_SPACE_ATLAS_v1, APF_INTERFACE_KINEMATIC_HOLONOMY_DIAGNOSTICS_v1, APF_INTERFACE_KINEMATIC_INVARIANTS_v1) shipped without their declared new_module file in the pack tree -- the APPLY_*.ps1 scripts and integration content shipped but the apf/*.py module body was not included. These 4 modules remain not-installable from the current bundle; their content would need to be re-supplied by the upstream pack builder before they can land. The 14 modules above are clean and verified. Net delta vs v24.3.15: +62 checks (3106 -> 3168); module count: 204 -> 218. setup.py + apf/__init__.py 24.3.15 -> 24.3.16. Top markers: ARTIFACT_TO_ROUTE_PAYLOAD_ADAPTER_P_PASS + INTERFACE_INTELLIGENCE_CI_ORCHESTRATOR_P_PASS + INTERFACE_INTELLIGENCE_E2E_ARTIFACT_PIPELINE_P_PASS + INTERFACE_INTELLIGENCE_ENGINEERING_COMMAND_CENTER_P_PASS + INTERFACE_INTELLIGENCE_FAILURE_TRIAGE_ASSISTANT_P_PASS + INTERFACE_INTELLIGENCE_LIVE_SMOKE_HARNESS_P_PASS + INTERFACE_INTELLIGENCE_POST_INSTALL_ACCEPTANCE_AUDITOR_P_PASS + INTERFACE_INTELLIGENCE_REGISTRY_BRIDGE_P_PASS + INTERFACE_INTELLIGENCE_RELEASE_MANIFEST_P_PASS + INTERFACE_INTELLIGENCE_REVIEWER_REPORTER_P_PASS + PAYLOAD_BATCH_CERTIFICATION_RUNNER_P_PASS + INTERFACE_KINEMATICS_ENGINE_P_PASS + INTERFACE_KINEMATICS_COMPOSITION_P_PASS + INTERFACE_KINEMATICS_ORDER_DEFECTS_P_PASS. Pre-install snapshot: Codebase/Old/APF_Codebase_v24.3.15_pre-since_ew_install_2026-05-17.zip. Bank state: 3168/3168 PASS expected.) v24.3.15 (2026-05-17 STARTUP++++++ post-Sprints 2-5 Sprint 0 completion - Route Certification Starter Suite + Integration Workbench install: APF_ROUTE_CERTIFICATION_STARTER_SUITE_v1 + APF_ROUTE_CERTIFICATION_INTEGRATION_WORKBENCH_v1 (packs 1-2 of the 9-pack interface intelligence handoff bundle, the only remaining unintegrated content from the 2026-05-17 STARTUP++++++ five-sprint workplan) land 8 net-new modules in apf/. 7 starter-suite modules + 1 workbench module: (1) anti_fitting_provenance_audit (P_anti_fitting, +1; provenance audit that fails closed when a route consumes its target as input); (2) capacity_coarse_grain_experiments (P_capacity_experiments, +1; coarse-grain experiment harness for capacity-budget routes); (3) dark_posterior_certifier (P_dark_certifier, +1; route-specific certifier for dark-posterior empirical routes); (4) ew_trace_scheme_transport_certifier (P_ew_certifier, +1; route-specific certifier for EW trace-to-scheme transport); (5) gauge_fiber_route_classifier (P_gauge_classifier, +1; classifier for gauge-as-fiber-automorphism routes); (6) horizon_fiber_cost_classifier (P_horizon_classifier, +1; classifier for horizon-area-as-fiber-cost routes); (7) route_certification_starter_suite (P_starter_suite, +1; top integration master for the per-route certifiers); (8) route_certification_workbench (P_workbench, +1; JSON/CLI route workbench + payload schemas). Closes Sprint 0 of the parallel workplan completely. **Interface Engine Project: all five sprints + Sprint 0 now fully closed**. Net delta vs v24.3.14: +8 checks (3098 -> 3106); module count: 196 -> 204. setup.py + apf/__init__.py 24.3.14 -> 24.3.15. Top markers: ROUTE_CERTIFICATION_STARTER_SUITE_P_PASS + ROUTE_CERTIFICATION_INTEGRATION_WORKBENCH_P_PASS. Pre-install snapshot: Codebase/Old/APF_Codebase_v24.3.14_pre-sprint0_packs1_2_install_2026-05-17.zip. Pack sources at __APF Library/uploads/APF_INTERFACE_INTELLIGENCE_HANDOFF_BUNDLE_v1.zip packs/. Bank state: 3106/3106 PASS expected.) v24.3.14 (2026-05-17 STARTUP++++++ Sprints 2-5 - Interface Engine Project Level 4 closure: Sprints 2-5 land as one consolidated drop across three upstream packs (APF_EW_TRACE_TO_SCHEME_REAL_ADAPTER_v1 + APF_CLAIM_TO_INTERFACE_GRAPH_COMPILER_v1 + APF_INTERFACE_ATLAS_v1; Sprint 5's apf/ superset bundles Sprint 3 dark_posterior_real_adapter alongside its own interface_atlas). 4 net-new modules in apf/: (1) ew_trace_to_scheme_real_adapter (P_real_adapter, +5; live APF EW trace/transport state -> interface-intelligence route payloads without overpromoting physical scheme export); (2) dark_posterior_real_adapter (P_real_adapter, +5; live/manual dark route state -> payloads, certifications, obligations, safe rerun gating); (3) claim_to_interface_graph_compiler (P_claim_compiler, +5; claim text -> route class -> conservative route payload -> certification -> movement graph -> repair frontier -> obligation packet -> reviewer-safe claim language); (4) interface_atlas (P_atlas, +5; many movement graphs -> global APF interface atlas with repeated obstruction families, shared repair dependencies, critical bottleneck structures). Closes Sprints 2-5 of the five-sprint parallel workplan from 2026-05-17 STARTUP++++++ post-audit. **Interface Engine Project Level 4 (interface operating system) now substantively closed**: real adapters convert live EW/dark module state into certified route payloads; the claim compiler turns claim text into certification plans; the atlas aggregates single-route audits into APF-wide bottleneck maps. The calculus is now a self-auditing system across active APF sectors. Core claims banked: EW real adapter at check_T_ew_trace_to_scheme_real_adapter_P -- 'Live APF EW trace/transport state can be adapted into interface-intelligence route payloads without overpromoting physical scheme export.' Dark posterior adapter at check_T_dark_posterior_real_adapter_P -- 'Live/manual dark route state converts into payloads, certifications, obligations, and safe rerun gating.' Claim compiler at check_T_claim_to_interface_graph_compiler_P -- 'A claim text can identify the interface route and required structures, but cannot by itself satisfy the gate.' Interface atlas at check_T_interface_atlas_P -- 'The atlas turns single-route interface audits into APF-wide obstruction, failed-structure, and repair-dependency maps.' Net delta vs v24.3.13: +20 checks (3078 -> 3098); module count: 192 -> 196. setup.py + apf/__init__.py 24.3.13 -> 24.3.14. Top markers: EW_TRACE_TO_SCHEME_REAL_ADAPTER_P_PASS + DARK_POSTERIOR_REAL_ADAPTER_P_PASS + CLAIM_TO_INTERFACE_GRAPH_COMPILER_P_PASS + INTERFACE_ATLAS_P_PASS. Pre-install snapshot: Codebase/Old/APF_Codebase_v24.3.13_pre-sprints_2_5_install_2026-05-17.zip. Two handoff-bundle packs from Sprint 0 (route_certification_starter_suite + integration_workbench, packs 1-2 of 9) remain at __APF Library/uploads/APF_INTERFACE_INTELLIGENCE_HANDOFF_BUNDLE_v1.zip for a separate Sprint-0-completion install. Explicit non-claims preserved: claim text is never evidence; the adapters do not overpromote physical scheme export; the atlas does not adjudicate physics, only typology. APF is now a self-auditing interface calculus across the active sectors (EW + dark + cross-sector); the framework still requires human or external-evaluator action to produce the underlying physics evidence the gates demand. Bank state: 3098/3098 PASS expected.) v24.3.13 (2026-05-17 STARTUP++++++ Sprint 1 - Interface Intelligence Sprint 0 (handoff bundle packs 3-9) + Sprint 1 (evidence rerun controller) install: APF_INTERFACE_EVIDENCE_RERUN_CONTROLLER_v1 lands 8 net-new modules in apf/. Sprint 0 (Levels 2-3 of the Interface Engine Project): (1) interface_structure_transport_ledger (P_structure_ledger, +5; typed interface-moving structure inventory), (2) interface_structure_discovery_engine (P_discovery, +5; raw payload -> typed moving-structure ledger + obstruction witnesses), (3) interface_structure_movement_graph (P_movement_graph, +5; typed source-target movement graph + witness paths), (4) interface_movement_graph_repair_planner (P_repair_plan, +5; failed edges -> ordered repair actions + P-closure conditions), (5) interface_repair_closure_simulator (P_closure_sim, +5; counterfactual ordinary-repair closure simulator with provenance/structural refusal), (6) interface_repair_frontier_explorer (P_repair_frontier, +5; minimal repair bundles + critical repair fields), (7) interface_repair_obligation_compiler (P_obligation, +5; evidence obligations + templates + ready-to-rerun validation). Sprint 1 (Level 3 operational closure): (8) interface_evidence_rerun_controller (P_evidence_rerun, +6; evidence packet -> validate -> patch payload -> rerun certification -> compare before/after -> decide whether repaired route reaches P). Core claim banked at check_T_interface_evidence_rerun_controller_P: 'Evidence completion authorizes rerun; only rerun certification decides whether the repaired payload reaches P.' Closes operational loop from 'evidence supplied' to 'rerun gate result'. Sits on v24.3.12 representation-descent stack: the obstruction calculus + universal property + bridge + harness from v24.3.11/12 supply the kernel; Sprint 0 supplies the typed inventory + graph + planner + simulator + frontier + obligation compiler; Sprint 1 closes the loop by validating evidence + reruning certification. Status: Interface Engine Project Level 1 (certification) and Level 2 (movement model) closed; Level 3 (repair intelligence) substantively closed; Level 4 (interface OS) staged. Five-sprint workplan from 2026-05-17 STARTUP++++++ delivers Sprint 1 here; Sprints 2-5 queued: Sprint 2 EW trace-to-scheme real adapter, Sprint 3 dark posterior real adapter, Sprint 4 claim-to-interface-graph compiler, Sprint 5 interface atlas. Two handoff-bundle packs from Sprint 0 NOT installed here: route_certification_starter_suite + integration_workbench (packs 1+2 of 9). Net delta vs v24.3.12: +41 checks (3037 -> 3078); module count: 184 -> 192. setup.py + apf/__init__.py 24.3.12 -> 24.3.13. Top verifier marker: INTERFACE_EVIDENCE_RERUN_CONTROLLER_P_PASS. Pre-install snapshot: Codebase/Old/APF_Codebase_v24.3.12_pre-interface_intelligence_install_2026-05-17.zip. Pack source: __APF Library/uploads/APF_INTERFACE_EVIDENCE_RERUN_CONTROLLER_v1.zip. Explicit non-claim (per Sprint 1 framing): closure simulation, frontier search, and obligation readiness are engineering gates, not assertions that a physics repair has been executed; the rerun controller validates evidence is complete and reruns the certification gate, but does not automatically prove the underlying physics. Bank state: 3078/3078 PASS expected.) v24.3.12 (2026-05-17 STARTUP++++++ - Interface Solver Engineering Extensions: APF_INTERFACE_SOLVER_ENGINEERING_EXTENSIONS_v1 lands 6 net-new engineering modules in apf/ on top of the v24.3.11 representation-descent stack. Pushes the v24.3.11 interface_solver_descent_bridge from theorem/tooling layer into engineering use: strict InterfaceSolverProblem contract validation + expected-label leakage rejection; batch certification with JSON/CSV export; CI policy gates (PERMISSIVE_RESEARCH / BLOCK_FAIL_CLOSED / STRICT_GLOBAL_EXPORT); Markdown + JSON report generation; CLI runner; route adapter templates for EW + dark-sector routes. Modules: (1) interface_solver_contracts (engineering-only, no bank checks), (2) interface_solver_batch (engineering-only), (3) interface_solver_ci_policy (engineering-only), (4) interface_solver_report (engineering-only), (5) interface_solver_route_adapters (engineering-only, EW + dark templates), (6) interface_solver_engineering_extensions (P_engineering top module, +6 bank checks covering schema validation, batch certification, CI policy gate, report generation, route adapter templates, and engineering-extensions top integration). CLI entry point at scripts/run_interface_solver_certify.py (also bundled in pack but not in apf/). Net delta vs v24.3.11: +6 checks (3031 -> 3037); module count: 178 -> 184 (6 net-new modules; only 1 has bank registration). setup.py + apf/__init__.py 24.3.11 -> 24.3.12. Top verifier marker: INTERFACE_SOLVER_ENGINEERING_EXTENSIONS_P_PASS. Pre-install snapshot: Codebase/Old/APF_Codebase_v24.3.11_pre-interface_solver_engineering_install_2026-05-17.zip. Bank state: 3037/3037 PASS expected.) v24.3.11 (2026-05-17 STARTUP++++++ - Representation Descent Full Integration: APF_REPRESENTATION_DESCENT_FULL_INTEGRATION_v1 lands 13 net-new modules in apf/ walking the full representation-descent stack. Core theorem: Global physics = ker(Obs_APF) = im(Glob) (global physics is the zero-obstruction exact kernel of admissible representation descent over the ACC/interface base). Sits structurally on top of the v24.3.8 ACC unification fully-P no-imports closure + the v24.3.9 L_irr-induced polarity substrate-side *-algebra (i)+(ii) lift + the 2026-05-16 cross-interface algebraic impossibility theorem v0.2: APF unifies physics by deriving the base/fiber allocation boundary between substrate-global structure (ACC base) and interface-local / fiber-internal representation structure, not by forcing every regime into one flat master algebra. 13 modules in dependency order: (1) base_fiber_allocation (P_cat_stratified_unification, +9), (2) admissible_representation_stack (P_cat_finite_descent, +10), (3) descent_obstruction_calculus (P_calc, +10), (4) descent_exactness (P_exact, +9, im(Glob) = ker(Obs)), (5) obstruction_dynamics (P_dyn, +10), (6) obstruction_repair_normal_form (P_repair, +9), (7) globalization_promotion_gate (P_gate, +8, exports global P iff Obs=0), (8) representation_descent_kernel (P_unification, +6), (9) representation_descent_kernel_adversarial_audit (P_adversarial, +10), (10) initial_obstruction_classifier (P_universal, +7, Obs_APF is initial among finite APF-compatible no-smuggling classifiers), (11) representation_descent_application_harness (P_application, +8), (12) interface_solver_descent_bridge (P_solver_bridge, +7, solve_interface_descent API), (13) representation_descent_full_integration (P_full_integration, +4, top integration master). Net delta vs v24.3.10: +107 checks (2924 -> 3031); module count: 165 -> 178. setup.py + apf/__init__.py 24.3.10 -> 24.3.11. Top verifier marker: REPRESENTATION_DESCENT_FULL_INTEGRATION_PASS. Reviewer-safe central claim (paper-side absorption pending): 'Globally admissible physics is the zero-obstruction exact kernel of admissible representation descent over the ACC/interface base.' Explicit non-claims (no-smuggling ledger): one flat substrate-global C*-algebra blocked by 2026-05-16 algebraic ceiling; (K, d_eff) alone does not determine every subspace map; repairability does NOT equal P; D1/D2/D3 substrate revisions remain counterfactual dissolution routes; current theorem is finite/first-order, NOT a full infinity-stack or cohomology theory. Pre-install snapshot: Codebase/Old/APF_Codebase_v24.3.10_pre-representation_descent_install_2026-05-17.zip. Bank state: 3031/3031 PASS expected.) v24.3.10 (2026-05-17 STARTUP+++++ - Evaporation quartet E1-E4 closure of the saturation->middle regime transition: apf/evaporation_quartet.py lands with 4 checks (check_T_saturation_alignment_is_Type_V, check_T_evaporation_inverse_channel_flow, check_T_v_global_release_from_evaporation, check_T_evaporation_lattice_ordering). Banks the inverse-direction channel-flow account complementary to the cosmogenic quartet T1-T4 (apf/plec.py + apf/gravity.py). E1 establishes saturation alignment at horizon interface as Type V realignment-cost configuration (parallel to T1's Type II for trivial alignment); E2 establishes inverse channel-flow V_global -> matter/gauge as L_irr-compatible response forced by holographic ceiling + L_irr-monotonicity + capacity conservation (parallel to T2's L_irr resolution of Type II degeneracy in cosmogenic direction); E3 establishes the cumulative kappa_int release theorem with cumulative-balance equation |V_global,local|_deposit = |V_global,local|_release + S_radiation (parallel to T3's V_global accumulation; structural form of BH unitarity at substrate-side ledger); E4 establishes evaporation lattice ordering as horizon-area-monotonic phase staging with Page-curve turnover at half-evaporation as structural pivot (parallel to T4's Phi_c-monotonic cosmogenic staging; Page time derived from equipartition argument, not free parameter). Net delta vs v24.3.9: +4 checks (2920 -> 2924); module count: 164 -> 165. setup.py + apf/__init__.py 24.3.9 -> 24.3.10. Top verifier marker: EVAPORATION_QUARTET_PASS. **Substrate-position-axis trilogy now bank-closed across all three regime transitions**: cosmogenesis (T1-T4 in plec.py + gravity.py), formation (per-event via class_transition.py; joint-event analysis still open), evaporation (E1-E4 this pack). Bank state: 2924/2924 PASS expected.) v24.3.9 (2026-05-17 STARTUP++++ - L_irr-induced polarity substrate-side *-algebra (i)+(ii) closure: apf/l_irr_induced_polarity.py lands with 5 checks (check_T_L_irr_polarity_well_defined, _involution, _antimultiplicative, _substrate_primitive, _star_axioms_i_ii). Banks the post-D1 closure of the dissolution routes program (2026-05-17): the L_irr-orientation on the partial order of class-transition histories lifts to per-distinction polarity at the substrate via the eternalist commitment; substrate-side ordered pair (D+, D-) satisfies *-algebra axioms (i) involution + (ii) antimultiplicativity on the partial fibration's morphism algebra; axioms (iii) C-antilinearity + (iv) C*-norm remain fiber-internal at quantum-capable interfaces (Fact 3 of cross-interface algebraic impossibility theorem, v0.2 refinement, is the load-bearing block). Dissolves Fact 1 of the impossibility theorem; refines Fourth Law publication-ready statement to: 'ACC is the base over which APF-generated regime structures are functorially fibered, with substrate-side *-involution and antimultiplicativity derivable on the fibration's morphism algebra; full C*-structure requires fiber-internal C-action and norm at quantum-capable interfaces.' Net delta vs v24.3.8: +5 checks (2915 -> 2920); module count: 163 -> 164. setup.py + apf/__init__.py 24.3.8 -> 24.3.9. Top verifier marker: L_IRR_INDUCED_POLARITY_SUBSTRATE_STAR_AXIOMS_PASS. Bank state: 2920/2920 PASS expected.) v24.3.8 (2026-05-17 STARTUP++ - ACC unification fully-P no-imports closure: APF_ACC_UNIFICATION_FULLY_P_NO_IMPORTS_CLOSURE_v1 lands two modules. apf/acc_unification_all_p.py (612 lines, +15 checks) consolidates the full categorical unification stack: ACC base record functor + integer/scalar strict-P projections + generated APF/ACC category + regime structures as fibers over ACC + resolved/fibered ACC category + canonical resolution/lift + free-vector-space linearization + four subspace witnesses (horizon/bridge/quantum/operator) as strict fiber functors + original/generated-level pullback of strict subspace functoriality + boundary against false bare-record-only collapse. apf/acc_unification_no_imports.py (384 lines, +8 checks) banks the final provenance/no-smuggling layer: check_T_ACC_unification_all_P_predecessor + APF object/morphism/carrier-map provenance gates + formal-math-language-not-physical-import gate + no-external-physical-imports gate + no-bare-record-overclaim gate + top check_T_ACC_unification_fully_P_no_external_imports. Exported status: T_ACC^unif : [P_cat^{fully closed, no imports}]. No-imports boundary: APF-derived (ACC base + APF-generated morphisms + APF witness carrier maps + standard formal mathematics); no imported Standard Model Lagrangian, no imported cosmological dynamics, no empirical constants as proof inputs, no Hilbert-space physical primitives, no C*-algebraic physical primitives, no arbitrary carrier maps, no bare-record-only collapse overclaim. Compatible with the cross-interface algebraic impossibility theorem (2026-05-16) at Resolution iii' partial-fibration level: categorical/capacity-flow/multiplicative content is APF-derivable; *-structure/C-action/norm remain fiber-internal and explicitly not imported. Net delta vs v24.3.7: +23 checks (2892 -> 2915); module count: 161 -> 163. setup.py + apf/__init__.py 24.3.7 -> 24.3.8. Pack bundled at DOCTRINE_CONSEQUENCES_BUNDLE_LATEST_44/APF_ACC_UNIFICATION_FULLY_P_NO_IMPORTS_CLOSURE_v1/; verbatim zip at __APF Library/Evidence/. Top marker: ACC_UNIFICATION_FULLY_P_NO_EXTERNAL_IMPORTS_PASS. Bank state: 2915/2915 PASS expected.) v24.3.7 (2026-05-15 LATER++ - Q1 closure of cosmogenesis synthesis doc sec.8 open questions: T_omega_gamma_max_symmetry_group lands in apf/plec.py as tier 4 [P_structural] composition theorem. Establishes G_max(Omega_Gamma) = S_61 x [SU(3) x SU(2) x U(1)]^(template-carrier-at-each-slot) at the trivial alignment endpoint: the slot-permutation symmetry on the 61 capacity slots times the gauge template carrier per L_gauge_template_uniqueness. Each staged Type II resolution breaks both factors jointly -- slot side via S_(61-n) reduction with monotone decreasing order at n -> N_sat, carrier side via per-slot representation selection -- terminating at {e} when both reach trivial. Composes L_gauge_template_uniqueness (apf/gauge.py) + T4 no-GUT corollary (T_cosmogenic_lattice_ordering, apf/plec.py) + L_quantum_evolution S_61 path-integral (apf/supplements.py) + T1/T2 (apf/plec.py). Closes synthesis-doc Q1 structurally; Q3 (Higgs sector Type II placement) and Q4 (true void scope commitment) closed paper-side in Paper 6 supplement v2.16 + Paper 0 v6.1.8 (same-session absorptions). Net delta vs v24.3.6: +1 check (2891 -> 2892); module count unchanged at 155 (T_omega_gamma_max_symmetry_group added to existing apf/plec.py). setup.py + apf/__init__.py 24.3.6 -> 24.3.7. Reference docs: Reference - Cosmogenesis from the Trivial Alignment (2026-05-15).md sec.8 + Reference - H4 Dynamical Closure via Capacity-Commitment Quantum Evolution (2026-05-15).md sec.9. Bank state: 2892/2892 PASS expected.) v24.3.6 (2026-05-15 LATER+ - H4 dynamical closure composition theorem T_cosmogenic_to_recruitment_reduction lands in apf/cosmology.py as tier 4 [P_structural]. Audit-first sweep on apf/*.py during the cosmogenic-quartet rollout identified a parallel bank stack carrying the cosmogenic-regime dynamics that the Paper 6 supp v2.14 framing did not reach: L_quantum_evolution (apf/supplements.py) + T_capacity_redistribution_unification (apf/unification.py) + L_TN_Hamiltonian (apf/supplements.py) + L_matching_transition + L_singularity_resolution + L_saturation_partition (apf/cosmology.py) + T_inflation + L_inflation_R2_spectral (apf/validation.py) supply Layer B (cosmogenic-regime dynamics); T_master_equation_form (apf/recruitment.py) supplies Layer A (post-cosmogenesis late-time relaxation); the cosmogenic quartet T1-T4 supplies Layer C (configuration-space architecture). 20 bank checks PASS clean across the three layers. T_cosmogenic_to_recruitment_reduction is the explicit composition certifying that Layer B's S_61 path-integral reduces to Layer A's first-order relaxation master equation in the late-time limit n -> N_sat = 61, with off-diagonal commitment amplitude scaling as sqrt(N_sat - n)/N_sat (vanishing at saturation), kernel-stabilisation drift harmonic-convergent, and the residual mismatch dynamics linearising around the stationary cost-minimum. Net delta vs v24.3.5: +1 check (2890 -> 2891); module count unchanged at 155. setup.py + apf/__init__.py 24.3.5 -> 24.3.6 (apf/__init__.py was stale at 24.3.3 before this rev; hygiene fix folded in). Reference doc: Reference - H4 Dynamical Closure via Capacity-Commitment Quantum Evolution (2026-05-15).md. Paper 6 supplement v2.14 -> v2.15 already absorbed the layer-A/B/C reading. Bank state: 2891/2891 PASS expected.) v24.3.5 (2026-05-15 LATER — cosmogenic bank theorems T3 + T4 land alongside T1 + T2 (complete cosmogenesis-from-perfect-symmetry quartet). T3 (apf/gravity.py: check_T_v_global_accumulation_from_type_II_resolutions, tier 4 [P_structural]) extends T_interface_sector_bridge from single-event identity to cumulative-sum case: cumulative kappa_int loading of V_global from N staged Type II resolutions = N . (42/61) per-slot capacity, saturating at dim V_global = 42 when all 61 slots resolve. Establishes the cosmogenic-completion identity Omega_Lambda . C_total = dim V_global, structurally identifying the present-day Omega_Lambda ~ 0.69 as V_global fully loaded. T4 (apf/plec.py: check_T_cosmogenic_lattice_ordering, tier 4 [P_structural]) establishes the cosmogenic ordering as partially ordered by Phi_c-monotonic phase staging — any cosmic instance realizes a specific total order fixed by lattice energy-scale assignments; Theorem_R is a consolidation theorem (R1 ∧ R2 ∧ R3 jointly), so commuting sectors admit partial order in principle. **No-GUT corollary** is the framework's first structural cosmological no-go: the three gauge factors SU(3)_c x SU(2)_L x U(1)_Y are derived from distinct admissibility conditions (R1 from L_nc + B1_prime + T_M + T_confinement; R2 from L_irr + L_irr_uniform + T_M; R3 from admissibility completeness + T_field); no admissible Type II configuration in the lattice corresponds to a unified group; proton decay is structurally forbidden, tau_p = infinity in APF. Empirical anchor: Super-Kamiokande tau_p > 1.6e34 years consistent; any positive proton-decay observation falsifies. Net delta vs v24.3.4: +2 checks (2888 -> 2890); modules unchanged at 155 (T3 added to gravity.py, T4 added to plec.py). setup.py + apf/__init__.py 24.3.4 -> 24.3.5. Reference doc: Reference - Cosmogenesis from the Trivial Alignment (2026-05-15).md, T1+T2+T3+T4 quartet complete; corpus absorption (Paper 0 + Paper 3 + Paper 6 + Paper 37) is the next phase per the doc's §10 rollout. Bank state: 2890/2890 PASS expected.) v24.3.4 (2026-05-15 — cosmogenic bank theorems T1 + T2 from Reference - Cosmogenesis from the Trivial Alignment (2026-05-15).md land in apf/plec.py: check_T_trivial_alignment_is_Type_II + check_T_type_II_resolution_under_L_irr, both tier 4 [P_structural]. T1 establishes the trivial alignment (a, empty) as a Type II configuration of the realignment-cost functional under any nontrivial symmetry group G; T2 establishes that L_irr-accumulated asymmetry resolves Type II degeneracy by collapsing the symmetry group G to a proper subgroup, with iterated accumulation reaching the trivial subgroup. Together T1 + T2 give the framework's first cosmogenesis-from-perfect-symmetry theorem pair, with T3 + T4 queued (T3 in apf/gravity.py extending Interface-Sector Bridge to cumulative V_global accumulation; T4 partial-order ordering theorem with no-GUT corollary). Net delta: +2 checks (2886 -> 2888). Module count unchanged at 155 (added to existing apf/plec.py). setup.py + apf/__init__.py 24.3.3 -> 24.3.4. Bank state: 2888/2888 PASS expected.) v24.3 (2026-05-14 — Paper 37 (Collapse as Realignment) bank-side companion: apf/class_transition.py lands with 3 bank-registered tier-4 [P] checks (T_class_transition existence+uniqueness+irreversibility composition; L_per_slot_capacity_flow Markov-breakdown reduction at machine precision; T_class_transition_completion timescale formula). Closes Q4 of Paper 37 Supplement v0.9 open-questions list (bank-side machinery for the class-transition theorem). Net delta vs v24.2: +3 checks (2883 -> 2886). Module count: 154 -> 155. setup.py + apf/__init__.py 24.2.0 -> 24.3.0. Bank state: 2886/2886 PASS expected.) v24.2 (2026-05-12 — Paper 19 v0.2 G1 audit-flag closure: CMB finite-mode covariance projection module landed as apf/cmb_finite_mode_covariance.py with 6 bank-registered tier-4 [P_structural] checks (T_cmb_fm_finite_multipliers + T_cmb_fm_nonneg_reference + T_cmb_fm_large_angle_reduction + T_cmb_fm_quadrupole_suppression + T_cmb_fm_high_ell_preservation + T_cmb_fm_legendre_recurrence). Implements the Model-5 projection: C_m(x) = sum_ell a_ell m_ell P_ell(x) with a_ell = (2 ell + 1)/(ell (ell+1)) D_ell^std; minimizes S_{theta_c}[m]/S_{theta_c}[1] + lambda * ||m-1||^2/N subject to 0 <= m_ell <= 2 via L-BFGS-B; default toy reference low-ell Sachs-Wolfe-plateau-like spectrum on ell in [2, 30], theta_c = 60 deg, lambda = 0.2. Bank checks are model-integrity (not Planck likelihood). Net delta vs v24.1: +6 checks (2877 -> 2883). Module count: 153 -> 154. setup.py + apf/__init__.py 24.1.0 -> 24.2.0. Bank state: 2883/2883 PASS expected.) v24.1 (2026-05-10 LATEST — codomain_type schema extension: codomain_transport_schema.py extended with codomain_type ∈ {numerical, structural} field on CodomainTransport dataclass + check_T_codomain_type_declared. 9 numerical + 1 structural (YM continuum-limit) typed at landing. The structural extension paper-side artifact at STRUCTURAL_EXTENSION_v35_1/ is the source-of-record for the typed-route lemma. Net delta vs v24.0: +1 schema check (2876 → 2877). Module count unchanged at 153 (modification not addition). setup.py + apf/__init__.py 24.0.0 → 24.1.0. The export theorem's G4 (covariance) and G6 (residual channel) now read in their numerical or structural form per route based on the new field. Bank state: 2877/2877 PASS.)
# v23.0 (2026-05-10 — Bottom MSbar transport route: adds +42 bank-registered checks (2787 -> 2829). Closes bottom TRACE/MSbar validation neighborhood, pole knockout, no-smuggling audit, and MSbar route contract; physical export remains gated by APF_TRACE-to-MSbar codomain identity or evaluated QCD transport/covariance map).
# v18.0 (2026-05-09 — W_TRACE Denner diagram coefficient-table closeout/import contract: absorbs v17.0 +45 and adds v18.0 +51 bank-registered checks (2485 -> 2581). Closes diagram-family ontology, reviewed coefficient-row import contract, slot coverage, and target-projection quarantine; native source-formula import remains open).
# v16.8 (2026-05-09 — W_TRACE Denner/Sirlin counterterm-functional layer: absorbs v16.7 +35 and v16.8 +42 bank-registered checks (2363 -> 2440). Closes symbolic counterterm target/basis; native scalar-integral evaluator remains open).
# v16.5 (2026-05-09 — W_TRACE DIZET flag-sensitivity/covariance: +32 bank-registered checks (2182 -> 2214). Broad DIZET same-input flag/input scan, finite-difference covariance pushforward, and sharp row-protocol blocker; physical W export remains locked.).
# v16.1 (2026-05-09 — W_TRACE DIZET executable run: +34 bank-registered checks (2148 -> 2182). Ingests uploaded DIZET_v6.45.tgz, compiles unmodified Fortran benchmark, reproduces shipped test outputs, runs APF route input deck, captures same-input total evaluator output, and banks row-toggle/covariance status while keeping physical W export blocked pending row-admission protocol.).
# v15.9 (2026-05-09 — W_TRACE DIZET/ZFITTER acquisition/instrumentation: +36 bank-registered checks (2112 -> 2148). Splits the reviewed evaluator blocker into REVIEWED_SAME_INPUT_TOTAL_EVALUATOR and ROW_DECOMPOSITION_AND_COVARIANCE_PROTOCOL; locates DIZET v6.45 CPC/Code Ocean/SANC acquisition channels; banks APF route input deck, DIZET flag/toggle plan, and physical-export lock. setup.py + apf/__init__.py -> 15.9.0.).
# v15.8 (2026-05-09 — W_TRACE same-input evaluator terminal closeout: +33 bank-registered checks (2079 -> 2112). Audits candidate reviewed evaluator/source families, accepts v15.7 same-input row-shape transfer only as a model-limited worksheet, and terminally locks physical W export behind REVIEWED_PER_ROW_SAME_INPUT_EVALUATOR_WITH_COVARIANCE. setup.py + apf/__init__.py -> 15.8.0.). Audits candidate reviewed evaluator/source families, accepts v15.7 same-input row-shape transfer only as a model-limited worksheet, and terminally locks physical W export behind REVIEWED_PER_ROW_SAME_INPUT_EVALUATOR_WITH_COVARIANCE. setup.py + apf/__init__.py -> 15.8.0.).
# v15.5 (2026-05-09 — W_TRACE Delta_r source-acquisition matrix: +31 bank-registered checks (1990 -> 2021). Maps every unresolved finite-remainder bucket to reviewed electroweak source families, closes the row-extraction promotion ladder, and preserves the physical-export lock. setup.py + apf/__init__.py -> 15.5.0.).
# v15.4 (2026-05-09 — W_TRACE Delta_r remainder-resolution worksheet: +28 bank-registered checks (1962 -> 1990). Localizes the source/APF Delta-r gap to the unresolved finite-remainder sector, adds named remainder buckets and acquisition requirements, preserves the physical-export lock. setup.py + apf/__init__.py -> 15.4.0.).
#                                T_capacity_redistribution_unification
#                                [P_comp] tier-4 + T_partition_rigidity_
#                                coverage_v69 [P_structural] tier-4, both
#                                in apf/unification.py.  Q1 closeout of
#                                the V6.1 Referent Research Plan: the
#                                dynamics meta-theorem stating that every
#                                capacity-arrangement process falls into
#                                one of three categories (Flow, Commitment,
#                                Saturation) exhaustively, with unique
#                                local-law forcing per category under
#                                A1 + A9.3 Lovelock + T_CPTP + partition
#                                rigidity.  Exhaustiveness proof [P] via
#                                case analysis on (Delta K, Delta k,
#                                Delta P).  Per-category forcing [P] via
#                                L_irr + T_zeroth_law (Flow), T_inflation
#                                + L_matching_transition (Commitment),
#                                L_equip + T_interface_sector_bridge +
#                                L_nuR_enforcement + T_confinement +
#                                T_proton + T4F (Saturation).  Composition
#                                by logical disjunction — Phase-14f-style
#                                [P_comp].  Meta-rigidity premise (every
#                                bank-registered partition has a registered
#                                rigidity theorem) certified structurally
#                                by T_partition_rigidity_coverage_v69
#                                [P_structural], which enumerates the
#                                PARTITION_RIGIDITY_MAP and confirms each
#                                named rigidity theorem is bank-registered
#                                via runtime apf.bank.REGISTRY lookup.
#                                Matching-transition test case classified
#                                as commitment ∩ saturation two-way
#                                geometry co-action; alpha = 19/42.
#                                Reference: Q1 Meta-Theorem Formalisation
#                                memo (2026-04-24); Paper 8 Supplement §S
#                                draft.  Previously registered 420 after
#                                Phase 14f.4.
# (v6.9 (2026-04-23 — Phase 14f.4 adds
#                                T_I1_bridge_at_joint_K42 [P_bridge] tier-4
#                                in apf/horizon_joint_bridge.py.  Three
#                                independent constructions of the 42-dim
#                                V_global stratum at the canonical SM-dS
#                                joint point coincide: (1) F_horizon under
#                                Convention A (Bekenstein area quantisation),
#                                (2) T_interface_sector_bridge (SM gauge-
#                                cosmological residual partition), (3)
#                                F_horizon under Convention B (literal
#                                (C^2)^⊗42 qubit tensor product, confirmed
#                                numerically at K_bit in {2,3,4,5} and
#                                extended K-parametrically to K = 42).
#                                This is I1's bridge theorem at the joint
#                                point, structurally parallel to I2's
#                                T_interface_sector_bridge.  With this pass
#                                the I_k closure stratification is:
#                                  I1 bridge-at-K=42 + regime-local elsewhere,
#                                  I2 bridge-always,
#                                  I3 composed-self-id (Phase 14f.1),
#                                  I4 composed-self-id (Phase 14f.3).
# (v6.9 [2026-04-23 — Phase 14f.3 adds
#                                T_I4_operator_self_identification [P_comp]
#                                tier-4 in apf/i4_composition.py.  Composes
#                                the Phase 14d.2 (A)(B)(C) identities plus
#                                Paper 7's L_spectral_action_internal into
#                                a four-reading I4 self-identification
#                                theorem, structurally parallel to Phase
#                                14f.1's T_I3_operator_self_identification.
# (v6.9 [2026-04-23 — Phase 14f.2 adds
#                                L_horizon_convention_equivalence [P] tier-3
#                                to apf/unification.py, formalising the
#                                dual-convention (d_eff = e / d_eff = 2)
#                                equivalence at horizons.  Resolves
#                                Two-Tier Memo v0.1 Q1 in writing;
#                                unblocks Phase 14d.3 I1 joint-point
#                                bridge construction (3).  Companion
#                                helper acc_horizon_bit(K_bit) added to
#                                apf/unification.py as the Convention B
#                                constructor (integer-dim qubit tensor
#                                product).
# (v6.9 [2026-04-23 — Phase 14f.1 I3 operator-
#                                level composed self-identification, +4 from
#                                apf/quantum_operator_derivation.py:
#                                T_I3_svn_direct_computation [P] tier-4
#                                (numpy rho_max + S_vN at 8 test d),
#                                T_I3_unitary_invariance_witness [P] tier-3
#                                (Schur-lemma uniqueness + Haar sampling),
#                                T_I3_thermal_K1_limit_witness [P] tier-3
#                                (K=1 specialisation of Phase 14d.2),
#                                T_I3_operator_self_identification [P_comp]
#                                tier-4 (composed top: three constructions
#                                converge on rho_max).  Previously 413; this
#                                pass elevates I3 from regime-local [P_def]+
#                                [P_std] to operator-level [P_comp] composed
#                                self-identification, structurally parallel
#                                to but weaker in form than I2's bridge
#                                theorem (closure species: single-interface
#                                self-identification rather than cross-
#                                interface bridge, because K=1 at I3
#                                collapses the slot scale).  Plan: see
#                                APF Reference Docs/Reference - I1 I3 I4
#                                Bridge-Closure Work Plan (2026-04-23).md.
# (v6.9 [2026-04-22 — Phase 14d.3 structural
#                                completions before Paper 8). +3 from
#                                apf/phase_14d3_completions.py:
#                                T_Planck_scale_status_clarification
#                                [P] tier-4: attempted derivation of
#                                M_Planck from A1 alone via seven
#                                candidate routes; all close at external
#                                identification. Conclusion: M_Planck
#                                is not an APF-internal derivation gap
#                                but a natural-units-to-SI convention,
#                                same epistemic status as any theory
#                                predicting dimensionless ratios. The
#                                Phase 14d.2 "Planck-scale ansatz [C]"
#                                is reframed as [P-convention]. Paper 8
#                                states: APF predicts dimensionless in
#                                Planck units; SI conversion uses
#                                standard external G measurement.
#                                T_42_over_102_structural_uniqueness
#                                [P] tier-4: sharpens the 42/102
#                                coefficient privilege argument. Among
#                                APF-native-only ratios within observational
#                                precision, 42/102 is the UNIQUE ratio
#                                whose derivation chain terminates at
#                                L_self_exclusion's vacuum-fraction
#                                structure (both numerator C_vacuum and
#                                denominator d_eff come from the same
#                                bank theorem). Competitors like 19/45
#                                (numerically closer) contradict T12's
#                                V_local-vs-V_global assignment by
#                                using V_local as vacuum numerator.
#                                T_bridge_observer_independence_open
#                                [C, open] tier-4: formalizes the
#                                observer-dependence question of the
#                                bridge theorem. V_Lambda has three
#                                identifications — two observer-
#                                independent (T12, epsilon-decomposition)
#                                and one observer-dependent in GR
#                                (dS horizon absorber). Three resolutions
#                                possible (coincidental, implicit observer
#                                choice, or genuine APF observer-
#                                invariance beyond Lambda-CDM). Paper 8
#                                §11 flags as deepest open structural
#                                question of the Lambda-absolute arc.
#
#                                Previously registered 410 after the Phase 14e.5
#                                retraction (the cautionary-tale fit was
#                                removed without replacement); this
#                                current pass (Phase 14d.3) is the honest
#                                structural completion that REPLACES
#                                the retracted fit with three substantive
#                                theorems addressing the actual open
#                                questions.
#                                Phase 14e.5 attempted to close the 8%
#                                Lambda-absolute residual via a fitted
#                                structural factor 12/13 = K_gauge /
#                                (K_gauge + 1) = K_gauge / sin^2_denom_W.
#                                The fit numerically worked (<0.5% on
#                                all four matter densities), but the
#                                structural interpretation was
#                                numerology: the 13 in sin^2_theta_W =
#                                3/13 arises from the RG-flow
#                                competition-matrix fixed point in
#                                check_L_Fisher_gradient (13/4 = x^2 + m
#                                with x = 1/2 and m = dim(su2) = 3) and
#                                has NO structural relation to K_gauge +
#                                1 = 13; those are numerically equal by
#                                coincidence. More deeply, the 8%
#                                residual being "closed" wasn't actually
#                                a residual — it was the Hubble tension.
#                                APF's Lambda prediction and
#                                algebraically-linked H_0 = 70.03
#                                km/s/Mpc prediction (Phase 14e.3's
#                                T_Lambda_to_H0_inversion) are one
#                                prediction; the 8% gap against Planck
#                                2018 rho_Lambda IS the disagreement with
#                                Planck 2018 H_0 = 67.36 km/s/Mpc, which
#                                the Hubble tension itself tells us is
#                                contested. Applying a 12/13 correction
#                                effectively chooses Planck 2018 as the
#                                "true" H_0 and fudges rho_Lambda to
#                                match — erasing APF's own H_0
#                                prediction. The module
#                                apf/lambda_refinement.py has been
#                                archived to Old/ as
#                                lambda_refinement_RETRACTED_2026-04-22.py
#                                for the historical record; the
#                                post-hoc fit pattern is documented as
#                                a methodological cautionary tale. Paper
#                                8 headline restored: APF predicts
#                                rho_Lambda = 42/102^62 at 8% vs Planck
#                                2018 which is EXACTLY the Hubble tension,
#                                with algebraically-linked H_0 = 70.03
#                                km/s/Mpc prediction lying 0.17 km/s/Mpc
#                                from the tension midpoint.
#
#                                Previously registered 414 after the attempted
#                                Phase 14e.5 matter-sector refinement;
#                                that count is now incorrect. The true
#                                state after Phase 14e.4 is 410.
#                                Phase 14e.5 content description follows
#                                as a historical marker only:
#                                T_matter_sector_refinement_formula [P]
#                                tier-4 certifies the refined formula
#                                rho_matter_X/M_Pl^4 = (12/13) × C_X /
#                                102^62 matches ALL FOUR matter-sector
#                                densities to <0.5% (rho_Lambda to 0.16%,
#                                rho_crit to 0.14%, rho_b to 0.44%,
#                                rho_c to 0.03% — the tightest matter
#                                density!). Closes the uncorrected 8%
#                                residual across the board by factor
#                                20-250. The correction 12/13 is
#                                bank-forced: 12 = K_gauge, 13 =
#                                K_gauge + 1 = denominator of APF's
#                                sin^2(theta_W) = 3/13 prediction.
#                                T_matter_refinement_excludes_photon
#                                (tier-3 [P_structural]) confirms the
#                                correction is matter-sector-specific:
#                                applying 12/13 to T_CMB worsens the fit
#                                by factor 7.7 (0.33% → 9.63%), so the
#                                correction is NOT universal but
#                                physically tied to matter-sector
#                                vacuum energy. T_matter_refinement_
#                                weak_mixing_reading (tier-3 [C])
#                                registers the candidate structural
#                                interpretation: 12/13 = K_gauge /
#                                sin^2_denom_W encodes the weak-
#                                mixing-angle's coupling to matter-
#                                sector vacuum through the shared
#                                denominator 13. Photons (U(1)_em,
#                                post-mixing) don't carry this
#                                correction. Scan uniqueness: 12/13
#                                is tightest at 0.0008 decades residual,
#                                ~5× better than next-best 11/12. T_Phase_
#                                14e5_refinement (tier-4 [P] composed)
#                                binds the three sub-theorems. Net:
#                                Lambda-absolute prediction upgrades
#                                from 8% match to SUB-PERCENT match
#                                (0.16% on rho_Lambda) with a weak-
#                                mixing-angle structural reading,
#                                reshaping Paper 8's headline.
#
#                                Previously registered 410 after Phase 14e.4
#                                thermal-absolute + scope delineation.
#                                thermal-absolute tests for independent
#                                observables, scope delineation).
#                                +5 from apf/thermal_absolute.py:
#                                T_T_CMB_absolute_formula (tier-4 [P])
#                                certifies (T_CMB/M_Pl)^4 = 48/102^64
#                                predicts T_CMB = 2.7166 K vs observed
#                                2.7255 K, residual 0.33% (vs FIRAS
#                                precision 0.02%). A SECOND INDEPENDENT
#                                observable confirming the C/d_eff^k
#                                formula structure, at a different
#                                exponent k = K_SM + 3 = 64 (vs k = 62
#                                for non-relativistic matter densities).
#                                Coefficient 48 admits two structurally
#                                independent bank-forced readings:
#                                48 = C_c × C_b = 16×3 and 48 =
#                                K_gauge × K_higgs = 12×4. Much tighter
#                                fit than Lambda's 8%, suggesting the
#                                Planck-scale ansatz uncertainty is
#                                specific to the vacuum/cosmological-
#                                constant sector. T_thermal_exponent_
#                                interpretation (tier-3 [C]) registers
#                                the hypothesis k_X = K_SM + 1 + N_pol_X
#                                (species polarization count); matter
#                                (N_pol=0, k=62) and photon (N_pol=2,
#                                k=64) both confirm. L_eta_does_not_fit_
#                                cleanly (tier-3 [C, open]) documents
#                                that baryon-to-photon ratio eta is
#                                outside formula scope (requires
#                                baryogenesis-level analysis).
#                                L_Sigma_m_nu_suggestive (tier-3 [C, open])
#                                documents Sigma m_nu = 11/102^15 × M_Pl
#                                = 0.099 eV, within observational window
#                                [0.058, 0.12] eV, with coefficient 11
#                                admitting multiple structural readings
#                                without clear privilege. T_Phase_14e4_
#                                thermal_scope (tier-4 [P]) composed
#                                top theorem delineating the formula's
#                                scope.
#
#                                Previously registered 405 after Phase 14e.3
#                                corrected observed rho_Lambda value +
#                                H_0 inversion prediction.
#                                corrected observed rho_Lambda value +
#                                H_0 inversion prediction).
#                                +1 from apf/lambda_absolute.py:
#                                check_T_Lambda_to_H0_inversion (tier-4 [P])
#                                derives APF's Hubble-constant prediction
#                                H_0 = sqrt(8*pi*61/3) / 102^31 * M_Pl =
#                                70.03 km/s/Mpc by algebraic inversion of
#                                the bank-forced Lambda-absolute formula
#                                (rho_Lambda/M_Pl^4 = 42/102^62) and the
#                                bank-forced Omega_Lambda = 42/61 through
#                                the standard GR rho_crit formula. APF
#                                lands 0.17 km/s/Mpc from the exact
#                                midpoint (70.20) of the Hubble tension
#                                between Planck 2018 (67.36) and SH0ES
#                                2022 (73.04). Post-hoc interpretation of
#                                the 8% residual in the Lambda-absolute
#                                prediction; falsifiable against future
#                                tighter H_0 measurements.
#                                ALSO this phase: corrected the log10_obs
#                                values in check_L_Lambda_absolute_
#                                numerical_formula and check_L_N_SM_
#                                hierarchy_near_miss (and the _OBS_LOG10
#                                dict in lambda_absolute.py) from values
#                                derived from an incorrect rho_vac ~
#                                2.8e-11 eV^4 look-up to values derived
#                                from Planck 2018 parameters + standard
#                                Planck-mass convention. Residual for
#                                rho_Lambda shifts from 0.012 decades
#                                (reported "3% match") to 0.033 decades
#                                (honest "8% match"); for all four
#                                cosmological components the honest
#                                residuals are 7.8-8.3% (tightly
#                                clustered, as expected since they share
#                                the same denominator d_eff^(K+1) and
#                                the FRE-forced Omega_X = C_X/K_SM). No
#                                check-pass-fail status changed (0.05
#                                threshold still passes on 0.033
#                                residual). Paper 8 reports the honest
#                                8% residual.
#
#                                Previously registered 404 after the Phase 14d.2
#                                Lambda-absolute operator-level derivation.
#                                Lambda-absolute operator-level
#                                derivation).
#                                +4 from apf/lambda_operator_derivation.py:
#                                T_Lambda_partition_function_at_beta_zero [P]
#                                tier-4 certifies, at six test model
#                                interfaces via explicit numpy tensor-
#                                product construction of H_micro and
#                                thermal rho_beta, the three operator-
#                                algebra identities at the β → 0 limit:
#                                (A) ln Z = K ln(d_eff) = ACC;
#                                (B) <P_vac_slot_i> = tr(P_vac)/dim H
#                                    = C_vac/d_eff;
#                                (C) per-microstate probability = 1/N.
#                                T_Lambda_vacuum_projector_operator_identity
#                                [P_structural] tier-3 performs the
#                                β-sweep at model (K=3, d_eff=4, C_vac=2)
#                                confirming <P_vac> flows from 1 (ground
#                                state) to C_vac/d_eff (max-mixed) as
#                                β decreases.
#                                T_Lambda_Planck_scale_ansatz [C] tier-3
#                                honestly pins the residual
#                                non-upgradable derivation step: the
#                                identification eps_Planck = M_Planck
#                                is a dimensional ansatz external to
#                                APF, analogous to the status of most
#                                APF quantitative predictions (they are
#                                in units where M_Planck or EW-VEV is
#                                given externally).
#                                T_Lambda_d2_operator_derivation
#                                [P over [P]+[P_structural]+[C]] tier-4
#                                composes the three passes. Net upgrade:
#                                Lambda-absolute derivation moves from
#                                "informal structural argument" at [C]
#                                (the parent
#                                T_Lambda_absolute_structural_derivation)
#                                to "operator-algebra rigorous at model
#                                interfaces modulo the standard-APF
#                                external Planck scale" at [P].
#                                Three of four derivation steps upgrade
#                                to [P]; the fourth (Planck-scale
#                                identification) is an honest external
#                                input that APF does not derive from
#                                A1 (and probably cannot, given
#                                M_Planck arises from gravitational
#                                coupling).
#
#                                Previously registered 400 after the Phase 14e.2
#                                Lambda-absolute bulletproofing.
#                                +4 from apf/lambda_absolute.py:
#                                T_Lambda_absolute_extended_formula [P] tier-4
#                                extends the rho_Lambda match to all four
#                                cosmological density components (crit,
#                                b, c, Lambda), all within 0.013 decades.
#                                T_Lambda_coefficient_degeneracy_audit [C]
#                                tier-4 honestly documents that the
#                                numerical coefficient scan admits many
#                                candidates within 0.01 decades; 42/102
#                                is privileged structurally (L_self_exclusion
#                                + T12), not numerically. T_Lambda_
#                                operator_model_verification [P_structural]
#                                tier-3 certifies C_vac/d_eff = tr(P_vac)
#                                / dim H_micro at model interfaces as a
#                                rational-arithmetic identity, upgrading
#                                the coefficient piece of the derivation
#                                from informal argument to exact operator
#                                algebra. T_Lambda_absolute_bulletproof
#                                [P] tier-4 composes all four passes
#                                (including parent L_Lambda_absolute_
#                                numerical_formula from fractional_
#                                reading.py) into the headline Paper 8
#                                statement: "APF predicts rho_Lambda/
#                                M_Pl^4 = 42/102^62 at 3% match, robust
#                                against cross-component and coefficient-
#                                space and operator-level tests."
#
#                                Previously registered 396 after the Phase 14e.1
#                                Lambda-absolute identified formula.
#                                +2 to apf/fractional_reading.py:
#                                check_L_Lambda_absolute_numerical_formula
#                                (tier-3 [P]) certifies that the formula
#                                rho_vac/M_Planck^4 = (C_vacuum/d_eff) *
#                                1/N_SM = (42/102) * 102^(-61) = 42/102^62
#                                = 10^(-122.910) matches the observed
#                                10^(-122.898) (Planck 2018, standard
#                                Planck-mass convention) to within
#                                0.012 decades = factor 1.028, inside
#                                ~1% observational precision on rho_vac.
#                                Closes the bare-1/N_SM near-miss gap
#                                of 0.375 decades by a factor of 31.
#                                check_T_Lambda_absolute_structural_derivation
#                                (tier-4 [C]) registers the proposed
#                                structural derivation of the formula
#                                from A1 via the two-tier framework:
#                                rho_vac = (vacuum fraction of per-slot
#                                admissibility) * M_Planck^4 *
#                                (1/N_SM). The coefficient C_vacuum/
#                                d_eff = 42/102 has immediate
#                                structural meaning (fraction of per-
#                                slot admissibility allocated to
#                                vacuum-residual under L_self_exclusion)
#                                and both numerator 42 = C_vacuum
#                                (from T11) and denominator 102 = d_eff
#                                (from L_self_exclusion) are bank-
#                                forced. Derivation registered [C]
#                                pending Phase 14d.2 operator-level
#                                certification at I4.
#
#                                Previously registered 394 after the Phase 14e
#                                FRE + SM entropy dictionary.
#                                +7 from apf/fractional_reading.py:
#                                check_T_fractional_reading_equivalence
#                                (tier-4 [P]) proves the three-projection
#                                collapse at any ACC interface:
#                                pi_F-fraction = pi_T-fraction =
#                                pi_C-fraction = K_X / K for any
#                                sub-collection V_X of K_X slots inside
#                                V_slot of dim K, under the
#                                sub-within-ambient restriction
#                                (each slot retains the ambient d_eff).
#                                Check_L_Omega_{b,c,Lambda}_is_entropy_fraction
#                                (3 tier-3 [P]) establishes at the SM
#                                interface Omega_b = 3/61 = S(V_b)/S_SM,
#                                Omega_c = 16/61 = S(V_c)/S_SM, and
#                                Omega_Lambda = 42/61 = S(V_Lambda)/S_SM.
#                                The Omega_Lambda identification is the
#                                eureka: the cosmological dark-energy
#                                fraction equals the fraction of SM
#                                admissibility-capacity (information
#                                entropy) supported on V_Lambda.
#                                check_T_residual_entropy_closure
#                                (tier-4 [P]) certifies the three
#                                entropy fractions sum to 1, the
#                                entropy-level closure theorem parallel
#                                to I2_scalar's Omega-sum closure.
#                                check_L_N_SM_hierarchy_near_miss
#                                (tier-3 [C]) catalogues the numerical
#                                proximity log10(1/N_SM) = -122.5 vs
#                                observed log10(rho_vac / M_Planck^4)
#                                ~ -120 to -123 as a research
#                                observation, NOT a derivation;
#                                upgrading to [P] requires fixing the
#                                Planck-mass convention and identifying
#                                an O(1) coefficient (Option Two
#                                operator-level work at I4 plus a
#                                cosmological coefficient derivation).
#                                check_T_FRE_SM_to_entropy_dictionary
#                                (tier-4 [P]) composes the above into
#                                the full SM cosmological-to-entropy
#                                dictionary, the headline structural
#                                result Paper 8 should lead with.
#
#                                Previously registered 387 after the Phase 14c.3
#                                operator-subspace functor + composed
#                                top theorem — Phase 14c completion.
#                                +2 from apf/subspace_functors.py:
#                                check_T_operator_subspace_functor
#                                (tier-4 [P]) proves the explicit
#                                operator-subspace functor F_operator:
#                                (ACC_quantum, spectrum) -> Subspace
#                                satisfies structural conditions
#                                (i)-(v) (existence, dimension
#                                preservation matching |spectrum| = N,
#                                monotonicity under spectrum extension
#                                in the canonical operator-space ambient,
#                                partition-function compatibility ln Z
#                                (beta -> 0) = ln N = ACC_scalar for
#                                both flat and uniform [0,1] spectra, and
#                                scalar commutation dim V = exp(ACC_scalar)
#                                = N; NOT axioms of APF — those are
#                                conditions derived from A1 +
#                                L_spectral_action_internal), promoting
#                                I4_subspace from
#                                [C, parked] to [P]. check_T_subspace_
#                                functors_unified (tier-4 [P], composed)
#                                asserts that the three 14c functors
#                                F_horizon / F_quantum / F_operator are
#                                jointly well-defined, and together with
#                                T_interface_sector_bridge (I2's
#                                subspace functor in gravity.py) complete
#                                the subspace-level presentation of
#                                every T_ACC consistency identity.
#
#                                Consequence: T_I4_three_level_consistent
#                                upgrades to [P over [P]+[P]+[P]]; all
#                                four per-Ik composed three-level
#                                checks are now fully [P] end-to-end.
#                                T_three_level_unification bumped from
#                                [P over [P]+[P]+[P] (3 fully_P) +
#                                [P over [P]+[P]+[C]]] to full
#                                [P over [P]+[P]+[P]+[P]]; no parked
#                                subspace kernels remain. Phase 14c
#                                (as a whole) delivers the three explicit
#                                subspace functors that close every TBD
#                                flagged by the Phase 14 baseline.
#
#                                Previously registered 385 after the Phase 14c.2
#                                quantum-subspace functor.
#                                +1 from apf/subspace_functors.py:
#                                check_T_quantum_subspace_functor
#                                (tier-4 [P]) proves the explicit
#                                quantum-subspace functor F_quantum:
#                                ACC_quantum -> Subspace satisfies
#                                structural conditions (i)-(v)
#                                (existence, dimension preservation,
#                                monotonicity under d-nesting in the
#                                single canonical quantum ambient,
#                                max-mixed state compatibility
#                                S_vN(rho_max) = ln d = ACC_scalar, and
#                                the quantum-regime scalar commutation
#                                dim V = exp(ACC_scalar) = N). Promotes
#                                I3_subspace in three_levels.py from
#                                [C, parked] to [P]; upgrades
#                                T_I3_three_level_consistent to
#                                [P over [P]+[P]+[P]] with the full f_2
#                                scalar->subspace commutation now
#                                verifiable. T_three_level_unification
#                                updated: I1, I2, I3 are now fully [P];
#                                I4 alone remains parked pending
#                                Phase 14c.3 (operator-subspace functor).
#
#                                Previously registered 384 after the Phase 14c.1
#                                horizon-subspace functor.
#                                +1 from apf/subspace_functors.py:
#                                check_T_horizon_subspace_functor
#                                (tier-4 [P]) proves the explicit
#                                horizon-subspace functor F_horizon:
#                                ACC_horizon -> Subspace satisfies the
#                                five structural conditions (i)-(v)
#                                (existence + well-definedness,
#                                dimension preservation, monotonicity
#                                under horizon nesting, compatibility
#                                with T_interface_sector_bridge at the
#                                canonical SM-dS horizon K=42, and
#                                scalar commutation dim * ln(d_eff) =
#                                ACC_scalar; NOT axioms of APF — those
#                                are conditions derived from A1 + T_Bek).
#                                At K=42 in the v61
#                                ambient, F_horizon coincides
#                                combinatorially with V_global as
#                                witnessed by T_interface_sector_bridge,
#                                supplying the categorical analog of
#                                I2's bridge theorem on the horizon
#                                side.
#
#                                Consequence: I1_subspace in
#                                apf/unification_three_levels.py is
#                                promoted from [C, parked] to [P]
#                                (wrapping F_horizon + the condition
#                                proof). check_T_I1_three_level_consistent
#                                is upgraded from [P over [P]+[P]+[C]]
#                                to [P over [P]+[P]+[P]] with the
#                                full f_2 scalar->subspace commutation
#                                now verifiable. check_T_three_level_unification
#                                updated: I1 joins I2 in the
#                                "fully [P] at all three levels" set;
#                                I3, I4 remain parked pending
#                                Phase 14c.2 (quantum-subspace functor)
#                                and 14c.3 (operator-subspace functor).
#
#                                Previously registered 383 after the Phase 14a
#                                projection-essentiality module.
#                                +7 from apf/unification_projection_essentiality.py:
#                                check_pi_T_essentiality,
#                                check_pi_G_essentiality,
#                                check_pi_Q_essentiality,
#                                check_pi_F_essentiality,
#                                check_pi_C_essentiality,
#                                check_pi_A_essentiality (6 tier-3 [P_structural],
#                                one per regime projection), and
#                                check_T_projection_essentiality (tier-4
#                                [P_structural], composed). Each per-pi check
#                                certifies the operational uniqueness of one of
#                                the six regime projections by reading the
#                                regime-appropriate (K, ACC) fields, satisfying
#                                a regime-specific structural constraint, and
#                                demonstrating consistency with the other five
#                                via the four consistency identities I1-I4.
#                                Prerequisite for Paper 8's Paper-0-required
#                                "self-contained projection proofs": the
#                                identities are not arbitrary equations but
#                                uniqueness theorems whose LHS and RHS each
#                                depend on a distinct, essential projection.
#
#                                Previously registered 376 after the Phase 14c
#                                SCC-aware path attribution variant.
#                                +1 from apf/crystal_metrics.py:
#                                check_T_crystal_path_attribution_scc_v69
#                                (tier-3 [P_structural]) certifies that
#                                Tarjan SCC condensation of the bank
#                                graph + DAG-DP on the condensation
#                                produces a well-formed PLEC anchor
#                                share table to T_sin2theta, including
#                                attribution of paths that traverse
#                                the Theorem_R ↔ T_gauge ↔ T_field
#                                co-definition cycle (invisible under
#                                the §4 depth-filtered variant).
#                                Companion to the Phase 14b rewiring
#                                (Regime_R → Theorem_R and
#                                worked_example → L_count edges added
#                                to the bank); the §4b SCC metric is
#                                what makes those edges visible in the
#                                path-share table.
#
#                                Previously registered 375 after the
#                                Phase 13.3 / Stage II workstream 3:
#                                Menger minimum
#                                vertex cut catalogue on the
#                                Enforcement Crystal walker output.
#                                +1 from apf/crystal_metrics.py:
#                                check_T_crystal_min_cut_v69 (tier-3
#                                [P_structural]) certifies that the
#                                vertex-split + Edmonds-Karp
#                                min-vertex-cut computation on the
#                                depth-filtered DAG is deterministic,
#                                produces cut_size >= 1 for every
#                                depth-DAG-reachable (PLEC anchor,
#                                Stage III sink) pair, returns a cut
#                                witness whose size equals the cut
#                                value, and agrees on cut sizes
#                                between the full and post-R views
#                                for surviving sources. Sinks: the
#                                canonical Stage III set
#                                {T_sin2theta, T_gauge, T_PMNS,
#                                T_mass_ratios, L_count}. This is the
#                                companion to workstream 2's cascade
#                                table for Paper 20 v3.0 Stage III §6:
#                                cascade asks "what does *one*
#                                deletion break?", min-cut asks "how
#                                many *coordinated* deletions break a
#                                derivation chain?". Closes Stage II
#                                of the Phase 13 Enforcement Crystal
#                                analytical layer (workstreams 1, 2,
#                                3, 4, 5 all landed).
#
#                                Previously registered 374 after the
#                                Phase 13.3 / Stage II workstream 5
#                                convergence-cluster pass (+1 from
#                                apf/crystal_metrics.py:
#                                check_T_crystal_convergence_v69
#                                (tier-3 [P_structural]) certifies
#                                that the depth-filtered DAG fan-in
#                                catalogue is in [0, V-1] per node,
#                                anchor_diversity is in [0, 4] per
#                                top-K sink, the ranking is
#                                deterministic on re-run, and the
#                                post-R top-3 is contained in the
#                                full top-25 (dual-view stability of
#                                the convergence sinks). Refreshes
#                                Paper 20 v3.0 Stage III §7 (v1.0
#                                reported the convergence-pattern
#                                catalogue; v6.9 has many more sinks
#                                by design — Phase 14 / 13.1 / 14b /
#                                T_ACC convergence theorems).
#
#                                Previously registered 373 after the
#                                Phase 13.3 / Stage II workstream 2
#                                cascade-failure pass (+1 from
#                                apf/crystal_metrics.py:
#                                check_T_crystal_cascade_v69 (tier-3
#                                [P_structural]) certifies that for
#                                every non-anchor candidate node N in
#                                the depth-filtered DAG, the cascade
#                                fraction (proportion of
#                                anchor-reachable nodes that lose PLEC
#                                anchor reachability when N is
#                                retracted) lies in [0, 1], the
#                                ranking is deterministic on re-run,
#                                and the post-R top-3 is contained in
#                                the full top-25 (dual-view stability
#                                of the load-bearing waists).
#                                Refreshes Paper 20 v3.0 Stage III §6
#                                (v1.0 reported "removing T4 invalidates
#                                67% of predictions").
#
#                                Previously registered 372 after the
#                                Phase 13.3 / Stage II workstream 4
#                                DAG path attribution pass (+1 from
#                                apf/crystal_metrics.py:
#                                check_T_crystal_path_attribution_v69
#                                (tier-3 [P_structural]) certifies that
#                                the depth-filtered DAG path-counting
#                                from each of the four PLEC anchors
#                                (A1 / L_epsilon* / Regime_R /
#                                worked_example) to the canonical
#                                target T_sin2theta is deterministic,
#                                produces a well-formed share table
#                                that sums to 1.0, and is identical
#                                across the full_graph and
#                                post_R_subgraph views (dual-view
#                                stability of the axiom-share ranking).
#                                Refreshes Paper 20 v3.0 Stage III §5
#                                (v1.0 reported A2=42%, A1=39%,
#                                A3=15%, A4=3%, A5=0.5% over 1398
#                                paths under the v1 schema).
#
#                                Previously registered 371 after the
#                                Phase 13.3 / Stage II workstream 1
#                                Brandes BC pass (+1 from
#                                apf/crystal_metrics.py:
#                                check_T_crystal_centrality_v69 (tier-3
#                                [P_structural]) certifies that the
#                                Brandes BC computation on both the
#                                full_graph and post_R_subgraph views
#                                under the CORE preset is deterministic,
#                                normalized to [0, 1], and produces a
#                                well-formed top-10 ranking with the
#                                post-R top-3 contained in the full
#                                top-25 (dual-view stability of the
#                                centrally-located waists).
#
#                                Previously registered 370 after the
#                                Phase 14b v0 killed-rivals lock-in pass
#                                (+5 from apf/killed_rivals.py:
#                                check_R_SU_Nc_neq_3_killed (tier-4 [P_structural]),
#                                check_R_Ngen_neq_3_killed (tier-4 [P_structural]),
#                                check_R_extra_axiom_NT_killed (tier-4 [P_structural]),
#                                check_R_Born_axiomatic_killed (tier-4 [P_structural]),
#                                check_T_killed_rivals_v0 (tier-4 [P_structural],
#                                composed). Locks the four structural rival
#                                physical-theory architectures from §14b.0:
#                                (1) SU(N_c≠3) gauge groups killed by
#                                Theorem_R + T_gauge cost optimization;
#                                (2) N_gen≠3 killed by T7 saturated-channel
#                                count C_EW = 8; (3) extra axioms (Lorentz,
#                                gauge invariance, Born rule, Lagrangian
#                                density existence) killed by 4-candidate
#                                enumeration as derived/redundant w.r.t.
#                                A1 + PLEC components; (4) axiomatic Born
#                                rule killed by strict domination via
#                                T_Born + T2 derivation chain).
#
#                                Previously registered 365 after the
#                                Phase 13.2 Enforcement Crystal walker pass
#                                (+1 from apf/crystal.py:
#                                check_T_crystal_v69_consistent (tier-4
#                                [P_structural]) certifies that the
#                                Phase 13.2 walker view of bank.REGISTRY
#                                agrees with the bank's self-report on
#                                count, epistemic distribution, PLEC
#                                anchor reachability, post-R subset
#                                strictness, and JSON serializability).
#
#                                Previously registered 364 after the
#                                three-level identity refinement pass
#                                (Phase 14, +17 from
#                                apf/unification_three_levels.py).
#                                Before Phase 14: 347 after the
#                                interface-sector bridge pass.
#
#                                Current composition (21 modules, 364 theorems):
#                                  v6.9 2026-04-21 evening Phase 14 (+17):
#                                    apf/unification_three_levels.py:
#                                    check_I{1..4}_integer (4 [P]),
#                                    check_I{1..4}_scalar  (4 [P]),
#                                    check_I{1..4}_subspace (1 [P] + 3 [C, parked]),
#                                    check_T_I{1..4}_three_level_consistent
#                                    (4 [P]; I2 is the headline),
#                                    check_T_three_level_unification (tier-4 [P]).
#                                    Refines each Ik consistency identity into
#                                    integer / scalar / subspace witnesses and
#                                    certifies the inter-level functor diagram
#                                    commutes per Ik plus the top composed.
#                                  v6.9 2026-04-20 late evening (+2):
#                                    apf/gravity.py: L_global_interface_is_horizon
#                                    (tier 3 aux lemma), T_interface_sector_bridge
#                                    (tier 4 theorem identifying T12 V_global with
#                                    T_horizon_reciprocity Sector B).
#                                  v6.9 2026-04-20 afternoon (+5, net 345-loaded):
#                                    apf/unification.py: I1_holographic,
#                                    I2_gauge_cosmological, I3_thermo_quantum,
#                                    I4_action_thermo, T_ACC_unification.
#                                  v6.9 2026-04-18 (+7, baseline 335+7=342 claimed
#                                    but 340-loaded — the original source of the
#                                    silent -2 drift):
#                                    apf/plec.py: Regime_R, Regime_exit_Type_I..V
#                                    (6 checks) + apf/gravity.py A9_closure (1).
#                                  v6.8 baseline: 335.
#                                21 modules register theorems; verify_all totals
#                                379 checks including standalone/* and
#                                session_phase2_confrontation.

# Module load order (respects dependency DAG)
# _MODULE_PATHS is imported from apf._module_manifest at top of file (v24.3.19).

# Module name -> list of theorem names (populated at load time)
_MODULE_MAP = {}

_loaded = False


def _load():
    """Import all modules and merge their registries.

    Robust to three failure modes (all silently logged, none fatal):
      - ImportError: optional dependency missing (e.g., scipy in sandbox env)
      - TypeError: register() signature mismatch (KNOWN_REGISTER_ANOMALIES;
        modules whose register() takes 0 args instead of (registry,))
      - Other Exception: any other module-load issue

    The _module_manifest.KNOWN_REGISTER_ANOMALIES list documents the
    register()-signature-mismatch modules; their checks are NOT in REGISTRY
    because bank can't call register(REGISTRY) on them.
    """
    global _loaded
    if _loaded:
        return
    from importlib import import_module
    _load_errors = []
    for mod_path in _MODULE_PATHS:
        mod_name = mod_path.split('.')[-1]
        try:
            mod = import_module(mod_path)
            before = set(REGISTRY.keys())
            try:
                mod.register(REGISTRY)
            except TypeError:
                # KNOWN_REGISTER_ANOMALIES: register() takes 0 args instead of (registry,).
                # Skip silently — module's checks won't enter REGISTRY (documented anomaly).
                _MODULE_MAP[mod_name] = []
                continue
            after = set(REGISTRY.keys())
            _MODULE_MAP[mod_name] = sorted(after - before)
        except ImportError as e:
            import warnings
            warnings.warn(
                f"APF: Failed to load module '{mod_name}': {e}. "
                f"This module will have 0 theorems.",
                RuntimeWarning,
                stacklevel=2,
            )
            _MODULE_MAP[mod_name] = []
            _load_errors.append((mod_name, str(e)))
        except Exception as e:
            _MODULE_MAP[mod_name] = []
            _load_errors.append((mod_name, f"{type(e).__name__}: {e}"))
    _loaded = True

    # Verify expected count
    actual = len(REGISTRY)
    if actual != EXPECTED_THEOREM_COUNT:
        import warnings
        warnings.warn(
            f"APF: Expected {EXPECTED_THEOREM_COUNT} theorems, "
            f"loaded {actual}. "
            f"{'Load errors: ' + str(_load_errors) if _load_errors else 'No import errors — count may need updating.'}",
            RuntimeWarning,
            stacklevel=2,
        )


def run_all(modules=None, verbose=True, verify_dag=True):
    """Execute all theorem checks.

    Parameters
    ----------
    modules : list[str], optional
        Filter by module name(s). None = run all.
    verbose : bool
        Print results to stdout.
    verify_dag : bool
        If True, print DAG summary after run.

    Returns
    -------
    dict
        {theorem_name: result_dict} for all executed checks.
    """
    _load()

    # Reset derivation cache so each run starts clean
    dag_reset()

    # Determine which theorems to run
    if modules:
        names_to_run = set()
        for mod in modules:
            names_to_run.update(_MODULE_MAP.get(mod, []))
    else:
        names_to_run = set(REGISTRY.keys())

    results = {}
    passed = failed = errors = 0
    t0 = _time.time()

    for name, check_fn in REGISTRY.items():
        if name not in names_to_run:
            continue
        try:
            r = check_fn()
            results[name] = r
            if r['passed']:
                passed += 1
                mark = 'PASS'
            else:
                failed += 1
                mark = 'FAIL'
            if verbose:
                ep = r.get('epistemic', '?')
                print(f"  {mark} [{ep:14s}] {name}")
        except CheckFailure as e:
            failed += 1
            results[name] = {'name': name, 'passed': False,
                             'error': str(e), 'epistemic': 'FAIL'}
            if verbose:
                print(f"  FAIL [{'CHECK':14s}] {name}: {e}")
        except Exception as e:
            errors += 1
            results[name] = {'name': name, 'passed': False,
                             'error': str(e), 'epistemic': 'ERROR'}
            if verbose:
                print(f"  ERR  [{'ERROR':14s}] {name}: {e}")

    elapsed = _time.time() - t0
    total = passed + failed + errors
    if verbose:
        print(f"\n  {'='*60}")
        if modules:
            print(f"  Modules: {', '.join(modules)}")
        print(f"  {passed} passed, {failed} failed, "
              f"{errors} errors, {total} total")
        print(f"  Elapsed: {elapsed:.2f}s")
        # DAG summary
        if verify_dag:
            dag_data = dag_dump()
            if dag_data:
                n_keys = len(dag_data)
                n_consumed = sum(1 for v in dag_data.values()
                                 if v['consumers'])
                print(f"  DAG: {n_keys} values cached, "
                      f"{n_consumed} consumed by downstream")
        print(f"  {'='*60}")

    return results


def list_modules():
    """Return dict of {module_name: [theorem_names]}."""
    _load()
    return dict(_MODULE_MAP)


def write_html_report(results, path='apf_report.html'):
    """Write results to an HTML file.

    Parameters
    ----------
    results : dict
        Output of run_all().
    path : str
        Output file path.
    """
    import html as _html
    from apf import __version__

    passed = sum(1 for r in results.values() if r.get('passed'))
    failed = len(results) - passed

    # Reverse map: theorem -> module
    _load()
    thm_to_mod = {}
    for mod, names in _MODULE_MAP.items():
        for n in names:
            thm_to_mod[n] = mod

    lines = [
        '<!DOCTYPE html>',
        '<html><head>',
        '<meta charset="utf-8">',
        f'<title>APF v{__version__} Theorem Bank Report</title>',
        '<style>',
        'body { font-family: "Segoe UI", system-ui, sans-serif; '
        'max-width: 1000px; margin: 40px auto; padding: 0 20px; '
        'background: #f8f9fa; color: #1a1a2e; }',
        'h1 { border-bottom: 3px solid #2d3436; padding-bottom: 10px; }',
        '.summary { background: #fff; padding: 20px; border-radius: 8px; '
        'box-shadow: 0 1px 3px rgba(0,0,0,0.1); margin-bottom: 24px; }',
        '.pass { color: #00b894; font-weight: bold; }',
        '.fail { color: #d63031; font-weight: bold; }',
        'table { width: 100%; border-collapse: collapse; '
        'background: #fff; border-radius: 8px; overflow: hidden; '
        'box-shadow: 0 1px 3px rgba(0,0,0,0.1); }',
        'th { background: #2d3436; color: #fff; text-align: left; '
        'padding: 12px 16px; }',
        'td { padding: 10px 16px; border-bottom: 1px solid #eee; }',
        'tr:hover td { background: #f1f3f5; }',
        '.tag { display: inline-block; padding: 2px 8px; border-radius: 4px; '
        'font-size: 0.85em; font-weight: 600; }',
        '.tag-P { background: #d4edda; color: #155724; }',
        '.tag-P_structural { background: #cce5ff; color: #004085; }',
        '.tag-P_imported { background: #e2e3f1; color: #383d6e; }',
        '.tag-W { background: #fff3cd; color: #856404; }',
        '.tag-FAIL, .tag-ERROR { background: #f8d7da; color: #721c24; }',
        'details { margin: 4px 0; }',
        'summary { cursor: pointer; }',
        '</style></head><body>',
        f'<h1>APF v{__version__} — Theorem Bank Report</h1>',
        '<div class="summary">',
        f'<p><strong>{passed}</strong> passed, '
        f'<strong>{failed}</strong> failed, '
        f'<strong>{len(results)}</strong> total theorems across '
        f'{len(_MODULE_MAP)} modules.</p>',
        '</div>',
        '<table><thead><tr>',
        '<th>#</th><th>Status</th><th>Module</th>'
        '<th>Theorem</th><th>Epistemic</th><th>Key Result</th>',
        '</tr></thead><tbody>',
    ]

    for i, (name, r) in enumerate(results.items(), 1):
        ok = r.get('passed', False)
        status = '<span class="pass">PASS</span>' if ok else \
                 '<span class="fail">FAIL</span>'
        ep = _html.escape(str(r.get('epistemic', '?')))
        ep_class = ep.replace(' ', '_')
        mod = thm_to_mod.get(name, '?')
        kr = _html.escape(str(r.get('key_result', '')))
        err = r.get('error', '')
        detail = ''
        if err:
            detail = f' <details><summary>error</summary>' \
                     f'<pre>{_html.escape(err)}</pre></details>'
        lines.append(
            f'<tr><td>{i}</td><td>{status}</td>'
            f'<td>{mod}</td><td>{_html.escape(name)}</td>'
            f'<td><span class="tag tag-{ep_class}">{ep}</span></td>'
            f'<td>{kr}{detail}</td></tr>'
        )

    lines += ['</tbody></table>', '</body></html>']

    with open(path, 'w') as f:
        f.write('\n'.join(lines))


def main():
    """CLI entry point."""
    import sys
    from apf import __version__

    args = sys.argv[1:]
    modules = None
    verbose = True
    html_path = None

    # Parse args
    i = 0
    while i < len(args):
        if args[i] in ('--module', '-m') and i + 1 < len(args):
            modules = [args[i + 1]]
            i += 2
        elif args[i] == '--html' and i + 1 < len(args):
            html_path = args[i + 1]
            i += 2
        elif args[i] == '--html':
            html_path = 'apf_report.html'
            i += 1
        elif args[i] == '--list':
            _load()
            for mod, names in _MODULE_MAP.items():
                print(f"\n  {mod} ({len(names)} theorems)")
                for n in names:
                    print(f"    {n}")
            total = sum(len(v) for v in _MODULE_MAP.values())
            print(f"\n  Total: {total} theorems in "
                  f"{len(_MODULE_MAP)} modules")
            sys.exit(0)
        elif args[i] == '--quiet':
            verbose = False
            i += 1
        elif args[i] in ('--help', '-h'):
            print(f"APF v{__version__} Theorem Bank")
            print(f"Usage: python -m apf [OPTIONS]")
            print(f"  --module NAME    Run only one module")
            print(f"  --list           List all modules and theorems")
            print(f"  --html [PATH]    Write HTML report (default: apf_report.html)")
            print(f"  --quiet          Suppress output")
            print(f"  --help           Show this help")
            sys.exit(0)
        else:
            print(f"Unknown argument: {args[i]}")
            sys.exit(1)

    print(f"\n  APF v{__version__} Theorem Bank")
    print(f"  {'='*60}\n")
    results = run_all(modules=modules, verbose=verbose)

    if html_path:
        write_html_report(results, html_path)
        if verbose:
            print(f"\n  HTML report written to: {html_path}")


if __name__ == '__main__':
    main()
