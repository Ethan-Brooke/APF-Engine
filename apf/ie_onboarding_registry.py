"""APF IE Onboarding Registry -- the bank->IE coverage instrument.

Full Bank Onboarding program, Phase 1 (2026-07-01). The program target, per the
principal's scoping: every bank module reachable through the Interface Engine
with an honest per-axis verdict (export of a global section vs a NAMED
obstruction), on a registration contract designed so that ADDING an interface
or an input is a declaration, never an engine edit.

What this module supplies
-------------------------
1. The IE_DECLARATIONS contract (new, multi-axis, additive). Any apf module
   may export::

       IE_DECLARATIONS: tuple[dict, ...]

   with each entry declaring one atlas input:

   ============== ========================================================
   field           meaning
   ============== ========================================================
   input_id        unique atlas input id (namespaced by convention:
                   "<sector>:<name>")
   axis            one of the live AxisKind values ("ROUTE" / "CODOMAIN" /
                   "CONTEXTUALITY" / "READOUT"). The registry reads the live
                   enum, so a future fifth axis needs NO edit here -- but it
                   does need its summarize_input dispatch branch in
                   interface_atlas.py; axis extension is an engine change,
                   input/interface extension is not
   claim_text      optional -- a CLAIM-kind input (structural probe)
   payload         optional -- a literal payload mapping
   payload_builder optional -- zero-arg callable returning the payload
                   (called lazily at compile time, not at import time)
   route           optional route tag (ROUTE axis)
   covers          optional tuple of apf module names whose bank content
                   this input onboards (coverage credit for sector
                   adapters that represent content living elsewhere)
   note            optional free-text provenance
   ============== ========================================================

   Exactly one of claim_text / payload / payload_builder must be supplied.
   The LEGACY single-input adapter contract (ATLAS_INPUT_ID / ATLAS_ROUTE /
   ATLAS_PAYLOAD_NAME / build_live_atlas_payload [+ ATLAS_AXIS], discovered by
   apf.interface_atlas_live_runner.discover_adapters) remains valid and is
   folded into the same coverage map; new work should prefer IE_DECLARATIONS.

2. The coverage map (``coverage_map()``): for every module in
   ``_module_manifest.MODULE_TYPES``, whether it is onboarded (exports
   IE_DECLARATIONS, conforms to the legacy contract, or is covered by another
   module's ``covers`` credit), which axes it feeds, and how many inputs.
   "Onboarded" means: AT LEAST ONE input routes SOME of this module's
   banked content through the IE -- a reachability bit, never a claim of
   content-complete coverage (the readout inputs onboard
   gauge_invariant_record's trichotomy slice, not its KS-coloring or CKM
   content). The onboarding TARGET SURFACE is the spine/sector/extension
   module types;
   engineering/infra/standalone are the machine itself and are reported but
   not targeted. The map is a measurement, not an aspiration: at Phase 1 the
   honest baseline is a small onboarded fraction -- the number the program
   exists to move.

3. The ratchet (``ONBOARDED_MODULE_FLOOR``): the banked check fails if the
   number of onboarded modules ever drops below the floor recorded at the
   last deliberate raise. Coverage can only regress loudly.

4. The banked structural check (``check_T_ie_onboarding_registry_coverage``,
   [P_structural_instrument], tier 4): certifies contract well-formedness,
   coverage-map exhaustiveness and internal consistency, the ratchet, the
   vendored v0.2 input set (42 inputs, unique ids, live-runner resolution to
   the in-repo module -- the Phase 0a fix), an END-TO-END EXTENSIBILITY
   WITNESS (a synthetic module carrying IE_DECLARATIONS flows through
   discovery -> compile -> summarize_input -> per-axis verdict with NO edit
   to any engine module), and JSON-serializability of the report (the
   dashboard contract).

Scope and honesty
-----------------
This is an INSTRUMENT. It certifies the onboarding machinery and measures
coverage; it asserts no physics. Verdicts delivered through the IE inherit
the grades of the banked theorems they route through; an input flowing
through this registry gains no epistemic status from the routing. The .290
scoping result stands: most bank interfaces are abstract (no correlator or
payload data), so onboarding is per-interface and per-axis -- a module with
nothing to feed an axis is honestly NOT onboarded on that axis, never
padded with a vacuous input.
"""

