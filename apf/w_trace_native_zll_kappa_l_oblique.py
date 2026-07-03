"""W_TRACE APF-native oblique leptonic effective-angle form factor kappa_l.

Gate A rung 2a (OS-W-to-[P] gate map, 2026-05-25). Rung 1
(w_trace_native_zll_vertex_form_factors) banked the generic vertex form-factor
substrate. This rung assembles the OBLIQUE part of the leptonic effective-angle
form factor kappa_l natively, using the effective-coupling recipe of
Dubovyk-Freitas-Gluza-Riemann-Usovitsch (arXiv:1906.08815, eqs 1.1-1.3) and the
banked native gauge-boson self-energies.

The recipe (1906.08815 eq 1.1/1.2)
---------------------------------
    v_f(s) = v^Z_f(s) - v^gamma_f(s) * Sigma^gZ(s)/(s + Sigma^gg(s)) ,
    a_f(s) = a^Z_f(s) - a^gamma_f(s) * Sigma^gZ(s)/(s + Sigma^gg(s)) ,
with tree couplings v^Z_f(0)=e(I3-2Q s^2)/(2 s c), v^gamma_f(0)=eQ,
a^Z_f(0)=e I3/(2 s c), a^gamma_f(0)=0; and sin^2 theta_eff^f =
(1/4|Q_f|)(1 - Re v_f/a_f). For charged leptons (Q=-1, I3=-1/2) this gives,
keeping tree v^Z/a^Z + the oblique (self-energy) corrections,

    sin^2 theta_eff = s^2 + s_W c_W Re[ Sigma^gZ(M_Z^2)/(M_Z^2 + Sigma^gg(M_Z^2)) ]
                          + (custodial Delta rho scheme shift) + (proper vertex) ,

so the oblique form factor splits as

    Delta kappa_l^obl = (c_W^2/s_W^2) Delta rho   +   (c_W/s_W) Re[ X ] ,
    X = Sigma^gZ(M_Z^2)/(M_Z^2 + Sigma^gg(M_Z^2)) .

The first term is the custodial piece (banked [P] at v24.3.67, 59% of the target
Delta kappa_l). The second is the gamma-Z-mixing piece, evaluated here natively
from the banked total (fermionic+bosonic) gamma-Z self-energy
w_trace_native_delta_r_mw_assembly.Sig_AZ at the Z pole. Its SIGN is sourced
from 1906.08815 eq 1.1/1.2 (not reconstructed from memory).

Result (DFGRU booking — adjudicated NON-CANONICAL 2026-07-03; pinned record)
------
gamma-Z Dkappa(DFGRU recipe) = (c/s) Sigma^gZ(M_Z^2)/M_Z^2 = +0.001483 (the
small Sigma^gg ~ Delta alpha denominator correction is a known ~6% higher-
order effect dropped here). With the banked custodial 0.021721 the DFGRU-
booking assembly is 0.023204 = 63.0% of the banked target 0.036808. The
CANONICAL (effva-booking) assembly is 0.019218 = 52.2%, canonical slot
budget +0.017590 — see the .358 block below.

What this module does (and does NOT) claim
-------------------------------------------
It evaluates the OBLIQUE kappa_l (custodial + gamma-Z mixing) natively, in the
DFGRU booking. [Pre-.358 this paragraph billed the gamma-Z piece as "the first
natively-computed slice of the non-oblique remainder" — that ladder-role
reading is RETIRED by the 2026-07-03 booking adjudication (effva canonical);
see the .358 block below. The DFGRU-booking numbers are retained as the
pinned record of the collision's second leg.]
It does NOT close kappa_l: the proper Zll vertex form factors Lambda_V/Lambda_A
(the genuine non-oblique ~37% remainder: proper vertex + light-fermion + the
data-bound Delta alpha) are NOT computed here -- they need the explicit one-loop
Zll vertex (LEP Yellow Report 'Precision Calculations for the Z Resonance',
CERN 95-03 = arXiv:hep-ph/9709229; or Akhundov-Bardin-Riemann NPB276(1986)1),
the next rung. No sin^2 theta_eff value is exported; DIZET stays the publishable
OS-W closure.

Honest caveat: Sig_AZ uses the .99 module's Denner input masses (m_t=140); the
gamma-Z self-energy at M_Z^2 is light-fermion-dominated (top below threshold,
entering only via the spacelike B0), so this piece is m_t-insensitive at the
quoted precision.

v24.3.358 update (2026-07-03) — the slot RE-PRICED + the booking collision
ADJUDICATED (Zll proper-vertex walk 2026-07-02, walker + hostile audit
SOUND-WITH-CORRECTIONS 0.90; principal ruling 2026-07-03: the EWWGR effva
booking is CANONICAL for the effective-angle ladder):

- The 0.013604 "proper vertex" slot is a MIXED-ORDER, MIXED-BOOKKEEPING
  RESIDUAL, not a one-loop vertex form-factor value: all-orders measured
  import (0.036808) minus custodial one-loop (0.021721) minus the naive
  gamma-Z one-loop rung (+0.001483) — two one-loop rungs in two DIFFERENT
  gamma-Z bookkeepings.
- The slot is now BENCHMARKED (ACFW published-one-loop harness, banked at
  the BSY validator .358): M_H-shape PASS <=1.7e-4 / absolute FAIL +0.0194
  M_H-flat — the overshoot is an assembly defect, not two-loop truncation.
- The implied TRUE one-loop vertex-sector content is ~ +0.0025 — an order
  of magnitude below the slot label — CONDITIONAL on the effva booking and
  a defect-free oblique sector (inference, not proof).
- GAMMA-Z BOOKING COLLISION, ADJUDICATED: this module's rung books
  +(c/s)·X = +0.001483 (DFGRU eq 1.1/1.2 recipe) while the EWWGR eq-effva
  composition books -(c/s)·[X + SgZ0] = -0.002503 on the SAME banked
  Sig_AZ object. At most one booking can feed the same ladder. RULED
  (principal, 2026-07-03, on the walk's evidence: custodial reproduction
  from inside Pi-hat^gZ + the ACFW M_H-shape match): the EFFVA booking is
  CANONICAL. This module's DFGRU-recipe rung is NON-CANONICAL as a ladder
  contribution — its surviving claim is the native arithmetic + sign
  provenance of the DFGRU-recipe evaluation, retained as the pinned
  record of the collision's second leg. The canonical gamma-Z mixing
  content is -0.002503; the canonical slot budget is +0.017590 (of which
  ~+0.0025 is the implied vertex content). An adjudication is a ruling,
  not a derivation — recorded in the Decisions List; both bookings stay
  machine-pinned in the slot check below (either number drifting fails
  the bank and re-opens the ruling).

Status
------
- Export_native_kappa_l_oblique_assembled        = 1   (NEW here)
- Export_native_kappa_l_gammaZ_mixing_evaluated   = 1   (NEW here)
- Export_native_kappa_l_proper_vertex_evaluated   = 0   (OPEN, next rung)
- Export_native_kappa_l_evaluated                 = 0   (OPEN, Gate A)
"""
from __future__ import annotations

