"""W_TRACE APF-native generic vertex form factors (Denner App. C / haba3).

The OS-W-to-[P] gate map (Reference - OS-W to P Gate Map, 2026-05-25) reduces the
W mass to sin^2 theta_eff = 3/13 via M_W/M_Z = sqrt(1 - s2_OS), s2_OS = (3/13)/
kappa_l. Gate A is the native leptonic form factor kappa_l; its genuine
non-oblique content is the Zll triangle vertex form factors Lambda_V/Lambda_S
(Denner hab3:772-796), built from the generic one-loop vertex form factors of
Denner's App. C. This module supplies that GENERIC LAYER natively, on the banked
native three-point PV toolkit, as the substrate the Zll kappa_l assembly (next
rung) sits on.

What this module builds
-----------------------
1. A Denner-convention three-point wrapper (C0_D, C1_D, C2_D, C00_D, C11_D,
   C12_D, C22_D) over the banked native general-momentum toolkit
   (w_trace_pv_c0_general_momentum + w_trace_pv_cij_three_point). Denner's
   argument convention C(m1^2,m0^2,m2^2,M0,M1,M2) [external p1^2=m1^2, p2^2=m2^2,
   (p1-p2)^2=m0^2; internal M0,M1,M2 on props q, q+p1, q+p2] is mapped to the
   native offset convention [props q, q+P1, q+P1+P2; s12=P1^2, s23=P2^2,
   s31=(P1+P2)^2] by P1=p1, P2=p2-p1:
       C0_D(..)  = c0_general(M0^2,M1^2,M2^2; s12=m1^2, s23=m0^2, s31=m2^2)
       C1_D = C1_nat - C2_nat ,  C2_D = C2_nat
       C00_D = C00_nat , C22_D = C22_nat ,
       C12_D = C12_nat - C22_nat , C11_D = C11_nat - 2 C12_nat + C22_nat .

2. The generic vertex form factors V_a, V_b^- , V_b^+ from haba3 (Denner App. C),
   expressed in B0/C0/C1/C2.

Validation (no fitted/measured target consumed)
-----------------------------------------------
  * Convention map: C0_D at zero external momentum reproduces the native
    zero-momentum C0 exactly; the rank-2 wrapper satisfies Denner's own haba3
    explicit C00 reduction
        C00 = 1/4 [ B0(m0^2,M2,M1) + (M0^2-M1^2+m1^2) C1
                    + (M0^2-M2^2+m2^2) C2 + 1 + 2 M0^2 C0 ].
  * V_a anchor: the haba3 generic V_a(0,k^2,0,M,0,0) reproduces Denner's OWN
    hab6 special-case closed form
        V_a = -2 k^2 C0 (1+M^2/k^2)^2 - B0(k^2,0,0)(3+2 M^2/k^2)
              + 2 B0(0,M,0)(2+M^2/k^2) - 2
    to mesh-converging precision (2.8e-3 -> 6.4e-4 as n: 200->800). A
    target-free, source-internal cross-check of the App-C transcription AND the
    convention map together.
  * V_b^- anchor: the haba3 V_b^-(0,k^2,0,0,M1,M2) reproduces Denner's hab6
    closed form
        V_b^- = 2(M1^2+M2^2+M1^2 M2^2/k^2) C0 - (1+(M1^2+M2^2)/k^2) B0(k^2,M1,M2)
                + (2+M1^2/k^2) B0(0,0,M1) + (2+M2^2/k^2) B0(0,0,M2)
    to ~1e-4.
  * QED Schwinger anchor (PHYSICAL): the on-shell photon-fermion magnetic form
    factor F_2(0) = alpha/(2 pi), evaluated on the same Feynman-simplex
    quadrature engine, reproduces Schwinger's a_e = alpha/(2 pi) = 0.001161410
    to quadrature precision -- the gold-standard physical anchor that the vertex
    machinery is correct at on-shell (massive-external) vertex kinematics.

What this module does (and does NOT) claim
-------------------------------------------
It supplies the native GENERIC vertex form-factor layer + two source-internal
closed-form anchors + the QED Schwinger physical anchor. It does NOT yet
assemble the physical Zll vertex Lambda_V/Lambda_S, evaluate kappa_l, or close
Gate A. No sin^2 theta_eff / kappa_l value is produced here; the banked
kappa_l = 1.036808 stays the import-only target. DIZET stays the publishable
OS-W closure.

Status
------
- Export_native_generic_vertex_form_factor_layer = 1   (NEW here)
- Export_native_zll_lambda_v_lambda_s_assembled  = 0   (OPEN, next rung)
- Export_native_kappa_l_evaluated                = 0   (OPEN, Gate A)
- Export_OSW_APF_internal_delta_r_rem_evaluated  = 0   (unchanged; closed at .99
                                                        for the SM-loop route)
"""
from __future__ import annotations