from __future__ import annotations

import importlib
import json
from typing import Any, Dict, List, Mapping, Tuple


# ---------------------------------------------------------------------------
# Contract constants
# ---------------------------------------------------------------------------

def _live_axes() -> Tuple[str, ...]:
    """Read the axis vocabulary from the live AxisKind enum.

    A new axis needs no registry edit, but DOES need its dispatch branch in
    interface_atlas.summarize_input -- the by-declaration extension claim is
    for interfaces and inputs, not axes."""
    from apf.interface_atlas import AxisKind
    return tuple(a.value for a in AxisKind)


#: Module types that constitute the onboarding target surface. The other
#: types (engineering / infra / standalone) are the machine, not the physics
#: surface, and are reported without being targeted.
TARGET_MODULE_TYPES: Tuple[str, ...] = ("spine", "sector", "extension")

#: The coverage ratchet. Compared against the covers-free DIRECT count
#: (modules that themselves export IE_DECLARATIONS or conform to the legacy
#: contract) so that covers-credit can never mask a regression. Measured at
#: v24.3.307 banking time: 33 conforming legacy adapters + the two axis
#: adapters carrying IE_DECLARATIONS (contextuality, readout). RAISED 35->39
#: at v24.3.310 (Wave 1b: core + gauge_invariant_record + yang_mills_md_bridge
#: + quantum_admissibility declare directly). Raise DELIBERATELY as onboarding
#: waves land; the banked check fails if the direct count drops below this
#: floor. Environmental import-skips (a module listed in MODULE_TYPES failing
#: to import in a degraded sandbox, e.g. numpy/scipy-less) are excluded from
#: the regression verdict Bucket-A style: they are REPORTED, and only a gap
#: not explained by import-skips fails the ratchet.
ONBOARDED_MODULE_FLOOR: int = 43  # raised at v24.3.313: cosmology + gravity + gauge (all spine) declare directly; prior raises .311 (ew_unitarity_eigenscreen) and .310 (Wave 1b)

_PAYLOAD_SOURCES = ("claim_text", "payload", "payload_builder")


# ---------------------------------------------------------------------------
# Declaration validation + discovery
# ---------------------------------------------------------------------------

def validate_declaration(decl: Mapping[str, Any], owner: str) -> List[str]:
    """Return a list of failure strings for one IE_DECLARATIONS entry."""
    fails: List[str] = []
    if not isinstance(decl, Mapping):
        return [owner + ": declaration is not a mapping: " + type(decl).__name__]
    input_id = decl.get("input_id")
    if not (isinstance(input_id, str) and input_id):
        fails.append(owner + ": missing/empty input_id")
    axis = decl.get("axis")
    axes = _live_axes()
    if axis not in axes:
        fails.append("%s:%s: axis %r not in live AxisKind %r" % (owner, input_id, axis, axes))
    supplied = [k for k in _PAYLOAD_SOURCES if decl.get(k) is not None]
    if len(supplied) != 1:
        fails.append("%s:%s: exactly one of %r required, got %r"
                     % (owner, input_id, _PAYLOAD_SOURCES, supplied))
    pb = decl.get("payload_builder")
    if pb is not None and not callable(pb):
        fails.append("%s:%s: payload_builder is not callable" % (owner, input_id))
    ee = decl.get("expect_export")
    if ee is not None and not isinstance(ee, bool):
        fails.append("%s:%s: expect_export must be a bool when present" % (owner, input_id))
    covers = decl.get("covers", ())
    if covers:
        if not all(isinstance(c, str) and c.startswith("apf.") for c in covers):
            fails.append("%s:%s: covers entries must be apf.* module names" % (owner, input_id))
        else:
            from apf import _module_manifest as manifest
            unknown = [c for c in covers if c not in manifest.MODULE_TYPES]
            if unknown:
                fails.append("%s:%s: covers targets not in MODULE_TYPES "
                             "(typo would silently drop credit): %r"
                             % (owner, input_id, unknown))
    return fails


