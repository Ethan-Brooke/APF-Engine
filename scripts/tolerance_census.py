#!/usr/bin/env python3
"""Tolerance census -- a REPORTING TOOL. Not a check. Not registered.

    python3 scripts/tolerance_census.py apf

Prints every numeric-bound comparison in the tree above a looseness floor,
grouped by an inferred unit with the evidence that produced it, and writes
census.json beside itself.

READ THIS BEFORE QUOTING ITS OUTPUT. The unit classification is a HEURISTIC
and it is wrong often enough to matter. Three blinded audits on 2026-08-01
established that inferring "is this number a percentage" from source syntax
is not a solved problem and probably is not a solvable one: the space of ways
to write a tolerance in Python is open-ended, and every audit found another
form the classifier had not anticipated -- leading-vs-trailing 100, bare
fractions, helper calls, chained comparisons, named-constant bounds, and an
f-string convention that means the OPPOSITE of what the classifier assumed.
Two successive banked-check versions built on this classifier were reduced
and reverted for exactly that reason.

So this ships as a tool that MAKES NO CLAIM. Its output is a starting point
for a human read, never a verdict, and nothing in the bank depends on it.
Every row it prints must be read in source before it is cited. The durable
findings it produced are written up in
`__APF Library/Artifacts_2026-08-01_session/tolerance_audit_repair/`.

The real fix, if this is ever picked up again, is not a better classifier: it
is to make tolerances DECLARE their unit and their envelope at the site, so
nothing has to be inferred. See the session note for that design.
"""

import sys, json, os
from collections import Counter

TOLERANCE_MIN_BOUND = 5.0        # percent; typed-tight sites at or below are dropped
TOLERANCE_FRACTION_FLOOR = 0.05  # an untyped bound in (this, 1.0] is retained


