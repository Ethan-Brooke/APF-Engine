# APF Orientation Guide — Generic LLM

*This guide is for any AI assistant being set up to work with the Admissibility Physics Framework. It is self-contained — you should be able to orient yourself from this document alone, then use the files in this repository to go deeper.*

---

## Overview in One Paragraph

The Admissibility Physics Framework (APF) is a formal mathematical program that derives the structure of quantum mechanics and the Standard Model of particle physics from a **single axiom** (A1: finite enforcement capacity) plus two regularity inputs. The result is a coherent derivation chain from a philosophical starting point ("distinctions cost something to maintain") through abstract mathematics to specific quantitative predictions — 47+ predictions matching experiment with mean error 3.8%. The framework is accompanied by a machine-verifiable Python codebase (349 check functions) that proves every theorem with exact rational arithmetic.

---

## Loading This Repository

To work with APF using an AI assistant, load the following files into your context or knowledge base:

**Essential (load these first):**
- `README.md` — overview and structure
- `ai_guides/GENERIC_LLM.md` — this file
- `apf/core.py` — Paper 1 core (48 checks, foundational)
- `apf/apf_utils.py` — constants and utilities
- `papers/paper1/main.tex` — the primary paper

**For gauge/Standard Model work:**
- `apf/gauge.py`
- `apf/supplements.py`
- `papers/paper2/main.tex`

**For mass/mixing work:**
- `apf/generations__8_.py`
- `apf/majorana.py`

**For cosmology work:**
- `apf/cosmology.py`
- `apf/gravity.py`

**For adversarial/red-team work:**
- `apf/red_team.py`
- `apf/bank.py`

**For precision prediction comparison:**
- `apf/validation.py`
- `papers/paper13/main.tex`

If your context window is limited, prioritize `core.py` + `apf_utils.py` + `README.md` — these give you the foundation for most tasks.

---

## The Axiom and the Argument

### A1: Finite Enforcement Capacity

> Any physical distinction that can be maintained must be maintainable by a process with finite operational cost.

An "enforcement" is any physical process that maintains a distinction — a measurement, a physical boundary, a conservation law. The axiom says these processes are not free: they have a cost, and that cost is finite.

**Two regularity inputs supplement A1:**
- **MD (Enforcement Isotropy):** No preferred direction in the space of distinctions
- **BW (Budget-Window Richness):** The capacity budget admits a continuum of enforcement windows

These are not additional physics assumptions — they are regularity conditions (analogous to Lebesgue measurability or Cauchy continuity in analysis).

### Why This Is Not Circular

A natural objection: "You're assuming a cost function, which is already a quantum-mechanical structure." APF addresses this carefully. The cost is *pre-physical* — it is a property of abstract distinctions, not of quantum states. The derivation goes: cost structure → state space → Hilbert space over ℂ → quantum mechanics. The Hilbert space is the output, not the input.

The D-quotient (space of maintained distinctions) is a definitional commitment, not an import from quantum mechanics.

---

## The Five-Layer Derivation Chain

### Layer 0: Admissibility Geometry

The foundational lemmas establish the mathematical structure of enforcement cost:

- `L_epsilon_star`: Minimum enforcement cost is positive (no free distinctions)
- `L_NZ`: Zero-cost enforcement does not exist
- `L_loc`: Enforcement is local
- `L_nc`: Non-commutativity of enforcement operators is forced (not assumed)
- `L_cost`: Cost function is uniquely F(d) = d by Cauchy's 1821 theorem
- `L_irr`: Enforcement operators are irreducible

These are all proved in `apf/core.py`.

### Layer I: Quantum Mechanics

From the geometry of enforcement:

- **T2**: The state space must be a Hilbert space over ℂ (not ℝ or ℍ)
- **T3**: Observable operators must be noncommutative
- **T_Born**: The Born rule is the unique enforcement-invariant probability assignment
- **T_Tsirelson**: Bell-inequality bound = 2√2 follows from budget constraints
- **T_CPTP**: Physical evolution is completely positive and trace-preserving

