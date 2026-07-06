#!/usr/bin/env python3
"""APF Full Verification Script.

Runs all check_ functions across all registered modules and prints a
complete scorecard with prediction accuracy summary.

Usage:
    python scripts/verify_all.py
    python scripts/verify_all.py --module core
    python scripts/verify_all.py --verbose
    python scripts/verify_all.py --no-scorecard
"""

import sys
import time
import argparse
import importlib
import traceback
from collections import defaultdict

# ── Module registry ──────────────────────────────────────────────────────────
# Mirrors the load order in apf/bank.py, plus standalone files.

# MODULES is built from apf._module_manifest as of v24.3.19 (2026-05-18 MODULES
# unification refactor). Previously, this file maintained an inline 223-entry
# list that drifted from bank._MODULE_PATHS (154 entries). The manifest is now
# the single source of truth.
#
# The original inline list is archived at
# Codebase/Old/APF_Codebase_v24.3.18_pre-modules-unification_2026-05-18.zip.
from apf._module_manifest import ALL_MODULES_VERIFY_ORDER as _MANIFEST_MODULES

# verify_all.MODULES is a list of (module_path, file_label) tuples for backward
# compatibility with the existing scorecard formatter. Build it from the manifest.
def _build_modules_tuples():
    tuples = []
    for path in _MANIFEST_MODULES:
        # Standalone lemmas use the apf.standalone.* path; map to a file label
        # that includes the standalone/ prefix.
        if path.startswith("apf.standalone."):
            label = "standalone/" + path[len("apf.standalone."):] + ".py"
        else:
            label = path[len("apf."):] + ".py"
        tuples.append((path, label))
    return tuples

MODULES = _build_modules_tuples()


# Architecture-only modules: have register() but contribute 0 bank checks BY DESIGN.
# Filtered out of bank-audit reports so the "loaded but 0 checks" bucket is informational
# only. Added 2026-05-18 alongside the --bank-audit CLI lane.
ARCHITECTURE_ONLY_WHITELIST = frozenset({
    "apf.coherent_materials_partner_pilot_lifecycle",  # v24.3.66 - CMAL collapse (kit+feedback+review_board+readiness+governance)
    "apf.coherent_materials_rc_certification",  # v24.3.66 - CMAL collapse (acceptance_test_harness+release_candidate_certifier)
    "apf.coherent_materials_red_team",  # v24.3.66 - CMAL collapse (adversarial+claim_fence+provenance_conflict_auditor)
    "apf.interaction_pattern_schema",  # v24.3.66 - architecture-only Pattern schema (6-field tau-tuple; Integrator Response Q4)
    "apf.ew_sector_closure",
    # 12 v24.3.18 defect-calculus architecture modules (no check_* fns by design):
    "apf.continuability_preservation_resolution",
    "apf.defect_transition_dynamics",
    "apf.defect_composition_calculus",
    "apf.defect_variational_principle",
    "apf.defect_scale_flow",
    "apf.defect_obstruction_cohomology",
    "apf.defect_global_descent_kernel",
    "apf.defect_functorial_transport",
    "apf.defect_falsifier_gate_logic",
    "apf.defect_observable_signatures",
    "apf.defect_master_integration",
    "apf.defect_domain_applications",
    # 5 ISEE engineering modules (engineering-only, no bank checks):
    "apf.interface_solver_batch",
    "apf.interface_solver_ci_policy",
    "apf.interface_solver_contracts",
    "apf.interface_solver_report",
    "apf.interface_solver_route_adapters",
    # v24.3.21 perturbative refinability defect (utility module, no register()):
    "apf.perturbative_refinability",
    # 19 v24.3.46 CMAL release-candidate landing modules (architecture-only):
    "apf.coherent_materials_batch_triage_runner",
    "apf.coherent_materials_candidate_triage_kernel",
    "apf.coherent_materials_golden_receipt_benchmark",
    "apf.coherent_materials_manual_dry_run_pilot",
    "apf.coherent_materials_manual_external_dry_run",
    "apf.coherent_materials_pilot_telemetry_schema",
    "apf.coherent_materials_portfolio_planner",
    "apf.coherent_materials_receipt_contract_validator",
    "apf.coherent_materials_receipt_trace_certificates",
})


