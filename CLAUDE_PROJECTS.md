# APF Orientation Guide — Claude Projects

*This guide is for an AI assistant being set up to help with Admissibility Physics Framework research through Claude Projects. It explains how to load the repository into a project, what you are working with, and the few rules that will bite you if you skip them.*

---

## Loading the repository into a Claude Project

1. Go to claude.ai → Projects → New Project, and name it "APF Research" (or similar).
2. Add the repository files to the project knowledge base. The high-value set is the `apf/` package, this guide, `README.md`, `SETUP.md`, and `CORE_PACKAGE_README.md` (the tight model-spine subset, for a limited file-count budget).
3. Optionally add recent session transcripts. They help maintain continuity across conversations.

Once loaded, the assistant can search and reference these files in every conversation in the project. The codebase itself is the specification; the papers are prose guides to reading it.

---

## What you are working with

You are assisting with the **Admissibility Physics Framework (APF)**, a single-primitive derivation of the quantum formalism and the Standard Model. The central claim is that complex Hilbert space, the Born rule, the gauge group SU(3) × SU(2) × U(1), the fermion content, and a few dozen quantitative predictions all follow from one primitive:

> **A1:** At every causally connected region, the total enforcement cost of maintaining physical distinctions is bounded above by a finite capacity.

Three regularity conditions complete it, packaged as the **Principle of Least Enforcement Cost (PLEC)**: a positive cost floor (MD), argmin selection over the admissible set (A2), and a non-degenerate cost spectrum (BW). From these the framework forces the gauge group, three generations of 45 fermions, the rigid capacity ledger C_total = 61, sin²θ_W = 3/13 as a source value, Ω_Λ = 42/61, and the rest of the constants map — with zero free dimensionless parameters and one dimensional anchor (the Planck magnitude).

The Python codebase is the machine-verifiable companion. As of v24.3.249 it carries **3,745 bank-registered theorems across 422 typed modules**, every load-bearing claim traced to a named `check_` function, with exact rational arithmetic in the core.

---

## The single source of truth

For working instructions — file locations, conventions, working rules, the live bank state, and the startup/signoff procedures — the canonical file is `__APF Library/CLAUDE.md` on the project Drive. Read it at the start of any APF session. This guide orients a fresh assistant; `CLAUDE.md` governs the work. If anything here and there ever disagree, `CLAUDE.md` wins.

---

## Where the codebase lives, and the one rule that bites

On 2026-06-08 the codebase moved off Google Drive into a git repository. The science did not change; where the code lives, and how you save your work, did.

- **Live tree (edit here):** `Dev/apf-codebase` on the principal machine — git repo, remote `Ethan-Brooke/APF-Engine`, branch `main`.
- **Frozen mirror (never edit):** the Drive copy under `__APF Library/Codebase/`. It is archival, read-only.
- **The rule:** run every `git` operation — add, commit, push — in a **native shell on the principal machine**, never through a sandbox mount. The sandbox bridge corrupts `.git/index`, and the remote is unreachable from inside a sandbox. A session may edit files and stage a commit message; the actual `git add && git commit && git push` runs natively. **The commit is the archive** — there is no separate zip-snapshot step for code.

---

## The code architecture

Every result is a `check_` function returning a dict with at least a name, a status, its dependencies, and a one-line summary. Core checks use `fractions.Fraction` — exact rational arithmetic, no floating-point "close enough." Modules register their checks at import; `apf/_module_manifest.py` is the canonical module index and the source of the expected registry size; `verify_all.py` runs everything and prints the scorecard.

```
apf/                    the theorem bank — one module per result; registers at import
apf/_module_manifest.py the canonical module index + MODULE_TYPES taxonomy
scripts/                utilities and orchestration
standalone/             standalone lemma modules
examples/               worked examples
verify_all.py           runs the full bank and prints the scorecard
```

Theorems are `T_…`, lemmas are `L_…`. Every claim carries an epistemic grade: `[P]` (proved from A1), `[P_structural]` (proved up to a named structural reading), `[P+tool]`/`[P+lattice]` (proved but consuming an external import), `[C]` (conjecture). Read the grade before the result.

---

## How Ethan works