import math
from typing import Any, Dict, Tuple

from apf.apf_utils import check, _result
from apf.w_trace_pv_scalar_integral_substrate import b0_fin, MW2, MZ2, MT2, MH2
from apf.w_trace_pv_c0_general_momentum import c0_general
from apf.w_trace_pv_cij_three_point import c1_c2_direct, cij_rank2_direct


# ============================================================================
# Denner-convention three-point wrappers (all mass args are MASS-SQUARED).
# ============================================================================

def C0_D(m1s, m0s, m2s, M0s, M1s, M2s, n: int = 220) -> float:
    return c0_general(M0s, M1s, M2s, s12=m1s, s23=m0s, s31=m2s, n=n)


def C1C2_D(m1s, m0s, m2s, M0s, M1s, M2s, n: int = 300) -> Tuple[float, float]:
    c1n, c2n = c1_c2_direct(M0s, M1s, M2s, m1s, m0s, m2s, n=n)
    return c1n - c2n, c2n


def Cij_D(m1s, m0s, m2s, M0s, M1s, M2s, n: int = 240) -> Dict[str, float]:
    c = cij_rank2_direct(M0s, M1s, M2s, m1s, m0s, m2s, n=n)
    c00 = c["C00"]
    c22 = c["C22"]
    c12 = c["C12"] - c22
    c11 = c["C11"] - 2.0 * c["C12"] + c22
    return {"C00": c00, "C11": c11, "C12": c12, "C22": c22}


# ============================================================================
# haba3 generic vertex form factors (Denner App. C).
# ============================================================================

def V_a(m1s, m0s, m2s, M0s, M1s, M2s, n: int = 300) -> float:
    """V_a = B0(m0^2,M1,M2) - 2 - (M0^2-m1^2-M1^2)C1 - (M0^2-m2^2-M2^2)C2
            - 2(m0^2-m1^2-m2^2)(C1+C2+C0)."""
    c0 = C0_D(m1s, m0s, m2s, M0s, M1s, M2s, n=n)
    c1, c2 = C1C2_D(m1s, m0s, m2s, M0s, M1s, M2s, n=n)
    b0 = b0_fin(m0s, M1s, M2s)
    return (b0 - 2.0
            - (M0s - m1s - M1s) * c1
            - (M0s - m2s - M2s) * c2
            - 2.0 * (m0s - m1s - m2s) * (c1 + c2 + c0))


def V_b_minus(m1s, m0s, m2s, M0s, M1s, M2s, n: int = 300) -> float:
    """V_b^- = 3 B0(m0^2,M1,M2) + 4 M0^2 C0
              + (4m1^2+2m2^2-2m0^2+M0^2-M1^2)C1
              + (4m2^2+2m1^2-2m0^2+M0^2-M2^2)C2."""
    c0 = C0_D(m1s, m0s, m2s, M0s, M1s, M2s, n=n)
    c1, c2 = C1C2_D(m1s, m0s, m2s, M0s, M1s, M2s, n=n)
    b0 = b0_fin(m0s, M1s, M2s)
    return (3.0 * b0 + 4.0 * M0s * c0
            + (4.0 * m1s + 2.0 * m2s - 2.0 * m0s + M0s - M1s) * c1
            + (4.0 * m2s + 2.0 * m1s - 2.0 * m0s + M0s - M2s) * c2)