# Modules whose checks populate the DAG cache. When --module filter is used,
# these run as a silent prelude (if not in the filtered set) so that
# downstream DAG consumers see a populated DAG. Derived from the 2026-04-20
# DAG-key audit: these are exactly the modules containing dag_put calls.
PRELUDE_MODULES = {
    "apf.core",
    "apf.gauge",
    "apf.spacetime",
    "apf.gravity",
    "apf.generations",
    "apf.cosmology",
    "apf.extensions",
    "apf.supplements",
}

# ── Helpers ──────────────────────────────────────────────────────────────────

def classify(name):
    n = name.replace("check_", "")
    if n.startswith("T_") or (n.startswith("T") and n[1:2].isdigit()):
        return "theorem"
    if n.startswith("L_"):
        return "lemma"
    if n.startswith("RT_"):
        return "red_team"
    return "other"


def run_module(mod_name, verbose=False):
    results = []
    try:
        mod = importlib.import_module(mod_name)
    except ModuleNotFoundError as e:
        return results, f"SKIP ({e})"
    except Exception as e:
        return results, f"IMPORT ERROR: {e}"

    checks = sorted(
        (name, fn)
        for name, fn in vars(mod).items()
        if name.startswith("check_") and callable(fn)
    )

    for name, fn in checks:
        status = "PASS"
        error_msg = None
        try:
            ret = fn()
            # Inspect return value: red-team and some structural checks
            # return {"passed": False, ...} without raising. Treat that as
            # a FLAG (distinct from FAIL = exception, distinct from PASS).
            if isinstance(ret, dict):
                passed = ret.get("passed")
                if passed is False:
                    status = "FLAG"
                    error_msg = (
                        ret.get("summary")
                        or ret.get("key_result")
                        or "passed=False"
                    )
                # Some legacy checks return {"status": "FAIL", ...}
                inner_status = ret.get("status")
                if isinstance(inner_status, str) and inner_status.upper() == "FAIL":
                    status = "FAIL"
                    error_msg = (
                        ret.get("summary")
                        or ret.get("error")
                        or "status=FAIL"
                    )
        except Exception as e:
            status = "FAIL"
            error_msg = str(e)
            if verbose:
                traceback.print_exc()
        results.append({
            "name": name,
            "category": classify(name),
            "status": status,
            "error": error_msg,
        })

    return results, None


def run_prelude_silently(prelude_mod_names):
    """Run DAG-producing modules silently to populate the DAG cache.

    Used when `--module` filter is active and the filtered set excludes
    upstream DAG producers. Runs each prelude module's check_* functions
    best-effort: exceptions inside checks don't propagate (the DAG will
    simply be missing the keys that the failing check would have
    written, which will produce a clear error downstream via the
    dag_has guards in consumer code).

    Returns
    -------
    tuple
        (n_modules_run, n_checks_run) for a one-line banner.
    """
    n_modules = 0
    n_checks = 0
    for mod_name in prelude_mod_names:
        try:
            mod = importlib.import_module(mod_name)
        except Exception:
            continue
        n_modules += 1
        check_names = sorted(n for n in dir(mod) if n.startswith('check_'))
        for name in check_names:
            try:
                fn = getattr(mod, name)
                if callable(fn):
                    fn()
                    n_checks += 1
            except Exception:
                pass  # best-effort — missing DAG keys will surface in the filtered run
    return n_modules, n_checks


def print_prediction_scorecard():
    try:
        from apf.validation import check_L_prediction_catalog
        r = check_L_prediction_catalog()
        print()
        print("Prediction scorecard")
        print("-" * 44)
        if isinstance(r, dict) and "summary" in r:
            print(r["summary"])
        else:
            print("  (run apf/validation.py directly for full catalog)")
    except Exception as e:
        print(f"\nPrediction scorecard unavailable: {e}")


# ── Interface Engine operational phase (optional, opt-in via --with-engine) ───