def declarations_from_module(mod: Any) -> Tuple[Mapping[str, Any], ...]:
    """Extract the IE_DECLARATIONS tuple from an (already imported) module."""
    decls = getattr(mod, "IE_DECLARATIONS", None)
    if decls is None:
        return ()
    return tuple(decls)


def discover_ie_declarations() -> Tuple[Dict[str, Tuple[Mapping[str, Any], ...]], Dict[str, str]]:
    """Scan every manifest-listed module for the IE_DECLARATIONS contract.

    Returns (declarations_by_module, skipped_by_module). Import failures are
    recorded as skips (Bucket-A style), never raised: the coverage map must
    be computable in degraded environments.
    """
    from apf import _module_manifest as manifest
    found: Dict[str, Tuple[Mapping[str, Any], ...]] = {}
    skipped: Dict[str, str] = {}
    for mod_name in manifest.MODULE_TYPES:
        try:
            mod = importlib.import_module(mod_name)
        except Exception as exc:  # noqa: BLE001 -- degraded-env tolerance
            skipped[mod_name] = "import failed: %s" % exc
            continue
        decls = declarations_from_module(mod)
        if decls:
            found[mod_name] = decls
    return found, skipped


def discover_legacy_adapters() -> Tuple[Dict[str, Dict[str, Any]], Dict[str, str]]:
    """Fold the legacy 4-attribute adapter contract into the coverage view."""
    from apf.interface_atlas_live_runner import discover_adapters
    raw = discover_adapters()
    conforming: Dict[str, Dict[str, Any]] = {}
    skipped: Dict[str, str] = {}
    for key, info in raw.items():
        if key.startswith("_skipped:"):
            skipped["apf." + key[len("_skipped:"):]] = str(info.get("reason"))
        else:
            mod_name = info.get("module_name") or ("apf." + key)
            conforming[mod_name] = dict(info)
    return conforming, skipped


# ---------------------------------------------------------------------------
# Declaration -> AtlasInput compilation
# ---------------------------------------------------------------------------

def compile_declaration(decl: Mapping[str, Any]) -> Any:
    """Compile one IE_DECLARATIONS entry into an AtlasInput.

    CLAIM if claim_text is supplied; otherwise a payload input whose
    AtlasInputKind follows the axis (CODOMAIN -> CODOMAIN_PAYLOAD, everything
    else ROUTE_PAYLOAD -- the summarize_input dispatcher keys on ``axis``
    before ``kind``).
    """
    from apf.interface_atlas import AtlasInput, AtlasInputKind, AxisKind
    axis = AxisKind(decl["axis"])
    claim_text = decl.get("claim_text")
    if claim_text is not None:
        return AtlasInput(
            input_id=decl["input_id"], kind=AtlasInputKind.CLAIM, route=None,
            claim_text=claim_text, payload=None, axis=axis,
        )
    payload = decl.get("payload")
    if payload is None:
        payload = decl["payload_builder"]()
    kind = (AtlasInputKind.CODOMAIN_PAYLOAD if axis == AxisKind.CODOMAIN
            else AtlasInputKind.ROUTE_PAYLOAD)
    return AtlasInput(
        input_id=decl["input_id"], kind=kind, route=decl.get("route"),
        claim_text=None, payload=dict(payload), axis=axis,
    )


# ---------------------------------------------------------------------------
# The coverage map
# ---------------------------------------------------------------------------

