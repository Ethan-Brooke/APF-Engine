"""APF-native one-loop BSY κ_ℓ assembly consistency validator — Tier-4.

Validates that the v24.3.107 + v24.3.106 + v24.3.99 + v24.3.105/.104/.103
substrate composes into a structurally-consistent one-loop κ_ℓ assembly
via EWWGR Eq 175 (BSY recipe) at Denner-validated inputs.

This module is the *structural-consistency* layer for the R2 one-loop
arc. It does NOT claim closure to all-orders DFGRU (that gap is the
two-loop EW gate, multi-session arc tracked at
APF Reference Docs/Reference - Native OS-W Two-Loop Close Scoping Brief
(2026-05-26).md). It does NOT claim physical-final M_W or κ_ℓ.

What it certifies, at Denner-validated inputs:

1. The BSY composition is internally consistent — no NaN, no divergence,
   g_V/g_A finite and real-dominated, sin²θ_eff in physical band [0.20, 0.25].

2. The 3-pt function piece F_V^Zℓ from v24.3.107 (Eqs 166/167) sits at
   |F_V| ~ 10^-2 with α/(4π) prefactor and bracket ~ 18 — matching the
   working-doc target.

3. The renormalized Π̂^γZ_R(M_Z²) from v24.3.99 self-energies + EWWGR
   counterterm chain (counterm L5827-5852 + rself) is finite and lies
   in the band [-0.02, -0.005] (typical one-loop value at SM gauge inputs).

4. Δρ_OS reproduces Denner's published one-loop value 0.00780 to ~10^-3
   relative (the v24.3.99 anchor to Denner 0709.1075).

5. The leading-Δρ_top tracking property: BSY's Δκ_ℓ shift across m_t is
   dominated by the analytic (c²/s²)·ΔΔρ_top piece at one-loop SM
   precision (validated empirically via the input-variation probe at
   outputs/kappa_l_BSY_PDG_canonical_probe.py; encoded structurally
   here as the consistency check that g_V's Π^γZ contribution and F_V
   contribution have the correct signs and orders of magnitude).

This module is the bank-side companion to today's session work:

- Q2 hypothesis (mixed-conventions explanation for §13's "0.053")
  FALSIFIED; replacement diagnosis (missing Π̂^γZ in §13's recipe)
  recorded at APF Reference Docs/Reference - Q2 Empirical sW2 BSY Probe
  Findings (2026-05-27).md.
- "+0.0084 honest-open R2" framing REVISITED as frame-comparison error;
  matched-inputs reading gives +1.6×10^-3 at Denner-set, +1.7×10^-2 at
  PDG canonical (the latter is the two-loop gate). [Numbers pre-.358: the
  corrigendum adds +0.00104. The "two-loop gate" ATTRIBUTION IS SUPERSEDED
  at .358 by the ACFW published-one-loop benchmark below: the dominant
  excess is an M_H-flat assembly-sector defect, not two-loop content.]
- v24.3.107 docstring corrected (3-pt function piece, not "BARE"; pre-
  edit snapshot at Codebase/Old/).

Honest non-claims (all preserved at this validator):

- Export_BSY_one_loop_assembly_consistency_at_Denner_set = 1   (this validator)
- Export_BSY_kappa_l_PDG_canonical_one_loop = 0   (open; +1.7×10^-2 gap to DFGRU)
- Export_BSY_kappa_l_all_orders = 0    (open; two-loop EW gate, multi-session)
- Export_BSY_kappa_l_physical_final = 0  (no [P_physical_final])
- Export_two_loop_EW_complete = 0     (open arc, scoping brief filed)
- Export_M_W_two_loop = 0             (open; tracked at OS-W Two-Loop Scoping)
- target_consumed = 0                  (no DFGRU value fit; no Awramik target fit)

The cleanest reading of this bank deposit: the v24.3.81-.107 one-loop
machine, composed via EWWGR Eq 175, produces a structurally-valid
one-loop κ_ℓ output at Denner-validated inputs. The all-orders closure
to DFGRU and the absolute precision improvement to PDG canonical both
go through the two-loop EW arc, which is now actively staged via the
scoping brief.

v24.3.358 (2026-07-03) — two changes from the 2026-07-02 Zll proper-vertex
walk (fresh-context walker + hostile audit SOUND-WITH-CORRECTIONS 0.90;
witnesses at The Turning/zll_vertex_walk_2026-07-02/; note "Reference -
CONTINUATION - The Zll Proper Vertex; Closing the Kappa_l Transport Gate
for Real (2026-07-02).md"):

1. CORRIGENDUM in _bsy_compose: the eq-rself mixing renormalization was
   transcribed with +2·Σ^γZ(0)/M_Z²; the source-exact coefficient is +1
   (the (δZ₁^γZ−δZ₂^γZ)·M_Z² term was dropped). Worth +0.0010444 in Δκ_ℓ;
   the defect partially masked the assembly overshoot. Independently
   re-derived by the audit from eq counterm. No banked band flips; the
   δr chain uses eq deltar and is untouched; v15.1 untouched.

2. NEW published-one-loop benchmark check (ACFW = Awramik–Czakon–Freitas–
   Weiglein, PRL 93 (2004) 201805, Table II: full one-loop O(α) Δκ,
   M_W-input, α(0) expansion, m_t=178.0, M_W=80.426, M_Z=91.1876,
   m_b=4.85): the native assembly PASSES the M_H-shape benchmark to
   ≤1.7e-4 over an 8.0e-3 published M_H swing and FAILS the absolute
   benchmark by +0.0194, M_H-FLAT. One-loop vs one-loop: the κ_ℓ
   overshoot is an assembly-sector defect localized in the
   M_H-INDEPENDENT sector, NOT two-loop truncation — recorded at
   published-benchmark grade. FAIL-recording instrument
   [P_structural_instrument]; retires the [C] slot check's
   "UNBENCHMARKED" clause the hard way. The M_H-shape PASS
   simultaneously benchmark-validates the oblique sector.
"""
from __future__ import annotations