def run_engine_phase(verbose: bool = False) -> dict:
    """Interface Engine operational phase (Sprints A-D) inline.

    Returns a dict {sprint_id: {status, detail}} that the caller summarizes.
    All four sprints run against live framework state.  Failures are surfaced
    as advisory: they do not break the standard verify_all exit code unless
    --strict-engine is also passed.
    """
    summary: dict = {}

    # Sprint A — registry-bridge live integration
    try:
        from apf.interface_intelligence_registry_bridge import build_registry_bridge_report
        rep = build_registry_bridge_report()
        summary["A_registry_bridge"] = {
            "status": "PASS" if rep.ready else "FAIL",
            "detail": f"15 top-check specs, ready={rep.ready}",
        }
    except Exception as exc:
        summary["A_registry_bridge"] = {"status": "ERROR", "detail": repr(exc) if verbose else type(exc).__name__}

    # Sprint B — EW live obligation
    try:
        from apf.ew_trace_to_scheme_real_adapter import build_live_adapter_report as ew_live
        rep_dict = ew_live(name="verify_all_engine_phase_ew").to_dict()
        pkt = rep_dict["obligation_packet"]
        ledger = rep_dict["certification"].get("ledger_certificate", {}).get("ledger", {})
        miss = [m.get("kind") for m in ledger.get("missing_required", [])]
        summary["B_ew_live"] = {
            "status": "PASS" if pkt.get("packet_status") else "FAIL",
            "detail": f"packet={pkt.get('packet_status')}; missing={miss}",
        }
    except Exception as exc:
        summary["B_ew_live"] = {"status": "ERROR", "detail": repr(exc) if verbose else type(exc).__name__}

    # Sprint C — dark live obligation
    try:
        from apf.dark_posterior_real_adapter import build_live_adapter_report as dark_live
        rep_dict = dark_live(name="verify_all_engine_phase_dark").to_dict()
        pkt = rep_dict["obligation_packet"]
        ledger = rep_dict["certification"].get("ledger_certificate", {}).get("ledger", {})
        miss = [m.get("kind") for m in ledger.get("missing_required", [])]
        summary["C_dark_live"] = {
            "status": "PASS" if pkt.get("packet_status") else "FAIL",
            "detail": f"packet={pkt.get('packet_status')}; missing={miss}",
        }
    except Exception as exc:
        summary["C_dark_live"] = {"status": "ERROR", "detail": repr(exc) if verbose else type(exc).__name__}

    # Sprint D — atlas v0.1 across 4 routes
    try:
        from apf.interface_atlas import AtlasInput, AtlasInputKind, build_interface_atlas
        from apf.ew_trace_to_scheme_real_adapter import build_live_adapter_report as ew_live
        from apf.dark_posterior_real_adapter import build_live_adapter_report as dark_live
        ew_rep = ew_live(name="atlas_input_ew").to_dict()
        dark_rep = dark_live(name="atlas_input_dark").to_dict()
        inputs = [
            AtlasInput("ew_live", AtlasInputKind.ROUTE_PAYLOAD, "ew", None, dict(ew_rep["payload"])),
            AtlasInput("dark_live", AtlasInputKind.ROUTE_PAYLOAD, "dark", None, dict(dark_rep["payload"])),
            AtlasInput("gauge_claim", AtlasInputKind.CLAIM, "gauge",
                       "The gauge group SU(3)_c x SU(2)_L x U(1)_Y supports the four PLEC features.", None),
            AtlasInput("horizon_claim", AtlasInputKind.CLAIM, "horizon",
                       "The horizon-area-as-fiber-cost reading recovers the Bekenstein bound.", None),
        ]
        atlas = build_interface_atlas(inputs, atlas_name="verify_all_engine_phase_v0.1")
        n_routes = len(atlas.route_summaries)
        top_obs = sorted(atlas.obstruction_counts.items(), key=lambda kv: -kv[1])[:3]
        summary["D_atlas"] = {
            "status": "PASS" if n_routes >= 4 else "FAIL",
            "detail": f"{n_routes} routes; top bottlenecks: " + ", ".join(f"{k}({v})" for k, v in top_obs),
        }
    except Exception as exc:
        summary["D_atlas"] = {"status": "ERROR", "detail": repr(exc) if verbose else type(exc).__name__}

    return summary


