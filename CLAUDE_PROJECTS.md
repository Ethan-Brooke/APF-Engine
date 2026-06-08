# APF Orientation Guide — Claude Projects

*This guide is written for an AI assistant (Claude) being set up to help with Admissibility Physics Framework research via Claude Projects.*

---

## How to Load This Repository Into Claude Projects

1. Go to claude.ai → Projects → New Project
2. Name it "APF Research" (or similar)
3. Upload all files in this repository to the project knowledge base:
   - All `.py` files from `apf/`
   - All `.tex` files from `papers/`
   - This guide, `README.md`, and `SETUP.md`
4. Optionally add session transcripts from past work (helps Claude maintain continuity across sessions)

Once loaded, Claude can search and reference these files in every conversation within the project.

---

## What You Are Working With

You are assisting with the **Admissibility Physics Framework (APF)**, a single-axiom derivation of quantum mechanics and the Standard Model authored by E.S. Brooke (Ethan). The central claim is that Hilbert space structure, the Born rule, gauge group SU(3)×SU(2)×U(1), fermion content, and 47+ quantitative predictions all follow from one axiom:

> **A1:** Any physical distinction that can be maintained must be maintainable by a process with finite operational cost.

This is not speculative — it is a formal mathematics program. Every result is either:
- **[P] Proved** — derivable from A1 + two regularity inputs (MD, BW)
- **[C] Conjecture** — stated precisely, not yet proved
- **[RT] Red-team** — adversarial self-test that must pass to confirm no circular reasoning

The Python codebase (349 check functions) is the machine-verifiable companion to the papers. Every theorem in the LaTeX has a corresponding `check_` function.

---

## The File Map You Need to Know

### Papers (read these first for context)
| File | What it is |
|---|---|
| `papers/paper1/main.tex` | Paper 1: derives Hilbert space + quantum mechanics from A1 |
| `papers/paper1/supplement.tex` | 71-page formal supplement with all proofs |
| `papers/paper2/main.tex` | Paper 2: derives Standard Model gauge content + cosmology |
| `papers/paper2/supplement.tex` | Paper 2 proofs |
| `papers/paper13/main.tex` | TLS Concordance: precision prediction comparison |

### Code (the verification backbone)
| File | What it contains |
|---|---|
| `apf/core.py` | 48 checks — Paper 1 core. Start here. |
| `apf/bank.py` | Theorem registry. `run_all()` runs everything. |
| `apf/apf_utils.py` | Constants, utilities, DAG. Import from here. |
| `apf/gauge.py` | Gauge sector (sin²θ_W, α_s, M_W, gauge group derivation) |
| `apf/generations__8_.py` | Mass matrix, CKM, PMNS, neutrino masses (largest module) |
| `apf/cosmology.py` | Ω_Λ, Ω_m, η_B, CMB observables |
| `apf/gravity.py` | Einstein equations, black hole thermodynamics, inflation |
| `apf/majorana.py` | Seesaw mechanism, M_R spectrum |
| `apf/red_team.py` | 19 adversarial checks — look here for known weak points |
| `apf/supplements.py` | Extended lemma collection (73 checks) |
| `apf/validation.py` | Full prediction catalog with experimental comparisons |

---

## The Conceptual Architecture (Read This Before Diving Into Files)

### The Single Axiom
A1 says: enforcement capacity is finite. An "enforcement" is any physical process that maintains a distinction (a measurement, a constraint, a physical boundary). If you had infinite capacity you could maintain anything — but capacity is finite, so only certain distinctions are maintainable.

From this: the set of maintainable states must have structure. APF derives what that structure must be.

### The Five Layers

**Layer 0 — Admissibility Geometry**  
The foundational lemmas: `L_epsilon_star` (minimum enforcement cost), `L_NZ` (no-zero cost), `L_loc` (locality), `L_nc` (noncommutativity forced), `L_cost` (cost function uniqueness via Cauchy 1821), `L_irr` (irreducibility).

**Layer I — Quantum Mechanics**  
`T2`: enforcement geometry forces ℂ-Hilbert space (not ℝ or ℍ).  
`T3`: noncommutativity of enforcement operators → quantum uncertainty.  
`T_Born`: the Born rule is the unique enforcement-invariant probability assignment.  
`T_Tsirelson`: Bell-inequality bound follows from enforcement budget constraints.

**Layer II — Standard Model**  
`Theorem_R`: three carrier requirements R1 (ternary/complex), R2 (chiral), R3 (abelian grading).  
`L_gauge_template_uniqueness`: scans all 17 compact simple Lie algebras; only SU(3)×SU(2)×U(1) template survives.  
`T_gauge`: cost optimization forces N_c = 3.  
`T_field`: exactly 45 fermions with correct representations.  
`L_count`: total enforcement cost C = 61 (rigid — changing any factor destroys all predictions).

**Layer III — Mass and Mixing**  
`L_Gram`, `T27c`: x = 1/2 (single-channel overlap).  
`L_multiplicative_amplitude`: x^q suppression from independence (replaces FN mechanism).  
`L_mass_from_capacity`: 11 quark/lepton masses from 2 anchors.  
`T_CKM`, `T_PMNS`: mixing matrices from capacity geometry.

**Layer IV — Cosmology**  
`L_equip` (horizon equipartition) → density fractions.  
`L_dark_budget` → Ω_DM, Ω_Λ, Ω_b.  
`L_equation_of_state` → w₀ = −1 exact.

