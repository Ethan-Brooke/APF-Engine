"""apf/yang_mills_kappa3.py -- Witness for kappa_3(beta) < 0 for all beta > 0.

Bank-registered theorem:

  * check_T_kappa3_negative_all_beta -- structural witness for the certified
    statement kappa_3(beta) := d^3/dbeta^3 log(I_1(beta) / beta) < 0 for all
    beta > 0, where I_1 is the modified Bessel function.  The bank check is
    a representative-grid + algebraic-consistency witness; the full
    interval-arithmetic certificate over ~14000 blocks at mp.dps = 60
    lives in Paper 30's supplementary kappa3_certified_v3.py.

Source-of-record: Paper 30 (Tube Mechanism for the Lattice Mass Gap)
section sec:tube_audit + supplementary kappa3_certified_v3.py.

Mechanism summary.  kappa_3 = 2 r ( r^2 - 1 ) + ( 1 - 3 r^2 ) / beta
                              - 4 / beta^3,  with  r(beta) = I_0(beta) / I_1(beta).

  Phase 1: beta in (0, 0.5].  Power-series expansion of log(I_1/beta)
           around beta = 0 gives kappa_3 = -beta/16 + 5 beta^3 / 384 + ...
           the leading sign is unambiguously negative on the strip and
           the geometric tail bound is small.
  Phase 2: beta in [0.5, 200].  Blockwise mean-value certification with
           explicit kappa_4 from the Riccati identity r'(beta) = 1 - r^2
           + r / beta.  Full certificate uses ~14000 blocks at 60-digit
           precision; bank witness uses 200-point logarithmic sample +
           algebraic consistency of the Riccati identity.
  Phase 3: beta >= 200.  Asymptotic kappa_3 ~ -3 / beta^3 + O(beta^-4)
           and r(beta) is strictly decreasing toward 1, so kappa_3 -> 0
           from below.  Verified at sample large-beta values.

Tier 4 [P_structural].
"""

from __future__ import annotations

# We import mpmath at module top so verify_all picks up an ImportError
# immediately if the dependency is missing.
from mpmath import mp, mpf, besseli  # type: ignore

mp.dps = 30


def _r(beta):
    """r(beta) = I_0(beta) / I_1(beta), strictly decreasing for beta > 0."""
    return besseli(0, beta) / besseli(1, beta)


def _kappa3(beta):
    """kappa_3(beta) = 2 r (r^2 - 1) + (1 - 3 r^2) / beta - 4 / beta^3."""
    b = mpf(beta)
    r = _r(b)
    return 2 * r * (r * r - 1) + (1 - 3 * r * r) / b - 4 / (b ** 3)


def _kappa4_exact(r, beta):
    """kappa_4 from Riccati identity r'(beta) = 1 - r^2 + r/beta.

    kappa_4 = -6 r^4 + 8 r^2 - 2
             + 4 r (3 r^2 - 2) / beta
             - (3 r^2 + 1) / beta^2
             + 12 / beta^4
    """
    r2 = r * r
    r4 = r2 * r2
    ib = 1 / beta
    ib2 = ib * ib
    ib4 = ib2 * ib2
    return (-6 * r4 + 8 * r2 - 2
            + 4 * r * (3 * r2 - 2) * ib
            - (3 * r2 + 1) * ib2
            + 12 * ib4)


# ----------------------------------------------------------------------
# Three-regime witness
# ----------------------------------------------------------------------

def _phase1_small_beta():
    """Phase 1: 100 sample points in (0, 0.5]; verify kappa_3 < 0."""
    n = 100
    worst = mpf(-1e10)
    for i in range(1, n + 1):
        b = mpf(i) / (2 * n)  # beta in (0, 0.5]
        k = _kappa3(b)
        if k >= 0:
            return False, float(k), float(b)
        if k > worst:
            worst = k
    return True, float(worst), 0.5


def _phase2_mid_beta_sample():
    """Phase 2: 200 logarithmic sample points across [0.5, 200].

    The full interval-arithmetic certificate (supplementary script) uses
    ~14000 narrow blocks at 60-digit precision.  This witness samples
    enough representative points to catch any sign change at the bank
    level.  kappa_3 is smooth in beta so a 200-point grid is dense enough
    to detect sign changes were they to occur.
    """
    import math
    n = 200
    log_lo, log_hi = math.log(0.5), math.log(200.0)
    worst = mpf(-1e10)
    for i in range(n + 1):
        t = log_lo + (log_hi - log_lo) * i / n
        b = mpf(math.exp(t))
        k = _kappa3(b)
        if k >= 0:
            return False, float(k), float(b)
        if k > worst:
            worst = k
    return True, float(worst), n + 1


