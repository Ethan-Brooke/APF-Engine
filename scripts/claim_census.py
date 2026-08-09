#!/usr/bin/env python3
r"""Claim census -- a REPORTING TOOL. Not a check. Not registered.

    python3 scripts/claim_census.py
    python3 scripts/claim_census.py --json out.json --report out.txt
    python3 scripts/claim_census.py --all            # print matched hits too
    python3 scripts/claim_census.py --field summary  # restrict to one field name

Every numeral that is a SOURCE LITERAL inside a string-valued field of the
record a registered check returns. Writes `claim_census.json` beside itself.

WHY THIS EXISTS
---------------
Registered checks return records carrying prose fields -- `key_result`,
`summary`, `status` and others. A numeral written into that prose as a string
literal is not recomputed when the check runs, so it can go stale while the
check stays green and the bank stays at gap 0. The corpus has a recorded
instance: a hardcoded `key_result` still printing "320 conjugates" after a
count edit left zero. Nothing in the engine can see that, because nothing in
the engine reads the prose.

This tool reads the prose. It tells you where the literal numerals are. It
does not tell you which of them are wrong -- most of them are not wrong.

WHAT IT ASSERTS
---------------
Four things, all syntactic and all decidable without inferring anyone's
intent:

  * a registered check's function resolves to a `def` in this tree, and that
    `def` parses -- or it does not, and it is named in the coverage list;
  * the expression a check returns is a record whose string-valued fields can
    be enumerated -- or it is not, and the check is named in the coverage list;
  * a given string-valued field's value is built entirely from source
    literals (LITERAL), partly from interpolated expressions (MIXED), or
    entirely from computed values (COMPUTED);
  * a given run of digits occurs inside a literal segment of such a field,
    at a located line, in a stated textual context.

That is the whole claim surface.

WHAT IT DOES NOT ASSERT, AND WILL NOT
-------------------------------------
  * That any reported numeral is WRONG, STALE, or a DEFECT. It is not
    recomputed -- that is all that is established. A fixed dimension, a
    citation year, a group order, a paper number and a genuinely stale count
    are indistinguishable to this tool, on purpose.
  * That an unreported check is clean. A check whose record could not be
    enumerated is named in the coverage list, not silently dropped.
  * Anything about whether a leg can fail, whether a check is vacuous, or
    whether a docstring's caveat survives into its key_result. Two
    instruments were built for that ground in this corpus, each audited
    REDUCE twice, and both were deleted under a standing do-not-repair
    ruling. This tool does not go there.

THE SHAPE BUCKETS ARE SHAPES, NOT VERDICTS
------------------------------------------
Reported numerals are partitioned into named syntactic shapes -- year-like,
version-like, inside-an-identifier, after-a-section-word, and so on. The
partition exists so that a reader is not sent hunting through several thousand
citation years to find the one count that moved. Membership in a shape bucket
is NOT a claim that the numeral is legitimate, and membership in the residual
UNMATCHED bucket is NOT a claim that it is a defect. The buckets are ordered
and disjoint, so the counts add up; the ordering is stated in SHAPES below.

The stratification that is actually worth reading is MIXED-vs-LITERAL. A
numeral sitting in a field that ALSO interpolates computed values is a numeral
whose author demonstrably knew how to interpolate at that site and did not, at
that spot. That is the exact shape of the "320 conjugates" instance. It is
still not a claim of defect.

THREE FAILURES THIS TOOL IS BUILT NOT TO REPEAT
-----------------------------------------------
  * DERIVE THE POPULATION BY AST. A census in this corpus matched two literal
    token spellings and undercounted its population by 2.3x. The population
    here is taken from `bank.REGISTRY` itself -- the function objects, not a
    name pattern -- resolved to `def` sites through `__code__.co_filename` and
    `co_firstlineno`, and every record field is found by binding call
    arguments to callee parameters, never by matching a helper's name.
  * REPORT COVERAGE AS A FRACTION, PROMINENTLY, AND NAME THE MISSES. Anchor
    sweeps here read 40.8% of their population for months without saying so.
    The coverage fraction is printed in the header and every unanalysed check
    is listed by name.
  * COUNT INSTANCES, NOT LINES. An earlier census collapsed two findings that
    shared a line into one. A field is counted once per (check, field, return
    site); a numeral is counted once per occurrence, including repeats of the
    same digits in the same string.

Registry keys in this corpus exist under both a bare-name and a `check_`
prefixed spelling. Every by-name lookup here checks both.
"""
import os
import re
import sys
import ast
import json
import hashlib
import collections

# ---------------------------------------------------------------------------
# Shape buckets. ORDERED and DISJOINT: the first predicate that matches wins,
# so the bucket counts sum to the raw hit count exactly. Each predicate reads
# a numeral together with a window of the literal text around it.
#
# These are SHAPES. A numeral landing in one of them has not been judged
# legitimate; a numeral landing in UNMATCHED has not been judged wrong.
# ---------------------------------------------------------------------------
UNIT_WORDS = (r'%|GeV|MeV|keV|TeV|eV|nats?|bits?|dBm|Mpc|kpc|km/s|km|kg|'
              r'sigma|σ|degrees?|deg|rad|Hz|K\b|ell_P|fm|ns|ms|s\b|dof')

