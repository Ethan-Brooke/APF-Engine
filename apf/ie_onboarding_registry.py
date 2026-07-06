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
ONBOARDED_MODULE_FLOOR: int = 157  # v24.3.400 note (the Tsirelson export declaration): quantum:tsirelson_bound declared on apf.core (already direct since Wave 6) -- the .398 ROOT-leg decline re-walked after the .399 debt-registration wave registered T_adj/T_sep/T2b; landed INTERNAL_IDENTITY_GLOBAL_P, exports 43 -> 44, atlas 199 -> 200; the floor stays 157. Prior v24.3.398 note (the quantum-spine export wave): three exporting inputs added on already-direct modules (the collapse triad split from the class_transition bundle, rent exclusion, the finite Born trace rule); two more intended exports DECLINED by the export-core census at module-closure strength (second law / apf.supplements at the NO-CONJECTURE leg; Tsirelson / apf.core at the ROOT leg, named-unregistered T_adj/T_sep/T2b) -- the floor stays 157. Prior raise at v24.3.388 (the open-surface clearing wave: the 11 remaining target_surface_open modules declare directly on the ROUTE axis -- 2 internal identities [delta_calculus, anchor_support_algebra], 4 closure-by-design obstructions [colour_solder_form_no_go, strong_cp_completion_no_go, wg2_dictionary_typing_no_go, amount_graded_testedness], 5 held claims at banked reading/instrument grades [anchor_center_correspondence, mcross_planck_ratio_composition, vacuum_label_code, vacuum_scheme_covariance, su2_string_cut_testbed]; direct count 146->157, target_surface_open -> 0); prior raise at v24.3.386 (IE onboarding of the gamma_C carrier program: apf.gamma_c_carrier_program declares gravity:gammaC_carrier_watch on the ROUTE axis as a HELD Cassini WATCH, direct count 145->146); prior raise at v24.3.384 (IE onboarding of the Paper 10 continuation calculus: apf.continuation_calculus declares foundation:continuation_capacity_floor_bound on the ROUTE axis, direct count 144->145); prior raise at v24.3.348 (Wave 8: the mw_from_effective_angle physics row found by the plumbing classification); prior raise at v24.3.347 (IE Wave 7 breadth sweep: 64 direct declarations incl. both remaining spines + 3 downstream w_trace consumers; covers extension +23 on the Wave-4 heads); prior raise at v24.3.346 (IE Wave 6: the 2026-07-02 arc onboarded -- thooft_anomaly_matching_chiral, vacuum_o1_fork, formal_kernel [spine], u1y_landau_pole, acc_reading_selection, abelian_coupling_capacity_count [the Wave-6(a) probe, post fix-down], fencea_hinge_trichotomy [+ MODULE_TYPES entry]; 3 depth rows on gauge_quotient_ledger/cosmology/base_fiber_allocation); prior raise at v24.3.330 (drawn_content_readings declares the generative functional + the 4|n rigidity as claim inputs; scenario payloads stay with their home modules per the .319 no-relabel discipline); prior raise at v24.3.319 (axis depth: ijc_feasbool_engine declares its own scenario library directly); prior raise at v24.3.317 (Wave 5: the ew_* distinction/absolute-scale lanes + 6 alternates, 10 modules declare directly); prior raises .316 / .313 / .311 / .310

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
            "plumbing": IE_PLUMBING.get(mod_name, (None, None))[0],
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
        "target_surface_plumbing": sum(
            1 for name, r in rows.items()
            if r["in_target_surface"] and not r["onboarded"]
            and r["plumbing"] is not None),
        "target_surface_open": sum(
            1 for name, r in rows.items()
            if r["in_target_surface"] and not r["onboarded"]
            and r["plumbing"] is None),
        "target_open_modules": sorted(
            name for name, r in rows.items()
            if r["in_target_surface"] and not r["onboarded"]
            and r["plumbing"] is None),
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
        # v24.3.320 held-route repair: every applied claim refresh targets a
        # real v0.2 input id and carries banked-check provenance
        refreshes = res.get("claim_refreshes")
        if refreshes is not None:
            v02_ids = set(ids)
            for row in refreshes:
                if row.get("input_id") not in v02_ids:
                    failures.append("claim refresh targets a non-v0.2 id: %r" % row)
                if not row.get("provenance"):
                    failures.append("claim refresh without provenance: %r" % row)
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


