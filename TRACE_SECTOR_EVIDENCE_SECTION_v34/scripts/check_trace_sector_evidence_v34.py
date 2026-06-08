#!/usr/bin/env python3
import csv, json, math, pathlib, sys
root = pathlib.Path(__file__).resolve().parents[1]
checks = []

def check(name, cond, detail=""):
    checks.append((name, bool(cond), detail))

# Load data
with open(root/"reports"/"trace_sector_evidence_v34_data.json") as f:
    data = json.load(f)

# Files present
required = [
    "paper/TRACE_SECTOR_EVIDENCE_SECTION_v34.tex",
    "tables/trace_sector_master_evidence_table_v34.csv",
    "tables/trace_sector_claim_ladder_v34.csv",
    "tables/trace_sector_no_smuggling_audit_v34.csv",
    "reports/trace_sector_evidence_summary_v34.md",
    "reports/trace_sector_evidence_v34_data.json",
]
for rel in required:
    check(f"file_present:{rel}", (root/rel).exists(), rel)

# Master table
with open(root/"tables"/"trace_sector_master_evidence_table_v34.csv", newline="") as f:
    rows = list(csv.DictReader(f))
objects = {r["object"]: r for r in rows}
for obj in ["sin2_theta_W", "M_W_APF_to_OS", "bottom", "top", "charged_leptons", "charm", "light_quarks"]:
    check(f"master_object_present:{obj}", obj in objects, obj)

# Core calculations
MW_trace = data["ew"]["M_W_APF_TRACE_GeV"]
MW_dizet = data["ew"]["M_W_DIZET_same_input_GeV"]
delta_mev = (MW_dizet - MW_trace) * 1000
check("MW_delta_matches", abs(delta_mev - data["ew"]["delta_MW_MeV"]) < 1e-9, str(delta_mev))
calc_pull = abs(data["ew"]["delta_MW_MeV"]) / data["ew"]["sigma_input_theory_MeV"]
check("MW_pull_matches", abs(calc_pull - data["ew"]["pull_sigma"]) < 1e-6, str(calc_pull))
check("sin2_trace_present", data["ew"]["sin2_theta_W_trace"] == "3/13")
check("gprime_ratio_present", data["ew"]["gprime_over_g"] == "sqrt(3/10)")

# Export candidates exactly W + bottom
check("export_candidates_exact", set(data["export_candidates"]) == {"W", "bottom"}, str(data["export_candidates"]))
check("bottom_export_candidate", "export_candidate" in data["fermions"]["bottom"]["status"], data["fermions"]["bottom"]["status"])
for sector in ["top", "charged_leptons", "charm", "light_quarks"]:
    check(f"{sector}_not_export", "export_candidate" not in data["fermions"][sector]["status"], data["fermions"][sector]["status"])

# No-smuggling audit
with open(root/"tables"/"trace_sector_no_smuggling_audit_v34.csv", newline="") as f:
    audit = list(csv.DictReader(f))
check("audit_rows_present", len(audit) >= 6, str(len(audit)))
check("all_audit_pass", all(r["status"] == "PASS" for r in audit), str([r["gate"] for r in audit if r["status"] != "PASS"]))
check("no_target_consumption", data["no_smuggling"]["target_consumption"] is False)
check("codomain_separation", data["no_smuggling"]["codomain_separation"] is True)
check("negative_controls_retained", data["no_smuggling"]["negative_controls_retained"] is True)
check("unresolved_not_promoted", data["no_smuggling"]["unresolved_branches_not_promoted"] is True)

# Claim ladder safe/forbidden
with open(root/"tables"/"trace_sector_claim_ladder_v34.csv", newline="") as f:
    claims = list(csv.DictReader(f))
check("claim_ladder_rows", len(claims) >= 8, str(len(claims)))
check("all_claims_safe", all(r["status"] == "SAFE" for r in claims))
check("forbidden_language_nonempty", all(r["forbidden_language"] for r in claims))

# Paper text gates
paper = (root/"paper"/"TRACE_SECTOR_EVIDENCE_SECTION_v34.tex").read_text()
for token in [
    "M_W^{\\rm APF\\text{-}TRACE}",
    "1.0900344137",
    "fermion trace sector locally closed",
    "physical export is route-dependent",
    "no-smuggling",
]:
    check(f"paper_contains:{token[:20]}", token in paper, token)

passed = sum(1 for _, ok, _ in checks if ok)
total = len(checks)
report_path = root/"reports"/"trace_sector_evidence_v34_targeted.txt"
with open(report_path, "w") as f:
    for name, ok, detail in checks:
        f.write(f"{'PASS' if ok else 'FAIL'} {name} {detail}\n")
    f.write(f"TRACE_SECTOR_EVIDENCE_SECTION_PASS {passed}/{total}\n" if passed == total else f"TRACE_SECTOR_EVIDENCE_SECTION_FAIL {passed}/{total}\n")
print(f"TRACE_SECTOR_EVIDENCE_SECTION_{'PASS' if passed == total else 'FAIL'} {passed}/{total}")
if passed != total:
    sys.exit(1)