SHAPES = [
    # ---- unambiguous textual forms -------------------------------------
    ("SHAPE_DATE",
     lambda d, pre, post: bool(re.search(r'\d{4}-\d{2}-\d{2}\Z', pre + d)
                               or re.match(r'-\d{2}-\d{2}', post))),
    ("SHAPE_VERSION",
     lambda d, pre, post: bool(re.search(r'[vV]\Z', pre) and re.match(r'[\d.]*\d', d))
                          or bool(re.search(r'\d+\.\d+\.\d+', d))
                          or bool(re.search(r'(?i)(version|v)\s*\Z', pre) and '.' in d)),
    ("SHAPE_URL_OR_DOI",
     lambda d, pre, post: 'zenodo' in pre.lower() or 'doi' in pre.lower()
                          or 'http' in pre.lower() or 'arxiv' in pre.lower()),
    ("SHAPE_EXPONENT_OR_TOLERANCE",
     lambda d, pre, post: bool(re.search(r'\d[eE][-+]?\Z', pre))
                          or bool(re.match(r'[eE][-+]?\d', post))
                          or bool(re.search(r'10\^[-+]?\Z', pre))),
    # ---- reference-like ------------------------------------------------
    ("SHAPE_SECTION_OR_THEOREM_REF",
     lambda d, pre, post: bool(re.search(
         r'(?i)(?:§|sec(?:tion)?\.?|ch(?:apter)?\.?|thm\.?|theorem|lemma|'
         r'lem\.?|eq(?:uation)?\.?|table|tab\.?|fig(?:ure)?\.?|app(?:endix)?\.?|'
         r'step|stage|rule|clause|item|part|leg|round|phase|tier|axiom|'
         r'premise|remark|prop(?:osition)?\.?|cor(?:ollary)?\.?|note|row|'
         r'footnote|point|def(?:inition)?\.?)\s*[.:#]?\s*\Z', pre))),
    ("SHAPE_PAPER_REF",
     lambda d, pre, post: bool(re.search(r'(?i)paper\s*\Z', pre))),
    ("SHAPE_CITATION_YEAR",
     lambda d, pre, post: bool(re.fullmatch(r'(1[89]|20)\d{2}', d))),
    # ---- notation ------------------------------------------------------
    ("SHAPE_IDENT_INTERNAL",
     lambda d, pre, post: bool(re.search(r'[A-Za-z_]\Z', pre))
                          or bool(re.match(r'[A-Za-z_]', post))),
    ("SHAPE_MATH_SUB_SUPERSCRIPT",
     lambda d, pre, post: bool(re.search(r'[_^]\s*\Z', pre))
                          or bool(re.match(r'\s*[_^]', post))),
    ("SHAPE_DIMENSION_PRODUCT",
     lambda d, pre, post: bool(re.search(r'\d\s*[x×*]\s*\Z', pre))
                          or bool(re.match(r'\s*[x×*]\s*\d', post))),
    ("SHAPE_ORDINAL",
     lambda d, pre, post: bool(re.match(r'(st|nd|rd|th)\b', post))),
    # ---- quantities ----------------------------------------------------
    ("SHAPE_UNIT_QUANTITY",
     lambda d, pre, post: bool(re.match(r'\s*(?:' + UNIT_WORDS + r')', post))),
    ("SHAPE_RATIO_OR_FRACTION",
     lambda d, pre, post: bool(re.search(r'\d\s*/\s*\Z', pre))
                          or bool(re.match(r'\s*/\s*\d', post))),
    ("SHAPE_DOTTED_VERSION_FRAGMENT",
     lambda d, pre, post: bool(re.search(r'\.\Z', pre))),
    # ---- syntactic position in an expression ---------------------------
    # These two are the largest buckets and they are the ones a reader should
    # be most sceptical of. `C_total = 61` lands in MATH_RELATION and so would
    # a capacity number that had gone stale. They are partitioned out because
    # the brief for this tool names `n = 2` as a case not worth chasing, not
    # because a numeral after an equals sign is safe.
    ("SHAPE_MATH_RELATION",
     lambda d, pre, post: bool(re.search(
         r'(?:->|<=|>=|!=|[=<>\u2264\u2265\u2260+\-*/~\u2248\u00b1])\s*\Z', pre))),
    ("SHAPE_ARG_OR_LIST_ELEMENT",
     lambda d, pre, post: bool(re.search(r'[\(\[\{,;|]\s*\Z', pre))),
    # ---- residual: a human reads these ---------------------------------
]
UNMATCHED = "UNMATCHED"

NUMERAL = re.compile(r'\d+(?:\.\d+)*')
CTX_PRE, CTX_POST = 24, 16


def bucket_of(digits, pre, post):
    for nm, pred in SHAPES:
        try:
            if pred(digits, pre, post):
                return nm
        except Exception:                       # a predicate must never decide
            continue                            # the population by crashing
    return UNMATCHED


