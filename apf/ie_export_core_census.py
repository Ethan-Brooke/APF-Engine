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
     FD1, FD2, FD4, SP, Paper0_row6), and occupancy (constitutive since
     v24.3.304; the per-interface profile is the QAC) with its cost face
     (L_Delta).
     Note occupancy appears BY NAME: a declared root of the export core,
     not smuggled content.

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
#: dispositions; principal ruling 2026-07-04). Measured at v24.3.400 tree
#: state, re-measured at v24.3.403; 45 export-core inputs (40 -> 43 at the .398 export wave; 43 -> 44
#: at the .400 Tsirelson re-declaration; 44 -> 45 at the .403 d4_unique
#: promotion -- apf.spacetime's closure adds NO new roots, conjectures, or
#: reading members: 10 roots all premise-genre already in the inventory,
#: UB_usage_billing_adopted already in the boundary set); reading boundary 16 -> 19 at .400
#: (the three core IJC-sector reading members the .398 decline kept out
#: enter with apf.core's module closure -- exactly the three the .398
#: narrative predicted); union-closure roots 14 -> 22 at .400 (see the
#: inventory comments; all eight entrants premise-genre); roots 22 -> 21
#: at v24.3.401 (audit M1, 2026-07-05: D-quotient left -- it is DERIVED,
#: aliased to the registered check_D_quotient_forced [P] in
#: crystal._DEP_ALIASES, the .396 A4 precedent).
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
    # the apf.core IJC-sector reading members (entered at v24.3.400 with
    # the Tsirelson re-declaration -- module-level granularity pulls
    # core's full closure; these are the three the .398 decline comment
    # said "never enter", entering now DELIBERATELY with the declared
    # input; SET-only, no dispositions, per the standing ruling):
    # .401 audit m5 (dialect note, 2026-07-05): these three entrants carry
    # epistemic='P_structural_reading' but their key_result strings say
    # "[P_structural]" -- a pre-existing dialect mismatch; candidate lint
    # extension per the .392 pattern (the status-field lint does not
    # cover key_result).
    "L_MD_extension",
    "L_threat_substrate_realization",
    "T_IJC_dichotomy",
})

