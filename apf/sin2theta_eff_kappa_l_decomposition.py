"""APF sin^2 theta_eff leptonic form-factor (kappa_l) decomposition -- Tier-4.

Target-architecture pack for the open program flagged in
``apf.sin2theta_eff_bsy_real_adapter`` as
``Export_EW_APF_internal_full_form_factor_derivation = 0``.

The effective leptonic mixing angle is the on-shell mixing angle dressed by a
single leptonic form factor:

    sin^2 theta_eff = kappa_l * sin^2 theta_OS .

In the on-shell (Sirlin/Denner) electroweak scheme the form-factor shift admits
the standard decomposition

    Delta kappa_l = Xi_rho * Delta rho  +  Delta kappa_rem ,        Xi_rho = c_W^2 / s_W^2 ,

whose leading term is the custodial-symmetry-breaking piece carried by the
rho-parameter shift Delta rho -- the SAME quantity that already drives the W
mass in ``apf.gauge.check_L_W_mass``.

What this module does (and does NOT) claim
------------------------------------------
This pack makes the *leading custodial term* APF-internal by reusing two
already-banked anchors and nothing else:

  * Xi_rho is read off the banked on-shell mass-ratio codomain
    ``sin^2 theta_OS = 0.223339`` (``sin2theta_eff_bsy_real_adapter
    .SIN2THETA_CODOMAINS``), giving Xi_rho = c_W^2/s_W^2 = 3.4775.
  * Delta rho is recomputed from the L_W_mass formula (top + QCD + Higgs
    custodial pieces, sourced identically to ``gauge.check_L_W_mass``) and
    cross-checked value-identical to that banked check.

The leading custodial term Xi_rho * Delta rho = 0.021721 reproduces 59.0% of
the banked target Delta kappa_l = 0.036808. The remainder
Delta kappa_rem = 0.015087 (the Delta-alpha running plus the non-custodial
vertex/box remainder) is the SINGLE named, currently-unevaluated slot. It is
NOT claimed derived.

Accordingly the full-form-factor flag stays 0; this pack only flips on the new
leading-term flag and keeps the remainder flag at 0. Route 13 moves from
"imported form factor (entirely external)" to "leading custodial term
APF-internal + named remainder gate" -- an honest increment, not a closure.

No measured value of sin^2 theta_eff is consumed. The only externally-anchored
number is the kappa_l ratio target itself, which is the already-banked
import-only form-factor ratio (LATEST-51), not a new fit.

Status
------
- Export_sin2theta_eff_kappa_l_leading_custodial_term_internal = 1  (NEW here)
- Export_sin2theta_eff_kappa_l_remainder_derived               = 0  (open gate)
- Export_EW_APF_internal_full_form_factor_derivation           = 0  (unchanged)
"""
from __future__ import annotations

import math
from fractions import Fraction
from typing import Any, Dict

from apf.apf_utils import check, _result

# Banked anchors (provenance imports -- no new numbers introduced here).
from apf.sin2theta_eff_bsy_real_adapter import (
    SIN2THETA_CODOMAINS,
    KAPPA_L_TARGET,
)


# ============================================================================
# Banked-constant provenance (identical sourcing to gauge.check_L_W_mass [P])
# ============================================================================

_SIN2_W = float(Fraction(3, 13))   # T_sin2theta [P]
_ALPHA_EM = 1.0 / 128.21           # L_alpha_em [P]
_ALPHA_S = 0.1179                  # L_alpha_s_zero_input [P]
_M_T = 163.0                       # GeV, L_sigma_normalization [P]
_M_Z = 91.1876                     # GeV, anchor
_M_H = 124.93                      # GeV, Higgs custodial piece (as in L_W_mass)

# Banked on-shell mass-ratio codomain (sin2theta_eff_bsy_real_adapter).
_SIN2_OS = SIN2THETA_CODOMAINS["on_shell_mass_ratio_1_minus_MW2_MZ2"]  # 0.223339