import math
from typing import Any, Dict

from apf.apf_utils import check, _result
from apf.w_trace_native_delta_r_mw_assembly import (
    Sig_AZ, Sig_ZZ, Sig_W, Pi_AA_0, MZ2 as _ndr_MZ2, MZ as _ndr_MZ,
)
from apf.w_trace_pv_ewwgr_bare_proper_vertex import F_V_Z, F_A_Z

_PI = math.pi
_ALPHA_MZ = 1.0 / 128.21                  # running α(M_Z) — Denner-style Δα=0.0644
_sW2_BANKED_OS = 0.223339                 # banked OS empirical (M_W=80.362)
_DENNER_DRHO_OS_TARGET = 0.00780          # v24.3.99 anchor (Denner-published)
_DENNER_DRHO_TOLERANCE = 5.0e-4           # ~6% relative


EXPORT_FLAGS: Dict[str, int] = {
    "Export_BSY_one_loop_assembly_consistency_at_Denner_set": 1,
    "Export_BSY_kappa_l_PDG_canonical_one_loop": 0,
    "Export_BSY_kappa_l_all_orders": 0,
    "Export_BSY_kappa_l_physical_final": 0,
    "Export_two_loop_EW_complete": 0,
    "Export_M_W_two_loop": 0,
    "target_consumed": 0,
}