### Key Design Decisions
- **D-quotient**: the space of maintained distinctions is a quotient construction. This is a *definitional commitment*, not a no-hidden-variables axiom.
- **κ = 2**: the enforcement multiplier κ = 2 is the framework's most important single number. `check_T_kappa()` derives it. If you find a gap here, it matters.
- **C_total = 61**: the total enforcement cost is rigid. Adding or removing any Standard Model sector changes C and destroys the prediction chain.
- **Import discipline**: every theorem is labelled [P] (proved from A1) or notes its imports explicitly. The goal is zero imports. As of v6.7, one conjecture [C] remains.

---

## How Ethan Works (Working Style Notes)

Understanding the author's working style helps you assist effectively:

**Directive and terse.** Approves or declines with single words ("proceed," "thoughts?"). Don't pad responses with summaries of what you're about to do — just do it.

**Audit before fixing.** Before implementing any change to a proof or theorem, Ethan wants an honest gap assessment. "Here is what is missing / weak / circular" before "here is my fix."

**Red-team framing.** Treat every theorem claim with a hostile reviewer mindset. Ask: is this circular? Does it import anything unacknowledged? Would this survive a peer review attack?

**Exact arithmetic.** All theorem checks use `fractions.Fraction` for exact rational arithmetic. Floating-point "close enough" is not acceptable for core results.

**LaTeX compile discipline.** Three sequential `pdflatex` passes. Check `grep -E "^!"` for errors. Check `grep "Rerun\|undefined"` for convergence. Use `str_replace` not `sed` for LaTeX edits.

**Phase-gated work.** Large restructuring is broken into named phases with explicit checkpoints. Don't splice restructuring into ongoing work.

**No version references in documents.** Papers present as current work, not "version X."

---

## Suggested First Tasks When Starting a Session

### If continuing existing work:
1. Ask Ethan what the current task is
2. Check relevant files for current state before proposing anything
3. Run relevant checks to confirm current passing state

### If doing a fresh audit:
```
Read apf/red_team.py and list any [RT] checks that are currently flagged 
as weak or have documented caveats. Then check apf/bank.py for any 
theorems not yet labelled [P].
```

### If asked to add a theorem:
1. Draft the statement and proof in plain English first
2. Identify all imports (what does the proof assume beyond A1+MD+BW?)
3. Write the `check_` function with exact arithmetic
4. Add it to `bank.py` registry
5. Run `verify_all.py` to confirm no regressions

### If asked to edit a LaTeX file:
1. Read the relevant section first with the `view` tool
2. Grep for the exact string before using `str_replace`
3. Compile with three pdflatex passes
4. Check compile log for errors and undefined references

---

## The Things Most Likely to Go Wrong

**Circular imports.** The most dangerous bug pattern. If a theorem in Paper 1 imports a result that depends on Paper 2, that's a series-level circularity. Always trace the full dependency chain.

**Wayfinding vs. content gaps.** Many reviewer complaints are reading-experience failures — the proof exists but is unreachable. Before concluding something is missing, check whether it exists but is buried.

**κ = 2 derivation.** The most important single result to stress-test. `check_T_kappa()` in `core.py`. Read the full derivation before touching anything upstream.

**DESI dynamical DE tension.** As of v6.7, the DESI DR2 data shows 2.8–4.2σ preference for evolving dark energy (w ≠ −1). APF predicts w₀ = −1 exactly. This is a live tension — watch `L_DESI_DR2_confrontation` in `supplements.py`.

**m_c at 2.6%.** The charm quark mass error is irreducible (Schur structural limit). Don't try to "fix" this — it's been verified that no 5 NNLO routes close the gap further.

---

## Vocabulary Reference

| Term | Meaning |
|---|---|
| A1 | The single axiom: finite enforcement capacity |
| MD | Enforcement isotropy (regularity input) |
| BW | Budget-window richness (regularity input) |
| [P] | Proved from A1+MD+BW |
| [C] | Conjecture — stated precisely, not yet proved |
| [RT] | Red-team adversarial check |
| C_total | Total enforcement cost = 61 (rigid) |
| x = 1/2 | Single-channel Gram overlap (derived) |
| κ = 2 | Enforcement multiplier (derived in T_kappa) |
| FN mechanism | Froggatt-Nielsen — replaced by L_multiplicative_amplitude |
| D-quotient | Space of maintained distinctions (definitional) |
| Theorem_R | Carrier requirements R1/R2/R3 → gauge group |
| L_gauge_template_uniqueness | Proves SU(N_c)×SU(2)×U(1) is unique template |
| T_field | Derives 45 fermions with correct representations |
| L_count | C = 45+4+12 = 61 (rigid) |
| M_R | Right-handed neutrino mass spectrum [31, 61, 177] GeV |
| σ | Admissibility scalar field (BSM prediction) |

---

## What APF Does Not Claim

- It does not claim to be a theory of everything in the string-theory sense
- It does not claim to derive the dynamics (Lagrangian) from A1 alone — this is Papers 3–4
- It does not identify the dark matter particle (T12 derives existence + properties)
- It does not claim the κ = 2 derivation is unassailable — this is acknowledged as the most important stress test
- It does not claim Papers 2–7 are complete — they are in various stages of development

---

*Last updated to reflect APF v6.7 (349 checks, 312 theorems in bank).*