### Layer II: The Standard Model

Three carrier requirements (Theorem_R) identify what physical systems can carry the minimum viable enforcement structure:

- **R1**: Carriers must support complex, trilinear interactions → forces SU(N_c) type
- **R2**: Carriers must break time-reversal → forces chiral (SU(2)) type
- **R3**: Carriers must distinguish gauge sectors → forces abelian grading (U(1))

`L_gauge_template_uniqueness` then scans all 17 compact simple Lie algebras against these requirements. Only SU(N_c)×SU(2)×U(1) survives. `T_gauge` fixes N_c = 3 by cost minimization.

`T_field` derives 45 fermions in exactly the Standard Model representations.

`L_count` proves the total enforcement cost C = 61 is *rigid* — altering any factor destroys all predictions simultaneously.

### Layer III: Mass and Mixing

- `L_Gram` + `T27c`: The single-channel Gram overlap x = 1/2 (derived, not fitted)
- `L_multiplicative_amplitude`: Exponential mass suppression from independence (x^q) — this is what the Froggatt-Nielsen mechanism was trying to capture
- `L_mass_from_capacity`: 11 quark/lepton masses from 2 anchors (m_t, m_τ), 0 free parameters
- `T_CKM`, `T_PMNS`: Quark and lepton mixing matrices from capacity geometry

### Layer IV: Cosmology

- `L_equip`: Horizon equipartition → density fractions
- `L_dark_budget`: Ω_Λ, Ω_DM, Ω_b from enforcement budget
- `L_equation_of_state`: w₀ = −1 exact (no dynamical dark energy)
- `L_N_eff_prediction`: Effective neutrino number

---

## The Code Architecture

Every theorem has a `check_` function. The convention:

```python
def check_T_Born():
    """T_Born: Born Rule from Admissibility Invariance.
    
    Statement: The Born rule p(x) = |⟨x|ψ⟩|² is the unique probability
    assignment invariant under admissibility-preserving unitaries.
    
    Dependencies: T2, L_irr, L_nc
    """
    # ... exact arithmetic proof ...
    return _result(
        name='T_Born: Born Rule from Admissibility',
        status='PASS',
        dependencies=['T2', 'L_irr', 'L_nc'],
        ...
    )
```

All checks return a dict with `name`, `status`, `dependencies`, and `summary`. All arithmetic uses `fractions.Fraction` — no floating-point approximations in core checks.

`apf/bank.py` maintains a registry of all theorems. `run_all()` runs everything and returns a summary.

### Check Function Naming Conventions

| Prefix | Type | Count |
|---|---|---|
| `T_` or `T{n}` | Theorem | 89 |
| `L_` | Lemma | 211 |
| `RT_` | Red-team adversarial | 24 |
| Other (`A1`, `M`, `Delta_*`, etc.) | Axiom/proposition/example | 25 |

---

## Key Numbers to Know

| Quantity | Value | Source |
|---|---|---|
| κ (enforcement multiplier) | 2 | T_kappa (derived) |
| x (Gram overlap) | 1/2 | L_Gram + T27c (derived) |
| C_total (enforcement cost) | 61 | L_count (rigid) |
| N_gen (generations) | 3 | T7 (derived) |
| sin²θ_W | 3/13 ≈ 0.2308 | L_Cauchy_uniqueness (derived) |
| M_R spectrum | [31, 61, 177] GeV | L_hierarchy_cascade |
| Σm_ν | 58.8 meV | L_sum_mnu_cosmo |

---

## Common Tasks and How to Approach Them

### "Check whether theorem X is circular"
1. Read the `check_X` function and its docstring
2. Extract the `dependencies` list
3. For each dependency, repeat recursively
4. Look for any dependency that itself depends (directly or indirectly) on X
5. Also check whether any input to the proof is "physics" that hasn't been derived from A1

