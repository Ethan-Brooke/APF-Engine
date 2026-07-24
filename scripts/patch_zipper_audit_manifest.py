#!/usr/bin/env python3
"""One-shot patch for the unbanked zipper audit-candidate manifest.

This script is intentionally idempotent. It records the zipper candidate modules
in ``apf._module_manifest`` without adding them to BANK_LOAD_MODULES,
ALL_MODULES_VERIFY_ORDER, MODULE_TYPES, or the theorem registry.
"""
from __future__ import annotations

from pathlib import Path

PATH = Path("apf/_module_manifest.py")
CANDIDATES = (
    "apf.zipper_clearance_occupancy",
    "apf.zipper_reduction",
    "apf.zipper_reflection_bridge",
    "apf.zipper_bridge_bank_concordance",
    "apf.zipper_reduction_frontier",
)


def main() -> int:
    text = PATH.read_text(encoding="utf-8")
    original = text

    text = text.replace("Four categories\n---------------", "Five categories\n---------------", 1)

    description_anchor = (
        "``STANDALONE_LEMMA_MODULES`` (4 modules)\n"
        "    Standalone-lemma modules under ``apf/standalone/``. Have check_* defs but\n"
        "    don't use the ``register(registry)`` contract. Listed in ``verify_all.MODULES``\n"
        "    for scorecard enumeration; NOT loaded by ``bank._load()``.\n\n"
    )
    description = (
        "``AUDIT_CANDIDATE_MODULES`` (5 modules)\n"
        "    Explicitly unbanked research/audit candidates. They are named here so\n"
        "    repository census tooling cannot silently miss them, but they are excluded\n"
        "    from ``BANK_LOAD_MODULES``, ``ALL_MODULES_VERIFY_ORDER``, ``MODULE_TYPES``,\n"
        "    and the production theorem registry. Dedicated CI invokes them directly.\n\n"
    )
    if description not in text:
        if description_anchor not in text:
            raise SystemExit("manifest description anchor not found")
        text = text.replace(description_anchor, description_anchor + description, 1)

    tuple_block = (
        "\n\n# Unbanked zipper research packet. Deliberately excluded from the production\n"
        "# bank load, standard verify_all scorecard, module-type crystal, and registry.\n"
        "# Dedicated audit CI imports and executes these modules explicitly.\n"
        "AUDIT_CANDIDATE_MODULES: tuple[str, ...] = (\n"
        + "".join(f'    "{name}",\n' for name in CANDIDATES)
        + ")\n"
    )
    insertion_anchor = (
        "STANDALONE_LEMMA_MODULES: tuple[str, ...] = (\n"
        "    \"apf.standalone.L_Cauchy_uniqueness\",\n"
        "    \"apf.standalone.L_CKM_resolution_limit\",\n"
        "    \"apf.standalone.phase1_seesaw_closure\",\n"
        "    \"apf.standalone.phase5_theorem_R_audit\",\n"
        ")\n"
    )
    if "AUDIT_CANDIDATE_MODULES: tuple[str, ...]" not in text:
        if insertion_anchor not in text:
            raise SystemExit("standalone tuple anchor not found")
        text = text.replace(insertion_anchor, insertion_anchor + tuple_block, 1)

    if text == original:
        print("zipper audit candidate manifest already current")
        return 0

    PATH.write_text(text, encoding="utf-8")
    print("patched", PATH)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