import math
from typing import Any, Dict

from apf.apf_utils import check, _result
from apf.w_trace_native_delta_r_mw_assembly import Sig_AZ, MZ2
from apf.sin2theta_eff_kappa_l_decomposition import _decomposition
from apf.sin2theta_eff_bsy_real_adapter import SIN2THETA_CODOMAINS

# Banked on-shell weak-angle codomain (same value the kappa_l decomposition uses).
_S2_OS = SIN2THETA_CODOMAINS["on_shell_mass_ratio_1_minus_MW2_MZ2"]  # 0.223339
_S = math.sqrt(_S2_OS)
_C = math.sqrt(1.0 - _S2_OS)


def kappa_l_gammaZ() -> float:
    """gamma-Z-mixing contribution to Delta kappa_l (leading), native + sign-sourced.

    Dkappa_gammaZ = (c_W/s_W) Re[ Sigma^gZ(M_Z^2)/M_Z^2 ]  (eq 1.1/1.2 sign).
    Sigma^gZ is the banked native total (fermionic+bosonic) gamma-Z self-energy.
    """
    X = Sig_AZ(MZ2, _S, _C, MZ2) / MZ2
    return (_C / _S) * X


def oblique_decomposition() -> Dict[str, float]:
    d = _decomposition()
    cust = d["lead_custodial_tot"]          # banked 0.021721 [P]
    target = d["delta_kappa_l_target"]      # banked 0.036808
    gz = kappa_l_gammaZ()
    obl = cust + gz
    # v24.3.358: the CANONICAL (adjudicated 2026-07-03) effva booking of the
    # same Sig_AZ object: gamma-Z mixing content = -(c/s)[X + SgZ0].
    X = Sig_AZ(MZ2, _S, _C, MZ2) / MZ2
    SgZ0 = Sig_AZ(0.0, _S, _C, MZ2) / MZ2
    gz_effva = -(_C / _S) * (X + SgZ0)
    obl_effva = cust + gz_effva
    return {
        "custodial_banked": cust,
        "gammaZ_native": gz,                       # DFGRU booking (non-canonical)
        "oblique_total": obl,                      # DFGRU-booking assembly
        "target": target,
        "remainder": target - obl,                 # legacy carve (DFGRU booking)
        "oblique_fraction": obl / target,
        "remainder_fraction": (target - obl) / target,
        "sig_gZ_over_MZ2": X,
        "sig_gZ0_over_MZ2": SgZ0,
        "gammaZ_effva_canonical": gz_effva,        # CANONICAL booking (ruled)
        "oblique_total_effva": obl_effva,
        "remainder_effva_canonical": target - obl_effva,
    }


