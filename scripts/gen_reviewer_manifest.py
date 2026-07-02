#!/usr/bin/env python3
"""Generate the reviewer-facing IE atlas artifacts (Full Bank Onboarding, use 2).

LANDING ORDER: bump the manifest/setup FIRST, regenerate SECOND -- the emitted
reproduce line bakes EXPECTED_REGISTRY_SIZE and the header bakes PIN_VERSION;
generating before the bump ships stale numbers (audit catch, v24.3.324).

Emits, from repo root (PYTHONPATH=. python3 scripts/gen_reviewer_manifest.py):

  artifacts/ie_atlas_export.json   -- machine-readable: every atlas input with
                                      its verdict, axis, route, owner module,
                                      provenance note, covers; the coverage
                                      summary; the verdict-pin version.
  REVIEWER_ATLAS.md                -- human-readable: what APF claims through
                                      the Interface Engine, at what grade,
                                      with what obstruction -- grouped by
                                      sector and cross-indexed to the
                                      deposited papers (curated map).

CURRENCY GUARANTEE: the banked check_T_ie_reviewer_manifest_current fails the
bank if the committed export's verdicts drift from apf/ie_atlas_verdict_pin.py
-- the reviewer artifact cannot rot silently. Regenerate at re-pin (signoff
Step 8b) and commit both together.

HONESTY: the paper cross-index is a CURATED coverage map (which atlas inputs
bear on which deposited papers), not a completeness claim; the notes carried
per input are the declarations' own provenance text; verdicts inherit the
grades of the theorems they route through, and routing confers nothing.
"""
from __future__ import annotations

import json
import os
import sys
import tempfile
from datetime import date

#: Curated paper cross-index: concept-DOI papers <- atlas input-id prefixes.
#: Coverage map, not completeness: an input listed under a paper bears on that
#: paper's content; absence means only that no atlas input routes it yet.
PAPER_INDEX = (
    ("Paper 0 + Paper 13 (foundations)", ("foundation:",)),
    ("Paper 5 (quantum structure) + the FeasBool lane", ("quantum:", "contextuality:", "spine:", "witness:")),
    ("Paper 18 + Paper 42 + Paper 28 (EW sector)", ("ew:", "ew_eigenscreen:", "wtrace:", "payload:ew", "claim:ew")),
    ("Papers 29/30/31 (YM trilogy) + the gauge sector", ("strong:", "gauge:", "readout:", "claim:gauge")),
    ("Paper 35 (dark sector)", ("dark:", "claim:dark", "payload:dark")),
    ("Paper 41 + Paper 8 (horizon / ledger)", ("gravity:", "claim:horizon", "payload:gravity", "payload:cosmogenesis", "payload:evaporation", "payload:horizon")),
    ("Paper 33 (trace-to-scheme) + the mass sector", ("mass:", "flavour:", "neutrino:", "claim:mass", "payload:top_", "payload:charm", "payload:bottom", "payload:charged_lepton", "payload:light_quark")),
    ("Paper 21 / the Engine (everything; the atlas itself is its artifact)", ()),
)


def _rows():
    from apf.interface_atlas_live_runner import run_live_atlas
    res = run_live_atlas(atlas_name="reviewer_manifest_run")
    decls = {d["input_id"]: d for d in res.get("declaration_results", [])}
    out = []
    for r in res.get("all_summaries", []):
        iid = r["input_id"]
        d = decls.get(iid, {})
        out.append({
            "input_id": iid,
            "axis": r.get("axis", "ROUTE"),
            "route": r.get("route"),
            "solver_status": str(r.get("solver_status")),
            "export_global_P": bool(r.get("export_global_P")),
            "owner_module": d.get("owner_module"),
            "expect_export": d.get("expect_export"),
        })
    return sorted(out, key=lambda x: x["input_id"]), res