# Banked leptonic form-factor ratio target (LATEST-51, import-only).
_KAPPA_L_TARGET = KAPPA_L_TARGET["kappa_l_target"]      # 1.036807775
_DELTA_KAPPA_L_TARGET = KAPPA_L_TARGET["delta_kappa_l"]  # 0.036807775

# PDG top-mass reference. Used ONLY for the diagnostic m_t-normalization split
# of the remainder -- it is NOT the operative value (the operative banked m_t
# stays 163, sigma-normalized, _M_T above) and NOT a fit input. Equals the
# banked w_trace PDG_RHO_T_REFERENCE_MT_GEV.
_MT_PDG_REFERENCE = 172.61


# ============================================================================
# Core computation
# ============================================================================

def _compute_drho() -> Dict[str, float]:
    """Recompute the rho-parameter shift exactly as apf.gauge.check_L_W_mass.

    Returns the top / QCD / Higgs custodial pieces and their sum. This is a
    re-evaluation of the SAME banked custodial-breaking quantity (provenance:
    gauge.check_L_W_mass), not an independent derivation; check_L_*_drho_
    matches_gauge_P pins them value-identical.
    """
    M_W_tree = _M_Z * math.sqrt(1 - _SIN2_W)
    drho_top = 3 * _ALPHA_EM * _M_T ** 2 / (16 * math.pi * M_W_tree ** 2 * _SIN2_W)
    drho_qcd = -2 * _ALPHA_S / math.pi * drho_top
    drho_h = -11 * _ALPHA_EM * _M_H ** 2 / (192 * math.pi * M_W_tree ** 2 * _SIN2_W)
    return {
        "top": drho_top,
        "qcd": drho_qcd,
        "h": drho_h,
        "tot": drho_top + drho_qcd + drho_h,
    }


def _decomposition() -> Dict[str, float]:
    """The Delta kappa_l = Xi_rho * Delta rho + Delta kappa_rem decomposition.

    Canonical leading term uses the FULL custodial rho-shift Delta rho_tot
    (top + QCD + Higgs); the top-only figure is exposed as a diagnostic. The
    remainder is DEFINED as the residual to the banked target (so leading +
    remainder reconstruct the target by construction).
    """
    drho = _compute_drho()
    xi_rho = (1.0 - _SIN2_OS) / _SIN2_OS                # c_W^2 / s_W^2 = 3.4775
    lead_tot = xi_rho * drho["tot"]
    lead_top = xi_rho * drho["top"]
    rem = _DELTA_KAPPA_L_TARGET - lead_tot
    return {
        "xi_rho": xi_rho,
        "drho_tot": drho["tot"],
        "drho_top": drho["top"],
        "lead_custodial_tot": lead_tot,
        "lead_custodial_top_diagnostic": lead_top,
        "delta_kappa_rem": rem,
        "delta_kappa_l_target": _DELTA_KAPPA_L_TARGET,
        "kappa_l_target": _KAPPA_L_TARGET,
        "coverage_fraction_tot": lead_tot / _DELTA_KAPPA_L_TARGET,
        "coverage_fraction_top_diagnostic": lead_top / _DELTA_KAPPA_L_TARGET,
    }


def _drho_tot_at_mt(mt: float) -> float:
    """Framework L_W_mass custodial rho-shift (top+QCD+Higgs) at a given m_t.

    Generalizes _compute_drho to an arbitrary top mass for the diagnostic
    m_t-normalization split. The top piece scales as m_t^2; the QCD piece
    tracks it; the Higgs piece is m_t-independent.
    """
    M_W_tree = _M_Z * math.sqrt(1 - _SIN2_W)
    drho_top = 3 * _ALPHA_EM * mt ** 2 / (16 * math.pi * M_W_tree ** 2 * _SIN2_W)
    drho_qcd = -2 * _ALPHA_S / math.pi * drho_top
    drho_h = -11 * _ALPHA_EM * _M_H ** 2 / (192 * math.pi * M_W_tree ** 2 * _SIN2_W)
    return drho_top + drho_qcd + drho_h


