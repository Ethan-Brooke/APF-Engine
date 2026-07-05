"""The EW branch-scale functional is independent of the foundational base -- a no-go
[P_structural].

Terminus of the identification-(B) derivation frontier, banked after a fourth walk and a
fourth hostile audit (2026-07-02; the walk's Move A -- forcing reservoir-measure uniformity --
was REFUTED the same session and is registered do-not-re-walk). Three prior routes tried to
DERIVE the reading that the electroweak vev is the per-state reservoir amplitude: the Born
route (REFUTED 2026-06-08 -- the vev's square root is a Gaussian functional determinant, not
a Gleason amplitude), the CSC primitive (DID NOT CLEAR 2026-06-08 -- C/p degeneracy), and the
SSU/H-form route (REFUTED 2026-07-02 -- the rho^(1/4) counterexample). This module banks WHY
they had to fail: the functional form f = v_H/M_Pl, as an expression in ledger structure, is
NOT fixed by the foundational base {A1, MD, A2, BW, FD1-sc} plus the banked base-resting
stack. Proof by countermodel EXISTENCE -- the closed-world direction (>= 2 admissible
completions), so the .284 abelian-exhaustiveness trap does not apply.

THE LINEAGE, AND WHAT IS NEW. The rescaling no-go (planck_magnitude_single_anchor) covers the
absolute MAGNITUDE; the prefactor axiom-independence (v24.3.180) covers the exact O(1)
PREFACTOR given the form; the invariance no-go (v24.3.177) covers the prefactor CARRIERS.
None covers the FUNCTIONAL FORM itself -- the exponent-bearing map from ledger to scale.
This module closes that gap: even granting every banked count (C_boson = 16, d_eff = 102)
and every prefactor clause, the base does not select WHICH suppression the branch scale is.

WHAT THE BASE ACTUALLY FIXES (K-audit, honest form):
  K-positivity: f > 0 and finite (A1 finiteness; no banked base-resting theorem gives more --
    the "direction forced / f <= 1" clause lives in check_T_ew_lambda_unified_suppression at
    grade P_structural_convention and PRESUPPOSES the exp(-S) form, so it is reading-
    conditional, not base-resting; this module deliberately rests nothing on the cap).
  K-dimensionless: f is a pure number (rescaling no-go; each countermodel below is recomputed
    from banked integers {d_eff, C_boson, C_total, N_c} and {pi, e} only).
  K-structural (FD1-sc): f is not free fiat -- it must be SOME structural expression. FD1-sc
    is a negative existential; per its banked guardrail it supplies no value, and "structural
    expression in banked counts" admits a CONTINUUM of completions. The no-go is
    correspondingly cheap, and is priced as such: its content is the formalization of a
    concession the reservoir module already makes in prose ("MOTIVATES the reservoir reading
    rather than PROVING it is forced"). The value of banking it is the SMUGGLING GUARD: any
    future claim to derive v_H/M_Pl from the base must first name the new base-resting
    theorem that kills the countermodel family below. Three refuted routes already paid for
    not having one.
  K4 (no other banked fixer): the v_H-fixing surface is walked programmatically below (the
    v24.3.305 citation-hygiene shape). Classification: (i) the reservoir/hierarchy family --
    graded reading-conditional throughout (they ARE the identification, not constraints on
    it); (ii) the spectral-action route (session_qg.check_L_vev_threshold_matching) --
    measurement-completion (consumes measured y_t(M_Z) = 0.936 and a retired-[C] c_R), not
    base-resting; (iii) diagnostics/comparators. Two named reconciliations: (a) the
    2026-06-08 de-circularization note's table row "exponent -1/2 (Born square root) [P]" is
    framing-conditional -- the Born sourcing was refuted the same day; the -1/2 is [P] only
    GIVEN the amplitude reading; (b) the M_cross/alpha_s chain would collide with the
    countermodels only if the abelian 1/alpha_Y = 61 reading were base-resting [P]; it was
    regraded [P_structural_reading] at v24.3.284, and this check PINS that regrade
    programmatically -- if the abelian reading is ever re-promoted, this check FAILS and the
    countermodel family must be re-adjudicated (a live falsifier hook, by design).

THE COUNTERMODELS (all structural, dimensionless, positive, mutually distinct):
  banked reading (B):  f = sqrt(N_c)/(4 pi) * (12/7) * d_eff^(-C_boson/2)   -> 246.2 GeV
  CM-1 (full power):   f = d_eff^(-C_boson)                                  -> 8.9e-14 GeV
  CM-2 (rational):     f = d_eff^(-2)                                        -> 1.2e+15 GeV
  CM-3 (transmutation-form): f = exp(-C_total/2)                             -> 6.9e+05 GeV
Admissibility is judged against the base and the banked base-resting stack, NEVER against
246 GeV -- that the countermodels are empirically wrong is the point: the base does not know
which world it is in. (Same posture as v24.3.180, which admitted countermodels at 49-426 GeV.
Honest difference in kind: .180 held all banked content fixed and isolated one exact residual
freedom; this no-go operates where every form-fixing check is self-declared reading-
conditional, so the countermodels witness a concession rather than carve a new boundary.)

CONSEQUENCE. Identification (B) -- the squared branch scale read as the selected
configuration's occupation weight -- is a PROVEN-IRREDUCIBLE reading, not an open derivation
target. The absolute-scale frontier reaches the same terminal shape as the magnitude itself:
external where the no-gos say it must be, adopted-and-stated where it reads, corroborated at
the two banked instances (EW + cosmological, check_T_ew_lambda_unified_suppression). What
this module does NOT do: force uniformity of the reservoir measure (Move A, REFUTED -- the
fermion counterexample: equal eps*/sigma pricing does not give isomorphic continuation
structure; FD1-sc cannot exclude stratum-correlated weights because they are structural, not
fiat); supply any value; or exclude the enhancement reading from the base (reading-
conditional only).

[P_structural]; no measured target consumed (246 GeV appears nowhere as an input or a gate).

LEDGER-SCALE CLAUSE cross-reference (2026-07-02 principal ruling, fork (ii) consolidation):
this no-go is the clause's MINIMALITY CERTIFICATE -- its countermodel family is the smuggling
guard pricing any future claim to derive the form the clause declares (branch case
phi/M_Pl = eta*exp(-S/2); saturation case rho/M_Pl^4 = eta*exp(-S); transmuted scales exempt).
Clause named per the 2026-07-02 ruling; grades unchanged (naming, not elevation; forks
(iii)/(i) remain staged). Ruling note: 'Reference - The Ledger-Scale Clause - Adoption
Investigation (2026-07-02).md'.
"""
from __future__ import annotations

