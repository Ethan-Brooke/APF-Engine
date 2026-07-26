"""RP-CT.W quarantine label -- the open W-export program, isolated for legibility.

NOT a bank module: it defines no ``check_*`` functions, registers nothing, and
changes no count. It names the RP-CT.W severable subtree so analysis and routing
tools can separate the *core / paper-adjacent* bank from the open W-export
program.

Background (2026-07-25 dependency trace). ~2,386 checks (~58% of the bank) are
the first-principles one-loop M_W / Delta-r derivation: Denner/DIZET import,
Passarino-Veltman substrate, coefficient tables, release/attestation ledgers.
That set is a self-contained sink -- consumed by nothing outside itself except a
25-check native-self-energy seam feeding Paper 33's S/T/U oblique parameters
(the 5 externally-cited seam checks are in ``SEAMS``). The program is still
``[P_export_candidate]``-OPEN and unpublished; left uncounted-apart it makes the
bank's published surface look ~3x smaller than it is (naive paper-coverage read
as ~12%). This module makes the split first-class WITHOUT removing, gating, or
reordering a single check.

Usage
-----
    from apf._rp_ct_w_quarantine import (
        RP_CT_W_SEVERABLE, RP_CT_W_SEAM_KEEP, SEAMS, core_bank, is_open_program)
    core = core_bank(bank.REGISTRY)   # REGISTRY names minus the severable sink

The partition ships in ``apf/data/rp_ct_w_quarantine.json`` (computed on the
4081-check bank). If the bank has drifted materially, recompute it from the 5
seam checks and refresh the JSON at signoff.
"""
import json
import os

_DATA = os.path.join(os.path.dirname(__file__), "data", "rp_ct_w_quarantine.json")
with open(_DATA, encoding="utf-8") as _f:
    _d = json.load(_f)

RP_CT_W_SEVERABLE = frozenset(_d["severable"])   # ~2386 open-program checks (the sink)
RP_CT_W_SEAM_KEEP = frozenset(_d["seam_keep"])   # 25 native-self-energy checks Paper 33 consumes
SEAMS = tuple(_d.get("seams", []))               # the 5 externally-cited seam checks
COMPUTED_ON_BANK_SIZE = _d.get("computed_on_bank_size")


def core_bank(registry_names):
    """Core / paper-adjacent bank = the given check names minus the RP-CT.W sink.

    ``registry_names`` may be a ``bank.REGISTRY`` dict or any iterable of names.
    """
    return set(registry_names) - RP_CT_W_SEVERABLE


def is_open_program(check_name):
    """True iff ``check_name`` is in the quarantined RP-CT.W open-export sink."""
    return check_name in RP_CT_W_SEVERABLE