### "Explain how the gauge group is derived"
Read in order:
1. `check_Theorem_R()` in `apf/gauge.py` — the three carrier requirements
2. `check_L_gauge_template_uniqueness()` — 17-algebra scan
3. `check_T_gauge()` — cost minimization to N_c = 3
4. `check_T_field()` — fermion content

### "Add a new theorem"
1. State the theorem precisely (what it claims, what it uses)
2. List all imports beyond A1+MD+BW explicitly
3. Write the check function with exact arithmetic
4. Add to `bank.py` registry
5. Run `scripts/verify_all.py`

### "Find weak points in the framework"
Start with `apf/red_team.py` — this is the self-adversarial module. Look for:
- Checks with documented caveats in their docstrings
- Any theorem labelled [C] (conjecture) in the bank
- The κ = 2 derivation (`check_T_kappa()`) — acknowledged most important stress test
- Theorem_R Step 4 — documented weak link for R1

### "Compare APF to experiment"
Start with `apf/validation.py` and `papers/paper13/main.tex`. The prediction catalog lists all 47 predictions with experimental values and error calculations.

---

## What APF Is and Is Not

**APF is:**
- A formal mathematical derivation program with machine-verified theorems
- A claim that quantum mechanics + Standard Model structure follows from A1
- Accompanied by specific, falsifiable quantitative predictions
- In an active development phase (Papers 3–7 not yet complete)

**APF is not:**
- A theory of everything in the string-theory sense
- Claiming to derive Lagrangian dynamics from A1 alone (that is Papers 3–4)
- Claiming the κ = 2 derivation is beyond question (it is the most important gap to stress-test)
- Claiming completeness — open problems are documented honestly

---

## Honest Accounting of Open Problems

| Problem | Why It's Hard |
|---|---|
| m_c at 2.6% error | Five NNLO routes examined and rejected; Schur structural limit |
| m_t, m_b as anchors | Absolute mass scale requires σ field derivation |
| Dark matter particle ID | T12 proves existence + properties but not identity |
| DESI w ≠ −1 tension | 2.8–4.2σ tension growing; APF predicts w = −1 exactly |
| Derive spectral action formalism | Long-term mathematical program (like deriving Riemannian geometry from EEP) |

---

## Relationship to Other Reconstruction Programs

APF belongs to the same intellectual tradition as:
- **Hardy (2001)**: 5 axioms → quantum theory (APF compares favorably in assumption count)
- **Chiribella-D'Ariano-Perinotti (CDP)**: Operational axioms → quantum theory
- **Masanes-Müller**: Informational axioms → quantum theory

APF's distinguishing features:
1. A single *physical* axiom (not multiple operational axioms)
2. Extension to the Standard Model — QM reconstructions stop at Hilbert space
3. Machine-verified proofs in a public codebase
4. Quantitative predictions testable against experiment

---

## Vocabulary Quick Reference

| Term | Meaning |
|---|---|
| A1 | The single axiom: finite enforcement capacity |
| MD | Enforcement isotropy (regularity input) |
| BW | Budget-window richness (regularity input) |
| [P] | Proved — derivable from A1+MD+BW |
| [C] | Conjecture — stated, not yet proved |
| [RT] | Red-team adversarial check |
| enforcement | Any process maintaining a physical distinction |
| D-quotient | Space of maintained distinctions |
| C_total = 61 | Total enforcement cost (rigid) |
| x = 1/2 | Single-channel Gram overlap (derived) |
| κ = 2 | Enforcement multiplier (derived) |
| Theorem_R | Three carrier requirements → gauge group |
| L_count | C = 45+4+12 = 61 (rigid, all predictions follow) |
| M_R | Right-handed neutrino masses [31, 61, 177] GeV |
| σ | Admissibility scalar field (BSM — testable) |
| FN mechanism | Froggatt-Nielsen — superseded by L_multiplicative_amplitude |

---

*Last updated to reflect APF v6.7 (349 checks, 312 theorems in bank).*