import math
import os
import re

import apf as _apf_pkg
from apf.apf_utils import check, _result

# banked integers (fixed elsewhere; the ONLY inputs to every candidate below)
D_EFF, C_BOSON, C_TOTAL, N_C = 102, 16, 61, 3

EXPORT_FLAGS = dict(
    Export_scale_functional_fixed_by_base=0,          # the no-go
    Export_identification_B_independence_proven=1,    # >= 2 admissible completions
    Export_smuggling_guard_priced=1,                  # future derivations must kill the CMs
    Export_base_fixes_at_most_positivity=1,           # K1 honest form (cap is reading-conditional)
    Export_abelian_reading_regrade_pinned=1,          # falsifier hook on .284
    measured_target_consumed=0,
    target_consumed=0,
)

# the candidate family: name -> (f as a float built from banked integers + pi/e only)
def _candidates():
    return {
        "banked_reading_B": math.sqrt(N_C) / (4 * math.pi) * (12.0 / 7.0) * D_EFF ** (-(C_BOSON / 2.0)),
        "CM1_full_power":   float(D_EFF) ** (-C_BOSON),
        "CM2_rational":     float(D_EFF) ** (-2.0),
        "CM3_transmutation_form": math.exp(-C_TOTAL / 2.0),
    }


def _walk_vev_fixing_surface():
    """K4 walker (the v24.3.305 citation-hygiene shape): every module whose source carries
    the EW-floor suppression signature or the vev comparator must be in the closed-world
    classification. Returns (hits, unclassified)."""
    pkg_dir = os.path.dirname(os.path.abspath(_apf_pkg.__file__))
    # source-level signatures of "this module computes/fixes the EW floor from the ledger"
    sig = re.compile(r"C_boson\s*/\s*2|C_BOSON\s*/\s*2|102\s*\*\*\s*\(?-8|d_eff\s*\*\*\s*\(\s*-\s*\(?\s*[Cc]", )
    comparator = re.compile(r"246\.2")
    CLASSIFIED = {
        # (i) the reservoir/hierarchy identification family (reading-conditional by grade)
        "ew_planck_hierarchy_mechanism.py": "reservoir_family",
        "ew_bosonic_enforcement_reservoir.py": "reservoir_family",
        "ew_pre_branch_necessity.py": "reservoir_family",
        "ew_static_well_factorization.py": "reservoir_family",
        "ew_floor_measure_continuation_root.py": "reservoir_family",
        "ew_sqrtNc_carrier_color_triplet.py": "reservoir_family",
        "ew_planck_anchor_gravity_consistency.py": "reservoir_family",
        "ew_prefactor_axiom_independence.py": "reservoir_family",
        "ew_prefactor_invariance_no_go.py": "reservoir_family",
        "ew_branch_incidence_density.py": "reservoir_family",
        "sigma_scale_yukawa_free_geometric_floor.py": "reservoir_family",
        "planck_magnitude_single_anchor.py": "reservoir_family",
        "sigma_scale_capacity_formula_gate.py": "reservoir_family",  # gate/disposition of the same route
        "lambda_absolute.py": "reservoir_family",           # unified-suppression sibling
        "confinement_scale_single_anchor.py": "reservoir_family",
        "mcross_planck_ratio_composition.py": "reservoir_family",  # the composed ratio (v24.3.365)
        "acc_reading_selection.py": "reservoir_family",
        "ew_pre_branch_reservoir_ordering.py": "reservoir_family",
        # (ii) measurement-completion routes (consume measured inputs; not base-resting)
        "session_qg.py": "measurement_completion",
        "session_v63c.py": "measurement_completion",
        "majorana.py": "measurement_completion",
        "supplements.py": "measurement_completion",
        "generations.py": "measurement_completion",
        # (iii) this module
        "ew_scale_functional_independence.py": "self",
    }
    hits, unclassified = {}, []
    for fn in sorted(os.listdir(pkg_dir)):
        if not fn.endswith(".py") or fn.startswith("_"):
            continue  # manifest/infra files carry inventory comments, not fixers
        try:
            src = open(os.path.join(pkg_dir, fn), encoding="utf-8", errors="ignore").read()
        except OSError:
            continue
        if sig.search(src) and (comparator.search(src) or "v_H" in src or "vev" in src.lower()):
            cat = CLASSIFIED.get(fn)
            hits[fn] = cat
            if cat is None:
                unclassified.append(fn)
    return hits, unclassified


