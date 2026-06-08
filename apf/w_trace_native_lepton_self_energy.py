"""APF-native lepton chiral self-energy on the lepton mass shell -- Tier-4 (ARCHITECTURE-ONLY).

Closes the last R2 v2 input gap flagged in INSTALL.md of the R2 v2 substrate
bundle: the external-leg lepton wavefunction counterterms

    delta_Z_2^L_lepton  and  delta_Z_2^R_lepton

which Denner's OS scheme extracts from the chiral lepton self-energy components
Sigma_L^ell(p^2) and Sigma_R^ell(p^2) on the lepton mass shell.

Status: ARCHITECTURE-ONLY (no register())
========================================
This module is sibling-AI available but NOT bank-promoted. Per the
"never bank a rushed number" discipline, the Denner Appendix B conventions
encoded here have NOT yet been validated against the v24.3.99 internal usage
(which carries them implicitly inside `delta_r_mw_assembly.Sig_W`'s lepton
block but does not expose them by chirality). The wrapper is shipped so the
sibling R2 v3 attempt can consume it; bank-promotion to [P_structural] waits
on a fresh-session pass after the sibling validates that consuming this
wrapper produces the structural kappa_l = 27/26 they target.

If the sibling's R2 v3 lands at the right kappa_l, the conventions here are
correct and this module gets promoted in the next session via the standard
ARCHITECTURE_ONLY -> BANK_REGISTRY_MODULES move. If it doesn't, the
SIGN_AUDIT_LEDGER in the sibling's pack will point at this wrapper as the
first suspect.

Convention
==========
Denner, Fortschr. Phys. 41 (1993) 307; arXiv:0709.1075 section 4.3 + appendix B
(fermion self-energies). Feynman gauge (xi = 1). MS-bar UV regularization;
photon mass lambda^2 as IR regulator (cancels in physical observables).

For a charged lepton ell with charge Q_ell = -1, isospin I3 = -1/2, the chiral
self-energy decomposes as

    Sigma^ell(p) = pslash P_L Sigma_L^ell(p^2)
                 + pslash P_R Sigma_R^ell(p^2)
                 + m_ell Sigma_S^ell(p^2).

Denner App.B with Feynman-gauge ksi=1 and the small-mass approximation
m_ell^2 / M_V^2 << 1 (valid for Z-pole kinematics) gives the chiral
components from three exchange diagrams (gamma, Z, W):

    Sigma_L^ell(p^2) = -(alpha/4pi) * [
          Q_ell^2 * B1(p^2; m_ell^2, lambda^2)      <-- photon (lepton in loop)
        + (g_L^Z,ell)^2 * B1(p^2; m_ell^2, M_Z^2)   <-- Z (lepton in loop)
        + (1/(2 s^2)) * B1(p^2; 0, M_W^2)           <-- W (neutrino in loop)
    ]

    Sigma_R^ell(p^2) = -(alpha/4pi) * [
          Q_ell^2 * B1(p^2; m_ell^2, lambda^2)      <-- photon
        + (g_R^Z,ell)^2 * B1(p^2; m_ell^2, M_Z^2)   <-- Z
    ]    <-- no W contribution (no right-handed neutrinos in SM)

with

    g_L^Z,ell = (I3 - s^2 Q_ell)/(s c) = (-1/2 + s^2)/(s c),
    g_R^Z,ell = -s Q_ell / c          = s/c.

The on-shell OS chiral wavefunction counterterms are then

    delta_Z_2^L_ell = -Sigma_L^ell(m_ell^2)
    delta_Z_2^R_ell = -Sigma_R^ell(m_ell^2)

in the massless-lepton approximation (the m_ell^2 * Sigma' correction is
m_ell^2 / M_Z^2 ~ 10^-5 at Z-pole kinematics, negligible for the R2 v2
purpose of delivering kappa_l to 3.2e-5).

Honest non-claims
=================
- Architecture-only; NOT bank-promoted.
- Conventions transcribed from Denner App.B but not yet anchored against
  the existing assembly's lepton-loop block. Sibling-validation pending.
- The W-exchange contribution to Sigma_L assumes m_neutrino = 0 (SM).
- The photon-mass regulator lambda^2 cancels in physical observables;
  individual values are lambda-dependent.
- Does NOT include two-loop or fermion-mass-suppressed corrections.
- Does NOT replace the existing assembly chain; this is a CHIRAL DECOMPOSITION
  of pieces already carried internally by Sig_W and Sig_ZZ in the v24.3.99
  evaluator. The wrapper exposes the chiral decomposition; the internal usage
  remains the source of truth.
- For the heavy-lepton tau (m_tau = 1.777 GeV), the small-mass approximation
  is m_tau^2/M_Z^2 ~ 4e-4, still small but worth flagging if precision
  becomes the limit.

Sibling consumer
================
APF_KAPPA_L_BOSONIC_ARC_TWO_ROUTE_CORROBORATION_v3 (R2 v3 renormalized-vertex
assembly), specifically the R2.b row (external lepton wavefunction
counterterms).
"""
from __future__ import annotations

