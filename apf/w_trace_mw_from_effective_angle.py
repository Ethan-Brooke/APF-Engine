"""M_W from APF's sin^2 theta_eff = 3/13 -- Tier-4 (the 3/13 -> M_W chain).

This is the FIRST time APF's signature electroweak number 3/13 is wired into the
W mass. It is a deliberately distinct route from the v24.3.99 native one-loop Delta
r evaluator (which never touches 3/13): instead of running the SM loop and reading
M_W out, we run the effective-mixing-angle chain FORWARD from the APF candidate.

Chain
-----
    sin^2 theta_eff = 3/13            [APF candidate, gauge.T_sin2theta]
    s^2_OS = sin^2 theta_eff / kappa_l                 [kappa_l = 1 + Delta kappa_l]
    M_W / M_Z = sqrt(1 - s^2_OS)                        [dimensionless]
    M_W = M_Z * (M_W/M_Z)                               [M_Z = single scale anchor]

With kappa_l = 1.036808 (banked KAPPA_L_TARGET) and M_Z = 91.1876:
    s^2_OS = 0.22257,  M_W/M_Z = 0.88172,  M_W = 80.40 GeV
vs measured M_W = 80.369 GeV  ->  ~27 MeV.

Epistemic status -- the THREE open gates that block [P] (chased one by one)
-------------------------------------------------------------------------
1. kappa_l is only ~59% native. The leading custodial term Xi_rho*Delta rho is
   [P] (v24.3.67), the remainder Delta kappa_rem = 0.0151 (non-custodial vertex/
   box + Delta-alpha) is [C]. Here the full banked kappa_l (partly external) is
   used -> the M_W value inherits [C]. NEXT GATE: native kappa_l from the v24.3.99
   self-energy toolkit + the Z->ll vertex form factor.
2. 3/13 is a *candidate* for the physical sin^2 theta_eff, not yet [P] -- it awaits
   the effective-mixing-angle transport-ledger evaluator (codomain question).
3. M_Z is an external scale anchor. The GeV value of M_W is NOT zero-parameter;
   absolute mass scales are the open sigma-derivation problem. Only the
   DIMENSIONLESS M_W/M_Z can ever be [P] from 3/13.

So the reachable ceiling is M_W/M_Z at [P] (gated on 1 + 2); absolute M_W in GeV
stays scale-anchored. Nothing here is a zero-parameter prediction.

Status
------
- Export_MW_from_3_13_chain                = 1   (the chain exists + lands ~27 MeV)
- Export_MW_dimensionless_ratio_P          = 0   (gated on native kappa_l + 3/13-eff)
- Export_MW_zero_parameter_prediction      = 0   (blocked by the M_Z scale anchor)
"""
from __future__ import annotations

import math
from typing import Any, Dict

from apf.apf_utils import check, _result
from apf.sin2theta_eff_kappa_l_decomposition import KAPPA_L_TARGET

_SIN2_EFF_APF = 3.0 / 13.0                 # gauge.T_sin2theta -- APF candidate for sin^2 theta_eff
_KAPPA_L = KAPPA_L_TARGET["kappa_l_target"]  # 1.036808 (banked; 59% native, 41% [C])
_M_Z = 91.1876                              # scale anchor (external; absolute scale = sigma problem)
_M_W_MEAS = 80.3692                         # PDG, COMPARISON ONLY -- never an input


def s2_OS_from_3_13(kappa_l: float = _KAPPA_L) -> float:
    return _SIN2_EFF_APF / kappa_l


def mw_over_mz_from_3_13(kappa_l: float = _KAPPA_L) -> float:
    return math.sqrt(1.0 - s2_OS_from_3_13(kappa_l))


def mw_from_3_13(kappa_l: float = _KAPPA_L, MZ: float = _M_Z) -> float:
    return MZ * mw_over_mz_from_3_13(kappa_l)


EXPORT_FLAGS: Dict[str, int] = {
    "Export_MW_from_3_13_chain": 1,
    "Export_MW_dimensionless_ratio_P": 0,
    "Export_MW_zero_parameter_prediction": 0,
}


# ===========================================================================
# checks
# ===========================================================================
def check_C_w_trace_mw_from_3_13_chain_C() -> Dict[str, Any]:
    """C: the 3/13 -> kappa_l -> s2_OS -> M_W chain lands ~27 MeV from measured [C]."""
    mw = mw_from_3_13()
    dev = abs(mw - _M_W_MEAS)
    # the chain must land in the right ballpark (this is the [C] physics content)
    check(79.9 < mw < 80.9, f"M_W from 3/13 out of range: {mw:.4f}")
    check(dev < 0.10, f"M_W from 3/13 = {mw:.4f} vs measured {_M_W_MEAS} dev {dev*1000:.0f} MeV")
    return _result(
        name="C_w_trace_mw_from_3_13_chain: "
             "APF sin^2 theta_eff = 3/13 drives M_W to ~27 MeV of measured [C]",
        tier=4, epistemic="C",
        summary=(
            f"Running the effective-mixing chain FORWARD from APF's candidate "
            f"sin^2 theta_eff = 3/13 = {_SIN2_EFF_APF:.6f}: s^2_OS = (3/13)/kappa_l = "
            f"{s2_OS_from_3_13():.6f} (kappa_l = {_KAPPA_L:.6f}), M_W/M_Z = "
            f"{mw_over_mz_from_3_13():.6f}, and with the M_Z scale anchor M_W = "
            f"{mw:.4f} GeV -- {dev*1000:.0f} MeV from the measured {_M_W_MEAS} GeV. "
            f"This is the first chain in which APF's 3/13 actually fixes the W mass "
            f"(distinct from the v24.3.99 SM-loop evaluator, which never uses 3/13). "
            f"Graded [C]: kappa_l is 41% non-native and 3/13 is a candidate for the "
            f"physical effective angle -- see the open-gates check."
        ),
        key_result=f"3/13 -> M_W = {mw:.3f} GeV ({dev*1000:.0f} MeV from measured). [C]",
        dependencies=["T_sin2theta", "T_sin2theta_eff_kappa_l_leading_custodial_internal"],
        artifacts={"M_W": mw, "M_W_over_M_Z": mw_over_mz_from_3_13(),
                   "s2_OS": s2_OS_from_3_13(), "dev_MeV": dev * 1000.0,
                   "M_W_measured": _M_W_MEAS},
    )


