# APF_LATTICE_CONSTRAINT_MANIFEST_v0.1

**Build date:** 2026-05-12
**Build stage:** Stage 0 — constraint manifest (prerequisite for Stage 1 validator).
**Codebase:** APF_Codebase_v24.1 (setup.py 24.2.0, EXPECTED_THEOREM_COUNT = 2883).

## What this pack is

The structural reference for the **constraint cascade** that determines which flow configurations on the (61, 102) APF interface lattice are admissible.

The (61, 102) lattice is not an arbitrary representation — per `check_T_horizon_reciprocity` + `check_T_interface_sector_bridge`, it is *exactly* the space of second-epsilon commitment options per channel. Each cell $(i, j)$ represents the proposition "channel $i$ commits its $2\varepsilon$ to target $j$." Flow values in $[0, 1]$ encode the rate/probability of that commitment being active.

The manifest catalogs **37 constraints** across six categories (foundational / structural / coupling / sector-specific / admissibility / export), each with:

- `bank_witnesses` — the `check_*` functions that *prove* the constraint
- `scope` — `global` / `cell_level` / `row_constraint` / `block_constraint` / `block_coupling` / `row_block` / `cross_sector` / `composed` / `dimension_fix` / `per_export_route`
- `lattice_form` — how the constraint expresses on the (61, 102) lattice
- `failure_mode` — what a violating configuration looks like (where applicable)
- `epistemic_tag` — `[P]` / `[P_structural]` / `[P_internal_2FCR]` / `[P_theory]`

## What this pack is for

**Stage 1 (validator).** `apf/lattice_validator.py` will read `manifest.json` and produce `ValidationReport` instances. For each constraint, the validator runs a corresponding check on a proposed lattice configuration.

**Stage 2 (UI integration).** The lattice viz already exists as the Cowork artifact `apf-precision-physics-tracking`'s sibling; Stage 2 wires the validator's output back into a paintable lattice + violations overlay.

**Stage 3 (engineering generalization).** This manifest is the SM-specific template. For non-SM engineered systems (QEC codes, communication channels, etc.), the analog manifest would be derived from APF first principles for that system's lattice dimensions.

## Counts

- **Constraints by category:** {'foundational': 5, 'structural': 8, 'coupling': 6, 'sector_specific': 9, 'admissibility': 1, 'export': 8}
- **Constraints by scope:** {k: v for k, v in MANIFEST["constraint_count_by_scope"].items() if v > 0}

## Pack contents

```
APF_LATTICE_CONSTRAINT_MANIFEST_v0.1/
├── README.md                  ← this file
├── manifest.json              ← the structured data (JSON)
└── docs/
    └── COMPANION.md           ← long-form companion (semantics + scope categories + design notes)
```

## Gaps surfaced

The audit explicitly named **6 gaps** in lattice expressibility — places where the (61, 102) representation is partial rather than complete. See `manifest.json` field `gaps_in_lattice_expressibility` and `docs/COMPANION.md` § "Gaps in lattice expressibility" for the full list and implications.

## Next steps

1. Stage 1 validator implementation (`apf/lattice_validator.py` reading `manifest.json`).
2. Stage 2 UI integration (paint-and-validate workflow on the existing lattice viz).
3. Stage 3 engineering generalization (target engineered system to be selected).

## Deductive cascade

```
  A1 (single axiom: finite enforcement capacity)
  → 4-input declaration (A1 + 3 primitive commitments + finite-physical-regime hypothesis) [check_T_four_input_declaration]
  → PLEC anchors A1/MD/A2/BW derived [check_T_PLEC_derived_from_spine]
  → Capacity partition 3 + 16 + 42 = 61 [check_T11, check_T12, check_T_partition_rigidity_coverage_v69]
  → Structural identities: L_count, L_self_exclusion, T_horizon_reciprocity, T_interface_sector_bridge
  → Sector-specific content: gauge template, sin²θ_W, dark-sector minimal CDM, vacuum w_2(x)
  → Export gates G1–G6 per route
```

Every constraint above derives from this cascade. The manifest's job is to make the cascade machine-readable.