def coverage_map(
    extra_declaration_modules: Tuple[Any, ...] = (),
) -> Dict[str, Any]:
    """Compute the bank->IE coverage map over MODULE_TYPES.

    ``extra_declaration_modules`` lets callers (and the extensibility witness)
    inject module OBJECTS carrying IE_DECLARATIONS without touching the
    manifest -- the add-an-interface path, exercised end-to-end.
    """
    from apf import _module_manifest as manifest
    decls, decl_skipped = discover_ie_declarations()
    legacy, legacy_skipped = discover_legacy_adapters()

    for mod in extra_declaration_modules:
        name = getattr(mod, "__name__", "<anonymous>")
        extra = declarations_from_module(mod)
        if extra:
            decls[name] = decls.get(name, ()) + extra

    # covers-credit: an input declared in module A may onboard module B content
    covered_by: Dict[str, List[str]] = {}
    for owner, entries in decls.items():
        for d in entries:
            for target in d.get("covers", ()) or ():
                covered_by.setdefault(target, []).append(d.get("input_id", "?"))

    rows: Dict[str, Dict[str, Any]] = {}
    axes = _live_axes()
    for mod_name in sorted(manifest.MODULE_TYPES):
        mtype = manifest.MODULE_TYPES[mod_name]
        mod_axes: List[str] = []
        n_inputs = 0
        if mod_name in legacy:
            mod_axes.append(str(legacy[mod_name].get("axis", "ROUTE")))
            n_inputs += 1
        for d in decls.get(mod_name, ()):
            if d.get("axis") in axes:
                mod_axes.append(d["axis"])
            n_inputs += 1
        credited = covered_by.get(mod_name, [])
        direct = bool(n_inputs)
        onboarded = direct or bool(credited)
        rows[mod_name] = {
            "module_type": mtype,
            "in_target_surface": mtype in TARGET_MODULE_TYPES,
            "onboarded": onboarded,
            "onboarded_direct": direct,
            "axes": sorted(set(mod_axes)),
            "input_count": n_inputs,
            "covered_by": credited,
        }

    n_total = len(rows)
    n_onboarded = sum(1 for r in rows.values() if r["onboarded"])
    n_direct = sum(1 for r in rows.values() if r["onboarded_direct"])
    target_rows = [r for r in rows.values() if r["in_target_surface"]]
    by_axis: Dict[str, int] = {a: 0 for a in axes}
    for r in rows.values():
        for a in r["axes"]:
            by_axis[a] = by_axis.get(a, 0) + 1
    summary = {
        "modules_total": n_total,
        "modules_onboarded": n_onboarded,
        "modules_onboarded_direct": n_direct,
        "modules_onboarded_via_covers": n_onboarded - n_direct,
        "target_surface_total": len(target_rows),
        "target_surface_onboarded": sum(1 for r in target_rows if r["onboarded"]),
        "modules_by_axis": by_axis,
        "declaration_modules": sorted(decls),
        "legacy_adapter_modules": sorted(legacy),
        "declaration_skips": decl_skipped,
        "legacy_skips": legacy_skipped,
        "onboarded_module_floor": ONBOARDED_MODULE_FLOOR,
        "target_module_types": list(TARGET_MODULE_TYPES),
        "axes": list(axes),
    }
    return {"rows": rows, "summary": summary}


# ---------------------------------------------------------------------------
# The banked structural check
# ---------------------------------------------------------------------------