# ---------------------------------------------------------------------------
# string-valued expressions
# ---------------------------------------------------------------------------
def string_parts(node, depth=0):
    """(literal_segments, n_interp, is_string_expr).

    literal_segments is a list of (text, node) -- source literal text that ends
    up in the string. n_interp counts interpolated expressions. is_string_expr
    is False only for values that are provably not strings (numbers, bools,
    None, dicts, lists, sets, tuples, comparisons).

    A Name / Call / Attribute / Subscript is treated as string-valued with ZERO
    literal segments: whatever it is, it contributes no source-literal numeral.
    That is the honest answer without inferring a type.
    """
    if depth > 12:
        return [], 1, True
    if isinstance(node, ast.Constant):
        if isinstance(node.value, str):
            return [(node.value, node)], 0, True
        return [], 0, False
    if isinstance(node, ast.JoinedStr):
        segs, interp = [], 0
        for p in node.values:
            if isinstance(p, ast.Constant) and isinstance(p.value, str):
                segs.append((p.value, node))
            elif isinstance(p, ast.FormattedValue):
                interp += 1
                if p.format_spec is not None:
                    s2, _i2, _ = string_parts(p.format_spec, depth + 1)
                    # a format spec is not record prose; its literals are dropped
                    del s2
            else:
                interp += 1
        return segs, interp, True
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        ls, li, lb = string_parts(node.left, depth + 1)
        rs, ri, rb = string_parts(node.right, depth + 1)
        if not (lb or rb):
            return [], 0, False
        return ls + rs, li + ri, True
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Mod):
        ls, li, lb = string_parts(node.left, depth + 1)
        if not lb:
            return [], 0, False
        n = len(node.right.elts) if isinstance(node.right, ast.Tuple) else 1
        return ls, li + n, True
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Mult):
        ls, li, lb = string_parts(node.left, depth + 1)
        rs, ri, rb = string_parts(node.right, depth + 1)
        if lb and not rb:
            return ls, li, True
        if rb and not lb:
            return rs, ri, True
        return [], 0, False
    if isinstance(node, ast.IfExp):
        bs, bi, bb = string_parts(node.body, depth + 1)
        os_, oi, ob = string_parts(node.orelse, depth + 1)
        if not (bb or ob):
            return [], 0, False
        return bs + os_, bi + oi, True
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
        if node.func.attr in ("format", "join", "replace", "strip", "rstrip",
                              "lstrip", "upper", "lower", "title"):
            ls, li, lb = string_parts(node.func.value, depth + 1)
            if not lb:
                return [], 1, True
            extra = len(node.args) + len(node.keywords) if node.func.attr in (
                "format", "join") else 0
            return ls, li + extra, True
        return [], 1, True
    if isinstance(node, (ast.Name, ast.Call, ast.Attribute, ast.Subscript,
                         ast.Await, ast.Starred)):
        return [], 1, True
    if isinstance(node, (ast.Dict, ast.List, ast.Set, ast.Tuple, ast.Compare,
                         ast.BoolOp, ast.UnaryOp, ast.ListComp, ast.DictComp,
                         ast.SetComp, ast.GeneratorExp, ast.Lambda)):
        return [], 0, False
    return [], 1, True


# ---------------------------------------------------------------------------
# locating the record a check returns
# ---------------------------------------------------------------------------
def own_nodes(fn):
    """Every node in fn's body EXCLUDING nested function/lambda bodies."""
    skip = set()
    for sub in ast.walk(fn):
        if sub is not fn and isinstance(sub, (ast.FunctionDef, ast.AsyncFunctionDef,
                                              ast.Lambda)):
            for x in ast.walk(sub):
                skip.add(id(x))
    return [n for n in ast.walk(fn) if id(n) not in skip]


def bind_call(call, callee):
    """(fieldname -> value_node, n_unbound). Positional arguments are bound to
    the callee's parameter names by position; keywords by name; **kwargs and
    *args at the call site are counted as unbound rather than guessed."""
    out, unbound = {}, 0
    pos = [a.arg for a in callee.args.posonlyargs] + [a.arg for a in callee.args.args]
    for i, a in enumerate(call.args):
        if isinstance(a, ast.Starred):
            unbound += 1
        elif i < len(pos):
            out[pos[i]] = a
        elif callee.args.vararg is not None:
            unbound += 1
        else:
            unbound += 1
    for kw in call.keywords:
        if kw.arg is None:
            unbound += 1
        else:
            out[kw.arg] = kw.value
    return out, unbound