def check_T_ie_atlas_verdict_tripwire() -> Dict[str, Any]:
    """T_ie_atlas_verdict_tripwire: every live-atlas verdict matches the
    deliberate pin; no verdict drifts silently, no input runs unpinned.

    Status: [P_structural_instrument]. Tier 4. The EXPECTED_THEOREM_COUNT
    discipline extended from theorem COUNTS to theorem CONSEQUENCES: any
    banked change that flips an export/obstruction verdict fails the bank
    at the next run unless the pin is regenerated DELIBERATELY
    (scripts/gen_ie_atlas_verdict_pin.py) and the diff explained by the
    wave that caused it. Guards, among others, the W export lock (a flip
    of payload:ew_transport_open to SOLVED_GLOBAL_P without the v15.1
    boundary being revisited) and the dark Gates 3/4 admission.
    """
    failures: List[str] = []
    try:
        from apf.ie_atlas_verdict_pin import PINNED_VERDICTS
        from apf.interface_atlas_live_runner import run_live_atlas
        res = run_live_atlas(atlas_name="ie_atlas_verdict_tripwire_run")
        summaries = res.get("all_summaries", [])
        live = {}
        for r in summaries:
            get = r.get if isinstance(r, dict) else lambda k, d=None: getattr(r, k, d)
            live[get("input_id")] = (str(get("solver_status")), bool(get("export_global_P")))
        if len(live) != len(summaries):
            failures.append("duplicate input_ids in the atlas (silent dict "
                            "collapse): %d rows -> %d unique ids"
                            % (len(summaries), len(live)))
        for iid, pinned in PINNED_VERDICTS.items():
            got = live.get(iid)
            if got is None:
                failures.append("pinned input vanished from the atlas: %s "
                                "(pinned %r)" % (iid, pinned))
            elif got != tuple(pinned):
                failures.append("VERDICT DRIFT %s: pinned %r -> live %r "
                                "(re-pin deliberately if a wave explains this)"
                                % (iid, tuple(pinned), got))
        unpinned = sorted(set(live) - set(PINNED_VERDICTS))
        if unpinned:
            failures.append("unpinned inputs (run scripts/gen_ie_atlas_verdict_pin.py "
                            "and commit the reviewed diff): %r" % unpinned[:10])
    except Exception as exc:  # noqa: BLE001
        failures.append("tripwire run failed: %s" % exc)

    passed = not failures
    return {
        "name": ("T_ie_atlas_verdict_tripwire: all live-atlas verdicts match "
                 "the deliberate pin (consequence-level EXPECTED discipline); "
                 "no silent verdict drift, no unpinned inputs "
                 "[P_structural_instrument]"),
        "passed": passed,
        "epistemic": "P_structural_instrument",
        "dependencies": ["T_ie_onboarding_registry_coverage"],
        "failures": failures,
        "key_result": (
            "Every atlas input's (solver_status, export_global_P) is pinned "
            "in apf/ie_atlas_verdict_pin.py and verified at every bank run. "
            "Verdict changes require a deliberate re-pin whose diff is "
            "explainable by the causing wave -- exports cannot silently "
            "appear (the W export lock, the dark admission) and obstructions "
            "cannot silently clear. An instrument; certifies stability of "
            "delivered verdicts, asserts no physics."
        ),
    }


def check_T_ie_reviewer_manifest_current() -> Dict[str, Any]:
    """T_ie_reviewer_manifest_current: the committed reviewer artifacts match
    the verdict pin -- the reviewer-facing atlas export cannot rot silently.

    Status: [P_structural_instrument]. Tier 4. Compares the COMMITTED
    artifacts/ie_atlas_export.json (generated by
    scripts/gen_reviewer_manifest.py, shipped in the repo for reviewers)
    against apf/ie_atlas_verdict_pin.py -- same input set, same verdicts,
    same pin version. Regenerate both together at re-pin (signoff Step 8b).
    Cheap: file-vs-pin, no atlas run.
    """
    import json as _json
    import os as _os
    failures: List[str] = []
    try:
        from apf.ie_atlas_verdict_pin import PINNED_VERDICTS, PIN_VERSION
        import apf as _apf
        root = _os.path.dirname(_os.path.dirname(_os.path.abspath(_apf.__file__)))
        fn = _os.path.join(root, "artifacts", "ie_atlas_export.json")
        if not _os.path.exists(fn):
            failures.append("artifacts/ie_atlas_export.json missing -- run "
                            "scripts/gen_reviewer_manifest.py and commit it")
        else:
            with open(fn, encoding="utf-8") as f:
                export = _json.load(f)
            got = {r["input_id"]: (str(r["solver_status"]), bool(r["export_global_P"]))
                   for r in export.get("inputs", [])}
            if set(got) != set(PINNED_VERDICTS):
                missing = sorted(set(PINNED_VERDICTS) - set(got))[:5]
                extra = sorted(set(got) - set(PINNED_VERDICTS))[:5]
                failures.append("export input set != pin (missing %r, extra %r) "
                                "-- regenerate the reviewer manifest" % (missing, extra))
            else:
                for iid, pinned in PINNED_VERDICTS.items():
                    if got[iid] != tuple(pinned):
                        failures.append("REVIEWER ARTIFACT STALE %s: export %r "
                                        "!= pin %r" % (iid, got[iid], tuple(pinned)))
            if export.get("pin_version") != PIN_VERSION:
                failures.append("export pin_version %r != live PIN_VERSION %r"
                                % (export.get("pin_version"), PIN_VERSION))
        md = _os.path.join(root, "REVIEWER_ATLAS.md")
        if not _os.path.exists(md):
            failures.append("REVIEWER_ATLAS.md missing -- regenerate")
        else:
            mdtext = open(md, encoding="utf-8").read()
            if ("pin v%s" % PIN_VERSION) not in mdtext:
                failures.append("REVIEWER_ATLAS.md not stamped with the live "
                                "pin version v%s -- stale, regenerate" % PIN_VERSION)
    except Exception as exc:  # noqa: BLE001
        failures.append("reviewer-manifest check failed: %s" % exc)

    passed = not failures
    return {
        "name": ("T_ie_reviewer_manifest_current: the committed reviewer atlas "
                 "export matches the verdict pin exactly (same inputs, same "
                 "verdicts, same pin version) [P_structural_instrument]"),
        "passed": passed,
        "epistemic": "P_structural_instrument",
        "dependencies": ["T_ie_atlas_verdict_tripwire"],
        "failures": failures,
        "key_result": (
            "The reviewer-facing artifacts (REVIEWER_ATLAS.md + "
            "artifacts/ie_atlas_export.json) are certified current against "
            "the pinned verdicts at every bank run: a reviewer reading the "
            "committed manifest reads what the engine actually delivers. "
            "Instrument; asserts no physics."
        ),
    }




