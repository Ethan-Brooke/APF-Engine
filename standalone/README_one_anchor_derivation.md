# Complete Derivation Package — "The One Anchor"

A single self-contained, peer-reviewable artifact for the result that reduces the Admissibility
Physics Framework to **one input** — the absolute Planck magnitude, equivalently the size of the
de Sitter universe — with **zero free dimensionless parameters**, predicting α_s(M_Z) from capacity
alone. Codebase anchor: **v24.3.192** (EXPECTED 3675 = REGISTRY 3675, gap 0).

## What it is

`derive_one_anchor.py` walks the whole arc end-to-end, in order, printing each step's derived value,
the measured comparator, the % match, the epistemic grade, and the bank-witness / paper provenance.
It asserts every target and exits 0 iff all checks pass (currently **11/11 PASS**). It is the story in
one place; the 3,675-check bank verifies the same facts module by module (witness names are cited at
each step so a reviewer can cross-check).

Dependencies: **Python standard library only** (`math`). No numpy, no framework imports — a reviewer
can drop the single file anywhere and run it.

```
python3 derive_one_anchor.py
```

## The chain (sections of the script)

0. **Primitive structural inputs** — the integers C_total=61, d_eff=102, N_c=3, N_gen=3,
   sin²θ_W=3/13, and the SM one-loop β-coefficients. These are *outputs of the upstream single-axiom
   chain* (A1 → L_nc → Theorem_R → T_gauge → T_field → L_count; Papers 1–18) and are **taken as
   established** here, with provenance cited per line. This package derives the closure *from* them.
1. **Capacity entropy** S_dS = C_total·ln(d_eff); the unique intensive quantum σ = ln(d_eff).
2. **β-tiling** 6|b₃|=42, 6|b₂|=19, 6|b_Y|=d_eff−C_total=41 — three independent equations, each forcing
   N_gen=3; the three tile d_eff=102.
3. **Crossing coupling** 1/α_cross = (C_total/6)·ln(d_eff) = S_dS/6 = 47.02 — the gauge-coupling
   *normalization*, derived from capacity counts, no measured coupling (25.6 ppm).
4. **m=0 rank-1 collapse** — the competition matrix A=[[1,x],[x,x²+m]] is rank 2 for SU(3)/SU(2)
   (m=8,3) and **rank 1 for U(1)** (m=0).
5. **Abelian capacity count** 1/α_Y(M_cross) = S_dS/σ = C_total = 61 — the rank-1 mode counts capacity
   *channels*, not σ-entropy per mode (a channel count, not a second entropy scale).
6. **PREDICTION** — with the derived crossing coupling, sin²θ_W=3/13, and 1/α_Y=C_total, the running
   distance is pinned and **α_s(M_Z) = 0.1179 to 0.00%**, 1/α₂(M_Z)=29.59, from **zero measured
   coupling** (α_s is the output).
7. **EW floor** v_H = M_Pl·√N_c·(4π)⁻¹·102⁻⁸·(12/7) = 246.22 GeV — every O(1) factor forced; the one
   dimensional input M_Pl enters here only, to convert capacity to GeV.
8. **The one anchor** — the rescaling no-go (M_Pl→λM_Pl leaves all dimensionless predictions
   invariant → the magnitude is the one irreducible input); and its name: the horizon area
   A/4ℓ_P² ≈ 102⁶¹ ⇒ R/ℓ_P = √(102⁶¹/π) ≈ 10⁶¹ (size of the universe), Planck length as the pixel.
9. **Parameter count** — 0 free dimensionless + 1 dimensional anchor.

## Epistemic discipline (for the reviewer)

- **[P]** = proved from A1. **[P_structural]** = a structural argument at the level of
  `L_coupling_capacity_id` (itself banked [P]), **carried by its validating prediction**, not reduced
  to a more elementary proof. The rank-1 capacity count (§5) is the newly-proposed principle of this
  arc; its validation is the zero-input α_s prediction to 0.00% (§6), exactly as the 25.6 ppm
  crossing-coupling match validates the non-abelian principle.
- **Honest non-claims** (asserted in the script's footer):
  - The Planck magnitude is **not derived** — it is the one irreducible input, by dimensional
    analysis. Its most physical name is the size of the universe.
  - α_s is an **output** (predicted), never consumed; measured values are comparators throughout.
  - No measured coupling enters anywhere in §§1–6.

## Scope (what is and isn't in this file)

In-package: the gauge-sector closure, the one-anchor reduction, and the α_s prediction, derived
end-to-end from the capacity ledger. Cited upstream (not re-derived here): *why* C_total=61, d_eff=102,
N_c=3, sin²θ_W=3/13 — those live in Papers 1–18 and their bank checks. A reviewer wanting the full
chain to A1 follows the cited witnesses; this package is the self-contained closure that the
v24.3.186–192 arc added on top.

## Companion reference notes (prose)

`The Electroweak-Planck Hierarchy as Capacity Suppression`, `The Hadronic Running as Capacity-Counted
Distinction Density`, `The Planck Magnitude as the Single Dimensional Anchor`, `The Muon g-2 HVP as
Capacity-Counted Distinction Density`, `The Gauge Coupling Normalization Audit`, `The One Anchor as the
Size of the Universe` (all under `APF Reference Docs/`, dated 2026-05-30).