def _extensibility_witness() -> List[str]:
    """The add-an-interface path, end to end, with no engine edit.

    Builds a synthetic module object exporting IE_DECLARATIONS with (a) a
    CONTEXTUALITY payload input (the CHSH-local table -- a known SepStr
    export) and (b) a CLAIM probe, with covers-credit onto apf.core; runs
    discovery-injection -> compile -> summarize_input; asserts per-axis
    verdicts and coverage credit.
    """
    import types
    from apf.interface_atlas import summarize_input

    fails: List[str] = []
    witness = types.ModuleType("_ie_onboarding_witness")
    witness.IE_DECLARATIONS = (
        {
            "input_id": "witness:chsh_local",
            "expect_export": True,
            "axis": "CONTEXTUALITY",
            "payload": {"contextuality_kind": "chsh_correlators",
                        "E": ["3/5", "3/5", "3/5", "3/5"]},
            "covers": ("apf.core",),
            "note": ("extensibility witness -- CHSH-local (all sign choices "
                     "give |S| = 6/5 <= 2, inside the Boole polytope), "
                     "expects SepStr export"),
        },
        {
            "input_id": "witness:claim_probe",
            "axis": "ROUTE",
            "claim_text": ("witness structural claim: the onboarding registry "
                           "compiles CLAIM declarations through the standard "
                           "route-adjudication path."),
        },
    )

    for d in witness.IE_DECLARATIONS:
        fails.extend(validate_declaration(d, witness.__name__))

    # compile + dispatch through the REAL engine entry point
    try:
        s_ctx = summarize_input(compile_declaration(witness.IE_DECLARATIONS[0]))
        if not s_ctx.export_global_P:
            fails.append("witness CHSH-local input did not export a global section")
        axis_val = getattr(getattr(s_ctx, "axis", None), "value", None)
        if axis_val not in (None, "CONTEXTUALITY"):
            fails.append("witness contextuality input bucketed wrong: %r" % axis_val)
        s_claim = summarize_input(compile_declaration(witness.IE_DECLARATIONS[1]))
        if not getattr(s_claim, "solver_status", None):
            fails.append("witness CLAIM input returned no solver_status verdict")
    except Exception as exc:  # noqa: BLE001
        fails.append("witness compile/dispatch raised: %s" % exc)

    # covers-credit visible in the coverage map, injected without manifest edit
    cov = coverage_map(extra_declaration_modules=(witness,))
    core_row = cov["rows"].get("apf.core")
    if core_row is None:
        fails.append("apf.core missing from coverage rows")
    elif "witness:chsh_local" not in core_row["covered_by"]:
        fails.append("covers-credit onto apf.core not recorded")
    if "_ie_onboarding_witness" in cov["rows"]:
        fails.append("synthetic witness module leaked into MODULE_TYPES rows")
    return fails


