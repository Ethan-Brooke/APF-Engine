"""Repository-integrity tests for the unbanked zipper audit packet."""
from __future__ import annotations

import importlib
from pathlib import Path

from apf import _module_manifest as manifest


EXPECTED_CANDIDATES = (
    "apf.zipper_clearance_occupancy",
    "apf.zipper_reduction",
    "apf.zipper_reflection_bridge",
    "apf.zipper_bridge_bank_concordance",
    "apf.zipper_reduction_frontier",
)

EXPECTED_TEST_FILES = (
    "tests/test_zipper_clearance_occupancy.py",
    "tests/test_zipper_reduction.py",
    "tests/test_zipper_reflection_bridge.py",
    "tests/test_zipper_bridge_bank_concordance.py",
    "tests/test_zipper_reduction_frontier.py",
    "tests/test_zipper_audit_manifest.py",
)


def test_candidate_manifest_is_exact_and_explicitly_unbanked():
    assert manifest.AUDIT_CANDIDATE_MODULES == EXPECTED_CANDIDATES
    for name in EXPECTED_CANDIDATES:
        assert name not in manifest.BANK_REGISTRY_MODULES
        assert name not in manifest.ARCHITECTURE_ONLY_MODULES
        assert name not in manifest.KNOWN_REGISTER_ANOMALIES
        assert name not in manifest.BANK_LOAD_MODULES
        assert name not in manifest.ALL_MODULES_VERIFY_ORDER
        assert name not in manifest.MODULE_TYPES


def test_every_manifested_candidate_imports_and_exposes_a_conditional_certificate():
    for name in EXPECTED_CANDIDATES:
        module = importlib.import_module(name)
        assert callable(getattr(module, "run_all", None)), name
        assert callable(getattr(module, "build_certificate", None)), name
        rows = module.run_all()
        assert rows, name
        assert all(row["passed"] for row in rows.values()), name
        assert all(row["physical_premises_certified"] is False for row in rows.values()), name
        certificate = module.build_certificate(rows)
        assert certificate.physical_premises_certified is False, name


def test_all_declared_focused_test_files_exist_in_the_pr_checkout():
    root = Path(__file__).resolve().parents[1]
    missing = [path for path in EXPECTED_TEST_FILES if not (root / path).is_file()]
    assert not missing, missing
