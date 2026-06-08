"""W_TRACE release-packet signed attestation / immutable manifest digest bank.

This module does not sign, release, or export a physical W value.  It banks the
attestation and immutable-manifest-digest contract that a future completed
release packet must satisfy before the W_TRACE export lock can even consider
opening.  Shipped state remains template-only and locked.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List

try:
    from apf.w_trace_release_packet_validator import (
        validate_release_packet,
        completed_shape_release_packet,
        W_RELEASE_PACKET_VALIDATOR_STATUS,
        RELEASE_PACKET_VALIDATOR_VERSION,
    )
except Exception:  # pragma: no cover
    validate_release_packet = None
    completed_shape_release_packet = None
    W_RELEASE_PACKET_VALIDATOR_STATUS = "P_w_release_packet_validator"
    RELEASE_PACKET_VALIDATOR_VERSION = "w_trace_release_packet_validator_v1"

W_RELEASE_ATTESTATION_STATUS = "P_w_release_attestation_manifest_digest"
RELEASE_ATTESTATION_VERSION = "w_trace_release_attestation_v1"
RELEASE_ATTESTATION_MODE = "signed_attestation_contract_only_no_real_signature_shipped"
ROOT = Path(__file__).resolve().parents[1]
EXAMPLE_DIR = ROOT / "examples" / "w_trace_release_attestation"
DOC_PATH = ROOT / "W_TRACE_RELEASE_ATTESTATION_BANK_v1_0.md"
TEMPLATE_PATH = EXAMPLE_DIR / "release_attestation_template.json"

HASH_ALGORITHM = "sha256"
SIGNATURE_SCHEMES = ("minisign", "sigstore_bundle", "gpg_detached", "x509_cose")
ATTESTATION_REQUIRED_FIELDS = (
    "attestation_version",
    "release_packet_digest",
    "release_packet_digest_algorithm",
    "immutable_manifest_digest",
    "immutable_manifest_digest_algorithm",
    "signer_identity",
    "signature_scheme",
    "signature_payload_digest",
    "signature_value_or_bundle_ref",
    "signed_at_utc",
    "release_packet_validator_version",
    "operator_runbook_version",
    "export_lock_acknowledged",
    "physical_export_requested",
    "template_only",
)
IMMUTABLE_MANIFEST_FIELDS = (
    "release_packet_digest",
    "review_packet_digest",
    "source_candidate_digest",
    "payload_digest",
    "session_log_digest",
    "session_replay_digest",
    "row_bundle_digest",
    "component_sum_certificate_digest",
    "covariance_certificate_digest",
    "uncertainty_certificate_digest",
    "counterterm_convention_digest",
    "final_export_readiness_digest",
)
FORBIDDEN_ATTESTATION_TOKENS = (
    "observed_M_W",
    "world_average_W_mass",
    "fit_residual",
    "apf_anchor_delta_r",
    "APF_ANCHOR_DELTA_R_TARGET",
    "manual_unlock",
    "force_export",
    "physical_M_W_override",
)
SHIPPED_STATE = {
    "real_signed_release_attestation_shipped": False,
    "real_signed_release_attestation_validated": False,
    "immutable_manifest_digest_bound": False,
    "signature_verified": False,
    "real_payload_rows_admitted": False,
    "real_component_sum_certified": False,
    "real_covariance_certified": False,
    "real_uncertainty_certified": False,
    "physical_W_export_enabled": False,
    "exports_physical_M_W": False,
}


def _canonical_json(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha256_hex(obj: Any) -> str:
    return hashlib.sha256(_canonical_json(obj).encode("utf-8")).hexdigest()


def _looks_sha256(value: Any) -> bool:
    return isinstance(value, str) and len(value) == 64 and all(c in "0123456789abcdef" for c in value.lower())


def _contains_forbidden_token(obj: Any) -> bool:
    text = _canonical_json(obj)
    return any(token in text for token in FORBIDDEN_ATTESTATION_TOKENS)


def immutable_manifest_template() -> Dict[str, Any]:
    return {
        field: ("0" * 64 if field.endswith("digest") else "")
        for field in IMMUTABLE_MANIFEST_FIELDS
    }


def release_attestation_template() -> Dict[str, Any]:
    manifest = immutable_manifest_template()
    return {
        "attestation_version": RELEASE_ATTESTATION_VERSION,
        "release_packet_digest": "0" * 64,
        "release_packet_digest_algorithm": HASH_ALGORITHM,
        "immutable_manifest_digest": sha256_hex(manifest),
        "immutable_manifest_digest_algorithm": HASH_ALGORITHM,
        "immutable_manifest": manifest,
        "signer_identity": "TEMPLATE_SIGNER_NOT_REAL",
        "signature_scheme": "minisign",
        "signature_payload_digest": "0" * 64,
        "signature_value_or_bundle_ref": "TEMPLATE_SIGNATURE_NOT_REAL",
        "signed_at_utc": "TEMPLATE_TIMESTAMP_NOT_REAL",
        "release_packet_validator_version": RELEASE_PACKET_VALIDATOR_VERSION,
        "operator_runbook_version": "w_trace_release_runbook_v1",
        "export_lock_acknowledged": True,
        "physical_export_requested": False,
        "template_only": True,
    }


def completed_shape_attestation() -> Dict[str, Any]:
    att = release_attestation_template()
    att.update({
        "signer_identity": "reviewer@example.invalid",
        "signature_value_or_bundle_ref": "artifact://detached-signature.sha256",
        "signed_at_utc": "2026-05-09T00:00:00Z",
        "signature_payload_digest": sha256_hex({"payload": "release-attestation-shape"}),
        "template_only": False,
    })
    return att


def validate_release_attestation(attestation: Dict[str, Any] | None = None) -> Dict[str, Any]:
    attestation = dict(attestation or release_attestation_template())
    errors: List[str] = []

    for field in ATTESTATION_REQUIRED_FIELDS:
        if field not in attestation:
            errors.append(f"missing:{field}")
    if attestation.get("attestation_version") != RELEASE_ATTESTATION_VERSION:
        errors.append("bad_attestation_version")
    if attestation.get("release_packet_digest_algorithm") != HASH_ALGORITHM:
        errors.append("bad_release_packet_digest_algorithm")
    if attestation.get("immutable_manifest_digest_algorithm") != HASH_ALGORITHM:
        errors.append("bad_manifest_digest_algorithm")
    if not _looks_sha256(attestation.get("release_packet_digest")):
        errors.append("bad_release_packet_digest")
    if not _looks_sha256(attestation.get("immutable_manifest_digest")):
        errors.append("bad_immutable_manifest_digest")
    if not _looks_sha256(attestation.get("signature_payload_digest")):
        errors.append("bad_signature_payload_digest")
    if attestation.get("signature_scheme") not in SIGNATURE_SCHEMES:
        errors.append("unsupported_signature_scheme")
    if attestation.get("template_only") is True:
        errors.append("template_packet_not_real")
    if attestation.get("physical_export_requested") is True:
        errors.append("physical_export_request_forbidden_here")
    if attestation.get("export_lock_acknowledged") is not True:
        errors.append("export_lock_not_acknowledged")
    if attestation.get("release_packet_validator_version") != RELEASE_PACKET_VALIDATOR_VERSION:
        errors.append("release_packet_validator_version_mismatch")
    if "TEMPLATE" in str(attestation.get("signer_identity", "")):
        errors.append("template_signer_not_allowed")
    if "TEMPLATE" in str(attestation.get("signature_value_or_bundle_ref", "")):
        errors.append("template_signature_not_allowed")
    if "TEMPLATE" in str(attestation.get("signed_at_utc", "")):
        errors.append("template_timestamp_not_allowed")
    manifest = attestation.get("immutable_manifest")
    if not isinstance(manifest, dict):
        errors.append("missing_immutable_manifest")
    else:
        missing = [field for field in IMMUTABLE_MANIFEST_FIELDS if field not in manifest]
        if missing:
            errors.append("manifest_missing_fields:" + ",".join(missing))
        bad = [field for field in IMMUTABLE_MANIFEST_FIELDS if field in manifest and not _looks_sha256(manifest[field])]
        if bad:
            errors.append("manifest_bad_digests:" + ",".join(bad))
        computed = sha256_hex(manifest)
        if attestation.get("immutable_manifest_digest") != computed:
            errors.append("immutable_manifest_digest_mismatch")
    if _contains_forbidden_token(attestation):
        errors.append("forbidden_token_detected")

    signature_verified = False  # contract-only: no real signature artifact is shipped
    immutable_bound = len(errors) == 0 and _looks_sha256(attestation.get("immutable_manifest_digest"))
    return {
        "release_attestation_status": W_RELEASE_ATTESTATION_STATUS,
        "release_attestation_version": RELEASE_ATTESTATION_VERSION,
        "release_attestation_mode": RELEASE_ATTESTATION_MODE,
        "valid_shape": len(errors) == 0,
        "errors": errors,
        "signature_verified": signature_verified,
        "immutable_manifest_digest_bound": immutable_bound,
        "physical_W_export_enabled": False,
        "exports_physical_M_W": False,
        "shipped_state": dict(SHIPPED_STATE),
    }


def write_template() -> Path:
    EXAMPLE_DIR.mkdir(parents=True, exist_ok=True)
    TEMPLATE_PATH.write_text(json.dumps(release_attestation_template(), indent=2, sort_keys=True) + "\n")
    return TEMPLATE_PATH


def _passed(r: Any) -> bool:
    return bool(r.get("passed", r.get("ok", False))) if isinstance(r, dict) else bool(r)


def _res(check: str, ok: bool, **extra: Any) -> Dict[str, Any]:
    return {"check": check, "passed": bool(ok), **extra}


def check_T_w_release_attestation_status_declared():
    return _res("status_declared", W_RELEASE_ATTESTATION_STATUS == "P_w_release_attestation_manifest_digest")


def check_T_w_release_attestation_depends_on_release_packet_validator():
    return _res("depends_on_validator", W_RELEASE_PACKET_VALIDATOR_STATUS == "P_w_release_packet_validator")


def check_T_w_release_attestation_required_fields_declared():
    return _res("required_fields_declared", len(ATTESTATION_REQUIRED_FIELDS) == 15)


def check_T_w_release_attestation_required_fields_unique():
    return _res("required_fields_unique", len(set(ATTESTATION_REQUIRED_FIELDS)) == len(ATTESTATION_REQUIRED_FIELDS))


def check_T_w_release_attestation_manifest_fields_declared():
    return _res("manifest_fields_declared", len(IMMUTABLE_MANIFEST_FIELDS) == 12)


def check_T_w_release_attestation_manifest_fields_unique():
    return _res("manifest_fields_unique", len(set(IMMUTABLE_MANIFEST_FIELDS)) == len(IMMUTABLE_MANIFEST_FIELDS))


def check_T_w_release_attestation_signature_schemes_declared():
    return _res("signature_schemes_declared", {"minisign", "sigstore_bundle", "gpg_detached"}.issubset(SIGNATURE_SCHEMES))


def check_T_w_release_attestation_template_rejected():
    r = validate_release_attestation(release_attestation_template())
    return _res("template_rejected", not r["valid_shape"] and "template_packet_not_real" in r["errors"])


def check_T_w_release_attestation_completed_shape_valid_but_export_locked():
    r = validate_release_attestation(completed_shape_attestation())
    return _res("completed_shape_valid_but_locked", r["valid_shape"] and r["physical_W_export_enabled"] is False)


def check_T_w_release_attestation_hash_algorithm_locked_sha256():
    return _res("hash_algorithm_locked_sha256", HASH_ALGORITHM == "sha256")


def check_T_w_release_attestation_bad_hash_rejected():
    att = completed_shape_attestation(); att["release_packet_digest"] = "bad"
    r = validate_release_attestation(att)
    return _res("bad_hash_rejected", "bad_release_packet_digest" in r["errors"])


def check_T_w_release_attestation_bad_signature_scheme_rejected():
    att = completed_shape_attestation(); att["signature_scheme"] = "homebrew"
    r = validate_release_attestation(att)
    return _res("bad_signature_scheme_rejected", "unsupported_signature_scheme" in r["errors"])


def check_T_w_release_attestation_manifest_digest_recomputed():
    att = completed_shape_attestation(); manifest = att["immutable_manifest"]
    return _res("manifest_digest_recomputed", att["immutable_manifest_digest"] == sha256_hex(manifest))


def check_T_w_release_attestation_manifest_mismatch_rejected():
    att = completed_shape_attestation(); att["immutable_manifest"]["payload_digest"] = "1" * 64
    r = validate_release_attestation(att)
    return _res("manifest_mismatch_rejected", "immutable_manifest_digest_mismatch" in r["errors"])


def check_T_w_release_attestation_missing_manifest_field_rejected():
    att = completed_shape_attestation(); att["immutable_manifest"].pop("payload_digest")
    r = validate_release_attestation(att)
    return _res("missing_manifest_field_rejected", any(e.startswith("manifest_missing_fields") for e in r["errors"]))


def check_T_w_release_attestation_bad_manifest_digest_rejected():
    att = completed_shape_attestation(); att["immutable_manifest"]["payload_digest"] = "x"
    r = validate_release_attestation(att)
    return _res("bad_manifest_digest_rejected", any(e.startswith("manifest_bad_digests") for e in r["errors"]))


def check_T_w_release_attestation_release_packet_digest_required():
    att = completed_shape_attestation(); att.pop("release_packet_digest")
    r = validate_release_attestation(att)
    return _res("release_packet_digest_required", "missing:release_packet_digest" in r["errors"])


def check_T_w_release_attestation_export_request_rejected():
    att = completed_shape_attestation(); att["physical_export_requested"] = True
    r = validate_release_attestation(att)
    return _res("export_request_rejected", "physical_export_request_forbidden_here" in r["errors"])


def check_T_w_release_attestation_export_lock_ack_required():
    att = completed_shape_attestation(); att["export_lock_acknowledged"] = False
    r = validate_release_attestation(att)
    return _res("export_lock_ack_required", "export_lock_not_acknowledged" in r["errors"])


def check_T_w_release_attestation_template_signer_rejected():
    att = completed_shape_attestation(); att["signer_identity"] = "TEMPLATE_SIGNER_NOT_REAL"
    r = validate_release_attestation(att)
    return _res("template_signer_rejected", "template_signer_not_allowed" in r["errors"])


def check_T_w_release_attestation_template_signature_rejected():
    att = completed_shape_attestation(); att["signature_value_or_bundle_ref"] = "TEMPLATE_SIGNATURE_NOT_REAL"
    r = validate_release_attestation(att)
    return _res("template_signature_rejected", "template_signature_not_allowed" in r["errors"])


def check_T_w_release_attestation_forbidden_observed_w_token_rejected():
    att = completed_shape_attestation(); att["notes"] = "observed_M_W must not enter"
    r = validate_release_attestation(att)
    return _res("forbidden_observed_w_token_rejected", "forbidden_token_detected" in r["errors"])


def check_T_w_release_attestation_forbidden_manual_unlock_rejected():
    att = completed_shape_attestation(); att["notes"] = "manual_unlock"
    r = validate_release_attestation(att)
    return _res("forbidden_manual_unlock_rejected", "forbidden_token_detected" in r["errors"])


def check_T_w_release_attestation_signature_not_verified_without_artifact():
    r = validate_release_attestation(completed_shape_attestation())
    return _res("signature_not_verified_without_artifact", r["signature_verified"] is False)


def check_T_w_release_attestation_no_physical_export_flags():
    r = validate_release_attestation(completed_shape_attestation())
    return _res("no_physical_export_flags", r["exports_physical_M_W"] is False and r["physical_W_export_enabled"] is False)


def check_T_w_release_attestation_real_state_false():
    return _res("real_state_false", not any(SHIPPED_STATE.values()))


def check_T_w_release_attestation_json_serializable():
    json.dumps(validate_release_attestation())
    return _res("json_serializable", True)


def check_T_w_release_attestation_template_path_declared():
    return _res("template_path_declared", str(TEMPLATE_PATH).endswith("release_attestation_template.json"))


def check_T_w_release_attestation_write_template():
    p = write_template()
    return _res("write_template", p.exists() and p.read_text().strip().startswith("{"))


def check_T_w_release_attestation_template_not_real():
    p = write_template(); data = json.loads(p.read_text())
    return _res("template_not_real", data.get("template_only") is True and "TEMPLATE" in data.get("signer_identity", ""))


def check_T_w_release_attestation_doc_exists():
    return _res("doc_exists", DOC_PATH.exists())


def check_T_w_release_attestation_doc_warns_locked():
    text = DOC_PATH.read_text() if DOC_PATH.exists() else ""
    return _res("doc_warns_locked", "physical W export remains locked" in text)


def check_T_w_release_attestation_immutable_manifest_binds_all_terminal_artifacts():
    terminal = {"release_packet_digest", "component_sum_certificate_digest", "covariance_certificate_digest", "uncertainty_certificate_digest", "final_export_readiness_digest"}
    return _res("manifest_binds_terminal_artifacts", terminal.issubset(set(IMMUTABLE_MANIFEST_FIELDS)))


def check_T_w_release_attestation_validator_version_pinned():
    att = completed_shape_attestation()
    return _res("validator_version_pinned", att["release_packet_validator_version"] == RELEASE_PACKET_VALIDATOR_VERSION)


def check_T_w_release_attestation_bad_validator_version_rejected():
    att = completed_shape_attestation(); att["release_packet_validator_version"] = "wrong"
    r = validate_release_attestation(att)
    return _res("bad_validator_version_rejected", "release_packet_validator_version_mismatch" in r["errors"])


def check_T_w_release_attestation_release_packet_validator_still_locked():
    if validate_release_packet is None or completed_shape_release_packet is None:
        return _res("release_packet_validator_still_locked", False, reason="dependency unavailable")
    r = validate_release_packet(completed_shape_release_packet())
    return _res("release_packet_validator_still_locked", r.get("physical_W_export_enabled") is False)


def check_T_w_release_attestation_terminal_state_blocked_default():
    r = validate_release_attestation()
    ok = r["valid_shape"] is False and r["physical_W_export_enabled"] is False
    return _res("terminal_state_blocked_default", ok, errors=r["errors"])


def check_T_w_release_attestation_bank_closure():
    rows = [fn() for fn in CHECKS.values() if fn is not check_T_w_release_attestation_bank_closure]
    ok = all(_passed(r) for r in rows) and len(rows) == 37
    return _res("bank_closure", ok, checked=len(rows), failed=[r.get("check") for r in rows if not _passed(r)])


CHECKS = {
    "T_w_release_attestation_status_declared": check_T_w_release_attestation_status_declared,
    "T_w_release_attestation_depends_on_release_packet_validator": check_T_w_release_attestation_depends_on_release_packet_validator,
    "T_w_release_attestation_required_fields_declared": check_T_w_release_attestation_required_fields_declared,
    "T_w_release_attestation_required_fields_unique": check_T_w_release_attestation_required_fields_unique,
    "T_w_release_attestation_manifest_fields_declared": check_T_w_release_attestation_manifest_fields_declared,
    "T_w_release_attestation_manifest_fields_unique": check_T_w_release_attestation_manifest_fields_unique,
    "T_w_release_attestation_signature_schemes_declared": check_T_w_release_attestation_signature_schemes_declared,
    "T_w_release_attestation_template_rejected": check_T_w_release_attestation_template_rejected,
    "T_w_release_attestation_completed_shape_valid_but_export_locked": check_T_w_release_attestation_completed_shape_valid_but_export_locked,
    "T_w_release_attestation_hash_algorithm_locked_sha256": check_T_w_release_attestation_hash_algorithm_locked_sha256,
    "T_w_release_attestation_bad_hash_rejected": check_T_w_release_attestation_bad_hash_rejected,
    "T_w_release_attestation_bad_signature_scheme_rejected": check_T_w_release_attestation_bad_signature_scheme_rejected,
    "T_w_release_attestation_manifest_digest_recomputed": check_T_w_release_attestation_manifest_digest_recomputed,
    "T_w_release_attestation_manifest_mismatch_rejected": check_T_w_release_attestation_manifest_mismatch_rejected,
    "T_w_release_attestation_missing_manifest_field_rejected": check_T_w_release_attestation_missing_manifest_field_rejected,
    "T_w_release_attestation_bad_manifest_digest_rejected": check_T_w_release_attestation_bad_manifest_digest_rejected,
    "T_w_release_attestation_release_packet_digest_required": check_T_w_release_attestation_release_packet_digest_required,
    "T_w_release_attestation_export_request_rejected": check_T_w_release_attestation_export_request_rejected,
    "T_w_release_attestation_export_lock_ack_required": check_T_w_release_attestation_export_lock_ack_required,
    "T_w_release_attestation_template_signer_rejected": check_T_w_release_attestation_template_signer_rejected,
    "T_w_release_attestation_template_signature_rejected": check_T_w_release_attestation_template_signature_rejected,
    "T_w_release_attestation_forbidden_observed_w_token_rejected": check_T_w_release_attestation_forbidden_observed_w_token_rejected,
    "T_w_release_attestation_forbidden_manual_unlock_rejected": check_T_w_release_attestation_forbidden_manual_unlock_rejected,
    "T_w_release_attestation_signature_not_verified_without_artifact": check_T_w_release_attestation_signature_not_verified_without_artifact,
    "T_w_release_attestation_no_physical_export_flags": check_T_w_release_attestation_no_physical_export_flags,
    "T_w_release_attestation_real_state_false": check_T_w_release_attestation_real_state_false,
    "T_w_release_attestation_json_serializable": check_T_w_release_attestation_json_serializable,
    "T_w_release_attestation_template_path_declared": check_T_w_release_attestation_template_path_declared,
    "T_w_release_attestation_write_template": check_T_w_release_attestation_write_template,
    "T_w_release_attestation_template_not_real": check_T_w_release_attestation_template_not_real,
    "T_w_release_attestation_doc_exists": check_T_w_release_attestation_doc_exists,
    "T_w_release_attestation_doc_warns_locked": check_T_w_release_attestation_doc_warns_locked,
    "T_w_release_attestation_immutable_manifest_binds_all_terminal_artifacts": check_T_w_release_attestation_immutable_manifest_binds_all_terminal_artifacts,
    "T_w_release_attestation_validator_version_pinned": check_T_w_release_attestation_validator_version_pinned,
    "T_w_release_attestation_bad_validator_version_rejected": check_T_w_release_attestation_bad_validator_version_rejected,
    "T_w_release_attestation_release_packet_validator_still_locked": check_T_w_release_attestation_release_packet_validator_still_locked,
    "T_w_release_attestation_terminal_state_blocked_default": check_T_w_release_attestation_terminal_state_blocked_default,
    "T_w_release_attestation_bank_closure": check_T_w_release_attestation_bank_closure,
}
_CHECKS = CHECKS


def register(registry: Dict[str, Any]) -> None:
    registry.update(_CHECKS)


def run_all() -> Dict[str, Any]:
    rows = []
    for name, fn in _CHECKS.items():
        try:
            result = fn()
            rows.append({"name": name, "passed": _passed(result), "result": result})
        except Exception as exc:
            rows.append({"name": name, "passed": False, "error": repr(exc)})
    ok = all(row["passed"] for row in rows)
    return {
        "passed": ok,
        "status": "W_TRACE_RELEASE_ATTESTATION_BANK_PASS" if ok else "W_TRACE_RELEASE_ATTESTATION_BANK_FAIL",
        "checks": rows,
        "report": validate_release_attestation(),
    }