def _tol_sites(root):
    """Every ``X < literal`` / ``X <= literal`` site under ``root``, AST-walked.

    Returns (sites, parse_failures). Each site is
    (relpath, funcname, expr_text, bound, ordinal, lineno, unit, evidence).
    Unit is one of percent / fraction / absolute / unknown and always carries
    the evidence that produced it; the caller never treats it as a verdict.
    """
    import ast, os, re
    ABS_UNIT = re.compile(r'(mev|gev|kev|tev|_ev|kg|km|mpc|deg|degree|rad|'
                          r'nat|bit|sigma|hz|dbm|kelvin)', re.I)
    PCT_NAME = re.compile(r'(?:^|_)(pct|percent)(?:$|_)', re.I)

    def up(n):
        try:
            return ast.unparse(n)
        except Exception:
            return '<unparse-failed>'

    def scaled_by_100(node):
        """Multiplied or divided by a literal 100, in EITHER operand order."""
        for s in ast.walk(node):
            if isinstance(s, ast.BinOp) and isinstance(s.op, (ast.Mult, ast.Div)):
                for side in (s.left, s.right):
                    if isinstance(side, ast.Constant) and isinstance(
                            side.value, (int, float)) and not isinstance(side.value, bool):
                        if abs(float(side.value) - 100.0) < 1e-9:
                            return True
        return False

    def has_div(n):
        return any(isinstance(s, ast.BinOp) and isinstance(s.op, ast.Div)
                   for s in ast.walk(n))

    def relative_deviation(node):
        """(a/b - 1), (1 - a/b) or (a-b)/b: a bare fractional deviation."""
        for s in ast.walk(node):
            if isinstance(s, ast.BinOp) and isinstance(s.op, ast.Sub):
                for a, b in ((s.left, s.right), (s.right, s.left)):
                    if isinstance(b, ast.Constant) and isinstance(b.value, (int, float)) \
                            and not isinstance(b.value, bool) \
                            and abs(float(b.value) - 1.0) < 1e-9 and has_div(a):
                        return True
            if isinstance(s, ast.BinOp) and isinstance(s.op, ast.Div) \
                    and isinstance(s.left, ast.BinOp) and isinstance(s.left.op, ast.Sub):
                return True
        return False

    class Fn:
        def __init__(self, node):
            self.assign, self.pct_fmt, self.frac_fmt = {}, set(), set()
            for s in ast.walk(node):
                if isinstance(s, (ast.Assign, ast.AugAssign)):
                    rhs = s.value
                    if isinstance(s, ast.AugAssign):
                        rhs = ast.BinOp(left=ast.Name(id='_', ctx=ast.Load()),
                                        op=s.op, right=s.value)
                    tgts = s.targets if isinstance(s, ast.Assign) else [s.target]
                    for t in tgts:
                        if isinstance(t, ast.Name):
                            self.assign.setdefault(t.id, []).append(rhs)
                if isinstance(s, ast.JoinedStr):
                    vals = s.values
                    for i, p in enumerate(vals):
                        if not isinstance(p, ast.FormattedValue):
                            continue
                        nxt = vals[i + 1] if i + 1 < len(vals) else None
                        if not (isinstance(nxt, ast.Constant)
                                and isinstance(nxt.value, str)
                                and nxt.value.lstrip().startswith('%')):
                            continue
                        # CORRECTED 2026-08-01. This rule was inverted and
                        # name-promiscuous, and the two faults compounded into
                        # SILENT DELETION. ``f"{100*x:.1f}%"`` proves x is a
                        # FRACTION -- the author is scaling it to print it --
                        # but the rule read it as evidence x is a PERCENT, and
                        # a percent below TOLERANCE_MIN_BOUND is dropped. It
                        # removed 13 live sites, among them a 15% gauge-
                        # unification envelope (supplements.py unif_quality).
                        # It also walked EVERY Name in the expression, so
                        # ``abs``, ``float`` and any dict name poisoned the
                        # function -- evidence strings in the corpus read
                        # "abs is printed immediately before a literal %".
                        # Only the ROOT of the formatted expression counts.
                        expr = p.value
                        if isinstance(expr, ast.Name):
                            self.pct_fmt.add(expr.id)            # {x}%  -> x is a percent
                            continue
                        if isinstance(expr, ast.BinOp) and isinstance(expr.op, ast.Mult):
                            for a, b in ((expr.left, expr.right), (expr.right, expr.left)):
                                if isinstance(a, ast.Constant) and isinstance(a.value, (int, float)) \
                                        and not isinstance(a.value, bool) \
                                        and abs(float(a.value) - 100.0) < 1e-9 \
                                        and isinstance(b, ast.Name):
                                    self.frac_fmt.add(b.id)      # {100*x}% -> x is a FRACTION

        def classify(self, left):
            txt = up(left)
            names = [n.id for n in ast.walk(left) if isinstance(n, ast.Name)]
            if relative_deviation(left) and not scaled_by_100(left):
                return 'fraction', 'compared expression is a bare relative deviation'
            if scaled_by_100(left):
                return 'percent', 'compared expression is scaled by 100'
            for nm in names:
                if PCT_NAME.search(nm):
                    return 'percent', 'name marks a percentage: %s' % nm
            for nm in names:
                for rhs in self.assign.get(nm, []):
                    if scaled_by_100(rhs):
                        return 'percent', '%s assigned from an expression scaled by 100' % nm
            for nm in names:
                for rhs in self.assign.get(nm, []):
                    if relative_deviation(rhs):
                        return 'fraction', '%s assigned from a bare relative deviation' % nm
            for nm in names:
                if nm in self.frac_fmt:
                    return 'fraction', '%s is printed as "{100*%s}%%", so it is a fraction' % (nm, nm)
            for nm in names:
                if nm in self.pct_fmt:
                    return 'percent', '%s is printed as "{%s}%%", so it is a percentage' % (nm, nm)
            for nm in names + [txt]:
                if ABS_UNIT.search(nm):
                    return 'absolute', 'carries a unit token: %s' % nm[:40]
            return 'unknown', 'no unit evidence'

    sites, fails, seen, kwtol = [], [], {}, []
    for dirpath, _, files in os.walk(root):
        if '__pycache__' in dirpath:
            continue
        for fname in sorted(files):
            if not fname.endswith('.py'):
                continue
            path = os.path.join(dirpath, fname)
            rel = os.path.relpath(path, root).replace(os.sep, '/')
            try:
                with open(path, encoding='utf-8') as fh:
                    tree = ast.parse(fh.read())
            except Exception as exc:
                fails.append((rel, str(exc)[:100]))
                continue
            # Module-level numeric constants, so a bound written as a NAME
            # is resolvable. Found by a blinded audit 2026-08-01: the bound in
            # ``abs(lam_nf3 - LAMBDA_QCD_PDG_NF3) < LAMBDA_QCD_PDG_NF3``
            # (confinement_scale_single_anchor.py) is a Name, so the site did
            # not exist for this audit at all -- and it accepts anything within
            # 100% of the PDG comparator. A tolerance is no less real for being
            # spelled with a constant.
            modconst = {}
            for node in tree.body:
                if isinstance(node, ast.Assign) and isinstance(node.value, ast.Constant) \
                        and isinstance(node.value.value, (int, float)) \
                        and not isinstance(node.value.value, bool):
                    for t in node.targets:
                        if isinstance(t, ast.Name):
                            modconst[t.id] = float(node.value.value)

            for node in ast.walk(tree):
                # Same parse, second shape: rel_tol / rtol keywords. Folded in
                # here rather than re-walking the tree, which doubled runtime.
                if isinstance(node, ast.Call):
                    for kw in node.keywords or []:
                        if kw.arg in ('rel_tol', 'rtol') \
                                and isinstance(kw.value, ast.Constant) \
                                and isinstance(kw.value.value, (int, float)) \
                                and not isinstance(kw.value.value, bool) \
                                and float(kw.value.value) > TOLERANCE_FRACTION_FLOOR:
                            kwtol.append({'file': rel, 'line': node.lineno,
                                          'kw': kw.arg, 'value': float(kw.value.value)})
            for fn in ast.walk(tree):
                if not isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    continue
                sc = Fn(fn)
                for cmp_ in ast.walk(fn):
                    if not isinstance(cmp_, ast.Compare):
                        continue
                    # Every (operand, op, bound) pair in the chain, not just
                    # the first. ``0.0 <= err_pct < 45.0`` is one Compare node
                    # with two ops; requiring len(ops) == 1 discarded it whole,
                    # and a blinded audit counted 115 loose chained sites lost
                    # that way. Reversed bounds (``45.0 > err_pct``) are read
                    # in the same pass -- an auditor smuggled a live tolerance
                    # through that shape.
                    for _i, (_op, _rhs) in enumerate(zip(cmp_.ops, cmp_.comparators)):
                        _lhs = cmp_.left if _i == 0 else cmp_.comparators[_i - 1]
                        if isinstance(_op, (ast.Lt, ast.LtE)):
                            quant, bound_node = _lhs, _rhs
                        elif isinstance(_op, (ast.Gt, ast.GtE)):
                            quant, bound_node = _rhs, _lhs
                        else:
                            continue
                        bound_is_name = False
                        if isinstance(bound_node, ast.Constant) \
                                and isinstance(bound_node.value, (int, float)) \
                                and not isinstance(bound_node.value, bool):
                            bound_val = float(bound_node.value)
                        elif isinstance(bound_node, ast.Name) and bound_node.id in modconst:
                            bound_val = modconst[bound_node.id]
                            bound_is_name = True
                        else:
                            continue
                        if isinstance(quant, ast.Constant):
                            continue          # literal < literal: not a tolerance
                        if isinstance(quant, ast.Name) and quant.id in modconst:
                            continue          # constant < constant, spelled with names
                        val = bound_val
                        if val <= 0:
                            continue          # a non-positive bound is not a tolerance
                        cmp_left = quant
                        unit, ev = sc.classify(cmp_left)
                        # Retention rule. A site is dropped ONLY when the
                        # classifier has POSITIVE evidence that it is tight.
                        # Anything the classifier cannot type is retained if its
                        # bound could be a fraction -- because the classifier
                        # recognises two relative-deviation templates and a
                        # genuine 30% gate written any other way
                        # (abs(p-o)/abs(o), a two-step ratio, a helper call)
                        # otherwise vanished with no site, no ledger row and no
                        # count. That silent drop was the sharpest finding of the
                        # 2026-08-01 blinded audit of this module's first version.
                        if unit == 'percent' and val <= TOLERANCE_MIN_BOUND:
                            continue
                        if unit == 'fraction':
                            if val > 1.0:
                                unit, ev = 'unknown', 'fraction reading exceeds 100%; unresolved'
                            elif val * 100 <= TOLERANCE_MIN_BOUND:
                                continue
                        if unit in ('absolute', 'unknown'):
                            plausible_fraction = TOLERANCE_FRACTION_FLOOR < val <= 1.0
                            if val <= TOLERANCE_MIN_BOUND and not plausible_fraction:
                                continue
                        expr = up(cmp_left)[:90]
                        if bound_is_name:
                            ev = ev + ' | bound is the module constant %s = %g' % (
                                bound_node.id, bound_val)
                        key = (rel, fn.name, expr, val)
                        seen[key] = seen.get(key, -1) + 1
                        sites.append((rel, fn.name, expr, val, seen[key],
                                      cmp_.lineno, unit, ev))
    return sites, fails, kwtol