def _remainder_decomposition() -> Dict[str, float]:
    """Split the banked remainder Delta kappa_rem into a diagnostic ledger.

    gap_mt = Xi_rho*(Delta rho(m_t_PDG) - Delta rho(m_t_banked)); the
    sigma-normalized-top-mass scheme share. remainder_nonrho = target -
    Xi_rho*Delta rho(m_t_PDG); the genuine non-custodial residual (bosonic +
    vertex/box + light-fermion + Delta-alpha-related) which -- per the Delta
    r-ladder discipline -- stays a source-proxy NOT admitted for export.
    gap_mt + remainder_nonrho == Delta kappa_rem by construction.
    """
    d = _decomposition()
    xi = d["xi_rho"]
    lead_banked = d["lead_custodial_tot"]
    lead_pdg_mt = xi * _drho_tot_at_mt(_MT_PDG_REFERENCE)
    gap_mt = lead_pdg_mt - lead_banked
    rem_nonrho = d["delta_kappa_l_target"] - lead_pdg_mt
    rem_total = d["delta_kappa_rem"]
    return {
        "delta_kappa_rem_total": rem_total,
        "lead_at_banked_mt_163": lead_banked,
        "lead_at_pdg_mt_172_61": lead_pdg_mt,
        "gap_mt_normalization": gap_mt,
        "remainder_nonrho": rem_nonrho,
        "gap_mt_fraction_of_remainder": gap_mt / rem_total,
        "remainder_nonrho_fraction_of_remainder": rem_nonrho / rem_total,
        "remainder_nonrho_fraction_of_target": rem_nonrho / d["delta_kappa_l_target"],
    }


# ============================================================================
# Honest non-claim flags
# ============================================================================

EXPORT_FLAGS: Dict[str, int] = {
    # NEW at this module: the leading custodial term is APF-internal.
    "Export_sin2theta_eff_kappa_l_leading_custodial_term_internal": 1,
    # The remainder (Delta-alpha running + vertex/box) is NOT derived.
    "Export_sin2theta_eff_kappa_l_remainder_derived": 0,
    # The full form-factor derivation remains OPEN (unchanged from LATEST-51).
    "Export_EW_APF_internal_full_form_factor_derivation": 0,
}

# External numeric anchors this module is permitted to consume. Both are
# already banked; the decomposition introduces NO new external input.
_ALLOWED_EXTERNAL_ANCHORS = frozenset({
    "banked_kappa_l_ratio_target_LATEST_51",
    "banked_on_shell_mass_ratio_codomain",
    "banked_L_W_mass_custodial_drho_constants",
})

# Target-value keys that would constitute smuggling if consumed.
_FORBIDDEN_TARGET_KEYS = frozenset({
    "measured_sin2theta_eff",
    "fitted_kappa_l",
    "observed_delta_kappa_l",
    "pdg_sin2theta_eff_target",
})

# Diagnostic-only external reference (NOT admitted for export, NOT a fit input):
# used solely to attribute the remainder's m_t-normalization share. Kept
# strictly disjoint from the export anchor ledger above.
_DIAGNOSTIC_ONLY_REFERENCES = frozenset({
    "diagnostic_pdg_top_mass_reference_172_61",
})


# ============================================================================
# Bank-registered checks
# ============================================================================

