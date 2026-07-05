"""APF IE export-core dependency census -- the soundness sweep, pinned.

v24.3.390 (2026-07-04). The first corpus-level consequence of the Full Bank
Onboarding program's completed open surface (target_surface_open = 0 at
v24.3.388): with every spine/sector/extension module reachable through the
Interface Engine and every atlas verdict pinned, the question "what does the
export core REST ON?" became computable. This module computes it and pins
the answer.

THE SWEEP. For every atlas input pinned with export_global_P = True (the
export core: SOLVED_GLOBAL_P + INTERNAL_IDENTITY_GLOBAL_P +
GLOBAL_SECTION_EXPORTED + COHERENT_CODOMAIN_SELECTED +
CANONICAL_RECORD_EXPORTED), resolve the input to its home module(s) via the
IE_DECLARATIONS / legacy-adapter discovery, take the home modules' registered
bank checks (for adapters that register none: the bank modules whose checks
the adapter imports), and walk the transitive dependency closure through
bank.REGISTRY via the canonical crystal normalizer (_normalize_dep,
apf/crystal.py). Census the closure's epistemic grades.

WHAT THE CHECK CERTIFIES (tier 4, [P_structural_instrument]) -- four legs:

  1. NO-CONJECTURE LEG. No member of any export-core dependency closure
     carries a conjecture-class grade ([C] or C-prefixed token). The export
     core is machine-verifiably conjecture-free down to its roots, over
     grade-carrying members (results lacking an epistemic field are
     censused and reported, not gated -- see SCOPE AND HONESTY).

  2. THE READING-BOUNDARY PIN (set only, per the principal's ruling of
     2026-07-04: "pin the set"). The set of reading-graded
     ([P_structural_reading]) checks appearing in ANY export-core closure is
     EXACTLY the pinned EXPORT_READING_BOUNDARY. The pin carries NO
     dispositions -- whether a given member is a co-resident, declared
     context, or load-bearing for the exported claim is prose-level
     adjudication, deliberately not claimed here. The tripwire is the SET:
     a new reading-graded check entering an export closure (or one leaving)
     fails the bank loudly and forces a deliberate re-pin.

  3. THE ROOT INVENTORY. The unresolved dependency names (after canonical
     normalization and non-dependency-string filtering) are exactly the
     pinned EXPORT_ROOT_INVENTORY: the constitutive premises (A2, BW, MD,
     FD1, FD2, FD4, SP, Paper0_row6), and the empirical bit (occupancy)
     with its cost face (L_Delta).
     Note occupancy appears BY NAME: the QAC empirical bit is a declared
     root of the export core, not smuggled content.

  4. CLOSURE INTEGRITY. No closure member raised at run time; every
     dependency name either resolves to a registered check, normalizes to a
     named root, or is a filtered non-dependency string (provenance paths,
     module attributions); the heavy-module skip list is empty on the
     closures actually reached.

SCOPE AND HONESTY. Granularity is MODULE-level: an input's routed content is
taken to be its home module's full registered check set (the reachability
convention of the onboarding registry, .307). This over-collects for
multi-check modules -- a reading-graded co-resident enters the closure even
when the exported claim does not cite it. The pin therefore bounds the
export core's reading exposure from ABOVE; it does not claim any member is
load-bearing. Grade strings are normalized (brackets stripped, first
comma-token) before classing; checks whose results carry no epistemic field
are censused and reported, not gated (recorded in the artifacts).

FALSIFIERS: a conjecture-class member reachable from any export-core input;
a reading-graded check in an export closure absent from the pin; an
unresolved dependency name outside the root inventory; any closure member
raising at run time.

Dependencies: T_ie_onboarding_registry_coverage, T_ie_atlas_verdict_tripwire.
Cross-refs: check_T_crystal_v69_consistent (the graph normalizer's home).
"""

from __future__ import annotations

import importlib
from typing import Dict, Optional, Tuple