**Directive and terse.** Approves or redirects in a few words. Don't pad responses with previews of what you are about to do — do it, then show the result.

**Audit before fixing.** Before changing a proof or theorem, give an honest gap assessment first — what is missing, weak, or circular — then the fix.

**Red-team posture.** Treat every claim as a hostile reviewer would. Is it circular? Does it import anything unacknowledged? Would it survive review?

**Exact arithmetic.** Core checks use `fractions.Fraction`. Floating-point "close enough" is not acceptable for load-bearing results.

**Compile discipline.** For LaTeX, run the passes needed for cross-references to settle and check the log for errors and undefined references. Apply edits directly, then show the compiled result — no long "here is what I changed" recaps.

**No version references in body prose.** Papers and docs present as current work, not "version X." Version history lives in changelogs and title blocks.

---

## Suggested first tasks

**Continuing existing work.** Ask what the current task is, read the relevant files for their current state before proposing anything, and run the relevant checks to confirm the passing baseline.

**A fresh audit.** Read the adversarial checks and list any flagged as weak or carrying caveats, then look for any claim still graded `[C]` and any `[P_structural]` seam that has drifted toward over-grading.

**Adding a theorem.** Draft the statement and proof in plain English; identify every import beyond A1+MD+BW; write the `check_` function with exact arithmetic; register it; run `verify_all.py` and confirm the expected count moved by exactly one with no regressions.

---

## The things most likely to go wrong

**Circular imports.** The most dangerous pattern. A Paper-1 result that depends on a Paper-2 result is a series-level circularity. Trace the full dependency chain.

**Wayfinding versus content gaps.** Many "missing" results exist but are buried. Before concluding something is absent, check whether it is merely unreachable.

**Over-grading a structural seam.** `[P_structural]` means closure on the present axioms with a named residual. The measured weak mixing angle is the canonical example — the source value 3/13 is `[P]`, the measured/effective angle stays `[P_structural]` behind the w ∝ g² dictionary. Don't quietly promote it.

**Editing the wrong copy.** Edit the live git tree, not the frozen Drive mirror. And don't run git through a sandbox mount.

---

## What APF does not claim

It does not claim to be a theory of everything in the string-theory sense. It does not derive Lagrangian dynamics from A1 alone. It does not identify the dark-matter particle (existence and properties, yes; identity, no). And it does not pretend the absolute Planck magnitude is derived — that is the one dimensional anchor, open by design. The open seams are stated, not hidden.

<!-- FOOTER:start -->
---

## About the APF series

The Admissibility Physics Framework is a constraint-first derivation of the Standard Model and cosmological structure from a single primitive — finite enforcement capacity. The corpus runs from the foundational papers through the gauge sector, the quantum formalism, Lorentzian spacetime and the Einstein field equations, the cosmological constant, the electroweak and dark sectors, and the lattice Yang–Mills program. Each paper's main text and Technical Supplement is deposited separately on Zenodo and collected in the **[admissibility_physics](https://zenodo.org/communities/admissibility_physics)** community. The engine in this repository is the machine-verifiable companion to all of it (v24.3.249 — 3,745 bank-registered theorems across 422 typed modules, 48 quantitative predictions).

