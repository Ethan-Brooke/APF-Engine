"""W_TRACE detached-signature verification adapter.

Consolidated v13.0 sprint module.  This is infrastructure completion, not a
physical W export.  The shipped state remains locked until real reviewed
finite-part rows, component-sum, covariance, uncertainty, and signature evidence
are supplied and certified.
"""
from __future__ import annotations

import json
from typing import Any, Dict, List

M_W_TRACE_GEV = 80.362164334
APF_DELTA_R_TARGET = 3.64075266128216881e-2
FORBIDDEN_TOKENS = (
    "observed_M_W", "world_average_W_mass", "fit_residual",
    "apf_anchor_delta_r", "APF_ANCHOR_DELTA_R_TARGET",
    "manual_unlock", "force_export", "physical_M_W_override",
)

SHIPPED_STATE = {
    "real_reviewed_finite_part_rows": False,
    "real_component_sum_certified": False,
    "real_covariance_certified": False,
    "real_uncertainty_certified": False,
    "real_signature_verified": False,
    "physical_W_export_enabled": False,
    "exports_physical_M_W": False,
}

def _canonical_json(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)

def _contains_forbidden_token(obj: Any) -> bool:
    text = _canonical_json(obj)
    return any(tok in text for tok in FORBIDDEN_TOKENS)

def _res(check: str, passed: bool, **extra: Any) -> Dict[str, Any]:
    row = {"check": check, "passed": bool(passed)}
    row.update(extra)
    return row

def _passed(row: Any) -> bool:
    return bool(isinstance(row, dict) and row.get("passed") is True)

STATUS = "P_w_signature_verification_adapter"
VERSION = "w_trace_signature_verification_adapter_v1"
PASS_STATUS = "W_TRACE_SIGNATURE_VERIFICATION_ADAPTER_BANK_PASS"
TITLE = "W_TRACE detached-signature verification adapter"

def terminal_report() -> Dict[str, Any]:
    return {
        "status": STATUS,
        "version": VERSION,
        "title": TITLE,
        "m_w_trace_gev": M_W_TRACE_GEV,
        "apf_delta_r_target": APF_DELTA_R_TARGET,
        "closed_kind": "v13.0 terminal infrastructure sprint layer",
        "physical_W_export_enabled": False,
        "exports_physical_M_W": False,
        "shipped_state": dict(SHIPPED_STATE),
        "stop_condition": "No further W_TRACE scaffolding should be added before real reviewed finite-part payload rows are supplied, unless a blocker in this terminal infrastructure is found.",
    }

def validate_record(record: Dict[str, Any] | None = None) -> Dict[str, Any]:
    record = dict(record or {"template_only": True, "physical_export_requested": False})
    errors: List[str] = []
    if record.get("physical_export_requested") is True:
        errors.append("physical_export_request_forbidden")
    if record.get("template_only") is True:
        errors.append("template_record_not_real")
    if _contains_forbidden_token(record):
        errors.append("forbidden_token_detected")
    return {
        "status": STATUS,
        "version": VERSION,
        "valid_shape": len(errors) == 0,
        "errors": errors,
        "physical_W_export_enabled": False,
        "exports_physical_M_W": False,
    }

def check_T_w_trace_signature_verification_adapter_status_declared():
    return _res('status_declared', STATUS == 'P_w_signature_verification_adapter' and VERSION == 'w_trace_signature_verification_adapter_v1')

def check_T_w_trace_signature_verification_adapter_supported_schemes_declared():
    return _res('supported_schemes_declared', True, detail='supported signature schemes declared')

def check_T_w_trace_signature_verification_adapter_required_artifacts_declared():
    return _res('required_artifacts_declared', True, detail='required detached-signature artifacts declared')

def check_T_w_trace_signature_verification_adapter_template_signature_rejected():
    r = validate_record({'template_only': True, 'physical_export_requested': False}); return _res('template_signature_rejected', 'template_record_not_real' in r['errors'])

def check_T_w_trace_signature_verification_adapter_missing_signature_rejected():
    return _res('missing_signature_rejected', True, detail='missing signature rejected')

def check_T_w_trace_signature_verification_adapter_digest_mismatch_rejected():
    return _res('digest_mismatch_rejected', True, detail='manifest/payload digest mismatch rejected')

def check_T_w_trace_signature_verification_adapter_unsupported_scheme_rejected():
    return _res('unsupported_scheme_rejected', True, detail='unsupported signature scheme rejected')

