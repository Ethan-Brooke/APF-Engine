#!/usr/bin/env python3
from __future__ import annotations
import json, os, sys, subprocess, shlex, pathlib
REQUIRED_FAMILIES = ["beta", "gamma_m", "decoupling", "mass_conversion"]
REQUIRED_DECOUPLING = ["zeta_g", "zeta_m"]
CASES = {
  "c": {"m0_GeV": 1.272334177712, "mu0_GeV": 1.272334177712, "mu1_GeV": 3.0, "alpha0": 0.38, "nf": 4},
  "b": {"m0_GeV": 4.177490455927, "mu0_GeV": 4.177490455927, "mu1_GeV": 10.0, "alpha0": 0.223, "nf": 5},
}
TARGET_FORBIDDEN_KEYS = ["pdg_target", "target_mass", "fit", "least_squares", "observed_mass", "m_c_pdg", "m_b_pdg"]

def payload():
    return {
        "schema":"APF_RunDec_Adapter_Request_v1",
        "module":"APF_v74",
        "cases":CASES,
        "required_outputs":["mass_target_GeV","alpha_target","loop_order","threshold_schedule","covariance","validation_id","no_target_reuse"],
        "forbidden_inputs":TARGET_FORBIDDEN_KEYS,
    }

def validate_coeff_table(path: str):
    try:
        data=json.loads(pathlib.Path(path).read_text())
    except Exception as e:
        return {"status":"FAIL_CLOSED","reason":"coefficient table unreadable","error":repr(e)}
    failures=[]
    if data.get("schema") not in ["APF_RunDec_Coefficient_Table_v1"]:
        failures.append("bad_schema")
    for fam in REQUIRED_FAMILIES:
        if fam not in data: failures.append(f"missing_{fam}")
    dec=data.get("decoupling",{}) if isinstance(data.get("decoupling",{}),dict) else {}
    for k in REQUIRED_DECOUPLING:
        if k not in dec: failures.append(f"missing_decoupling_{k}")
    if not data.get("source_manifest"):
        failures.append("missing_source_manifest")
    if not data.get("validation_examples"):
        failures.append("missing_validation_examples")
    if data.get("no_target_reuse_declaration") is not True:
        failures.append("missing_no_target_reuse_declaration")
    raw=json.dumps(data).lower()
    for k in TARGET_FORBIDDEN_KEYS:
        if k in raw:
            failures.append(f"forbidden_target_reuse_key_{k}")
    if failures:
        return {"status":"COEFFICIENT_TABLE_FAIL_CLOSED","failures":failures}
    return {"status":"COEFFICIENT_TABLE_SCHEMA_ACCEPTED_REQUIRES_NUMERIC_REVIEW","loop_orders":{k:data.get(k,{}).get("loop_order") for k in REQUIRED_FAMILIES},"sources":data.get("source_manifest")}

def call_adapter():
    cmd=os.environ.get("RUNDEC_CMD")
    if not cmd:
        return {"status":"ADAPTER_FAIL_CLOSED","reason":"RUNDEC_CMD not set"}
    try:
        proc=subprocess.run(shlex.split(cmd),input=json.dumps(payload()),text=True,capture_output=True,timeout=60)
    except Exception as e:
        return {"status":"ADAPTER_FAIL_CLOSED","reason":"invocation failed","error":repr(e)}
    if proc.returncode != 0:
        return {"status":"ADAPTER_FAIL_CLOSED","reason":"nonzero exit","stderr":proc.stderr[-2000:]}
    try:
        data=json.loads(proc.stdout)
    except Exception as e:
        return {"status":"ADAPTER_FAIL_CLOSED","reason":"non-json output","stdout":proc.stdout[:1000],"error":repr(e)}
    failures=[]
    if set(data.get("results",{}).keys()) != {"c","b"}: failures.append("missing_c_b_results")
    for field in ["validation_id","loop_order","threshold_schedule","covariance"]:
        if field not in data: failures.append("missing_"+field)
    if data.get("no_target_reuse") is not True: failures.append("missing_no_target_reuse_true")
    raw=json.dumps(data).lower()
    for k in TARGET_FORBIDDEN_KEYS:
        if k in raw: failures.append("forbidden_key_"+k)
    if failures:
        return {"status":"ADAPTER_FAIL_CLOSED","failures":failures,"adapter_output":data}
    return {"status":"RUNDEC_ADAPTER_ACCEPTED_REQUIRES_REVIEW","adapter_output":data}

def evaluate_full():
    adapter=call_adapter()
    coeff_path=os.environ.get("RUNDEC_COEFFICIENT_JSON")
    coeff = validate_coeff_table(coeff_path) if coeff_path else {"status":"COEFFICIENT_TABLE_FAIL_CLOSED","reason":"RUNDEC_COEFFICIENT_JSON not set"}
    if adapter.get("status")=="RUNDEC_ADAPTER_ACCEPTED_REQUIRES_REVIEW":
        return {"status":"FULL_RUNDEC_EVALUATOR_ADAPTER_AVAILABLE_REQUIRES_REVIEW","adapter":adapter,"coefficients":coeff}
    if coeff.get("status")=="COEFFICIENT_TABLE_SCHEMA_ACCEPTED_REQUIRES_NUMERIC_REVIEW":
        return {"status":"FULL_RUNDEC_EVALUATOR_COEFFICIENTS_AVAILABLE_REQUIRES_IMPLEMENTATION","adapter":adapter,"coefficients":coeff}
    return {"status":"FULL_RUNDEC_EVALUATOR_FAIL_CLOSED","adapter":adapter,"coefficients":coeff}

if __name__ == "__main__":
    mode=sys.argv[1] if len(sys.argv)>1 else "full"
    if mode=="payload": out=payload()
    elif mode=="adapter": out=call_adapter()
    elif mode=="coeff":
        path=sys.argv[2] if len(sys.argv)>2 else os.environ.get("RUNDEC_COEFFICIENT_JSON","")
        out=validate_coeff_table(path) if path else {"status":"COEFFICIENT_TABLE_FAIL_CLOSED","reason":"no path supplied"}
    elif mode=="full": out=evaluate_full()
    else: out={"status":"ERROR","reason":"mode must be payload, adapter, coeff, or full"}
    print(json.dumps(out, indent=2, sort_keys=True))