import math
from typing import Any, Dict

from apf.w_trace_pv_tensor_reduction import b1_direct


PI = math.pi
ALPHA = 1.0 / 137.0359895
A4PI = ALPHA / (4.0 * PI)
MZ = 91.1876
MZ2 = MZ * MZ
MW = 80.379
MW2 = MW * MW

# Charged-lepton pole masses (matches w_trace_native_delta_r_mw_assembly conventions)
ML: Dict[str, float] = {"e": 0.51099906e-3, "mu": 0.105658387, "tau": 1.77682}

# Standard photon-mass IR regulator (matches Sig_W's lambda^2 = 1e-4)
LAMBDA2_DEFAULT = 1e-4


def _sw_cw_from_MW(mw: float = MW, mz: float = MZ) -> tuple:
    """Return (sin theta_W, cos theta_W) in the on-shell scheme."""
    c2 = (mw * mw) / (mz * mz)
    s2 = 1.0 - c2
    return math.sqrt(s2), math.sqrt(c2)


def _g_L_Z_lepton(s: float, c: float) -> float:
    """Left-handed Z coupling for a charged lepton: g_L^Z,ell = (-1/2 + s^2) / (s c)."""
    return (-0.5 + s * s) / (s * c)


def _g_R_Z_lepton(s: float, c: float) -> float:
    """Right-handed Z coupling for a charged lepton: g_R^Z,ell = s/c."""
    return s / c


def Sigma_L_lepton(
    p2: float,
    lepton: str = "e",
    s: float | None = None,
    c: float | None = None,
    mu2: float = MZ2,
    lam2: float = LAMBDA2_DEFAULT,
) -> float:
    """Left-chirality self-energy Sigma_L^ell(p^2).

    Sums photon + Z (lepton in loop) and W (neutrino in loop) exchange
    contributions via the banked B1 function. Denner App.B convention,
    Feynman gauge.

    Parameters:
        p2       : external invariant p^2 [GeV^2]
        lepton   : "e", "mu", or "tau"
        s, c     : sin / cos of theta_W (OS scheme); default from MW/MZ
        mu2      : MS-bar renormalization scale squared [GeV^2]
        lam2     : photon-mass IR regulator squared [GeV^2]; cancels in physical observables
    """
    if s is None or c is None:
        s, c = _sw_cw_from_MW()
    Q_ell = -1.0
    ml2 = ML[lepton] ** 2
    gL_Z = _g_L_Z_lepton(s, c)

    # Photon exchange: charge Q_ell on a lepton with internal lepton (mass m_ell)
    # and IR-regulated photon (mass lambda).
    photon = (Q_ell * Q_ell) * b1_direct(p2, ml2, lam2, mu2)

    # Z exchange: g_L^Z,ell coupling on a lepton with internal lepton + Z.
    z = (gL_Z * gL_Z) * b1_direct(p2, ml2, MZ2, mu2)

    # W exchange: only contributes to Sigma_L (no right-handed neutrinos).
    # Coupling factor 1/(2 s^2) from the SU(2)_L charged-current vertex.
    # Internal fermion is a massless neutrino.
    w = (1.0 / (2.0 * s * s)) * b1_direct(p2, 0.0, MW2, mu2)

    return -A4PI * (photon + z + w)


