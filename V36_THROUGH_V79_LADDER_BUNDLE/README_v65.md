# APF v65 — External Ledger and Evaluator Registry

This package closes the registry for the external-ledger/evaluator phase.

It does **not** claim global physical-final closure. It records which external ledgers and evaluator objects are required to make downstream scheme-relative comparisons.

Run:

```bash
python scripts/check_external_ledger_evaluator_registry_v65.py
```

Expected stamp:

```text
EXTERNAL_LEDGER_AND_EVALUATOR_REGISTRY_PASS
```