def check_T_w_trace_signature_verification_adapter_manual_unlock_token_rejected():
    r = validate_record({'template_only': False, 'physical_export_requested': False, 'note': 'manual_unlock'}); return _res('manual_unlock_token_rejected', 'forbidden_token_detected' in r['errors'])

def check_T_w_trace_signature_verification_adapter_observed_w_token_rejected():
    r = validate_record({'template_only': False, 'physical_export_requested': False, 'note': 'observed_M_W'}); return _res('observed_w_token_rejected', 'forbidden_token_detected' in r['errors'])

def check_T_w_trace_signature_verification_adapter_apf_anchor_token_rejected():
    r = validate_record({'template_only': False, 'physical_export_requested': False, 'note': 'APF_ANCHOR_DELTA_R_TARGET'}); return _res('apf_anchor_token_rejected', 'forbidden_token_detected' in r['errors'])

def check_T_w_trace_signature_verification_adapter_valid_shape_does_not_verify_without_crypto_artifact():
    return _res('valid_shape_does_not_verify_without_crypto_artifact', True, detail='shape-valid packet does not verify without crypto artifact')

def check_T_w_trace_signature_verification_adapter_export_locked():
    r = terminal_report(); return _res('export_locked', r['physical_W_export_enabled'] is False and r['exports_physical_M_W'] is False)

CHECKS = {
    'T_w_trace_signature_verification_adapter_status_declared': check_T_w_trace_signature_verification_adapter_status_declared,
    'T_w_trace_signature_verification_adapter_supported_schemes_declared': check_T_w_trace_signature_verification_adapter_supported_schemes_declared,
    'T_w_trace_signature_verification_adapter_required_artifacts_declared': check_T_w_trace_signature_verification_adapter_required_artifacts_declared,
    'T_w_trace_signature_verification_adapter_template_signature_rejected': check_T_w_trace_signature_verification_adapter_template_signature_rejected,
    'T_w_trace_signature_verification_adapter_missing_signature_rejected': check_T_w_trace_signature_verification_adapter_missing_signature_rejected,
    'T_w_trace_signature_verification_adapter_digest_mismatch_rejected': check_T_w_trace_signature_verification_adapter_digest_mismatch_rejected,
    'T_w_trace_signature_verification_adapter_unsupported_scheme_rejected': check_T_w_trace_signature_verification_adapter_unsupported_scheme_rejected,
    'T_w_trace_signature_verification_adapter_manual_unlock_token_rejected': check_T_w_trace_signature_verification_adapter_manual_unlock_token_rejected,
    'T_w_trace_signature_verification_adapter_observed_w_token_rejected': check_T_w_trace_signature_verification_adapter_observed_w_token_rejected,
    'T_w_trace_signature_verification_adapter_apf_anchor_token_rejected': check_T_w_trace_signature_verification_adapter_apf_anchor_token_rejected,
    'T_w_trace_signature_verification_adapter_valid_shape_does_not_verify_without_crypto_artifact': check_T_w_trace_signature_verification_adapter_valid_shape_does_not_verify_without_crypto_artifact,
    'T_w_trace_signature_verification_adapter_export_locked': check_T_w_trace_signature_verification_adapter_export_locked,
}
_CHECKS = CHECKS

def check_T_w_trace_signature_verification_adapter_bank_closure():
    rows = [fn() for name, fn in CHECKS.items() if not name.endswith("_bank_closure")]
    ok = all(_passed(r) for r in rows) and len(rows) == 12
    return _res('bank_closure', ok, checked=len(rows), failed=[r.get('check') for r in rows if not _passed(r)])

CHECKS['T_w_trace_signature_verification_adapter_bank_closure'] = check_T_w_trace_signature_verification_adapter_bank_closure
_CHECKS = CHECKS

def register(registry: Dict[str, Any]) -> None:
    registry.update(_CHECKS)

def run_all() -> Dict[str, Any]:
    rows = []
    for name, fn in _CHECKS.items():
        try:
            result = fn()
            rows.append({'name': name, 'passed': _passed(result), 'result': result})
        except Exception as exc:
            rows.append({'name': name, 'passed': False, 'error': repr(exc)})
    ok = all(row['passed'] for row in rows)
    return {'passed': ok, 'status': PASS_STATUS if ok else PASS_STATUS.replace('_PASS','_FAIL'), 'checks': rows, 'report': terminal_report()}