EXPORT_FLAGS: Dict[str, int] = {
    "Export_native_kappa_l_oblique_assembled": 1,
    "Export_native_kappa_l_gammaZ_mixing_evaluated": 1,
    "Export_native_kappa_l_proper_vertex_evaluated": 0,
    "Export_native_kappa_l_evaluated": 0,
}

# remainder budget from the banked decomposition (genuine non-custodial residual)
_REMAINDER_BUDGET = 0.011815


def check_T_w_trace_native_kappa_l_gammaZ_mixing_P() -> Dict[str, Any]:
    """T: the DFGRU-recipe gamma-Z-mixing evaluation, native + sign-sourced
    [P_structural]; BOOKING ADJUDICATED NON-CANONICAL (2026-07-03).

    Dkappa_gammaZ(DFGRU recipe) = (c/s) Sigma^gZ(M_Z^2)/M_Z^2, with Sigma^gZ
    the banked native total gamma-Z self-energy and the sign from 1906.08815
    eq 1.1/1.2. Anchored by: positive (sourced sign), magnitude within the
    banked genuine-non-custodial remainder budget, native (no fitted target).

    BOOKING ADJUDICATED (v24.3.358, principal ruling 2026-07-03): the EWWGR
    eq-effva booking of this same Sig_AZ object, -(c/s)[X + SgZ0] = -0.002503,
    is CANONICAL for the effective-angle ladder; this rung's DFGRU-recipe
    booking is NON-CANONICAL — it does NOT feed the ladder. The pre-.358
    claim "the first natively-computed slice of the non-oblique remainder"
    is RETIRED. What this check retains: the native arithmetic + sign
    provenance of the DFGRU-recipe evaluation, pinned as the record of the
    collision's second leg (drift here re-opens the adjudication). Ruling
    recorded in the Decisions List; collision machine-pinned at
    check_L_w_trace_native_kappa_l_proper_vertex_open_C.
    """
    d = oblique_decomposition()
    gz = d["gammaZ_native"]
    check(gz > 0, f"gamma-Z Dkappa must be positive (sourced sign), got {gz}")
    check(abs(gz - 0.001483) < 5e-5, f"gamma-Z Dkappa {gz} != native 0.001483")
    # magnitude bound only (vs the legacy DFGRU-carve budget); NOT a
    # ladder-role claim — that claim was retired at the .358 adjudication.
    check(gz < _REMAINDER_BUDGET,
          f"gamma-Z piece {gz} must fit within the remainder budget {_REMAINDER_BUDGET}")
    return _result(
        name="T_w_trace_native_kappa_l_gammaZ_mixing: "
             "DFGRU-recipe gamma-Z-mixing evaluation [P_structural]; "
             "booking ADJUDICATED NON-CANONICAL (2026-07-03)",
        tier=4, epistemic="P_structural_partial",
        summary=(
            f"The DFGRU-recipe gamma-Z-mixing evaluation, Dkappa_gammaZ = "
            f"(c/s) Re[Sigma^gZ(M_Z^2)/M_Z^2] = {gz:.6f}, computed natively from "
            f"the banked total (fermionic+bosonic) gamma-Z self-energy "
            f"(w_trace_native_delta_r_mw_assembly.Sig_AZ at the Z pole), sign "
            f"sourced from arXiv:1906.08815 eq 1.1/1.2, not reconstructed. "
            f"BOOKING ADJUDICATED (v24.3.358, principal ruling 2026-07-03): the "
            f"EWWGR eq-effva booking of the same Sig_AZ object, -(c/s)[X + SgZ0] "
            f"= {d['gammaZ_effva_canonical']:+.6f}, is CANONICAL for the "
            f"effective-angle ladder; THIS rung's booking is NON-CANONICAL and "
            f"does not feed the ladder. The pre-.358 ladder-role claim ('first "
            f"natively-computed slice of the non-oblique remainder') is RETIRED. "
            f"Surviving claim: the native arithmetic + sign provenance of the "
            f"DFGRU-recipe evaluation, pinned as the collision's second leg "
            f"(drift re-opens the adjudication). Ruled on the walk's evidence "
            f"(custodial reproduction from inside Pi-hat^gZ + the ACFW M_H-shape "
            f"benchmark); an adjudication is a ruling, not a derivation."
        ),
        key_result=(
            f"DFGRU-recipe gamma-Z evaluation = {gz:.6f} (sign-sourced); booking "
            f"adjudicated NON-CANONICAL (effva canonical, ruling 2026-07-03). "
            f"[P_structural]"
        ),
        dependencies=["T_sin2theta_eff_kappa_l_leading_custodial_internal",
                      "T_w_trace_native_delta_r_mu_independent"],
        cross_refs=["check_T_w_trace_native_vertex_ff_subgate_partial_P"],
        artifacts={k: round(v, 9) for k, v in d.items()},
    )