# ---------------------------------------------------------------------------
# The plumbing classification (Wave 8, v24.3.348).
#
# CRITERION. A target-surface module is PLUMBING when it carries no claimable
# standalone physics for the reviewer atlas, in exactly one of two senses:
#
#   "stage_certificate"  -- the module's banked checks certify interior
#       pipeline stages of an already-adjudicated computation lane
#       (construction certificates, PV/tensor reduction stages, transcription/
#       ingestion instrumentation, validation and sprint reports, release
#       attestations, replay gates, status ledgers). The lane's terminal
#       physics claim is routed through the IE elsewhere; the stage certifies
#       THAT A STEP WAS DONE CORRECTLY, not a statement about the world. All
#       current entries are the OS-W/w_trace lane (terminals: the four
#       Wave-4/5 heads; the physical W export adjudicated [P_boundary], v15.1).
#   "no_banked_checks"   -- the module registers nothing in the theorem bank
#       (architecture-only, or register() deliberately returns None).
#
# The label is EXCLUSIVE with onboarding: a plumbing module may not carry
# IE_DECLARATIONS and may not be covers-listed by any head. Bringing a
# plumbing module's content into the atlas requires REMOVING it from this map
# in the same pass (the check below fails the bank otherwise). New bank
# modules are neither onboarded nor plumbing until dispositioned -- they
# surface in ``target_open_modules``, which is the honest owed-work list.
#
# Machine-checked predicates (check_T_ie_plumbing_classification):
#   (i)   every key is a manifest module of a target-surface type;
#   (ii)  tag validity;
#   (iii) exclusivity with onboarding (no declarations, no covers-credit);
#   (iv)  "no_banked_checks" entries contain zero ``def check_`` defs (static);
#   (v)   "stage_certificate" entries belong to a lane family with at least
#         one declared head (currently: the w_trace/w_os lane).
# The class assignment itself (stage vs physics) is curated -- pinned here,
# reviewed by diff, one fresh-context classification pass + audit per wave.
# ---------------------------------------------------------------------------
PLUMBING_TAGS = ("stage_certificate", "no_banked_checks")
PLUMBING_LANE_PREFIXES = ("apf.w_trace_", "apf.w_os_")
PLUMBING_LANE_HEADS = (
    "apf.w_os_route_terminal_closure",
    "apf.w_trace_native_delta_r_mw_assembly",
    "apf.w_trace_native_two_loop_phase2_master_interface_router",
    "apf.mw_value_from_equilibrium_and_custodial",
)
IE_PLUMBING = {
    "apf.continuability_preservation_resolution": ("no_banked_checks", "Architecture/math scaffolding only with no check_* functions and no register(); [P_architecture] status, pre-seeded architecture-only."),
    "apf.ew_sector_closure": ("no_banked_checks", "register() deliberately returns None by design (pre-seeded adjudication); the module carries a sector-closure ledger but banks nothing."),
    "apf.perturbative_refinability": ("no_banked_checks", "Utility module implementing the refinability defect formula with no check_* functions and no register(); pre-seeded architecture-only."),
    "apf.w_trace_acfw_candidate_preflight": ("stage_certificate", "Source-acquisition preflight: certifies the ACFW candidate is registered, not admitted, forbidden tokens absent, and export stays locked ..."),
    "apf.w_trace_cms_global_fit_context": ("stage_certificate", "Comparison-context ingestion: records the CMS-era global-fit SM prediction as a comparator row and certifies it is not an observed-W inpu..."),
    "apf.w_trace_correlated_uncertainty_model": ("stage_certificate", "Uncertainty-propagation harness for the source-comparison cluster: certifies conservative-floor weighted summaries stay under pull thresh..."),
    "apf.w_trace_delta_r_pull_diagnostics": ("stage_certificate", "Pull-diagnostic instrumentation over the comparison cluster (GREEN/AMBER/RED bands); certifies the diagnostic computation and export lock..."),
    "apf.w_trace_delta_r_source_candidate_registry": ("stage_certificate", "Candidate-only literature registry for Delta_r sources: names source classes and admission preconditions, admits no numerical rows, certi..."),
    "apf.w_trace_delta_r_source_mapping": ("stage_certificate", "Import-strategy pivot module: declares the standard Delta_r decomposition payload contract and forbidden tokens; certifies mapping/schema..."),
    "apf.w_trace_denner_diagram_coefficient_table_closeout": ("stage_certificate", "Import-contract closeout: turns the reviewed-Denner-coefficient-table obstruction into machine-checkable gates and quarantines the numeri..."),
    "apf.w_trace_denner_formula_import_native_assembly": ("stage_certificate", "Source-formula import matrix + partial assembly gates: certifies which rows are evaluated vs target-only and that open gates block full c..."),
    "apf.w_trace_denner_sirlin_notation_map": ("stage_certificate", "Notation-map ingestion: certifies the Denner/Sirlin symbol map is complete and consistent with the standard decomposition; pure transcrip..."),
    "apf.w_trace_denner_ward_identity_counterterm_import": ("stage_certificate", "Reviewed-relation import layer: certifies the Ward/counterterm relation DAG is imported, orphan-free, and that target residuals remain ta..."),
    "apf.w_trace_diagram_family_numeric_evaluator_import": ("stage_certificate", "Family-frontier ledger separating APF-owned evaluated rows from acquisition targets; certifies bucket decomposition, no-fit guard, and op..."),
    "apf.w_trace_import_session_log": ("stage_certificate", "Audit-trail bank for future reviewed payload import sessions: immutable record schema, digests, admission-state locks; certifies logging ..."),
    "apf.w_trace_import_session_replay": ("stage_certificate", "Replay/reproducibility validator over the import session log: digest recomputation, mismatch fail-closed, export-lock invariants; a repla..."),
    "apf.w_trace_independent_delta_r_crosscheck": ("stage_certificate", "Independent-source cross-check bank (DGG 2015, GFitter 2012): certifies the comparison rows exclude observed-W inputs and gaps sit within..."),
    "apf.w_trace_input_convention_stress_test": ("stage_certificate", "Convention stress test of the extraction against nearby SM prediction conventions; certifies sensitivity and gap bounds with export locke..."),
    "apf.w_trace_measurement_quarantine_context": ("stage_certificate", "Quarantine layer proving observed CMS/CDF W measurements are context-only and cannot feed source extraction or export; a discipline gate,..."),
    "apf.w_trace_multisource_delta_r_comparison": ("stage_certificate", "Multi-source comparison harness: weighted/envelope summaries of prediction sources vs the W_TRACE anchor; verdict is explicitly a no-expo..."),
    "apf.w_trace_native_bosonic_gauge_self_energy": ("stage_certificate", "Transcription certificate: Denner's reviewed bosonic self-energy closed forms evaluated natively with pole/regularity validation against ..."),
    "apf.w_trace_native_bosonic_photon_vp": ("stage_certificate", "Stage-3 rung: native evaluation of Denner's reviewed transverse photon self-energy with transversality and pole -3 validation; certifies ..."),
    "apf.w_trace_native_bosonic_scalar_vp": ("stage_certificate", "First bosonic sub-rung: constructs and validates the charged-scalar (Goldstone) photon VP loop (Ward identity, quarter-fermion pole, clos..."),
    "apf.w_trace_native_charge_running": ("stage_certificate", "Validation rung: assembles the gauge-invariant charge running from Denner's two reviewed self-energies and certifies the native evaluator..."),
    "apf.w_trace_native_delta_r_uv_assembly": ("stage_certificate", "Stage-4 capstone gate: certifies the assembled Delta r UV pole cancels to machine precision and delta_VB matches the reviewed closed form..."),
    "apf.w_trace_native_ew_self_energy": ("stage_certificate", "Stage-2 rung: slot-by-slot fermion-loop self-energies reduced to native PV functions, validated by photon transversality and reproduction..."),
    "apf.w_trace_native_fermion_sum_self_energy": ("stage_certificate", "Assembly rung: full SM fermion-content sum with mu-independence gate and anchors to already-banked quantities; coherent-assembly certific..."),
    "apf.w_trace_native_fermionic_gauge_self_energy": ("stage_certificate", "Pole-structure rung: fermionic self-energy p^2-pole coefficients assembled from SM charges and validated against internal sum-rule anchor..."),
    "apf.w_trace_native_lepton_self_energy": ("no_banked_checks", "Self-declared ARCHITECTURE-ONLY with no register(): the Denner chiral lepton self-energy wrapper is shipped for a sibling attempt but exp..."),
    "apf.w_trace_native_os_renormalized_self_energy": ("stage_certificate", "Step-2 rung: builds the twice-subtracted OS-renormalized self-energy and proves it mu-independent; renormalization-machinery certificate,..."),
    "apf.w_trace_native_timelike_gauge_width": ("stage_certificate", "Unitarity cross-check rung: native absorptive parts satisfy the optical theorem against tree widths from the same couplings; validates th..."),
    "apf.w_trace_native_timelike_self_energy": ("stage_certificate", "Internal validation anchor: the timelike machinery reproduces the ALREADY-BANKED Delta alpha_lep (from apf.delta_alpha_leptonic) to rel 5..."),
    "apf.w_trace_native_two_loop_phase2_bosonic_vertex_master_anchors": ("stage_certificate", "MASTERS ONLY: CAF 2006 bosonic master integrals I4-I10 banked as named anchors with pole ledger; docstring is explicit that the diagram c..."),
    "apf.w_trace_native_two_loop_phase2_coefficient_output_slices": ("stage_certificate", "Algebraic substrate slices: TP5/SUN3/ZFF/BOSONIC coefficient rows with every row carrying physical_value = 0; certifies the numerator-exp..."),
    "apf.w_trace_native_two_loop_phase2_coefficient_surface_no_smuggling": ("stage_certificate", "Degree-5 coefficient surface + sector no-smuggling guard; certifies the expansion identity and the irreducibility discipline gate, explic..."),
    "apf.w_trace_native_two_loop_phase2_counterterm_residue_formula_ledger": ("stage_certificate", "Structural-contract certificate for the formula infrastructure: channels seeded with physical_value = 0, comparator-typed grid, no self-e..."),
    "apf.w_trace_native_two_loop_phase2_current_source_coefficient_no_go": ("stage_certificate", "Audit-first source-sufficiency finding scoped to the currently uploaded source set ('NOT a physics impossibility theorem'); certifies an ..."),
    "apf.w_trace_native_two_loop_phase2_delta_r_source_import": ("stage_certificate", "Source-import stage: 10 literature rows ingested at byte-precise ranges and the AC 2002 Eq. 11 formula transcribed with the source's own ..."),
    "apf.w_trace_native_two_loop_phase2_ew_self_energy_assembly_gate": ("stage_certificate", "TOY LEDGER ONLY: pole-cancellation gate exercised against a manufactured toy ledger; docstring states it proves the algebraic gate only, ..."),
    "apf.w_trace_native_two_loop_phase2_ew_source_table_extraction": ("stage_certificate", "Aggregate-formula/convention extraction from five literature sources with the strict rule that no row-level coefficient is promoted; inge..."),
    "apf.w_trace_native_two_loop_phase2_ew_source_table_extraction_queue": ("stage_certificate", "NO ROWS EXTRACTED: a discipline-gate extraction queue naming source families; refuses pre-promoted targets, banks no coefficient."),
    "apf.w_trace_native_two_loop_phase2_ew_tex_source_exact_extraction": ("stage_certificate", "SOURCE WINDOWS ONLY: byte-level verbatim source citations with SHA256; promotion class is fixed to 'not_coefficient_row' - pure acquisiti..."),
    "apf.w_trace_native_two_loop_phase2_fermionic_vertex_reduction_ledger": ("stage_certificate", "METHODS ONLY: ACFW 2004 reduction methods banked as row records, every row status='coefficient_table_open'; method-ingestion certificate."),
    "apf.w_trace_native_two_loop_phase2_missing_terms_source_and_derivation_plan": ("stage_certificate", "Plan/ledger module banking the source-acquisition order, gap-to-source matrix, workplan stages, and claim-language rules; workflow bookke..."),
    "apf.w_trace_native_two_loop_phase2_osw_deltar_connector_refusal": ("stage_certificate", "TOY ONLY connector + refusal gate: exercises coverage/refusal validation with deliberately non-fitted toy coefficients, claims no physica..."),
    "apf.w_trace_native_two_loop_phase2_projectors_preibp_router": ("stage_certificate", "Projector/pre-IBP/router infrastructure with an exact-rational toy cancellation testbench; certifies the gate is load-bearing, banks no p..."),
    "apf.w_trace_native_two_loop_phase2_zfitter_comparator_guard": ("stage_certificate", "FORMAL ROLE LEDGER: closed set of allowed ZFITTER/DIZET roles + forbidden component tokens; a pure anti-smuggling role guard."),
    "apf.w_trace_native_two_loop_phase2_zpole_bosonic_deltakappa_import": ("stage_certificate", "AGGREGATE SHIFT ROWS import: ACF 2006 published shift tables ingested and the source's own Hollik cross-check reproduced; import-fidelity..."),
    "apf.w_trace_native_two_loop_phase2_zpole_form_factor_connector_dag": ("stage_certificate", "CONNECTOR ONLY: the ACF 2006 NNLO Z-pole decomposition encoded as a 12-node DAG; evaluates nothing, coefficient ledger stays open."),
    "apf.w_trace_native_two_loop_sunset": ("stage_certificate", "Source-DE + threshold gate for the sunset topology; the full numeric master is explicitly NOT promoted here (next pack), and the one nume..."),
    "apf.w_trace_native_two_loop_tier1_status": ("stage_certificate", "Self-described status ledger: 'NOT a math module - purely a structural-status record of which gates have closed at which grades'."),
    "apf.w_trace_native_two_loop_two_point": ("stage_certificate", "Source-formula binding + DOUBLE_COUNT discipline gate for the bubble master - explicitly NOT the full master integral; gates, anchors, an..."),
    "apf.w_trace_native_uv_cancellation_stage4": ("stage_certificate", "Stage-4 UV gate: proves bosonic self-energy poles are linear in p^2 and cancelled by OS counterterms - exactly a 'UV poles cancel' stage ..."),
    "apf.w_trace_native_uv_pole": ("stage_certificate", "PV pole-bookkeeping layer: exact pole coefficients for A0/B0/B1/B11/B00 validated three ways against the banked finite toolkit; toolkit-c..."),
    "apf.w_trace_native_zll_vertex_form_factors": ("stage_certificate", "Generic-layer substrate for the Zll kappa_l assembly: Denner App. C vertex form factors on the native three-point toolkit, validated agai..."),
    "apf.w_trace_physics_source_stop_condition": ("stage_certificate", "No-more-scaffold gate: declares stop conditions and allowed/forbidden next actions; pure workflow discipline."),
    "apf.w_trace_prediction_cluster_robustness": ("stage_certificate", "Robustness diagnostics (floor scans, subset scans) over the comparison cluster; certifies the comparison stays GREEN with export locked -..."),
    "apf.w_trace_publication_claim_language": ("stage_certificate", "Claim-language bank: allowed vs forbidden publication sentences and a safety predicate; publication-report instrumentation verbatim."),
    "apf.w_trace_pv_c0_general_momentum": ("stage_certificate", "PV substrate stage: native general-momentum spacelike scalar C0 with self-validation (zero-momentum limit, permutation symmetry, mesh); e..."),
    "apf.w_trace_pv_cij_three_point": ("stage_certificate", "PV tensor-reduction stage: rank-1/2 three-point coefficients with trace/contraction identity self-validation; toolkit construction certif..."),
    "apf.w_trace_pv_d0_general_momentum": ("stage_certificate", "PV substrate stage: native spacelike box scalar D0 with symmetry and mesh validation; 'Spacelike scalar D0 only', remaining assembly open."),
    "apf.w_trace_pv_derivative_two_point": ("stage_certificate", "PV derivative stage: native B0'/B1' validated against finite differences and closed forms; explicitly does not assemble any self-energy o..."),
    "apf.w_trace_pv_dij_four_point": ("stage_certificate", "PV box tensor-reduction stage (rank 1-3) with contraction/trace-relation self-validation; toolkit construction certificate."),
    "apf.w_trace_pv_ewwgr_bare_proper_vertex": ("stage_certificate", "Vertex-assembly sub-rung (R1b) of the Gate A kappa_l arc: EWWGR Zff/gamma-ff form factors assembled on the BHM layer with reference-value..."),
    "apf.w_trace_pv_lambda_bhm_vertex": ("stage_certificate", "R1 rung: BHM Lambda_2/Lambda_3 Z-vertex scalar functions implemented from the LEP Yellow Report closed forms with Li2 and reference-value..."),
    "apf.w_trace_pv_timelike_three_point": ("stage_certificate", "R0 rung: timelike/above-threshold scalar C0 branch with absorptive-part validation two ways; PV-branch construction certificate."),
    "apf.w_trace_pv_timelike_three_point_tensor": ("stage_certificate", "R0b rung: timelike rank-1 tensor coefficients with stability fix and closed-form validation; PV-branch construction certificate."),
    "apf.w_trace_pv_timelike_three_point_tensor_rank2": ("stage_certificate", "R0c rung: timelike rank-2 tensor coefficients (C00/C11/C12/C22) with trace-relation and threshold validation; PV-branch construction cert..."),
    "apf.w_trace_release_attestation": ("stage_certificate", "Release attestation contract: signed-attestation and immutable-manifest-digest schema, template-only and locked; release attestation verb..."),
    "apf.w_trace_release_evidence_bundle": ("stage_certificate", "Terminal release evidence bundle: 'infrastructure completion, not a physical W export'; certifies missing evidence blocks release."),
    "apf.w_trace_release_packet_validator": ("stage_certificate", "Release-packet preflight validator: rejects templates, bad digests, forbidden tokens, export overrides; pure release gating."),
    "apf.w_trace_release_runbook": ("stage_certificate", "Operator release checklist/runbook bank; declares required artifacts and predicates, ships nothing real; process documentation certificate."),
    "apf.w_trace_residual_interpretation": ("stage_certificate", "Interpretation layer over the residual with an overclaim guard and a paper-safe sentence ending 'not a physical W-mass export'; validatio..."),
    "apf.w_trace_review_packet_validator": ("stage_certificate", "Completed source-review packet validator/preflight: default packets fail closed, export locked; review-gate instrumentation."),
    "apf.w_trace_reviewed_source_import_handoff": ("stage_certificate", "Handoff gate between validated review packet and payload loader: permission-boundary contract with fail-closed behavior; import-gate inst..."),
    "apf.w_trace_signed_release_replay": ("stage_certificate", "Signed release replay contract: ordered replay stages, digest chain, unsigned/template rejection; replay/consistency gate verbatim."),
    "apf.w_trace_source_acquisition_review_packet": ("stage_certificate", "Acquisition worksheet/review-packet bank, template-only artifacts, no real source acquired; acquisition instrumentation."),
    "apf.w_trace_source_authority_grading": ("stage_certificate", "Source authority grading ledger (A/A-/B+/Q grades, measurements quarantined); comparison-source bookkeeping, no physics value."),
    "apf.w_trace_source_candidate_registry": ("stage_certificate", "External-source acquisition checklist/candidate registry, candidate entries only, no rows admitted; acquisition instrumentation."),
    "apf.w_trace_tensor_coefficient_map_scaffold": ("stage_certificate", "Tensor/coefficient-map scaffold over the PV substrate; deliberately refuses to promote fitted coefficients, leaves the reviewed table as ..."),
    "apf.w_trace_terminal_state_report": ("stage_certificate", "Terminal open/closed state report; 'infrastructure completion, not a physical W export' - status ledger verbatim."),
    "apf.w_trace_v142_physics_validation_sprint_report": ("stage_certificate", "Sprint terminal report aggregating three validation modules; certifies sub-module passes and export locks - validation/sprint report verb..."),
    "apf.w_trace_v143_physics_deep_validation_report": ("stage_certificate", "Sprint terminal report for the v14.3 deep-validation pass; aggregates sub-module state and export locks."),
    "apf.w_trace_v144_publication_validation_report": ("stage_certificate", "Publication-validation sprint terminal report; aggregates authority/robustness/residual/claim-language sub-modules, export locked."),
    "apf.w_trace_v14_physics_sprint_terminal_report": ("stage_certificate", "v14.0 sprint terminal report listing the five sprint modules and the no-more-scaffold status; sprint report verbatim."),
}