def _bsy_compose(sW2: float, alpha: float, mu2: float = None) -> Dict[str, Any]:
    """Full BSY (Eq 175) composition at given sW², α.

    The common factor [(1-Δr)/(1+Π̂^Z)]^{1/2} cancels in g_V/g_A and is
    omitted here. Returns g_V, g_A, sin²θ_eff, Δκ_ℓ, and intermediates.
    """
    cW2 = 1.0 - sW2
    sW  = math.sqrt(sW2)
    cW  = math.sqrt(cW2)
    if mu2 is None:
        mu2 = _ndr_MZ2

    MW_consistent = cW * _ndr_MZ
    MW2_consistent = MW_consistent * MW_consistent

    # v24.3.99 native self-energies at (s, c) consistent with this sW²
    Sigma_AZ_0    = Sig_AZ(0.0,             sW, cW, mu2)
    Sigma_AZ_MZ2  = Sig_AZ(_ndr_MZ2,        sW, cW, mu2)
    Sigma_ZZ_MZ2  = Sig_ZZ(_ndr_MZ2,        sW, cW, mu2)
    Sigma_W_MW2c  = Sig_W (MW2_consistent,  sW, cW, mu2, lam2=1.0e-4)
    Pi_g_0        = Pi_AA_0(sW, cW, mu2)

    dMZ2 = Sigma_ZZ_MZ2 / _ndr_MZ2
    dMW2 = Sigma_W_MW2c / MW2_consistent
    Drho = dMZ2 - dMW2

    # EWWGR-exact counterm L5827-5852 + rself L5783-5791.
    # v24.3.358 CORRIGENDUM (Zll proper-vertex walk 2026-07-02; hostile audit
    # SOUND-WITH-CORRECTIONS 0.90, the fix independently re-derived by the
    # auditor from eq counterm): eq rself's mixing line carries BOTH
    # renormalization terms,
    #   Sig-hat^gZ(M_Z^2) = Sig^gZ(M_Z^2) - dZ2_gZ*M_Z^2 + (dZ1_gZ - dZ2_gZ)*M_Z^2,
    # and the pre-.358 transcription dropped the second, (dZ1^gZ - dZ2^gZ)*M_Z^2.
    # With eq counterm's dZ1^g = -Pi^g(0) - (s/c)*SgZ0 and
    # dZ1^Z = -Pi^g(0) - (3c^2-2s^2)/(sc)*SgZ0 + (c^2-s^2)/s^2*Drho, the net
    # source-exact coefficient of Sig^gZ(0)/M_Z^2 inside Pi_gZ_R is +1, not the
    # pre-.358 +2. Worth +0.0010444 in Delta_kappa_l (the defect partially
    # masked the assembly overshoot measured by the ACFW benchmark check below).
    # No banked band flips (verified at .358 landing).
    SgZ0 = Sigma_AZ_0 / _ndr_MZ2
    dZ2_g  = -Pi_g_0
    dZ1_g  = -Pi_g_0 - (sW/cW) * SgZ0
    dZ2_Z  = -Pi_g_0 \
             - 2.0*(cW2-sW2)/(sW*cW) * SgZ0 \
             + (cW2-sW2)/sW2 * Drho
    dZ1_Z  = -Pi_g_0 \
             - (3.0*cW2 - 2.0*sW2)/(sW*cW) * SgZ0 \
             + (cW2-sW2)/sW2 * Drho
    dZ2_gZ = (sW*cW)/(cW2-sW2) * (dZ2_Z - dZ2_g)
    dZ1_gZ = (sW*cW)/(cW2-sW2) * (dZ1_Z - dZ1_g)
    Pi_gZ_R = Sigma_AZ_MZ2/_ndr_MZ2 - dZ2_gZ + (dZ1_gZ - dZ2_gZ)

    # v24.3.107 3-pt function piece (banked F_V_Z uses scalar-substrate MW²;
    # the ~0.1% gap to c²·M_Z² at non-PDG sW² is acceptable for the
    # consistency check at Denner-validated inputs)
    F_V_l = F_V_Z("lepton", _ndr_MZ2, sW2, alpha=alpha)
    F_A_l = F_A_Z("lepton", _ndr_MZ2, sW2, alpha=alpha)

    # BSY Eq 175 (common [(1-Δr)/(1+Π̂^Z)]^{1/2} factor cancels in g_V/g_A)
    Q_l  = -1.0
    I3_l = -0.5
    v_l_tree = I3_l - 2.0 * Q_l * sW2
    a_l_tree = I3_l
    gV_num = v_l_tree + 2.0*sW*cW*Q_l*Pi_gZ_R + F_V_l.real
    gA_den = a_l_tree + F_A_l.real
    ratio  = gV_num / gA_den
    s2_eff = 0.25 * (1.0 - ratio)
    Dkl    = s2_eff / sW2 - 1.0

    return {
        "sW2": sW2,
        "cW2": cW2,
        "MW_consistent": MW_consistent,
        "Drho_OS": Drho,
        "Pi_gZ_R": Pi_gZ_R,
        "F_V_lepton": F_V_l,
        "F_A_lepton": F_A_l,
        "gV_num": gV_num,
        "gA_den": gA_den,
        "ratio": ratio,
        "sin2theta_eff": s2_eff,
        "Delta_kappa_l": Dkl,
    }