def print_engine_phase_summary(summary: dict) -> int:
    """Print the engine phase summary. Returns 0 if all PASS, 1 otherwise."""
    print()
    print("=" * 55)
    print("INTERFACE ENGINE OPERATIONAL PHASE")
    print("=" * 55)
    for sprint, s in summary.items():
        mark = "PASS" if s["status"] == "PASS" else "----"
        print(f"  [{mark}] {sprint:22s} {s['status']:6s} {s['detail']}")
    n_pass = sum(1 for s in summary.values() if s["status"] == "PASS")
    n_total = len(summary)
    overall = "PASS" if n_pass == n_total else "FAIL"
    print()
    print(f"  Engine phase: {n_pass}/{n_total} PASS")
    print(f"  INTERFACE_ENGINE_VERIFY_ALL_PHASE_{overall}")
    return 0 if overall == "PASS" else 1


# ── Main ─────────────────────────────────────────────────────────────────────



def _run_engine_only(args) -> int:
    """--engine-only: run Sprints A-D inline, skip the full bank.

    Fast CI lane: the engine phase doesn't need the full 3000+ check bank verification.
    Exit code 0 iff all 4 sprints PASS.
    """
    import json
    print("APF Interface Engine — Operational Phase (Sprints A-D)")
    print("=" * 55)
    summary = run_engine_phase(verbose=args.verbose)
    rc = print_engine_phase_summary(summary)
    if args.json_out:
        from pathlib import Path
        Path(args.json_out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.json_out).write_text(
            json.dumps(summary, indent=2, default=str),
            encoding="utf-8",
        )
        print(f"\nJSON output: {args.json_out}")
    return rc


def _run_interface_ci(args) -> int:
    """--interface-ci: run the Interface Intelligence CI orchestrator directly.

    Returns the release gate status (14-check release gate). Faster than running the
    orchestrator through the full bank prelude path.
    """
    import json
    print("APF Interface Intelligence CI Orchestrator")
    print("=" * 55)
    try:
        from apf.interface_intelligence_CI_orchestrator import run_interface_intelligence_CI
    except Exception as exc:
        print(f"  FAIL: could not import orchestrator: {exc}")
        return 2
    report = run_interface_intelligence_CI()
    rd = report.to_dict() if hasattr(report, "to_dict") else dict(report.__dict__)
    counts = rd.get("summary_counts") or rd.get("counts") or {}
    print(f"  release_gate_pass: {rd.get('release_gate_pass')}")
    print(f"  release_gate_reason: {rd.get('release_gate_reason', '')[:120]}")
    if counts:
        print(f"  counts: {counts}")
    if args.json_out:
        from pathlib import Path
        Path(args.json_out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.json_out).write_text(
            json.dumps(rd, indent=2, default=str),
            encoding="utf-8",
        )
        print(f"\nJSON output: {args.json_out}")
    return 0 if rd.get("release_gate_pass") else 1


