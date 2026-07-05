"""APF-native BHM Lambda_2(s, M^2) and Lambda_3(s, M^2) Z-vertex scalar functions -- Tier-4.

R1 of the OS-W Gate A "native kappa_l" arc (Route 1). Implements the BHM
Z-vertex scalar form factors Lambda_2(s, M^2) and Lambda_3(s, M^2) used in the
Zll proper-vertex assembly, per the LEP Yellow Report "Precision Calculations
for the Z Resonance" (CERN 95-03 = arXiv:hep-ph/9709229, EWWGR.tex L6062), with
the explicit Feynman iepsilon prescription:

    w = M^2 / (s + i eps) ,

    Lambda_2(s, M^2) = -7/2 - 2 w - (2 w + 3) log(-w)
                       + 2 (1 + w)^2 [ Li_2(1 + 1/w) - pi^2 / 6 ] ,

    Lambda_3(s, M^2) = 5/6 - 2 w / 3
                       - (2 w + 1) / 3 * sqrt(1 - 4 w) * log(x)
                       + 2/3 * w (w + 2) * log(x)^2 ,
    with x = (sqrt(1 - 4 w) - 1) / (sqrt(1 - 4 w) + 1) .

SIGN CORRIGENDUM (v24.3.360, 2026-07-03) -- THE PUBLISHED FORMULA IS WRONG.
EWWGR.tex L6067-6072 (and the 1995 CERN-95-03 print edition, glyph-verified)
prints the single-log term with a PLUS sign. That printed closed form is
defective: (i) it carries an unphysical 1/s pole (Lambda_3_printed -> -8w/3
- 10/9 as s -> 0; no s-independent renormalization can produce a massless
pole in a weak form factor whose defining diagram class is finite there),
while the corrected form vanishes at s = 0 identically, parallel to the
validated Lambda_2; (ii) the corrected form equals the zero-momentum-
subtracted Denner generic, Lambda_3 = (1/3)[V_b^-(0,s,0,0,M,M) - V_b^-(0)]
with V_b^-(0) = 3 ln(mu^2/M^2) - 1/2 (Denner, Fortschr. Phys. 41 (1993) 307
= arXiv:0709.1075, hab6/haba3), to <= 5e-6 over spacelike AND timelike
grids incl. s = M_Z^2, where the printed form fails by O(1)-O(16) swings;
(iii) a from-scratch Passarino-Veltman evaluation of the SAME Yellow
Report's TOPAZ0-chapter F_3 combination (EWWGR.tex ~L7060-7105, an
independent group and formalism) matches the corrected form at quadrature
precision with the parameter-free coupling cross-ratio 23.993 vs the
predicted 24, and rejects the printed form at O(1) even granted a free
affine calibration. Note sqrt(1-4w)*log(x) is branch-EVEN (sqrt -> -sqrt
sends x -> 1/x in both log factors; log^2 even), so this is a genuine
function difference, not a branch convention. The correction collapses the
ACFW published-one-loop benchmark gap from +0.0194 M_H-flat to <= 1.0e-4 at
all four Table-II Higgs masses (see the BSY validator module).

PROVENANCE SETTLED (2026-07-03, same landing; both originals acquired into
the Lit Review and read): the sign error is ORIGINAL TO CERN-95-03. BHM
1986 (Boehm-Hollik-Spiesberger, Fortschr. Phys. 34 (1986) 687, eq. B.5
region p. 748) prints the CORRECT function -- their log argument is the
INVERSE of EWWGR's x, i.e. ln[(sqrt(1-4w)+1)/(sqrt(1-4w)-1)] = -ln(x), so
their '+' single-log term equals the corrected '-' in EWWGR's convention;
they also state Lambda_3(0, M) = 0 explicitly (the boundary property the
analytic leg demanded). Hollik DESY 88-188 (= Fortschr. Phys. 38 (1990)
165), Appendix C eq. (C.5) p. 105, prints the timelike arctan form -- 
machine-verified IDENTICAL to the corrected function at float precision
(legs 4-5 of the corrigendum check below). THE MECHANISM: when the report
recast the formula into x = (sqrt(1-4w)-1)/(sqrt(1-4w)+1), the even log^2
term survived the inversion unchanged while the odd single-log term needed
a sign flip it never received -- a convention-recast transcription slip,
which is exactly the asymmetric error the corrigendum reverses. The
corrected function is derived, not fitted (ACFW enters only as the gate). Witnesses: The Turning/zll_defect_hunt_2026-07-03/ (three walker
stages + the auditor's TOPAZ0 script, pinned offline); walker + fresh-
context hostile audit SOUND-WITH-CORRECTIONS 0.97. LESSON OF RECORD: the
mpmath dps=40 anchor validated TRANSCRIPTION of the printed formula, not
its physics -- the published-benchmark instrument class (ACFW, .358) is
what caught this.

These combine with the SM gauge couplings to build F_L^f, F_V^Zf, F_A^Zf -- the
proper-vertex form factors entering the on-shell effective leptonic mixing
angle through the renormalized Zll coupling. At s = M_Z^2 with internal mass
M = M_W (the W-W-Z triangle), Lambda_2 has an absorptive part from the
M_W-loop branch cut while Lambda_3 is real (the 2 M_W threshold sits at
s = 4 M_W^2 > M_Z^2 -- closed at the Z pole). At s = M_Z^2 with internal
M = M_Z (the Z-Z exchange triangle), Lambda_2 is complex.

R1 closes the closed-form route: the BHM analytic expressions are implemented
in pure Python with a self-contained dilogarithm Li_2 (series + reflection)
and the iepsilon prescription threaded through cmath. The NATIVE composition
from the timelike C-toolkit (R0 scalar C0 v24.3.103 + R0b rank-1 C1/C2
v24.3.104 + R0c rank-2 Cij v24.3.105) per the Denner generic-vertex form
factors is the natural cross-anchor and remains OPEN here -- the next rung
(R1b) wires the timelike Cij into the haba3 V_a / V_b decomposition to
reproduce Lambda_2 and Lambda_3 the second way.

Self-validation (no fitted/measured target)
-------------------------------------------
  * Li_2 reference values: Li_2(1) = pi^2 / 6, Li_2(-1) = -pi^2 / 12,
    Li_2(1/2) = pi^2 / 12 - (ln 2)^2 / 2, Li_2(0) = 0.
  * Li_2 Abel identity:
        Li_2(z) + Li_2(1 - z) + log(z) log(1 - z) = pi^2 / 6
    holds on complex test points.
  * spacelike reality: Lambda_2(s, M^2), Lambda_3(s, M^2) are real
    (|Im| < epsilon_real) for s < 0.
  * physical-kinematics reference values (independently computed via mpmath
    at dps=40 and hardcoded here): match the pure-Python implementation to
    relative 1e-12.

Honest scope
------------
The BHM Lambda_2 / Lambda_3 scalar functions only (closed-form route). The
NATIVE composition from the Denner generic vertex form factors V_a / V_b
using the timelike C-toolkit (R1b cross-anchor), the renormalized Zll
proper vertex with counterterms (R2), the bosonic Delta kappa contribution
(R3), the light-fermion / Delta alpha contribution (R4), and the assembled
kappa_l value (R5) remain OPEN. No kappa_l / Delta r_rem / M_W value is
produced; DIZET stays the publishable OS-W closure.

Status
------
- Export_native_bhm_lambda_closed_form_evaluated  = 1   (NEW here)
- Export_native_bhm_lambda_via_C_toolkit          = 0   (OPEN, R1b)
- Export_native_zll_renormalized_vertex           = 0   (OPEN, R2)
- Export_native_kappa_l_evaluated                 = 0   (OPEN, R5)
- Export_OSW_APF_internal_delta_r_rem_evaluated   = 0   (OPEN, unchanged)
"""
from __future__ import annotations

