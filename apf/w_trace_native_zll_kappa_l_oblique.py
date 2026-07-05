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
It does NOT close kappa_l. [Pre-.358 paragraph, retained as history: the
"proper Zll vertex ... NOT computed here ... the next rung" framing below
described the pre-fill state; post-.361 the vertex COMPONENT is closed (see
the .361 block) and the surviving open content is the Delta-alpha legs.]
The proper Zll vertex form factors Lambda_V/Lambda_A
(the genuine non-oblique ~37% remainder: proper vertex + light-fermion + the
data-bound Delta alpha) were NOT computed here at banking time -- they needed
the explicit one-loop Zll vertex (LEP Yellow Report 'Precision Calculations
for the Z Resonance', CERN 95-03 = arXiv:hep-ph/9709229; or
Akhundov-Bardin-Riemann NPB276(1986)1), then the next rung. No sin^2 theta_eff value is exported; DIZET stays the publishable
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
  the BSY validator .358): the .358 instrument recorded M_H-shape PASS
  <=1.7e-4 / absolute FAIL +0.0194 M_H-flat. UPDATE v24.3.360: THE +0.019
  WAS FOUND — a sign error in the PUBLISHED CERN-95-03 closed form of
  Lambda_3 (corrigendum + three-witness certification in
  w_trace_pv_lambda_bhm_vertex); post-corrigendum the benchmark is shape
  AND absolute PASS at ~1e-4.
- The one-loop vertex-sector content on the corrected Lambda_3 is
  +0.0032 (ACFW deck, alpha(0)) — an order of magnitude below the slot
  label, now COMPUTED on a benchmark-validated assembly rather than
  inferred. Filling the slot with it is a separate landing (this check
  stays [C]; the Delta-alpha legs remain named-open).
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
  +0.0032 is the vertex content computed on the .360-corrected Lambda_3). An adjudication is a ruling,
  not a derivation — recorded in the Decisions List; both bookings stay
  machine-pinned in the slot check below (either number drifting fails
  the bank and re-opens the ruling).

v24.3.361 update (2026-07-03) — THE VERTEX-COMPONENT FILL: the vertex
component of the canonical slot is CLOSED at Dk_vertex = +0.003452700
(banked-OS deck; ACFW-deck cross-value +0.003247798), computed from the
banked F_V/F_A on the .360-corrected Lambda_3, gated LIVE by the ACFW
published-one-loop benchmark. Canonical ladder: custodial [P] + effva
gamma-Z (ruled) + vertex = +0.022670 = 61.6% of the all-orders import;
the Delta-alpha-legs residual +0.014137 stays named-open [C] (the re-cut
slot check). kappa_l itself stays OPEN. Grade riders in-token: the effva
adjudication is a RULING; the ACFW instrument is the gate.

Status
------
- Export_native_kappa_l_oblique_assembled        = 1
- Export_native_kappa_l_gammaZ_mixing_evaluated   = 1
- Export_native_kappa_l_proper_vertex_evaluated   = 1   (v24.3.361 FILL)
- Export_native_kappa_l_evaluated                 = 0   (OPEN: Delta-alpha legs)
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


def kappa_l_vertex_component(sW2: float, alpha: float):
    """The vertex component of the canonical slot (v24.3.361 fill).

    Dk_vertex := s2eff(Pi-hat = 0, F_V^Zl, F_A^Zl)/sW2 - 1 -- the F_V/F_A-only
    shift of the g_V/g_A ratio, on the v24.3.360 sign-corrected Lambda_3, per
    the banked BSY framing (real parts through the ratio; the common
    [(1 - Delta r)/(1 + Pi-hat^Z)]^{1/2} factor cancels). One-loop,
    3-pt-piece-only; external-WF legs priced <= ~1e-4 by the .360 ACFW
    residual. Returns (Dk_vertex, tree_baseline_deviation, F_V, F_A).
    """
    from apf.w_trace_pv_ewwgr_bare_proper_vertex import F_V_Z, F_A_Z
    from apf.w_trace_pv_scalar_integral_substrate import MZ2 as _PV_MZ2
    # s-point: the PV-substrate M_Z^2 (91.1876^2) -- the F's own convention
    # (the module-level MZ2 import is the .99-deck stale 91.177, used by the
    # Sig_AZ gammaZ rung; the two s-points are declared per-rung in the deck
    # ledger; the difference is ~6e-7 in Dk_vertex, inside every pin band)
    v_t, a_t = -0.5 + 2.0 * sW2, -0.5
    FV = F_V_Z("lepton", _PV_MZ2, sW2, alpha=alpha)
    FA = F_A_Z("lepton", _PV_MZ2, sW2, alpha=alpha)
    s2e = 0.25 * (1.0 - (v_t + FV.real) / (a_t + FA.real))
    base_dev = 0.25 * (1.0 - v_t / a_t) - sW2   # must vanish identically
    return s2e / sW2 - 1.0, base_dev, FV, FA


