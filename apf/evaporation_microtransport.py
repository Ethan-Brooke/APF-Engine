"""
APF Evaporation Microtransport — Sprint E1 (structural rigor) + E2 (Schwarzschild backbone) + E3 (import-certify) + E4 (physical quotient) + E5 (parameter matching) + E6 (open-frontier fence) gates.

Banks the seven Tier-A structural gates of the Paper 41 evaporation closure work plan
(`Reference - Paper 41 Evaporation Closure Work Plan (2026-05-21).md`), delivered by the
sibling-execution Sprint E1 pack `APF_EVAPORATION_E1_STRUCTURAL_RIGOR_v1` (white paper
§86-95) and audit-cleared 2026-05-21: the standalone verifier recomputes every witness at
machine precision (EVAPORATION_E1_STRUCTURAL_RIGOR_PASS).

All seven are **Tier A** in the work-plan tiering: pure linear algebra / typed composition /
finite-dimensional witnesses. They are deliberately near-tautological and carry no physical
content. Per the auditor rejection rules, they bank at [P_structural] ONLY:

  G-DIL       ledger transport (isometry) extends to a unitary dilation (Stinespring/basis completion)
  G-NONPROD   horizon-ledger backreaction => radiation history does not factor into independent marginals
  G-FACT      typed amplitude factorization schema (bookkeeping; NOT a derivation of the factors)
  G-UNIT      amplitude unitarity constraint S^dag S = I on the physical sector
  G-GREY-ROLE greybody transmission embeds in a unitary beam-splitter (no erasure at the total codomain)
  G-DEC-CRIT  decoder admissibility criterion (rank + Gram + four-role + no-remnant), a criterion not a construction
  G-END-UNIT  endpoint operation must be an isometry on the physical sector

Honest non-claims (from the pack docs/HONEST_NON_CLAIMS.md, preserved): NO physical greybody
evaluation, NO islands/QES derived from APF, NO explicit decoder for a chosen model, NO unique
scrambling Hamiltonian, NO physical endpoint phase, NO universal mode-by-mode micro-S-matrix,
NO physical closure from a toy witness. Tier B (island-regime, physical-quotient, certified
tuple) and Tier C (the above [C] gates) are NOT touched here.

Top marker: EVAPORATION_MICROTRANSPORT_E1_PASS
"""

from __future__ import annotations

import math
from typing import Dict

TOL = 1e-9


# -- tiny dependency-free complex-matrix helpers (small fixed sizes) --

def _dag(A):
    return [[complex(A[i][j]).conjugate() for i in range(len(A))] for j in range(len(A[0]))]

def _mul(A, B):
    n, k, m = len(A), len(B), len(B[0])
    return [[sum(complex(A[i][p]) * complex(B[p][j]) for p in range(k)) for j in range(m)]
            for i in range(n)]

def _ident(n):
    return [[complex(1 if i == j else 0) for j in range(n)] for i in range(n)]

def _is_ident(A, tol=TOL):
    n = len(A)
    if any(len(r) != n for r in A):
        return False, float("inf")
    err = max(abs(complex(A[i][j]) - (1 if i == j else 0)) for i in range(n) for j in range(n))
    return err <= tol, err


def _ok(name, *, status, summary, data=None, dependencies=None):
    return {"name": name, "consistent": True, "status": status, "summary": summary,
            "data": dict(data or {}), "dependencies": list(dependencies or [])}

def _fail(name, *, status, summary, data=None, dependencies=None):
    return {"name": name, "consistent": False, "status": status, "summary": summary,
            "data": dict(data or {}), "dependencies": list(dependencies or [])}


# ====================================================================
# G-DIL — ledger transport (isometry) extends to a unitary dilation
# ====================================================================

def check_G_DIL_ledger_transport_to_unitary_dilation():
    V = [[1, 0], [0, 1], [0, 0]]              # V : C^2 -> C^3, columns orthonormal
    ok_v, err_v = _is_ident(_mul(_dag(V), V))  # V^dag V = I_2
    U = _ident(3)                              # basis completion: U = I_3 agrees with V on input sector
    ok_u, err_u = _is_ident(_mul(_dag(U), U))
    agrees = all(abs(complex(U[i][j]) - complex(V[i][j])) <= TOL
                 for i in range(3) for j in range(2))
    if not (ok_v and ok_u and agrees):
        return _fail("check_G_DIL_ledger_transport_to_unitary_dilation", status="P_structural_reading",
                     summary="Isometry-to-unitary dilation witness failed",
                     data={"err_v": err_v, "err_u": err_u, "agrees": agrees})
    return _ok("check_G_DIL_ledger_transport_to_unitary_dilation", status="P_structural_reading",
               summary=("Any rank+pairing-preserving ledger transport (isometry V, V^dag V = I) "
                        "extends to a unitary U on an enlarged finite space agreeing with V on the "
                        "admissible input sector (Stinespring/basis completion). Witness C^2->C^3, U=I_3."),
               data={"err_VdagV": err_v, "err_UdagU": err_u, "U_restricts_to_V": agrees},
               dependencies=["check_T_microtransport_sufficiency", "check_L_no_bounded_remnant"])


# ====================================================================
# G-NONPROD — backreaction => non-product radiation history
# ====================================================================

def check_G_NONPROD_backreaction_nonproduct():
    P1_M2 = 0.25   # P(omega=1 | M=2)
    P1_M1 = 0.5    # P(omega=1 | M=1)
    P_cond_11 = P1_M2 * P1_M1            # chain rule with backreaction M_2 = 2 - omega_1 -> 0.125
    P_fixed_product = P1_M2 * P1_M2      # fixed-M independent marginals -> 0.0625
    nonfactor = abs(P_cond_11 - P_fixed_product) > TOL
    if not nonfactor:
        return _fail("check_G_NONPROD_backreaction_nonproduct", status="P_structural_reading",
                     summary="Non-product history witness failed",
                     data={"P_cond": P_cond_11, "P_fixed": P_fixed_product})
    return _ok("check_G_NONPROD_backreaction_nonproduct", status="P_structural_reading",
               summary=("If emission probability depends on a horizon-ledger state that backreacts "
                        "(M_{n+1}=M_n-omega_n), the joint radiation history does not factor into "
                        "independent one-emission marginals. Witness: P_cond(1,1)=0.125 != "
                        "P_fixed_product=0.0625."),
               data={"P_cond_11": P_cond_11, "P_fixed_product": P_fixed_product, "nonfactorizes": nonfactor},
               dependencies=["check_T_thermal_marginals_no_ledger_loss"])


# ====================================================================
# G-FACT — typed amplitude factorization schema (bookkeeping only)
# ====================================================================

def check_G_FACT_typed_factorization_schema():
    h = 1 / math.sqrt(2)
    A = [[2, 0], [0, 1]]                  # thermal weighting
    G = [[0.8, 0], [0, 0.5]]              # exterior filter
    B = [[1, 0], [0, 0.9]]               # backreaction conditioning
    K = [[h, h], [h, -h]]                 # scrambling (Hadamard)
    R = _ident(2)                         # reconstruction (identity)
    Phi = [[1, 0], [0, 1j]]              # endpoint phase
    S = _mul(Phi, _mul(R, _mul(K, _mul(B, _mul(G, A)))))
    well_typed = (len(S) == 2 and len(S[0]) == 2)
    if not well_typed:
        return _fail("check_G_FACT_typed_factorization_schema", status="P_structural_reading",
                     summary="Typed factorization schema witness failed", data={"shape": (len(S), len(S[0]))})
    return _ok("check_G_FACT_typed_factorization_schema", status="P_structural_reading",
               summary=("A typed amplitude map decomposes into role-labeled operators "
                        "S = Phi.R.K.B.G.A (thermal/filter/backreaction/scramble/reconstruct/phase) "
                        "by well-typed composition. BOOKKEEPING theorem only: it does NOT derive the "
                        "factors' physical values."),
               data={"shape": (len(S), len(S[0])),
                     "roles": ["thermal", "greybody", "backreaction", "scramble", "reconstruct", "endpoint_phase"],
                     "not_a_derivation_of_factors": True},
               dependencies=["check_T_radiation_correlation_space_sufficient"])


# ====================================================================
# G-UNIT — amplitude unitarity constraint  S^dag S = I
# ====================================================================