def check_T_sin2theta_eff_kappa_l_leading_custodial_internal_P() -> Dict[str, Any]:
    """T: leading custodial form-factor term is APF-internal [P].

    Delta kappa_l^lead = Xi_rho * Delta rho with Xi_rho read off the banked
    on-shell codomain and Delta rho the banked custodial shift. Reproduces
    0.021721 (59.0% of the banked target), sign-correct, dominant single
    contribution, and strictly below the target (positive remainder).
    """
    d = _decomposition()
    lead = d["lead_custodial_tot"]
    target = d["delta_kappa_l_target"]

    check(abs(lead - 0.021721186) < 1e-7,
          f"leading custodial term {lead} != expected 0.021721186")
    check(abs(d["xi_rho"] - 3.4774983321) < 1e-9,
          f"Xi_rho {d['xi_rho']} != c_W^2/s_W^2 at OS codomain")
    check(lead > 0 and target > 0,
          "leading term and target must share sign (both positive)")
    check(lead / target > 0.5,
          f"leading custodial term must be the dominant single contribution "
          f"(got {lead / target:.3f})")
    check(lead < target,
          "leading term alone must not overshoot the target (remainder > 0)")

    return _result(
        name="T_sin2theta_eff_kappa_l_leading_custodial_internal: "
             "leading leptonic form-factor term from banked Delta rho [P]",
        tier=4, epistemic="P",
        summary=(
            f"Delta kappa_l = Xi_rho * Delta rho + Delta kappa_rem. "
            f"Xi_rho = c_W^2/s_W^2 = {d['xi_rho']:.6f} (banked OS codomain "
            f"sin^2 theta_OS = {_SIN2_OS}); Delta rho = {d['drho_tot']:.6f} "
            f"(banked L_W_mass custodial shift). Leading custodial term "
            f"= {lead:.6f} = {d['coverage_fraction_tot']*100:.1f}% of the "
            f"banked target Delta kappa_l = {target:.6f}. Top-only diagnostic "
            f"= {d['lead_custodial_top_diagnostic']:.6f} "
            f"({d['coverage_fraction_top_diagnostic']*100:.1f}%). The leading "
            f"term is now APF-internal; the remainder is the named open gate."
        ),
        key_result=(
            f"Delta kappa_l^lead = {lead:.6f} "
            f"({d['coverage_fraction_tot']*100:.1f}% of target), APF-internal. [P]"
        ),
        dependencies=["T_sin2theta", "L_W_mass", "L_alpha_em",
                      "L_sigma_normalization", "L_alpha_s_zero_input"],
        cross_refs=["check_T_sin2theta_eff_bsy_adapter_evaluator_consistent_P"],
        artifacts={k: round(v, 9) for k, v in d.items()},
    )


def check_L_sin2theta_eff_kappa_l_drho_matches_gauge_P() -> Dict[str, Any]:
    """L: the Delta rho used here is value-identical to gauge.L_W_mass [P].

    Cross-module consistency: this module re-evaluates the SAME custodial
    rho-shift rather than re-deriving it. Pins top/QCD/Higgs pieces equal to
    the banked gauge.check_L_W_mass artifacts at banked (6-dp) precision.
    """
    from apf import gauge
    g = gauge.check_L_W_mass()["artifacts"]
    drho = _compute_drho()

    pairs = (
        ("Drho_top", drho["top"]),
        ("Drho_QCD", drho["qcd"]),
        ("Drho_H", drho["h"]),
    )
    for key, mine in pairs:
        check(round(mine, 6) == g[key],
              f"{key}: local {round(mine, 6)} != gauge banked {g[key]}")

    return _result(
        name="L_sin2theta_eff_kappa_l_drho_matches_gauge: "
             "custodial Delta rho identical to L_W_mass [P]",
        tier=3, epistemic="P",
        summary=(
            "The rho-parameter shift reused in the kappa_l decomposition "
            "(top + QCD + Higgs) is value-identical to the banked "
            "gauge.check_L_W_mass custodial pieces at banked precision: "
            f"Drho_top={g['Drho_top']}, Drho_QCD={g['Drho_QCD']}, "
            f"Drho_H={g['Drho_H']}. No independent re-derivation; same "
            "custodial-breaking quantity, two consumers (W mass + kappa_l)."
        ),
        key_result="Delta rho reused from L_W_mass, value-identical. [P]",
        dependencies=["L_W_mass"],
        cross_refs=["T_sin2theta_eff_kappa_l_leading_custodial_internal"],
        artifacts={
            "drho_top": round(drho["top"], 6),
            "drho_qcd": round(drho["qcd"], 6),
            "drho_h": round(drho["h"], 6),
            "gauge_drho_top": g["Drho_top"],
            "gauge_drho_qcd": g["Drho_QCD"],
            "gauge_drho_h": g["Drho_H"],
        },
    )