from apf.apf_utils import check, _result

# ---------------------------------------------------------------------------
# The pins (re-derive with the sweep; review every diff line before re-pin)
# ---------------------------------------------------------------------------

#: Leg 2 -- the reading-graded boundary of the export core (SET ONLY, no
#: dispositions; principal ruling 2026-07-04). Measured at v24.3.389 tree
#: state, 40 export-core inputs; union closure at the v24.3.391 root repair: 11 roots (see the inventory comments).
EXPORT_READING_BOUNDARY = frozenset({
    "T_no_IJC_no_noncommutativity",
    "UB_usage_billing_adopted",
    "check_T_register_reading_grounds_ceil_log2_count",
    "check_T_su2_string_cut_comovement",  # registry key carries the check_ prefix
    "T_ym_conformal_phase_excluded_by_record_locking",
    "T_ym_gap_positivity_from_MD",
    "T_ym_meaningful_spectrum_is_singlet_gapped",
    "T_ym_ir_endpoint_trichotomy_branch2_open",
    "T_ladder_ceiling_calibration_from_saturation",
    "T_contextuality_implies_superadditive_cost",
    # the status-dialect colour-record family (grades stored in the
    # 'status' result field; surfaced by the v24.3.392 fallback reader --
    # all reading-graded on the no-B reading, all previously invisible to
    # this pin):
    "check_T_canonical_colour_record_iff_multiplicity_free_P",
    "check_T_gauge_connection_is_gauge_variant_convention_P",
    "check_T_gauge_invariant_colour_record_general_N",
    "check_T_matter_free_colour_record_deep_superselection_no_go",
    "check_T_only_gauge_invariant_sharp_colour_record_is_nonfactorizable_singlet_P",
    "check_T_unique_gauge_invariant_colour_state_of_N_fundamentals_is_entangled_baryon_P",
})

#: Leg 3 -- the named roots the export core bottoms out in: axioms and
#: constitutive premises (A2/BW/MD/FD*/SP), structural imports
#: (Maschke_semisimplicity, K3_theorem), named lemma/partition aliases not
#: registered under these strings (L_col, L_epsilon_star, L_Delta,
#: T12_partition, Paper0_row6_operational_completeness), and the QAC
#: empirical bit (occupancy) -- a declared root, exactly as the framework
#: bills it.
EXPORT_ROOT_INVENTORY = frozenset({
    # the referent's constitutive premises (Paper 0 / Paper 1 kernel)
    "A2", "BW", "MD", "FD1", "FD2", "FD4", "SP",
    "Paper0_row6_operational_completeness",
    # the empirical bit (QAC) and its cost face (superadditivity --
    # occupancy-adjacent by the Phase 21 ruling; not a derivation target)
    "occupancy", "L_Delta",
})
# (The L_col registration debt was PAID at v24.3.393: check_L_col banked
# in apf/core.py from Paper 13 App. A.4 + Paper 18's collapse sketch,
# hostile-audited; the root converted to a graded [P] node with the
# selection clause billed to A2 as a dependency edge. Roots 11 -> 10.)
# Import-score history: 15 roots at v24.3.390 -> 11 at v24.3.391 (the
# root-repair pass: L_epsilon_star + T12_partition were dangling aliases
# of registered [P] content, fixed in crystal._DEP_ALIASES; K3_theorem was
# certified in-body by its own citing check, moved to cross_refs;
# Maschke_semisimplicity banked as the graded [P_math] witness
# L_maschke_semisimplicity_witness in formal_kernel.py).

#: Modules whose checks are never executed by the census (multi-minute
#: analytics; the closure must not reach them -- leg 4 asserts the skip
#: accounting stays empty).
HEAVY_MODULES = ("apf.crystal_metrics", "apf.crystal",
                 "apf.cmb_finite_mode_covariance")