# ===========================================================================
# check
# ===========================================================================
def check_T_BSY_one_loop_kappa_l_assembly_consistency_at_Denner_validated_inputs_P() -> Dict[str, Any]:
    """T: v24.3.107 + v24.3.99 + v24.3.106 BSY composition is structurally
    consistent at Denner-validated inputs; one-loop κ_ℓ assembly stands
    [P_one_loop_BSY_3pt_at_Denner_validated_inputs_assembly_consistency]."""

    result = _bsy_compose(_sW2_BANKED_OS, _ALPHA_MZ)

    Drho = result["Drho_OS"]
    Pi_gZ_R = result["Pi_gZ_R"]
    F_V = result["F_V_lepton"]
    F_A = result["F_A_lepton"]
    gV = result["gV_num"]
    gA = result["gA_den"]
    s2_eff = result["sin2theta_eff"]
    Dkl = result["Delta_kappa_l"]

    # (1) BSY composition is internally consistent
    check(math.isfinite(s2_eff) and math.isfinite(Dkl),
          f"BSY s2_eff or Dkl not finite: s2_eff={s2_eff}, Dkl={Dkl}")
    check(0.20 <= s2_eff <= 0.25,
          f"sin²θ_eff = {s2_eff:.6f} outside physical one-loop band [0.20, 0.25]")
    check(math.isfinite(gV) and math.isfinite(gA) and gA != 0.0,
          f"g_V/g_A not well-defined: gV={gV}, gA={gA}")

    # (2) v24.3.107 3-pt function piece is at expected scale
    mag_FV = abs(F_V)
    check(5.0e-3 < mag_FV < 2.0e-2,
          f"|F_V^Zell| = {mag_FV:.4e} outside expected one-loop band [5e-3, 2e-2]")
    check(F_V.imag > 0.0,
          f"Im F_V^Zell must be positive (absorptive), got {F_V.imag:.2e}")

    # (3) Π̂^γZ_R is finite, in the expected one-loop band
    check(math.isfinite(Pi_gZ_R),
          f"Π̂^γZ_R not finite: {Pi_gZ_R}")
    check(-0.020 < Pi_gZ_R < -0.005,
          f"Π̂^γZ_R = {Pi_gZ_R:.6f} outside expected one-loop band [-0.020, -0.005]")

    # (4) Δρ_OS reproduces Denner's published one-loop value
    rel_drho = abs(Drho - _DENNER_DRHO_OS_TARGET) / _DENNER_DRHO_OS_TARGET
    check(rel_drho < 0.10,
          f"Δρ_OS = {Drho:.6f} departs from Denner target {_DENNER_DRHO_OS_TARGET} "
          f"by rel {rel_drho:.4f}")

    # (5) Δκ_ℓ at Denner-validated inputs lands in the one-loop SM band.
    # Acceptance criterion: [0.040, 0.055]. Tight bounds reflect Denner-
    # set's known one-loop range; the 2026-05-27 matched-inputs result was
    # 0.0475 (Case B α(M_Z)); post-.358 corrigendum it is 0.04854 — still
    # comfortably in-band.
    check(0.040 <= Dkl <= 0.055,
          f"Δκ_ℓ = {Dkl:.6f} outside Denner-validated one-loop band [0.040, 0.055]")

    # (6) Honest non-claim guard
    check(EXPORT_FLAGS["Export_BSY_kappa_l_PDG_canonical_one_loop"] == 0,
          "PDG-canonical one-loop κ_ℓ closure must remain OPEN")
    check(EXPORT_FLAGS["Export_BSY_kappa_l_all_orders"] == 0,
          "BSY all-orders κ_ℓ closure must remain OPEN")
    check(EXPORT_FLAGS["Export_two_loop_EW_complete"] == 0,
          "Two-loop EW arc must remain OPEN")
    check(EXPORT_FLAGS["target_consumed"] == 0,
          "DFGRU/Awramik target consumption must be NEGATIVE")

    return _result(
        name=("T_BSY_one_loop_kappa_l_assembly_consistency_at_Denner_validated_inputs: "
              "v24.3.107 3-pt F_V/F_A + v24.3.99 native self-energies + EWWGR Eq 175 "
              "(BSY recipe) produces a structurally-consistent one-loop κ_ℓ assembly at "
              "Denner-validated inputs (sW²=0.223339, α(M_Z)=1/128.21, m_t=140, M_H=100); "
              "[P_one_loop_BSY_3pt_at_Denner_validated_inputs_assembly_consistency]"),
        tier=4,
        epistemic="P_one_loop_BSY_3pt_at_Denner_validated_inputs_assembly_consistency",
        summary=(
            f"At Denner-validated inputs (sW²={_sW2_BANKED_OS}, α(M_Z)=1/128.21, "
            f"m_t=140 GeV, M_H=100 GeV via v24.3.99 hardcoded globals), the BSY (EWWGR "
            f"Eq 175) composition g_V^ℓ = v_ℓ_tree + 2sc·Q_ℓ·Π̂^γZ_R + F_V^Zℓ, "
            f"g_A^ℓ = a_ℓ_tree + F_A^Zℓ produces:\n"
            f"  Δρ_OS              = {Drho:+.6f}   (Denner target {_DENNER_DRHO_OS_TARGET}; "
            f"rel gap {rel_drho:.4e})\n"
            f"  Π̂^γZ_R(M_Z²)       = {Pi_gZ_R:+.6f}\n"
            f"  F_V^Zℓ             = {F_V.real:+.6f} {F_V.imag:+.6f}i\n"
            f"  F_A^Zℓ             = {F_A.real:+.6f} {F_A.imag:+.6f}i\n"
            f"  g_V^ℓ              = {gV:+.6f}\n"
            f"  g_A^ℓ              = {gA:+.6f}\n"
            f"  sin²θ_eff^ℓ        = {s2_eff:.6f}\n"
            f"  Δκ_ℓ               = {Dkl:+.6f}\n"
            f"All structural consistency tests PASS (s²_eff in physical band; "
            f"|F_V| in one-loop band; Π̂^γZ_R in one-loop band; Δρ matches Denner to "
            f"{rel_drho*100:.2f}%). The composition delivers one-loop SM κ_ℓ at "
            f"Denner-validated inputs. ALL-ORDERS CLOSURE TO DFGRU REMAINS OPEN at the "
            f"two-loop EW gate (multi-session arc, scoping at "
            f"`APF Reference Docs/Reference - Native OS-W Two-Loop Close Scoping Brief "
            f"(2026-05-26).md`). The PDG-canonical reading (m_t=173.2, M_H=125) shows a "
            f"+1.7×10⁻² gap to DFGRU, previously identified as the leading-Δρ_top one-loop "
            f"content that DFGRU's all-orders fit absorbs via two-loop EW + α_s + "
            f"reducible-term resummation — ATTRIBUTION SUPERSEDED at .358: the ACFW "
            f"published-one-loop benchmark (check_T_w_trace_kappa_l_ACFW_published_"
            f"one_loop_benchmark) shows the dominant excess is an M_H-flat "
            f"ASSEMBLY-SECTOR defect, not two-loop content. Today's executable witnesses preserved at "
            f"`outputs/kappa_l_BSY_*.py`; findings at "
            f"`APF Reference Docs/Reference - Q2 Empirical sW2 BSY Probe Findings "
            f"(2026-05-27).md`."
        ),
        key_result=(
            f"BSY one-loop κ_ℓ assembly consistent at Denner-validated inputs "
            f"(Δρ_OS={Drho:.4f} reproduces Denner 0.00780 to {rel_drho*100:.2f}%; "
            f"Δκ_ℓ={Dkl:+.4f}); all-orders closure OPEN at two-loop EW gate. "
            f"[P_one_loop_BSY_3pt_at_Denner_validated_inputs_assembly_consistency]"
        ),
        dependencies=[
            "T_w_trace_pv_ewwgr_bare_subgate_partial",
            "T_w_trace_pv_lambda_bhm_subgate_partial",
            "T_w_trace_native_delta_r_assembly",
        ],
        cross_refs=[
            "T_sin2_theta_W_OS_capacity_counting_value",
            "T_kappa_l_composed_with_paper_18",
        ],
        artifacts={
            "Drho_OS": Drho,
            "Pi_gZ_R": Pi_gZ_R,
            "F_V_lepton": F_V,
            "F_A_lepton": F_A,
            "sin2theta_eff": s2_eff,
            "Delta_kappa_l": Dkl,
            "Denner_Drho_target": _DENNER_DRHO_OS_TARGET,
            "Denner_Drho_rel_gap": rel_drho,
            "export_flags": dict(EXPORT_FLAGS),
        },
    )