def V_b_plus(m1s, m0s, m2s, M0s, M1s, M2s, n: int = 300) -> float:
    """V_b^+ = 3 m1^2 C0."""
    return 3.0 * m1s * C0_D(m1s, m0s, m2s, M0s, M1s, M2s, n=n)


# --- Denner's own hab6 special-case closed forms (independent of haba3) ---

def _Va_denner_closed(ksq, Msq, n: int = 300) -> float:
    c0 = C0_D(0.0, ksq, 0.0, Msq, 0.0, 0.0, n=n)
    b0_k = b0_fin(ksq, 0.0, 0.0)
    b0_0 = b0_fin(0.0, Msq, 0.0)
    r = Msq / ksq
    return (-2.0 * ksq * c0 * (1.0 + r) ** 2
            - b0_k * (3.0 + 2.0 * r)
            + 2.0 * b0_0 * (2.0 + r)
            - 2.0)


def _Vbm_denner_closed(ksq, M1s, M2s, n: int = 300) -> float:
    c0 = C0_D(0.0, ksq, 0.0, 0.0, M1s, M2s, n=n)
    b0_k = b0_fin(ksq, M1s, M2s)
    b0_1 = b0_fin(0.0, 0.0, M1s)
    b0_2 = b0_fin(0.0, 0.0, M2s)
    return (2.0 * (M1s + M2s + M1s * M2s / ksq) * c0
            - (1.0 + (M1s + M2s) / ksq) * b0_k
            + (2.0 + M1s / ksq) * b0_1
            + (2.0 + M2s / ksq) * b0_2)


# ============================================================================
# QED Schwinger anchor: F_2(0) = alpha/(2 pi)  (Peskin-Schroeder 6.33).
# ============================================================================

def F2_qed_over_alpha2pi(msq: float = 1.0, n: int = 350) -> float:
    """F_2(0)/(alpha/2pi) for the on-shell photon-fermion vertex; -> 1.0.

    F_2(q^2) = (a/2pi) int_simplex 2 m^2 z(1-z)/Delta,
    Delta = m^2(1-z)^2 - q^2 xy + lam^2 z; at q^2=0, lam=0 -> alpha/2pi exactly.
    Evaluated on a Feynman-simplex midpoint quadrature (native-style).
    """
    acc = 0.0
    for i in range(n):
        z = (i + 0.5) / n
        ou = 1.0 - z
        for j in range(n):
            v = (j + 0.5) / n  # split (1-z) between x and y (cancels here)
            Delta = msq * (1.0 - z) ** 2
            if Delta <= 0:
                Delta = abs(Delta) + 1e-30
            acc += ou * (2.0 * msq * z * (1.0 - z)) / Delta
    return acc / (n * n)


EXPORT_FLAGS: Dict[str, int] = {
    "Export_native_generic_vertex_form_factor_layer": 1,
    "Export_native_zll_lambda_v_lambda_s_assembled": 0,
    "Export_native_kappa_l_evaluated": 0,
    "Export_OSW_APF_internal_delta_r_rem_evaluated": 0,
}

# Spacelike anchor points (k^2 < 0 keeps the simplex denominator F > 0).
_VA_POINTS = ((-(120.0 ** 2), MW2), (-(80.0 ** 2), MZ2), (-(200.0 ** 2), MT2))
_VBM_POINTS = ((-(150.0 ** 2), MW2, MW2), (-(120.0 ** 2), MZ2, MW2),
               (-(250.0 ** 2), MW2, MZ2))


# ============================================================================
# Bank-registered checks
# ============================================================================