def check_T_w_trace_native_kappa_l_custodial_consistent_P() -> Dict[str, Any]:
    """T: custodial leading term ties to the banked kappa_l decomposition [P]."""
    d = oblique_decomposition()
    check(abs(d["custodial_banked"] - 0.021721186) < 1e-7,
          f"custodial {d['custodial_banked']} != banked 0.021721186")
    check(abs(d["target"] - 0.036807775) < 1e-7,
          f"target {d['target']} != banked 0.036807775")
    return _result(
        name="T_w_trace_native_kappa_l_custodial_consistent: "
             "custodial leading term ties to banked kappa_l decomposition [P]",
        tier=4, epistemic="P",
        summary=(
            f"The oblique assembly reuses the banked custodial leading term "
            f"Xi_rho*Delta rho = {d['custodial_banked']:.6f} [P, v24.3.67] and the "
            f"banked target Delta kappa_l = {d['target']:.6f}, so the oblique kappa_l "
            f"is built on the validated decomposition, not a new fit."
        ),
        key_result="custodial term consistent with banked decomposition. [P]",
        dependencies=["T_sin2theta_eff_kappa_l_leading_custodial_internal"],
        artifacts={"custodial_banked": round(d["custodial_banked"], 9),
                   "target": round(d["target"], 9)},
    )