def main():
    root = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else 'apf')
    sites, fails, kwtol = _tol_sites(root)
    rows = [dict(file=f, func=fn, expr=ex, bound=b, ordinal=o, line=ln,
                 unit=u, evidence=ev)
            for f, fn, ex, b, o, ln, u, ev in sites]
    with open('census.json', 'w') as fh:
        json.dump(dict(root=root, sites=rows, parse_failures=fails,
                       keyword_tolerances=kwtol), fh, indent=1)

    print('root:', root)
    print('parse failures:', len(fails))
    print('sites above floor:', len(rows), dict(Counter(r['unit'] for r in rows)))
    print('rel_tol/rtol above floor:', len(kwtol))
    print()
    print('EVERY ROW BELOW IS A HEURISTIC. Read it in source before citing it.')

    def show(title, sel, key):
        sub = sorted([r for r in rows if sel(r)], key=key)
        print(chr(10) + '===== %s: %d =====' % (title, len(sub)))
        for r in sub:
            print('%-9g %s:%d  %s' % (r['bound'], r['file'], r['line'], r['func']))
            print('          %s   [%s]' % (r['expr'], r['unit']))
            print('          -> %s' % r['evidence'][:150])

    show('RELATIVE tolerances written as bare fractions (bound x100 = percent)',
         lambda r: r['unit'] == 'fraction', lambda r: -r['bound'])
    show('PERCENT tolerances above the floor',
         lambda r: r['unit'] == 'percent', lambda r: -r['bound'])
    show('ABSOLUTE -- dimensionful; this tool CANNOT price them',
         lambda r: r['unit'] == 'absolute', lambda r: -r['bound'])
    # UNKNOWN is where the loosest real finding of this lane turned up -- a
    # 100%-of-PDG gate whose bound is a named constant. Printing only a COUNT
    # for this bucket would hide exactly the class of thing the tool exists to
    # surface, so the two highest-yield slices are printed in full.
    unk = [r for r in rows if r['unit'] == 'unknown']
    show('UNKNOWN but the bound is a NAMED CONSTANT -- read every one',
         lambda r: r['unit'] == 'unknown' and 'module constant' in r['evidence'],
         lambda r: -r['bound'])
    show('UNKNOWN with a bound in (0.05, 1.0] -- could be a bare fraction, '
         'i.e. a >5% tolerance',
         lambda r: (r['unit'] == 'unknown'
                    and TOLERANCE_FRACTION_FLOOR < r['bound'] <= 1.0),
         lambda r: -r['bound'])
    shown = sum(1 for r in unk
                if 'module constant' in r['evidence']
                or TOLERANCE_FRACTION_FLOOR < r['bound'] <= 1.0)
    print(chr(10) + '===== UNKNOWN, no unit evidence -- NEEDS A HUMAN VERDICT: '
          '%d (%d printed above, %d more in census.json) =====' % (len(unk), shown, len(unk) - shown))
    print('Retained deliberately: an untyped bound in (0.05, 1.0] could be a '
          'fraction, and dropping those silently was the sharpest defect found '
          'in this lane.')


if __name__ == '__main__':
    main()
