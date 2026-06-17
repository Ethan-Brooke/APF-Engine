# Vendored dark-posterior evidence probes

These are the small `results/CLOSURE_STATEMENT.json` files for the 9 dark-sector
Route-C evidence packs that `apf/interface_dark_posterior_evidence_intake.py` and
`apf/dark_empirical_posterior_admission_contract.py` read to verify the dark
empirical-posterior admission contract (7 bank-registered checks).

**Why they live here.** The full evidence bundle
`DOCTRINE_CONSEQUENCES_BUNDLE_LATEST_44/` is git-ignored and lives on Drive; it did
not travel with the 2026-06-08 move of the codebase off Drive into this git repo.
The 7 contract checks therefore failed on every clean off-Drive checkout (0/9
probes loaded). Only these small JSONs (≈61 KB total) are load-bearing for the
checks, so they are vendored here. The loader prefers the full Drive bundle when
present and falls back to this vendored copy otherwise, so `verify_all` is clean on
any checkout.

**Provenance.** Copied verbatim from
`DOCTRINE_CONSEQUENCES_BUNDLE_LATEST_44/<pack>/results/CLOSURE_STATEMENT.json`
(2026-06-17). If a pack's closure statement is regenerated in the full bundle,
refresh the corresponding file here.