def _compute_bank_audit_buckets() -> dict:
    """Categorize the bank-load gap into the 4-bucket triage.

    Buckets:
      A — modules that failed to import (sandbox or optional-dep blocked; production likely loads them)
      B — modules that imported but registered 0 checks (after architecture-only whitelist filter)
      C — modules with more static check_* defs than registered checks (helper sub-checks)
      D — stale EXPECTED arithmetic (total static defs vs EXPECTED constant)
    """
    import importlib, re, warnings
    from pathlib import Path
    warnings.filterwarnings("ignore", category=RuntimeWarning)
    import apf.bank as bank
    bank._load()

    here = Path(__file__).parent
    failed_imports = []
    zero_check_loaded = []
    helper_subcheck_delta = []
    total_static_defs = 0

    for mod_path in bank._MODULE_PATHS:
        mod_name = mod_path.split(".")[-1]
        registered = bank._MODULE_MAP.get(mod_name, [])

        rel = mod_path.replace(".", "/") + ".py"
        f = here / rel
        if not f.exists():
            continue
        src = f.read_text(encoding="utf-8", errors="replace")
        n_static = len(re.findall(r"^def check_\w+", src, re.MULTILINE))
        total_static_defs += n_static

        if not registered:
            if mod_path in ARCHITECTURE_ONLY_WHITELIST:
                continue  # expected zero-check by design
            try:
                importlib.import_module(mod_path)
                zero_check_loaded.append(mod_path)
            except Exception as exc:
                failed_imports.append({
                    "module": mod_path,
                    "exception_type": type(exc).__name__,
                    "exception_message": str(exc)[:200],
                    "static_check_defs": n_static,
                })
        else:
            if n_static > len(registered) + 2:
                helper_subcheck_delta.append({
                    "module": mod_path,
                    "static_defs": n_static,
                    "registered": len(registered),
                    "delta": n_static - len(registered),
                })

    return {
        "expected_theorem_count": bank.EXPECTED_THEOREM_COUNT,
        "actual_registry_size": len(bank.REGISTRY),
        "gap": bank.EXPECTED_THEOREM_COUNT - len(bank.REGISTRY),
        "total_static_check_defs": total_static_defs,
        "stale_expected_estimate": bank.EXPECTED_THEOREM_COUNT - total_static_defs,
        "module_paths_count": len(bank._MODULE_PATHS),
        "module_paths_unique": len(set(bank._MODULE_PATHS)),
        "bucket_a_failed_imports": {
            "count": len(failed_imports),
            "items": failed_imports,
            "description": "Modules whose import failed (often scipy/optional-dep blocked in sandboxes). In a full environment these load.",
        },
        "bucket_b_zero_check_loaded": {
            "count": len(zero_check_loaded),
            "items": zero_check_loaded,
            "description": "Modules that imported cleanly but registered 0 checks (after architecture-only whitelist filter).",
        },
        "bucket_c_helper_subcheck_delta": {
            "count": len(helper_subcheck_delta),
            "items": helper_subcheck_delta,
            "description": "Modules with more static check_* defs than registered checks; delta is helper sub-checks not directly added to REGISTRY.",
        },
        "bucket_d_stale_expected": {
            "value": bank.EXPECTED_THEOREM_COUNT - total_static_defs,
            "description": "EXPECTED - total_static_check_defs. Positive means EXPECTED is incremented beyond what _MODULE_PATHS actually contains; suggests narrative-incremented EXPECTED needs re-derivation.",
        },
        "architecture_only_whitelist": sorted(ARCHITECTURE_ONLY_WHITELIST),
    }


def _run_bank_audit(args) -> int:
    """--bank-audit: 4-bucket triage of the bank-load gap."""
    import json
    print("APF Bank Audit — 4-bucket triage")
    print("=" * 55)
    result = _compute_bank_audit_buckets()
    print(f"  EXPECTED_THEOREM_COUNT:    {result['expected_theorem_count']}")
    print(f"  Actual REGISTRY size:      {result['actual_registry_size']}")
    print(f"  Gap (sandbox-environment): {result['gap']}")
    print(f"  Total static check_* defs: {result['total_static_check_defs']}")
    print(f"  Stale-EXPECTED estimate:   {result['stale_expected_estimate']}")
    print(f"  _MODULE_PATHS:             {result['module_paths_count']} entries ({result['module_paths_unique']} unique)")
    print()
    for key, label in [
        ("bucket_a_failed_imports", "Bucket A — failed imports"),
        ("bucket_b_zero_check_loaded", "Bucket B — loaded but 0 registered checks"),
        ("bucket_c_helper_subcheck_delta", "Bucket C — helper sub-check delta"),
        ("bucket_d_stale_expected", "Bucket D — stale EXPECTED arithmetic"),
    ]:
        info = result[key]
        print(f"{label}:")
        if "count" in info:
            print(f"  count: {info['count']}")
            for x in info.get("items", [])[:5]:
                if isinstance(x, dict):
                    print(f"    - {x.get('module', x)}")
                else:
                    print(f"    - {x}")
            if len(info.get("items", [])) > 5:
                print(f"    ... +{len(info['items'])-5} more")
        elif "value" in info:
            print(f"  value: {info['value']}")
        print()
    if args.json_out:
        from pathlib import Path
        Path(args.json_out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.json_out).write_text(
            json.dumps(result, indent=2, default=str),
            encoding="utf-8",
        )
        print(f"JSON output: {args.json_out}")
    return 0