import math
import cmath
from typing import Any, Dict

from apf.apf_utils import check, _result
from apf.w_trace_pv_scalar_integral_substrate import MW2, MZ2

_DEFAULT_EPS = 1e-14
PI = math.pi
PI2_OVER_6 = PI * PI / 6.0


def Li2(z) -> complex:
    """Principal-branch dilogarithm Li_2(z) = sum_{n=1}^inf z^n / n^2.

    Strategy:
      |z| > 1                : reflection  Li_2(z) = -Li_2(1/z) - pi^2/6 - (1/2) log(-z)^2
      |z| <= 1, Re z > 1/2   : reflection  Li_2(z) = pi^2/6 - log(z) log(1-z) - Li_2(1-z)
      |z| <= 1, Re z <= 1/2  : power series (converges quickly there)
    """
    z = complex(z)
    if abs(z) < 1e-15:
        return 0.0 + 0.0j
    if abs(z - 1.0) < 1e-15:
        return PI2_OVER_6 + 0.0j
    if abs(z + 1.0) < 1e-15:
        return -PI * PI / 12.0 + 0.0j
    if abs(z) > 1.0:
        return -Li2(1.0 / z) - PI2_OVER_6 - 0.5 * cmath.log(-z) ** 2
    if z.real > 0.5:
        return PI2_OVER_6 - cmath.log(z) * cmath.log(1.0 - z) - Li2(1.0 - z)
    # power series; converges geometrically for |z| <= 1/2
    result = 0.0 + 0.0j
    term = z
    for n in range(1, 200):
        contribution = term / (n * n)
        result += contribution
        if abs(contribution) < 1e-18:
            break
        term *= z
    return result