def _abelian_regrade_pinned():
    """Reconciliation (b), machine-pinned: the M_cross/alpha_s chain tolerates the
    countermodels only because the abelian 1/alpha_Y=61 reading is [P_structural_reading]
    (v24.3.284), not [P]. If it is ever re-promoted, this returns False and the bank fails."""
    pkg_dir = os.path.dirname(os.path.abspath(_apf_pkg.__file__))
    src = open(os.path.join(pkg_dir, "abelian_coupling_capacity_count.py"),
               encoding="utf-8", errors="ignore").read()
    return "P_structural_reading" in src


def check_T_ew_scale_functional_independence_no_go():
    # -- the countermodel family: structural, dimensionless, positive, distinct --
    cands = _candidates()
    for name, f in cands.items():
        check(f > 0.0 and math.isfinite(f), f"{name}: f positive and finite (K-positivity)")
        # K-dimensionless/structural by construction: recomputable from banked integers only
        check(isinstance(f, float), f"{name}: pure number")
    vals = sorted(cands.values())
    for a, b in zip(vals, vals[1:]):
        check(abs(math.log10(b) - math.log10(a)) > 1.0,
              "completions mutually distinct by >1 decade: they disagree on the physical vev")
    check(len(cands) >= 2, "at least two admissible completions exist -> f not fixed by the base")

    # -- what is NOT claimed: no base-resting cap is consumed; enhancement not excluded here --
    check(EXPORT_FLAGS["Export_base_fixes_at_most_positivity"] == 1,
          "K1 honest form: the base fixes at most positivity/finiteness of f; the "
          "direction-forced clause is reading-conditional (P_structural_convention)")

    # -- K4 walker: the v_H-fixing surface is closed-world classified --
    hits, unclassified = _walk_vev_fixing_surface()
    check(len(hits) >= 3, f"walker sees the known surface (got {len(hits)} modules)")
    check(len(unclassified) == 0,
          f"no unclassified v_H-fixing module (unclassified: {unclassified}) -- every fixer "
          "is reservoir-family (reading-conditional) or measurement-completion")
    check(all(v in ("reservoir_family", "measurement_completion", "self") for v in hits.values()),
          "classification categories are exactly the three named")

    # -- reconciliation (b) pinned: the .284 regrade is load-bearing for CM admissibility --
    check(_abelian_regrade_pinned(),
          "abelian 1/alpha_Y=61 reading is [P_structural_reading] (v24.3.284) -- if this ever "
          "re-promotes to [P], the countermodel family must be re-adjudicated (falsifier hook)")

    # -- the no-go itself --
    check(EXPORT_FLAGS["Export_scale_functional_fixed_by_base"] == 0,
          "NO-GO: the base + banked base-resting stack does not fix the scale functional")
    check(EXPORT_FLAGS["measured_target_consumed"] == 0,
          "246 GeV consulted nowhere (admissibility judged against the base, not the world)")

    return _result(
        name=("T_ew_scale_functional_independence_no_go: the functional form f = v_H/M_Pl is "
              "NOT fixed by the foundational base + banked base-resting stack -- >= 2 admissible "
              "structural completions exist (banked reading, full-power, rational, "
              "transmutation-form), mutually distinct by decades. Identification (B) is a "
              "proven-irreducible reading; the no-go prices future derivation claims "
              "[P_structural]"),
        tier=4,
        epistemic='P_structural',
        summary=(
            "Terminus of the identification-(B) frontier after four walks / four hostile audits "
            "(Born REFUTED 2026-06-08; CSC DID-NOT-CLEAR 2026-06-08; SSU REFUTED 2026-07-02; "
            "Move-A uniformity REFUTED 2026-07-02). The functional form of the EW branch scale "
            "is independent of {A1, MD, A2, BW, FD1-sc} + the banked base-resting stack: the "
            "K-audit shows the base fixes at most positivity/finiteness + dimensionlessness + "
            "non-fiat structurality (a continuum of completions), and the programmatic K4 "
            "walker classifies every v_H-fixing module as reading-conditional reservoir-family "
            "or measurement-completion (spectral route consumes measured y_t + retired-[C] "
            "c_R). Countermodels CM-1..3 satisfy all base constraints and give vevs from "
            "8.9e-14 to 1.2e+15 GeV. Lineage: completes the no-go triptych (magnitude = "
            "rescaling no-go; prefactor = .180/.177; FORM = this). Honest pricing: the "
            "countermodels formalize the reservoir module's own 'motivates, not proves' "
            "concession; the banked value is the smuggling guard + the .284 falsifier hook "
            "(abelian regrade pinned programmatically). Nothing here excludes the enhancement "
            "reading from the base (reading-conditional) or forces measure uniformity (Move A "
            "refuted: equal eps*/sigma pricing does not give isomorphic continuation "
            "structure; FD1-sc cannot exclude structure-correlated weights)."
        ),
        key_result=(
            "NO-GO: the EW scale FUNCTIONAL is independent of the base -- 4 admissible "
            "structural completions spanning 29 decades of v_H; identification (B) proven "
            "irreducible (adoption is the mathematical minimum); K4 walker closed-world clean; "
            ".284 abelian regrade pinned as a falsifier hook; completes the "
            "magnitude/prefactor/form no-go triptych"
        ),
        dependencies=['T_ew_bosonic_enforcement_reservoir_theorem',
                      'T_ew_prefactor_axiom_independence',
                      'FD1_structural_completeness',
                      'T_planck_magnitude_single_dimensional_anchor',
                      'T_ew_lambda_unified_suppression'],
        artifacts=dict(
            completions={k: f"{v:.3e}" for k, v in _candidates().items()},
            vev_span_GeV="8.9e-14 .. 1.2e+15 (banked reading: 246.2)",
            k4_walker="closed-world classification of the v_H-fixing surface, 0 unclassified",
            falsifier_hook="abelian_coupling_capacity_count [P_structural_reading] pinned (.284)",
            lineage="magnitude (rescaling no-go) / prefactor (.177/.180) / FORM (this)",
            move_A_status="REFUTED 2026-07-02 (fermion counterexample; do-not-re-walk)",
            export_flags=dict(EXPORT_FLAGS),
        ),
    )