| # | Title | Concept DOI |
|---|---|---|
| Engine | Admissibility Physics — Unified Theorem Bank & Verification Engine | [10.5281/zenodo.18529115](https://doi.org/10.5281/zenodo.18529115) |
| 0 | What Physics Permits: A Constraint-First Framework for Physics | [10.5281/zenodo.18439523](https://doi.org/10.5281/zenodo.18439523) |
| 1 | The Enforceability of Distinction | [10.5281/zenodo.18439200](https://doi.org/10.5281/zenodo.18439200) |
| 2 | Finite Admissibility and the Failure of Global Description | [10.5281/zenodo.18439274](https://doi.org/10.5281/zenodo.18439274) |
| 3 | Entropy, Time, and Accumulated Cost | [10.5281/zenodo.18439363](https://doi.org/10.5281/zenodo.18439363) |
| 4 | Admissibility Constraints and Structural Saturation | [10.5281/zenodo.18439397](https://doi.org/10.5281/zenodo.18439397) |
| 5 | Quantum Structure from Finite Enforceability | [10.5281/zenodo.18439433](https://doi.org/10.5281/zenodo.18439433) |
| 6 | Dynamics and Geometry as Optimal Admissible Reallocation | [10.5281/zenodo.18439445](https://doi.org/10.5281/zenodo.18439445) |
| 7 | A Minimal Quantum of Action from Finite Admissibility | [10.5281/zenodo.18439513](https://doi.org/10.5281/zenodo.18439513) |
| 8 | The Admissibility-Capacity Ledger | [10.5281/zenodo.19721384](https://doi.org/10.5281/zenodo.19721384) |
| 9 | The Geometric Substrate as Cost Structure of Comparison Continuations | [10.5281/zenodo.20041675](https://doi.org/10.5281/zenodo.20041675) |
| 10 | The Calculus of Finite Continuability | [10.5281/zenodo.20041680](https://doi.org/10.5281/zenodo.20041680) |
| 11 | Forced Universality from Capacity-Bounded Admissibility | [10.5281/zenodo.20684198](https://doi.org/10.5281/zenodo.20684198) |
| 13 | The Minimal Admissibility Core | [10.5281/zenodo.18361446](https://doi.org/10.5281/zenodo.18361446) |
| 16 | Markov Breakdown and the Hard Problems | [10.5281/zenodo.20684207](https://doi.org/10.5281/zenodo.20684207) |
| 18 | The Electroweak Sector as a Capacity Equilibrium | [10.5281/zenodo.20684209](https://doi.org/10.5281/zenodo.20684209) |
| 20 | The Enforcement Crystal | [10.5281/zenodo.18531732](https://doi.org/10.5281/zenodo.18531732) |
| 21 | APF Engine — Unified Theorem Bank and Verification Engine | [10.5281/zenodo.18529115](https://doi.org/10.5281/zenodo.18529115) |
| 24 | The Recruitment-Radius Extension — Foundations | [10.5281/zenodo.20684211](https://doi.org/10.5281/zenodo.20684211) |
| 28 | Absolute Mass Scales from Electroweak Capacity Saturation | [10.5281/zenodo.20684215](https://doi.org/10.5281/zenodo.20684215) |
| 29 | Plaquette Representation Dominance and Confinement | [10.5281/zenodo.20684218](https://doi.org/10.5281/zenodo.20684218) |
| 30 | A Tube Mechanism for the Lattice Mass Gap | [10.5281/zenodo.20684220](https://doi.org/10.5281/zenodo.20684220) |
| 31 | Osterwalder–Schrader Structure of Lattice Yang–Mills | [10.5281/zenodo.20684222](https://doi.org/10.5281/zenodo.20684222) |
| 33 | Trace-to-Scheme Export Architecture | [10.5281/zenodo.20684224](https://doi.org/10.5281/zenodo.20684224) |
| 35 | The Dark Sector as a Two-Role Capacity Decomposition | [10.5281/zenodo.20684228](https://doi.org/10.5281/zenodo.20684228) |
| 40 | Between Symmetry and the Void — The Thermodynamics of Finite Distinction | [10.5281/zenodo.20684235](https://doi.org/10.5281/zenodo.20684235) |
| 41 | The Horizon as a Continuation Ledger | [10.5281/zenodo.20684241](https://doi.org/10.5281/zenodo.20684241) |
| 42 | The Weak Mixing Angle Is Not Free | [10.5281/zenodo.20684245](https://doi.org/10.5281/zenodo.20684245) |

Concept DOIs always resolve to the latest version. Technical Supplements are deposited as linked records — `isSupplementTo` the main paper, `isDocumentedBy` the companion repository.

## Author

Ethan Brooke — Independent Researcher, San Anselmo, California, USA.

- ORCID: [0009-0001-2261-4682](https://orcid.org/0009-0001-2261-4682)
- LinkedIn: [linkedin.com/in/ethanbrooke](https://www.linkedin.com/in/ethanbrooke/)
- GitHub: [github.com/Ethan-Brooke](https://github.com/Ethan-Brooke)
- Contact: brooke.ethan@gmail.com

License: CC-BY-4.0.
<!-- FOOTER:end -->