def Lambda_2(s: float, M2: float, eps: float = _DEFAULT_EPS) -> complex:
    """BHM Lambda_2(s, M^2) with Feynman iepsilon prescription w = M^2/(s + i eps)."""
    w = M2 / complex(s, eps)
    return (-3.5 - 2.0 * w - (2.0 * w + 3.0) * cmath.log(-w)
            + 2.0 * (1.0 + w) ** 2 * (Li2(1.0 + 1.0 / w) - PI2_OVER_6))


def Lambda_3(s: float, M2: float, eps: float = _DEFAULT_EPS) -> complex:
    """Lambda_3(s, M^2), SIGN-CORRECTED (v24.3.360) vs the printed EWWGR form.

    Feynman iepsilon prescription w = M^2/(s + i eps). The single-log term
    carries a MINUS sign; EWWGR.tex L6067-6072 prints '+', which is a source
    defect (see the module-docstring corrigendum). Corrected form verified
    three independent ways; equals (1/3)[V_b^-(s) - V_b^-(0)] of the Denner
    generics (machine-checked in check_T_w_trace_pv_lambda3_sign_corrigendum
    _denner_anchor below).
    """
    w = M2 / complex(s, eps)
    sq = cmath.sqrt(1.0 - 4.0 * w)
    x = (sq - 1.0) / (sq + 1.0)
    lx = cmath.log(x)
    return (5.0 / 6.0 - 2.0 * w / 3.0
            - (2.0 * w + 1.0) / 3.0 * sq * lx
            + 2.0 / 3.0 * w * (w + 2.0) * lx * lx)


def Lambda_3_printed_defective(s: float, M2: float,
                               eps: float = _DEFAULT_EPS) -> complex:
    """The DEFECTIVE closed form as printed in EWWGR.tex L6067-6072 ('+' on
    the single-log term). Retained ONLY as the negative control for the
    corrigendum check below; never use in physics composition."""
    w = M2 / complex(s, eps)
    sq = cmath.sqrt(1.0 - 4.0 * w)
    x = (sq - 1.0) / (sq + 1.0)
    lx = cmath.log(x)
    return (5.0 / 6.0 - 2.0 * w / 3.0
            + (2.0 * w + 1.0) / 3.0 * sq * lx
            + 2.0 / 3.0 * w * (w + 2.0) * lx * lx)


# Reference values computed independently via mpmath at dps=40 (Li_2 = mp.polylog(2, .)),
# with the SAME iepsilon convention w = M^2/(s + i eps). Hardcoded to give a
# tight bank-side anchor without taking a runtime mpmath dependency.
_REF_VALUES: Dict[str, complex] = {
    # Lambda_2(M_Z^2, M_W^2) -- ν/W/W triangle at the Z pole
    "L2_MZ2_MW2":  complex( 1.1805183681875155,  2.1068900271751924),
    # Lambda_3(M_Z^2, M_W^2) -- real (2 M_W threshold closed at s = M_Z^2)
    # (re-anchored v24.3.360 to the SIGN-CORRECTED form; the pre-.360 value
    #  -3.2679780980165249 anchored the defective printed formula)
    "L3_MZ2_MW2":  complex(-0.28695288568781208,  0.0),
    # Lambda_2(M_Z^2, M_Z^2) -- Z exchange
    "L2_MZ2_MZ2":  complex( 1.0797362673929057,  1.7127254544798509),
    # Lambda_2(-M_Z^2, M_W^2) -- spacelike, must be real
    "L2_neg_MZ2_MW2": complex(-1.7719799883977947, 0.0),
    # Lambda_3(-M_Z^2, M_W^2) -- spacelike, must be real
    # (re-anchored v24.3.360; pre-.360 defective-formula value +1.0147076906274485)
    "L3_neg_MZ2_MW2": complex( 0.20642869687946931, 0.0),
}


EXPORT_FLAGS: Dict[str, int] = {
    "Export_native_bhm_lambda_closed_form_evaluated": 1,
    "Export_native_bhm_lambda_via_C_toolkit": 0,
    "Export_native_zll_renormalized_vertex": 0,
    "Export_native_kappa_l_evaluated": 0,
    "Export_OSW_APF_internal_delta_r_rem_evaluated": 0,
}