#: A dependency string is a non-dependency (provenance path, module/function
#: attribution) if it contains any of these after normalization survives.
_NONDEP_MARKERS = ("/", " ", "apf.")


def _grade_token(epistemic) -> str:
    """Normalize an epistemic string: strip brackets, first comma-token."""
    s = str(epistemic or "").strip().strip("[]").strip()
    return s.split(",", 1)[0].strip()


#: Values of the 'status' result field that are RUN outcomes, not grades.
_STATUS_NOT_A_GRADE = frozenset({"PASS", "FAIL", "ok", "OK", "None", ""})


def _extract_grade(result: dict):
    """Read a result's grade: the 'epistemic' field, else the 'status'
    field when it carries a grade-shaped token (the gauge_invariant_record
    / real-adapter dialect stores grades in 'status'; the standard
    apf_utils._result stores the run outcome 'PASS' there). A status value
    in the run-outcome vocabulary is never read as a grade."""
    g = result.get("epistemic")
    if g is not None:
        return g
    st = str(result.get("status") or "").strip()
    if st and st not in _STATUS_NOT_A_GRADE and st[0] in "PC[":
        return st
    return None


def _is_conjecture(epistemic) -> bool:
    tok = _grade_token(epistemic)
    return tok == "C" or tok.startswith(("C_", "C ", "C+", "C-"))


def _is_reading(epistemic) -> bool:
    return "reading" in _grade_token(epistemic)


def _load_registry() -> Tuple[dict, dict]:
    """Full bank load; returns (REGISTRY, owner: check-name -> module).

    Ownership is derived by calling each module's register() into a
    THROWAWAY dict, never from global-registry set diffs -- the diff
    approach silently returns an empty ownership map in any process where
    the bank is already loaded (e.g. inside verify_all), which would make
    the census walk nothing and fail its own pins confusingly."""
    from apf import bank
    from apf._module_manifest import BANK_REGISTRY_MODULES
    owner: Dict[str, str] = {}
    for m in BANK_REGISTRY_MODULES:
        mod = importlib.import_module(m)
        if hasattr(mod, "register"):
            tmp: Dict[str, object] = {}
            mod.register(tmp)
            bank.REGISTRY.update(tmp)
            for k in tmp:
                owner[k] = m
    return bank.REGISTRY, owner


def _export_inputs() -> dict:
    from apf.ie_atlas_verdict_pin import PINNED_VERDICTS
    return {k: v for k, v in PINNED_VERDICTS.items() if v[1]}


def _scope_inputs(scope: str) -> dict:
    from apf.ie_atlas_verdict_pin import PINNED_VERDICTS
    if scope == "export":
        return {k: v for k, v in PINNED_VERDICTS.items() if v[1]}
    if scope == "full":
        return dict(PINNED_VERDICTS)
    raise ValueError(f"unknown census scope: {scope!r}")


#: Grade tokens that mark DECLARED EXTERNAL CONTENT (measured anchors,
#: imported numeric kernels/ledgers) -- the empirical-import surface.
_EXTERNAL_GRADE_MARKERS = ("external", "imported")


def _input_homes(pinned: dict) -> Dict[str, set]:
    """Attribute-scan mapping (no discovery calls: the legacy discovery
    path builds live payloads, which is minutes of work the census does
    not need). The registry load has already imported every bank module,
    so the contract attributes are readable off sys.modules; the
    architecture-only adapters are imported here by name."""
    import sys
    from apf._module_manifest import MODULE_TYPES
    homes: Dict[str, set] = {}
    for mname in MODULE_TYPES:
        mod = sys.modules.get(mname)
        if mod is None:
            try:
                mod = importlib.import_module(mname)
            except Exception:
                continue
        for d in getattr(mod, "IE_DECLARATIONS", ()) or ():
            if isinstance(d, dict) and d.get("input_id"):
                homes.setdefault(d["input_id"], set()).add(mname)
        iid = getattr(mod, "ATLAS_INPUT_ID", None)
        pname = getattr(mod, "ATLAS_PAYLOAD_NAME", None)
        for cand in (iid, ("payload:" + str(pname)) if pname else None):
            if cand and cand in pinned:
                homes.setdefault(cand, set()).add(mname)
    return homes