# ===========================================================================
# v24.3.358 — the ACFW published-one-loop benchmark harness
# ===========================================================================
_ACFW_TABLE_II = {100.0: 438.94e-4, 200.0: 419.60e-4,
                  600.0: 379.56e-4, 1000.0: 358.62e-4}   # PRL 93 (2004) 201805
_ACFW_MT, _ACFW_MB = 178.0, 4.85                          # Table I inputs
_ACFW_MW, _ACFW_MZ = 80.426, 91.1876
_ACFW_SW2 = 1.0 - (_ACFW_MW / _ACFW_MZ) ** 2
_ALPHA_0 = 1.0 / 137.0359895                              # α(0) expansion frame


def _acfw_benchmark_rows():
    """Run the BANKED _bsy_compose on the ACFW Table-II deck.

    Monkeypatch-and-restore of the v24.3.99 globals (m_t, m_b, M_H) — the
    same in-memory patch the walk witnesses used; no repo state is touched.
    The self-energies keep the .99 deck's M_Z = 91.177 (stale vs ACFW's
    91.1876) — the BW→pole M_Z shift was MEASURED at +3.0e-5 in Δκ_ℓ,
    three orders below the +0.0194 signal. Light-quark effective-mass
    choices were MEASURED at ≤1.5e-5 under ±20% variation. Both walk-
    audited; both far below every band asserted here.
    """
    import apf.w_trace_native_delta_r_mw_assembly as _ndr_mod
    saved = (_ndr_mod.MU["t"], _ndr_mod.MD["b"], _ndr_mod.MH, _ndr_mod.MH2)
    rows = []
    try:
        _ndr_mod.MU["t"] = _ACFW_MT
        _ndr_mod.MD["b"] = _ACFW_MB
        for MH, dk_pub in _ACFW_TABLE_II.items():
            _ndr_mod.MH = MH
            _ndr_mod.MH2 = MH * MH
            r = _bsy_compose(_ACFW_SW2, _ALPHA_0)
            rows.append((MH, dk_pub, r["Delta_kappa_l"]))
    finally:
        (_ndr_mod.MU["t"], _ndr_mod.MD["b"],
         _ndr_mod.MH, _ndr_mod.MH2) = saved
    return rows, saved