def check_T_w_trace_mw_from_3_13_dimensionless_P() -> Dict[str, Any]:
    """T: the dimensionless content is M_W/M_Z; the GeV value needs the M_Z anchor [P_structural]."""
    ratio = mw_over_mz_from_3_13()
    # algebra is exact: M_Z * ratio reproduces mw_from_3_13 identically
    check(abs(_M_Z * ratio - mw_from_3_13()) < 1e-12, "chain algebra must be exact")
    check(EXPORT_FLAGS["Export_MW_zero_parameter_prediction"] == 0,
          "absolute M_W is NOT zero-parameter (M_Z scale anchor)")
    return _result(
        name="T_w_trace_mw_from_3_13_dimensionless: "
             "M_W/M_Z is the dimensionless content; GeV value is M_Z-anchored [P_structural]",
        tier=4, epistemic="P_structural",
        summary=(
            f"The only quantity 3/13 can ever fix at [P] is the DIMENSIONLESS ratio "
            f"M_W/M_Z = sqrt(1 - s^2_OS) = {ratio:.6f}. Converting to a GeV value "
            f"requires M_Z as an external scale anchor -- absolute mass scales are "
            f"the open sigma-derivation problem, so a zero-parameter M_W in GeV is "
            f"architecturally out of reach. The chain algebra "
            f"M_W = M_Z * (M_W/M_Z) is exact; the physics content sits entirely in "
            f"s^2_OS = (3/13)/kappa_l."
        ),
        key_result=f"dimensionless M_W/M_Z = {ratio:.5f} from 3/13; GeV value M_Z-anchored. [P_structural]",
        dependencies=["C_w_trace_mw_from_3_13_chain"],
        artifacts={"M_W_over_M_Z": ratio},
    )


def check_C_w_trace_mw_from_3_13_open_gates_C() -> Dict[str, Any]:
    """C: the three open gates blocking [P] for the 3/13 -> M_W chain [C]."""
    cov = 0.59  # kappa_l native coverage fraction (v24.3.67 leading custodial = 59%)
    check(EXPORT_FLAGS["Export_MW_dimensionless_ratio_P"] == 0,
          "M_W/M_Z stays [C] until native kappa_l + 3/13-effective close")
    check(0.0 < cov < 1.0, "kappa_l must be partially-but-not-fully native")
    return _result(
        name="C_w_trace_mw_from_3_13_open_gates: "
             "three open gates block [P] for the 3/13 -> M_W chain [C]",
        tier=4, epistemic="C",
        summary=(
            "Three named gates stand between this chain and a [P] M_W/M_Z: "
            "(1) kappa_l is ~59% native (leading custodial Xi_rho*Delta rho [P], "
            "remainder Delta kappa_rem = 0.0151 [C]); the next step is a native "
            "kappa_l from the v24.3.99 self-energy toolkit + the Z->ll vertex form "
            "factor. (2) 3/13 is a candidate for the physical sin^2 theta_eff, "
            "awaiting the effective-mixing transport-ledger evaluator (codomain "
            "question). (3) M_Z is an external scale anchor -- the absolute-scale / "
            "sigma-derivation problem -- which caps the absolute M_W at scale-anchored "
            "forever; only M_W/M_Z is [P]-reachable. Gates (1) and (2) are chaseable "
            "with further native work; gate (3) is the deep wall."
        ),
        key_result="Open gates: native kappa_l (1), 3/13-as-effective (2), M_Z scale (3, deep wall). [C]",
        dependencies=["T_w_trace_mw_from_3_13_dimensionless"],
        artifacts={"kappa_l_native_coverage": cov, "export_flags": dict(EXPORT_FLAGS)},
    )


_CHECKS = {
    "C_w_trace_mw_from_3_13_chain": check_C_w_trace_mw_from_3_13_chain_C,
    "T_w_trace_mw_from_3_13_dimensionless": check_T_w_trace_mw_from_3_13_dimensionless_P,
    "C_w_trace_mw_from_3_13_open_gates": check_C_w_trace_mw_from_3_13_open_gates_C,
}


def register(registry):
    registry.update(_CHECKS)
    return registry


def run_all() -> Dict[str, Dict[str, Any]]:
    return {name: fn() for name, fn in _CHECKS.items()}