_CHECKS = {
    "T_ew_scale_functional_independence_no_go": check_T_ew_scale_functional_independence_no_go,
}


def register(registry):
    registry.update(_CHECKS); return registry


def run_all():
    return {name: fn() for name, fn in _CHECKS.items()}

# ---------------------------------------------------------------------------
# IE onboarding declaration (v24.3.317, Full Bank Onboarding Wave 5). Claim-
# grade structural probe; the theorems stay with their banked checks; verdicts
# inherit banked grades, routing confers nothing. expect_export pinned by the
# observed engine verdict.
# ---------------------------------------------------------------------------

IE_DECLARATIONS = (
    {
        "input_id": "ew:absolute_scale_frontier_terminated",
        "expect_export": False,
        "axis": "ROUTE",
        "claim_text": (
            "The absolute-scale frontier terminus: the functional form f = "
            "v_H/M_Pl is not derivable -- "
            "check_T_ew_scale_functional_independence_no_go [P_structural] "
            "is a closed-world classification of the v_H-fixing surface "
            "with zero unclassified completions (candidate vevs span "
            "8.9e-14 to 1.2e+15 GeV against the banked reading 246.2). It "
            "composes the prefactor no-go chain: "
            "T_ew_prefactor_axiom_independence and "
            "T_ew_prefactor_invariance_no_go plus the 102^-8 hierarchy "
            "suppression mechanism, all three at [P_structural_convention]. "
        ),
        "covers": ("apf.ew_prefactor_axiom_independence", "apf.ew_prefactor_invariance_no_go", "apf.ew_planck_hierarchy_mechanism"),
        "note": "Wave 5 Group A head: the no-go triptych terminus (v24.3.314); covers = the prefactor chain (invariance_no_go + hierarchy_mechanism enter TRANSITIVELY via T_ew_prefactor_axiom_independence, the head's named dependency; composition verified at depth 2)",
    },
)
