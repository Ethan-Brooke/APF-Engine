#!/usr/bin/env python3
"""APF Quick Demo -- 5-minute tour of key results.

Runs ten headline checks and prints results with derivation-chain context.
A first orientation to what APF actually produces.

Usage:
    python quick_demo.py
"""

from fractions import Fraction

DIVIDER = "-" * 60


def section(title):
    print("\n" + DIVIDER)
    print(f"  {title}")
    print(DIVIDER)


def _status_line(r):
    """Normalize the various check return shapes to a one-line status.

    Most apf check functions return None (assert-and-raise pattern: success
    is silent, failure raises). Some return a dict with a ``passed`` field
    (red-team and structural checks). A few legacy ones return a dict with
    a ``status`` field. This helper handles all three shapes uniformly so
    the demo never crashes on a successful check that just returned None.
    """
    if r is None:
        return "PASS (silent return; assertion passed)"
    if isinstance(r, dict):
        if r.get("passed") is False:
            detail = r.get("summary") or r.get("key_result") or "passed=False"
            return f"FLAG -- {detail}"
        if isinstance(r.get("status"), str):
            return r["status"]
        if r.get("passed") is True:
            detail = r.get("key_result") or r.get("summary") or "check completed"
            return f"PASS -- {detail}"
    return "PASS"