# ===========================================================================
# checks
# ===========================================================================
def check_T_w_trace_pv_lambda_bhm_Li2_reference_values_P() -> Dict[str, Any]:
    """T: Li_2 reproduces classical reference values [P]."""
    mx = 0.0
    cases = [
        (1.0,  PI2_OVER_6),
        (-1.0, -PI * PI / 12.0),
        (0.5,  PI * PI / 12.0 - 0.5 * math.log(2.0) ** 2),
        (0.0,  0.0),
    ]
    for z, ref in cases:
        v = Li2(z)
        mx = max(mx, abs(v.real - ref), abs(v.imag))
    check(mx < 1e-13, f"Li_2 reference-value max abs err {mx:.2e}")
    return _result(
        name=("T_w_trace_pv_lambda_bhm_Li2_reference_values: "
              "Li_2 reproduces Li_2(1) = pi^2/6, Li_2(-1) = -pi^2/12, "
              "Li_2(1/2) = pi^2/12 - (ln 2)^2/2, Li_2(0) = 0 [P]"),
        tier=4, epistemic="P",
        summary=(
            f"The pure-Python principal-branch dilogarithm Li_2 reproduces four "
            f"classical reference values (Li_2(1) = pi^2/6, Li_2(-1) = -pi^2/12, "
            f"Li_2(1/2) = pi^2/12 - (ln 2)^2/2, Li_2(0) = 0) to max abs err "
            f"{mx:.1e} -- validates the series + reflection implementation."
        ),
        key_result=f"Li_2 reference values match (max abs err {mx:.1e}). [P]",
        dependencies=[],
        artifacts={"max_abs_err": mx},
    )


def check_T_w_trace_pv_lambda_bhm_Li2_abel_identity_P() -> Dict[str, Any]:
    """T: Li_2 satisfies the Abel identity Li_2(z) + Li_2(1-z) + log(z) log(1-z) = pi^2/6 [P]."""
    mx = 0.0
    # Test points off the Li_2 cut [1, infty) AND off (-infty, 0] (so 1 - z is also off the cut)
    test_pts = [
        complex(0.3,  0.0),
        complex(0.7,  0.0),
        complex(0.4,  0.6),
        complex(-0.2, 1.1),
        complex(0.8, -0.3),
        complex(0.1,  0.4),
    ]
    for z in test_pts:
        lhs = Li2(z) + Li2(1.0 - z) + cmath.log(z) * cmath.log(1.0 - z)
        mx = max(mx, abs(lhs - PI2_OVER_6))
    check(mx < 1e-12, f"Li_2 Abel-identity max abs err {mx:.2e}")
    return _result(
        name=("T_w_trace_pv_lambda_bhm_Li2_abel_identity: "
              "Li_2(z) + Li_2(1-z) + log(z) log(1-z) = pi^2/6 on complex test points [P]"),
        tier=4, epistemic="P",
        summary=(
            f"The pure-Python Li_2 satisfies the Abel identity "
            f"Li_2(z) + Li_2(1 - z) + log(z) log(1 - z) = pi^2 / 6 on six "
            f"complex test points (real + complex, |z| < 1 + |z| > 1) to max "
            f"abs err {mx:.1e} -- a target-free validation across the full "
            f"branch structure of the implementation."
        ),
        key_result=f"Li_2 Abel identity holds (max abs err {mx:.1e}). [P]",
        dependencies=["T_w_trace_pv_lambda_bhm_Li2_reference_values"],
        artifacts={"max_abs_err": mx},
    )


def check_T_w_trace_pv_lambda_bhm_spacelike_real_P() -> Dict[str, Any]:
    """T: Lambda_2(s, M^2), Lambda_3(s, M^2) real for s < 0 (spacelike) [P]."""
    mx = 0.0
    for s, M2 in [(-MZ2, MW2), (-MZ2, MZ2), (-2.0 * MZ2, MW2), (-5000.0, 1000.0)]:
        L2 = Lambda_2(s, M2)
        L3 = Lambda_3(s, M2)
        mx = max(mx, abs(L2.imag), abs(L3.imag))
    check(mx < 1e-10, f"spacelike Lambda max abs Im {mx:.2e}")
    return _result(
        name=("T_w_trace_pv_lambda_bhm_spacelike_real: "
              "Lambda_2, Lambda_3 are real for spacelike s < 0 [P]"),
        tier=4, epistemic="P",
        summary=(
            f"For spacelike external invariant s < 0 (where the s-channel "
            f"branch cut is closed) the absorptive parts of Lambda_2, Lambda_3 "
            f"vanish to max |Im| {mx:.1e} across four kinematic test points -- "
            f"confirms the correct analytic structure of the Feynman iepsilon "
            f"prescription w = M^2 / (s + i eps)."
        ),
        key_result=f"Lambda_2, Lambda_3 real for s<0 (max |Im| {mx:.1e}). [P]",
        dependencies=["T_w_trace_pv_lambda_bhm_Li2_abel_identity"],
        artifacts={"max_abs_im": mx},
    )