def check_T_w_trace_native_kappa_l_oblique_assembly_P() -> Dict[str, Any]:
    """T: the oblique kappa_l assembly, DUAL-BOOKING record [P_structural].

    Pre-.358 this check billed "custodial + gamma-Z = 63% of target" in the
    DFGRU booking. The booking adjudication (2026-07-03: effva canonical)
    re-scopes it: the CANONICAL oblique assembly is custodial + effva
    gamma-Z = +0.019218 = 52.2% of target; the DFGRU-booking assembly
    (+0.023204 = 63.0%) is retained as the pinned record of the
    non-canonical leg. Both bookings machine-pinned; drift in either
    re-opens the adjudication.
    """
    d = oblique_decomposition()
    # DFGRU-booking leg (non-canonical, pinned record)
    check(abs(d["oblique_total"] - 0.023204) < 1e-4,
          f"DFGRU-booking oblique total {d['oblique_total']} != 0.023204")
    check(d["oblique_total"] < d["target"],
          "DFGRU-booking oblique must not overshoot the target")
    check(0.60 < d["oblique_fraction"] < 0.66,
          f"DFGRU-booking fraction {d['oblique_fraction']:.3f} not ~63%")
    # CANONICAL (effva) leg — adjudicated 2026-07-03
    check(abs(d["oblique_total_effva"] - 0.019218) < 1e-4,
          f"canonical oblique total {d['oblique_total_effva']} != 0.019218")
    check(0.0 < d["oblique_total_effva"] < d["custodial_banked"],
          "canonical oblique must sit below custodial-only (effva gamma-Z "
          "is negative) and stay positive")
    check(abs(d["remainder_effva_canonical"] - 0.017590) < 5e-5,
          f"canonical remainder {d['remainder_effva_canonical']} != 0.017590")
    return _result(
        name="T_w_trace_native_kappa_l_oblique_assembly: "
             "oblique kappa_l dual-booking record — canonical (effva) 52.2% / "
             "DFGRU 63.0% pinned [P_structural]",
        tier=4, epistemic="P_structural_partial",
        summary=(
            f"Oblique Delta kappa_l in BOTH bookings of the same banked Sig_AZ "
            f"object (booking adjudicated 2026-07-03: effva CANONICAL). "
            f"CANONICAL: custodial (banked {d['custodial_banked']:.6f}) + effva "
            f"gamma-Z ({d['gammaZ_effva_canonical']:+.6f}) = "
            f"{d['oblique_total_effva']:.6f} = "
            f"{d['oblique_total_effva']/d['target']*100:.1f}% of the banked "
            f"target {d['target']:.6f}; canonical remainder "
            f"{d['remainder_effva_canonical']:.6f} (Delta-alpha/light-fermion "
            f"legs + ~+0.0025 implied vertex content — see the slot check). "
            f"DFGRU-BOOKING (non-canonical, pinned record): custodial + "
            f"{d['gammaZ_native']:+.6f} = {d['oblique_total']:.6f} = "
            f"{d['oblique_fraction']*100:.1f}%; its legacy remainder "
            f"{d['remainder']:.6f} was the pre-.358 slot label. Neither booking "
            f"overshoots the target; both are machine-pinned."
        ),
        key_result=(
            f"oblique kappa_l: canonical (effva) {d['oblique_total_effva']:.6f} "
            f"(52.2%); DFGRU record {d['oblique_total']:.6f} (63.0%) pinned. "
            f"[P_structural]"
        ),
        dependencies=["T_w_trace_native_kappa_l_gammaZ_mixing",
                      "T_w_trace_native_kappa_l_custodial_consistent"],
        artifacts={k: round(v, 9) for k, v in d.items()},
    )