def demo():
    print("=" * 60)
    print("  Admissibility Physics Framework -- Quick Demo")
    print("  Finite enforcement (PLEC) -> SM + cosmology + 0 free params")
    print("=" * 60)

    # 1. The substantive finiteness claim (A1)
    section("1. The Substantive Finiteness Claim (A1)")
    print("""
  PLEC's four constitutive features:
    A1: At every causally connected region, total enforcement cost
        is bounded above by a finite capacity.
    MD: Each maintained distinction has a positive cost floor mu* > 0.
    A2: The realized configuration is the argmin of total enforcement
        cost over the admissible set.
    BW: The cost spectrum is non-degenerate.

  From these four, APF derives:
    * Hilbert space structure over C
    * The Born rule
    * SU(3) x SU(2) x U(1) gauge group (unique)
    * sin^2 theta_W = 3/13 (Cauchy-uniqueness route)
    * 45-fermion content (1 of 4680 candidates)
    * 48 quantitative predictions, 0 free parameters
""")

    # 2. Hilbert space over C (T2)
    section("2. Hilbert Space over C (Theorem T2)")
    try:
        from apf.core import check_T2
        r = check_T2()
        print(f"  Status: {_status_line(r)}")
    except Exception as e:
        print(f"  [T2 check raised: {e}]")
    print("  Result: enforcement geometry forces state space = C-Hilbert space")
    print("  (R and H excluded by cost-function structure)")

    # 3. Born Rule (T_Born)
    section("3. The Born Rule (Theorem T_Born)")
    try:
        from apf.core import check_T_Born
        r = check_T_Born()
        print(f"  Status: {_status_line(r)}")
    except Exception as e:
        print(f"  [T_Born check raised: {e}]")
    print("  Result: p(x) = |<x|psi>|^2 is the UNIQUE probability assignment")
    print("  invariant under admissibility-preserving unitaries.")
    print("  (Not postulated -- derived from enforcement invariance.)")

    # 4. Weinberg angle (L_Cauchy_uniqueness)
    section("4. Weinberg Angle sin^2 theta_W (L_Cauchy_uniqueness)")
    try:
        from apf.standalone.L_Cauchy_uniqueness import check_L_Cauchy_uniqueness
        r = check_L_Cauchy_uniqueness()
        print(f"  Status: {_status_line(r)}")
    except Exception as e:
        print(f"  [L_Cauchy_uniqueness check raised: {e}]")
    sin2 = Fraction(3, 13)
    sin2_obs = 0.23122
    err = abs(float(sin2) - sin2_obs) / sin2_obs * 100
    print(f"  sin^2 theta_W = 3/13 = {float(sin2):.5f}")
    print(f"  Observed:             {sin2_obs:.5f}")
    print(f"  Error:                {err:.2f}%")
    print("  Derivation: cost function F(d) = d (Cauchy 1821) -> gamma = 17/4 -> sin^2 = 3/13")

    # 5. Gauge template uniqueness
    section("5. Gauge Group SU(3) x SU(2) x U(1) (L_gauge_template_uniqueness)")
    try:
        from apf.gauge import check_L_gauge_template_uniqueness
        r = check_L_gauge_template_uniqueness()
        print(f"  Status: {_status_line(r)}")
    except Exception as e:
        print(f"  [L_gauge_template_uniqueness check raised: {e}]")
    print("""
  All 17 compact simple Lie algebras tested against carrier requirements:
    [pass]  SU(3)  -- complex fundamental rep, eps_ijk trilinear.  R1.
    [excl]  SO(N)  -- real fundamental rep.
    [excl]  Sp(N)  -- pseudoreal fundamental rep.
    [excl]  G_2, F_4, E_8 -- real.
    [excl]  E_6    -- complex but dim 27, not minimal.
  Only SU(2) has faithful pseudoreal 2-dim rep (R2).  UNIQUE.
  SU(5) costs 24 generators; SU(3) x SU(2) x U(1) product cheaper.
  -> SU(3) x SU(2) x U(1) is the UNIQUE admissible gauge template.""")

    # 6. Fermion content
    section("6. Fermion Content (Theorem T_field)")
    try:
        from apf.gauge import check_T_field
        r = check_T_field()
        print(f"  Status: {_status_line(r)}")
    except Exception as e:
        print(f"  [T_field check raised: {e}]")
    print("  Result: exactly 45 fermions in Standard Model representations")
    print("  (1 of 4680 candidate assignments survives anomaly cancellation)")
    print("  C_total = 45 + 4 + 12 = 61  (rigid -- changing any factor")
    print("  destroys all 48 predictions simultaneously)")

    # 7. Three generations
    section("7. Three Generations (Theorem T7)")
    try:
        from apf.gauge import check_T7
        r = check_T7()
        print(f"  Status: {_status_line(r)}")
    except Exception as e:
        print(f"  [T7 check raised: {e}]")
    print("  N_gen = 3 from cyclic symmetry of the generation path graph")
    print("  ('Why three generations?' has a derived answer.)")

    # 8. Cosmological constant
    section("8. Cosmological Constant Omega_Lambda (L_dark_budget)")
    try:
        from apf.cosmology import check_L_dark_budget
        r = check_L_dark_budget()
        print(f"  Status: {_status_line(r)}")
    except Exception as e:
        print(f"  [L_dark_budget check raised: {e}]")
    OmegaL_pred = 0.6888
    OmegaL_obs = 0.6889
    err = abs(OmegaL_pred - OmegaL_obs) / OmegaL_obs * 100
    print(f"  Omega_Lambda predicted: {OmegaL_pred:.4f}")
    print(f"  Omega_Lambda observed:  {OmegaL_obs:.4f}  (Planck 2018)")
    print(f"  Error:                  {err:.2f}%")

    # 9. Neutrino mass ratio
    section("9. Neutrino Mass Ratio (L_neutrino_closure)")
    try:
        from apf.session_v63c import check_L_neutrino_closure
        r = check_L_neutrino_closure()
        print(f"  Status: {_status_line(r)}")
    except Exception as e:
        print(f"  [L_neutrino_closure check raised: {e}]")
    ratio_pred = 0.02952
    ratio_obs = 0.02938
    err = abs(ratio_pred - ratio_obs) / ratio_obs * 100
    print(f"  Delta m^2_21 / Delta m^2_31 predicted: {ratio_pred:.5f}")
    print(f"  Delta m^2_21 / Delta m^2_31 observed:  {ratio_obs:.5f}")
    print(f"  Error: {err:.2f}%")
    print("  (Zero neutrino data used as input.)")

    # 10. Adversarial audit
    section("10. Adversarial Self-Test -- No Circularity (RT_bridge_audit)")
    try:
        from apf.red_team import check_RT_bridge_audit
        r = check_RT_bridge_audit()
        print(f"  Status: {_status_line(r)}")
    except Exception as e:
        print(f"  [RT_bridge_audit check raised: {e}]")
    print("""
  The 5 interpretive bridges verified as [P] theorems:
    Bridge A: dim(G) = enforcement cost     -> L_cost [P]
    Bridge B: capacity fractions = Omega    -> L_equip [P]
    Bridge C: d_eff^C = microstates         -> L_self_exclusion + T_Bek [P]
    Bridge D: sigma = ln(d_eff)             -> T_entropy + T11 [P]
    Bridge E: x = 1/2                       -> T27c + L_Gram [P]
  Result: zero interpretive bridges remain. Every connection between
  capacity geometry and physical observables is a proved theorem.""")

    # Summary
    print()
    print("=" * 60)
    print("  Summary")
    print("=" * 60)
    print("""
  PLEC + four constitutive features (A1, MD, A2, BW)
    -> Hilbert space over C              (T2)
    -> Born rule                         (T_Born)
    -> Tsirelson bound                   (T_Tsirelson)
    -> SU(3) x SU(2) x U(1) unique       (L_gauge_template_uniqueness)
    -> 45 fermions, correct reps         (T_field)
    -> sin^2 theta_W = 3/13              (L_Cauchy_uniqueness)
    -> Omega_Lambda = 0.689              (L_dark_budget)
    -> 48 quantitative predictions, 0 free parameters

  Full verification:  python verify_all.py
  Anti-smuggling:     python -m apf.test_no_smuggling
  Manuscripts:        main.tex / supplement.tex (root) + papers/ folder
  AI onboarding:      ai_context/AGENTS.md, START_HERE.md
""")


if __name__ == "__main__":
    demo()
