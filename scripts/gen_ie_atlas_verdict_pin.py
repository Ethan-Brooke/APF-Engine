#!/usr/bin/env python3
"""Regenerate apf/ie_atlas_verdict_pin.py from the live atlas (deliberate re-pin).

Run from repo root: PYTHONPATH=. python3 scripts/gen_ie_atlas_verdict_pin.py
Review the diff before committing: every changed line is a consequence change
and must be explainable by the wave's banked content.
"""
import datetime
import os
import sys
import tempfile


def main() -> int:
    from apf.interface_atlas_live_runner import run_live_atlas
    res = run_live_atlas()
    rows = sorted(((r["input_id"], str(r["solver_status"]), bool(r["export_global_P"]))
                   for r in res["all_summaries"]), key=lambda t: t[0])
    fn = "apf/ie_atlas_verdict_pin.py"
    src = open(fn, encoding="utf-8").read()
    head, sep, _ = src.partition("PINNED_VERDICTS = {")
    assert sep, "pin dict anchor missing"
    body = "\n".join('    "%s": ("%s", %r),' % t for t in rows)
    # bump the generated-date line in the docstring
    import re
    head = re.sub(r"Generated \d{4}-\d{2}-\d{2} from", "Generated %s from" % datetime.date.today().isoformat(), head)
    new = head + "PINNED_VERDICTS = {\n" + body + "\n}\n\nPIN_VERSION = \"%s\"\n" % _pin_version()
    fd, tmp = tempfile.mkstemp(dir="apf", suffix=".tmp")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(new)
    os.replace(tmp, fn)
    print("re-pinned %d verdicts -> %s (review the diff before committing)" % (len(rows), fn))
    return 0


def _pin_version() -> str:
    import re
    s = open("setup.py", encoding="utf-8").read()
    m = re.search(r"version='([^']+)'", s)
    return m.group(1) if m else "unknown"


if __name__ == "__main__":
    sys.exit(main())