def check_L_w_trace_native_kappa_l_proper_vertex_open_C() -> Dict[str, Any]:
    """L: the kappa_l slot, RE-PRICED (v24.3.358) — a mixed-order,
    mixed-bookkeeping residual; booking ADJUDICATED effva-canonical
    (2026-07-03); canonical slot budget +0.017590 of which ~+0.0025 is the
    implied vertex content; still the OPEN gate [C].

    Pre-.358 this check billed the 0.013604 remainder as "the proper Zll
    vertex ... UNBENCHMARKED". The 2026-07-02 walk (hostile audit
    SOUND-WITH-CORRECTIONS 0.90) re-priced it: see the module docstring's
    .358 block. The [C] stays; what changed is the slot's honest label,
    the benchmark status (now benchmarked — FAIL recorded at the ACFW
    harness), the booking adjudication (effva canonical, principal ruling
    2026-07-03, recorded in the Decisions List), and the machine-pinned
    dual-booking record below.
    """
    d = oblique_decomposition()
    check(d["remainder"] > 1e-3, "remainder must be a genuine open gap")
    check(EXPORT_FLAGS["Export_native_kappa_l_proper_vertex_evaluated"] == 0,
          "proper vertex must remain UNCLAIMED (flag 0)")
    check(EXPORT_FLAGS["Export_native_kappa_l_evaluated"] == 0,
          "native kappa_l must remain OPEN (Gate A not closed)")

    # --- slot contract, machine-pinned (v24.3.358) ---
    # slot = all-orders import - custodial one-loop - naive gammaZ one-loop
    check(abs(d["remainder"] - 0.013603943) < 5e-5,
          f"slot residual drifted from the pinned contract: {d['remainder']}")
    check(abs(d["target"] - 0.036807775) < 1e-7, "all-orders import drifted")
    check(abs(d["custodial_banked"] - 0.021721186) < 1e-7, "custodial rung drifted")

    # --- the gamma-Z booking collision, ADJUDICATED and machine-pinned ---
    # (principal ruling 2026-07-03: the EWWGR effva booking is CANONICAL)
    X = d["sig_gZ_over_MZ2"]
    SgZ0 = d["sig_gZ0_over_MZ2"]
    booking_oblique = (_C / _S) * X                    # DFGRU rung (non-canonical)
    booking_effva = -(_C / _S) * (X + SgZ0)            # EWWGR eq effva (CANONICAL)
    check(abs(booking_oblique - 0.001483) < 5e-5,
          f"DFGRU booking drifted: {booking_oblique}")
    check(abs(booking_effva - (-0.002503)) < 5e-5,
          f"canonical effva booking drifted: {booking_effva}")
    check(booking_oblique > 0 > booking_effva,
          "the collision's sign opposition must hold; if this fails, "
          "one rung changed — the adjudication re-opens")
    # canonical slot budget under the ruled booking
    check(abs(d["remainder_effva_canonical"] - 0.017590) < 5e-5,
          f"canonical slot budget drifted: {d['remainder_effva_canonical']}")

    return _result(
        name="L_w_trace_native_kappa_l_proper_vertex_open: "
             "the kappa_l slot re-priced — mixed-order residual, ~+0.0025 "
             "conditional vertex content, booking ADJUDICATED effva-canonical [C]",
        tier=4, epistemic="C",
        summary=(
            f"SLOT CONTRACT (re-priced v24.3.358, walk 2026-07-02): the "
            f"{d['remainder']:.6f} residual is NOT a one-loop vertex form-factor "
            f"value. It is an all-orders measured import ({d['target']:.6f}, the "
            f"LATEST-51 adapter) minus two one-loop rungs computed in two "
            f"DIFFERENT gamma-Z bookkeepings (custodial "
            f"{d['custodial_banked']:.6f} + naive gamma-Z {booking_oblique:+.6f}) "
            f"-- a mixed-order, mixed-bookkeeping residual. "
            f"BENCHMARK STATUS: now BENCHMARKED at the ACFW published-one-loop "
            f"harness (T_w_trace_kappa_l_ACFW_published_one_loop_benchmark, "
            f".358): M_H-shape PASS <=1.7e-4 / absolute FAIL +0.0194 M_H-flat "
            f"-- the overshoot is an ASSEMBLY DEFECT (the eq-rself +2->+1 "
            f"corrigendum landed same leg; worth +0.00104), not two-loop "
            f"truncation. IMPLIED TRUE one-loop vertex-sector content ~ "
            f"+0.0025 -- an order of magnitude below the slot label -- "
            f"conditional on the RULED booking (see below) and a defect-free "
            f"oblique sector (inference from M_H-flatness + literature scale, "
            f"not proof). GAMMA-Z BOOKING COLLISION, ADJUDICATED (principal "
            f"ruling 2026-07-03): this module's rung books "
            f"{booking_oblique:+.6f} = +(c/s)X (DFGRU eq 1.1/1.2) while the "
            f"EWWGR eq-effva composition books {booking_effva:+.6f} = "
            f"-(c/s)[X + SgZ0] on the SAME banked Sig_AZ object; at most one "
            f"can feed the same ladder; the slot budget was carved in the "
            f"former while the assembly-grade filler runs in the latter. "
            f"RULED: the EFFVA booking is CANONICAL (on the walk's evidence: "
            f"custodial reproduction from inside Pi-hat^gZ + the ACFW "
            f"M_H-shape match; an adjudication is a ruling, not a derivation; "
            f"Decisions List of record). CANONICAL SLOT BUDGET: "
            f"{d['remainder_effva_canonical']:+.6f} = target - custodial - "
            f"effva gamma-Z, of which ~+0.0025 is the implied vertex content "
            f"and the rest is the named-open Delta-alpha/light-fermion legs. "
            f"The legacy 0.013604 carve is retained as the DFGRU-booking "
            f"record; both bookings machine-pinned (drift re-opens the "
            f"ruling). WHAT CLOSING NOW MEANS: fix-the-assembly (done .358) "
            f"-> booking adjudicated (done, ruling 2026-07-03) -> close the "
            f"~0.0025 slot with the native vertex "
            f"already transcribed at 8e-16 anchor fidelity "
            f"(w_trace_pv_ewwgr_bare_proper_vertex F_V/F_A) under the ACFW "
            f"benchmark as the gate. The Delta-alpha / light-fermion legs "
            f"stay named-open ([P+tool]-class content, no delta_alpha_* "
            f"claim). Native kappa_l stays OPEN; DIZET stays publishable; "
            f"no 3/13-is-physical claim; v15.1 untouched."
        ),
        key_result=(
            f"slot re-priced: mixed-order residual; booking ADJUDICATED effva-"
            f"canonical (ruling 2026-07-03); canonical budget "
            f"{d['remainder_effva_canonical']:+.6f} of which ~+0.0025 implied "
            f"vertex content; benchmarked (ACFW shape PASS / absolute FAIL); "
            f"dual-booking pinned ({booking_oblique:+.6f} vs "
            f"{booking_effva:+.6f}). [C]"
        ),
        dependencies=["T_w_trace_native_kappa_l_oblique_assembly"],
        cross_refs=["T_w_trace_kappa_l_ACFW_published_one_loop_benchmark"],
        artifacts={"remainder": round(d["remainder"], 9),
                   "slot_is_mixed_order_mixed_bookkeeping_residual": True,
                   "vertex_slot_benchmarked": True,
                   "benchmark_shape": "PASS",
                   "benchmark_absolute": "FAIL_RECORDED",
                   "implied_true_vertex_content_conditional": 0.0025,
                   "booking_collision": "ADJUDICATED effva-canonical (ruling 2026-07-03)",
                   "booking_dfgru_cs_X_noncanonical": round(booking_oblique, 9),
                   "booking_effva_cs_X_plus_SgZ0_canonical": round(booking_effva, 9),
                   "canonical_slot_budget_effva": round(d["remainder_effva_canonical"], 9),
                   "export_flags": dict(EXPORT_FLAGS)},
    )


