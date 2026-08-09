#!/usr/bin/env python3
r"""Anchor census -- a REPORTING TOOL. Not a check. Not registered.

    python3 scripts/anchor_census.py "<path to Papers>"
    python3 scripts/anchor_census.py "<path to Papers>" --all-anchors
    python3 scripts/anchor_census.py "<path to Papers>" --json out.json

Every place a paper names a code object, across EVERY anchor macro the corpus
actually uses, resolved against this repository. Writes `anchor_census.json`
beside itself.

WHY THIS EXISTS
---------------
The house convention is `\coderef{check\_name}{module.py}`, and every
anchor-drift sweep ever run here was written against `\coderef`. On 2026-08-06
a live paper site was found stating a claim its cited check does not support,
and it had been invisible to all of them because it uses `\codeid{}`.

Measured: `\coderef` is **40.8%** of anchor call SITES (55.5% of named
objects -- it takes two arguments where `\codeid` takes one). Quote the site
figure for sweep coverage; a grep matches sites.
Six idioms are in live use. Four live papers contain no `\coderef` at all, and
the three most anchor-dense papers in the corpus -- Papers 20, 13 and 0 -- are
effectively invisible to a `\coderef` sweep (3 of 555, 1 of 353, 8 of 330).

So every previous sweep read a minority of the anchors, and a different
minority each time it was rewritten. That is why fixing one anchor problem kept
revealing another: the instrument was handing out fragments of a finite list.
This tool exists to hand out the whole list at once.

WHAT IT CLAIMS
--------------
Four things, all facts:

  * an anchor's argument names a `def` that exists in this tree, or it does not;
  * an anchor's module argument names a file that exists in this tree, or not;
  * a resolved check anchor names something the bank actually registers;
  * a two-argument anchor's check and module agree -- that the named check is
    actually defined in the named module. A check that moved between modules
    leaves both arguments resolving and the pairing wrong, which is exactly
    what an existence-only sweep cannot see.

That is all. A resolution failure is objective and worth acting on. Everything
else -- whether the sentence around an anchor is *supported* by the check it
names -- is a judgement this tool deliberately does not make.

WHAT IT DOES NOT CLAIM, AND WHY
-------------------------------
An earlier version of this work shipped a comparator that flagged docstrings
carrying a scope caveat their `key_result` dropped. It returned 216 flags; nine
were hand-read and six were false positives. Under Working Rule 17 -- an
instrument that infers from syntax what the code never wrote down is the wrong
shape, and its audit findings will be infinite -- that comparator is NOT part
of this tool and its 216 figure may not be cited. Semantic drift between a
paper's sentence and a check's content is read by a person, one anchor at a
time, or by a seat with a brief.

`\codeid` is overloaded: it also typesets git SHAs, LaTeX labels, macro
parameters and JSON keys. Those are partitioned out by shape and reported
separately rather than counted as unresolved anchors.

TWO BUGS THIS TOOL WAS BORN WITH, FIXED, AND KEPT FIXED
------------------------------------------------------
  * `^\s*def\s+` -- `\s` matches newlines, which puts the match start on a
    preceding blank line and shifts every reported line number. Use `[ \t]*`.
  * module arguments are written `apf/foo.py`; matching on basename alone
    reports ~50 phantom resolutions.

Both were found by the seat that wrote the first version, in its own output.
"""
import os
import re
import sys
import json
import collections

# --------------------------------------------------------------------------
# anchor macros. Derived by enumeration on 2026-08-06, not assumed; rerun the
# discovery pass (--discover) if a paper starts using a new one.
#
# value = indices of the macro's brace-arguments that name a code object.
# --------------------------------------------------------------------------
ANCHOR_MACROS = {
    "coderef":    [0, 1],
    "coderefbrk": [0, 1],
    "coderefcap": [0, 1],
    "codeid":     [0],
    "checkid":    [0],
    "bank":       [0, 1],
}

HELD_FILES = {"carrier_side_dependency_ledger.py"}   # held out of the bank by design


def classify_tex(path, papers_root):
    parts = os.path.relpath(path, papers_root).split(os.sep)
    if "Old" in parts:        return "OLD"
    if "_to_delete" in parts: return "TO_DELETE"
    if "Reviews" in parts:    return "REVIEWS"
    return "LIVE" if len(parts) == 2 else "ANCILLARY"