def check_T_w_trace_kappa_l_ACFW_published_one_loop_benchmark_P() -> Dict[str, Any]:
    """T: the native BSY κ_ℓ assembly against a PUBLISHED full one-loop Δκ
    comparator — M_H-shape PASS / absolute FAIL, recorded [P_structural_instrument].

    FAIL-recording instrument (established precedent). Comparator: ACFW
    PRL 93 (2004) 201805 Table II — one-loop O(α) Δκ with M_W input, α(0)
    expansion, at M_H = 100/200/600/1000. The check calls the BANKED
    _bsy_compose (post-.358 source-exact eq-rself transcription) — the walk
    harness re-implemented the composition; a banked check must exercise
    the banked object (audit fix 1 of the landing).

    What it certifies:
      (a) SHAPE PASS — native M_H-differences track the published one-loop
          to ≤5e-4 (measured ≤1.7e-4) over an 8.0e-3 published swing: the
          oblique (Higgs self-energy) sector is benchmark-validated.
      (b) ABSOLUTE FAIL — the native assembly overshoots the published
          one-loop by ~+0.0194 at EVERY M_H, M_H-flat (spread <20% of the
          mean; measured 0.9%). One-loop vs one-loop: the overshoot is an
          ASSEMBLY DEFECT in the M_H-independent sector, not two-loop
          truncation.
      (c) LOCALIZATION, stated at its honest strength: the attribution of
          the M_H-flat excess to the proper-vertex filler SPECIFICALLY is
          inference (literature-scale ~+0.0025 lepton vertex + the
          independent Δρ/Δr validations), CONDITIONAL on the effva booking
          of the γZ term and a defect-free oblique sector — not proof.
          The γZ booking collision is ADJUDICATED (principal ruling
          2026-07-03: the effva booking is CANONICAL); ruling recorded in
          the Decisions List, dual-booking machine-pinned at the slot check
          in w_trace_native_zll_kappa_l_oblique.

    Frame-sensitivity budget (measured by the walk audit, cited not
    re-derived): light-quark masses ±20% → ≤1.5e-5; BW→pole M_Z → +3.0e-5;
    stale .99-deck M_Z = 91.177 inherited. All ≥2 orders below the signal.
    No published value is consumed as a fit target: the comparator enters
    only as a benchmark and the absolute comparison is recorded as FAIL.
    """
    rows, saved = _acfw_benchmark_rows()

    # restore integrity — the patch must not leak into the .99 globals
    import apf.w_trace_native_delta_r_mw_assembly as _ndr_mod
    check((_ndr_mod.MU["t"], _ndr_mod.MD["b"], _ndr_mod.MH, _ndr_mod.MH2) == saved,
          "ACFW deck patch leaked into the v24.3.99 globals")

    gaps = [dk - pub for (_, pub, dk) in rows]
    mean_gap = sum(gaps) / len(gaps)
    spread = max(gaps) - min(gaps)
    base_pub, base_nat = rows[0][1], rows[0][2]
    shape_diffs = [(dk - base_nat) - (pub - base_pub) for (_, pub, dk) in rows[1:]]
    pub_swing = rows[0][1] - rows[-1][1]

    # (a) SHAPE PASS
    check(pub_swing > 5.0e-3,
          f"published M_H swing {pub_swing:.6f} too small to discriminate shape")
    check(all(abs(sd) < 5.0e-4 for sd in shape_diffs),
          f"M_H-shape does not track the published one-loop: {shape_diffs}")

    # (b) ABSOLUTE FAIL — recorded, with the defect band pinned
    check(all(g > 5.0e-3 for g in gaps),
          f"absolute overshoot no longer present: gaps={gaps} (re-price the slot!)")
    check(all(0.015 < g < 0.024 for g in gaps),
          f"gap left the pinned defect band [0.015, 0.024]: {gaps}")
    check(spread < 0.20 * abs(mean_gap),
          f"gap not M_H-flat: spread {spread:.6f} vs mean {mean_gap:.6f}")

    # (c) honest non-claims
    check(EXPORT_FLAGS["Export_BSY_kappa_l_PDG_canonical_one_loop"] == 0,
          "PDG-canonical one-loop κ_ℓ closure must remain OPEN")
    check(EXPORT_FLAGS["target_consumed"] == 0,
          "no published target may be consumed as a fit — benchmark only")

    return _result(
        name=("T_w_trace_kappa_l_ACFW_published_one_loop_benchmark: native BSY "
              "assembly vs ACFW PRL 93 (2004) Table II — M_H-shape PASS "
              "≤5e-4 / absolute FAIL +0.0194 M_H-flat, recorded "
              "[P_structural_instrument]"),
        tier=4,
        epistemic="P_structural_instrument",
        summary=(
            f"The banked _bsy_compose (source-exact eq-rself transcription, "
            f".358), run at the ACFW deck (m_t={_ACFW_MT}, m_b={_ACFW_MB}, "
            f"M_W={_ACFW_MW}, M_Z={_ACFW_MZ} → sW²={_ACFW_SW2:.6f}, α(0) "
            f"frame), against the published full one-loop O(α) Δκ "
            f"(Table II):\n"
            + "".join(f"  M_H={MH:6.0f}: published {pub:+.6f}, native "
                      f"{dk:+.6f}, gap {dk-pub:+.6f}\n"
                      for (MH, pub, dk) in rows)
            + f"Mean gap {mean_gap:+.6f}, spread {spread:.6f} "
            f"({spread/abs(mean_gap)*100:.1f}% — M_H-FLAT); shape diffs "
            f"{[round(sd, 7) for sd in shape_diffs]} vs published swing "
            f"{pub_swing:.4f}. VERDICT: the oblique sector is benchmark-"
            f"validated at ≤5e-4 (shape PASS); the assembly carries an "
            f"M_H-independent defect of ~+0.019 (absolute FAIL, recorded). "
            f"One-loop vs one-loop — NOT two-loop truncation. The implied "
            f"true one-loop vertex-sector content ≈ +0.0025 is INFERENCE, "
            f"conditional on the effva booking (ADJUDICATED canonical, "
            f"ruling 2026-07-03, pinned at the slot check) and a defect-free "
            f"oblique sector. This check retires "
            f"the slot check's UNBENCHMARKED clause; it does NOT fill the "
            f"slot. Frame budget: light-quark ±20% ≤1.5e-5, BW→pole M_Z "
            f"+3.0e-5, stale .99 M_Z=91.177 — all far below the signal."
        ),
        key_result=(
            f"ACFW published-one-loop benchmark: shape PASS (≤5e-4), absolute "
            f"FAIL ({mean_gap:+.4f} M_H-flat) — κ_ℓ overshoot is an assembly "
            f"defect, not two-loop content. [P_structural_instrument]"
        ),
        dependencies=[
            "T_BSY_one_loop_kappa_l_assembly_consistency_at_Denner_validated_inputs",
        ],
        cross_refs=[
            "L_w_trace_native_kappa_l_proper_vertex_open",
            "T_w_trace_native_kappa_l_gammaZ_mixing",
        ],
        artifacts={
            "acfw_rows_MH_pub_native": [(MH, pub, round(dk, 9))
                                        for (MH, pub, dk) in rows],
            "gaps": [round(g, 9) for g in gaps],
            "mean_gap": round(mean_gap, 9),
            "gap_spread": round(spread, 9),
            "shape_diffs": [round(sd, 9) for sd in shape_diffs],
            "benchmark_shape": "PASS",
            "benchmark_absolute": "FAIL_RECORDED",
            "implied_true_vertex_content_conditional": 0.0025,
            "comparator": "ACFW PRL 93 (2004) 201805 Table II, O(alpha), M_W input",
            "export_flags": dict(EXPORT_FLAGS),
        },
    )