def _adapter_content_modules(mname: str, bank_modules) -> set:
    mod = importlib.import_module(mname)
    mods = set()
    for a in dir(mod):
        h = getattr(getattr(mod, a), "__module__", "")
        if h.startswith("apf.") and h != mname and h in bank_modules:
            mods.add(h)
    return mods


def run_census(scope: str = "export") -> dict:
    """Compute the export-core dependency census. Deterministic; memoized
    per call. Returns the full report consumed by the check."""
    from apf._module_manifest import BANK_REGISTRY_MODULES
    from apf.crystal import _normalize_dep

    registry, owner = _load_registry()
    # DAG prelude (the crystal walker's _bootstrap_dag, reused): several
    # checks read DAG keys populated by upstream checks (e.g. L_count's
    # C_total); running them cold out of order raises. LAZY: the prelude
    # costs tens of seconds, so it fires only before the first actual
    # check execution of this process (cache-hit passes never pay it).
    _prelude_done = [False]

    def _ensure_prelude():
        if not _prelude_done[0]:
            from apf.crystal import _bootstrap_dag
            _bootstrap_dag()
            _prelude_done[0] = True
    bank_modules = set(BANK_REGISTRY_MODULES)
    exports = _scope_inputs(scope)
    homes = _input_homes(exports)

    mod_checks: Dict[str, list] = {}
    for k, m in owner.items():
        mod_checks.setdefault(m, []).append(k)

    def resolve(name: str) -> Tuple[Optional[str], Optional[object]]:
        n = _normalize_dep(name)
        if n is None:
            return None, None
        for cand in (n, "check_" + n,
                     n[len("check_"):] if n.startswith("check_") else None):
            if cand and cand in registry:
                return cand, registry[cand]
        return n, None

    memo: Dict[str, Optional[dict]] = {}
    # Test affordance (default off): APF_CENSUS_CACHE=<path> persists the
    # per-check memo as JSON across processes, so environments with hard
    # wall-clock caps (the ~45 s sandbox) can verify the census in
    # resumable passes. Cold host-side runtime is ~60 s. HONESTY (audit
    # F2): a cache substitutes stale results AND stale dependency lists,
    # so a stale cache can mask drift on the cached members -- currency is
    # the operator's responsibility. The fingerprint below discards any
    # cache written against a different registry size; cached error /
    # heavy_skipped entries are re-accumulated into the leg-4 accounting
    # on memo hit, so a partially-erroring prior pass cannot convert a
    # leg-4 failure into a resumed PASS.
    import json as _json
    import os as _os
    _cache_path = _os.environ.get("APF_CENSUS_CACHE")
    if _cache_path and _os.path.exists(_cache_path):
        try:
            _loaded = _json.load(open(_cache_path))
            from apf._module_manifest import EXPECTED_REGISTRY_SIZE as _ERS
            if _loaded.get("__meta__", {}).get("expected") == _ERS:
                _loaded.pop("__meta__", None)
                memo.update(_loaded)
            # else: fingerprint mismatch -- discard, recompute cold
        except Exception:
            pass
    def _atomic_save():
        if not _cache_path:
            return
        try:
            from apf._module_manifest import EXPECTED_REGISTRY_SIZE as _E
            tmp_path = _cache_path + ".tmp"
            with open(tmp_path, "w") as fh:
                _json.dump({**memo, "__meta__": {"expected": _E}}, fh)
            _os.replace(tmp_path, _cache_path)  # atomic: a kill mid-dump
        except Exception:                        # never corrupts the cache
            pass

    heavy_hits: list = []
    run_errors: list = []

    def run_one(name: str) -> Optional[dict]:
        if name in memo:
            hit = memo[name]
            if isinstance(hit, dict):
                if hit.get("kind") == "error" and (hit.get("name"), "cached") not in run_errors:
                    run_errors.append((hit.get("name"), "cached"))
                elif hit.get("kind") == "heavy_skipped" and hit.get("name") not in heavy_hits:
                    heavy_hits.append(hit.get("name"))
            return hit
        rname, fn = resolve(name)
        if rname is None:
            memo[name] = {"kind": "nondep"}
            return memo[name]
        if fn is None:
            # unresolved after normalization: root or non-dep string
            if any(m in rname for m in _NONDEP_MARKERS):
                memo[name] = {"kind": "nondep"}
            else:
                memo[name] = {"kind": "root", "name": rname}
            return memo[name]
        if rname != name and rname in memo:
            memo[name] = memo[rname]
            return memo[name]
        if owner.get(rname, "") in HEAVY_MODULES:
            heavy_hits.append(rname)
            memo[name] = {"kind": "heavy_skipped", "name": rname}
            return memo[name]
        import os as _os, sys as _sys, time as _time
        if _os.environ.get("APF_CENSUS_TRACE"):
            _t = _time.time()
        _ensure_prelude()
        try:
            r = fn()
            if _os.environ.get("APF_CENSUS_TRACE"):
                _d = _time.time() - _t
                if _d > 0.5:
                    print(f"[census] {rname} {_d:.1f}s", file=_sys.stderr)
            memo[name] = {"kind": "check", "name": rname,
                          "epistemic": _extract_grade(r),
                          "deps": list(r.get("dependencies") or [])}
        except Exception as exc:  # leg-4 surface
            run_errors.append((rname, str(exc)[:100]))
            memo[name] = {"kind": "error", "name": rname}
        if rname != name:
            memo[rname] = memo[name]
        if _cache_path:
            _atomic_save()
        return memo[name]

    per_input = {}
    union_reading: set = set()
    union_roots: set = set()
    union_external: set = set()
    conjectures: list = []
    no_epi_names: set = set()

    for iid in sorted(exports):
        content: set = set()
        for h in sorted(homes.get(iid, set())):
            if h in mod_checks:
                content |= set(mod_checks[h])
            else:
                for cm in _adapter_content_modules(h, bank_modules):
                    content |= set(mod_checks.get(cm, []))
        seen: set = set()
        stack = sorted(content)
        reading_here: set = set()
        while stack:
            n = stack.pop()
            if n in seen:
                continue
            seen.add(n)
            r = run_one(n)
            if r is None or r["kind"] == "nondep":
                continue
            if r["kind"] == "root":
                union_roots.add(r["name"])
                continue
            if r["kind"] in ("heavy_skipped", "error"):
                continue
            g = r.get("epistemic")
            if g is None:
                no_epi_names.add(r["name"])
            if _is_conjecture(g):
                conjectures.append((iid, r["name"], str(g)))
            if _is_reading(g):
                reading_here.add(r["name"])
            tok = _grade_token(g).lower()
            if any(m in tok for m in _EXTERNAL_GRADE_MARKERS):
                union_external.add(r["name"])
            for d in r["deps"]:
                if d not in seen:
                    stack.append(d)
        union_reading |= reading_here
        per_input[iid] = {"n_closure": len(seen),
                          "reading": sorted(reading_here),
                          "homes": sorted(homes.get(iid, set()))}

    _atomic_save()
    return {
        "scope": scope,
        "union_external": union_external,
        "n_export_inputs": len(exports),
        "per_input": per_input,
        "union_reading": union_reading,
        "union_roots": union_roots,
        "conjectures": conjectures,
        "heavy_hits": heavy_hits,
        "run_errors": run_errors,
        "unmapped": [i for i in exports if not homes.get(i)],
        "no_epistemic_results": len(no_epi_names),
    }