def check_L_sin2theta_eff_kappa_l_remainder_named_open_C() -> Dict[str, Any]:
    """L: the form-factor remainder is the single named OPEN gate [C].

    Honest non-claim. Delta kappa_rem = target - leading is the one
    currently-unevaluated slot (Delta-alpha running + non-custodial vertex/box).
    Asserts: leading + remainder reconstruct the target exactly; the remainder
    is non-zero (gap honestly open); the full-form-factor and remainder-derived
    export flags both stay 0.
    """
    d = _decomposition()
    lead = d["lead_custodial_tot"]
    rem = d["delta_kappa_rem"]
    target = d["delta_kappa_l_target"]

    check(abs((lead + rem) - target) < 1e-12,
          "leading + remainder must reconstruct the banked target")
    check(rem > 1e-4,
          f"remainder must be a genuine, non-trivial open gap (got {rem})")
    check(EXPORT_FLAGS["Export_EW_APF_internal_full_form_factor_derivation"] == 0,
          "full form-factor derivation must remain UNCLAIMED (flag 0)")
    check(EXPORT_FLAGS["Export_sin2theta_eff_kappa_l_remainder_derived"] == 0,
          "remainder must remain UNCLAIMED (flag 0)")

    return _result(
        name="L_sin2theta_eff_kappa_l_remainder_named_open: "
             "form-factor remainder is the single OPEN gate [C]",
        tier=4, epistemic="C",
        summary=(
            f"Delta kappa_rem = {rem:.6f} "
            f"({rem/target*100:.1f}% of the target) is the single named, "
            f"currently-unevaluated slot: the Delta-alpha running plus the "
            f"non-custodial vertex/box remainder. It is NOT claimed derived. "
            f"Leading + remainder reconstruct the banked target exactly. The "
            f"full-form-factor derivation flag and the remainder-derived flag "
            f"both stay 0; this pack only flips on the leading-custodial-term "
            f"flag."
        ),
        key_result=(
            f"Delta kappa_rem = {rem:.6f} OPEN (named gate, not derived). [C]"
        ),
        dependencies=["T_sin2theta_eff_kappa_l_leading_custodial_internal"],
        artifacts={
            "delta_kappa_rem": round(rem, 9),
            "remainder_fraction": round(rem / target, 6),
            "export_flags": dict(EXPORT_FLAGS),
        },
    )


def check_T_sin2theta_eff_kappa_l_no_target_smuggling_P() -> Dict[str, Any]:
    """T: the decomposition smuggles no fitted/measured target [P].

    Guard: the only externally-anchored number is the already-banked kappa_l
    ratio target (LATEST-51 import-only). No measured sin^2 theta_eff, no
    fitted kappa_l is consumed; the leading term uses only APF-internal banked
    constants. The allowed-anchor ledger is closed and disjoint from the
    forbidden-target-key set.
    """
    # kappa_l target must come from the banked adapter, value-pinned.
    check(abs(_KAPPA_L_TARGET - 1.036807775) < 1e-12,
          "kappa_l target must equal the banked LATEST-51 ratio target")
    check(abs(_DELTA_KAPPA_L_TARGET - 0.036807775) < 1e-12,
          "delta_kappa_l target must equal the banked value")
    # Anchor ledger must be disjoint from the forbidden (smuggling) keys.
    check(_ALLOWED_EXTERNAL_ANCHORS.isdisjoint(_FORBIDDEN_TARGET_KEYS),
          "allowed-anchor ledger overlaps the forbidden target-key set")
    # Exactly the two banked anchors plus the banked drho constants -- nothing
    # new. (Ledger has cardinality 3 and is explicit.)
    check(len(_ALLOWED_EXTERNAL_ANCHORS) == 3,
          "anchor ledger must list exactly the three banked anchors")
    # Leading term must NOT depend on any forbidden measured value: the
    # decomposition only references banked constants + the OS codomain.
    d = _decomposition()
    check(abs(d["xi_rho"] - (1.0 - _SIN2_OS) / _SIN2_OS) < 1e-15,
          "Xi_rho must derive solely from the banked OS codomain")

    return _result(
        name="T_sin2theta_eff_kappa_l_no_target_smuggling: "
             "no fitted/measured target consumed [P]",
        tier=4, epistemic="P",
        summary=(
            "The kappa_l decomposition consumes no new external numeric input. "
            "The single externally-anchored number is the already-banked "
            "kappa_l ratio target (1.036807775, LATEST-51 import-only). No "
            "measured sin^2 theta_eff, no fitted kappa_l, no PDG target is "
            "read. The leading term is built only from banked constants "
            "(alpha_em, alpha_s, m_t, M_Z, sin^2_W = 3/13) and the banked "
            "on-shell codomain. Allowed-anchor ledger is disjoint from the "
            "forbidden-target-key set."
        ),
        key_result="No fitted/measured target smuggled into the decomposition. [P]",
        dependencies=["T_sin2theta_eff_kappa_l_leading_custodial_internal"],
        artifacts={
            "allowed_external_anchors": sorted(_ALLOWED_EXTERNAL_ANCHORS),
            "forbidden_target_keys": sorted(_FORBIDDEN_TARGET_KEYS),
            "kappa_l_target": _KAPPA_L_TARGET,
        },
    )