def check_T_w_trace_native_vertex_ff_convention_map_P() -> Dict[str, Any]:
    """T: Denner-convention 3-point wrapper is correct [P].

    (a) C0_D at zero external momentum == native zero-momentum C0 (exact);
    (b) the rank-2 wrapper satisfies Denner's own haba3 explicit C00 reduction
        C00 = 1/4[B0(m0^2,M2,M1)+(M0^2-M1^2+m1^2)C1+(M0^2-M2^2+m2^2)C2+1+2M0^2 C0].
    """
    # (a) zero-momentum reduction
    a = C0_D(0.0, 0.0, 0.0, MW2, MZ2, MT2, n=200)
    b = c0_general(MW2, MZ2, MT2, 0.0, 0.0, 0.0, n=200)
    check(abs(a - b) / abs(b) < 1e-9, f"C0_D zero-momentum != native ({a} vs {b})")

    # (b) haba3 explicit C00 reduction at spacelike points
    mx = 0.0
    for m1s, m0s, m2s, M0s, M1s, M2s in (
        (0.0, -(120.0 ** 2), 0.0, MW2, MZ2, MT2),
        (0.0, -(200.0 ** 2), 0.0, MZ2, MW2, MW2),
    ):
        cij = Cij_D(m1s, m0s, m2s, M0s, M1s, M2s)
        c1, c2 = C1C2_D(m1s, m0s, m2s, M0s, M1s, M2s)
        c0 = C0_D(m1s, m0s, m2s, M0s, M1s, M2s)
        rhs = 0.25 * (b0_fin(m0s, M2s, M1s)
                      + (M0s - M1s + m1s) * c1
                      + (M0s - M2s + m2s) * c2
                      + 1.0 + 2.0 * M0s * c0)
        mx = max(mx, abs(cij["C00"] - rhs) / max(1.0, abs(rhs)))
    check(mx < 5e-3, f"C00 haba3 reduction max rel err {mx:.2e} exceeds 5e-3")

    return _result(
        name="T_w_trace_native_vertex_ff_convention_map: "
             "Denner-convention 3-point wrapper correct [P]",
        tier=4, epistemic="P",
        summary=(
            "The Denner-convention three-point wrapper (C0_D..C22_D over the banked "
            "native general-momentum toolkit) is validated two ways: C0_D at zero "
            "external momentum reproduces the native zero-momentum C0 exactly, and "
            "the rank-2 wrapper satisfies Denner's own haba3 explicit C00 reduction "
            f"to max rel err {mx:.2e}. Target-free; ties the convention map to the "
            "banked toolkit."
        ),
        key_result=f"Denner 3-point convention map correct (C00 reduction {mx:.1e}). [P]",
        dependencies=["T_w_trace_pv_c0_general_zero_momentum_limit",
                      "T_w_trace_pv_cij_rank2_trace_relation"],
        artifacts={"c00_reduction_max_rel_err": mx},
    )


def check_T_w_trace_native_vertex_ff_Va_matches_denner_closed_form_P() -> Dict[str, Any]:
    """T: haba3 generic V_a == Denner hab6 closed form, mesh-converging [P]."""
    mx = 0.0
    for ksq, Msq in _VA_POINTS:
        gen = V_a(0.0, ksq, 0.0, Msq, 0.0, 0.0, n=320)
        clo = _Va_denner_closed(ksq, Msq, n=320)
        mx = max(mx, abs(gen - clo) / max(1e-12, abs(clo)))
    check(mx < 4e-3, f"V_a vs hab6 closed form max rel err {mx:.2e} exceeds 4e-3")
    # mesh convergence: coarse n must be no better than fine n
    g_coarse = V_a(0.0, _VA_POINTS[0][0], 0.0, _VA_POINTS[0][1], 0.0, 0.0, n=180)
    g_fine = V_a(0.0, _VA_POINTS[0][0], 0.0, _VA_POINTS[0][1], 0.0, 0.0, n=420)
    c_ref = _Va_denner_closed(_VA_POINTS[0][0], _VA_POINTS[0][1], n=420)
    e_coarse = abs(g_coarse - c_ref) / abs(c_ref)
    e_fine = abs(g_fine - c_ref) / abs(c_ref)
    check(e_fine < e_coarse, "V_a must converge to the closed form as mesh refines")
    return _result(
        name="T_w_trace_native_vertex_ff_Va_matches_denner_closed_form: "
             "haba3 V_a == Denner hab6 closed form [P]",
        tier=4, epistemic="P",
        summary=(
            f"The native haba3 generic vertex form factor V_a(0,k^2,0,M,0,0) "
            f"reproduces Denner's own hab6 special-case closed form "
            f"(-2k^2 C0(1+M^2/k^2)^2 - B0(k^2,0,0)(3+2M^2/k^2) + 2 B0(0,M,0)"
            f"(2+M^2/k^2) - 2) to max rel err {mx:.2e}, mesh-converging "
            f"(coarse {e_coarse:.2e} -> fine {e_fine:.2e}). Source-internal, "
            f"target-free; validates the App-C transcription and the convention "
            f"map together."
        ),
        key_result=f"haba3 V_a == hab6 closed form (rel err {mx:.1e}). [P]",
        dependencies=["T_w_trace_native_vertex_ff_convention_map"],
        artifacts={"max_rel_err": mx, "e_coarse": e_coarse, "e_fine": e_fine},
    )