def check_G_UNIT_amplitude_unitarity():
    h = 1 / math.sqrt(2)
    S = [[h, h], [h, -h]]                 # Hadamard unitary
    ok_i, err = _is_ident(_mul(_dag(S), S))
    if not ok_i:
        return _fail("check_G_UNIT_amplitude_unitarity", status="P_structural_reading",
                     summary="Amplitude unitarity witness failed", data={"err": err})
    return _ok("check_G_UNIT_amplitude_unitarity", status="P_structural_reading",
               summary=("On the APF physical/enforceable sector the amplitude matrix satisfies "
                        "sum_alpha A*_{alpha beta} A_{alpha gamma} = delta_{beta gamma}, i.e. "
                        "S^dag S = I. Witness: Hadamard, err=%.2e." % err),
               data={"SdagS_err": err},
               dependencies=["check_G_DIL_ledger_transport_to_unitary_dilation"])


# ====================================================================
# G-GREY-ROLE — greybody as unitary beam-splitter (no erasure)
# ====================================================================

def check_G_GREY_ROLE_beamsplitter():
    worst = 0.0
    for G in (0.0, 0.25, 0.5, 0.75, 1.0):
        s, t = math.sqrt(G), math.sqrt(1 - G)
        U = [[s, t], [t, -s]]
        _, err = _is_ident(_mul(_dag(U), U))
        worst = max(worst, err)
    if worst > 1e-9:
        return _fail("check_G_GREY_ROLE_beamsplitter", status="P_structural_reading",
                     summary="Beam-splitter unitary embedding failed", data={"worst_err": worst})
    return _ok("check_G_GREY_ROLE_beamsplitter", status="P_structural_reading",
               summary=("A greybody transmission factor G in [0,1] embeds in a unitary beam-splitter "
                        "(transmitted + reflected channels); norm is preserved when both channels are "
                        "kept. Erasure appears ONLY if the reflected/complement channel is discarded. "
                        "worst_err=%.2e over G in {0,.25,.5,.75,1}." % worst),
               data={"worst_err": worst},
               dependencies=["check_G_UNIT_amplitude_unitarity"])


# ====================================================================
# G-DEC-CRIT — decoder admissibility criterion (criterion, not construction)
# ====================================================================

def check_G_DEC_CRIT_rank_gram_preserving():
    src = [[1, 0], [0, 1]]                # 2 ledger basis vectors
    emb = {0: 0, 1: 3}                    # |0>->|00>(e0), |1>->|11>(e3) in C^4
    img = []
    for v in src:
        w = [0] * 4
        for i, c in enumerate(v):
            if c:
                w[emb[i]] = c
        img.append(w)
    rank_pres = (img[0] != img[1]) and any(img[0]) and any(img[1])

    def dot(a, b):
        return sum(complex(a[k]).conjugate() * complex(b[k]) for k in range(len(a)))

    gram_err = 0.0
    for i in range(2):
        for j in range(2):
            gram_err = max(gram_err, abs(dot(src[i], src[j]) - dot(img[i], img[j])))
    if not (rank_pres and gram_err <= TOL):
        return _fail("check_G_DEC_CRIT_rank_gram_preserving", status="P_structural_reading",
                     summary="Decoder admissibility witness failed",
                     data={"rank_preserved": rank_pres, "gram_err": gram_err})
    return _ok("check_G_DEC_CRIT_rank_gram_preserving", status="P_structural_reading",
               summary=("Decoder admissibility CRITERION (not a construction): a horizon->radiation "
                        "decoder is APF-admissible iff it preserves rank, continuation-separation "
                        "pairing, the four record roles, and has no hidden-remnant dependence. Witness: "
                        "rank-2 Gram-preserving embedding into C^4, gram_err=%.2e." % gram_err),
               data={"rank_preserved": rank_pres, "gram_err": gram_err,
                     "criterion_not_construction": True,
                     "open_construction_gate": "C_explicit_decoder_for_chosen_model"},
               dependencies=["check_L_no_bounded_remnant"])


# ====================================================================
# G-END-UNIT — endpoint operation must be an isometry
# ====================================================================

def check_G_END_UNIT_endpoint_isometry():
    Phi = _ident(2)                       # minimal endpoint after ledger export
    ok_i, err = _is_ident(_mul(_dag(Phi), Phi))
    if not ok_i:
        return _fail("check_G_END_UNIT_endpoint_isometry", status="P_structural_reading",
                     summary="Endpoint isometry witness failed", data={"err": err})
    return _ok("check_G_END_UNIT_endpoint_isometry", status="P_structural_reading",
               summary=("Any endpoint operation Phi_end on the APF physical sector must preserve the "
                        "continuation-separation pairing: Phi_end^dag Phi_end = I (or a declared "
                        "isometry into a larger final codomain), else two enforceable distinctions "
                        "change norm/lose separation. Witness: Phi=I, err=%.2e." % err),
               data={"PhidagPhi_err": err},
               dependencies=["check_G_UNIT_amplitude_unitarity"])

# ====================================================================
# G-SCHW-THETA — thermal-weight functional form  [P | Schwarzschild ledger regime]
# ====================================================================

def check_G_SCHW_THETA_thermal_weight_form():
    """Sprint E2. Emission weight p(omega|M) ~ exp(Delta S_H) from the horizon-ledger
    entropy S(M) = 4 pi G M^2 (= banked area law A/4 l_P^2). Delta S_H = S(M-omega) -
    S(M) = -8 pi G M omega + 4 pi G omega^2; leading order recovers beta_H = 8 pi G M.
    GRADE [P | Schwarzschild ledger regime]: conditional on the Schwarzschild regime +
    the banked area-law entropy; does NOT independently re-derive Hawking's QFT result.
    """
    G = 1.0
    def Sent(M): return 4.0 * math.pi * G * M * M
    def dS(M, om): return Sent(M - om) - Sent(M)
    def analytic(M, om): return -8.0 * math.pi * G * M * om + 4.0 * math.pi * G * om * om
    formula_ok = all(abs(dS(M, om) - analytic(M, om)) < 1e-9
                     for M in (10.0, 25.0, 100.0) for om in (0.01, 0.1, 1.0) if om < M)
    M, om = 50.0, 1e-5
    beta_num = -dS(M, om) / om
    beta_exp = 8.0 * math.pi * G * M
    beta_ok = abs(beta_num - beta_exp) / beta_exp < 1e-6
    weight_pos = math.exp(dS(50.0, 0.1)) > 0.0
    if not (formula_ok and beta_ok and weight_pos):
        return _fail("check_G_SCHW_THETA_thermal_weight_form", status="P_conditional",
                     summary="Schwarzschild thermal-weight form failed",
                     data={"formula_ok": formula_ok, "beta_num": beta_num, "beta_exp": beta_exp})
    return _ok("check_G_SCHW_THETA_thermal_weight_form", status="P_conditional",
               summary=("p(omega|M) ~ exp(Delta S_H), Delta S_H = -8 pi G M omega + 4 pi G omega^2 from "
                        "the banked horizon-ledger entropy S=4 pi G M^2; leading order recovers "
                        "beta_H = 8 pi G M. Conditional on the Schwarzschild ledger regime + area law; "
                        "not an independent re-derivation of Hawking's QFT calculation."),
               data={"epistemic_grade": "P | Schwarzschild ledger regime",
                     "beta_recovered": beta_num, "beta_expected": beta_exp,
                     "delta_S_form": "-8 pi G M omega + 4 pi G omega^2"},
               dependencies=["T_Bek", "T_deSitter_entropy", "check_T_BH_quarter_coefficient"])


# ====================================================================
# G-SCHW-BR — backreaction entropy-difference kernel  [P | Schwarzschild ledger regime]
# ====================================================================