#: Leg 3 -- the named roots the export core bottoms out in: axioms and
#: constitutive premises (A2/BW/MD/FD*/SP), structural imports
#: (Maschke_semisimplicity, K3_theorem), named lemma/partition aliases not
#: registered under these strings (L_col, L_epsilon_star, L_Delta,
#: T12_partition, Paper0_row6_operational_completeness), and the
#: occupancy root (constitutive since v24.3.304; the per-interface
#: profile is the QAC) -- declared exactly as the framework bills it.
EXPORT_ROOT_INVENTORY = frozenset({
    # the referent's constitutive premises (Paper 0 / Paper 1 kernel)
    "A2", "BW", "MD", "FD1", "FD2", "FD4", "SP",
    "Paper0_row6_operational_completeness",
    # the empirical bit (QAC) and its cost face (superadditivity --
    # occupancy-adjacent by the Phase 21 ruling; not a derivation target)
    "occupancy", "L_Delta",
    # the v24.3.398 quantum-spine export wave (three exporting inputs
    # landed: the collapse triad, rent exclusion, the finite Born trace
    # rule; TWO intended exports DECLINED by this census's own legs --
    # the second law on apf.supplements at the NO-CONJECTURE leg
    # ([C]-class hierarchy lemmas in the module closure), and the
    # Tsirelson bound on apf.core at this ROOT leg (the module closure
    # carries the named-unregistered tokens T_adj / T_sep / T2b, which
    # would have re-introduced non-premise debt and broken the .393
    # certified sentence; those three tokens were REGISTERED at
    # v24.3.399, the debt-registration wave -- whether to re-declare
    # the Tsirelson export on apf.core is a future leg's decision,
    # deliberately not made there)). The landed inputs bottom out in four
    # additional constitutive-premise tokens only, each already
    # genre-typed "premise" in FULL_SURFACE_TYPED_ROOTS at the .396
    # full-surface adjudication (the Paper 0 loads-table rows 7a/7b/9/10
    # cited by the rent-exclusion and triad closures). The certified
    # sentence keeps its shape: constitutive premises + occupancy +
    # L_Delta, NO non-premise debts.
    "Paper0_row7a_threat_totality",
    "Paper0_row7b_defense_billing_locus",
    "Paper0_row9_cost_kind_dichotomy",
    "Paper0_row10_observer_reading",
    # the v24.3.400 Tsirelson re-declaration (the decision the .398 wave
    # deliberately left open, taken 2026-07-05): quantum:tsirelson_bound
    # declared on apf.core, expect_export=True, landed
    # INTERNAL_IDENTITY_GLOBAL_P. The .398 decline reason is DISCHARGED:
    # T_adj / T_sep / T2b were registered at v24.3.399, so core's module
    # closure now bottoms out in premise-genre tokens only. Measured on
    # the .400 cold walk: exactly eight roots entered, ALL already
    # genre-typed "premise" in FULL_SURFACE_TYPED_ROOTS at the .396
    # adjudication (the Paper 1 kernel operational-requirement rows and
    # foundation premises core's spine cites); NOTHING left; ZERO
    # conjecture-class members entered any closure. The certified
    # sentence keeps its shape: constitutive premises + occupancy +
    # L_Delta, NO non-premise debts. Roots 14 -> 22.
    # (D-quotient REMOVED at v24.3.401, audit M1 (2026-07-05) -- roots
    #  22 -> 21: it is DERIVED, not premised; core.py's registered
    #  check_D_quotient_forced [P] pins "D-quotient derived from A1 + K1",
    #  so the dep string is aliased to the registered key in
    #  crystal._DEP_ALIASES per the .396 A4 precedent. The certified
    #  sentence gets STRONGER: one fewer premise, same shape.)
    "D_positivity",
    "FD3",
    "K1",
    "O4",
    "OR0",
    "OR2",
    "SC",
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

#: Pinned legacy assert-only checks that return no result record (set-exact
#: exemption for run_one's None-tolerance; .396 audit m2). A future check
#: that returns None WITHOUT a row here errors into leg 1.
NONE_RETURNING_LEGACY = frozenset({"T_cosmogenic_to_recruitment_reduction"})


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
        import os as _os0
        if _os0.environ.get("APF_CENSUS_NO_PRELUDE"):
            return  # seeding affordance: skip the spine prelude (DAG-
                    # dependent checks will error and must be re-run in a
                    # prelude-enabled pass; never ship a cache with them)
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
    # the operator's responsibility. The same channel is an INJECTION
    # surface, not merely a staleness one (.396 second-audit F7, proven
    # in-session: a draft cache carried a manufactured graded record with
    # hand-written edges for a check that returns None): the fingerprint
    # gates only registry size, so a seeded cache can substitute grades
    # and edges the checks never returned. Cache-assisted runs are a
    # sandbox affordance, never the certification; the certifying pass
    # is cache-free. The fingerprint below discards any
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
    comp_registered: list = []  # (owner, resolved-key) pairs; leg-9 lint

    def run_one(name: str) -> Optional[dict]:
        if name in memo:
            hit = memo[name]
            if isinstance(hit, dict):
                if hit.get("kind") == "error":
                    tag = "cached: " + hit.get("msg", "")
                    if (hit.get("name"), tag) not in run_errors:
                        run_errors.append((hit.get("name"), tag))
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
            if r is None and rname in NONE_RETURNING_LEGACY:
                # Pinned legacy assert-only check (no _result record). It
                # RAN AND PASSED (an assertion failure would have raised
                # into the except arm); it contributes no grade (counted in
                # no_epistemic_results) and no dependency edges -- the
                # honest alternative, hand-writing a dependency list here,
                # would manufacture graph edges the bank never declared.
                # .396 audit m2: the exemption is BY NAME (set-exact); any
                # OTHER check returning a non-dict falls through to the
                # error arm and fails leg 1 until dispositioned here.
                r = {}
            elif not isinstance(r, dict):
                raise TypeError(
                    f"{rname} returned {type(r).__name__}, not a result "
                    "record, and is not in NONE_RETURNING_LEGACY")
            memo[name] = {"kind": "check", "name": rname,
                          "epistemic": _extract_grade(r),
                          "deps": list(r.get("dependencies") or [])}
            _comps = list(r.get("component_checks") or [])
            if _comps:  # .396 second-audit F3: carried for the leg-9 lint
                memo[name]["components"] = _comps
        except Exception as exc:  # leg-4 surface
            run_errors.append((rname, str(exc)[:100]))
            memo[name] = {"kind": "error", "name": rname,
                          "msg": f"{type(exc).__name__}: {str(exc)[:200]}"}
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
            for c in r.get("components", ()):
                # .396 second-audit F3: the parts-not-premises channel
                # (component_checks, the .391 K3 / .396 w_os precedent) is
                # only honest while its members stay UNREGISTERED; a
                # registered key parked there would exit every census leg
                # silently. Collect violations for the leg-9 lint.
                rc, rf = resolve(c)
                if rf is not None and (r["name"], rc) not in comp_registered:
                    comp_registered.append((r["name"], rc))
        union_reading |= reading_here
        per_input[iid] = {"n_closure": len(seen),
                          "reading": sorted(reading_here),
                          "homes": sorted(homes.get(iid, set()))}

    _atomic_save()
    walked = {v["name"] for v in memo.values()
              if isinstance(v, dict) and v.get("kind") == "check"}
    return {
        "scope": scope,
        "walked_members": walked,
        "component_registered": comp_registered,
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


# =============================================================================
# The full-surface input inventory (v24.3.396)
# =============================================================================

#: Typed root inventory for the FULL surface (scope="full", all 200 pinned
#: atlas inputs since v24.3.400): 61 names, 7 genres (67 -> 62 at
#: v24.3.399, the debt-registration wave; 62 -> 61 at v24.3.401, the
#: audit-M1 D-quotient de-premising -- premise genre 23 -> 22); every
#: unresolved dependency name the full walk produces is pinned here BY
#: NAME with its
#: adjudicated genre.
#: Landings that add/remove roots re-pin by hand (the EXPECTED discipline).
FULL_SURFACE_TYPED_ROOTS = {
    # -- premise: constitutive/foundational premise rows (Paper 0 referent
    #    rows, the Paper 1 kernel, foundation inputs, the empirical bit and
    #    its cost face). The export-core 10 are all here (consistency leg).
    "A1_note": None,  # placeholder removed below; A1 itself is REGISTERED, never a root
    # (A4 is NOT here: it is DERIVED -- core.py's L_irr [P] pins
    #  "A1 + occupancy + L_loc + L_cost ==> A4"; aliased A4 -> L_irr at the
    #  .396 audit, M1. A premise pin would have machine-certified that the
    #  framework ASSUMES irreversibility, against its own headline chain.)
    "A2": "premise", "BW": "premise", "MD": "premise",
    "FD1": "premise", "FD2": "premise", "FD3": "premise", "FD4": "premise",
    "K1": "premise", "SP": "premise", "SC": "premise",
    # (D-quotient is NOT here since v24.3.401, audit M1 (2026-07-05):
    #  it is DERIVED -- check_D_quotient_forced [P], "A1 + K1 ==>
    #  D-quotient"; aliased in crystal._DEP_ALIASES like A4 -> L_irr.
    #  Premise genre 23 -> 22, typed roots 62 -> 61.)
    "D_positivity": "premise",
    "finite_physical_regime": "premise",
    "occupancy": "premise",  # the empirical bit (QAC); constitutive per the 2026-07-01 ruling
    "L_Delta": "premise",    # the cost face
    "Paper0_row6_operational_completeness": "premise",
    "Paper0_row7a_threat_totality": "premise",
    "Paper0_row7b_defense_billing_locus": "premise",
    "Paper0_row9_cost_kind_dichotomy": "premise",
    "Paper0_row10_observer_reading": "premise",
    # O4/OR0/OR2: RE-ADJUDICATED premise at .396 (the staged CONTINUATION
    # listed them as alias candidates; recorded divergence, audit m6): they
    # are operational-REQUIREMENT rows of the Paper 1 kernel -- conditions a
    # physical record interface must satisfy, stated not derived; no
    # registered target exists to alias to. OR2's three banked witnesses
    # (OR2_spin/_repetition/_steane) INSTANTIATE the requirement downstream;
    # a witness of a requirement is not the requirement's derivation.
    "O4": "premise", "OR0": "premise", "OR2": "premise",
    # -- named_unregistered: in-corpus named theorems/lemmas cited as deps
    #    with NO registered surface (the L_col genre pre-.393 -- honest debt
    #    rows; each is a candidate for its own registration leg, none is
    #    silently promoted by appearing here).
    # Re-pinned 10 -> 5 at v24.3.399 (the debt-registration wave,
    # 2026-07-05): T_adj, T_sep, T2b registered in apf/core.py (exact
    # finite witnesses of the Paper 1 spine-era statements, [P]);
    # L_MW_scheme_correction written + registered unconditionally in
    # apf/gauge.py (the dead v6.3b conditional import removed);
    # L_spectral_action_coefficients registered in apf/supplements.py
    # at its existing docstring grade [P]. Measured post-wave: exactly
    # those five names left the root set, NOTHING entered (the new
    # checks' dependencies are registered checks + already-pinned
    # premise rows only); all other pins byte-stable.
    "T10_grav": "named_unregistered",
    "L_x_half": "named_unregistered",
    "L_rec_loc": "named_unregistered",
    "L_hierarchy": "named_unregistered",
    "L_crossing_correction": "named_unregistered",
    # -- named_internal: module-internal clause/quantity names used as dep
    #    strings (kappa_int bound clauses; ledger quantities).
    "C1": "named_internal", "C2": "named_internal", "C3": "named_internal",
    "C4": "named_internal", "C5": "named_internal",
    "Q_spent": "named_internal",
    # -- math_reference: standard mathematics cited by name.
    "T_vonNeumann_entropy_identity": "math_reference",
    # -- constructor_ref: engine-native factories/projections (the
    #    unification family); constructions, not theorems.
    "acc_SM": "constructor_ref", "acc_horizon": "constructor_ref",
    "acc_quantum": "constructor_ref",
    "pi_A": "constructor_ref", "pi_A_log": "constructor_ref",
    "pi_C": "constructor_ref", "pi_F": "constructor_ref",
    "pi_G": "constructor_ref", "pi_Q": "constructor_ref",
    "pi_T": "constructor_ref",
    # -- contract_ref: architecture contracts / module names cited as deps.
    "QCD_trace_to_scheme_scaffold": "contract_ref",
    "TraceToSchemeTransport": "contract_ref",
    "W_trace_contract": "contract_ref",
    "sigma_scale_yukawa_free_geometric_floor": "contract_ref",
    # The six upstream-bank contract tokens below entered the walk when the
    # .396 audit-m3 repair made the w_os composite cite its three REGISTERED
    # closure composites as dependencies (they were unreachable before m3;
    # the 22:50 pin predated that re-measurement -- caught by leg 2 on the
    # first post-m3 cold walk, re-pinned same session). They are the
    # transport-theorem layer's upstream-bank names (module-contract
    # surfaces, the TraceToSchemeTransport genre), cited by
    # check_T_transport_theorem_upstream_banks_closed:
    "trace_sector_closure": "contract_ref",
    "trace_to_scheme_boundary": "contract_ref",
    "transport_completion_gate": "contract_ref",
    "transport_composition": "contract_ref",
    "transport_ledger": "contract_ref",
    "transport_routes": "contract_ref",
    # -- data_ref: measured anchors / imported numeric kernels cited by name
    #    (the declared-external surface's dependency-string shadow).
    "m_t_APF_TRACE": "data_ref",
    "charged_lepton_pole_masses": "data_ref",
    "charm_msbar_rundec_real_adapter": "data_ref",
    "bottom_msbar_export_candidate": "data_ref",
    "chetyrkin_two_massive_one_massless_scalar": "data_ref",
    "confinement_scale_single_anchor": "data_ref",
    "substrate_constants_hbar_c_G": "data_ref",  # re-genred premise -> data_ref at the .396 audit (M3): hbar and c are defensible unit conventions but G's magnitude is empirical, and the corpus bills the Planck magnitude as the single dimensional calibration -- three measured numbers do not ride inside "the named premises"
}
del FULL_SURFACE_TYPED_ROOTS["A1_note"]

#: The 13 declared external-ledger members (grade-token census, .392 dialect
#: extraction): the empirical-import surface, named.
FULL_SURFACE_EXTERNAL_LEDGERS = frozenset({
    "T_delta_alpha_had_principled_external_universal_QCD",
    "check_T_bottom_msbar_rundec_adapter_external_ledger_declared_P",
    "check_T_charged_lepton_pole_adapter_external_ledger_declared_P",
    "check_T_charged_lepton_qed_adapter_external_ledger_declared_P",
    "check_T_charged_lepton_qed_multiloop_coefficient_ledger_P",
    "check_T_charm_msbar_rundec_adapter_external_ledger_declared_P",
    "check_T_dark_apf2_adapter_external_ledger_declared_P",
    "check_T_ew_dizet_adapter_external_ledger_declared_P",
    "check_T_light_quark_adapter_external_ledger_declared_P",
    "check_T_light_quark_adapter_flag_kernel_consistent_P",
    "check_T_sin2theta_eff_bsy_adapter_external_ledger_declared_P",
    "check_T_top_msr_R_star_adapter_external_ledger_declared_P",
    "check_T_top_msr_r_evolution_adapter_external_ledger_declared_P",
})

#: The 23 [C]-class nodes any full-surface closure reaches: the honest
#: open-lane surface, named. (The export core reaches ZERO of these --
#: the banked .390 leg.)
FULL_SURFACE_CONJECTURE_NODES = frozenset({
    "C_ew_osw_source_families_values_open",
    "C_w_trace_mw_from_3_13_chain",
    "C_w_trace_mw_from_3_13_open_gates",
    "L_N_SM_hierarchy_near_miss",
    "L_Sigma_m_nu_suggestive",
    "L_delta_alpha_hadronic_external_open",
    "L_eta_does_not_fit_cleanly",
    "L_hierarchy_boson_suppression",
    "L_hierarchy_cascade",
    "L_neutrino_closure",
    "L_sin2theta_eff_kappa_l_nonrho_remainder_open",
    "L_sin2theta_eff_kappa_l_remainder_named_open",
    "L_vev_threshold_matching",
    "L_w_trace_native_kappa_l_proper_vertex_open",
    "L_yD_spectral",
    "T_Lambda_Planck_scale_ansatz",
    "T_Lambda_absolute_structural_derivation",
    "T_bridge_observer_independence_open",
    "T_delta_alpha_had_principled_external_universal_QCD",
    "T_kappa_b_universality_falsified",
    "T_thermal_exponent_interpretation",
    "check_C_evaporation_ledger_completion",
    "check_C_evaporation_open_frontier_fence",
})

#: The 13-member heavy skip set (runtime quarantine, NOT an epistemic
#: exemption): dependency closures BEYOND these members are unwalked, and
#: the check discloses exactly that.
FULL_SURFACE_HEAVY_SKIP = frozenset({
    "T_cmb_fm_finite_multipliers", "T_cmb_fm_high_ell_preservation",
    "T_cmb_fm_large_angle_reduction", "T_cmb_fm_legendre_recurrence",
    "T_cmb_fm_nonneg_reference", "T_cmb_fm_quadrupole_suppression",
    "T_crystal_cascade_v69", "T_crystal_centrality_v69",
    "T_crystal_convergence_v69", "T_crystal_min_cut_v69",
    "T_crystal_path_attribution_scc_v69", "T_crystal_path_attribution_v69",
    "T_crystal_v69_consistent",
})

#: The 15 engine-native inputs with no bank home (the v0.2 vendored claim:/
#: payload:/route probes): pinned as a named class, not silently dropped.
FULL_SURFACE_ENGINE_NATIVE = frozenset({
    "claim:capacity_overspend", "claim:cstar_substrate", "claim:dark_runtime",
    "claim:ew_global_export", "claim:ew_local_trace", "claim:gauge_fiber",
    "claim:generic", "claim:horizon_cost", "claim:provenance_smuggling",
    "dark:route_desi_full_shape_exact", "dark:route_full_growth_likelihood",
    "neutrino:route_dune_juno_hierarchy",
    "payload:capacity_overspend", "payload:dark_runtime_open",
    "payload:ew_transport_open",
})

#: Distinct closure members carrying no extractable epistemic field on the
#: full surface (legacy assert-only checks and ungraded result records) --
#: censused and pinned, not gated. Landings that change this count re-pin.
#: Re-pinned 95 -> 101 post-audit-m3 (same session): the m3-reachable
#: composite-constituent records (trace-to-scheme + w-lock closure
#: families) carry pass/status fields but no epistemic field.
FULL_SURFACE_NO_EPISTEMIC = 101


def check_T_ie_full_surface_input_inventory():
    """T_ie_full_surface_input_inventory: The Full-Surface Input Inventory [P_structural_instrument].

    v24.3.396 (2026-07-04). The full-surface companion to the banked
    export-core census (.390): the SAME walk, over ALL pinned atlas
    inputs (196 at .396; 199 at the .398 export wave; 200 since the .400
    Tsirelson re-declaration) rather than the export-class ones (40 at
    .396; 43 at .398; 44 since .400), with every category of
    input the framework consumes pinned BY NAME. What is banked is the
    measurement plus its tripwires -- the sentence this check certifies:

        A1 + the named premises + 13 declared external ledgers
        + 23 pinned conjectures, full surface, machine-verified.

    (One premise FEWER since v24.3.401, audit M1: D-quotient left the
    premise genre -- it is DERIVED, check_D_quotient_forced [P] from
    A1 + K1; the certified sentence got strictly stronger.)

    (A1 itself is a REGISTERED bank member -- it appears inside the walk,
    never as an unresolved root. The roots below are what the walk could
    NOT resolve, each one adjudicated and typed.)

    LEGS:
      0. SCOPE: all 200 pinned inputs walked; the 15 engine-native
         no-bank-home inputs are exactly the pinned named class.
      1. INTEGRITY: zero run errors (a cached error entry from a stale
         seeding cache FAILS here -- the cache-honesty design of .390/.395).
      2. TYPED ROOTS: the unresolved-name set is EXACTLY the typed
         inventory (61 names, 7 genres; 67 -> 62 at v24.3.399, the
         debt-registration wave; 62 -> 61 at v24.3.401, the audit-M1
         D-quotient de-premising). Set-only tripwire: a new root,
         a vanished root, or an unadjudicated genre fails the bank
         (fired live twice in-session: the audit-M1 A4 de-premising and
         the audit-m3 reachability growth were both leg-2 catches).
      3. EXPORT-CORE CONSISTENCY: the banked .390 EXPORT_ROOT_INVENTORY
         is a subset of the premise genre -- the full surface cannot
         demote a constitutive premise.
      4. EXTERNALS: the declared external-ledger surface is exactly the
         13 pinned members.
      5. CONJECTURE SURFACE: the [C]-reachable node set is exactly the
         23 pinned names (the honest open-lane surface; the export core
         reaches zero of them, banked at .390).
      6. HEAVY ACCOUNTING: the runtime-quarantined skip set is exactly
         the 13 pinned members, DISCLOSED as unwalked-beyond (a runtime
         quarantine, not an epistemic exemption).
      7. GRADE-COVERAGE DISCLOSURE: the no-epistemic-field count is
         pinned (95) -- censused, not gated.
      8. A1 TRIPWIRE (.396 audit m4): A1 is asserted PRESENT in the
         walked-member union -- the sentence's first term is load-tested,
         not assumed.
      9. COMPONENT-CHECK LINT (.396 second-audit F3): no component_checks
         entry of any walked record resolves to a registered key -- the
         parts-not-premises channel that absorbed the nine unregistered
         w_os constituents cannot silently demote a registered (possibly
         [C]-graded) dependency out of the census.

    DISCLOSED OVERLAP (.396 audit m5): one node
    (T_delta_alpha_had_principled_external_universal_QCD) is a member of
    BOTH the external-ledger pin and the conjecture pin -- its grade token
    is C-prefixed AND carries the external marker. The "13 + 23" of the
    certified sentence names two pinned SETS, not a disjoint sum; the
    overlap is exported as an artifact.

    NOT CLAIMED: no grade uplift for any member; no promotion of any
    named_unregistered root (each stays a debt row until its own
    registration leg, the L_col .393 pattern); no walk beyond the heavy
    skip boundary; nothing about the world -- this is a bank-closed-world
    instrument (the .318 species).

    GRADE [P_structural_instrument]: mechanical census + typed pins +
    drift tripwires; the genre adjudications are recorded human judgment
    (same disclaimer as .390/.391/.392).
    """
    rep = run_census(scope="full")

    # Leg 0: scope + the engine-native named class.
    check(rep["n_export_inputs"] == 200,
          f"full scope: 200 pinned inputs walked (got {rep['n_export_inputs']})"
          " -- re-pinned 199->200 at v24.3.400 (the Tsirelson re-declaration:"
          " the .398-declined export on apf.core re-declared after the"
          " v24.3.399 debt-registration wave registered T_adj/T_sep/T2b;"
          " landed INTERNAL_IDENTITY_GLOBAL_P; the .398 second-law decline"
          " on apf.supplements STANDS at the NO-CONJECTURE leg). Prior"
          " re-pin 196->199 at v24.3.398 (the quantum-spine export wave)")
    um = set(rep["unmapped"])
    check(um == FULL_SURFACE_ENGINE_NATIVE,
          "engine-native class: unmapped inputs are exactly the 15 pinned "
          f"no-bank-home probes (entered: {sorted(um - FULL_SURFACE_ENGINE_NATIVE)[:4]}; "
          f"left: {sorted(FULL_SURFACE_ENGINE_NATIVE - um)[:4]})")

    # Leg 1: integrity.
    check(not rep["run_errors"],
          f"closure integrity: no member raised and no stale cached error "
          f"survives (errors: {rep['run_errors'][:3]})")

    # Leg 2: typed roots, set-exact.
    pinned = set(FULL_SURFACE_TYPED_ROOTS)
    live = set(rep["union_roots"])
    check(live == pinned,
          f"TYPED-ROOT pin: unresolved names are exactly the {len(pinned)}-name typed "
          f"inventory (entered: {sorted(live - pinned)[:5]}; "
          f"left: {sorted(pinned - live)[:5]})")
    genres = set(FULL_SURFACE_TYPED_ROOTS.values())
    check(genres == {"premise", "named_unregistered", "named_internal",
                     "math_reference", "constructor_ref", "contract_ref",
                     "data_ref"},
          f"genre closure: exactly the seven adjudicated genres (got {sorted(genres)})")

    # Leg 3: export-core consistency.
    premises = {n for n, g in FULL_SURFACE_TYPED_ROOTS.items() if g == "premise"}
    check(EXPORT_ROOT_INVENTORY <= premises,
          "export-core consistency: the banked .390 root inventory is a "
          "subset of the premise genre "
          f"(missing: {sorted(EXPORT_ROOT_INVENTORY - premises)[:4]})")

    # Leg 4: the declared-external surface.
    ext = set(rep["union_external"])
    check(ext == FULL_SURFACE_EXTERNAL_LEDGERS,
          "EXTERNAL-LEDGER pin: the declared external surface is exactly the "
          f"13 pinned members (entered: {sorted(ext - FULL_SURFACE_EXTERNAL_LEDGERS)[:4]}; "
          f"left: {sorted(FULL_SURFACE_EXTERNAL_LEDGERS - ext)[:4]})")

    # Leg 5: the conjecture surface.
    conj = {c[1] for c in rep["conjectures"]}
    check(conj == FULL_SURFACE_CONJECTURE_NODES,
          "CONJECTURE-SURFACE pin: the [C]-reachable node set is exactly the "
          f"23 pinned names (entered: {sorted(conj - FULL_SURFACE_CONJECTURE_NODES)[:4]}; "
          f"left: {sorted(FULL_SURFACE_CONJECTURE_NODES - conj)[:4]})")

    # Leg 6: heavy accounting (disclosed).
    heavy = set(rep["heavy_hits"])
    check(heavy == FULL_SURFACE_HEAVY_SKIP,
          "HEAVY-SKIP pin: the runtime-quarantined members are exactly the 13 "
          f"pinned names, deps beyond them UNWALKED by disclosure "
          f"(entered: {sorted(heavy - FULL_SURFACE_HEAVY_SKIP)[:4]}; "
          f"left: {sorted(FULL_SURFACE_HEAVY_SKIP - heavy)[:4]})")

    # Leg 7: grade-coverage disclosure.
    check(rep["no_epistemic_results"] == FULL_SURFACE_NO_EPISTEMIC,
          f"grade-coverage pin: {FULL_SURFACE_NO_EPISTEMIC} members carry no "
          f"epistemic field (got {rep['no_epistemic_results']}) -- censused, "
          "not gated; landings re-pin")

    # Leg 8: the sentence's first term, load-tested (.396 audit m4).
    check("A1" in rep["walked_members"],
          "A1 tripwire: A1 is a WALKED registered member of the full "
          "surface (never a root; the certified sentence's first term)")

    # Leg 9: component-check lint (.396 second-audit F3).
    check(not rep["component_registered"],
          "component-check lint: no component_checks entry of any walked "
          "record resolves to a registered key -- the parts-not-premises "
          "channel is not a demotion channel "
          f"(violations: {rep['component_registered'][:4]})")

    n_by_genre = {}
    for g in FULL_SURFACE_TYPED_ROOTS.values():
        n_by_genre[g] = n_by_genre.get(g, 0) + 1
    return _result(
        name="T_ie_full_surface_input_inventory",
        tier=4,
        epistemic="P_structural_instrument",
        summary=(
            "The full-surface input inventory over all 200 pinned atlas "
            "inputs: every unresolved dependency name typed and pinned "
            "(61 roots / 7 genres), the declared external-ledger surface "
            "pinned (13), the [C]-reachable surface pinned (23), the heavy "
            "skip set pinned and disclosed (13), the engine-native class "
            "pinned (15). Set-exact tripwires throughout; genre "
            "adjudications are recorded human judgment."
        ),
        key_result=(
            "A1 + the named premises + 13 declared external ledgers + 23 "
            "pinned conjectures, full surface, machine-verified: 200 inputs; "
            f"{len(FULL_SURFACE_TYPED_ROOTS)} typed roots ({n_by_genre['premise']} premise / "
            f"{n_by_genre['named_unregistered']} named-unregistered debt / "
            f"{n_by_genre['named_internal']} internal / "
            f"{n_by_genre['math_reference']} math-ref / "
            f"{n_by_genre['constructor_ref']} constructor / "
            f"{n_by_genre['contract_ref']} contract / "
            f"{n_by_genre['data_ref']} data-ref); zero run errors; heavy "
            "skip disclosed. [P_structural_instrument]"
        ),
        dependencies=["T_ie_export_core_dependency_census",
                      "T_ie_onboarding_registry_coverage",
                      "T_ie_atlas_verdict_tripwire"],
        cross_refs=["T_which_v_no_registered_interior_reader",
                    "T_config_demand_register_split_bank_respected"],
        artifacts={"typed_roots": dict(sorted(FULL_SURFACE_TYPED_ROOTS.items())),
                   "genre_counts": n_by_genre,
                   "n_inputs": rep["n_export_inputs"],
                   "heavy_skip": sorted(FULL_SURFACE_HEAVY_SKIP),
                   "engine_native": sorted(FULL_SURFACE_ENGINE_NATIVE),
                   "external_conjecture_overlap": sorted(
                       FULL_SURFACE_EXTERNAL_LEDGERS
                       & FULL_SURFACE_CONJECTURE_NODES)},
    )


_CHECKS = {
    "T_ie_export_core_dependency_census":
        check_T_ie_export_core_dependency_census,
    "T_ie_full_surface_input_inventory":
        check_T_ie_full_surface_input_inventory,
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
