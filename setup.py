# Admissibility Physics Framework (APF) -- package setup.
#
# v7.9.0 (2026-05-04 LATER — Phase 42 foundation-alignment codebase rev): four
# new bank-registered tier-4 [P_structural] checks added closing the LATER-9
# input-collapse + LATER-11 through LATER-22 codebase alignment.
#
# New module apf/foundation_inputs.py with two checks:
#  - check_T_four_input_declaration: canonical 4-input set (FD1 + FD2 + FD3 +
#    finite-physical-regime hypothesis); names them, asserts no fifth input
#    is invoked; PLEC and downstream commitments are derivable consequences.
#  - check_T_PLEC_derived_from_spine: A1/MD/A2/BW each derived from the
#    4-input set under Paper 10 v1.12 §3.5 reductions.
#
# apf/kappa_int_bounds.py extended with two checks:
#  - check_T_R1_R4_spine_derivable: R1 (compactness) automatic for finite
#    interrogation; R2 (robustness) built into FD2; R3 (LSC) from cost-
#    positive-only-on-physical structure; R4 (finite capacity) = A1 itself.
#  - check_T_minimum_distinction_floor_via_MD: floor theorem proved via
#    MD's uniform floor pointwise; no compactness, LSC, or Weierstrass
#    infimum-attainment theorem invoked.
#
# EXPECTED_THEOREM_COUNT 467 → 471; verify_all 484 → 488; modules 27 → 28.
# Codebase folder rename APF_Codebase_v7.8 → APF_Codebase_v7.9.
#
# v7.8.0 (2026-05-04 LATER-15 — Phase 38 κ_int structural rigidity codebase rev):
# three new bank-registered checks added in new module apf/kappa_int_bounds.py
# closing the κ_int structural rigidity work from Paper 1 Supplement v8.27
# §9 + §14.5.  New checks: check_T_kappa_int_lower_bound (marginal-floor lemma
# + sum-of-floors corollary + structural lower bound on the singleton-form
# interface term, all derived from MD via BW; witnessed on a 4-site toy
# interface with ε*=0.5), check_T_kappa_int_upper_bound_C1C5 (continuum-bridge
# upper bound from kernel-norm finiteness + far-separation exponential
# suppression at L=97, ξ_rec=1.5 giving κ_int = 2.83e-29), and
# check_T_kappa_int_two_sided_rigidity (two-sided structural bound packaging
# both sides; envelope width 1.054 on the witness; audit-flagged 'free
# functional' complaint closed -- the residue is structurally constrained,
# not free).  All three tier-4 [P_structural].  EXPECTED_THEOREM_COUNT
# 464 -> 467; verify_all 481 -> 484; modules 26 -> 27.
#
# v7.7.0 (2026-05-02 — Paper-24/25 recruitment-radius codebase rev): seven new
# bank-registered checks added to apf/recruitment.py closing the recruitment-
# radius foundation work introduced in Papers 24 and 25.  New checks:
# check_T_master_equation_form, check_T_three_regimes_tau_rec,
# check_T_substrate_anchor_entangled_state,
# check_T_cross_branch_matrix_element_form,
# check_T_sixteen_case_unification_structural,
# check_T_DCE_Q_dependence_prediction, check_T_purcell_DCE_consistency.
# All seven tier-4 [P_structural].  EXPECTED_THEOREM_COUNT 457 -> 464;
# verify_all 474 -> 481; modules unchanged at 26.  apf/recruitment.py
# extended in place from 3 to 10 checks; closed-form Einstein A
# (check_T_quantum_anchor_einstein_A) was already present at v7.6 and
# carries the 'closed form on 1' commitment.
#
# v7.3.0 (2026-04-28 Phase 22b): codebase landing of Paper 5 Supplement v5.1
# quantum-structure framework -- Quantum Admissibility Condition, branch
# taxonomy split (SepStr/SepAdm/IJCStr/IJCAdm/IJCPres), kappa_Bool defender
# minimization, capacity lower-bound certificate, complex-field selection
# via APF-complete composite accounting, and the Born trace rule.  New
# module apf/quantum_admissibility.py with six bank-registered checks
# (T_branch_taxonomy_inclusions, T_kappa_Bool_minimum,
# T_capacity_lower_bound_certificate, T_quantum_admissibility_condition,
# T_field_selection_complex, T_Born_trace_rule).  EXPECTED_THEOREM_COUNT
# 434 -> 440; verify_all 451 -> 457; modules 24 -> 25.  Theorem bank:
# 440 bank-registered theorems, 457 verify_all checks, 25 registered
# modules + apf/standalone/.
#
# v7.2.0 (2026-04-28 Phase 22a): codebase landing of Paper 1 Supplement v7.1
# minimal-foundation framework -- Admissible Possibility Space (APS) as the
# foundation object.  New module apf/aps.py with three bank-registered
# checks (T_APS_construction, T_continuation_preorder,
# T_state_distinction_ledger_induced).  EXPECTED_THEOREM_COUNT 431 -> 434;
# verify_all 448 -> 451; modules 23 -> 24.
#
# v7.1.0 (2026-04-26 Phase 21): inseparable-IJC bridge premise; substrate-
# factorizability dichotomy with paired witnesses (Sep / IJC); branch-(IJC)
# classification at quantum-capable interfaces empirically inherited from
# Bell + Kochen-Specker.
#
# Theorem bank (v7.1): 431 bank-registered theorems, 448 verify_all checks, 23
# registered modules + apf/standalone/, 48 quantitative predictions.
#
# Full per-version changelog lives in apf/bank.py (EXPECTED_THEOREM_COUNT
# docstring) and CHANGELOG.md, not here. setup.py is metadata only.

from setuptools import setup, find_packages

setup(
    name="apf",
    version='24.3.260',
    description=(
        "Admissibility Physics Framework: a machine-verifiable theorem bank "
        "deriving the Standard Model and cosmological structure from finite "
        "enforcement (PLEC). 3675 bank-registered checks, zero free dimensionless parameters (one dimensional anchor)."
    ),
    long_description=(
        "APF is a framework that takes finite enforcement seriously as a "
        "physical quantity. The Principle of Least Enforcement Cost (PLEC) "
        "and its four constitutive features (A1, MD, A2, BW) generate the "
        "Standard Model gauge group, fermion content, and cosmological "
        "capacity partition with zero free dimensionless parameters (one dimensional anchor). Every claim traces "
        "to a named check function in the apf/ package. See README.md for "
        "orientation and verify_all.py for the full verification suite."
    ),
    long_description_content_type="text/markdown",
    author="E. S. Brooke",
    author_email="brooke.ethan@gmail.com",
    url="https://github.com/Ethan-Brooke/APF-Engine-Repo",
    license="MIT",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.20",
        "scipy>=1.7",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Physics",
    ],
)