def check_T_ie_plumbing_classification():
    """The plumbing map is well-formed, exclusive with onboarding, and its
    machine-checkable predicates hold. [P_structural_instrument] tier 4.

    Certifies predicates (i)-(v) of the criterion above. The curated class
    assignment is pinned data (review-the-diff discipline); this check makes
    the label impossible to abuse silently: a plumbing module that gains
    IE_DECLARATIONS or covers-credit fails the bank until the label is
    removed in the same pass.
    """
    import io as _io
    failures = []
    from apf import _module_manifest as manifest
    for mod, (tag, _reason) in IE_PLUMBING.items():
        if mod not in manifest.MODULE_TYPES:
            failures.append("%s: not a manifest module" % mod)
            continue
        if manifest.MODULE_TYPES[mod] not in TARGET_MODULE_TYPES:
            failures.append("%s: plumbing label on a non-target type %s"
                            % (mod, manifest.MODULE_TYPES[mod]))
        if tag not in PLUMBING_TAGS:
            failures.append("%s: unknown tag %r" % (mod, tag))
        if tag == "no_banked_checks":
            src = _io.open(mod.replace("apf.", "apf/") + ".py",
                           encoding="utf-8").read()
            if "def check_" in src:
                failures.append("%s: tagged no_banked_checks but defines "
                                "check_* functions" % mod)
        if tag == "stage_certificate":
            if not mod.startswith(PLUMBING_LANE_PREFIXES):
                failures.append("%s: stage_certificate outside the declared "
                                "lane families" % mod)
    # lane heads must actually be declared (the lane terminal is routed)
    import importlib as _il
    n_head_decls = 0
    for h in PLUMBING_LANE_HEADS:
        try:
            n_head_decls += len(declarations_from_module(_il.import_module(h)))
        except Exception as exc:  # noqa: BLE001
            failures.append("lane head %s failed to import: %s" % (h, exc))
    if n_head_decls == 0:
        failures.append("no lane head carries a declaration -- "
                        "stage_certificate labels are unanchored")
    # exclusivity with onboarding
    cov = coverage_map()
    for mod in IE_PLUMBING:
        r = cov["rows"].get(mod)
        if r is None:
            continue
        if r["onboarded"]:
            failures.append("%s: plumbing label on an ONBOARDED module -- "
                            "remove the label in the same pass" % mod)
    # summary coherence
    s = cov["summary"]
    if s.get("target_surface_plumbing") != sum(
            1 for m in IE_PLUMBING
            if manifest.MODULE_TYPES.get(m) in TARGET_MODULE_TYPES):
        failures.append("summary plumbing count inconsistent with IE_PLUMBING")
    if s.get("target_surface_open") != len(s.get("target_open_modules", ())):
        failures.append("summary open count inconsistent with open list")
    return {
        "name": "check_T_ie_plumbing_classification",
        "passed": not failures,
        "failures": failures,
        "status": "P_structural_instrument",
        "summary": ("plumbing map: %d entries (%d stage_certificate, %d "
                    "no_banked_checks); target surface open: %d"
                    % (len(IE_PLUMBING),
                       sum(1 for v in IE_PLUMBING.values() if v[0] == "stage_certificate"),
                       sum(1 for v in IE_PLUMBING.values() if v[0] == "no_banked_checks"),
                       s.get("target_surface_open", -1))),
    }