def build() -> None:
    from apf.ie_atlas_verdict_pin import PINNED_VERDICTS, PIN_VERSION
    from apf.ie_onboarding_registry import coverage_map, discover_ie_declarations
    rows, res = _rows()
    # tag legacy adapter-swap rows so bold EXPORT rows are never note-less
    adapter_note = {}
    for ar in res.get("adapter_results", []):
        adapter_note[ar.get("swapped_id")] = (
            "live adapter payload (swap of %s); imported/banked content and "
            "grades per its adapter module" % ar.get("original_id"))
    decl_notes = {}
    decls, _ = discover_ie_declarations()
    for owner, entries in decls.items():
        for d in entries:
            decl_notes[d["input_id"]] = {"note": d.get("note"),
                                          "covers": list(d.get("covers", ()) or ())}
    for r in rows:
        r.update(decl_notes.get(r["input_id"], {}))
        if not r.get("note") and r["input_id"] in adapter_note:
            r["note"] = adapter_note[r["input_id"]]

    cov = coverage_map()["summary"]
    export = {
        "generated": date.today().isoformat(),
        "pin_version": PIN_VERSION,
        "coverage_summary": cov,
        "how_to_regenerate": "PYTHONPATH=. python3 scripts/gen_reviewer_manifest.py "
                              "(after: python3 verify_all.py --bank-audit)",
        "verdict_semantics": {
            "export_global_P=True": "the route exports a global section in the "
                                     "IE's own currency (a certified closure)",
            "export_global_P=False": "the route holds with a NAMED obstruction "
                                      "or as an honest open/held disposition -- "
                                      "obstructions are results, not defects",
        },
        "inputs": rows,
    }
    os.makedirs("artifacts", exist_ok=True)
    fn = "artifacts/ie_atlas_export.json"
    fd, tmp = tempfile.mkstemp(dir="artifacts", suffix=".tmp")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(export, f, indent=1, default=str)
    os.replace(tmp, fn)
    print("wrote", fn, "(%d inputs)" % len(rows))

    # ---- the human-readable manifest
    lines = []
    a = lines.append
    a("# APF Reviewer Atlas -- what the framework claims, machine-checked")
    a("")
    a("Generated %s against verdict pin v%s. Every row "
      "below is produced by running the banked engine, not written by hand; "
      "the committed copy is certified current against the verdict pin by "
      "`check_T_ie_reviewer_manifest_current` (a failing bank run means this "
      "file is stale)." % (export["generated"], PIN_VERSION))
    a("")
    a("**How to reproduce**: clone the repo, `python3 verify_all.py --bank-audit` "
      "(the full theorem bank, %d checks), then "
      "`PYTHONPATH=. python3 scripts/gen_reviewer_manifest.py`." % _expected())
    a("")
    a("**Reading a verdict**: `EXPORT` = the route exports a global section in "
      "the engine's own currency. `held/obstructed` = the route holds with a "
      "NAMED obstruction or an honest open disposition -- in this framework "
      "obstructions are results (e.g. a Bell/noncontextuality certificate, a "
      "no-go, an honest OPEN statement), not defects. Verdicts inherit the "
      "grades of the banked theorems they route through; routing confers "
      "nothing.")
    a("")
    a("**Coverage**: %d of %d loaded modules onboarded (%d directly), %d of %d "
      "on the physics target surface. Modules not onboarded are honestly so "
      "(pipeline stages of banked programs, or abstract interfaces with no "
      "payload data)." % (cov["modules_onboarded"], cov["modules_total"],
                          cov["modules_onboarded_direct"],
                          cov["target_surface_onboarded"], cov["target_surface_total"]))
    a("")
    used = set()
    for title, prefixes in PAPER_INDEX:
        sect = [r for r in rows if any(r["input_id"].startswith(p) for p in prefixes)]
        if not prefixes:
            sect = [r for r in rows if r["input_id"] not in used]
        for r in sect:
            used.add(r["input_id"])
        if not sect:
            continue
        a("## %s" % title)
        a("")
        a("| input | axis | verdict | note |")
        a("|---|---|---|---|")
        for r in sect:
            verdict = "**EXPORT**" if r["export_global_P"] else r["solver_status"]
            note = (r.get("note") or "").replace("|", "/")
            if len(note) > 140:
                note = note[:137] + "..."
            a("| `%s` | %s | %s | %s |" % (r["input_id"], r["axis"], verdict, note))
        a("")
    a("---")
    a("*The paper cross-index is a curated coverage map, not a completeness "
      "claim. Concept DOIs for all deposited papers: see the repo README / "
      "the Zenodo community `admissibility_physics`.*")
    fn = "REVIEWER_ATLAS.md"
    fd, tmp = tempfile.mkstemp(dir=".", suffix=".tmp")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    os.replace(tmp, fn)
    print("wrote", fn, "(%d lines)" % len(lines))


def _expected() -> int:
    from apf import _module_manifest as m
    return m.EXPECTED_REGISTRY_SIZE


if __name__ == "__main__":
    build()
    sys.exit(0)