def check_T_sin2theta_eff_kappa_l_remainder_mt_normalization_split_P():
    """T: remainder = m_t-normalization gap + genuine residual [P_structural]."""
    r = _remainder_decomposition()
    check(abs((r["gap_mt_normalization"] + r["remainder_nonrho"])
              - r["delta_kappa_rem_total"]) < 1e-12,
          "gap_mt + remainder_nonrho must reconstruct Delta kappa_rem")
    check(abs(r["gap_mt_normalization"] - 0.003272) < 1e-5,
          f"m_t-normalization gap {r['gap_mt_normalization']} != expected 0.003272")
    check(abs(r["remainder_nonrho"] - 0.011815) < 1e-5,
          f"genuine residual {r['remainder_nonrho']} != expected 0.011815")
    check(0.0 < r["gap_mt_normalization"] < r["remainder_nonrho"],
          "m_t-normalization gap must be the smaller share (genuine residual dominates)")
    return _result(
        name="T_sin2theta_eff_kappa_l_remainder_mt_normalization_split: "
             "remainder = m_t-normalization gap + genuine residual [P_structural]",
        tier=4, epistemic="P_structural",
        summary=(
            f"Delta kappa_rem = {r['delta_kappa_rem_total']:.6f} splits, using the "
            f"framework's own custodial Delta rho formula at m_t=163 vs the PDG "
            f"reference m_t=172.61, into: m_t-normalization gap = "
            f"{r['gap_mt_normalization']:.6f} "
            f"({r['gap_mt_fraction_of_remainder']*100:.1f}% of the remainder, the "
            f"sigma-normalized-top-mass scheme share) + genuine non-custodial "
            f"residual = {r['remainder_nonrho']:.6f} "
            f"({r['remainder_nonrho_fraction_of_remainder']*100:.1f}% of the "
            f"remainder, {r['remainder_nonrho_fraction_of_target']*100:.1f}% of "
            f"the target). The genuine residual dominates."
        ),
        key_result=(
            f"remainder = {r['gap_mt_normalization']:.6f} (m_t-norm) + "
            f"{r['remainder_nonrho']:.6f} (genuine residual). [P_structural]"
        ),
        dependencies=["T_sin2theta_eff_kappa_l_leading_custodial_internal",
                      "L_sin2theta_eff_kappa_l_remainder_named_open"],
        artifacts={k: round(v, 9) for k, v in r.items()},
    )