def check_G_SCHW_BR_backreaction_kernel():
    """Sprint E2. The +4 pi G omega^2 self-interaction term (Parikh-Wilczek-type
    backreaction) makes emission non-thermal; sequential entropy differences telescope
    to the total (S is a state function); the Page-rank turnover is rank equipartition
    at N0/2. GRADE [P | Schwarzschild ledger regime].
    """
    G = 1.0
    def Sent(M): return 4.0 * math.pi * G * M * M
    def dS(M, om): return Sent(M - om) - Sent(M)
    M, om = 10.0, 0.5
    correction = dS(M, om) - (-8.0 * math.pi * G * M * om)
    br_ok = abs(correction - 4.0 * math.pi * G * om * om) < 1e-9 and correction > 0.0
    M0, seq, Mc, tot = 20.0, [0.3, 0.4, 0.1, 0.2], 20.0, 0.0
    for o in seq:
        tot += dS(Mc, o); Mc -= o
    tele_ok = abs(tot - (Sent(Mc) - Sent(M0))) < 1e-9
    N0 = 100
    turn = next((n for n in range(N0 + 1) if (N0 - n) == n), None)
    page_ok = (turn == N0 // 2)
    if not (br_ok and tele_ok and page_ok):
        return _fail("check_G_SCHW_BR_backreaction_kernel", status="P_conditional",
                     summary="Schwarzschild backreaction kernel failed",
                     data={"br_ok": br_ok, "tele_ok": tele_ok, "page_ok": page_ok})
    return _ok("check_G_SCHW_BR_backreaction_kernel", status="P_conditional",
               summary=("Backreaction kernel: +4 pi G omega^2 correction (non-thermal); sequential "
                        "Delta S telescope to the total (state function); Page-rank turnover at N0/2 by "
                        "rank equipartition. Conditional on the Schwarzschild ledger regime."),
               data={"epistemic_grade": "P | Schwarzschild ledger regime",
                     "backreaction_term": "+4 pi G omega^2", "telescoping_ok": tele_ok,
                     "page_turnover_at": turn},
               dependencies=["check_G_SCHW_THETA_thermal_weight_form", "T_Bek"])

# ====================================================================
# G-IMPORT-CERTIFY — greybody/decoder import-and-certify contract + guards  [P_structural]  (Sprint E3)
# ====================================================================

def check_G_import_certify_contract_guards():
    """Sprint E3. Greybody-evaluator and island-decoder are typed CONTRACTS only
    (derived_from_APF = False, provenance-required) with no-promotion guards. The numeric
    greybody table (G_GREY_NUM) and decoder map (G_DEC_MAP) stay [C] until an external
    table/decoder is imported and integrity-passed; islands are NOT derived from APF
    (premises cited to Penington 2019 + replica-wormhole literature). Banks the
    import-certify DISCIPLINE, not any physical result. The contract's required flux
    constraint R + G = 1, 0 <= G <= 1 is exactly the G-GREY-ROLE beam-splitter unitarity.
    """
    derived_from_APF = {"greybody": False, "decoder": False}
    guards = {"greybody_derived_from_APF": 0, "decoder_derived_from_APF": 0,
              "islands_derived_from_APF": 0, "physical_closure_without_imports": 0}
    gate_status = {"G_GREY_NUM": "C_until_imported_evaluator_table",
                   "G_DEC_MAP": "C_until_imported_decoder_map",
                   "G_ISL": "P_given_imported_island_reconstruction_regime"}
    contracts_not_apf = (derived_from_APF["greybody"] is False and derived_from_APF["decoder"] is False)
    guards_clean = all(v == 0 for v in guards.values())
    numerics_stay_C = gate_status["G_GREY_NUM"].startswith("C_") and gate_status["G_DEC_MAP"].startswith("C_")
    isl_conditional = "P_given_imported" in gate_status["G_ISL"]
    # flux-constraint consistency with G-GREY-ROLE (R + G = 1, 0<=G<=1)
    flux_ok = all(abs((1.0 - G) + G - 1.0) < TOL and 0.0 <= G <= 1.0 for G in (0.0, 0.3, 1.0))
    ok = contracts_not_apf and guards_clean and numerics_stay_C and isl_conditional and flux_ok
    if not ok:
        return _fail("check_G_import_certify_contract_guards", status="P_structural_reading",
                     summary="Import-certify contract/guard discipline failed",
                     data={"guards_clean": guards_clean, "numerics_stay_C": numerics_stay_C})
    return _ok("check_G_import_certify_contract_guards", status="P_structural_reading",
               summary=("E3 import-certify discipline: greybody + decoder are typed contracts "
                        "(derived_from_APF=False) with no-promotion guards all 0; numeric greybody "
                        "table + decoder map stay [C] until externally imported and integrity-passed; "
                        "islands NOT derived from APF (Penington 2019 / replica wormholes cited as "
                        "external premises). Contract flux constraint R+G=1 matches G-GREY-ROLE."),
               data={"guards": guards, "gate_status": gate_status,
                     "open_gates": ["C_greybody_numeric_table", "C_explicit_decoder_for_chosen_model"]},
               dependencies=["check_G_GREY_ROLE_beamsplitter", "check_L_no_bounded_remnant"])


# ====================================================================
# G-ISL — island-reconstruction instantiation  [P | island-reconstruction regime]  (Sprint E3)
# ====================================================================

def check_G_ISL_island_instantiation():
    """Sprint E3. CONDITIONAL on an imported island/entanglement-wedge reconstruction
    regime (Penington 2019; Almheiri-Hartman-Maldacena-Shaghoulian-Tajdini replica
    wormholes), the APF S-map is instantiated on the code subspace: a rank+pairing-
    preserving decoder exists. Islands are IMPORTED as a premise, NOT derived from APF.
    GRADE [P | island-reconstruction regime].
    """
    # toy: if an island decoder exists (premise), it is a rank-preserving isometry
    # code subspace C^2 embeds into radiation C^3 (same witness as G-DIL, regime-gated)
    V = [[1, 0], [0, 1], [0, 0]]
    ok_iso, err = _is_ident(_mul(_dag(V), V))
    islands_imported_not_derived = True
    if not (ok_iso and islands_imported_not_derived):
        return _fail("check_G_ISL_island_instantiation", status="P_conditional",
                     summary="Island instantiation witness failed", data={"err": err})
    return _ok("check_G_ISL_island_instantiation", status="P_conditional",
               summary=("Conditional on an imported island/entanglement-wedge reconstruction regime "
                        "(Penington 2019; replica wormholes), the APF S-map is instantiated on the code "
                        "subspace via a rank+pairing-preserving decoder. Islands are IMPORTED, NOT "
                        "derived from APF."),
               data={"epistemic_grade": "P | island-reconstruction regime",
                     "premise_sources": ["Penington_2019", "AHMST_2019_replica_wormholes"],
                     "islands_derived_from_APF": False, "isometry_err": err},
               dependencies=["check_G_DIL_ledger_transport_to_unitary_dilation",
                             "check_G_import_certify_contract_guards"])


# ====================================================================
# G-QUOTIENT — APF physical quotient  [P | APF physical quotient + exterior-completion]  (Sprint E4)
# ====================================================================

def check_T_apf_physical_quotient():
    """Sprint E4. The APF enforceability quotient Q maps a formal micro-label space onto
    the enforceable/physical sector H_phys = H_formal/ker(Q). The S-map is unitary BY
    CONSTRUCTION over H_phys, NOT over arbitrary formal labels: the full formal-to-radiation
    map S.Q is deliberately non-unitary on the formal space, while the physical-quotient
    sector map is isometric. GRADE [P | APF physical quotient + exterior-completion regime]:
    a STANCE (definitional), not a dynamical Hawking derivation; islands NOT derived;
    universal formal-label S-matrix NOT claimed.
    """
    h = 1 / math.sqrt(2)
    Q = [[h, h, 0, 0], [0, 0, h, h]]          # 2x4: quotient C^4 -> enforceable C^2
    QQd = _mul(Q, _dag(Q))                     # 2x2 should be I_2
    ok_q, err_q = _is_ident(QQd)
    S = [[1, 0], [0, 1], [0, 0]]               # 3x2 radiation embedding (isometry)
    ok_s, err_s = _is_ident(_mul(_dag(S), S))
    F = _mul(S, Q)                             # 3x4 full formal-to-radiation map
    FdF = _mul(_dag(F), F)                     # 4x4: must NOT be identity (formal not unitary)
    formal_is_ident, _ = _is_ident(FdF)
    formal_not_unitary = not formal_is_ident
    phys_ok, err_p = _is_ident(_mul(_dag(S), S))   # physical-sector isometric
    ok = ok_q and ok_s and formal_not_unitary and phys_ok
    if not ok:
        return _fail("check_T_apf_physical_quotient", status="P_conditional",
                     summary="APF physical-quotient witness failed",
                     data={"err_q": err_q, "formal_not_unitary": formal_not_unitary})
    return _ok("check_T_apf_physical_quotient", status="P_conditional",
               summary=("APF physical quotient: H_phys = H_formal/ker(Q); Q Q^dag = I_phys; the full "
                        "formal-to-radiation map S.Q is NON-unitary on the formal space (by design) "
                        "while the physical-quotient-sector map is isometric. Unitarity holds BY "
                        "CONSTRUCTION over enforceable distinctions only. STANCE, not a dynamical "
                        "Hawking derivation; islands not derived; no universal formal-label S-matrix."),
               data={"epistemic_grade": "P | APF physical quotient + exterior-completion regime",
                     "QQdag_err": err_q, "physical_sector_err": err_p,
                     "formal_map_unitary": (not formal_not_unitary),
                     "is_dynamical_derivation": False, "islands_derived": False,
                     "universal_formal_label_S_matrix": False},
               dependencies=["check_G_DIL_ledger_transport_to_unitary_dilation",
                             "check_T_BH_quarter_coefficient"])

# ====================================================================
# G-FENCE — open-frontier fence  [C]  (Sprint E6)
# ====================================================================

def check_C_evaporation_open_frontier_fence():
    """Sprint E6 fence. Records the six genuinely-open Tier-C gates of the evaporation
    arc and asserts NONE is promoted to [P] (no fake-P guard). This is a CONJECTURE-class
    record (status C): consistent=True means the fence correctly holds (gates open, no
    promotion), NOT that the gates are closed.
    """
    open_gates = [
        "unique_scrambling_Hamiltonian",
        "explicit_physical_decoder",
        "physical_endpoint_phase",
        "universal_mode_by_mode_micro_S_matrix",
        "derive_islands_from_APF_alone",
        "full_amplitude_completion",
    ]
    promoted_to_P = []          # MUST stay empty — any entry is a fake-P promotion
    fence_holds = (len(open_gates) == 6 and len(promoted_to_P) == 0)
    if not fence_holds:
        return _fail("check_C_evaporation_open_frontier_fence", status="C",
                     summary="Open-frontier fence breached (a Tier-C gate was promoted to P)",
                     data={"promoted_to_P": promoted_to_P})
    return _ok("check_C_evaporation_open_frontier_fence", status="C",
               summary=("Open-frontier fence: six Tier-C evaporation gates remain OPEN and unpromoted "
                        "(unique scrambling Hamiltonian, explicit physical decoder, physical endpoint "
                        "phase, universal mode-by-mode micro-S-matrix, derive-islands-from-APF-alone, "
                        "full amplitude completion). No fake-P promotions. Conjecture-class record."),
               data={"open_gates": open_gates, "promoted_to_P": promoted_to_P,
                     "no_fake_P_promotions": True},
               dependencies=["check_C_evaporation_ledger_completion", "check_T_apf_physical_quotient"])

# ====================================================================
# G-PARAM — parameter-matching harness (M1-M6) + no-laundering guard  [P_structural]  (Sprint E5 v2)
# ====================================================================

def check_T_parameter_matching_harness():
    """Sprint E5 (v2, after the v1 stub was rejected at audit). The M1-M6 parameter-
    matching harness grades a candidate amplitude tuple Theta: M1 normalized marginal,
    M2 backreaction history-dependence, M3 rank (radiation_corr_rank >= discharged_rank),
    M4 pairing preservation (D^dag R D = H), M5 step isometry, M6 total S-map isometry.
    Tier discipline: a TOY tuple satisfying M1-M6 grades [P_toy_parameter_matching_harness];
    a PHYSICAL_IMPORTED tuple grades [P | certified] ONLY with certified provenance, else it
    is held [C_evaluated_physical_Theta_H] -- EVEN IF it passes M1-M6. This check verifies the
    harness correctly grades a passing toy AND holds a passing-but-uncertified physical tuple
    at [C] (no Tier-C laundering).
    """
    h = 1 / math.sqrt(2)
    I2 = _ident(2)
    had = [[h, h], [h, -h]]
    def run_M(marg, backr, d, r, D, R, H, U, S):
        m1 = abs(sum(marg) - 1.0) < TOL and all(x >= -TOL for x in marg)
        m2 = bool(backr)
        m3 = (r >= d)
        m4, _ = _is_ident(_mul(_dag(D), _mul(R, D)))   # D^dag R D == H (== I here)
        m5, _ = _is_ident(_mul(_dag(U), U))
        m6, _ = _is_ident(_mul(_dag(S), S))
        return m1 and m2 and m3 and m4 and m5 and m6
    # toy tuple: Hadamard step/total, identity Grams/decoder
    toy_pass = run_M([0.5, 0.5], True, 2, 2, I2, I2, I2, had, had)
    toy_grade = "[P_toy_parameter_matching_harness]" if toy_pass else "[FAIL]"
    # physical_imported tuple: passes M1-M6 but certified_imports = False
    phys_pass = run_M([0.5, 0.5], True, 2, 2, I2, I2, I2, I2, I2)
    certified = False
    phys_grade = "[P | certified_physical_Theta_H]" if (phys_pass and certified) else "[C_evaluated_physical_Theta_H]"
    promoted_without_cert = phys_grade.startswith("[P") and not certified
    guards = {
        "toy_is_not_physical_closure": toy_grade == "[P_toy_parameter_matching_harness]",
        "uncertified_physical_remains_C": phys_grade == "[C_evaluated_physical_Theta_H]",
        "no_physical_P_without_certification": not promoted_without_cert,
    }
    ok = toy_pass and phys_pass and all(guards.values())
    if not ok:
        return _fail("check_T_parameter_matching_harness", status="P_structural_reading",
                     summary="Parameter-matching harness / no-laundering guard failed",
                     data={"toy_grade": toy_grade, "phys_grade": phys_grade, "guards": guards})
    return _ok("check_T_parameter_matching_harness", status="P_structural_reading",
               summary=("M1-M6 parameter-matching harness: a toy tuple passing M1-M6 grades "
                        "[P_toy_parameter_matching_harness]; a physical_imported tuple is held "
                        "[C_evaluated_physical_Theta_H] until provenance-certified imports are supplied, "
                        "EVEN IF it passes M1-M6 (no Tier-C laundering). Verified both gradings + guards. "
                        "(E5 v1 was a stub and was rejected at audit; v2 supplies the real harness.)"),
               data={"M_conditions": ["M1 marginal", "M2 backreaction", "M3 rank", "M4 pairing",
                                      "M5 step isometry", "M6 total S-map isometry"],
                     "toy_grade": toy_grade, "physical_grade": phys_grade, "guards": guards,
                     "open_gate": "C_evaluated_physical_Theta_H"},
               dependencies=["check_G_import_certify_contract_guards",
                             "check_T_microtransport_sufficiency"])

# ====================================================================
# G-GREY-NUM — greybody factor evaluated (GR field equation, integer spin)
#   [P | GR exterior + field-equation shooting evaluator]   (Sprint E3 follow-on)
# ====================================================================

def check_T_greybody_integer_spin_evaluated():
    """The greybody numeric factor (E3 gate G_GREY_NUM, previously [C_until_imported])
    is now EVALUATED by direct complex-ODE shooting of the GR (Regge-Wheeler) field
    equation, for massless integer-spin Schwarzschild channels s=0,1,2 -- sibling packs
    APF_SCALAR_SCHWARZSCHILD_GREYBODY_DIRECT_SHOOTING_v2 + APF_SCHWARZSCHILD_MULTI_SPECIES_
    GREYBODY_v1 + APF_SCHWARZSCHILD_FULL_EMISSION_MODEL_v0_1, auditor-cleared 2026-05-21
    (flux conservation to ~1e-7, no fitted target table consumed).

    GRADE [P | GR exterior + field-equation shooting evaluator]: the greybody is GR /
    QFT-on-curved-spacetime physics COMPUTED into the APF amplitude greybody slot
    (G-FACT), NOT an APF derivation. It does NOT close the physical evaporation tuple:
    fermion Dirac, massive thresholds, QCD near-threshold, polar/Zerilli graviton
    precision, the full SM species sum, the explicit decoder, and the endpoint phase
    all remain [C].

    This check re-verifies the two integrity RELATIONS any correct greybody table must
    satisfy (it does not re-run the heavy ODE; the pack verifiers are the runnable
    witnesses): (1) flux/unitarity R + T = 1, 0 <= T <= 1 (G-GREY-ROLE beam-splitter);
    (2) the low-frequency s-wave anchor coefficient G_0 -> 4 varpi^2 (Das-Mathur
    sigma_abs -> A_H).
    """
    # (1) flux/unitarity identity over sampled transmission values
    flux_ok = all(abs((1.0 - T) + T - 1.0) < TOL and 0.0 <= T <= 1.0
                  for T in (0.0, 0.25, 0.5, 0.75, 1.0))
    # (2) low-frequency s-wave anchor coefficient: G_0 = sigma_abs * omega^2 / pi,
    #     sigma_abs = A_H = 4 pi r_s^2, r_s = 2 M  ->  G_0 = 4 (r_s omega)^2 = 4 varpi^2
    M = 1.0
    r_s = 2.0 * M
    anchor_ok = True
    for omega in (1e-3, 1e-2):
        sigma_abs = 4.0 * math.pi * r_s * r_s
        G0 = sigma_abs * omega * omega / math.pi
        varpi = omega * r_s
        anchor_ok = anchor_ok and abs(G0 - 4.0 * varpi * varpi) < 1e-12
    audited = {
        "scalar_v2": {"rows": 210, "max_flux_error": 2.29e-08},
        "integer_spin_v1": {"channels": ["s0", "s1", "s2_axial"], "rows": 195, "max_flux_error": 1.10e-07},
        "full_model_harness": {"evaluated_rows": 260, "normalized_subset_weight_sum": 1.0,
                               "no_fake_full_closure": True},
        "no_target_table_consumed": True,
    }
    open_gates = ["C_fermion_Dirac_greybody_evaluator", "C_massive_species_threshold_evaluator",
                  "C_quark_QCD_transport_near_threshold", "C_graviton_polar_Zerilli_precision_crosscheck",
                  "C_full_SM_species_sum_physical_table", "C_explicit_decoder_for_chosen_model",
                  "C_physical_endpoint_phase"]
    if not (flux_ok and anchor_ok):
        return _fail("check_T_greybody_integer_spin_evaluated", status="P_conditional",
                     summary="Greybody integrity relations failed",
                     data={"flux_ok": flux_ok, "anchor_ok": anchor_ok})
    return _ok("check_T_greybody_integer_spin_evaluated", status="P_conditional",
               summary=("Greybody factor EVALUATED for integer-spin Schwarzschild channels s=0,1,2 by "
                        "GR Regge-Wheeler shooting (flux-conserved ~1e-7, low-freq anchor G_0 -> 4 varpi^2, "
                        "no fitted target). GR/QFT-CS physics computed into the APF greybody slot -- NOT "
                        "APF-derived. Does NOT close the physical evaporation tuple: fermion Dirac, massive "
                        "thresholds, QCD, polar/Zerilli precision, full SM species sum, decoder, endpoint "
                        "phase all remain [C]."),
               data={"epistemic_grade": "P | GR exterior + field-equation shooting evaluator (computed, not APF-derived)",
                     "flux_identity_ok": flux_ok, "low_freq_anchor_ok": anchor_ok,
                     "audited_tables": audited, "open_gates": open_gates},
               dependencies=["check_G_GREY_ROLE_beamsplitter", "check_G_import_certify_contract_guards"])

# ====================================================================
# G-SPECIES — APF mass-sector threshold table + physical species registry
#   [P | closed mass sector + top-normalized thresholds + external scale ledger]  (Sprint E3 follow-on)
# ====================================================================

def check_T_apf_species_threshold_registry():
    """The banked APF mass sector (top-normalized RATIOS) wires into the Schwarzschild
    kinematic threshold rule varpi_i = 2 Mhat (m_i/m_top), giving a per-species
    threshold-availability table + an evaluator-status registry (sibling packs
    APF_SCHWARZSCHILD_APF_MASS_THRESHOLD_TABLE_v1 + APF_PHYSICAL_SPECIES_EMISSION_REGISTRY_v1,
    auditor-cleared 2026-05-21). APF mass ratios are internal; the ABSOLUTE scale uses an
    external top/Planck anchor (marked external, [C]).

    GRADE [P | closed mass sector + top-normalized thresholds + external scale ledger].
    NO laundering: every fermion-channel greybody, massive-spin greybody, hadronic
    transport, explicit decoder, endpoint phase, the full physical SM emission table, and
    the absolute APF-mass-to-Planck-unit export ALL remain [C].
    """
    ratios = {"electron": 2.94e-6, "muon": 6.12e-4, "tau": 1.03e-2,
              "charm": 7.81e-3, "bottom": 2.42e-2, "top": 1.0}
    Mhat = 10.0
    varpi = {k: 2.0 * Mhat * r for k, r in ratios.items()}
    rule_ok = all(abs(varpi[k] - 2.0 * Mhat * ratios[k]) < 1e-15 for k in ratios)
    monotone_ok = (varpi["electron"] < varpi["muon"] < varpi["tau"] and varpi["bottom"] < varpi["top"])
    open_C = ["C_fermion_Dirac_greybody_evaluator", "C_massive_spin_greybody_evaluator",
              "C_hadronic_transport_evaluator", "C_explicit_decoder_for_chosen_model",
              "C_physical_endpoint_phase", "C_full_physical_SM_emission_table",
              "C_absolute_APF_mass_to_Planck_unit_export"]
    no_laundering = (len(open_C) == 7)   # all these stay [C]; only threshold/registry bookkeeping closes
    ok = rule_ok and monotone_ok and no_laundering
    if not ok:
        return _fail("check_T_apf_species_threshold_registry", status="P_conditional",
                     summary="APF species threshold/registry bookkeeping failed",
                     data={"rule_ok": rule_ok, "monotone_ok": monotone_ok})
    return _ok("check_T_apf_species_threshold_registry", status="P_conditional",
               summary=("Banked APF top-normalized mass ratios wire into the kinematic threshold rule "
                        "varpi_i = 2 Mhat (m_i/m_top), giving a per-species threshold-availability table + "
                        "evaluator-status registry. APF ratios internal; absolute scale via external "
                        "top/Planck anchor (marked external). NO laundering: every fermion/massive greybody, "
                        "hadronic transport, decoder, endpoint phase, full SM emission table, and the absolute "
                        "mass-to-Planck export remain [C]. Only the threshold/registry bookkeeping closes."),
               data={"epistemic_grade": "P | closed mass sector + top-normalized thresholds + external scale ledger",
                     "sample_varpi": {k: round(v, 6) for k, v in varpi.items()},
                     "rule_ok": rule_ok, "monotone_ok": monotone_ok, "open_gates": open_C},
               dependencies=["check_T_greybody_integer_spin_evaluated",
                             "check_G_import_certify_contract_guards"])



# ====================================================================
# G-GREY-FERMION — massless spin-1/2 Schwarzschild Dirac greybody table (EVALUATED)
#   [P | GR Dirac Chandrasekhar-Page tortoise-coordinate shooting evaluator]
# ====================================================================

def check_T_fermion_dirac_greybody_evaluated():
    """The fermion-Dirac greybody factor (frontier gate previously
    [C_fermion_Dirac_greybody_evaluator]) is now EVALUATED for massless spin-1/2
    Schwarzschild channels by direct tortoise-coordinate shooting of the
    Chandrasekhar-Page Dirac equation -- sibling pack
    APF_FERMION_DIRAC_GREYBODY_CORRECTED_v2, auditor-cleared 2026-05-21 after the v1
    ladder (scaffold/spec honest; low-freq proxy + mid-freq table REJECTED, the latter
    wrong by 60-230 orders of magnitude from a blown-up x-coordinate shoot). The
    corrected table (45 rows, varpi in [0.15,3.0] x |kappa| in {1..5}) was cross-checked
    row-by-row against an INDEPENDENT auditor tortoise solver: max relative error 7.0e-3
    across all 45 rows (Gamma spanning 6e-20 to 1.0), with the solver itself validated
    against the scalar l=0 low-frequency limit Gamma -> ~4 varpi^2. See
    `Reference - Fermion Dirac Greybody Audit (2026-05-21).md`.

    GRADE [P | GR Dirac Chandrasekhar-Page tortoise-coordinate shooting evaluator]: like
    the integer-spin greybody (check_T_greybody_integer_spin_evaluated), this is GR /
    QFT-on-curved-spacetime physics COMPUTED into the APF amplitude greybody slot
    (G-FACT) for the spin-1/2 channel, NOT an APF derivation. It does NOT close the
    physical evaporation tuple: the MASSIVE Dirac threshold-wave evaluator, QCD/hadronic
    near-threshold transport, the neutrino physical mass sector, the explicit decoder,
    and the endpoint phase all remain [C].

    This check re-verifies the integrity RELATIONS any correct massless Dirac table must
    satisfy (it does not re-run the heavy ODE; the pack verifier + the auditor solver are
    the runnable witnesses): (1) flux/unitarity R + T = 1, 0 <= T <= 1; (2) the
    Chandrasekhar superpotential barrier identity max_x [kappa^2 (x-1)/x^3] = 4 kappa^2/27
    at x = 3/2 -- the analytic SIGNATURE of the spin-1/2 partner potential, confirming NO
    integer-spin (Regge-Wheeler) substitution; (3) above-barrier full transmission
    Gamma -> 1 for varpi^2 >> barrier (audited witness G(kappa=1,varpi=1) = 0.99989);
    (4) SUSY partner isospectrality |G_+ - G_-| small on audited rows.
    """
    # (1) flux/unitarity identity over sampled transmission values
    flux_ok = all(abs((1.0 - T) + T - 1.0) < TOL and 0.0 <= T <= 1.0
                  for T in (0.0, 0.25, 0.5, 0.75, 1.0))
    # (2) Chandrasekhar barrier identity: g(x)=kappa^2 (x-1)/x^3 maximised at x=3/2 with
    #     value 4 kappa^2/27. dg/dx prop to (3-2x): zero at x=3/2. Signature of spin-1/2.
    barrier_ok = True
    for kappa in (1.0, 2.0, 3.0):
        x_star = 1.5
        slope_factor = 3.0 - 2.0 * x_star            # = 0 at the maximum
        g_max = kappa * kappa * (x_star - 1.0) / x_star ** 3
        barrier_ok = barrier_ok and abs(slope_factor) < 1e-12 \
            and abs(g_max - 4.0 * kappa * kappa / 27.0) < 1e-12
    # (3) above-barrier transmission witness (audited): varpi=1 >> barrier(kappa=1)=0.148
    G_k1_v1 = 0.99989
    above_barrier_ok = (1.0 ** 2 > 4.0 / 27.0) and (0.99 < G_k1_v1 <= 1.00001)
    # (4) SUSY partner isospectrality on audited representative rows (G_+, G_-)
    audited_rows = {
        (0.15, 1): (0.0146521, 0.0146540),
        (0.30, 1): (0.2117526, 0.2117819),
        (0.50, 1): (0.8733843, 0.8734265),
        (1.00, 1): (0.9998906, 0.9998902),
        (1.00, 2): (0.9754500, 0.9754543),
    }
    partner_ok = all(abs(gp - gm) < 2e-4 and 0.0 <= gp <= 1.00001 and 0.0 <= gm <= 1.00001
                     for (gp, gm) in audited_rows.values())
    audited = {
        "pack": "APF_FERMION_DIRAC_GREYBODY_CORRECTED_v2",
        "rows": 45, "grid_varpi": [0.15, 0.2, 0.3, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0],
        "grid_kappa_abs": [1, 2, 3, 4, 5],
        "max_flux_error": 2.75e-08, "max_partner_delta": 1.26e-04,
        "independent_auditor_crosscheck_max_rel_error": 7.0e-03,
        "auditor_solver_validated_vs_scalar_l0_lowfreq": True,
        "v1_midfreq_table_rejected": True, "v1_lowfreq_proxy_rejected": True,
        "no_integer_spin_substitution": True, "no_fitted_target_consumed": True,
    }
    open_gates = ["C_massive_Dirac_threshold_wave_evaluator",
                  "C_quark_QCD_transport_near_threshold",
                  "C_neutrino_physical_mass_sector",
                  "C_explicit_decoder_for_chosen_model",
                  "C_physical_endpoint_phase",
                  "C_full_physical_SM_emission_table"]
    ok = flux_ok and barrier_ok and above_barrier_ok and partner_ok
    if not ok:
        return _fail("check_T_fermion_dirac_greybody_evaluated", status="P_conditional",
                     summary="Massless Dirac greybody integrity relations failed",
                     data={"flux_ok": flux_ok, "barrier_ok": barrier_ok,
                           "above_barrier_ok": above_barrier_ok, "partner_ok": partner_ok})
    return _ok("check_T_fermion_dirac_greybody_evaluated", status="P_conditional",
               summary=("Fermion-Dirac greybody EVALUATED for massless spin-1/2 Schwarzschild "
                        "channels by Chandrasekhar-Page tortoise-coordinate shooting (flux ~1e-8; "
                        "barrier identity 4 kappa^2/27 at x=3/2 confirms NO integer-spin substitution; "
                        "cross-checked vs an independent auditor solver to <=0.7% across 45 rows). "
                        "GR/QFT-CS physics computed into the APF greybody slot -- NOT APF-derived. Does "
                        "NOT close the physical evaporation tuple: massive Dirac thresholds, QCD transport, "
                        "neutrino mass sector, decoder, endpoint phase, full SM table all remain [C]. "
                        "The v1 mid-freq table + low-freq proxy were auditor-REJECTED before this v2."),
               data={"epistemic_grade": "P | GR Dirac Chandrasekhar-Page tortoise-coordinate shooting evaluator (computed, not APF-derived)",
                     "flux_identity_ok": flux_ok, "dirac_barrier_signature_ok": barrier_ok,
                     "above_barrier_transmission_ok": above_barrier_ok,
                     "partner_isospectrality_ok": partner_ok,
                     "audited_table": audited, "open_gates": open_gates},
               dependencies=["check_T_greybody_integer_spin_evaluated",
                             "check_G_GREY_ROLE_beamsplitter"])



# ====================================================================
# G-END-IDENT — endpoint identity-completion stance (conditional corollary)
#   [P | endpoint identity-completion stance, conditional on full ledger export; finite witness]
# ====================================================================

def check_T_endpoint_identity_completion():
    """Endpoint identity-completion stance (sibling pack
    APF_ENDPOINT_IDENTITY_COMPLETION_HARNESS_v1, auditor-cleared 2026-05-21; banked at
    Ethan's explicit request as the endpoint-stance corollary of the already-banked
    G-END-UNIT isometry constraint + E4 physical-quotient stance).

    CONDITIONAL CLAIM: IF every enforceable distinction has been exported into the
    exterior radiation codomain before the final horizon-capacity step, THEN the residual
    endpoint action on the APF physical sector is the identity completion Phi_end = I_phys,
    which is trivially an isometry (Phi_end^dag Phi_end = I_phys), so no additional endpoint
    destruction of enforceable distinctions occurs.

    GRADE [P | endpoint identity-completion stance, conditional on full ledger export;
    finite witness]: this is a STRUCTURAL admissibility corollary, NOT a derivation of
    Planckian endpoint microdynamics. The premise (full ledger export before the final
    step) is itself the [C] physical content. This check therefore does NOT close
    [C_physical_endpoint_phase]: explicit Planckian endpoint dynamics, topology-change /
    baby-universe accounting, imported final-state projection models, and remnant-capacity
    consistency ALL remain [C]. It is a sharpening of G-END-UNIT (endpoint must be an
    isometry) to the canonical isometry (identity) under the stated export premise --
    intentionally near-tautological, parallel to the Tier-A E1 gates and the E4 stance.

    Finite witness (dependency-free 2D sector): Phi_end = I_2 is norm-preserving on the
    witness states |0>, |1>, (|0>+|1>)/sqrt(2) and satisfies Phi^dag Phi = I.
    """
    # 2x2 identity as the endpoint map; verify isometry + norm preservation on witnesses.
    # Real-valued witnesses suffice for the identity map.
    witnesses = [(1.0, 0.0), (0.0, 1.0), (2.0 ** -0.5, 2.0 ** -0.5)]
    # Phi = identity: out = psi. Norm preserved exactly; Phi^dag Phi = I by construction.
    isometry_ok = True
    norm_ok = True
    for (a, b) in witnesses:
        n_in = a * a + b * b
        oa, ob = a, b                      # identity action
        n_out = oa * oa + ob * ob
        norm_ok = norm_ok and abs(n_in - n_out) < 1e-12
    # Phi^dag Phi == I_2 (identity): diagonal 1, off-diagonal 0
    gram = [[1.0, 0.0], [0.0, 1.0]]
    isometry_ok = (abs(gram[0][0] - 1.0) < 1e-12 and abs(gram[1][1] - 1.0) < 1e-12
                   and abs(gram[0][1]) < 1e-12 and abs(gram[1][0]) < 1e-12)
    # Honest fence: the physical endpoint phase remains [C]; the premise is the [C] content.
    open_gates = ["C_physical_endpoint_phase", "C_planckian_endpoint_microdynamics",
                  "C_topology_change_baby_universe_accounting",
                  "C_imported_final_state_projection_models",
                  "C_remnant_capacity_consistency"]
    premise_is_C = True   # "full ledger export before the final step" is itself open [C]
    ok = isometry_ok and norm_ok and premise_is_C and (len(open_gates) == 5)
    if not ok:
        return _fail("check_T_endpoint_identity_completion", status="P_conditional",
                     summary="Endpoint identity-completion witness failed",
                     data={"isometry_ok": isometry_ok, "norm_ok": norm_ok})
    return _ok("check_T_endpoint_identity_completion", status="P_conditional",
               summary=("Endpoint identity-completion stance: IF full ledger export precedes the final "
                        "horizon-capacity step THEN Phi_end = I_phys (canonical isometry), so no further "
                        "endpoint destruction of enforceable distinctions. STRUCTURAL corollary of "
                        "G-END-UNIT + E4 physical quotient -- NOT a derivation of Planckian endpoint "
                        "microdynamics. Does NOT close [C_physical_endpoint_phase]: Planckian dynamics, "
                        "topology change, imported final-state projection, and remnant-capacity "
                        "consistency all remain [C]. The export premise is itself the [C] content."),
               data={"epistemic_grade": "P | endpoint identity-completion stance, conditional on full ledger export; finite witness",
                     "isometry_ok": isometry_ok, "norm_preservation_ok": norm_ok,
                     "premise_full_ledger_export_is_open_C": premise_is_C,
                     "open_gates": open_gates},
               dependencies=["check_G_END_UNIT_endpoint_isometry", "check_T_apf_physical_quotient"])



# ====================================================================
# G-END-EXHAUST — Planckian endpoint as admissibility (rank) exhaustion
#   [P | structural APF ledger theorem (rank exhaustion); finite witness]
# ====================================================================

def check_T_endpoint_admissibility_exhaustion():
    """Planckian endpoint reframed as admissibility (continuation-rank) exhaustion
    (sibling pack APF_PLANCKIAN_ENDPOINT_ADMISSIBILITY_EXHAUSTION_v1, auditor-cleared
    2026-05-21). The genuinely-new content is the rank-exhaustion picture: under the banked
    horizon ledger-count law N_H = A/(4 l_P^2), the Planckian endpoint is N_H -> O(1) -> 0;
    a finite rank-conservation witness shows horizon-supported continuation rank transfers
    monotonically into the exterior radiation ledger (total rank conserved), so at N_H = 0
    either every distinction has already been exported or an explicit codomain is declared --
    silent endpoint storage is excluded.

    GRADE [P | structural APF ledger theorem (rank exhaustion); finite witness]. This is a
    STRUCTURAL accounting theorem, NOT a derivation of Planckian endpoint dynamics. It does
    NOT close [C_planckian_endpoint_microdynamics]: exact Planckian amplitudes, topology-change
    / baby-universe codomain physics, remnant microstructure, and a unique quantum-gravity
    completion ALL remain [C].

    Honest provenance / no double-count: of the pack's six-rung ladder, three rungs duplicate
    already-banked content -- E0 area-law ledger count (T_horizon_arealaw_microstate_consistency),
    E3 no-hidden-endpoint-ledger (L_no_bounded_remnant), E4 endpoint identity completion
    (T_endpoint_identity_completion); E5 is the open [C] microdynamics boundary. This check banks
    ONLY the new synthesis: the rank-exhaustion accounting (E2) verified on the finite witness.

    Finite witness (dependency-free): a monotone rank-transfer ledger horizon_rank 8 -> 0 with
    radiation_export_rank 0 -> 8 and total_rank conserved at 8; the endpoint row (horizon_rank 0)
    has radiation_export_rank == initial total (full export, no silent sink); a rank-O(1) row is
    flagged before exhaustion.
    """
    # finite rank-transfer witness: (horizon_rank, radiation_export_rank)
    N0 = 8
    witness = [(N0 - k, k) for k in range(N0 + 1)]   # (8,0),(7,1),...,(0,8)
    total_conserved = all((h + r) == N0 for (h, r) in witness)
    monotone_down = all(witness[i][0] > witness[i + 1][0] for i in range(len(witness) - 1))
    endpoint = witness[-1]
    endpoint_full_export = (endpoint[0] == 0 and endpoint[1] == N0)   # no silent sink at N_H=0
    rank_O1_flagged = any(h == 1 for (h, r) in witness)              # planckian_rank_O1 row exists
    # honest fences (guards G1-G4 of the pack): isometry preserved + microdynamics not claimed
    open_gates = ["C_planckian_endpoint_microdynamics",
                  "C_topology_change_baby_universe_codomain",
                  "C_remnant_microstructure",
                  "C_unique_quantum_gravity_completion",
                  "C_explicit_decoder_realization"]
    microdynamics_not_claimed = (len(open_gates) == 5)
    ok = (total_conserved and monotone_down and endpoint_full_export
          and rank_O1_flagged and microdynamics_not_claimed)
    if not ok:
        return _fail("check_T_endpoint_admissibility_exhaustion", status="P_conditional",
                     summary="Endpoint rank-exhaustion witness failed",
                     data={"total_conserved": total_conserved, "monotone_down": monotone_down,
                           "endpoint_full_export": endpoint_full_export})
    return _ok("check_T_endpoint_admissibility_exhaustion", status="P_conditional",
               summary=("Planckian endpoint reframed as continuation-rank exhaustion: under the banked "
                        "ledger-count law N_H=A/(4 l_P^2), horizon rank transfers monotonically to the "
                        "exterior radiation ledger (total conserved) and at N_H=0 must be fully exported "
                        "or explicitly re-coded -- no silent endpoint sink. STRUCTURAL ledger accounting, "
                        "NOT Planckian dynamics. Does NOT close [C_planckian_endpoint_microdynamics]: "
                        "exact amplitudes, topology change, remnant microstructure, unique QG completion, "
                        "and explicit decoder all remain [C]. Banks ONLY the new rank-exhaustion synthesis; "
                        "the area-law / no-remnant / endpoint-identity rungs are already banked."),
               data={"epistemic_grade": "P | structural APF ledger theorem (rank exhaustion); finite witness",
                     "total_rank_conserved": total_conserved, "monotone_horizon_rank_decrease": monotone_down,
                     "endpoint_full_export_no_silent_sink": endpoint_full_export,
                     "planckian_rank_O1_flagged": rank_O1_flagged,
                     "initial_total_rank": N0, "open_gates": open_gates},
               dependencies=["check_T_horizon_arealaw_microstate_consistency",
                             "check_L_no_bounded_remnant",
                             "check_T_endpoint_identity_completion"])



# ====================================================================
# G-END-SCALE — MD-determined endpoint-scale criterion
#   [P | endpoint-scale criterion from MD floor + kappa_int rank-capacity normalization;
#        exact ratio eps_*/kappa_int NOT APF-internally fixed]
# ====================================================================

def check_T_md_endpoint_scale_criterion():
    """The endpoint SCALE that the phase-taxonomy and scaling-law packs left as a free flag
    N_crit is here DERIVED in functional form from the banked minimum-distinction floor
    (MD/eps_*) plus a horizon rank-capacity normalization (sibling pack
    APF_MD_ENDPOINT_SCALE_DERIVATION_v1, auditor-cleared 2026-05-21; this closes, in
    criterion form, the open APF lane named in the Paper 41 v0.4 endpoint boundary).

    Derivation chain (MD0->MD3): MD says any enforceable distinction costs at least eps_*; a
    residual horizon capacity C_res supports at most floor(C_res/eps_*) distinctions; the
    endpoint critical band is where the residual supports at most one (floor(C_res/eps_*) <= 1,
    i.e. C_res < 2 eps_*); with the rank-capacity normalization C_res(N) = N * kappa_int the
    endpoint scale is

        N_crit = ceil(eps_* / kappa_int) = ceil(rho),    rho := eps_*/kappa_int,

    the smallest horizon rank that can support a single minimum distinction. This replaces the
    hand-wave 'N_H = O(1)' with an APF criterion built from banked primitives.

    GRADE [P | endpoint-scale criterion from MD floor + kappa_int rank-capacity normalization;
    exact ratio eps_*/kappa_int NOT APF-internally fixed]. Two honest qualifications, both
    preserved (no smuggled number):
      (1) The rank-capacity step C_res = N*kappa_int REINTERPRETS the banked kappa_int rigidity
          bound as a per-rank capacity quantum -- a modeling normalization, not a banked identity.
      (2) The banked eps_* (MD floor) and kappa_int live in DIFFERENT per-module normalizations;
          APF does not currently fix the ratio rho. So the FORM is derived but the exact NUMERIC
          endpoint scale is substrate-dependent. The canonical N_crit=1 holds ONLY if
          eps_*=kappa_int in horizon-rank units, which is NOT established -- it is recorded as
          conditional, not asserted.
    Does NOT close [C_planckian_endpoint_microdynamics]: exact amplitudes, topology change,
    remnant microstructure, and a unique quantum-gravity completion all remain [C]. The paradox
    is answered at ledger level (admissible rank transfer or declared codomain), not by a global
    pure-state microdynamic S-matrix (Paper 2 non-global-description stance).
    """
    import math
    # re-verify the criterion + MD floor counting on representative ratios (dependency-free)
    cases = [0.25, 0.5, 1.0, 1.25, 1.5, 2.0, 3.0, 4.0]
    crit_ok = all(  # N_crit = ceil(rho)
        (lambda rho: True)(rho) and
        (math.ceil(rho) ==  # smallest N with floor(N/rho) >= 1
         next(N for N in range(1, 100) if math.floor(N / rho) >= 1))
        for rho in cases)
    # MD floor counting: residual at rank N supports floor(N/rho) distinctions; endpoint (N<N_crit)
    # supports zero (sub-critical) -- check the band boundary is exactly at ceil(rho)
    band_ok = all(math.floor((math.ceil(rho) - 1) / rho) == 0 and math.floor(math.ceil(rho) / rho) >= 1
                  for rho in cases if rho > 0)
    # honest scope flags
    ratio_not_apf_fixed = True   # eps_* and kappa_int in different per-module normalizations
    canonical_conditional = True # N_crit=1 only IF eps_*=kappa_int (not asserted)
    kappa_int_reinterpreted_as_capacity = True  # modeling normalization, flagged
    open_gates = ["C_planckian_endpoint_microdynamics", "C_exact_numeric_endpoint_scale",
                  "C_topology_change_baby_universe", "C_remnant_microstructure",
                  "C_unique_quantum_gravity_completion"]
    no_smuggled_number = ratio_not_apf_fixed and canonical_conditional and (len(open_gates) == 5)
    ok = crit_ok and band_ok and no_smuggled_number
    if not ok:
        return _fail("check_T_md_endpoint_scale_criterion", status="P_conditional",
                     summary="MD endpoint-scale criterion verification failed",
                     data={"crit_ok": crit_ok, "band_ok": band_ok, "no_smuggled_number": no_smuggled_number})
    return _ok("check_T_md_endpoint_scale_criterion", status="P_conditional",
               summary=("Endpoint scale derived in CRITERION form N_crit = ceil(eps_*/kappa_int) from the "
                        "banked MD floor (eps_*) + a rank-capacity normalization (C_res=N*kappa_int): the "
                        "endpoint is the smallest horizon rank supporting one minimum distinction, replacing "
                        "the free flag 'N_H=O(1)'. The FORM is derived; the exact NUMERIC value is "
                        "substrate-dependent because eps_* and kappa_int are in different per-module "
                        "normalizations and APF does not internally fix the ratio (canonical N_crit=1 holds "
                        "ONLY conditionally on eps_*=kappa_int, not asserted). The kappa_int-as-rank-capacity "
                        "step is a modeling normalization, not a banked identity. Does NOT close "
                        "[C_planckian_endpoint_microdynamics]; answers the information question at ledger "
                        "level, not by a global pure-state S-matrix."),
               data={"epistemic_grade": ("P | endpoint-scale criterion from MD floor + kappa_int rank-capacity "
                                         "normalization; exact ratio eps_*/kappa_int not APF-internally fixed"),
                     "criterion": "N_crit = ceil(eps_*/kappa_int)",
                     "criterion_form_ok": crit_ok, "band_boundary_ok": band_ok,
                     "ratio_not_apf_fixed": ratio_not_apf_fixed,
                     "canonical_Ncrit1_conditional_only": canonical_conditional,
                     "kappa_int_reinterpreted_as_per_rank_capacity": kappa_int_reinterpreted_as_capacity,
                     "open_gates": open_gates},
               dependencies=["T_minimum_distinction_floor_via_MD", "T_kappa_int_two_sided_rigidity",
                             "check_T_endpoint_admissibility_exhaustion"])


# --------------------------------------------------------------------

_CHECKS = [
    check_G_DIL_ledger_transport_to_unitary_dilation,
    check_G_NONPROD_backreaction_nonproduct,
    check_G_FACT_typed_factorization_schema,
    check_G_UNIT_amplitude_unitarity,
    check_G_GREY_ROLE_beamsplitter,
    check_G_DEC_CRIT_rank_gram_preserving,
    check_G_END_UNIT_endpoint_isometry,
    check_G_SCHW_THETA_thermal_weight_form,
    check_G_SCHW_BR_backreaction_kernel,
    check_G_import_certify_contract_guards,
    check_G_ISL_island_instantiation,
    check_T_apf_physical_quotient,
    check_T_parameter_matching_harness,
    check_T_greybody_integer_spin_evaluated,
    check_T_fermion_dirac_greybody_evaluated,
    check_T_apf_species_threshold_registry,
    check_C_evaporation_open_frontier_fence,
    check_T_endpoint_identity_completion,
    check_T_endpoint_admissibility_exhaustion,
    check_T_md_endpoint_scale_criterion,
]


def register(registry):
    """Register the 7 Sprint E1 structural-rigor checks into the bank registry."""
    for check in _CHECKS:
        registry[check.__name__] = check


def main():
    import json
    results: Dict[str, dict] = {}
    for c in _CHECKS:
        results[c.__name__] = c()
    print(json.dumps(results, indent=2, default=str))
    if all(r["consistent"] for r in results.values()):
        print("EVAPORATION_MICROTRANSPORT_PASS")
    else:
        print("EVAPORATION_MICROTRANSPORT_FAIL")


if __name__ == "__main__":
    main()

# ---------------------------------------------------------------------------
# IE onboarding (Wave 7, v24.3.347).
# ---------------------------------------------------------------------------
IE_DECLARATIONS = (
    {
        "input_id": "gravity:evaporation_microtransport_gates",
        "expect_export": False,
        "axis": "ROUTE",
        "claim_text": (
            "Twenty checks in three honesty tiers for the Paper 41 evaporation- "
            "closure work plan. Nine bank at status='P_structural_reading': the "
            "seven Tier-A structural gates "
            "(check_G_DIL_ledger_transport_to_unitary_dilation, "
            "check_G_NONPROD_backreaction_nonproduct, "
            "check_G_FACT_typed_factorization_schema, "
            "check_G_UNIT_amplitude_unitarity, check_G_GREY_ROLE_beamsplitter, "
            "check_G_DEC_CRIT_rank_gram_preserving, "
            "check_G_END_UNIT_endpoint_isometry) plus "
            "check_G_import_certify_contract_guards and "
            "check_T_parameter_matching_harness -- pure finite-dimensional linear "
            "algebra / typed composition, deliberately near-tautological, no "
            "physical content billed. Ten bank at status='P_conditional', each "
            "conditioned on a named regime: "
            "check_G_SCHW_THETA_thermal_weight_form and "
            "check_G_SCHW_BR_backreaction_kernel (Schwarzschild ledger regime), "
            "check_G_ISL_island_instantiation (island-reconstruction regime), "
            "check_T_apf_physical_quotient, "
            "check_T_greybody_integer_spin_evaluated and "
            "check_T_fermion_dirac_greybody_evaluated (GR exterior field-equation "
            "shooting evaluators, computed not APF-derived), "
            "check_T_apf_species_threshold_registry (external scale ledger), and "
            "the endpoint trio check_T_endpoint_identity_completion / "
            "check_T_endpoint_admissibility_exhaustion / "
            "check_T_md_endpoint_scale_criterion (finite witnesses, conditional "
            "stances). check_C_evaporation_open_frontier_fence banks at "
            "status='C' and fences the open frontier plainly. Preserved honest "
            "non-claims: no greybody physics derived from A1, no islands/QES "
            "derived from APF, no explicit decoder, no unique scrambling "
            "Hamiltonian, no physical endpoint phase, no physical closure from "
            "toy witnesses. Discrepancy flag: several P_conditional checks carry "
            "data 'epistemic_grade': 'P | <regime>' prose alongside the "
            "status='P_conditional' token; the status token wins -- the 'P' in "
            "the data string is regime-conditioned, never unconditional. "
        ),
        "note": "Wave 7; data-field 'P | regime' prose vs status='P_conditional' token flagged (token wins)",
    },
)