def check_T_w_trace_pv_lambda_bhm_physical_values_P() -> Dict[str, Any]:
    """T: Lambda_2, Lambda_3 at physical kinematics match mpmath-computed reference [P]."""
    mx = 0.0
    pairs = [
        ((MZ2,  MW2), _REF_VALUES["L2_MZ2_MW2"],    Lambda_2),
        ((MZ2,  MW2), _REF_VALUES["L3_MZ2_MW2"],    Lambda_3),
        ((MZ2,  MZ2), _REF_VALUES["L2_MZ2_MZ2"],    Lambda_2),
        ((-MZ2, MW2), _REF_VALUES["L2_neg_MZ2_MW2"], Lambda_2),
        ((-MZ2, MW2), _REF_VALUES["L3_neg_MZ2_MW2"], Lambda_3),
    ]
    for (s, M2), ref, fn in pairs:
        v = fn(s, M2)
        denom = max(1.0, abs(ref))
        mx = max(mx, abs(v - ref) / denom)
    check(mx < 1e-12, f"Lambda physical-kinematics max rel err vs mpmath {mx:.2e}")
    return _result(
        name=("T_w_trace_pv_lambda_bhm_physical_values: "
              "Lambda_2, Lambda_3 at physical kinematics match mpmath dps=40 [P]"),
        tier=4, epistemic="P",
        summary=(
            f"At physical kinematics (s = M_Z^2 with M = M_W and M = M_Z; "
            f"s = -M_Z^2 spacelike) the pure-Python implementation matches "
            f"an independent high-precision mpmath computation (Li_2 = "
            f"polylog(2, .), dps = 40, w = M^2 / (s + i eps)) to max rel err "
            f"{mx:.1e} -- a tight machine-level reference anchor on five "
            f"kinematic points spanning timelike + spacelike."
        ),
        key_result=f"Lambda_2, Lambda_3 == mpmath dps=40 reference (rel err {mx:.1e}). [P]",
        dependencies=["T_w_trace_pv_lambda_bhm_spacelike_real"],
        artifacts={"max_rel_err": mx, "reference_values": dict(_REF_VALUES)},
    )


def check_T_w_trace_pv_lambda_bhm_subgate_partial_P() -> Dict[str, Any]:
    """T: BHM Lambda closed-form done; native C-toolkit route + Zll vertex OPEN [P_structural]."""
    check(EXPORT_FLAGS["Export_native_bhm_lambda_closed_form_evaluated"] == 1,
          "Lambda closed-form flag must be 1")
    check(EXPORT_FLAGS["Export_native_bhm_lambda_via_C_toolkit"] == 0,
          "Lambda via C-toolkit (R1b) must remain OPEN")
    check(EXPORT_FLAGS["Export_native_zll_renormalized_vertex"] == 0,
          "renormalized Zll vertex (R2) must remain OPEN")
    check(EXPORT_FLAGS["Export_native_kappa_l_evaluated"] == 0,
          "no kappa_l evaluated by this rung")
    check(EXPORT_FLAGS["Export_OSW_APF_internal_delta_r_rem_evaluated"] == 0,
          "no Delta r_rem evaluated by this rung")
    return _result(
        name=("T_w_trace_pv_lambda_bhm_subgate_partial: "
              "BHM Lambda_2, Lambda_3 closed forms native; C-toolkit route + Zll vertex OPEN [P_structural]"),
        tier=4, epistemic="P_structural_partial",
        summary=(
            "The BHM Z-vertex scalar functions Lambda_2(s, M^2) and "
            "Lambda_3(s, M^2) (EWWGR L6062 / hep-ph/9709229) are now native "
            "via the closed-form route: pure-Python implementation with a "
            "self-contained Li_2 + reflection structure, Feynman iepsilon "
            "prescription w = M^2 / (s + i eps), and a tight mpmath-anchored "
            "physical-kinematics reference. Together with the three-point "
            "complex tensor basis (R0 scalar + R0b rank-1 + R0c rank-2) this "
            "completes the closed-form vertex-function layer needed by the "
            "renormalized Zll vertex assembly. Still OPEN toward kappa_l: the "
            "native composition of Lambda_2, Lambda_3 from the timelike "
            "C-toolkit through the Denner haba3 generic V_a / V_b form "
            "factors (R1b cross-anchor); the renormalized Zll proper vertex "
            "with counterterms (R2, gate: UV / WWZ cancellation); the "
            "bosonic Delta kappa contribution (R3); the light-fermion / "
            "Delta alpha contribution (R4); and the assembled native "
            "kappa_l = 0.036808 / sin^2 theta_eff = 0.23155 (R5). DIZET "
            "stays the publishable OS-W closure."
        ),
        key_result="BHM Lambda closed forms native; C-toolkit route + Zll vertex OPEN. [P_structural]",
        dependencies=["T_w_trace_pv_lambda_bhm_physical_values"],
        cross_refs=["T_w_trace_pv_timelike_c0_subgate_partial",
                    "T_w_trace_pv_timelike_c1_c2_subgate_partial",
                    "T_w_trace_pv_timelike_cij_rank2_subgate_partial"],
        artifacts={"export_flags": dict(EXPORT_FLAGS)},
    )