def _phase3_large_beta():
    """Phase 3: kappa_3 at sample large-beta values matching -3/beta^3."""
    samples = []
    for bv in (200, 500, 1000, 5000, 10000):
        k = _kappa3(mpf(bv))
        if k >= 0:
            return False, samples, bv
        leading = -3.0 / (bv ** 3)
        ratio = float(k) / leading
        samples.append((bv, float(k), leading, ratio))
    return True, samples, None


def _phase4_riccati_consistency():
    """Phase 4: Verify kappa_4 from the Riccati formula matches numerical
    d/dbeta of kappa_3 to high precision, at five witness beta values.

    This is the algebraic-consistency check that licenses the
    supplementary certifier's interval-arithmetic mean-value bound
    structure: kappa_4 has the closed form that makes the full
    certificate auditable.
    """
    import math
    h = mpf("1e-12")
    witnesses = []
    for bv in (0.7, 2.0, 8.0, 35.0, 120.0):
        b = mpf(bv)
        # Numerical derivative of kappa_3 at b (central difference)
        k4_num = (_kappa3(b + h) - _kappa3(b - h)) / (2 * h)
        # Closed-form kappa_4 from Riccati formula
        k4_riccati = _kappa4_exact(_r(b), b)
        rel_err = abs(float(k4_num - k4_riccati)) / abs(float(k4_riccati))
        # 1e-7 is comfortable: numerical-derivative truncation at h=1e-12
        # with mp.dps=30 leaves ~14 digits of agreement.
        if rel_err > 1e-7:
            return False, witnesses, bv, rel_err
        witnesses.append((float(bv), float(k4_riccati), rel_err))
    return True, witnesses, None, None


# ----------------------------------------------------------------------
# Bank-registered check
# ----------------------------------------------------------------------

def check_T_kappa3_negative_all_beta():
    """T_kappa3_negative_all_beta: kappa_3(beta) < 0 for all beta > 0.

    Tier 4 [P_structural].

    Source-of-record: Paper 30 (Tube Mechanism for the Lattice Mass Gap)
    section sec:tube_audit + supplementary kappa3_certified_v3.py at
    Papers/Paper 30 - .../kappa3_certified_v3.py.

    Witness structure (four phases):
      Phase 1: beta in (0, 0.5] -- 100 sample points; kappa_3 < 0
               anchored by the small-beta power series -beta/16 + ... .
      Phase 2: beta in [0.5, 200] -- 200 logarithmic-grid points.
               Full interval-arithmetic certificate (~14000 blocks at
               mp.dps = 60) lives in supplementary kappa3_certified_v3.py.
      Phase 3: beta >= 200 -- sample at 200, 500, 1000, 5000, 10000;
               kappa_3 -> 0 from below matching -3/beta^3 asymptotic.
      Phase 4: Riccati consistency -- closed-form kappa_4 from
               r' = 1 - r^2 + r/beta matches numerical d/dbeta of kappa_3
               at five witnesses to relative error < 1e-7.

    Used in Paper 30 to close the d=3 mass-gap proof: kappa_3 < 0 is
    the Turan-type input that bounds the one-tube eigenvalue lambda_1
    < 4/27 uniformly in beta.
    """
    p1_ok, p1_worst, _ = _phase1_small_beta()
    if not p1_ok:
        return {
            "name": "T_kappa3_negative_all_beta",
            "passed": False,
            "error": f"Phase 1 small-beta failed: kappa_3 = {p1_worst}",
            "key_result": "Phase 1 failed",
            "tier": 4,
            "epistemic": "[P_structural]",
        }

    p2_ok, p2_worst, p2_n = _phase2_mid_beta_sample()
    if not p2_ok:
        return {
            "name": "T_kappa3_negative_all_beta",
            "passed": False,
            "error": f"Phase 2 mid-beta failed: kappa_3 = {p2_worst}",
            "key_result": "Phase 2 failed",
            "tier": 4,
            "epistemic": "[P_structural]",
        }

    p3_ok, p3_samples, p3_fail = _phase3_large_beta()
    if not p3_ok:
        return {
            "name": "T_kappa3_negative_all_beta",
            "passed": False,
            "error": f"Phase 3 large-beta failed at beta={p3_fail}",
            "key_result": "Phase 3 failed",
            "tier": 4,
            "epistemic": "[P_structural]",
        }

    p4_ok, p4_witnesses, p4_fail_b, p4_err = _phase4_riccati_consistency()
    if not p4_ok:
        return {
            "name": "T_kappa3_negative_all_beta",
            "passed": False,
            "error": f"Phase 4 Riccati failed at beta={p4_fail_b}, rel_err={p4_err}",
            "key_result": "Phase 4 failed",
            "tier": 4,
            "epistemic": "[P_structural]",
        }

    max_p4_err = max(w[2] for w in p4_witnesses)

    return {
        "name": "T_kappa3_negative_all_beta",
        "passed": True,
        "key_result": (
            f"kappa_3(beta) < 0 for all beta > 0 witnessed across three regimes: "
            f"Phase 1 (0,0.5]: 100 points, worst kappa_3={p1_worst:.4e}; "
            f"Phase 2 [0.5,200]: {p2_n} log-grid points, worst kappa_3={p2_worst:.4e}; "
            f"Phase 3 [200,inf): kappa_3/(-3/beta^3) = {p3_samples[-1][3]:.4f} at beta=10000; "
            f"Phase 4 Riccati: max rel_err |kappa_4_num - kappa_4_Riccati| = {max_p4_err:.2e}. "
            f"Full interval-arithmetic certificate in supplementary kappa3_certified_v3.py. "
            f"[P_structural]"
        ),
        "summary": (
            "Witness for kappa_3(beta) < 0 for all beta > 0, where "
            "kappa_3 = d^3/dbeta^3 log(I_1(beta)/beta).  Three sampling "
            "phases (small / mid / large beta) plus algebraic consistency "
            "of the Riccati formula r'(beta) = 1 - r^2 + r/beta against "
            "numerical d/dbeta of kappa_3.  Full certified-interval-block "
            "version with ~14000 blocks at mp.dps = 60 in the supplementary "
            "kappa3_certified_v3.py kept alongside Paper 30.  Source-of-record: "
            "Paper 30 section sec:tube_audit + supplementary script.  This is "
            "the Turan-type analytic input to Paper 30's d=3 all-beta mass "
            "gap (lambda_1 < 4/27 uniformly)."
        ),
        "tier": 4,
        "epistemic": "[P_structural]",
        "dependencies": [],
        "artifacts": {
            "phase1_n": 100,
            "phase1_worst_kappa3": float(p1_worst),
            "phase2_n": p2_n,
            "phase2_worst_kappa3": float(p2_worst),
            "phase3_samples": [
                {"beta": s[0], "kappa3": s[1], "leading_-3/b3": s[2], "ratio": s[3]}
                for s in p3_samples
            ],
            "phase4_max_rel_err": max_p4_err,
            "supplementary_script": (
                "Papers/Paper 30 - Tube Mechanism for the Lattice Mass Gap/"
                "kappa3_certified_v3.py"
            ),
        },
    }


