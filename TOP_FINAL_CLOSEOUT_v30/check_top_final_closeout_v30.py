#!/usr/bin/env python3
import json, csv
from pathlib import Path
base=Path(__file__).resolve().parent
data=json.loads((base/'top_final_closeout_v30_data.json').read_text())
checks=[]
def ck(n,c): checks.append((n,bool(c)))
ck('status', data['pass_status']=='TOP_FINAL_CLOSEOUT_PASS')
ck('export_blocked', data['physical_export_status']=='BLOCKED_NOT_CLAIMED')
ck('trace_between_contexts', data['external_anchors']['MSbar_self_scale_context_GeV'] < data['apf_trace']['m_t_APF_TRACE_GeV'] < data['external_anchors']['pole_context_GeV'])
ck('external_msr_closed', data['closure_decision']['external_MSR_codomain']=='CLOSED')
ck('terminal_gate_named', 'MSR_SCALE_SELECTION' in data['closure_decision']['terminal_gate'])
with open(base/'top_final_checks_v30.csv') as f:
    for r in csv.DictReader(f): ck('csv_'+r['check'], r['pass']=='True')
failed=[n for n,p in checks if not p]
if failed:
    print('TOP_FINAL_CLOSEOUT_FAIL')
    for f in failed: print('FAIL', f)
    raise SystemExit(1)
print(f'TOP_FINAL_CLOSEOUT_PASS: {len(checks)}/{len(checks)} PASS')