# ===========================================================================
# v24.3.360 -- the sign-corrigendum certification (Denner anchor + s->0)
# ===========================================================================
def _denner_pv_pieces(s_val: float, M2: float, n: int = 20000):
    """From-scratch 1D-reduced Feynman-parameter PV finite parts (mu^2 = MU2).

    Independent of the closed forms under test; midpoint mesh n = 2e4 gives
    ~1e-5 accuracy -- five orders below the O(1)-O(16) discriminating signal.
    Valid for s < 4 M^2 (includes the physical s = M_Z^2). Full-precision
    version (n = 2.5e5) pinned offline: The Turning/zll_defect_hunt_2026-07-03/
    stage2_denner_route_proof_witness.py.
    """
    from apf.w_trace_pv_scalar_integral_substrate import MU2 as _MU2
    h = 1.0 / n
    # B0_fin(s, M, M)
    b0_sMM = -h * sum(
        math.log((M2 - ((i + 0.5) * h) * (1.0 - (i + 0.5) * h) * s_val) / _MU2)
        for i in range(n))
    b0_00M = 1.0 - math.log(M2 / _MU2)
    # C0(0,s,0; 0,M,M): inner x3-integral analytic
    acc = 0.0
    for i in range(n):
        x2 = (i + 0.5) * h
        a = x2 * M2
        b = M2 - x2 * s_val
        acc += math.log1p(b * (1.0 - x2) / a) / b
    c0 = -acc * h
    return b0_sMM, b0_00M, c0


def _V_b_minus(s_val: float, M2: float, n: int = 20000) -> float:
    """Denner V_b^-(0,s,0,0,M,M) (arXiv:0709.1075 hab6/haba3, massless
    external fermions, equal internal boson masses), from first-principles
    PV pieces."""
    b0_sMM, b0_00M, c0 = _denner_pv_pieces(s_val, M2, n)
    return (2.0 * (2.0 * M2 + M2 * M2 / s_val) * c0
            - (1.0 + 2.0 * M2 / s_val) * b0_sMM
            + 2.0 * (2.0 + M2 / s_val) * b0_00M)