def brace_args(s, i):
    """Read consecutive {...} groups starting at i. Brace-matched, not regex:
    anchor arguments contain escaped underscores and occasionally nested braces."""
    args = []
    n = len(s)
    while i < n and s[i] in " \t":
        i += 1
    while i < n and s[i] == "{":
        depth, j = 0, i
        while j < n:
            if s[j] == "\\":
                j += 2
                continue
            if s[j] == "{":
                depth += 1
            elif s[j] == "}":
                depth -= 1
                if depth == 0:
                    break
            j += 1
        if j >= n:
            break
        args.append(s[i + 1:j])
        i = j + 1
    return args, i


def clean(arg):
    """Strip the LaTeX that survives into an argument."""
    a = arg.strip()
    a = re.sub(r"\\[,;:!]", "", a)                       # thin spaces
    a = a.replace("\\_", "_").replace("\\%", "%")
    a = re.sub(r"\\(?:texttt|textit|textbf|emph|mbox|text)\s*\{([^}]*)\}", r"\1", a)
    a = a.replace("{", "").replace("}", "").replace("$", "")
    return a.strip()


# argument shapes that are NOT code objects -----------------------------------
RE_SHA        = re.compile(r"^[0-9a-f]{7,40}$")
RE_TEX_LABEL  = re.compile(r"^(?:sec|fig|tab|eq|thm|lem|rem|def|app|alg|prop|cor):")
RE_MACROPARAM = re.compile(r"^#\d")
RE_MODULE     = re.compile(r"^[\w./\\-]+\.py$")
RE_IDENT      = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def arg_kind(a):
    if not a:                       return "EMPTY"
    if RE_MACROPARAM.match(a):      return "MACRO_PARAM"
    if RE_TEX_LABEL.match(a):       return "TEX_LABEL"
    if RE_MODULE.match(a):          return "MODULE"
    if RE_SHA.match(a):             return "SHA"
    if RE_IDENT.match(a):           return "CHECKNAME" if a.startswith("check_") else "IDENT"
    return "OTHER"


NON_CODE = {"MACRO_PARAM", "TEX_LABEL", "SHA", "EMPTY", "OTHER"}


def index_code(code_root):
    """def-name -> [(relpath, lineno)] (ALL sites, needed for the pairing test),
    and the set of module relpaths."""
    defs = collections.defaultdict(list)
    modules = set()
    # [ \t]* and NOT \s* -- \s eats newlines and shifts every line number.
    pat = re.compile(r"^[ \t]*def[ \t]+([A-Za-z_][A-Za-z0-9_]*)[ \t]*\(", re.M)
    for root, dirs, names in os.walk(code_root):
        dirs[:] = [d for d in dirs if d not in ("__pycache__", ".git", ".pytest_cache")]
        for n in names:
            if not n.endswith(".py") or n in HELD_FILES:
                continue
            p = os.path.join(root, n)
            rel = os.path.relpath(p, code_root).replace(os.sep, "/")
            modules.add(rel)
            try:
                s = open(p, encoding="utf-8", errors="replace").read()
            except OSError:
                continue
            for m in pat.finditer(s):
                defs[m.group(1)].append((rel, s.count("\n", 0, m.start()) + 1))
    return defs, modules


def resolve(kind, arg, defs, modules):
    """(status, evidence). status in RESOLVED / UNRESOLVED / NOT_CODE."""
    if kind in NON_CODE:
        return "NOT_CODE", kind
    if kind == "MODULE":
        a = arg.replace("\\", "/")
        if a in modules:
            return "RESOLVED", a
        tail = [m for m in modules if m.endswith("/" + a) or m == a]
        if len(tail) == 1:
            return "RESOLVED", tail[0]
        if len(tail) > 1:
            return "RESOLVED", f"{len(tail)} matches: {sorted(tail)[:3]}"
        # basename-only match is how ~50 phantom resolutions were once reported;
        # it is recorded as evidence, never as a resolution.
        base = [m for m in modules if os.path.basename(m) == os.path.basename(a)]
        return "UNRESOLVED", (f"basename-only match {base[0]}" if base else "no such file")
    for cand in (arg, "check_" + arg):
        if cand in defs:
            rel, line = defs[cand][0]
            return "RESOLVED", f"{rel}:{line}" + (f" (+{len(defs[cand])-1} more)" if len(defs[cand]) > 1 else "")
    near = sorted(n for n in defs if arg and (n.startswith(arg) or arg in n))[:3]
    return "UNRESOLVED", ("near: " + ", ".join(near) if near else "no such def")


