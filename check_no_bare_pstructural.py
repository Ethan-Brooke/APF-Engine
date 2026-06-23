#!/usr/bin/env python3
"""Guard: assert no bare 'P_structural' epistemic/status field survives the
v24.3.268 grade split. Every structural-meta mark must carry one of the six
sub-grades (P_structural_seam / _partial / _exhaustive / _instrument /
_reading / _convention). Exits non-zero if any bare mark remains.

Covers both result-construction syntaxes:
  keyword-arg :  epistemic='P_structural'   /  status="P_structural"
  dict-literal:  'epistemic': 'P_structural' / "status": "P_structural"
"""
import re, glob, sys

BARE = re.compile(
    r"(?:epistemic|status)\s*=\s*['\"]P_structural['\"]"          # keyword-arg
    r"|['\"](?:epistemic|status)['\"]\s*:\s*['\"]P_structural['\"]"  # dict-literal
)

def main() -> int:
    hits = []
    for fn in sorted(glob.glob("apf/*.py")):
        for i, line in enumerate(open(fn, encoding="utf-8"), 1):
            if BARE.search(line):
                hits.append(f"{fn}:{i}: {line.strip()}")
    if hits:
        print(f"FAIL: {len(hits)} bare 'P_structural' field(s) remain:")
        print("\n".join(hits))
        return 1
    print("OK: zero bare 'P_structural' fields (all carry a sub-grade).")
    return 0

if __name__ == "__main__":
    sys.exit(main())