def main():
    # v24.3.401 audit M3 (2026-07-05): some host consoles (Windows cp1252)
    # cannot encode the box-drawing characters in the scorecard; reconfigure
    # to UTF-8 with replacement rather than crash. No-op on healthy streams.
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass
    parser = argparse.ArgumentParser(description="APF Full Verification")
    parser.add_argument("--module", help="Run only checks matching this string (e.g. 'core')")
    parser.add_argument("--verbose", "-v", action="store_true", help="Print full tracebacks on failure")
    parser.add_argument("--no-scorecard", action="store_true", help="Skip prediction scorecard")
    parser.add_argument("--with-engine", action="store_true",
                        help="Run the Interface Engine operational phase (Sprints A-D) after the standard bank check. Advisory by default.")
    parser.add_argument("--strict-engine", action="store_true",
                        help="Treat Interface Engine phase failures as fatal exit codes (requires --with-engine).")
    # CI hardening lanes (added 2026-05-18):
    parser.add_argument("--engine-only", action="store_true",
                        help="Run ONLY the Interface Engine operational phase (Sprints A-D); skip the full bank. Fast.")
    parser.add_argument("--interface-ci", action="store_true",
                        help="Run ONLY the Interface Intelligence CI orchestrator (14-check release gate); skip the full bank. Fast.")
    parser.add_argument("--bank-audit", action="store_true",
                        help="Categorize the bank-load gap into the 4-bucket triage (failed-imports / zero-check-loaded / helper-subcheck-delta / stale-EXPECTED) and exit.")
    parser.add_argument("--bank-only", action="store_true",
                        help="Run only the standard bank verification (default behavior; explicit lane for CI clarity).")
    parser.add_argument("--quiet", action="store_true",
                        help="Suppress per-module narration; print summary only. Useful in CI where stdout is noisy.")
    parser.add_argument("--json-out", type=str, default=None,
                        help="Write structured JSON output to this path. Works with --engine-only, --interface-ci, --bank-audit.")
    args = parser.parse_args()

    # CI hardening lane dispatches — early-return before the full-bank flow.
    if args.engine_only:
        sys.exit(_run_engine_only(args))
    if args.interface_ci:
        sys.exit(_run_interface_ci(args))
    if args.bank_audit:
        sys.exit(_run_bank_audit(args))

    print("APF v16.1 — Full Verification")
    print("=" * 55)

    modules_to_run = MODULES
    if args.module:
        modules_to_run = [(m, f) for m, f in MODULES if args.module.lower() in m.lower()]
        if not modules_to_run:
            print(f"No modules matching '{args.module}' found.")
            sys.exit(1)

        # If the filter excludes upstream DAG-producing modules, silently
        # pre-run them so downstream consumers see a populated DAG. Without
        # this, e.g. `--module unification` fails because L_count in
        # apf.gauge has not yet written C_total, and the 2026-04-20 dag_has
        # guards in acc_SM raise loudly on missing keys (by design).
        filtered_names = {m for m, _ in modules_to_run}
        missing_prelude = [m for m in MODULES
                           if m[0] in PRELUDE_MODULES
                           and m[0] not in filtered_names]
        if missing_prelude:
            prelude_names = [m for m, _ in missing_prelude]
            n_mods, n_checks = run_prelude_silently(prelude_names)
            print(f"[prelude: ran {n_checks} checks across {n_mods} "
                  f"upstream DAG producer(s) to populate cache for filtered run]")
            print()

    all_results = []
    module_summaries = []
    t_start = time.time()

    for mod_name, file_label in modules_to_run:
        results, err = run_module(mod_name, verbose=args.verbose)
        n_pass = sum(1 for r in results if r["status"] == "PASS")
        n_fail = sum(1 for r in results if r["status"] == "FAIL")
        n_flag = sum(1 for r in results if r["status"] == "FLAG")
        n = len(results)

        if err:
            status_str = err
        elif n_fail == 0 and n_flag == 0 and n > 0:
            status_str = "PASS"
        elif n == 0:
            status_str = "no checks"
        elif n_fail == 0 and n_flag > 0:
            status_str = f"FLAG ({n_flag}/{n})"
        else:
            status_str = f"FAIL ({n_fail}/{n})"

        module_summaries.append((file_label, n, status_str))
        all_results.extend(results)

        if n_fail > 0:
            for r in results:
                if r["status"] == "FAIL":
                    print(f"  FAIL  {r['name']}")
                    if r["error"]:
                        print(f"        {r['error'][:120]}")
        if n_flag > 0:
            for r in results:
                if r["status"] == "FLAG":
                    print(f"  FLAG  {r['name']}")
                    if r["error"]:
                        print(f"        {r['error'][:120]}")

    elapsed = time.time() - t_start

    if not args.quiet:
        print(f"\n{'Module':<47} {'Checks':>6}  {'Status'}")
        print(f"{'──────':<47} {'──────':>6}  {'──────'}")
        for label, n, status in module_summaries:
            print(f"{label:<47} {n:>6}  {status}")

    cats = defaultdict(lambda: {"pass": 0, "fail": 0, "flag": 0})
    for r in all_results:
        if r["status"] == "PASS":
            cats[r["category"]]["pass"] += 1
        elif r["status"] == "FLAG":
            cats[r["category"]]["flag"] += 1
        else:
            cats[r["category"]]["fail"] += 1

    total_pass = sum(r["status"] == "PASS" for r in all_results)
    total_fail = sum(r["status"] == "FAIL" for r in all_results)
    total_flag = sum(r["status"] == "FLAG" for r in all_results)
    total = len(all_results)

    print()
    print("=" * 55)
    print(f"Total checks:    {total:>4}")
    print(f"  Theorems  [T]: {cats['theorem']['pass']:>4}  pass   {cats['theorem']['fail']:>3}  fail   {cats['theorem']['flag']:>3}  flag")
    print(f"  Lemmas    [L]: {cats['lemma']['pass']:>4}  pass   {cats['lemma']['fail']:>3}  fail   {cats['lemma']['flag']:>3}  flag")
    print(f"  Red-team [RT]: {cats['red_team']['pass']:>4}  pass   {cats['red_team']['fail']:>3}  fail   {cats['red_team']['flag']:>3}  flag")
    print(f"  Other:         {cats['other']['pass']:>4}  pass   {cats['other']['fail']:>3}  fail   {cats['other']['flag']:>3}  flag")
    print()

    if total_fail == 0 and total_flag == 0 and total > 0:
        print(f"\u2713 All {total} checks PASSED  ({elapsed:.1f}s)")
    elif total == 0:
        print("No checks found - check module paths.")
    elif total_fail == 0 and total_flag > 0:
        print(f"\u26a0 {total_pass}/{total} PASS, {total_flag} FLAG  ({elapsed:.1f}s)")
        print("\nFlagged checks (returned passed=False):")
        for r in all_results:
            if r["status"] == "FLAG":
                print(f"  {r['name']}")
                if r["error"]:
                    print(f"    {r['error'][:200]}")
    else:
        print(f"\u2717 FAILURES: {total_fail}/{total} checks FAILED  ({elapsed:.1f}s)")
        if total_flag > 0:
            print(f"  (also {total_flag} FLAG)")
        print("\nFailed checks:")
        for r in all_results:
            if r["status"] == "FAIL":
                print(f"  {r['name']}")
                if r["error"]:
                    print(f"    {r['error'][:200]}")

    if not args.no_scorecard:
        print_prediction_scorecard()

    # Interface Engine operational phase (opt-in via --with-engine).  Advisory
    # by default — engine status is surfaced but does not break the standard
    # exit code unless --strict-engine is also passed.
    engine_failed = False
    if args.with_engine:
        engine_summary = run_engine_phase(verbose=args.verbose)
        engine_rc = print_engine_phase_summary(engine_summary)
        engine_failed = engine_rc != 0
        if engine_failed and not args.strict_engine:
            print("  (engine phase advisory: standard exit code preserved)")

    # Exit code: 0 only if zero FAIL and zero FLAG. Treat FLAG as a non-fatal
    # but caller-visible non-zero exit (1) so CI / wrappers can detect them.
    if total_fail > 0:
        sys.exit(1)
    if total_flag > 0:
        sys.exit(1)
    if engine_failed and args.strict_engine:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