def check_T_w_trace_pv_lambda3_sign_corrigendum_denner_anchor_P() -> Dict[str, Any]:
    """T: the v24.3.360 Lambda_3 sign corrigendum is certified against the
    Denner generic V_b^- (independent source) + the s->0 boundary property;
    the printed EWWGR form fails both as the pinned negative control;
    provenance SETTLED against both originals [P].

    Five in-check legs (the TOPAZ0 sixth leg is pinned offline):
      (1) s->0: Lambda_3_corrected(s->0) -> 0 (like the validated Lambda_2);
          the printed form diverges as -8w/3 - 10/9 (negative control; the
          -10/9 constant is the audit-corrected value).
      (2) Denner anchor: Lambda_3_corr(s) = (1/3)[V_b^-(s) - V_b^-(0)] with
          V_b^-(0) = 3 ln(mu^2/M^2) - 1/2, constant over a spacelike AND
          timelike grid incl. s = M_Z^2; the printed form fails the same
          identity with O(1) swings (negative control).
      (3) The physical point pins the corrected value -0.2869528856878121
          (mpmath dps=40).
      (4) PROVENANCE (settled 2026-07-03): BHM 1986 p. 748 -- the ORIGIN
          paper's spacelike closed form (log argument inverted vs EWWGR's
          x) equals the corrected function at 1e-12; BHM also states
          Lambda_3(0, M) = 0 explicitly.
      (5) PROVENANCE: Hollik DESY 88-188 eq (C.5) p. 105 -- the timelike
          arctan form equals the corrected function at 1e-12.
      Both originals correct => the sign error is ORIGINAL TO CERN-95-03
      (a convention-recast slip: the even log^2 term survived the x ->
      inverse-argument rewrite, the odd single-log term lost its flip).
    """
    from apf.w_trace_pv_scalar_integral_substrate import MU2 as _MU2
    M2 = MW2

    # --- leg 1: s -> 0 boundary ---
    s_tiny = -MZ2 / 7766.6
    w_tiny = M2 / s_tiny
    l3c_0 = Lambda_3(s_tiny, M2)
    l3p_0 = Lambda_3_printed_defective(s_tiny, M2)
    check(abs(l3c_0) < 5e-3,
          f"corrected Lambda_3 must vanish as s->0: |{l3c_0}|")
    div_pred = -8.0 * w_tiny / 3.0 - 10.0 / 9.0   # audit-corrected constant
    check(abs(l3p_0.real - div_pred) < abs(div_pred) * 1e-3,
          f"printed-form negative control: expected divergence {div_pred:.3f}, "
          f"got {l3p_0.real:.3f}")

    # --- leg 2: Denner anchor over the grid ---
    const_b = math.log(_MU2 / M2) - 1.0 / 6.0   # (1/3) V_b^-(0)
    grid = (-4.0 * MZ2, -MZ2, 0.5 * MZ2, MZ2)
    dev_corr, resid_printed = [], []
    for s_val in grid:
        vb3 = _V_b_minus(s_val, M2) / 3.0
        dev_corr.append(abs(vb3 - Lambda_3(s_val, M2).real - const_b))
        resid_printed.append(vb3 - Lambda_3_printed_defective(s_val, M2).real)
    check(max(dev_corr) < 5e-4,
          f"Denner anchor failed for corrected Lambda_3: max dev {max(dev_corr):.2e}")
    swing = max(resid_printed) - min(resid_printed)
    check(swing > 1.0,
          f"printed-form negative control unexpectedly passes: swing {swing:.3f}")

    # --- leg 3: physical-point pin ---
    l3_phys = Lambda_3(MZ2, M2)
    check(abs(l3_phys.real - (-0.28695288568781208)) < 1e-12,
          f"physical-point pin drifted: {l3_phys.real}")
    check(abs(l3_phys.imag) < 1e-12,
          "Lambda_3(M_Z^2, M_W^2) must be real (2 M_W threshold closed)")

    # --- legs 4+5 (provenance, settled 2026-07-03): the ORIGINALS are correct ---
    # Leg 4: BHM 1986 p. 748 spacelike form -- log argument INVERTED vs EWWGR's
    # x, so BHM's '+' single-log = the corrected '-' in x-convention.
    dev_bhm = 0.0
    for s_sp in (-4.0 * MZ2, -MZ2, -0.25 * MZ2):
        w = M2 / s_sp
        sq = math.sqrt(1.0 - 4.0 * w)                  # real, spacelike
        ln_inv = math.log((sq + 1.0) / (sq - 1.0))     # BHM's log argument
        bhm = (5.0 / 6.0 - 2.0 * w / 3.0
               + (2.0 * w + 1.0) / 3.0 * sq * ln_inv
               + 2.0 / 3.0 * w * (w + 2.0) * ln_inv * ln_inv)
        dev_bhm = max(dev_bhm, abs(bhm - Lambda_3(s_sp, M2).real))
    check(dev_bhm < 1e-12,
          f"BHM 1986 (B.5) spacelike form != corrected Lambda_3: {dev_bhm:.2e}")
    # Leg 5: Hollik DESY 88-188 eq (C.5) timelike arctan form (0 < s < 4M^2).
    dev_hol = 0.0
    for s_tl in (0.5 * MZ2, MZ2, 2.0 * MZ2):
        w = M2 / s_tl
        r = math.sqrt(4.0 * w - 1.0)
        at = math.atan(1.0 / r)
        hol = (5.0 / 6.0 - 2.0 * w / 3.0
               + (2.0 / 3.0) * (2.0 * w + 1.0) * r * at
               - (8.0 / 3.0) * w * (w + 2.0) * at * at)
        dev_hol = max(dev_hol, abs(hol - Lambda_3(s_tl, M2).real))
    check(dev_hol < 1e-12,
          f"Hollik (C.5) arctan form != corrected Lambda_3: {dev_hol:.2e}")

    return _result(
        name=("T_w_trace_pv_lambda3_sign_corrigendum_denner_anchor: the "
              "corrected Lambda_3 equals (1/3)[V_b^- - V_b^-(0)] (Denner) and "
              "vanishes at s=0; the printed EWWGR form fails both (pinned "
              "negative control) [P]"),
        tier=4, epistemic="P",
        summary=(
            f"The v24.3.360 sign corrigendum certified in-check: (1) s->0 -- "
            f"corrected Lambda_3({s_tiny/MZ2:.2e}*M_Z^2) = {abs(l3c_0):.2e} "
            f"(vanishes, like the validated Lambda_2), while the printed form "
            f"tracks its unphysical divergence -8w/3 - 10/9 = {div_pred:.1f} "
            f"(negative control); (2) the Denner anchor -- Lambda_3_corr(s) = "
            f"(1/3)[V_b^-(0,s,0,0,M_W,M_W) - V_b^-(0)] with V_b^-(0) = "
            f"3 ln(mu^2/M_W^2) - 1/2, holds over spacelike AND timelike grid "
            f"points incl. s = M_Z^2 to max dev {max(dev_corr):.1e} (from-"
            f"scratch 1D-reduced PV integrals, mesh 2e4), while the printed "
            f"form fails the same identity with an O({swing:.0f}) swing; "
            f"(3) the physical point pins Lambda_3(M_Z^2, M_W^2) = "
            f"{l3_phys.real:.13f} (mpmath dps=40 anchored); "
            f"(4)+(5) PROVENANCE SETTLED against both acquired originals -- "
            f"BHM 1986 p. 748 spacelike form (inverse log argument; max dev "
            f"{dev_bhm:.1e}) and Hollik DESY 88-188 eq C.5 timelike arctan "
            f"form (max dev {dev_hol:.1e}) BOTH equal the corrected function "
            f"at machine precision: the sign error is ORIGINAL TO CERN-95-03, "
            f"a convention-recast slip (BHM's ln[(sq+1)/(sq-1)] = -ln x; the "
            f"even log^2 term survived the rewrite, the odd single-log term "
            f"lost its flip). The formalism-independent TOPAZ0 leg (ratio-24 "
            f"coupling coherence) is pinned offline at The Turning/"
            f"zll_defect_hunt_2026-07-03/audit_topaz0_pv_independent_witness.py. "
            f"This check is the bank-permanent record that the PUBLISHED "
            f"CERN-95-03 closed form is defective and the corrected form is "
            f"derived, not fitted."
        ),
        key_result=(
            f"Lambda_3 sign corrigendum certified: Denner anchor holds at "
            f"{max(dev_corr):.1e}; printed form fails at O({swing:.0f}); "
            f"s->0 + physical pin green; PROVENANCE SETTLED -- both originals "
            f"(BHM 1986, Hollik 1990) correct at 1e-12, the error is original "
            f"to CERN-95-03. [P]"
        ),
        dependencies=["T_w_trace_pv_lambda_bhm_physical_values"],
        cross_refs=["T_w_trace_kappa_l_ACFW_published_one_loop_benchmark",
                    "T_w_trace_pv_ewwgr_bare_reference_values"],
        artifacts={
            "L3_corrected_MZ2_MW2": l3_phys.real,
            "L3_printed_defective_MZ2_MW2": -3.2679780980165249,
            "denner_anchor_max_dev": max(dev_corr),
            "printed_negative_control_swing": swing,
            "s_to_0_corrected": abs(l3c_0),
            "s_to_0_printed_divergence_predicted": div_pred,
            "topaz0_leg": "pinned offline (audit_topaz0_pv_independent_witness.py)",
            "provenance": ("SETTLED 2026-07-03: BHM 1986 + Hollik DESY 88-188 "
                           "both CORRECT at machine precision (legs 4-5); the "
                           "sign error is ORIGINAL TO CERN-95-03 "
                           "(convention-recast slip)"),
            "bhm_1986_form_max_dev": dev_bhm,
            "hollik_C5_form_max_dev": dev_hol,
        },
    )


_CHECKS = {
    "T_w_trace_pv_lambda3_sign_corrigendum_denner_anchor":
        check_T_w_trace_pv_lambda3_sign_corrigendum_denner_anchor_P,
    "T_w_trace_pv_lambda_bhm_Li2_reference_values": check_T_w_trace_pv_lambda_bhm_Li2_reference_values_P,
    "T_w_trace_pv_lambda_bhm_Li2_abel_identity":   check_T_w_trace_pv_lambda_bhm_Li2_abel_identity_P,
    "T_w_trace_pv_lambda_bhm_spacelike_real":      check_T_w_trace_pv_lambda_bhm_spacelike_real_P,
    "T_w_trace_pv_lambda_bhm_physical_values":     check_T_w_trace_pv_lambda_bhm_physical_values_P,
    "T_w_trace_pv_lambda_bhm_subgate_partial":     check_T_w_trace_pv_lambda_bhm_subgate_partial_P,
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
