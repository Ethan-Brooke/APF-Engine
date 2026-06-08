"""Generate apf/crystal_snapshot_v6.9.json — the source-of-truth
numerical snapshot that Paper 20 v3.0 tables cite by row.

Runs:
  1. build_crystal('CORE')                     → full_graph + post_R_subgraph
  2. centrality_report                          (both views, top-15)
  3. cascade_analysis                           (both views, top-15)
  4. path_attribution_by_anchor                 (both views, one row per
                                                canonical Stage III sink)
  5. convergence_cluster_analysis               (both views, top-15)
  6. min_cut_table                              (post_R only; sinks =
                                                canonical Stage III sink set;
                                                sources = four PLEC anchors)
  7. Depth / width profile                      (both views)
  8. Epistemic split                             (full graph)
  9. Sector closures (default from dashboard_payload)

Writes the combined result to
``apf/crystal_snapshot_v6.9.json`` at ~UTF-8 pretty-indent-2. Stable
across reruns; every numerical claim in Paper 20 v3.0 traces to a row
in this file.

Usage
-----
    cd APF_Codebase_v6.9/
    python scripts/generate_crystal_snapshot.py

The snapshot path is relative to the codebase root (``apf/``); run
from the codebase root so the output lands inside the ``apf/`` package
directory.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

# Make the apf package importable when run from the codebase root.
_THIS = Path(__file__).resolve()
_ROOT = _THIS.parent.parent
sys.path.insert(0, str(_ROOT))

from apf.crystal import build_crystal, dashboard_payload, _DEFAULT_SECTOR_VERDICTS
from apf.crystal_metrics import (
    centrality_report,
    cascade_analysis,
    convergence_cluster_analysis,
    min_cut_table,
    path_attribution_by_anchor,
)


# Canonical Stage III sink set (shared across workstreams 3 + 4).
STAGE3_SINKS = [
    "T_sin2theta",
    "T_gauge",
    "T_PMNS",
    "T_mass_ratios",
    "L_count",
]


def _view_summary(graph) -> dict:
    """Depth + width profile, epistemic split, module split."""
    by_depth = {int(d): list(ids) for d, ids in graph.by_depth.items()}
    width_profile = {int(d): len(ids) for d, ids in by_depth.items()}

    epi_counts: dict[str, int] = {}
    for n in graph.nodes.values():
        epi_counts[n.epistemic] = epi_counts.get(n.epistemic, 0) + 1

    tier_counts: dict[int, int] = {}
    for n in graph.nodes.values():
        tier_counts[n.tier] = tier_counts.get(n.tier, 0) + 1

    module_counts: dict[str, int] = {}
    for n in graph.nodes.values():
        module_counts[n.module] = module_counts.get(n.module, 0) + 1

    return {
        "view":              graph.view,
        "preset":            graph.preset,
        "n_nodes":           graph.n_nodes,
        "n_edges":           graph.n_edges,
        "max_depth":         graph.max_depth,
        "width_profile":     width_profile,
        "by_depth":          by_depth,
        "waist_candidates":  graph.waist_candidates,
        "plec_anchor_ids":   list(graph.plec_anchor_ids),
        "notes":             list(graph.notes),
        "epistemic_counts":  dict(sorted(epi_counts.items())),
        "tier_counts":       {str(k): v for k, v in sorted(tier_counts.items())},
        "module_counts":     dict(sorted(module_counts.items())),
    }


def _attribution_for_all_sinks(graph, sinks: list[str], method: str = "depth_filtered") -> dict:
    """Path attribution per Stage III sink.

    method: "depth_filtered" (v3.0 baseline, drops same-depth edges) or
            "scc"            (v3.1+ primary, Tarjan SCC condensation —
                              cycle-aware, e.g., correctly attributes
                              through the Theorem_R ↔ T_gauge ↔ T_field
                              mutual-definition cycle).
    """
    out: dict[str, dict] = {}
    for s in sinks:
        if s not in graph.nodes:
            out[s] = {"error": f"sink {s!r} not in view"}
            continue
        out[s] = path_attribution_by_anchor(graph, s, anchor_filter="plec", method=method)
    return out


def _simplify_min_cut(mct: dict) -> dict:
    """Keep a paper-friendly projection of the min-cut table result."""
    rows = []
    for r in mct["rows"]:
        rows.append({
            "source":       r["source"],
            "source_role":  r.get("source_role", ""),
            "sink":         r["sink"],
            "reachable":    r["reachable"],
            "direct":       r["direct"],
            "cut_size":     r["cut_size"],
            "cut_witness":  list(r.get("cut_witness", [])),
        })
    return {
        "rows":           rows,
        "by_sink_min":    mct["by_sink_min"],
        "by_source_min":  mct["by_source_min"],
        "n_pairs":        mct["n_pairs"],
        "n_reachable":    mct["n_reachable"],
        "n_direct":       mct["n_direct"],
    }


def build_snapshot() -> dict:
    print("[1/7] Building CrystalGraph (CORE preset)...")
    crystal = build_crystal("CORE", do_prelude=True)
    full = crystal["full_graph"]
    post_R = crystal["post_R_subgraph"]
    print(f"      full_graph:    {full.n_nodes} nodes, {full.n_edges} edges, max_depth {full.max_depth}")
    print(f"      post_R_sub:    {post_R.n_nodes} nodes, {post_R.n_edges} edges, max_depth {post_R.max_depth}")

    print("[2/7] Centrality (Brandes BC, top-15)...")
    bc_full = centrality_report(full, top_k=15)
    bc_post = centrality_report(post_R, top_k=15)

    print("[3/7] Cascade analysis (top-15)...")
    casc_full = cascade_analysis(full, top_k=15, skip_anchors=True)
    casc_post = cascade_analysis(post_R, top_k=15, skip_anchors=True)

    print("[4/7] Path attribution per Stage III sink (both views, both methods)...")
    # v3.0 baseline (depth-filtered DAG-DP): retained for reproducibility.
    attr_full_df = _attribution_for_all_sinks(full,   STAGE3_SINKS, method="depth_filtered")
    attr_post_df = _attribution_for_all_sinks(post_R, STAGE3_SINKS, method="depth_filtered")
    # v3.1+ primary (Tarjan SCC condensation): cycle-aware; correctly counts
    # through Theorem_R ↔ T_gauge ↔ T_field and any other non-trivial SCC.
    attr_full_scc = _attribution_for_all_sinks(full,   STAGE3_SINKS, method="scc")
    attr_post_scc = _attribution_for_all_sinks(post_R, STAGE3_SINKS, method="scc")

    print("[5/7] Convergence-cluster analysis (top-15, min_fan_in=2)...")
    conv_full = convergence_cluster_analysis(full, top_k=15, min_fan_in=2)
    conv_post = convergence_cluster_analysis(post_R, top_k=15, min_fan_in=2)

    print("[6/7] Min vertex cuts (post_R, Stage III sinks × 4 PLEC anchors)...")
    mct_post = _simplify_min_cut(min_cut_table(post_R, STAGE3_SINKS))

    print("[7/7] View summaries + assembling payload...")
    full_sum = _view_summary(full)
    post_sum = _view_summary(post_R)

    # Truncate BC dicts to keep the snapshot small (top-50 each view).
    def _trim_bc(report, keep=50):
        items = sorted(report["bc"].items(), key=lambda kv: (-kv[1], kv[0]))
        return {
            "view":      report["view"],
            "preset":    report["preset"],
            "n_nodes":   report["n_nodes"],
            "n_edges":   report["n_edges"],
            "top_k":     report["top_k"],
            "stats":     report["stats"],
            "bc_top50":  dict(items[:keep]),
        }

    payload = {
        "version":           "APF v6.9 crystal snapshot",
        "preset":            "CORE",
        "stage3_sinks":      STAGE3_SINKS,
        "views": {
            "full_graph":      full_sum,
            "post_R_subgraph": post_sum,
        },
        "centrality": {
            "full_graph":      _trim_bc(bc_full),
            "post_R_subgraph": _trim_bc(bc_post),
        },
        "cascade": {
            "full_graph":      casc_full,
            "post_R_subgraph": casc_post,
        },
        "path_attribution": {
            # v3.1+ primary: SCC-aware (cycle-correct) — first-class field.
            "full_graph":      attr_full_scc,
            "post_R_subgraph": attr_post_scc,
            "method":          "scc",
            # v3.0 baseline: depth-filtered (drops same-depth edges) —
            # retained side-by-side for reproducibility of Paper 20 v3.0
            # numbers and for the v3.1 §5 contrast table.
            "_depth_filtered": {
                "full_graph":      attr_full_df,
                "post_R_subgraph": attr_post_df,
                "method":          "depth_filtered",
            },
        },
        "convergence": {
            "full_graph":      conv_full,
            "post_R_subgraph": conv_post,
        },
        "min_cut": {
            "post_R_subgraph": mct_post,
        },
        "sector_verdicts":   dict(_DEFAULT_SECTOR_VERDICTS),
    }

    return payload


def main():
    out_path = _ROOT / "apf" / "crystal_snapshot_v6.9.json"
    payload = build_snapshot()

    # Pretty-indent-2, ensure sorted keys within each dict level for
    # deterministic diffs across reruns.
    text = json.dumps(payload, indent=2, sort_keys=False, ensure_ascii=False, default=str)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(text)
        f.write("\n")
    size_kb = os.path.getsize(out_path) / 1024.0
    print(f"\n[done] Wrote {out_path.name} ({size_kb:.1f} KB)")


if __name__ == "__main__":
    main()