class ModuleIndex(object):
    """Parses repo modules on demand and resolves a called NAME to the `def`
    that will actually run.

    Three hops are needed and all three are load-bearing here. The record
    builder in most modules is `_result`, which is (a) not defined in the
    calling module, (b) imported from `apf.apf_utils`, and (c) an ALIAS there
    (`_result = result`). Resolving only same-module `def`s reads 79.3% of the
    population and silently reports the rest as unreadable -- measured, not
    assumed.
    """

    def __init__(self, root):
        self.root = root
        self._ast = {}          # relpath -> (tree, ok)
        self._funcs = {}        # relpath -> {name: node}
        self._aliases = {}      # relpath -> {name: target_name}
        self._imports = {}      # relpath -> {local_name: (module_rel, orig_name)}
        self._stars = collections.defaultdict(list)   # relpath -> [module_rel]
        self._lines = {}        # relpath -> source lines, for numeral location

    def tree(self, rel):
        if rel in self._ast:
            return self._ast[rel]
        path = os.path.join(self.root, rel)
        try:
            t = ast.parse(open(path, encoding="utf-8").read())
        except Exception:
            t = None
        self._ast[rel] = t
        return t

    def source_lines(self, rel):
        if rel in self._lines:
            return self._lines[rel]
        try:
            v = open(os.path.join(self.root, rel), encoding="utf-8").read().split("\n")
        except Exception:
            v = None
        self._lines[rel] = v
        return v

    def _scan(self, rel):
        if rel in self._funcs:
            return
        self._funcs[rel], self._aliases[rel], self._imports[rel] = {}, {}, {}
        self._stars[rel] = []
        t = self.tree(rel)
        if t is None:
            return
        for node in ast.walk(t):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                self._funcs[rel].setdefault(node.name, node)
            elif isinstance(node, ast.Assign) and isinstance(node.value, ast.Name):
                for tg in node.targets:
                    if isinstance(tg, ast.Name):
                        self._aliases[rel].setdefault(tg.id, node.value.id)
            elif isinstance(node, ast.ImportFrom) and node.module is not None:
                # RELATIVE imports matter: apf/held_holonomy.py reaches its ten
                # record builders through `from ._held_holonomy_groups import`.
                # Requiring level == 0 left those ten checks unread.
                base = os.path.dirname(rel) if node.level else ""
                mrel = os.path.join(base, node.module.replace(".", "/") + ".py") \
                    if node.level else node.module.replace(".", "/") + ".py"
                mrel = mrel.replace(os.sep, "/")
                if not os.path.exists(os.path.join(self.root, mrel)):
                    mrel2 = mrel[:-3] + "/__init__.py"
                    mrel = mrel2 if os.path.exists(
                        os.path.join(self.root, mrel2)) else None
                if mrel:
                    for a in node.names:
                        if a.name == "*":
                            # `from ._held_holonomy_common import *` is how ten
                            # checks reach their record builder. Without this
                            # hop they read as unreadable returns.
                            self._stars[rel].append(mrel)
                        else:
                            self._imports[rel].setdefault(a.asname or a.name,
                                                          (mrel, a.name))

    def resolve(self, name, rel, _seen=None):
        """(node, defining_module_rel) or (None, None)."""
        _seen = _seen or set()
        if (name, rel) in _seen or len(_seen) > 8:
            return None, None
        _seen.add((name, rel))
        self._scan(rel)
        if name in self._funcs[rel]:
            return self._funcs[rel][name], rel
        if name in self._aliases[rel]:
            return self.resolve(self._aliases[rel][name], rel, _seen)
        if name in self._imports[rel]:
            mrel, orig = self._imports[rel][name]
            got = self.resolve(orig, mrel, _seen)
            if got[0] is not None:
                return got
        for mrel in self._stars[rel]:
            got = self.resolve(name, mrel, _seen)
            if got[0] is not None:
                return got
        return None, None


def class_params(cls):
    """A dataclass-style ClassDef read as a positional parameter list."""
    init = None
    for n in cls.body:
        if isinstance(n, ast.FunctionDef) and n.name == "__init__":
            init = n
    if init is not None:
        return init
    fields = [n.target.id for n in cls.body
              if isinstance(n, ast.AnnAssign) and isinstance(n.target, ast.Name)]
    fake = ast.parse("def _f(%s): pass" % ", ".join(fields or ["_x"])).body[0]
    return fake


def helper_param_to_key(callee):
    """param name -> record key, read off the callee's own returned Dict.

    `_ok(name, *, status, summary, ...)` returning `{'summary': summary, ...}`
    lets a positional/keyword binding be renamed to the key the record actually
    carries. When a helper cannot be read this way the parameter name is used
    and the field is marked so in the JSON.
    """
    m = {}
    for r in ast.walk(callee):
        if isinstance(r, ast.Return) and isinstance(r.value, ast.Dict):
            for k, v in zip(r.value.keys, r.value.values):
                if isinstance(k, ast.Constant) and isinstance(k.value, str) \
                        and isinstance(v, ast.Name):
                    m.setdefault(v.id, k.value)
    for a in ast.walk(callee):
        if isinstance(a, ast.Assign) and isinstance(a.value, ast.Dict):
            for k, v in zip(a.value.keys, a.value.values):
                if isinstance(k, ast.Constant) and isinstance(k.value, str) \
                        and isinstance(v, ast.Name):
                    m.setdefault(v.id, k.value)
    return m


def dict_fields(d):
    out = []
    for k, v in zip(d.keys, d.values):
        if isinstance(k, ast.Constant) and isinstance(k.value, str):
            out.append((k.value, v))
    return out