def Sigma_R_lepton(
    p2: float,
    lepton: str = "e",
    s: float | None = None,
    c: float | None = None,
    mu2: float = MZ2,
    lam2: float = LAMBDA2_DEFAULT,
) -> float:
    """Right-chirality self-energy Sigma_R^ell(p^2).

    Only the photon and Z exchanges contribute (no right-handed neutrino in
    SM, so no W exchange piece). Denner App.B convention, Feynman gauge.
    """
    if s is None or c is None:
        s, c = _sw_cw_from_MW()
    Q_ell = -1.0
    ml2 = ML[lepton] ** 2
    gR_Z = _g_R_Z_lepton(s, c)

    photon = (Q_ell * Q_ell) * b1_direct(p2, ml2, lam2, mu2)
    z = (gR_Z * gR_Z) * b1_direct(p2, ml2, MZ2, mu2)
    return -A4PI * (photon + z)


def delta_Z2_L_lepton(
    lepton: str = "e",
    s: float | None = None,
    c: float | None = None,
    mu2: float = MZ2,
    lam2: float = LAMBDA2_DEFAULT,
) -> float:
    """OS left-chirality wavefunction counterterm: delta_Z_2^L_ell = -Sigma_L^ell(m_ell^2).

    In the massless-lepton approximation (m_ell^2/M_V^2 << 1), the additional
    m_ell^2 * Sigma' correction to the OS wavefunction is neglected. For the
    R2.b row at Z-pole kinematics this is the standard treatment.
    """
    ml2 = ML[lepton] ** 2
    return -Sigma_L_lepton(ml2, lepton, s, c, mu2, lam2)


def delta_Z2_R_lepton(
    lepton: str = "e",
    s: float | None = None,
    c: float | None = None,
    mu2: float = MZ2,
    lam2: float = LAMBDA2_DEFAULT,
) -> float:
    """OS right-chirality wavefunction counterterm: delta_Z_2^R_ell = -Sigma_R^ell(m_ell^2)."""
    ml2 = ML[lepton] ** 2
    return -Sigma_R_lepton(ml2, lepton, s, c, mu2, lam2)


# ============================================================================
# Architecture-only: no register() function.
#
# This module is sibling-AI available via direct import but does NOT register
# with bank.REGISTRY. Bank-promotion to [P_structural] waits on a fresh-session
# pass after the R2 v3 sibling delivery validates the conventions encoded here
# by reproducing the structural kappa_l = 27/26 to within DFGRU noise.
# ============================================================================


def run_smoke() -> Dict[str, Any]:
    """Sanity smoke for the wrapper. Returns the chiral SE values + counterterms
    at standard Denner inputs for all three charged leptons."""
    s, c = _sw_cw_from_MW()
    out: Dict[str, Any] = {
        "convention": "Denner App.B Feynman gauge ksi=1 (arXiv:0709.1075)",
        "sin2_theta_W_OS": s * s,
        "lambda2_IR_regulator": LAMBDA2_DEFAULT,
        "mu2": MZ2,
        "honest_non_claims": [
            "ARCHITECTURE-ONLY (no register()); not bank-promoted.",
            "Conventions transcribed from Denner App.B; sibling-validation pending.",
            "Massless-lepton approximation in delta_Z_2^{L,R}; m_ell^2/M_V^2 corrections neglected.",
            "Photon-mass lambda^2 cancels in physical observables; individual values are lambda-dependent.",
        ],
        "leptons": {},
    }
    for lepton in ("e", "mu", "tau"):
        sL0 = Sigma_L_lepton(0.0, lepton, s, c)
        sR0 = Sigma_R_lepton(0.0, lepton, s, c)
        sL_ml2 = Sigma_L_lepton(ML[lepton] ** 2, lepton, s, c)
        sR_ml2 = Sigma_R_lepton(ML[lepton] ** 2, lepton, s, c)
        dZL = delta_Z2_L_lepton(lepton, s, c)
        dZR = delta_Z2_R_lepton(lepton, s, c)
        out["leptons"][lepton] = {
            "m_ell_GeV": ML[lepton],
            "Sigma_L_at_0": sL0,
            "Sigma_R_at_0": sR0,
            "Sigma_L_at_m_ell2": sL_ml2,
            "Sigma_R_at_m_ell2": sR_ml2,
            "delta_Z2_L": dZL,
            "delta_Z2_R": dZR,
        }
    return out


if __name__ == "__main__":
    import json
    print(json.dumps(run_smoke(), indent=2))