# ---------------------------------------------------------------------------
# The repair-frontier census (v24.3.349) -- the engine's first full-bank lap.
#
# With the target surface fully dispositioned (162 onboarded / 85 plumbing /
# 0 open at .348), the atlas was swept end-to-end for the first time and the
# ENGINE-NATIVE rows (vendored v0.2 canonical inputs + v0.3 refresh layer +
# legacy real adapters -- i.e. every input NOT introduced as an
# IE_DECLARATIONS claim row) were partitioned by what the solver actually
# demands. THE FINDING, pinned below: the genuinely open, engine-repairable
# frontier of the whole bank is EVIDENCE-SHAPED, not theory-shaped -- every
# genuine-open row carries packet_status OPEN_EVIDENCE_REQUIRED with
# empirical-run fields (posterior_closed / robustness_checks_passed /
# run_completed): the dark empirical gates (DESI full-shape, growth
# likelihood, cross-SN profile, the dark runtime lock) and the DUNE/JUNO
# hierarchy watch row. The one held theory-side row (payload:ew_transport_open)
# is the v15.1 [P_boundary] adjudication, not owed work.
#
# SEMANTICS GUARD (the sweep's methodological finding): movement-graph
# frontiers on DECLARED CLAIM ROWS measure parse-visibility of the claim
# text, NOT physics distance -- e.g. abstract categorical claims parse to
# NO_CLOSING_FRONTIER with zero critical fields. Claim rows are therefore
# EXCLUDED from this census by construction (their verdict stability is the
# .323 tripwire's job). Never rank claim rows by frontier size. Honesty
# note on the census's own composition: four of the five GENUINE-OPEN
# frontiers are parse-derived from VENDORED claim text (the v0.2 canonical
# inputs, refresh-layer provenance discipline); only payload:dark_runtime_open
# earns its frontier from payload data. The finding rests on those vendored
# texts being accurate descriptions of the empirical gates, not on
# independent solver measurement.
# ---------------------------------------------------------------------------
FRONTIER_GENUINE_OPEN = {
    "payload:dark_runtime_open": ("posterior_closed", "robustness_checks_passed"),
    "dark:route_desi_full_shape_exact": ("posterior_closed", "robustness_checks_passed"),
    "dark:route_cross_sn_profile_probe": ("posterior_closed", "robustness_checks_passed"),
    "dark:route_full_growth_likelihood": ("posterior_closed", "robustness_checks_passed", "run_completed"),
    "neutrino:route_dune_juno_hierarchy": ("posterior_closed", "robustness_checks_passed", "run_completed"),
}
FRONTIER_ADJUDICATED_BOUNDARY = {
    "payload:ew_transport_open": ("uncertainty_protocol_declared",),
}
FRONTIER_CONTROL_WITNESS = (
    "claim:capacity_overspend", "claim:dark_runtime", "claim:ew_global_export",
    "claim:ew_local_trace", "claim:gauge_fiber", "claim:generic",
    "claim:horizon_cost", "payload:capacity_overspend",
)
FRONTIER_CLOSED_STATUSES = (
    "OBSTRUCTION_NAMED_CLOSURE", "FAIL_CLOSED_PROVENANCE",
    "BLOCKED_SUBSTRATE_REVISION_REQUIRED",
)


