"""Portable test launcher; no credentials are accepted or read."""
import argparse
import sys
import unittest
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument("--gate-root", required=True)
p.add_argument("--fixture-root", required=True)
p.add_argument("--admin-gate-root", required=True)
a = p.parse_args()
sys.path.insert(0, str(Path(a.gate_root).resolve()))
sys.path.insert(0, str(Path(a.fixture_root).resolve()))
sys.path.insert(0, str(Path(__file__).parent.resolve()))
import apf
apf.__path__.append(str(Path(a.admin_gate_root).resolve() / "apf"))
sys.path.insert(0, str(Path(a.admin_gate_root).resolve() / "tests"))
suite = unittest.defaultTestLoader.discover(str(Path(__file__).parent), pattern="test_*transport.py")
result = unittest.TextTestRunner(verbosity=2).run(suite)
raise SystemExit(0 if result.wasSuccessful() else 1)