def check_T_ie_export_core_dependency_census():
    """The export-core soundness census: four legs over the live sweep."""
    rep = run_census()

    # Leg 0 (precondition): every export input maps to a home module.
    check(not rep["unmapped"],
          "every export-core input resolves to a home module "
          f"(unmapped: {rep['unmapped'][:4]})")

    # Leg 1: no conjecture-class member in any export closure.
    check(not rep["conjectures"],
          "NO-CONJECTURE leg: no export-core dependency closure contains a "
          f"[C]-class member (found: {rep['conjectures'][:4]})")

    # Leg 2: the reading boundary is exactly the pin (set only).
    extra = rep["union_reading"] - EXPORT_READING_BOUNDARY
    gone = EXPORT_READING_BOUNDARY - rep["union_reading"]
    check(not extra and not gone,
          "READING-BOUNDARY pin: the reading-graded set in export closures "
          f"is exactly the pin (entered: {sorted(extra)[:4]}; "
          f"left: {sorted(gone)[:4]})")

    # Leg 3: roots are exactly the named inventory.
    r_extra = rep["union_roots"] - EXPORT_ROOT_INVENTORY
    r_gone = EXPORT_ROOT_INVENTORY - rep["union_roots"]
    check(not r_extra and not r_gone,
          "ROOT inventory: unresolved names are exactly the pinned "
          f"axiom/premise/import roots (entered: {sorted(r_extra)[:4]}; "
          f"left: {sorted(r_gone)[:4]})")

    # Leg 4: closure integrity.
    check(not rep["run_errors"],
          f"closure integrity: no member raised (errors: {rep['run_errors'][:3]})")
    check(not rep["heavy_hits"],
          "closure integrity: no export closure reaches a heavy-skipped "
          f"module (hits: {rep['heavy_hits'][:3]})")

    return _result(
        name="T_ie_export_core_dependency_census",
        tier=4,
        epistemic="P_structural_instrument",
        summary=(
            "The export-core soundness census over the completed IE surface: "
            f"{rep['n_export_inputs']} export-class inputs, module-level "
            "transitive dependency closures via the canonical crystal "
            "normalizer. Conjecture-free down to the named roots; the "
            "reading-graded boundary pinned as a SET (no dispositions, per "
            "the 2026-07-04 ruling); roots pinned incl. occupancy by name."
        ),
        key_result=(
            "Export core conjecture-free over grade-carrying members: 0 "
            "[C]-class members in any of "
            f"{rep['n_export_inputs']} export-input closures; reading "
            f"boundary = {len(EXPORT_READING_BOUNDARY)} pinned checks "
            f"(set-only tripwire); {len(EXPORT_ROOT_INVENTORY)} named roots "
            "incl. occupancy; zero run errors. Module-level granularity: "
            "the pin bounds reading exposure from above "
            f"({rep['no_epistemic_results']} distinct closure members carry no "
            "epistemic field -- censused, not gated)."
        ),
        dependencies=["T_ie_onboarding_registry_coverage",
                      "T_ie_atlas_verdict_tripwire"],
        cross_refs=["T_crystal_v69_consistent"],
        artifacts={"per_input_closure_sizes":
                   {k: v["n_closure"] for k, v in rep["per_input"].items()},
                   "reading_boundary": sorted(rep["union_reading"]),
                   "roots": sorted(rep["union_roots"])},
    )


_CHECKS = {
    "T_ie_export_core_dependency_census":
        check_T_ie_export_core_dependency_census,
}


def register(registry):
    """Register the export-core census into the bank."""
    registry.update(_CHECKS)


def run_all():
    return {name: fn() for name, fn in _CHECKS.items()}


if __name__ == "__main__":
    for _n, _r in run_all().items():
        print(("PASS" if _r.get("passed", True) else "FAIL"), _n)
        print("  ", _r["key_result"])