def check_T_ie_onboarding_registry_coverage() -> Dict[str, Any]:
    """T_ie_onboarding_registry_coverage: the bank->IE onboarding registry is
    well-formed, exhaustive, ratcheted, and extensible end-to-end.

    Status: [P_structural_instrument]. Tier 4. Certifies machinery and
    measures coverage; asserts no physics.
    """
    failures: List[str] = []

    # (1) contract well-formedness + registry-wide input_id uniqueness
    decls, _decl_skips = discover_ie_declarations()
    seen_ids: Dict[str, str] = {}
    for owner in sorted(decls):
        for d in decls[owner]:
            failures.extend(validate_declaration(d, owner))
            iid = d.get("input_id")
            if isinstance(iid, str):
                if iid in seen_ids:
                    failures.append("duplicate input_id %r in %s and %s"
                                    % (iid, owner, seen_ids[iid]))
                else:
                    seen_ids[iid] = owner

    # (1b) every REAL declaration compiles and receives an honest per-axis
    #      verdict through the live engine entry point (no aspirational rows)
    from apf.interface_atlas import summarize_input
    for owner in sorted(decls):
        for d in decls[owner]:
            try:
                sm = summarize_input(compile_declaration(d))
                if not getattr(sm, "solver_status", None):
                    failures.append("%s: no verdict for %s" % (owner, d.get("input_id")))
                gp = getattr(sm, "export_global_P", None)
                if not isinstance(gp, bool):
                    failures.append("%s: no export/obstruction bit for %s"
                                    % (owner, d.get("input_id")))
                elif d.get("expect_export") is not None and gp != d["expect_export"]:
                    failures.append("%s: %s promised expect_export=%r but got %r "
                                    "-- covers-credit rides an unearned verdict"
                                    % (owner, d.get("input_id"), d["expect_export"], gp))
            except Exception as exc:  # noqa: BLE001
                failures.append("%s: declaration %s failed to dispatch: %s"
                                % (owner, d.get("input_id"), exc))

    # (2) coverage-map exhaustiveness + internal consistency
    cov = coverage_map()
    rows, summary = cov["rows"], cov["summary"]
    from apf import _module_manifest as manifest
    if set(rows) != set(manifest.MODULE_TYPES):
        failures.append("coverage rows do not partition MODULE_TYPES exactly")
    n_onb = sum(1 for r in rows.values() if r["onboarded"])
    if n_onb != summary["modules_onboarded"]:
        failures.append("summary onboarded count inconsistent with rows")
    n_tgt = sum(1 for r in rows.values() if r["in_target_surface"])
    if n_tgt != summary["target_surface_total"]:
        failures.append("summary target-surface count inconsistent with rows")

    # (3) the ratchet -- on the covers-free DIRECT count, so covers-credit
    #     can never mask the loss of a real adapter or declaration module.
    #     Environmental import-skips are excluded Bucket-A style: a degraded
    #     sandbox (numpy/scipy-less) must not read as a coverage regression.
    n_direct = summary["modules_onboarded_direct"]
    if n_direct < ONBOARDED_MODULE_FLOOR:
        n_import_skips = (len(summary["declaration_skips"])
                          + len(summary["legacy_skips"]))
        if n_direct + n_import_skips < ONBOARDED_MODULE_FLOOR:
            failures.append("coverage regression: directly-onboarded %d < floor %d "
                            "(and the %d import-skips do not explain the gap)"
                            % (n_direct, ONBOARDED_MODULE_FLOOR, n_import_skips))

    # (4) the extensibility witness (end-to-end, no engine edit)
    failures.extend(_extensibility_witness())

    # (5) the vendored v0.2 input set (Phase 0a): 42 inputs, unique ids, and
    #     the live runner resolves to the in-repo module, not the Drive bundle
    try:
        from apf.interface_atlas_v02_inputs import assemble_inputs
        v02 = assemble_inputs()
        if len(v02) != 42:
            failures.append("vendored v0.2 set has %d inputs, expected 42" % len(v02))
        ids = [i.input_id for i in v02]
        if len(set(ids)) != len(ids):
            failures.append("vendored v0.2 input_ids not unique")
        clash = set(ids) & set(seen_ids)
        if clash:
            failures.append("declaration input_ids collide with v0.2 ids: %r" % sorted(clash))
        from pathlib import Path
        from apf.interface_atlas_live_runner import _import_v02_runner
        provider = _import_v02_runner(Path("."))
        if getattr(provider, "__name__", "") != "apf.interface_atlas_v02_inputs":
            failures.append("live runner resolves v0.2 inputs to %r, not the vendored module"
                            % provider)
    except Exception as exc:  # noqa: BLE001
        failures.append("vendored v0.2 set failed: %s" % exc)

    # (6) every live-atlas input receives an honest verdict (no silent drops)
    try:
        from apf.interface_atlas_live_runner import run_live_atlas
        res = run_live_atlas(atlas_name="ie_onboarding_registry_verdict_run")
        summaries = res.get("all_summaries") or []
        if res.get("total_inputs", 0) < 42:
            failures.append("live atlas ran %r inputs, expected >= 42"
                            % res.get("total_inputs"))
        if not summaries:
            failures.append("live atlas returned no summaries")
        legacy_conf, _ls = discover_legacy_adapters()
        wired_count = len(res.get("adapter_results") or [])
        if wired_count != len(legacy_conf):
            failures.append("onboarded-but-never-dispatched legacy adapters: "
                            "%d conforming but only %d wired into the atlas "
                            "(a typo'd ATLAS_INPUT_ID silently drops the swap)"
                            % (len(legacy_conf), wired_count))
        # v24.3.308 Wave 1c: every discovered declaration appears in the live
        # atlas artifact with its promised verdict (not only inside this check)
        decl_rows = res.get("declaration_results")
        if decl_rows is not None:
            n_decl = sum(len(v) for v in decls.values())
            if len(decl_rows) != n_decl:
                failures.append("live atlas carries %d declaration rows, expected %d"
                                % (len(decl_rows), n_decl))
            for row in decl_rows:
                if row.get("compile_error"):
                    failures.append("declaration failed to compile in the live atlas: %r"
                                    % row)
                elif not row.get("solver_status"):
                    failures.append("declaration compiled but never received a "
                                    "verdict in the live atlas (dropped?): %r" % row)
                elif row.get("verdict_matches_expectation") is False:
                    failures.append("live-atlas verdict contradicts expect_export: %r"
                                    % row)
        for s in summaries:
            status = s.get("solver_status") if isinstance(s, dict) else getattr(s, "solver_status", None)
            gp = s.get("export_global_P") if isinstance(s, dict) else getattr(s, "export_global_P", None)
            if not status or not isinstance(gp, bool):
                failures.append(("input without an honest verdict: %r" % (s,))[:200])
                break
    except Exception as exc:  # noqa: BLE001
        failures.append("live-atlas verdict run failed: %s" % exc)

    # (7) dashboard contract: the coverage report is JSON-serializable
    try:
        json.dumps(cov)
    except Exception as exc:  # noqa: BLE001
        failures.append("coverage report not JSON-serializable: %s" % exc)

    passed = not failures
    return {
        "name": (
            "T_ie_onboarding_registry_coverage: the bank->IE onboarding registry "
            "(IE_DECLARATIONS contract + legacy adapter fold-in + covers-credit) is "
            "well-formed, partitions MODULE_TYPES exactly, holds the coverage "
            "ratchet, vendors the v0.2 input set in-repo, delivers an honest "
            "verdict for every live-atlas input, and admits new interfaces by "
            "declaration alone -- witnessed end-to-end [P_structural_instrument]"
        ),
        "passed": passed,
        "epistemic": "P_structural_instrument",
        "dependencies": [
            "T_interface_contextuality_adapter",
            "T_interface_readout_axis_adapter",
        ],
        "failures": failures,
        "key_result": (
            "Phase 1 of the Full Bank Onboarding program: the coverage instrument. "
            "Baseline at banking: %d of %d loaded modules onboarded (%d of %d on "
            "the spine/sector/extension target surface), floor ratcheted at %d. "
            "Adding an interface or input = export IE_DECLARATIONS from any "
            "module (or pass a module object to coverage_map); the witness "
            "proves the path discovery -> compile -> summarize_input -> per-axis "
            "verdict with zero engine edits. This is an instrument: verdicts "
            "inherit the grades of the theorems they route through; routing "
            "confers nothing."
            % (summary["modules_onboarded"], summary["modules_total"],
               summary["target_surface_onboarded"], summary["target_surface_total"],
               ONBOARDED_MODULE_FLOOR)
        ),
    }


_CHECKS = {
    "T_ie_onboarding_registry_coverage": check_T_ie_onboarding_registry_coverage,
}


def register(registry):
    registry.update(_CHECKS)


if __name__ == "__main__":
    r = check_T_ie_onboarding_registry_coverage()
    print(("PASS" if r["passed"] else "FAIL"), r["name"])
    for f in r["failures"]:
        print("   -", f)
    cov = coverage_map()
    s = cov["summary"]
    print("coverage: %d/%d modules; target surface %d/%d; by axis %r"
          % (s["modules_onboarded"], s["modules_total"],
             s["target_surface_onboarded"], s["target_surface_total"],
             s["modules_by_axis"]))