def discover(papers_root):
    """Every macro token in the corpus, by live occurrence count. Rerun this
    when a paper may have started using an anchor idiom not in ANCHOR_MACROS."""
    counts = collections.Counter()
    for root, dirs, names in os.walk(papers_root):
        for n in names:
            if not n.endswith(".tex"):
                continue
            p = os.path.join(root, n)
            if classify_tex(p, papers_root) != "LIVE":
                continue
            s = open(p, encoding="utf-8", errors="replace").read()
            for m in re.finditer(r"\\([A-Za-z@]+)", s):
                counts[m.group(1)] += 1
    return counts


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    papers_root = os.path.abspath(argv[1])
    code_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    show_all = "--all-anchors" in argv
    out_json = argv[argv.index("--json") + 1] if "--json" in argv else \
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "anchor_census.json")

    if "--discover" in argv:
        for mac, c in discover(papers_root).most_common(60):
            mark = "  <- in ANCHOR_MACROS" if mac in ANCHOR_MACROS else ""
            print(f"{c:8d}  \\{mac}{mark}")
        return 0

    defs, modules = index_code(code_root)
    print(f"code index: {len(defs)} distinct def names, {len(modules)} modules "
          f"(held files excluded: {sorted(HELD_FILES)})")

    rows = []
    by_macro_occ = collections.Counter()   # macro CALL SITES, counted as scanned
    per_file_class = collections.Counter()
    for root, dirs, names in os.walk(papers_root):
        for n in sorted(names):
            if not n.endswith(".tex"):
                continue
            p = os.path.join(root, n)
            cls = classify_tex(p, papers_root)
            per_file_class[cls] += 1
            if cls != "LIVE":
                continue
            paper = os.path.relpath(p, papers_root).split(os.sep)[0]
            s = open(p, encoding="utf-8", errors="replace").read()
            for m in re.finditer(r"\\([A-Za-z]+)", s):
                mac = m.group(1)
                if mac not in ANCHOR_MACROS:
                    continue
                by_macro_occ[mac] += 1
                args, _ = brace_args(s, m.end())
                line = s.count("\n", 0, m.start()) + 1
                for slot in ANCHOR_MACROS[mac]:
                    if slot >= len(args):
                        continue
                    a = clean(args[slot])
                    kind = arg_kind(a)
                    status, evidence = resolve(kind, a, defs, modules)
                    rows.append(dict(paper=paper, file=os.path.relpath(p, papers_root),
                                     line=line, macro=mac, slot=slot, arg=a,
                                     kind=kind, status=status, evidence=evidence))

    code_rows = [r for r in rows if r["status"] != "NOT_CODE"]

    # An unresolved argument is only an ANCHOR FAILURE if it was trying to name
    # a code object in the first place. \codeid is also used to typeset premise
    # and axiom identifiers -- FD2, OR0, D_positivity, Paper0_row10_* -- which
    # are bare identifiers that will never resolve because they are not defs.
    # Counting those as broken anchors inflated the first run of this tool by
    # roughly 100 and would have sent someone hunting for checks that were never
    # meant to exist. They are reported separately and are not failures.
    def is_anchor_failure(r):
        if r["status"] != "UNRESOLVED":
            return False
        if r["kind"] in ("MODULE", "CHECKNAME"):
            return True
        return r["evidence"].startswith("near: check_")      # bare name, clear code referent

    unres = [r for r in code_rows if is_anchor_failure(r)]
    ambiguous = [r for r in code_rows
                 if r["status"] == "UNRESOLVED" and not is_anchor_failure(r)]

    print(f"\ntex files: " + "  ".join(f"{k} {v}" for k, v in sorted(per_file_class.items())))
    print(f"anchor arguments in LIVE papers: {len(rows)}   "
          f"code-shaped: {len(code_rows)}   "
          f"ANCHOR FAILURES: {len(unres)}   "
          f"non-code identifiers (premise/axiom IDs, not failures): {len(ambiguous)}")

    # TWO UNITS, and they differ by ~17 points. Report both; a single figure
    # here gets quoted without its unit and then disagrees with the next
    # measurement for no visible reason.
    #   occurrences = macro call sites. This is what a `grep \coderef` sees,
    #                 so it is the honest denominator for sweep coverage.
    #   arguments   = named code objects. \coderef{a}{b} names two, \codeid{x} one.
    by_macro_args = collections.Counter(r["macro"] for r in rows)
    # Counted at the call site during the scan. Deriving this from `rows` by
    # de-duplicating (file, line, macro) collapses two anchors that share a
    # line into one, which undercounts \codeid badly -- it is the idiom most
    # often used twice in a sentence.
    tot_args = sum(by_macro_args.values()) or 1
    tot_occ = sum(by_macro_occ.values()) or 1
    print("\nidiom coverage            occurrences        arguments")
    for mac, _ in by_macro_args.most_common():
        o, a = by_macro_occ.get(mac, 0), by_macro_args[mac]
        print(f"  \\{mac:<12s}  {o:6d} {100.0*o/tot_occ:5.1f}%    {a:6d} {100.0*a/tot_args:5.1f}%")
    print(f"\n  A \\coderef-only sweep sees {100.0*by_macro_occ.get('coderef',0)/tot_occ:.1f}% "
          f"of anchor SITES ({100.0*by_macro_args.get('coderef',0)/tot_args:.1f}% of named objects).")
    print("  Quote the site figure for sweep coverage: a grep matches sites, not arguments.")

    # The payoff of resolving \coderef too: nobody had ever checked those.
    ur_cr = [r for r in unres if r["macro"] == "coderef"]
    print(f"\n  Of {len(unres)} unresolved anchors, {len(ur_cr)} are in \\coderef itself"
          f" — the idiom every previous sweep did read, and none resolved.")

    print("\nper-paper: anchors / of which \\coderef / unresolved")
    per = collections.defaultdict(lambda: [0, 0, 0])
    for r in rows:
        per[r["paper"]][0] += 1
        if r["macro"] == "coderef":
            per[r["paper"]][1] += 1
    for r in unres:
        per[r["paper"]][2] += 1
    for paper in sorted(per, key=lambda k: -per[k][0]):
        a, c, u = per[paper]
        flag = "  <- no \\coderef at all" if c == 0 else ""
        print(f"  {a:5d} / {c:5d} / {u:4d}   {paper}{flag}")

    def bucket(r):
        if r["kind"] == "MODULE":
            return "MODULE_MISSING" if r["evidence"] == "no such file" else "MODULE_BASENAME_ONLY"
        ev = r["evidence"]
        if ev.startswith("near: "):
            for c in ev[6:].split(", "):
                if c == r["arg"] + "_P" or c == "check_" + r["arg"]:
                    return "GRADE_SUFFIX_DROPPED"
            return "NEAR_MISS"
        return "CHECK_ABSENT"

    buckets = collections.Counter(bucket(r) for r in unres)
    print("\ntriage of anchor failures")
    for k, c in buckets.most_common():
        print(f"  {k:<24s} {c:5d}")
    print("\n  GRADE_SUFFIX_DROPPED is one habit, not N problems. Checked against git:\n"
          "  the _P forms have been present since the initial import and the bare\n"
          "  forms never existed, so this is not a rename the papers missed -- it is\n"
          "  the grade suffix being dropped when a name is transcribed by hand.\n"
          "  Fix the pattern, and expect it wherever names are typed from memory.")

    print(f"\n=== ANCHOR FAILURES: {len(unres)} occurrences, "
          f"{len({r['arg'] for r in unres})} distinct names ===")
    grouped = collections.defaultdict(list)
    for r in unres:
        grouped[(r["arg"], r["evidence"])].append(r)
    for (arg, ev), rs in sorted(grouped.items(), key=lambda kv: -len(kv[1])):
        sites = ", ".join(f"{x['paper']}:{x['line']}" for x in rs[:3])
        more = f" (+{len(rs)-3})" if len(rs) > 3 else ""
        print(f"  {len(rs):4d}x  {arg:<58s} {ev}")
        print(f"           {sites}{more}")

    if ambiguous:
        names = sorted({r["arg"] for r in ambiguous})
        print(f"\n=== NOT ANCHOR FAILURES: {len(ambiguous)} occurrences, {len(names)} distinct ===")
        print("  Bare identifiers typeset with an anchor macro that name no code object.")
        print("  Premise IDs, axiom labels, row identifiers. Listed so nobody hunts for them.")
        for i in range(0, min(len(names), 40), 4):
            print("   " + "  ".join(f"{x:<28s}" for x in names[i:i+4]))
        if len(names) > 40:
            print(f"   ... and {len(names)-40} more (see JSON)")

    # ---- PAIRING. A two-argument anchor names a check AND a module. Resolving
    # each independently is not enough: a check that MOVED between modules
    # leaves both arguments resolving and the pairing silently wrong. This is
    # the failure an existence-only sweep cannot see, and it is the reason this
    # stage exists.
    sites_pair = collections.defaultdict(dict)
    for r in rows:
        if len(ANCHOR_MACROS.get(r["macro"], [])) > 1:
            sites_pair[(r["file"], r["line"], r["macro"])][r["slot"]] = r
    mismatch = []
    paired = 0
    for slots in sites_pair.values():
        a, b = slots.get(0), slots.get(1)
        if not (a and b):
            continue
        if a["status"] != "RESOLVED" or b["status"] != "RESOLVED":
            continue
        if a["kind"] not in ("CHECKNAME", "IDENT") or b["kind"] != "MODULE":
            continue
        homes = set()
        for cand in (a["arg"], "check_" + a["arg"]):
            for rel, _ln in defs.get(cand, []):
                homes.add(rel)
        if not homes:
            continue
        # A macro DEFINITION in a preamble reads as \coderef{a}{b}; single-letter
        # arguments are the tell, and they are not anchors.
        if len(a["arg"]) < 3:
            continue
        paired += 1
        want = b["arg"].replace("\\", "/")
        if not any(h == want or h.endswith("/" + want) or
                   os.path.basename(h) == os.path.basename(want) for h in homes):
            mismatch.append((a, want, sorted(homes)))

    print(f"\n=== PAIRING: {paired} two-argument anchors with both arguments resolved ===")
    print(f"    MISMATCHED (check exists, module exists, check is not in it): {len(mismatch)}")
    if mismatch:
        print("    Invisible to any existence-only sweep.")
        seen_pair = set()
        for a, want, homes in sorted(mismatch, key=lambda x: (x[0]["paper"], x[0]["line"])):
            k = (a["arg"], want)
            if k in seen_pair:
                continue
            seen_pair.add(k)
            print(f"      {a['arg']}")
            print(f"          paper says {want:<38s} lives in {', '.join(homes[:3])}")
            print(f"          {a['paper']}:{a['line']}")

    # ---- REGISTRATION. A def can exist and not be in the bank. A paper
    # anchoring one cites a function the engine never runs as a check. Guarded:
    # if the registry will not import, the rest of this tool still works.
    try:
        import sys as _sys
        _sys.path.insert(0, code_root)
        from apf import bank as _bank            # noqa
        _bank._load()
        reg = set(_bank.REGISTRY)
        reg |= {k[6:] for k in list(reg) if k.startswith("check_")}
        reg |= {"check_" + k for k in list(reg)}
    except Exception as e:                        # noqa
        reg = None
        print(f"\n(registry probe unavailable: {type(e).__name__}; skipping the registration stage)")

    if reg is not None:
        chk = [r for r in rows if r["status"] == "RESOLVED" and r["kind"] in ("CHECKNAME", "IDENT")]
        unreg = [r for r in chk if r["arg"] not in reg]
        names = sorted({r["arg"] for r in unreg})
        print(f"\n=== REGISTRATION: {len(chk)} resolved check anchors, "
              f"{len(unreg)} naming a def the bank does not register "
              f"({len(names)} distinct) ===")
        print("    NOT automatically a defect. Helper functions, record factories and")
        print("    apf/standalone/ are unregistered by design. It IS a defect when a")
        print("    paper cites one as if the engine verified it. Read each.")
        for i in range(0, len(names), 3):
            print("     " + "  ".join(f"{x:<38s}" for x in names[i:i+3]))

    nc = collections.Counter(r["kind"] for r in rows if r["status"] == "NOT_CODE")
    if nc:
        print("\npartitioned out as not naming a code object (\\codeid is overloaded):")
        for k, c in nc.most_common():
            print(f"  {k:<14s} {c}")

    if show_all:
        print("\n=== ALL RESOLVED ANCHORS ===")
        for r in sorted(code_rows, key=lambda x: (x["paper"], x["line"])):
            if r["status"] == "RESOLVED":
                print(f"  {r['paper']:<44s} {r['line']:6d}  \\{r['macro']:<10s} "
                      f"{r['arg']:<52s} {r['evidence']}")

    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(dict(rows=rows, code_root=code_root, papers_root=papers_root,
                    pairing_mismatch=[dict(arg=a["arg"], claimed=w, actual=h,
                                           paper=a["paper"], line=a["line"])
                                      for a, w, h in mismatch]), f, indent=1)
    print(f"\nwrote {out_json}")
    print("\nThis tool makes no claim about whether a resolved anchor's sentence is\n"
          "supported by the check it names. That is a human read, one anchor at a time.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