EXPORT_FLAGS: Dict[str, int] = {
    "Export_native_kappa_l_oblique_assembled": 1,
    "Export_native_kappa_l_gammaZ_mixing_evaluated": 1,
    "Export_native_kappa_l_proper_vertex_evaluated": 1,   # v24.3.361 FILL
    "Export_native_kappa_l_evaluated": 0,                 # kappa_l NOT closed
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
        cross_refs=["T_w_trace_native_vertex_ff_subgate_partial"],
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
            f"legs + the +0.0032 post-.360 vertex content — see the slot check). "
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


def check_T_w_trace_native_kappa_l_vertex_component_closed_P() -> Dict[str, Any]:
    """T: the VERTEX COMPONENT of the canonical kappa_l slot is CLOSED
    (v24.3.361 fill) [P_structural_vertex_component_effva_canonical_ruling_
    ACFW_benchmark_gated].

    The fill of record: Dk_vertex = +0.003452700 at the banked-OS deck
    (sW2 = 0.223339, alpha(M_Z) = 1/128.21), computed from the banked
    F_V^Zl/F_A^Zl on the .360 sign-corrected Lambda_3, under the ACFW
    published-one-loop benchmark as the LIVE GATE (called in-check).

    DECK LEDGER (the honest frame statement -- the ladder is NOT single-deck):
    the g_V/g_A extraction frame and every rung's PREFACTOR live at the
    banked-OS/alpha(M_Z) frame; the rungs' internal mass decks differ and are
    pinned per-rung in artifacts: the custodial rung is the banked [P] object
    deliberately frozen at its own deck (alpha(M_Z) + s2 = 0.223339 in Xi_rho;
    internal Drho at 3/13-tree M_W, m_t = 163, M_H = 124.93); the effva gammaZ
    rung reads Sig_AZ at the .99-deck masses (m_t = 140, stale M_Z = 91.177)
    with the (c/s) prefactor at OS; the vertex rung's F's carry no top and no
    Higgs at one loop (lepton Zll triangles: only M_W/M_Z/sW2/alpha enter), so
    the m_t/M_H deck sensitivity localizes ENTIRELY in the custodial rung.
    The two riders that carry the grade, named in the token: (i) the
    effva-canonical booking is a principal RULING (2026-07-03, Decisions List;
    not a derivation; dual-booking pins keep it re-openable), and (ii) the
    ACFW published-benchmark instrument [P_structural_instrument] is the gate.
    kappa_l itself stays OPEN (Delta-alpha legs; Export_native_kappa_l_
    evaluated = 0, asserted). No sin2theta_eff export; DIZET stays the
    publishable OS-W closure.
    """
    # (1)+(2) flags: component claimed, kappa_l NOT closed
    check(EXPORT_FLAGS["Export_native_kappa_l_proper_vertex_evaluated"] == 1,
          "vertex-component flag must be 1 post-fill")
    check(EXPORT_FLAGS["Export_native_kappa_l_evaluated"] == 0,
          "kappa_l must remain OPEN (Delta-alpha legs; W-export-lock fence)")

    # (3) extraction-convention self-check: tree baseline subtracts identically
    dk_OS, base_OS, FV_OS, FA_OS = kappa_l_vertex_component(_S2_OS, 1.0 / 128.21)
    _ACFW_SW2 = 1.0 - (80.426 / 91.1876) ** 2
    dk_AC, base_AC, FV_AC, FA_AC = kappa_l_vertex_component(_ACFW_SW2, 1.0 / 137.0359895)
    check(abs(base_OS) < 1e-15 and abs(base_AC) < 1e-15,
          f"tree baseline must subtract identically: {base_OS}, {base_AC}")

    # (4) dual-deck value pins (deck-dependence is part of the claim)
    check(abs(dk_OS - 0.003452700) < 5e-6,
          f"banked-OS fill drifted: {dk_OS}")
    check(abs(dk_AC - 0.003247798) < 5e-6,
          f"ACFW-deck value drifted: {dk_AC}")

    # (5) F pins + absorptive parts
    check(abs(FV_OS - complex(0.001710465, 0.001402308)) < 5e-6 and
          abs(FA_OS - complex(0.001624383, 0.001265760)) < 5e-6,
          "banked-OS F_V/F_A pins drifted")
    check(FV_OS.imag > 0 and FA_OS.imag > 0,
          "absorptive parts must be positive")

    # (6) THE GATE: the fill's license is the published benchmark, called live
    from apf.w_trace_BSY_one_loop_kappa_l_native_validator import (
        check_T_w_trace_kappa_l_ACFW_published_one_loop_benchmark_P)
    gate = check_T_w_trace_kappa_l_ACFW_published_one_loop_benchmark_P()
    check(gate["passed"],
          "the ACFW benchmark gate FAILED -- the Lambda_3 corrigendum chain "
          "is broken; the fill loses its license")

    # (7) canonical ladder sum + residual (the named-open survives numerically)
    d = oblique_decomposition()
    ladder = d["custodial_banked"] + d["gammaZ_effva_canonical"] + dk_OS
    check(abs(ladder - 0.022670427) < 5e-5, f"ladder sum drifted: {ladder}")
    check(0.60 < ladder / d["target"] < 0.63,
          f"ladder fraction {ladder/d['target']:.4f} outside (0.60, 0.63)")
    residual = d["remainder_effva_canonical"] - dk_OS
    check(abs(residual - 0.014137348) < 5e-5 and residual > 1e-3,
          f"Delta-alpha-legs residual drifted or vanished: {residual}")

    # (8) no overshoot of the carve
    check(0.0 < dk_OS < d["remainder_effva_canonical"],
          "vertex component must sit inside the canonical slot budget")

    # (9) additivity: no double-count against the gammaZ rung
    from apf.w_trace_BSY_one_loop_kappa_l_native_validator import _bsy_compose
    r = _bsy_compose(_S2_OS, 1.0 / 128.21)
    v_t, a_t = -0.5 + 2.0 * _S2_OS, -0.5
    def _s2eff_of(pigz, fv, fa):
        return 0.25 * (1 - (v_t + 2*_S*_C*(-1.0)*pigz + fv) / (a_t + fa))
    dk_P = _s2eff_of(r["Pi_gZ_R"], 0, 0) / _S2_OS - 1
    dk_F = _s2eff_of(0, r["F_V_lepton"].real, r["F_A_lepton"].real) / _S2_OS - 1
    cross = r["Delta_kappa_l"] - dk_P - dk_F
    check(abs(cross) < 1.5e-4,
          f"additivity cross-term too large (double-count?): {cross}")

    # (10) no target smuggled: the extraction consumed no measured
    # sin2theta_eff and no ACFW row (ACFW enters only through the gate call)
    check(EXPORT_FLAGS["Export_native_kappa_l_oblique_assembled"] == 1,
          "sanity: module flags intact")

    return _result(
        name=("T_w_trace_native_kappa_l_vertex_component_closed: the vertex "
              "component of the canonical kappa_l slot CLOSED at +0.003453 "
              "(banked-OS deck) under the ACFW gate; kappa_l stays OPEN "
              "(Delta-alpha legs) [P_structural_vertex_component_effva_"
              "canonical_ruling_ACFW_benchmark_gated]"),
        tier=4,
        epistemic="P_structural_vertex_component_effva_canonical_ruling_ACFW_benchmark_gated",
        summary=(
            f"THE FILL (v24.3.361): Dk_vertex = {dk_OS:+.9f} at the banked-OS "
            f"deck (sW2 = {_S2_OS}, alpha(M_Z) = 1/128.21); ACFW-deck "
            f"cross-value {dk_AC:+.9f} (the .360 headline '+0.0032'); both "
            f"pinned -- the ~6% deck spread is alpha/sW2 frame, part of the "
            f"claim. Extraction: the F_V/F_A-only shift of g_V/g_A at "
            f"Pi-hat = 0 (tree baseline subtracts to < 1e-15, asserted), on "
            f"the .360 sign-corrected Lambda_3, gated LIVE by the banked ACFW "
            f"published-one-loop benchmark (shape AND absolute PASS ~1e-4). "
            f"CANONICAL LADDER: custodial {d['custodial_banked']:+.6f} [P] + "
            f"effva gammaZ {d['gammaZ_effva_canonical']:+.6f} (ruled booking) "
            f"+ vertex {dk_OS:+.6f} (this fill) = {ladder:+.6f} = "
            f"{ladder/d['target']*100:.1f}% of the ALL-ORDERS import "
            f"{d['target']:.6f}; the remainder {residual:+.6f} is the "
            f"Delta-alpha/light-fermion legs + higher orders, named-open at "
            f"the surviving [C] -- the shortfall is data-bound content, not "
            f"missing vertex physics; never quote 'one loop complete'. DECK "
            f"LEDGER: extraction frame + all rung prefactors at banked-OS/"
            f"alpha(M_Z); custodial internal deck = the banked [P] object "
            f"(m_t = 163, 3/13-tree M_W inside Drho); gammaZ Sig_AZ at .99 "
            f"masses; the lepton vertex F's carry no top/Higgs -- m_t/M_H "
            f"sensitivity localizes in the custodial rung. Additivity "
            f"cross-term {cross:+.1e} (< 1.5e-4; the effva booking books "
            f"Sig_AZ only, the F's enter g_V/g_A separately -- no double-"
            f"count). GRADE RIDERS (in-token): the effva-canonical booking "
            f"is a principal RULING (2026-07-03, Decisions List; dual-booking "
            f"pins keep it re-openable) and the ACFW instrument is the gate. "
            f"kappa_l stays OPEN (flag asserted 0); no sin2theta_eff export; "
            f"DIZET stays the publishable OS-W closure; ladder sum != the "
            f"_bsy_compose composition 0.028229 (different custodial decks; "
            f"both pinned, never equated)."
        ),
        key_result=(
            f"vertex component CLOSED: +0.003453 (banked-OS) / +0.003248 "
            f"(ACFW), ACFW-gated; canonical ladder 61.6% of the all-orders "
            f"import; Delta-alpha legs stay [C]. Riders: effva RULING + "
            f"ACFW gate. [P_structural_vertex_component_effva_canonical_"
            f"ruling_ACFW_benchmark_gated]"
        ),
        dependencies=["T_w_trace_native_kappa_l_oblique_assembly",
                      "T_w_trace_kappa_l_ACFW_published_one_loop_benchmark",
                      "T_w_trace_pv_lambda3_sign_corrigendum_denner_anchor"],
        cross_refs=["L_w_trace_native_kappa_l_proper_vertex_open"],
        artifacts={
            "vertex_component_banked_OS_deck": round(dk_OS, 9),
            "vertex_component_ACFW_deck": round(dk_AC, 9),
            "vertex_component_3_13_diagnostic": 0.003124240,  # substrate s-point
            "canonical_ladder_sum": round(ladder, 9),
            "ladder_fraction_of_all_orders_import": round(ladder / d["target"], 6),
            "delta_alpha_legs_residual": round(residual, 9),
            "additivity_cross_term": round(cross, 9),
            "deck_ledger": {
                "extraction_frame": "banked-OS sW2=0.223339, alpha(M_Z)=1/128.21",
                "custodial_internal": "banked [P] object: m_t=163, M_H=124.93, "
                                      "3/13-tree M_W inside Drho "
                                      "(sin2theta_eff_kappa_l_decomposition)",
                "gammaZ_internal": "Sig_AZ at .99-deck masses (m_t=140, "
                                   "M_Z=91.177 stale); (c/s) prefactor at OS",
                "vertex_internal": "F_V/F_A at s = PV-substrate M_Z^2 "
                                   "(91.1876^2; NOT the .99-deck stale "
                                   "91.177 the gammaZ rung reads); no top, "
                                   "no Higgs at one loop; M_W/M_Z substrate "
                                   "masses inside the Lambda's",
            },
            "export_flags": dict(EXPORT_FLAGS),
        },
    )


def check_L_w_trace_native_kappa_l_proper_vertex_open_C() -> Dict[str, Any]:
    """L: the kappa_l named-open, RE-CUT (v24.3.361) to the Delta-alpha-legs
    residual: +0.014137 of the canonical slot budget stays OPEN [C] after
    the vertex-component fill.

    Slot history (each step banked + audited): the 0.013604 label was a
    mixed-order mixed-bookkeeping residual (.358 re-price); the ACFW
    instrument recorded the absolute FAIL (.358) that found the published
    Lambda_3 sign defect (corrigendum .360, provenance settled); the gamma-Z
    booking was ADJUDICATED effva-canonical (principal ruling 2026-07-03,
    Decisions List); the vertex component was FILLED at .361
    (+0.003452700 banked-OS, ACFW-gated — see the companion check above).
    WHAT REMAINS [C]: the Delta-alpha / light-fermion legs (+0.014137348)
    — [P+tool]-class, data-bound content (delta_alpha_* modules exist and
    are NOT claimed here) + genuine higher orders. kappa_l itself stays
    OPEN (Export_native_kappa_l_evaluated = 0, asserted). The dual-booking
    pins and the legacy DFGRU-carve pin are retained verbatim (drift
    re-opens the booking ruling).
    """
    d = oblique_decomposition()
    check(d["remainder"] > 1e-3, "legacy carve must remain a genuine gap record")
    # v24.3.361: the vertex-component flag is now 1 (the fill, certified by
    # the companion check); what THIS check keeps open is the residual.
    check(EXPORT_FLAGS["Export_native_kappa_l_proper_vertex_evaluated"] == 1,
          "cross-consistency: the companion fill check owns the flag")
    check(EXPORT_FLAGS["Export_native_kappa_l_evaluated"] == 0,
          "native kappa_l must remain OPEN (Delta-alpha legs)")
    # the Delta-alpha-legs residual: the surviving named-open, pinned
    dk_OS, _, _, _ = kappa_l_vertex_component(_S2_OS, 1.0 / 128.21)
    residual = d["remainder_effva_canonical"] - dk_OS
    check(abs(residual - 0.014137348) < 5e-5 and residual > 1e-3,
          f"Delta-alpha-legs residual drifted or vanished: {residual}")

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
             "the kappa_l named-open, re-cut to the Delta-alpha-legs residual "
             "+0.014137 after the .361 vertex-component fill [C]",
        tier=4, epistemic="C",
        summary=(
            f"THE SURVIVING NAMED-OPEN (re-cut v24.3.361): of the canonical "
            f"slot budget {d['remainder_effva_canonical']:+.6f} (= all-orders "
            f"import {d['target']:.6f} - custodial {d['custodial_banked']:.6f} "
            f"- effva gamma-Z {d['gammaZ_effva_canonical']:+.6f}), the vertex "
            f"component +0.003453 is CLOSED (the .361 fill, ACFW-gated -- see "
            f"T_w_trace_native_kappa_l_vertex_component_closed); the residual "
            f"{residual:+.6f} stays OPEN [C]: the Delta-alpha / light-fermion "
            f"legs ([P+tool]-class, data-bound; delta_alpha_* modules exist "
            f"and are NOT claimed here) + genuine higher orders. Native "
            f"kappa_l therefore stays OPEN (flag asserted 0); DIZET stays the "
            f"publishable OS-W closure; no 3/13-is-physical claim; v15.1 "
            f"untouched. SLOT HISTORY, pinned: the legacy 0.013604 label was "
            f"a mixed-order mixed-bookkeeping residual (.358 re-price, walk "
            f"2026-07-02); the .358 ACFW instrument recorded the absolute "
            f"FAIL +0.0194 M_H-flat that found the PUBLISHED CERN-95-03 "
            f"Lambda_3 sign defect (corrigendum .360, provenance settled "
            f"against BHM 1986 + Hollik DESY 88-188); the gamma-Z booking "
            f"collision was ADJUDICATED effva-canonical (principal ruling "
            f"2026-07-03, Decisions List; an adjudication is a ruling, not a "
            f"derivation): this module's DFGRU rung books "
            f"{booking_oblique:+.6f} = +(c/s)X vs the canonical effva "
            f"{booking_effva:+.6f} = -(c/s)[X + SgZ0] on the SAME banked "
            f"Sig_AZ object -- both bookings and the legacy carve stay "
            f"machine-pinned below; drift in any re-opens the ruling."
        ),
        key_result=(
            f"named-open re-cut: Delta-alpha legs {residual:+.6f} stay [C] "
            f"(vertex component closed at .361, ACFW-gated); dual-booking "
            f"pinned ({booking_oblique:+.6f} vs {booking_effva:+.6f}); "
            f"kappa_l stays OPEN. [C]"
        ),
        dependencies=["T_w_trace_native_kappa_l_oblique_assembly"],
        cross_refs=["T_w_trace_kappa_l_ACFW_published_one_loop_benchmark",
                    "T_w_trace_native_kappa_l_vertex_component_closed"],
        artifacts={"remainder_legacy_dfgru_carve": round(d["remainder"], 9),
                   "slot_is_mixed_order_mixed_bookkeeping_residual": True,
                   "vertex_component_closed_at_361": True,
                   "vertex_component_banked_OS_deck": round(dk_OS, 9),
                   "delta_alpha_legs_residual_open": round(residual, 9),
                   "benchmark_shape": "PASS",
                   "benchmark_absolute": "PASS_post_360",
                   "benchmark_absolute_history": "FAIL_RECORDED at .358 -> "
                       "defect found .360: published Lambda_3 sign",
                   "booking_collision": "ADJUDICATED effva-canonical (ruling 2026-07-03)",
                   "booking_dfgru_cs_X_noncanonical": round(booking_oblique, 9),
                   "booking_effva_cs_X_plus_SgZ0_canonical": round(booking_effva, 9),
                   "canonical_slot_budget_effva": round(d["remainder_effva_canonical"], 9),
                   "export_flags": dict(EXPORT_FLAGS)},
    )