_CHECKS = {
    "T_w_trace_native_kappa_l_gammaZ_mixing":
        check_T_w_trace_native_kappa_l_gammaZ_mixing_P,
    "T_w_trace_native_kappa_l_custodial_consistent":
        check_T_w_trace_native_kappa_l_custodial_consistent_P,
    "T_w_trace_native_kappa_l_oblique_assembly":
        check_T_w_trace_native_kappa_l_oblique_assembly_P,
    "L_w_trace_native_kappa_l_proper_vertex_open":
        check_L_w_trace_native_kappa_l_proper_vertex_open_C,
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

# ---------------------------------------------------------------------------
# IE onboarding (Wave 7, v24.3.347).
# ---------------------------------------------------------------------------
IE_DECLARATIONS = (
    {
        "input_id": "wtrace:zll_kappa_l_oblique",
        "expect_export": False,
        "axis": "ROUTE",
        "claim_text": (
            "Four banked checks assembling the OBLIQUE part of the leptonic "
            "effective-angle form factor kappa_l natively per the DFGRU recipe "
            "(arXiv:1906.08815 eqs 1.1-1.2). "
            "check_T_w_trace_native_kappa_l_gammaZ_mixing_P (tier 4, "
            "epistemic=P_structural_partial) certifies the gamma-Z-mixing piece "
            "(c/s) x Sigma^gZ(M_Z^2)/M_Z^2 = +0.001483 evaluated natively from "
            "the banked Sig_AZ self-energy, sign sourced from the reference, with "
            "the ~6% Sigma^gg denominator correction named as a dropped higher- "
            "order effect. check_T_w_trace_native_kappa_l_custodial_consistent_P "
            "(tier 4, epistemic=P) certifies consistency with the banked "
            "custodial term 0.021721. "
            "check_T_w_trace_native_kappa_l_oblique_assembly_P (tier 4, "
            "epistemic=P_structural_partial) certifies the oblique assembly "
            "Delta_kappa_l^obl = 0.023204 = 63.0% of the banked target 0.036808. "
            "check_L_w_trace_native_kappa_l_proper_vertex_open_C (tier 4, "
            "epistemic=C) is the honest-OPEN record: the proper Zll vertex form "
            "factors (the genuine ~37% non-oblique remainder: proper vertex + "
            "light-fermion + data-bound Delta_alpha) are NOT computed -- the "
            "named next rung. No sin^2 theta_eff value is exported; kappa_l is "
            "NOT closed. Caveat as banked: Sig_AZ uses the v24.3.99 Denner input "
            "masses (m_t = 140), m_t-insensitive at the quoted precision. "
        ),
        "note": ("Wave 7; mixed-grade module, per-check grades listed from "
                 "machine fields. ADJUDICATION NOTE (v24.3.358, ruling "
                 "2026-07-03): the claim text above is the Wave-7 onboarding "
                 "snapshot and predates the booking adjudication (effva "
                 "canonical). Post-.358: the gammaZ_mixing rung's ladder-role "
                 "claim is RETIRED (native arithmetic + sign provenance "
                 "record only); the oblique_assembly check is a DUAL-BOOKING "
                 "record (canonical effva 0.019218 = 52.2% / DFGRU 0.023204 "
                 "= 63.0% pinned); the proper_vertex_open slot is re-priced "
                 "(mixed-order mixed-bookkeeping residual; canonical budget "
                 "+0.017590; ~+0.0025 conditional vertex content; "
                 "benchmarked at the .358 ACFW harness — shape PASS / "
                 "absolute FAIL recorded)."),
    },
)
