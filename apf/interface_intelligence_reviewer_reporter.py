"""
APF Interface Intelligence Reviewer Reporter.

Purpose
-------
Convert interface-intelligence JSON reports into reviewer/integrator-facing status text:

    CI / atlas / adapter / claim audit reports
      -> banked / held / blocked status table
      -> safe claim-boundary language
      -> next-evidence checklist
      -> compact markdown report

Boundary
--------
This reporter summarizes certificates and obligations. It does not promote claims.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Iterable, Mapping, Optional, Tuple, List
import json


class ReviewerStatus(str, Enum):
    BANKED_P = "BANKED_P"
    HELD_FOR_REPAIR = "HELD_FOR_REPAIR"
    FAIL_CLOSED_PROVENANCE = "FAIL_CLOSED_PROVENANCE"
    STRUCTURAL_BLOCK = "STRUCTURAL_BLOCK"
    INTEGRATION_FAIL = "INTEGRATION_FAIL"
    UNKNOWN = "UNKNOWN"
    # v24.3.41 — Step D audit Findings (Mass-sector 2/3 + RDFI 2):
    OBSTRUCTION_NAMED_CLOSURE = "OBSTRUCTION_NAMED_CLOSURE"
    INTERNAL_IDENTITY_GLOBAL_P = "INTERNAL_IDENTITY_GLOBAL_P"
    SUBSTRATE_REVISION_REQUIRED = "SUBSTRATE_REVISION_REQUIRED"


@dataclass(frozen=True)
class ReviewerFinding:
    item_id: str
    route: str
    status: ReviewerStatus
    summary: str
    safe_language: str
    next_evidence: Tuple[str, ...]
    source: str

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["status"] = self.status.value
        return d


@dataclass(frozen=True)
class ReviewerReport:
    title: str
    findings: Tuple[ReviewerFinding, ...]
    overall_summary: str
    markdown: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "findings": [f.to_dict() for f in self.findings],
            "overall_summary": self.overall_summary,
            "markdown": self.markdown,
        }


def _load_json(path: str | Path) -> Mapping[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _cert_from_report(report: Mapping[str, Any]) -> Mapping[str, Any]:
    # Claim/compiler and adapters usually use this path.
    try:
        return report["certification"]["ledger_certificate"]["certificate"]
    except Exception:
        pass
    try:
        return report["movement_graph"]["certificate"]
    except Exception:
        pass
    if "original_certificate" in report:
        return report["original_certificate"]
    return {}


def _route_from_report(report: Mapping[str, Any]) -> str:
    for path in [
        ("compilation", "route"),
        ("payload", "name"),
        ("route",),
    ]:
        cur: Any = report
        ok = True
        for key in path:
            if isinstance(cur, Mapping) and key in cur:
                cur = cur[key]
            else:
                ok = False
                break
        if ok and cur is not None:
            return str(cur)
    payload = report.get("payload", {})
    if isinstance(payload, Mapping):
        name = str(payload.get("name", "unknown"))
        if "ew" in name.lower():
            return "ew"
        if "dark" in name.lower():
            return "dark"
    return "unknown"


def _status_from_cert_and_packet(cert: Mapping[str, Any], packet_status: Optional[str], frontier_status: Optional[str]) -> ReviewerStatus:
    solver = str(cert.get("solver_status", ""))
    obstruction = tuple(cert.get("obstruction", ()))
    # v24.3.41 — Mass-sector Step D Findings 2/3 + RDFI Finding 2: explicit handling
    # for new InterfaceSolverStatus values + BLOCKED_SUBSTRATE_REVISION_REQUIRED.
    if solver == "INTERNAL_IDENTITY_GLOBAL_P":
        return ReviewerStatus.INTERNAL_IDENTITY_GLOBAL_P
    if solver == "OBSTRUCTION_NAMED_CLOSURE":
        return ReviewerStatus.OBSTRUCTION_NAMED_CLOSURE
    if solver == "BLOCKED_SUBSTRATE_REVISION_REQUIRED":
        return ReviewerStatus.SUBSTRATE_REVISION_REQUIRED
    if cert.get("export_global_P") is True or solver == "SOLVED_GLOBAL_P":
        return ReviewerStatus.BANKED_P
    if solver == "FAIL_CLOSED_PROVENANCE" or "PROVENANCE_SMUGGLE" in obstruction or packet_status == "BLOCKED_PROVENANCE_REBUILD_REQUIRED":
        return ReviewerStatus.FAIL_CLOSED_PROVENANCE
    if packet_status == "BLOCKED_SUBSTRATE_THEOREM_REQUIRED" or frontier_status == "REFUSE_SUBSTRATE_FRONTIER" or "STRUCTURAL_BLOCKER" in obstruction:
        return ReviewerStatus.STRUCTURAL_BLOCK
    if solver == "SOLVED_LOCAL_HELD_FOR_REPAIR" or packet_status == "OPEN_EVIDENCE_REQUIRED":
        return ReviewerStatus.HELD_FOR_REPAIR
    if solver.startswith("FAIL") or solver == "UNSUPPORTED":
        return ReviewerStatus.INTEGRATION_FAIL
    return ReviewerStatus.UNKNOWN


def _obligation_fields(report: Mapping[str, Any]) -> Tuple[str, ...]:
    packet = report.get("obligation_packet", report)
    fields: List[str] = []
    for bundle in packet.get("bundles", []) if isinstance(packet, Mapping) else []:
        for obl in bundle.get("obligations", []):
            field = obl.get("field")
            if field and field not in fields:
                fields.append(str(field))
    # Atlas summaries can carry critical_fields.
    for f in report.get("critical_fields", []) if isinstance(report, Mapping) else []:
        if f not in fields:
            fields.append(str(f))
    return tuple(fields)


def _safe_language(status: ReviewerStatus, route: str, fields: Tuple[str, ...]) -> str:
    if status == ReviewerStatus.BANKED_P:
        return f"{route}: the interface certificate reports global P for this route."
    if status == ReviewerStatus.HELD_FOR_REPAIR:
        needed = ", ".join(fields[:6]) if fields else "the missing interface evidence"
        return f"{route}: held for repair; do not promote to global P until {needed} are supplied and the gate is rerun."
    if status == ReviewerStatus.FAIL_CLOSED_PROVENANCE:
        return f"{route}: fail-closed on provenance; rebuild from clean inputs before any promotion attempt."
    if status == ReviewerStatus.STRUCTURAL_BLOCK:
        return f"{route}: structural/substrate blocker; ordinary evidence patching is insufficient and a theorem-level repair is required."
    if status == ReviewerStatus.INTEGRATION_FAIL:
        return f"{route}: integration or unsupported-route failure; inspect the emitted report before using this claim."
    return f"{route}: status unknown; treat as not promoted."


def finding_from_report(item_id: str, report: Mapping[str, Any], *, source: str = "json") -> ReviewerFinding:
    cert = _cert_from_report(report)
    packet = report.get("obligation_packet", {})
    frontier = report.get("frontier", {})
    packet_status = packet.get("packet_status") if isinstance(packet, Mapping) else report.get("packet_status")
    frontier_status = frontier.get("frontier_status") if isinstance(frontier, Mapping) else report.get("frontier_status")
    route = _route_from_report(report)
    status = _status_from_cert_and_packet(cert, packet_status, frontier_status)
    fields = _obligation_fields(report)

    solver = cert.get("solver_status", "UNKNOWN")
    obstruction = cert.get("obstruction", [])
    summary = f"solver_status={solver}; export_global_P={cert.get('export_global_P')}; obstruction={obstruction}; packet_status={packet_status}"
    return ReviewerFinding(
        item_id=item_id,
        route=route,
        status=status,
        summary=summary,
        safe_language=_safe_language(status, route, fields),
        next_evidence=fields,
        source=source,
    )


def findings_from_atlas(atlas: Mapping[str, Any], *, source: str = "atlas") -> Tuple[ReviewerFinding, ...]:
    findings: List[ReviewerFinding] = []
    for idx, row in enumerate(atlas.get("route_summaries", [])):
        cert = {
            "solver_status": row.get("solver_status"),
            "export_global_P": row.get("export_global_P"),
            "obstruction": row.get("obstruction", []),
        }
        fake = {
            "route": row.get("route", "unknown"),
            "original_certificate": cert,
            "packet_status": row.get("packet_status"),
            "critical_fields": row.get("critical_fields", []),
        }
        findings.append(finding_from_report(row.get("input_id", f"atlas:{idx}"), fake, source=source))
    return tuple(findings)


def render_markdown_report(title: str, findings: Iterable[ReviewerFinding]) -> str:
    findings = tuple(findings)
    counts: Dict[str, int] = {}
    for f in findings:
        counts[f.status.value] = counts.get(f.status.value, 0) + 1

    lines = [
        f"# {title}",
        "",
        "## Status counts",
        "",
    ]
    for status in ReviewerStatus:
        if counts.get(status.value, 0):
            lines.append(f"- **{status.value}**: {counts[status.value]}")
    if not any(counts.values()):
        lines.append("- No findings.")

    lines += [
        "",
        "## Findings",
        "",
        "| Item | Route | Status | Safe language | Next evidence |",
        "|---|---|---|---|---|",
    ]

    for f in findings:
        evidence = ", ".join(f.next_evidence) if f.next_evidence else "—"
        lines.append(f"| `{f.item_id}` | `{f.route}` | `{f.status.value}` | {f.safe_language} | {evidence} |")

    lines += [
        "",
        "## Boundary",
        "",
        "This report summarizes interface certificates and obligations. It does not promote held claims to P.",
    ]
    return "\n".join(lines) + "\n"


def build_reviewer_report_from_json_files(paths: Iterable[str | Path], *, title: str = "APF Interface Intelligence Reviewer Report") -> ReviewerReport:
    findings: List[ReviewerFinding] = []
    for path in paths:
        p = Path(path)
        report = _load_json(p)
        if "route_summaries" in report:
            findings.extend(findings_from_atlas(report, source=str(p)))
        elif "module_results" in report and "release_gate_pass" in report:
            # CI report: summarize as integration status finding.
            status = ReviewerStatus.BANKED_P if report.get("release_gate_pass") else ReviewerStatus.INTEGRATION_FAIL
            findings.append(ReviewerFinding(
                item_id=p.stem,
                route="ci",
                status=status,
                summary=str(report.get("release_gate_reason", "")),
                safe_language="Interface-intelligence software CI passed." if status == ReviewerStatus.BANKED_P else "Interface-intelligence CI did not fully pass; inspect module_results.",
                next_evidence=tuple(),
                source=str(p),
            ))
        else:
            findings.append(finding_from_report(p.stem, report, source=str(p)))

    md = render_markdown_report(title, findings)
    counts: Dict[str, int] = {}
    for f in findings:
        counts[f.status.value] = counts.get(f.status.value, 0) + 1
    overall = "; ".join(f"{k}={v}" for k, v in sorted(counts.items())) or "no findings"
    return ReviewerReport(title=title, findings=tuple(findings), overall_summary=overall, markdown=md)


def write_reviewer_report(paths: Iterable[str | Path], out_md: str | Path, out_json: Optional[str | Path] = None, *, title: str = "APF Interface Intelligence Reviewer Report") -> ReviewerReport:
    report = build_reviewer_report_from_json_files(paths, title=title)
    Path(out_md).write_text(report.markdown, encoding="utf-8")
    if out_json:
        Path(out_json).write_text(json.dumps(report.to_dict(), indent=2, sort_keys=True), encoding="utf-8")
    return report


def canonical_example_reports() -> Dict[str, Mapping[str, Any]]:
    held = {
        "payload": {"name": "ew_claim"},
        "certification": {"ledger_certificate": {"certificate": {
            "solver_status": "SOLVED_LOCAL_HELD_FOR_REPAIR",
            "export_global_P": False,
            "obstruction": ["EVALUATOR_MISSING", "CODOMAIN_MISMATCH"],
        }}},
        "obligation_packet": {"packet_status": "OPEN_EVIDENCE_REQUIRED", "bundles": [
            {"obligations": [
                {"field": "evaluator_map_found"},
                {"field": "codomain_transport_found"},
            ]}
        ]},
    }
    banked = {
        "payload": {"name": "dark_clean"},
        "certification": {"ledger_certificate": {"certificate": {
            "solver_status": "SOLVED_GLOBAL_P",
            "export_global_P": True,
            "obstruction": [],
        }}},
        "obligation_packet": {"packet_status": "NOT_REQUIRED_ALREADY_P", "bundles": []},
    }
    prov = {
        "payload": {"name": "prov_fail"},
        "certification": {"ledger_certificate": {"certificate": {
            "solver_status": "FAIL_CLOSED_PROVENANCE",
            "export_global_P": False,
            "obstruction": ["PROVENANCE_SMUGGLE"],
        }}},
        "obligation_packet": {"packet_status": "BLOCKED_PROVENANCE_REBUILD_REQUIRED", "bundles": []},
    }
    struct = {
        "route": "cstar",
        "original_certificate": {
            "solver_status": "SOLVED_LOCAL_HELD_FOR_REPAIR",
            "export_global_P": False,
            "obstruction": ["STRUCTURAL_BLOCKER"],
        },
        "packet_status": "BLOCKED_SUBSTRATE_THEOREM_REQUIRED",
        "critical_fields": [],
    }
    return {"held": held, "banked": banked, "provenance": prov, "structural": struct}


def check_T_reviewer_reporter_classifies_status_P() -> Dict[str, Any]:
    reports = canonical_example_reports()
    findings = {k: finding_from_report(k, v) for k, v in reports.items()}
    tests = {
        "held": findings["held"].status == ReviewerStatus.HELD_FOR_REPAIR,
        "banked": findings["banked"].status == ReviewerStatus.BANKED_P,
        "provenance": findings["provenance"].status == ReviewerStatus.FAIL_CLOSED_PROVENANCE,
        "structural": findings["structural"].status == ReviewerStatus.STRUCTURAL_BLOCK,
    }
    return {
        "name": "check_T_reviewer_reporter_classifies_status_P",
        "consistent": all(tests.values()),
        "status": "P_reviewer_reporter" if all(tests.values()) else "FAIL",
        "summary": "Reviewer reporter classifies banked/held/provenance/structural statuses.",
        "data": {"tests": tests},
    }


def check_T_reviewer_reporter_safe_language_P() -> Dict[str, Any]:
    reports = canonical_example_reports()
    held = finding_from_report("held", reports["held"])
    prov = finding_from_report("prov", reports["provenance"])
    tests = {
        "held_says_do_not_promote": "do not promote" in held.safe_language.lower(),
        "held_mentions_rerun": "rerun" in held.safe_language.lower(),
        "prov_says_rebuild": "rebuild" in prov.safe_language.lower(),
        "held_evidence_fields": set(held.next_evidence) == {"evaluator_map_found", "codomain_transport_found"},
    }
    return {
        "name": "check_T_reviewer_reporter_safe_language_P",
        "consistent": all(tests.values()),
        "status": "P_reviewer_reporter" if all(tests.values()) else "FAIL",
        "summary": "Reviewer reporter emits conservative claim-boundary language and next evidence fields.",
        "data": {"tests": tests},
        "dependencies": ["check_T_reviewer_reporter_classifies_status_P"],
    }


def check_T_reviewer_reporter_markdown_P() -> Dict[str, Any]:
    findings = tuple(finding_from_report(k, v) for k, v in canonical_example_reports().items())
    md = render_markdown_report("Demo Report", findings)
    tests = {
        "has_title": "# Demo Report" in md,
        "has_table": "| Item | Route | Status |" in md,
        "has_boundary": "does not promote" in md,
        "has_all_statuses": "HELD_FOR_REPAIR" in md and "BANKED_P" in md and "FAIL_CLOSED_PROVENANCE" in md,
    }
    return {
        "name": "check_T_reviewer_reporter_markdown_P",
        "consistent": all(tests.values()),
        "status": "P_reviewer_reporter" if all(tests.values()) else "FAIL",
        "summary": "Reviewer reporter renders markdown status tables with boundary language.",
        "data": {"tests": tests},
        "dependencies": ["check_T_reviewer_reporter_safe_language_P"],
    }


def check_T_interface_intelligence_reviewer_reporter_P() -> Dict[str, Any]:
    subchecks = [
        check_T_reviewer_reporter_classifies_status_P(),
        check_T_reviewer_reporter_safe_language_P(),
        check_T_reviewer_reporter_markdown_P(),
    ]
    ok = all(x["consistent"] for x in subchecks)
    return {
        "name": "check_T_interface_intelligence_reviewer_reporter_P",
        "consistent": ok,
        "status": "P_reviewer_reporter" if ok else "FAIL",
        "summary": "Interface Intelligence Reviewer Reporter is P: JSON interface reports become reviewer-safe status language.",
        "data": {
            "core_claim": "The reporter converts certificates/obligations into safe human-facing status summaries without promoting held claims.",
            "subchecks": [x["name"] for x in subchecks],
        },
        "dependencies": [x["name"] for x in subchecks],
    }


CHECKS = {
    "check_T_reviewer_reporter_classifies_status_P": check_T_reviewer_reporter_classifies_status_P,
    "check_T_reviewer_reporter_safe_language_P": check_T_reviewer_reporter_safe_language_P,
    "check_T_reviewer_reporter_markdown_P": check_T_reviewer_reporter_markdown_P,
    "check_T_interface_intelligence_reviewer_reporter_P": check_T_interface_intelligence_reviewer_reporter_P,
}


def register(registry=None):
    if registry is None:
        return CHECKS
    if hasattr(registry, "update"):
        registry.update(CHECKS)
        return registry
    for name, fn in CHECKS.items():
        if hasattr(registry, "register"):
            registry.register(name, fn)
        elif hasattr(registry, "add"):
            registry.add(name, fn)
        else:
            raise TypeError("Unsupported registry type for interface_intelligence_reviewer_reporter.register")
    return registry


def run_all() -> Dict[str, Dict[str, Any]]:
    return {name: fn() for name, fn in CHECKS.items()}


if __name__ == "__main__":
    results = run_all()
    print(json.dumps(results, indent=2, sort_keys=True))
    raise SystemExit(0 if all(x.get("consistent") for x in results.values()) else 1)