def record_fields(fn, idx, rel):
    """[(field, value_node, provenance)], status, detail.

    status: OK | NO_RETURN | UNRESOLVED_RETURN
    """
    nodes = own_nodes(fn)
    rets = [n for n in nodes if isinstance(n, ast.Return) and n.value is not None]
    if not rets:
        return [], "NO_RETURN", ""
    fields, unresolved = [], []
    for ri, r in enumerate(rets):
        v = r.value
        got = resolve_record_expr(v, nodes, idx, rel, ri, depth=0)
        if got is None:
            unresolved.append(describe_expr(v))
        else:
            fields.extend(got)
    if not fields and unresolved:
        return [], "UNRESOLVED_RETURN", "; ".join(sorted(set(unresolved))[:4])
    return fields, "OK", ("; ".join(sorted(set(unresolved))[:4]) if unresolved else "")


def describe_expr(v):
    if isinstance(v, ast.Call):
        f = v.func
        return "call:" + (f.id if isinstance(f, ast.Name) else getattr(f, "attr", "?"))
    return type(v).__name__


def resolve_record_expr(v, nodes, idx, rel, ri, depth):
    """Return [(field, node, provenance)] or None if the record cannot be read."""
    if depth > 3:
        return None
    if isinstance(v, ast.Dict):
        return [(k, n, "return-dict#%d" % ri, rel) for k, n in dict_fields(v)]
    if isinstance(v, ast.Name):
        # trace assignments of that name inside this function, plus later
        # subscript stores and .update({...}) calls on it
        out, seen = [], False
        for n in nodes:
            if isinstance(n, ast.Assign) and any(
                    isinstance(t, ast.Name) and t.id == v.id for t in n.targets):
                if isinstance(n.value, ast.Dict):
                    out.extend((k, x, "var:%s#%d" % (v.id, ri), rel)
                               for k, x in dict_fields(n.value))
                    seen = True
            if isinstance(n, ast.Assign):
                for t in n.targets:
                    if isinstance(t, ast.Subscript) and isinstance(t.value, ast.Name) \
                            and t.value.id == v.id and isinstance(t.slice, ast.Constant) \
                            and isinstance(t.slice.value, str):
                        out.append((t.slice.value, n.value,
                                    "store:%s#%d" % (v.id, ri), rel))
                        seen = True
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) \
                    and n.func.attr == "update" and isinstance(n.func.value, ast.Name) \
                    and n.func.value.id == v.id and n.args \
                    and isinstance(n.args[0], ast.Dict):
                out.extend((k, x, "update:%s#%d" % (v.id, ri), rel)
                           for k, x in dict_fields(n.args[0]))
                seen = True
        return out if seen else None
    if isinstance(v, ast.Call):
        if isinstance(v.func, ast.Name):
            cname = v.func.id
        elif isinstance(v.func, ast.Attribute):
            cname = v.func.attr
        else:
            return None
        callee, crel = idx.resolve(cname, rel)
        if callee is None:
            return None
        sig = class_params(callee) if isinstance(callee, ast.ClassDef) else callee
        bound, _unb = bind_call(v, sig)
        rename = ({} if isinstance(callee, ast.ClassDef)
                  else helper_param_to_key(callee))
        out = [(rename.get(p, p), node, "helper:%s#%d" % (cname, ri), rel)
               for p, node in bound.items()]
        if out:
            return out
        # A callee taking no arguments that builds the record itself -- the
        # `*_impl` idiom. Read its own returned dict, one hop.
        if not isinstance(callee, ast.ClassDef):
            for r2 in ast.walk(callee):
                if isinstance(r2, ast.Return) and r2.value is not None:
                    got = resolve_record_expr(r2.value, own_nodes(callee), idx,
                                              crel, ri, depth + 1)
                    if got:
                        return [(k, n, "helper-body:%s#%d" % (cname, ri), dm)
                                for k, n, _p, dm in got]
        return None
    return None


# ---------------------------------------------------------------------------
def locate_numeral_line(seg_text, start, digits, node, src_lines):
    """Best line for a numeral inside a (possibly implicitly concatenated,
    possibly multi-line) literal. Returns (lineno, exact:bool).

    A string literal in this corpus routinely spans thirty lines of implicit
    concatenation, and on Python 3.10 the parts of an f-string all carry the
    JoinedStr's own position. So the node's `lineno` is a range start, not a
    location. The line is recovered by searching the node's line span for the
    numeral's surrounding text, narrowing the window until the match is unique.
    A line that could not be pinned this way is printed with a leading `~` and
    carries `line_exact: false` in the JSON -- it is the node's first line, and
    the numeral is somewhere in [line, end_line].
    """
    lo = getattr(node, "lineno", 1)
    hi = getattr(node, "end_lineno", lo) or lo
    span = range(lo, min(hi, len(src_lines)) + 1)
    for back, fwd in ((10, 14), (6, 8), (3, 4)):
        window = seg_text[max(0, start - back):start + fwd]
        if not window.strip():
            continue
        found = [i for i in span if window in src_lines[i - 1]]
        if len(found) == 1:
            return found[0], True
    found = [i for i in span if digits in src_lines[i - 1]]
    if len(found) == 1:
        return found[0], True
    return lo, False


