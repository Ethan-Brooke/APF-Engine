"""Run one exact reviewed private request, with a durable uncertainty journal.

Authorization hash must be supplied through the independently trusted Executive
release, never calculated from untrusted candidate data by this runner.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--gate-root", required=True)
    p.add_argument("--authorization-file", required=True)
    p.add_argument("--authorization-sha256", required=True)
    p.add_argument("--publisher-id", required=True)
    p.add_argument("--method", required=True)
    p.add_argument("--path", required=True)
    p.add_argument("--payload", required=True)
    p.add_argument("--content-type", required=True)
    p.add_argument("--lane", choices=("scientific", "administrative"), default="scientific")
    p.add_argument("--action")
    p.add_argument("--credentials", required=True)
    p.add_argument("--journal-dir", required=True)
    args = p.parse_args()
    sys.path.insert(0, str(Path(args.gate_root).resolve()))
    from apf.evidence_gate import GateRejected, digest, validate_request
    from p2m_guarded_client import P2MClient, AdministrativeP2MClient
    validator = validate_request
    client_type = P2MClient
    if args.lane == "administrative":
        from apf.administrative_publisher import validate_administrative_request
        validator = validate_administrative_request
        client_type = AdministrativeP2MClient

    authority = {"path": str(Path(args.authorization_file).resolve()),
                 "sha256": args.authorization_sha256}
    payload = Path(args.payload).read_bytes()
    request = dict(action=args.action or ("administrative_update" if args.lane == "administrative" else "private_stage"), method=args.method, path=args.path,
                   payload=payload, content_type=args.content_type)
    # Preflight before reading credentials or refreshing. This is not a cached
    # permit: the installed wrapper validates again immediately before the write.
    validator(authority, publisher_id=args.publisher_id, **request)
    journal = Path(args.journal_dir).resolve()
    journal.mkdir(parents=True, exist_ok=True)
    state_path = journal / "REQUEST_STATE.json"
    if state_path.exists():
        raise RuntimeError("Prior attempt exists: perform read-only reconciliation before any new attempt")
    state = {"status": "prepared", "method": args.method, "path": args.path,
             "content_type": args.content_type, "body_sha256": digest(payload),
             "authorization": authority}
    def save():
        state["updated_at"] = datetime.now(timezone.utc).isoformat()
        state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    def before_mutation(*_):
        state["status"] = "network_started"
        save()
    save()
    (journal / "REQUEST_BODY.bin").write_bytes(payload)
    client = client_type(authority, args.publisher_id, before_mutation=before_mutation)
    try:
        client.connect(args.credentials)
        sender = client.send_administrative if args.lane == "administrative" else client.send_reviewed
        result = sender(**request)
    except GateRejected:
        state["status"] = "denied_before_mutation"
        save()
        raise
    except Exception:
        state["status"] = "uncertain" if state["status"] == "network_started" else "failed_before_mutation"
        save()
        raise
    (journal / "RESPONSE.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    state["status"] = "response_received_readback_required"
    save()
    print("Response saved; exact remote readback is still required.")


if __name__ == "__main__":
    main()
