# APF Zipper Packet — Repository-Integrity Correction v0.1

**Status:** unbanked audit correction; no theorem-bank, registry-size, census-pin, version, or export change  
**Branch:** `audit/zipper-reduction-v0.1`

## 1. Correction

Two earlier verification statements were too strong.

First, the zipper `apf/*.py` files were initially absent from `apf._module_manifest`. Second, a truncated fetched PR diff was not sufficient evidence that the focused adversarial test files existed in the branch.

Both issues are now addressed explicitly.

## 2. What `verify_all.py --bank-audit` actually checks

`--bank-audit` iterates only `apf.bank._MODULE_PATHS`, which is derived from the production bank-load manifest. It does **not** scan the repository for every `apf/*.py` file. It also exits with status zero after reporting its four bank-load buckets.

Therefore an unmanifested audit-candidate module is invisible to that command. A successful `--bank-audit` run establishes only that the manifest-defined production bank surface still loads as before. It does not establish repository-wide module completeness and does not prove that candidate files or tests are present.

The prior phrase “unchanged-bank verification” is retained only in this narrower sense.

## 3. Explicit audit-candidate manifest

`apf._module_manifest` now defines the exact tuple

```python
AUDIT_CANDIDATE_MODULES = (
    "apf.zipper_clearance_occupancy",
    "apf.zipper_reduction",
    "apf.zipper_reflection_bridge",
    "apf.zipper_bridge_bank_concordance",
    "apf.zipper_reduction_frontier",
)
```

The tuple is deliberately excluded from:

- `BANK_REGISTRY_MODULES`;
- `ARCHITECTURE_ONLY_MODULES`;
- `KNOWN_REGISTER_ANOMALIES`;
- `BANK_LOAD_MODULES`;
- `ALL_MODULES_VERIFY_ORDER`;
- `MODULE_TYPES`;
- the production theorem registry.

This makes the files census-visible without silently banking them or changing the standard scorecard.

## 4. Focused test presence and execution

`tests/test_zipper_audit_manifest.py` verifies all of the following in the checked-out PR tree:

1. the audit-candidate tuple is set-exact;
2. no candidate appears on a production bank/load/type surface;
3. every candidate imports;
4. every candidate exposes `run_all()` and `build_certificate()`;
5. every candidate check passes while `physical_premises_certified` remains false;
6. every declared focused test file exists.

The focused test files are:

```text
tests/test_zipper_audit_manifest.py
tests/test_zipper_clearance_occupancy.py
tests/test_zipper_reduction.py
tests/test_zipper_reflection_bridge.py
tests/test_zipper_bridge_bank_concordance.py
tests/test_zipper_reduction_frontier.py
```

The dedicated workflow runs the manifest-integrity test separately and then runs the full six-file focused suite.

## 5. Correct verification language

The licensed verification statements are now:

- the production bank surface is unchanged **relative to the production manifest**;
- the audit-candidate modules are explicitly named on a separate unbanked manifest surface;
- focused test presence is asserted from the checked-out tree;
- focused test execution is established only by the dedicated workflow step and its recorded result.

The packet may not cite a truncated diff, a successful `--bank-audit` run, or a module import performed outside the checked-out PR tree as proof of focused test presence.