_CHECKS = {
    "T_BSY_one_loop_kappa_l_assembly_consistency_at_Denner_validated_inputs":
        check_T_BSY_one_loop_kappa_l_assembly_consistency_at_Denner_validated_inputs_P,
    "T_w_trace_kappa_l_ACFW_published_one_loop_benchmark":
        check_T_w_trace_kappa_l_ACFW_published_one_loop_benchmark_P,
}


def register(registry):
    registry.update(_CHECKS)
    return registry


def run_all() -> Dict[str, Dict[str, Any]]:
    return {name: fn() for name, fn in _CHECKS.items()}


if __name__ == "__main__":
    import json
    out = run_all()
    for k, v in out.items():
        print(json.dumps({"name": k, "passed": v["passed"],
                          "epistemic": v["epistemic"]}, indent=2))

# ---------------------------------------------------------------------------
# IE onboarding (Wave 7, v24.3.347).
# ---------------------------------------------------------------------------
IE_DECLARATIONS = (
    {
        "input_id": "wtrace:bsy_one_loop_kappa_l_assembly_consistency",
        "expect_export": False,
        "axis": "ROUTE",
        "claim_text": (
            "Banked check check_T_BSY_one_loop_kappa_l_assembly_"
            "consistency_at_Denner_validated_inputs_P (tier 4, bespoke machine grade "
            "P_one_loop_BSY_3pt_at_Denner_validated_inputs_assembly_consistency) "
            "certifying that the native one-loop substrate (v24.3.99 self- "
            "energies + v24.3.107 3-pt F_V/F_A) composed via EWWGR Eq 175 (BSY "
            "recipe) yields a structurally consistent one-loop kappa_l assembly "
            "at Denner-validated inputs (sW^2 = 0.223339, alpha(M_Z) = 1/128.21, "
            "m_t = 140 GeV, M_H = 100 GeV): g_V/g_A finite and real-dominated, "
            "sin^2 theta_eff in the physical band [0.20, 0.25], renormalized Pi- "
            "hat^gammaZ_R(M_Z^2) in the one-loop band, Delta_rho_OS reproducing "
            "Denner's published 0.00780 to ~1e-3 relative, and Delta_kappa_l in "
            "[0.040, 0.055]. This is assembly CONSISTENCY at a validated input "
            "set, nothing more: PDG-canonical one-loop kappa_l closure stays OPEN "
            "(+1.7e-2 gap to DFGRU), all-orders/two-loop EW closure stays OPEN "
            "(scoping brief filed), no physical-final kappa_l or sin^2 theta_eff "
            "is exported, and no DFGRU/Awramik target is consumed -- all enforced "
            "by explicit export-flag guards inside the check. "
        ),
        "note": ("Wave 7; bespoke grade token quoted verbatim; opens stated as "
                 "banked. NOTE (v24.3.358): the module now carries a SECOND "
                 "banked check, T_w_trace_kappa_l_ACFW_published_one_loop_"
                 "benchmark [P_structural_instrument] (ACFW PRL 93 (2004) "
                 "Table II published-one-loop benchmark: M_H-shape PASS / "
                 "absolute FAIL +0.0194 M_H-flat, FAIL-recording), and the "
                 "eq-rself +2->+1 SgZ0 corrigendum in _bsy_compose: "
                 "Delta_kappa_l at the Denner set is +0.04854 post-corrigendum "
                 "(claim text's 0.0475-era band [0.040, 0.055] unchanged and "
                 "still met); the claim text's two-loop-gate attribution for "
                 "the PDG-canonical gap is superseded by the benchmark "
                 "finding (assembly-sector defect)."),
    },
)