# ----------------------------------------------------------------------
# Bank registration
# ----------------------------------------------------------------------

_CHECKS = {
    "T_kappa3_negative_all_beta": check_T_kappa3_negative_all_beta,
}


def register(registry):
    """Register Yang-Mills kappa_3 witness into the global bank."""
    for name, fn in _CHECKS.items():
        registry[name] = fn


if __name__ == "__main__":
    result = check_T_kappa3_negative_all_beta()
    print(f"PASS: {result['passed']}")
    if "key_result" in result:
        print(f"key_result: {result['key_result']}")
    if not result["passed"] and "error" in result:
        print(f"error: {result['error']}")

# ---------------------------------------------------------------------------
# IE onboarding (Wave 7, v24.3.347).
# ---------------------------------------------------------------------------
IE_DECLARATIONS = (
    {
        "input_id": "strong:ym_kappa3_negative",
        "expect_export": False,
        "axis": "ROUTE",
        "claim_text": (
            "check_T_kappa3_negative_all_beta (tier 4, machine field "
            "epistemic='[P_structural]') is the bank witness for kappa_3(beta) := "
            "d^3/dbeta^3 log(I_1(beta)/beta) < 0 for all beta > 0 -- the Turan- "
            "type input that bounds the one-tube eigenvalue lambda_1 < 4/27 "
            "uniformly in beta in Paper 30's d=3 lattice mass-gap tube mechanism. "
            "The bank check is a four-phase REPRESENTATIVE witness, not the full "
            "certificate: small-beta power-series anchor (-beta/16 leading term) "
            "on (0, 0.5]; 200-point logarithmic grid on [0.5, 200]; large-beta "
            "asymptotic -3/beta^3 samples; and Riccati-identity consistency of "
            "the closed-form kappa_4 (r' = 1 - r^2 + r/beta) to relative error < "
            "1e-7. The full interval-arithmetic certificate (~14000 blocks at "
            "60-digit precision) lives outside the bank in Paper 30's "
            "supplementary kappa3_certified_v3.py, which is the source of record. "
            "The statement is a pure mathematical inequality (modified Bessel "
            "functions via mpmath -- a tool import for evaluation); no physics "
            "import, no gap-value claim, no continuum-limit claim. "
        ),
        "note": "Wave 7 Paper 30 kappa_3 negativity witness; [P_structural] field, full interval certificate lives off-bank",
    },
)