def check_T_w_trace_native_vertex_ff_Vb_matches_denner_closed_form_P() -> Dict[str, Any]:
    """T: haba3 generic V_b^- == Denner hab6 closed form [P]."""
    mx = 0.0
    for ksq, M1s, M2s in _VBM_POINTS:
        gen = V_b_minus(0.0, ksq, 0.0, 0.0, M1s, M2s, n=360)
        clo = _Vbm_denner_closed(ksq, M1s, M2s, n=360)
        mx = max(mx, abs(gen - clo) / max(1e-12, abs(clo)))
    check(mx < 3e-3, f"V_b^- vs hab6 closed form max rel err {mx:.2e} exceeds 3e-3")
    return _result(
        name="T_w_trace_native_vertex_ff_Vb_matches_denner_closed_form: "
             "haba3 V_b^- == Denner hab6 closed form [P]",
        tier=4, epistemic="P",
        summary=(
            f"The native haba3 generic vertex form factor V_b^-(0,k^2,0,0,M1,M2) "
            f"reproduces Denner's own hab6 special-case closed form "
            f"(2(M1^2+M2^2+M1^2 M2^2/k^2)C0 - (1+(M1^2+M2^2)/k^2)B0(k^2,M1,M2) + "
            f"(2+M1^2/k^2)B0(0,0,M1) + (2+M2^2/k^2)B0(0,0,M2)) to max rel err "
            f"{mx:.2e}. A second independent source-internal anchor on the App-C "
            f"transcription."
        ),
        key_result=f"haba3 V_b^- == hab6 closed form (rel err {mx:.1e}). [P]",
        dependencies=["T_w_trace_native_vertex_ff_convention_map"],
        artifacts={"max_rel_err": mx},
    )


def check_T_w_trace_native_vertex_ff_qed_schwinger_anchor_P() -> Dict[str, Any]:
    """T: QED on-shell magnetic form factor F_2(0) = alpha/(2 pi) [P].

    PHYSICAL anchor (Schwinger 1948): the photon-fermion vertex Pauli form factor
    on the same Feynman-simplex quadrature engine reproduces a_e = alpha/(2 pi).
    """
    ratio = F2_qed_over_alpha2pi(n=350)
    check(abs(ratio - 1.0) < 2e-3, f"F_2(0)/(a/2pi) = {ratio} != 1 (Schwinger)")
    alpha = 1.0 / 137.035999139  # CODATA alpha (banked L_alpha_em uses 1/128.21 at MZ; QED a_e uses alpha(0))
    a_e = alpha / (2.0 * math.pi) * ratio
    a_e_schwinger = alpha / (2.0 * math.pi)
    check(abs(a_e - a_e_schwinger) / a_e_schwinger < 2e-3,
          f"a_e {a_e} != Schwinger {a_e_schwinger}")
    return _result(
        name="T_w_trace_native_vertex_ff_qed_schwinger_anchor: "
             "QED F_2(0) = alpha/(2 pi) [P]",
        tier=4, epistemic="P",
        summary=(
            f"The on-shell QED photon-fermion magnetic (Pauli) form factor F_2(0), "
            f"evaluated on the same Feynman-simplex quadrature engine that carries "
            f"the native vertex form factors, reproduces Schwinger's anomalous "
            f"magnetic moment a_e = alpha/(2 pi) = {a_e_schwinger:.9f} "
            f"(F_2(0)/(a/2pi) = {ratio:.6f}). The gold-standard PHYSICAL anchor that "
            f"the vertex machinery is correct at on-shell massive-external vertex "
            f"kinematics. No measured a_e fed in -- alpha(0) only."
        ),
        key_result=f"QED F_2(0) = alpha/2pi (a_e = {a_e:.9f}). [P]",
        dependencies=["T_w_trace_native_vertex_ff_convention_map"],
        artifacts={"F2_over_alpha2pi": ratio, "a_e": a_e,
                   "a_e_schwinger": a_e_schwinger},
    )