def main(argv):
    here = os.path.dirname(os.path.abspath(__file__))
    root = os.path.dirname(here)
    out_json = argv[argv.index("--json") + 1] if "--json" in argv else \
        os.path.join(here, "claim_census.json")
    out_report = argv[argv.index("--report") + 1] if "--report" in argv else None
    show_all = "--all" in argv
    only_field = argv[argv.index("--field") + 1] if "--field" in argv else None

    sys.path.insert(0, root)
    from apf import bank
    bank._load()
    reg = bank.REGISTRY

    # ---- population, derived from the registry itself ---------------------
    n_keys = len(reg)
    bare = sum(1 for k in reg if not k.startswith("check_"))
    by_site = collections.defaultdict(list)     # (relpath, co_name, firstlineno)
    by_obj = set()
    for k, f in reg.items():
        c = getattr(f, "__code__", None)
        if c is None:
            by_site[("<no __code__>", str(k), 0)].append(k)
            continue
        rel = os.path.relpath(c.co_filename, root).replace(os.sep, "/")
        by_site[(rel, c.co_name, c.co_firstlineno)].append(k)
        by_obj.add((rel, getattr(f, "__name__", c.co_name), c.co_firstlineno))
    population = len(by_site)
    # Both key spellings, counted rather than assumed.
    both_spellings = bare_only = prefixed_only = 0
    for site, ks in by_site.items():
        has_bare = any(not k.startswith("check_") for k in ks)
        has_pref = any(k.startswith("check_") for k in ks)
        if has_bare and has_pref:
            both_spellings += 1
        elif has_bare:
            bare_only += 1
        else:
            prefixed_only += 1

    # ---- parse + locate ----------------------------------------------------
    files = collections.defaultdict(list)
    for site, keys in by_site.items():
        files[site[0]].append((site, keys))

    parse_failed, not_located = [], []
    analysed, no_return, unresolved_return = [], [], []
    rows = []
    MI = ModuleIndex(root)
    # The field population, counted as the walk runs -- NOT derived afterwards
    # from the hit list. Deriving it from hits would report only fields that
    # happened to contain a numeral and silently omit the denominator, which is
    # the whole failure this tool's coverage discipline exists to avoid.
    field_kinds = collections.Counter()      # LITERAL / MIXED / COMPUTED
    field_names = collections.Counter()      # every string-valued field name
    fields_with_numeral = collections.Counter()
    nonstring_fields = collections.Counter()

    for rel, want in sorted(files.items()):
        path = os.path.join(root, rel)
        try:
            src = open(path, encoding="utf-8").read()
            tree = ast.parse(src)
        except Exception as e:
            for site, keys in want:
                parse_failed.append((site, keys, "%s: %s" % (type(e).__name__, e)))
            continue
        src_lines = src.split("\n")
        modfuncs = {}
        bylineno = collections.defaultdict(list)
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                modfuncs.setdefault(node.name, node)
                bylineno[(node.name, node.lineno)].append(node)
                for d in node.decorator_list:
                    bylineno[(node.name, d.lineno)].append(node)
        for site, keys in want:
            _rel, cname, ln = site
            cands = bylineno.get((cname, ln)) or bylineno.get((cname, ln + 1))
            if not cands:
                cands = [n for n in modfuncs.values() if n.name == cname]
                if len(cands) != 1:
                    not_located.append((site, keys))
                    continue
            fn = cands[0]
            fields, status, detail = record_fields(fn, MI, rel)
            if status == "NO_RETURN":
                no_return.append((site, keys))
                continue
            if status == "UNRESOLVED_RETURN":
                unresolved_return.append((site, keys, detail))
                continue
            analysed.append(site)
            for fname, vnode, prov, defmod in fields:
                if only_field and fname != only_field:
                    continue
                segs, interp, is_str = string_parts(vnode)
                if not is_str:
                    nonstring_fields[fname] += 1
                    continue
                kind = ("MIXED" if (segs and interp) else
                        "LITERAL" if segs else "COMPUTED")
                field_kinds[kind] += 1
                field_names[fname] += 1
                if any(NUMERAL.search(t) for t, _ in segs):
                    fields_with_numeral[fname] += 1
                for text, snode in segs:
                    for m in NUMERAL.finditer(text):
                        d = m.group(0)
                        pre = text[max(0, m.start() - CTX_PRE):m.start()]
                        post = text[m.end():m.end() + CTX_POST]
                        dlines = (src_lines if defmod == rel else
                                  (MI.source_lines(defmod) or src_lines))
                        lineno, exact = locate_numeral_line(text, m.start(), d,
                                                            snode, dlines)
                        rows.append(dict(
                            module=rel, check=cname, keys=sorted(keys),
                            field_module=defmod,
                            field=fname, provenance=prov, field_kind=kind,
                            digits=d, pre=pre, post=post,
                            context=(pre + "[" + d + "]" + post).replace("\n", " "),
                            line=lineno, line_exact=exact,
                            bucket=bucket_of(d, pre, post)))

    coverage = len(analysed)
    frac = 100.0 * coverage / population if population else 0.0
    raw = len(rows)
    unmatched = [r for r in rows if r["bucket"] == UNMATCHED]
    buckets = collections.Counter(r["bucket"] for r in rows)

    L = []
    P = L.append
    P("APF CLAIM CENSUS -- literal numerals in the prose fields of registered checks")
    P("A REPORTING TOOL. It asserts a numeral is a source literal. It asserts")
    P("NOTHING about whether that numeral is correct, current, or a defect.")
    P("")
    P("THE FOUR NUMBERS, kept separate on purpose")
    P("  population          %6d  distinct check `def` sites in bank.REGISTRY"
      % population)
    P("  coverage            %6d  of %d = %.2f%% -- sites whose returned record"
      % (coverage, population, frac))
    P("                              was located and enumerated")
    P("  raw hits            %6d  literal-numeral occurrences in string-valued fields"
      % raw)
    P("  after partitioning  %6d  occurrences in the residual UNMATCHED bucket"
      % len(unmatched))
    P("")
    P("registry keys %d  (bare-name %d / check_-prefixed %d)"
      % (n_keys, bare, n_keys - bare))
    P("  %d `def` sites are registered under BOTH spellings; %d under a bare name"
      % (both_spellings, bare_only))
    P("  only and %d under a check_-prefixed key only. The population above is"
      % (prefixed_only))
    P("  taken from the registry's VALUES, so no spelling can hide a check from")
    P("  it -- a by-name lookup against one spelling reports a false absence,")
    P("  and that defect cost a census in this corpus its figure on 2026-08-06.")
    P("distinct function objects %d   distinct `def` sites %d"
      % (len(by_obj), population))
    P("  Three different denominators. Keys exceed function objects because a")
    P("  factory registers one closure under several names; function objects")
    P("  exceed `def` sites because those closures share one code object.")
    P("")
    P("COVERAGE -- what could not be analysed, by name")
    P("  parse failed          %4d" % len(parse_failed))
    P("  def not located       %4d" % len(not_located))
    P("  no return statement   %4d" % len(no_return))
    P("  return not a record   %4d" % len(unresolved_return))
    for label, lst in (("PARSE FAILED", parse_failed),
                       ("DEF NOT LOCATED", not_located)):
        if lst:
            P("  -- %s --" % label)
            for item in lst:
                P("     %s :: %s" % (item[0][0], item[0][1]))
    if no_return:
        P("  -- NO RETURN STATEMENT --")
        for site, keys in sorted(no_return):
            P("     %-46s %s:%d" % (site[1], site[0], site[2]))
    if unresolved_return:
        P("  -- RETURN EXPRESSION NOT READABLE AS A RECORD --")
        P("     (the record is built somewhere this tool does not follow;")
        P("      these are NOT clean, they are UNREAD)")
        for site, keys, detail in sorted(unresolved_return):
            P("     %-46s %s:%d   [%s]" % (site[1], site[0], site[2], detail))
    P("")
    P("RECORD FIELDS, BY HOW THE VALUE IS BUILT")
    P("  Unit: one field per check per return site. A field appears once for")
    P("  each way the record can be returned, so a check with two return sites")
    P("  contributes its fields twice. That is instances, not lines.")
    tot_f = sum(field_kinds.values()) or 1
    P("  record fields that could carry a source-literal string  %6d"
      % tot_f)
    P("  (across %d analysed checks)" % coverage)
    for k in ("LITERAL", "MIXED", "COMPUTED"):
        P("    %-9s %6d  %5.1f%%" % (k, field_kinds.get(k, 0),
                                     100.0 * field_kinds.get(k, 0) / tot_f))
    P("  LITERAL  = built only from source literals, nothing interpolated")
    P("  MIXED    = literal text plus at least one interpolated expression")
    P("  COMPUTED = no literal segment at all; the value is a bare name, a call")
    P("             or a subscript. Its runtime type is unknown to this tool and")
    P("             is NOT claimed to be a string; it is counted here because it")
    P("             is a field that could have carried one, and it contributes")
    P("             no source literal by construction.")
    P("  fields carrying at least one literal numeral  %6d  (%.1f%% of the above)"
      % (sum(fields_with_numeral.values()),
         100.0 * sum(fields_with_numeral.values()) / tot_f))
    P("  non-string record fields skipped             %6d"
      % sum(nonstring_fields.values()))
    P("")
    P("  field name                            fields   of which carry a numeral")
    for nm, c in field_names.most_common(30):
        P("    %-32s %8d %14d" % (nm, c, fields_with_numeral.get(nm, 0)))
    if len(field_names) > 30:
        P("    ... and %d more field names (see JSON)" % (len(field_names) - 30))
    P("")
    P("PARTITION BY SHAPE  (ordered, disjoint; first match wins; counts sum to raw)")
    P("  Membership is a syntactic fact. It is NOT a claim of legitimacy, and")
    P("  UNMATCHED is NOT a claim of defect.")
    for nm, c in buckets.most_common():
        P("  %-30s %6d  %5.1f%%" % (nm, c, 100.0 * c / (raw or 1)))
    P("  %-30s %6d" % ("TOTAL", sum(buckets.values())))
    P("")
    P("  READ THE BUCKET DEFINITIONS BEFORE TRUSTING THE RESIDUAL. The two")
    P("  largest partitions -- SHAPE_MATH_RELATION (a numeral after =, <, >, +,")
    P("  -, *, /) and SHAPE_ARG_OR_LIST_ELEMENT (a numeral after ( [ { , ; |) --")
    P("  are positional, not semantic. `C_total = 61` lands in the first and so")
    P("  would a capacity number that had gone stale. They are partitioned out")
    P("  because a reader asked for the residual, not because a numeral after an")
    P("  equals sign is safe. If the residual comes up empty, read those two.")
    P("  Run with --all to print every hit including the shape-matched ones.")
    P("")
    n_exact = sum(1 for r in rows if r["line_exact"])
    P("  line numbers: %d of %d located exactly (%.1f%%). The rest are printed"
      % (n_exact, raw, 100.0 * n_exact / (raw or 1)))
    P("  with a leading `~` and are the first line of a multi-line literal; the")
    P("  numeral is somewhere inside that literal. This is not a defect in the")
    P("  source -- string literals here routinely span thirty lines of implicit")
    P("  concatenation, and on Python 3.10 every part of an f-string carries the")
    P("  f-string's own position.")
    P("")
    P("STRATIFICATION -- the reading worth doing first")
    P("  A literal numeral in a MIXED field sits beside interpolated values:")
    P("  the author interpolated at that site and not at that spot. This is the")
    P("  shape of the recorded '320 conjugates' instance. Still not a verdict.")
    x = collections.Counter((r["field_kind"], r["bucket"] == UNMATCHED) for r in rows)
    P("             UNMATCHED   shape-matched")
    for k in ("MIXED", "LITERAL", "COMPUTED"):
        P("  %-9s  %8d   %8d" % (k, x.get((k, True), 0), x.get((k, False), 0)))
    P("")

    def dump(title, sel):
        P("=" * 78)
        P("%s -- %d occurrences, %d distinct (check, field, digits)"
          % (title, len(sel), len({(r["check"], r["field"], r["digits"]) for r in sel})))
        P("=" * 78)
        by_mod = collections.defaultdict(list)
        for r in sel:
            by_mod[r["module"]].append(r)
        for mod in sorted(by_mod):
            P("")
            P("--- %s  (%d)" % (mod, len(by_mod[mod])))
            for r in sorted(by_mod[mod], key=lambda z: (z["check"], z["line"])):
                mark = "" if r["line_exact"] else "~"
                P("  %s%-6d %-9s %-16s %s" % (mark, r["line"], r["field_kind"],
                                              r["field"][:16], r["check"]))
                P("          %s" % r["context"][:150])

    dump("UNMATCHED BY ANY SHAPE -- a human reads these", unmatched)
    mixed_unmatched = [r for r in unmatched if r["field_kind"] == "MIXED"]
    if mixed_unmatched:
        dump("SUBSET: UNMATCHED and in a MIXED field -- read these first",
             mixed_unmatched)
    if show_all:
        dump("ALL HITS INCLUDING SHAPE-MATCHED", rows)

    P("")
    P("This tool has not claimed that any numeral above is wrong. It has claimed")
    P("that each one is written in the source and is not recomputed when the")
    P("check runs. Which of them matter is a human read, one numeral at a time.")

    text = "\n".join(L)
    print(text)

    payload = dict(
        tool="claim_census",
        asserts=["numeral occurs as a source literal in a string-valued field "
                 "of a registered check's returned record"],
        does_not_assert=["that any reported numeral is wrong, stale, or a defect",
                         "that an unreported check is clean",
                         "anything about leg vacuity or whether a leg can fail"],
        population=population, coverage=coverage, coverage_pct=round(frac, 2),
        raw_hits=raw, unmatched_hits=len(unmatched),
        registry_keys=n_keys, bare_name_keys=bare,
        sites_registered_under_both_spellings=both_spellings,
        sites_bare_name_only=bare_only, sites_prefixed_only=prefixed_only,
        distinct_function_objects=len(by_obj),
        buckets=dict(buckets), field_kinds=dict(field_kinds),
        field_names=dict(field_names),
        fields_with_numeral=dict(fields_with_numeral),
        nonstring_fields=dict(nonstring_fields),
        not_analysed=dict(
            parse_failed=[dict(module=s[0], check=s[1], line=s[2], keys=k, err=e)
                          for s, k, e in parse_failed],
            not_located=[dict(module=s[0], check=s[1], line=s[2], keys=k)
                         for s, k in not_located],
            no_return=[dict(module=s[0], check=s[1], line=s[2], keys=k)
                       for s, k in no_return],
            unresolved_return=[dict(module=s[0], check=s[1], line=s[2], keys=k,
                                    detail=d) for s, k, d in unresolved_return]),
        hits=rows)
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=1, sort_keys=True)
    print("\nwrote %s  (sha256 %s)"
          % (out_json, hashlib.sha256(
              open(out_json, "rb").read()).hexdigest()[:16]))
    if out_report:
        with open(out_report, "w", encoding="utf-8") as f:
            f.write(text + "\n")
        print("wrote %s" % out_report)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