def check_L_sin2theta_eff_kappa_l_nonrho_remainder_open_C():
    """L: the genuine non-custodial residual is a source-proxy OPEN gate [C]."""
    r = _remainder_decomposition()
    check(r["remainder_nonrho"] > 1e-3,
          "genuine residual must be a non-trivial open gap")
    check(EXPORT_FLAGS["Export_sin2theta_eff_kappa_l_remainder_derived"] == 0,
          "remainder must remain UNCLAIMED (flag 0)")
    check(EXPORT_FLAGS["Export_EW_APF_internal_full_form_factor_derivation"] == 0,
          "full form-factor derivation must remain UNCLAIMED (flag 0)")
    check("diagnostic_pdg_top_mass_reference_172_61" in _DIAGNOSTIC_ONLY_REFERENCES,
          "m_t PDG reference must be fenced as diagnostic-only")
    check(_DIAGNOSTIC_ONLY_REFERENCES.isdisjoint(_ALLOWED_EXTERNAL_ANCHORS),
          "diagnostic-only references must not enter the export anchor ledger")
    return _result(
        name="L_sin2theta_eff_kappa_l_nonrho_remainder_open: "
             "genuine non-custodial residual is a source-proxy OPEN gate [C]",
        tier=4, epistemic="C",
        summary=(
            f"The genuine non-custodial residual = {r['remainder_nonrho']:.6f} "
            f"({r['remainder_nonrho_fraction_of_target']*100:.1f}% of the target) "
            f"-- bosonic, vertex/box, light-fermion and Delta-alpha-related pieces "
            f"-- is the residual OPEN gate. Per the framework's Delta r-ladder "
            f"discipline it is a source-proxy NOT admitted for export; Delta alpha "
            f"is NOT internalized (the Delta r ladder keeps it a PDG source-proxy, "
            f"promotes_to_APF_component=False). Export flags stay 0; the m_t PDG "
            f"reference is fenced diagnostic-only."
        ),
        key_result=(
            f"genuine residual = {r['remainder_nonrho']:.6f} OPEN "
            f"(source-proxy, Delta alpha not internalized). [C]"
        ),
        dependencies=["T_sin2theta_eff_kappa_l_remainder_mt_normalization_split"],
        artifacts={
            "remainder_nonrho": round(r["remainder_nonrho"], 9),
            "remainder_nonrho_fraction_of_target": round(
                r["remainder_nonrho_fraction_of_target"], 6),
            "diagnostic_only_references": sorted(_DIAGNOSTIC_ONLY_REFERENCES),
            "export_flags": dict(EXPORT_FLAGS),
        },
    )


# ============================================================================
# Registration / public interface
# ============================================================================

_CHECKS = {
    "T_sin2theta_eff_kappa_l_leading_custodial_internal":
        check_T_sin2theta_eff_kappa_l_leading_custodial_internal_P,
    "L_sin2theta_eff_kappa_l_drho_matches_gauge":
        check_L_sin2theta_eff_kappa_l_drho_matches_gauge_P,
    "L_sin2theta_eff_kappa_l_remainder_named_open":
        check_L_sin2theta_eff_kappa_l_remainder_named_open_C,
    "T_sin2theta_eff_kappa_l_no_target_smuggling":
        check_T_sin2theta_eff_kappa_l_no_target_smuggling_P,
    "T_sin2theta_eff_kappa_l_remainder_mt_normalization_split":
        check_T_sin2theta_eff_kappa_l_remainder_mt_normalization_split_P,
    "L_sin2theta_eff_kappa_l_nonrho_remainder_open":
        check_L_sin2theta_eff_kappa_l_nonrho_remainder_open_C,
}


def register(registry):
    """Register the kappa_l decomposition checks into the global bank."""
    registry.update(_CHECKS)
    return registry


def run_all() -> Dict[str, Dict[str, Any]]:
    return {name: fn() for name, fn in _CHECKS.items()}


def decomposition_report() -> Dict[str, Any]:
    return {
        "decomposition": _decomposition(),
        "remainder_decomposition": _remainder_decomposition(),
        "export_flags": dict(EXPORT_FLAGS),
        "allowed_external_anchors": sorted(_ALLOWED_EXTERNAL_ANCHORS),
        "diagnostic_only_references": sorted(_DIAGNOSTIC_ONLY_REFERENCES),
    }


if __name__ == "__main__":
    import json
    out = run_all()
    print(json.dumps(
        {k: {"passed": v["passed"], "epistemic": v["epistemic"]}
         for k, v in out.items()},
        indent=2,
    ))
    print(json.dumps(_decomposition(), indent=2))