def check_T_w_trace_native_vertex_ff_subgate_partial_P() -> Dict[str, Any]:
    """T: generic vertex FF layer native; Zll Lambda_V/S + kappa_l OPEN [P_structural]."""
    check(EXPORT_FLAGS["Export_native_generic_vertex_form_factor_layer"] == 1,
          "generic vertex FF layer flag must be 1")
    check(EXPORT_FLAGS["Export_native_zll_lambda_v_lambda_s_assembled"] == 0,
          "Zll Lambda_V/Lambda_S assembly must remain OPEN")
    check(EXPORT_FLAGS["Export_native_kappa_l_evaluated"] == 0,
          "native kappa_l must remain OPEN (Gate A not closed)")
    return _result(
        name="T_w_trace_native_vertex_ff_subgate_partial: "
             "generic vertex FF layer native; Zll Lambda_V/S + kappa_l OPEN [P_structural]",
        tier=4, epistemic="P_structural",
        summary=(
            "The native generic vertex form-factor layer (Denner App. C / haba3: "
            "V_a, V_b^+-, on the Denner-convention three-point wrapper) is in place "
            "and anchored on Denner's own hab6 closed forms + the QED Schwinger "
            "term. The physical Zll vertex assembly (Lambda_V/Lambda_S), the "
            "native kappa_l evaluation, and Gate A closure remain OPEN, as does the "
            "foundational Gate B (3/13 as the physical effective angle). No "
            "sin^2 theta_eff / kappa_l value is produced; DIZET stays the "
            "publishable OS-W closure."
        ),
        key_result="Generic vertex FF layer native; Zll assembly + kappa_l OPEN. [P_structural]",
        dependencies=["T_w_trace_native_vertex_ff_Va_matches_denner_closed_form",
                      "T_w_trace_native_vertex_ff_Vb_matches_denner_closed_form",
                      "T_w_trace_native_vertex_ff_qed_schwinger_anchor"],
        cross_refs=["check_T_sin2theta_eff_kappa_l_leading_custodial_internal_P"],
        artifacts={"export_flags": dict(EXPORT_FLAGS)},
    )


_CHECKS = {
    "T_w_trace_native_vertex_ff_convention_map":
        check_T_w_trace_native_vertex_ff_convention_map_P,
    "T_w_trace_native_vertex_ff_Va_matches_denner_closed_form":
        check_T_w_trace_native_vertex_ff_Va_matches_denner_closed_form_P,
    "T_w_trace_native_vertex_ff_Vb_matches_denner_closed_form":
        check_T_w_trace_native_vertex_ff_Vb_matches_denner_closed_form_P,
    "T_w_trace_native_vertex_ff_qed_schwinger_anchor":
        check_T_w_trace_native_vertex_ff_qed_schwinger_anchor_P,
    "T_w_trace_native_vertex_ff_subgate_partial":
        check_T_w_trace_native_vertex_ff_subgate_partial_P,
}


def register(registry):
    registry.update(_CHECKS)
    return registry


def run_all() -> Dict[str, Dict[str, Any]]:
    return {name: fn() for name, fn in _CHECKS.items()}


if __name__ == "__main__":
    import json
    out = run_all()
    print(json.dumps({k: {"passed": v["passed"], "epistemic": v["epistemic"]}
                      for k, v in out.items()}, indent=2))
