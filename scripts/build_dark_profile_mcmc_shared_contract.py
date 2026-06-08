#!/usr/bin/env python3
"""Build APF_DARK_PROFILE_MCMC_SHARED_RUNTIME_CONTRACT_v1."""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from apf.dark_profile_mcmc_shared_contract import MARKER, export_contract_pack
if __name__ == "__main__":
    out = export_contract_pack(root=ROOT)
    print(f"{MARKER}: {out}")