def check_T_ie_repair_frontier_census():
    """The engine-native open frontier is pinned: five evidence-shaped rows,
    one adjudicated boundary, nothing else. [P_structural_instrument] tier 4.

    Recomputes the live atlas, restricts to engine-native rows (every input
    not introduced by an IE_DECLARATIONS claim row), and certifies the
    partition: EXPORTED / CLOSED-BY-DESIGN / ADJUDICATED-BOUNDARY /
    GENUINE-OPEN / CONTROL-WITNESS covers the native rows exactly. For each
    GENUINE-OPEN row the critical-field frontier must equal the pinned set
    and the packet must remain OPEN_EVIDENCE_REQUIRED; a row that starts
    exporting FAILS THE BANK on purpose -- an empirical gate closing is an
    adjudication event, never a silent flip. The boundary row must stay held
    per the v15.1 ruling. New engine-native rows fail the .323 tripwire
    (unpinned input) and, if neither exporting nor closed-status, this
    census too -- an already-exporting or closed-status arrival is absorbed
    into its class here and caught by the tripwire alone (defense in depth;
    the .348 plumbing pattern, at frontier level).

    Cost note: one full atlas run (the .323
    memoization decision stands -- coupling cost beats runtime at current
    scale).
    """
    failures = []
    from apf.interface_atlas_live_runner import run_live_atlas
    import apf.interface_atlas as _ia
    _cap = {}
    _orig = _ia.build_interface_atlas
    def _hook(inputs, **kw):
        a = _orig(inputs, **kw); _cap["atlas"] = a; return a
    _ia.build_interface_atlas = _hook
    try:
        run_live_atlas(atlas_name="ie_repair_frontier_census_run")
    finally:
        _ia.build_interface_atlas = _orig
    atlas = _cap.get("atlas")
    if atlas is None:
        return {"name": "check_T_ie_repair_frontier_census", "passed": False,
                "failures": ["atlas capture failed"], "status": "P_structural_instrument"}
    decls, _skips = discover_ie_declarations()
    declared_ids = {d.get("input_id") for entries in decls.values() for d in entries}
    native = {s.input_id: s for s in atlas.route_summaries
              if s.input_id not in declared_ids}
    classified = set()
    for iid, fields in FRONTIER_GENUINE_OPEN.items():
        s = native.get(iid)
        if s is None:
            failures.append("GENUINE-OPEN row vanished: %s" % iid); continue
        classified.add(iid)
        if s.export_global_P:
            failures.append("%s EXPORTS -- an empirical gate closed; "
                            "adjudicate the promotion, re-pin deliberately" % iid)
        if tuple(sorted(s.critical_fields)) != tuple(sorted(fields)):
            failures.append("%s frontier drift: %r != pinned %r"
                            % (iid, sorted(s.critical_fields), sorted(fields)))
        if str(s.packet_status) != "OPEN_EVIDENCE_REQUIRED":
            failures.append("%s packet %r != OPEN_EVIDENCE_REQUIRED"
                            % (iid, s.packet_status))
    for iid, fields in FRONTIER_ADJUDICATED_BOUNDARY.items():
        s = native.get(iid)
        if s is None:
            failures.append("boundary row vanished: %s" % iid); continue
        classified.add(iid)
        if s.export_global_P or str(s.solver_status) != "SOLVED_LOCAL_HELD_FOR_REPAIR":
            failures.append("%s left its v15.1 [P_boundary] state: %s/%r"
                            % (iid, s.solver_status, s.export_global_P))
        if tuple(sorted(s.critical_fields)) != tuple(sorted(fields)):
            failures.append("%s boundary frontier drift: %r"
                            % (iid, sorted(s.critical_fields)))
    for iid in FRONTIER_CONTROL_WITNESS:
        if iid in native:
            classified.add(iid)
        else:
            failures.append("control row vanished: %s" % iid)
    for iid, s in native.items():
        if iid in classified:
            continue
        if s.export_global_P:
            continue  # EXPORTED class
        if str(s.solver_status) in FRONTIER_CLOSED_STATUSES:
            continue  # CLOSED-BY-DESIGN class
        failures.append("undispositioned engine-native row: %s (%s) -- "
                        "classify it (genuine-open / boundary / control) "
                        "before it rides" % (iid, s.solver_status))
    n_exported = sum(1 for s in native.values() if s.export_global_P)
    return {
        "name": "check_T_ie_repair_frontier_census",
        "passed": not failures,
        "failures": failures,
        "status": "P_structural_instrument",
        "summary": ("engine-native rows: %d (exported %d, genuine-open %d, "
                    "boundary %d, controls %d); the open frontier is "
                    "evidence-shaped" % (len(native), n_exported,
                    len(FRONTIER_GENUINE_OPEN), len(FRONTIER_ADJUDICATED_BOUNDARY),
                    len(FRONTIER_CONTROL_WITNESS))),
    }


_CHECKS = {
    "T_ie_onboarding_registry_coverage": check_T_ie_onboarding_registry_coverage,
    "T_ie_atlas_verdict_tripwire": check_T_ie_atlas_verdict_tripwire,
    "T_ie_reviewer_manifest_current": check_T_ie_reviewer_manifest_current,
    "T_ie_plumbing_classification": check_T_ie_plumbing_classification,
    "T_ie_repair_frontier_census": check_T_ie_repair_frontier_census,
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