_CHECKS = {
    "T_w_trace_native_kappa_l_gammaZ_mixing":
        check_T_w_trace_native_kappa_l_gammaZ_mixing_P,
    "T_w_trace_native_kappa_l_vertex_component_closed":
        check_T_w_trace_native_kappa_l_vertex_component_closed_P,
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
            "Five banked checks on the leptonic effective-angle ladder "
            "(post v24.3.361). The gamma-Z booking is ADJUDICATED "
            "effva-canonical (principal ruling 2026-07-03, Decisions List; "
            "dual-booking machine-pinned: DFGRU +0.001483 non-canonical vs "
            "effva -0.002503 canonical). "
            "check_T_w_trace_native_kappa_l_gammaZ_mixing_P (tier 4, "
            "P_structural_partial) retains the DFGRU-recipe arithmetic as "
            "the collision's pinned second leg (ladder-role claim retired). "
            "check_T_w_trace_native_kappa_l_custodial_consistent_P (tier 4, "
            "P) ties the custodial rung 0.021721 to the banked "
            "decomposition. check_T_w_trace_native_kappa_l_oblique_assembly_P "
            "(tier 4, P_structural_partial) is the dual-booking record: "
            "canonical effva assembly 0.019218 = 52.2 percent of the target "
            "/ DFGRU 0.023204 = 63.0 percent pinned as the non-canonical "
            "record. check_T_w_trace_native_kappa_l_vertex_component_closed_P "
            "(tier 4, bespoke grade P_structural_vertex_component_effva_"
            "canonical_ruling_ACFW_benchmark_gated) CLOSES the vertex "
            "component of the canonical slot at +0.003453 (banked-OS deck; "
            "ACFW-deck cross-value +0.003248) on the v24.3.360 "
            "sign-corrected Lambda_3, gated live by the ACFW "
            "published-one-loop benchmark; canonical ladder 0.022670 = 61.6 "
            "percent of the all-orders import. "
            "check_L_w_trace_native_kappa_l_proper_vertex_open_C (tier 4, C) "
            "is the surviving honest-OPEN record, re-cut to the "
            "Delta-alpha/light-fermion legs residual +0.014137 "
            "([P+tool]-class, not claimed). kappa_l is NOT closed; no sin^2 "
            "theta_eff value is exported; DIZET stays the publishable OS-W "
            "closure. "
        ),
        "note": ("Wave 7 onboarding; claim_text RE-ONBOARDED at v24.3.361 "
                 "(the Wave-7 snapshot described the pre-.358 state; "
                 "verdict-tested through summarize_input before landing, "
                 "token unchanged SOLVED_LOCAL_HELD_FOR_REPAIR per the "
                 "generic ledger-solver vocabulary -- kappa_l not closed, "
                 "no global-P export)."),
    },
)
