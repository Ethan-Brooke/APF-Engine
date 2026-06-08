from apf import w_trace_source_authority_grading as m1
from apf import w_trace_prediction_cluster_robustness as m2
from apf import w_trace_residual_interpretation as m3
from apf import w_trace_publication_claim_language as m4
from apf import w_trace_v144_publication_validation_report as m5
mods=[m1,m2,m3,m4,m5]
rows=[]
for m in mods:
    out=m.run_all(); rows.extend(out["checks"]); print(out["status"])
ok=all(r["passed"] for r in rows)
print("SUMMARY", sum(r["passed"] for r in rows), "/", len(rows), "PASS")
print("W_TRACE_V14_4_PUBLICATION_VALIDATION_SPRINT_PASS" if ok else "W_TRACE_V14_4_PUBLICATION_VALIDATION_SPRINT_FAIL")
raise SystemExit(0 if ok else 1)
