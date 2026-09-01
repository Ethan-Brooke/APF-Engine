#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Grade-token census -- a REPORTING TOOL. It prints. It gates nothing.

AUTHORISATION
    GT12@2026-08-30, ruled 2026-08-31 in
    "Reference - DECISION - The Grade-Token Docket (2026-08-31).md" section 2:
    option (a) then (b) -- disposition batches first, reporting tool second,
    ratchet check not yet.  That ruling IS the Corpus-Hygiene-fence ruling for
    this tool, in the Working Rule 17 shape: it prints, nothing gates on it,
    nothing has to audit it.  The registered ratchet check remains
    UNAUTHORISED until a separate ruling is made.

WHAT THIS TOOL IS NOT
    It is not a validator, not a gate, not a registered check, and not a
    tripwire.  It returns exit status 0 on every successful run whatever it
    measures.  It makes no claim about whether any site is correct, and it
    rules on nothing: the partition below implements rulings that already
    exist and cites each one at the bucket that applies it.

USAGE
    py -3 scripts/grade_token_census.py                  # report to stdout
    py -3 scripts/grade_token_census.py --json out.json  # + machine record
    py -3 scripts/grade_token_census.py --baseline b.json    # per-bucket delta
    py -3 scripts/grade_token_census.py --root apf --sites-for TOKEN

Stdlib only.  Run from the repository root.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import re
import sys
from collections import Counter, defaultdict

TOOL_NAME = "grade_token_census"
TOOL_VERSION = "1.0"

# ---------------------------------------------------------------------------
# DECLARED SETS.  Every set below is quoted from a dated ruling or is an
# explicit enumeration stated in this file's own printed header.  Nothing here
# is inferred from the tree, and nothing here mints a token
# (GT11@2026-08-30 = E2R2@2026-08-30: no seat mints a grade token).
# ---------------------------------------------------------------------------

# GT1@2026-08-30 option (b): the canonical set.  The foundation grades, the
# ruled P_structural_* sub-grades, and P_math (declared by that ruling; the
# declaration records existing usage and mints nothing).  The set's size is a
# property of the tuples below, printed at run time and stated in no comment.
CANONICAL_FOUNDATION = ("AXIOM", "POSTULATE", "P", "C", "RED_TEAM")
CANONICAL_SUBGRADES = (
    "P_structural_seam",
    "P_structural_partial",
    "P_structural_exhaustive",
    "P_structural_instrument",
    "P_structural_reading",
    "P_structural_convention",
)
CANONICAL_PMATH = ("P_math",)
CANONICAL = tuple(CANONICAL_FOUNDATION + CANONICAL_SUBGRADES + CANONICAL_PMATH)
CANONICAL_SET = frozenset(CANONICAL)

# GT9@2026-08-30 option (a): an explicit RESERVED set, EXCLUDED from validation
# rather than validated -- the bank's own error paths.
RESERVED_GT9 = frozenset({"FAIL", "ERROR"})

# An explicit enumeration of run-outcome strings, used ONLY to separate the
# `status` field's run-outcome population from its grade-shaped one.  This is a
# stated enumeration, not a shape test: a string is a run outcome here because
# it is listed here, and for no other reason.  Working Rule 17 is the reason it
# is enumerated rather than inferred.
RUN_OUTCOME_ENUM = frozenset({
    "PASS", "FAIL", "OK", "ok", "SKIP", "SKIPPED", "ERROR", "PENDING",
    "CLOSED", "CONSISTENT", "UNKNOWN", "NA", "N/A", "TRUE", "FALSE", "",
})

# GT5@2026-08-30 option (a): ` | ` (spaced pipe) is reserved for a NAMED PREMISE
# only, `<base> | R_NAME [+ R_NAME...]`, premise names UNDERSCORED.
RIDER_SEPARATOR = " | "
RIDER_PREMISE_JOINER = " + "
RIDER_PREMISE_RE = re.compile(r"^R[A-Z0-9_]*$")

# GT6@2026-08-30 option (a): the P_structural_* family is the ruled sub-grades
# EXACTLY; membership is by ruling, never by prefix.
SUBGRADE_PREFIX = "P_structural_"

# GT2@2026-08-30 / GT3@2026-08-30(c): brackets carry no information on read;
# `[X]` and `X` are the same token, and new bracketed spellings in fields are
# defects.  GT4@2026-08-30(a): tokens are case-sensitive, uppercase canonical.
BRACKET_RE = re.compile(r"^\[(?P<inner>.*)\]$", re.DOTALL)

# The named disposition populations GT2 / GT3 / GT4 put in the batches.  Names
# only; every count beside them is computed at run time.
DISPOSITION_TOKENS = (
    ("P_structural, bare or bracketed -- GT2 batch", ("P_structural", "[P_structural]")),
    ("[P_math] bracketed -- GT3 stray", ("[P_math]",)),
    ("[P] bracketed -- GT3 stray", ("[P]",)),
    ("axiom lowercase -- GT4 stray", ("axiom",)),
)

# Grade-bearing field names.  An explicit enumeration; a field-name census
# cannot see a dialect nobody named, which is this tool's stated limitation
# below and the reason for the token-first adjunct in section 8.
FIELD_EPISTEMIC = ("epistemic", "epistemic_tag")
FIELD_STATUS = ("status",)
FIELD_OTHER_GRADE = ("grade", "registry_status", "toy_grade", "phys_grade")
GRADE_FIELDS = tuple(FIELD_EPISTEMIC + FIELD_STATUS + FIELD_OTHER_GRADE)
GRADE_FIELD_SET = frozenset(GRADE_FIELDS)

FIELD_GROUPS = (
    ("epistemic-family", FIELD_EPISTEMIC),
    ("status", FIELD_STATUS),
    ("other-grade", FIELD_OTHER_GRADE),
)

# Reproduction of the grade-shape filter stated in
# `RETURN_E2_retake_2026-08-30.md` section 1 (its tightened form), carried so
# the GT7@2026-08-30(c) `status` figure of record is comparable rather than
# re-judged here.  It is quoted, not invented.
E2_TIGHT_SHAPE_RE = re.compile(r"^\[?(P|C)([_|+\] ]|$)")
E2_TIGHT_EXCLUDE = frozenset({"PASS", "FAIL", "ok", "OK", "SKIP", "ERROR", ""})
E2_TIGHT_BARE = frozenset({"P", "C", "AXIOM", "POSTULATE", "RED_TEAM"})

# Bucket names, in report order.
BUCKETS = (
    "EXACT",
    "NORMALISABLE_ALIAS",
    "RULED_RIDER_FORM",
    "RESERVED_GT9",
    "RUN_OUTCOME_ENUM",
    "LONG_TAIL_UNDECLARED",
    "MALFORMED",
)

SYNTAX_DIALECTS = (
    ("call_keyword", "a call keyword argument, f(epistemic=...)"),
    ("call_positional_signature", "a call positional arg resolved against the callee's own def signature"),
    ("dataclass_positional", "a positional arg resolved against a class's annotated field order"),
    ("dict_value", "a dict-literal entry keyed 'epistemic'/'status'/... at any nesting depth"),
    ("assign", "a bare assignment, status = '...'"),
    ("subscript_assign", "a subscript assignment on a built record, res['epistemic'] = '...'"),
    ("annassign_default", "an annotated class or module field default, grade: str = '...'"),
    ("param_default", "a parameter default, def f(epistemic='...')"),
    ("get_default", "a .get()/.setdefault() default, d.get('epistemic', '...')"),
)

RESOLUTIONS = (
    ("literal", "a string constant (adjacent literals are joined at parse time)"),
    ("concat_literal", "a + chain of string constants, and of names already resolved to strings"),
    ("module_constant", "a NAME = <string expression> in the same file, resolved by name"),
    ("ifexp_true_branch", "the true branch of a conditional; reported apart, never folded in (GT8)"),
    ("unresolved", "anything else -- recorded, never guessed"),
)


# ---------------------------------------------------------------------------
# Normalisation and classification
# ---------------------------------------------------------------------------

def strip_brackets(value):
    """GT3@2026-08-30(c): `[X]` and `X` are the same token on read."""
    m = BRACKET_RE.match(value.strip())
    if m:
        return m.group("inner").strip(), True
    return value.strip(), False


def classify(value):
    """Return (bucket, reason, base).

    Every branch cites the ruling it implements.  No branch decides anything
    that is not already ruled; anything a ruling does not reach lands in
    LONG_TAIL_UNDECLARED or MALFORMED with its reason named.
    """
    raw = value
    if raw in RESERVED_GT9:
        return "RESERVED_GT9", "bank error path, excluded from validation (GT9)", raw
    if raw in RUN_OUTCOME_ENUM:
        return "RUN_OUTCOME_ENUM", "listed in this tool's stated run-outcome enumeration", raw

    inner, was_bracketed = strip_brackets(raw)

    # Rider form (GT5): base, spaced pipe, underscored premise names.
    if RIDER_SEPARATOR in inner:
        base, _, rider = inner.partition(RIDER_SEPARATOR)
        base = base.strip()
        premises = [p.strip() for p in rider.split(RIDER_PREMISE_JOINER)]
        base_ok = base in CANONICAL_SET
        premises_ok = bool(premises) and all(RIDER_PREMISE_RE.match(p) for p in premises)
        if base_ok and premises_ok and not was_bracketed:
            return "RULED_RIDER_FORM", "conforms to GT5 <base> | R_NAME [+ R_NAME]", base
        if base_ok and premises_ok and was_bracketed:
            return "MALFORMED", "GT5 rider form inside brackets (GT3 forbids bracketed fields)", base
        if base_ok:
            return ("MALFORMED",
                    "GT5 separator with a non-conforming rider (branch tag, hyphenated or sentence premise)",
                    base)
        return "LONG_TAIL_UNDECLARED", "GT5 separator over an undeclared base", base

    # Other separator spellings the mapping measured: bare pipe, bare plus,
    # spaced plus at top level.  GT5 rules one separator and one relation.
    if "|" in inner or "+" in inner:
        head = re.split(r"[|+]", inner, maxsplit=1)[0].strip()
        if head in CANONICAL_SET:
            return "MALFORMED", "composite in a separator spelling GT5 does not admit", head
        return "LONG_TAIL_UNDECLARED", "composite over an undeclared base", head

    if inner in CANONICAL_SET:
        if not was_bracketed and inner == raw:
            return "EXACT", "verbatim canonical token (GT1)", inner
        return "NORMALISABLE_ALIAS", "canonical token in a bracketed spelling (GT2/GT3)", inner

    # Case: GT4 rules tokens case-sensitive with uppercase canonical, so a case
    # variant is an alias to be dispositioned, not a conforming token.
    for canon in CANONICAL:
        if inner.lower() == canon.lower():
            return "NORMALISABLE_ALIAS", "canonical token in a case variant (GT4)", canon

    # GT6: membership in the P_structural_* family is by ruling, never prefix.
    if inner == "P_structural":
        return "MALFORMED", "the bare base the 2026-06-22 split retired (GT2 batch)", inner
    if inner.startswith(SUBGRADE_PREFIX):
        return ("MALFORMED",
                "P_structural_ prefix on a token outside the ruled sub-grades (GT6)", inner)

    # Sentence-valued, contract-string and other non-identifier grades.
    if not re.match(r"^[A-Za-z][A-Za-z0-9_.-]*$", inner):
        return ("MALFORMED",
                "not an identifier-shaped token (sentence, contract string or prose in a grade field)",
                inner)

    if was_bracketed:
        return ("MALFORMED",
                "bracketed spelling of an undeclared token (GT3 forbids; the base needs a ruling first)",
                inner)

    return "LONG_TAIL_UNDECLARED", "well-formed token with no declaration (GT1 long tail)", inner


# ---------------------------------------------------------------------------
# AST extraction
# ---------------------------------------------------------------------------

class Site(object):
    __slots__ = ("path", "line", "field", "dialect", "resolution", "value", "context")

    def __init__(self, path, line, field, dialect, resolution, value, context):
        self.path = path
        self.line = line
        self.field = field
        self.dialect = dialect
        self.resolution = resolution
        self.value = value
        self.context = context

    def as_dict(self):
        return {
            "path": self.path, "line": self.line, "field": self.field,
            "dialect": self.dialect, "resolution": self.resolution,
            "value": self.value, "context": self.context,
        }


def const_str(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    return None


def concat_str(node, names=None):
    """`'a' + 'b'`, chains of them, and chains whose operands are names already
    resolved to strings.  The declared-constant idiom the corpus treats as good
    practice writes its grade as `BASE + SEPARATOR + PREMISE` over three
    module-level names, so a resolver that folds only literals cannot read the
    grades most carefully declared."""

    def one(sub):
        text = const_str(sub)
        if text is not None:
            return text
        if names is not None and isinstance(sub, ast.Name):
            return names.get(sub.id)
        return concat_str(sub, names)

    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        left = one(node.left)
        right = one(node.right)
        if left is not None and right is not None:
            return left + right
    return None


def subscript_key(tgt):
    """The string key of `x['k']`, across the ast shapes Python has used."""
    sl = tgt.slice
    if hasattr(ast, "Index") and isinstance(sl, getattr(ast, "Index")):
        sl = sl.value
    return const_str(sl)


class ModuleIndex(object):
    """The module-level tables the resolvers need: string constants, def
    signatures, and annotated class field orders."""

    def __init__(self, tree):
        self.constants = {}
        self.rebound_names = set()
        self.signatures = {}
        self.class_fields = {}
        self._index(tree)

    def _index(self, tree):
        self._index_constants(tree)
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                args = node.args
                names = [a.arg for a in list(args.posonlyargs) + list(args.args)]
                self.signatures.setdefault(node.name, names)
            elif isinstance(node, ast.ClassDef):
                fields = [b.target.id for b in node.body
                          if isinstance(b, ast.AnnAssign) and isinstance(b.target, ast.Name)]
                if fields:
                    self.class_fields.setdefault(node.name, fields)

    def _index_constants(self, tree):
        """Every `NAME = <string expression>` anywhere in the file, resolved to a
        fixed point so that a name built from other names resolves too.

        A name that binds to more than one distinct string in the file is
        AMBIGUOUS: it is recorded in `rebound_names` and bound to nothing, so a
        site reading it resolves as unresolved.  Picking one of two bindings
        would be guessing, and the direction of a guess is unknowable from here.
        """
        pending = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for tgt in node.targets:
                    if isinstance(tgt, ast.Name):
                        pending.append((tgt.id, node.value))

        candidates = defaultdict(set)
        for name, value in pending:
            text = const_str(value)
            if text is not None:
                candidates[name].add(text)
        self._commit(candidates)

        changed = True
        while changed:
            changed = False
            grown = defaultdict(set)
            for name, value in pending:
                if name in self.constants or name in self.rebound_names:
                    continue
                text = concat_str(value, self.constants)
                if text is not None:
                    grown[name].add(text)
            if grown:
                before = len(self.constants) + len(self.rebound_names)
                self._commit(grown)
                changed = (len(self.constants) + len(self.rebound_names)) != before

    def _commit(self, candidates):
        for name, values in candidates.items():
            if len(values) == 1:
                self.constants[name] = next(iter(values))
            else:
                self.rebound_names.add(name)
                self.constants.pop(name, None)

    def resolve(self, node):
        """Return (resolution, value_or_None)."""
        val = const_str(node)
        if val is not None:
            return "literal", val
        val = concat_str(node, self.constants)
        if val is not None:
            return "concat_literal", val
        if isinstance(node, ast.Name) and node.id in self.constants:
            return "module_constant", self.constants[node.id]
        if isinstance(node, ast.IfExp):
            branch = const_str(node.body)
            if branch is None:
                branch = concat_str(node.body)
            if branch is None and isinstance(node.body, ast.Name):
                branch = self.constants.get(node.body.id)
            return "ifexp_true_branch", branch
        return "unresolved", None


def callee_name(func):
    if isinstance(func, ast.Name):
        return func.id
    if isinstance(func, ast.Attribute):
        return func.attr
    return None


def snippet(node):
    try:
        text = ast.unparse(node)
    except Exception:
        return ""
    return " ".join(text.split())[:160]


def collect_sites(rel, index, tree):
    sites = []
    unresolved = []

    def emit(value_node, field, dialect, ctx_node, line):
        resolution, value = index.resolve(value_node)
        rec = Site(rel, line, field, dialect, resolution, value, snippet(ctx_node))
        if value is None:
            rec.resolution = "unresolved" if resolution != "ifexp_true_branch" else resolution
            unresolved.append(rec)
        elif resolution == "ifexp_true_branch":
            sites.append(rec)
        else:
            sites.append(rec)

    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            for kw in node.keywords:
                if kw.arg in GRADE_FIELD_SET:
                    emit(kw.value, kw.arg, "call_keyword", node,
                         getattr(kw.value, "lineno", node.lineno))
            name = callee_name(node.func)
            if name:
                params = index.signatures.get(name)
                if params:
                    for i, arg in enumerate(node.args):
                        if i < len(params) and params[i] in GRADE_FIELD_SET:
                            emit(arg, params[i], "call_positional_signature", node,
                                 getattr(arg, "lineno", node.lineno))
                fields = index.class_fields.get(name)
                if fields:
                    for i, arg in enumerate(node.args):
                        if i < len(fields) and fields[i] in GRADE_FIELD_SET:
                            emit(arg, fields[i], "dataclass_positional", node,
                                 getattr(arg, "lineno", node.lineno))
                if name in ("get", "setdefault") and len(node.args) == 2:
                    key = const_str(node.args[0])
                    if key in GRADE_FIELD_SET:
                        emit(node.args[1], key, "get_default", node,
                             getattr(node.args[1], "lineno", node.lineno))
        elif isinstance(node, ast.Dict):
            for k, v in zip(node.keys, node.values):
                key = const_str(k) if k is not None else None
                if key in GRADE_FIELD_SET:
                    emit(v, key, "dict_value", v, getattr(v, "lineno", node.lineno))
        elif isinstance(node, ast.Assign):
            for tgt in node.targets:
                if isinstance(tgt, ast.Name) and tgt.id in GRADE_FIELD_SET:
                    emit(node.value, tgt.id, "assign", node, node.lineno)
                elif isinstance(tgt, ast.Subscript):
                    key = subscript_key(tgt)
                    if key in GRADE_FIELD_SET:
                        emit(node.value, key, "subscript_assign", node, node.lineno)
        elif isinstance(node, ast.AnnAssign):
            if isinstance(node.target, ast.Name) and node.target.id in GRADE_FIELD_SET \
                    and node.value is not None:
                emit(node.value, node.target.id, "annassign_default", node, node.lineno)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            args = node.args
            positional = list(args.posonlyargs) + list(args.args)
            if args.defaults:
                for arg, default in zip(positional[len(positional) - len(args.defaults):],
                                        args.defaults):
                    if arg.arg in GRADE_FIELD_SET:
                        emit(default, arg.arg, "param_default", node,
                             getattr(default, "lineno", node.lineno))
            for arg, default in zip(args.kwonlyargs, args.kw_defaults):
                if default is not None and arg.arg in GRADE_FIELD_SET:
                    emit(default, arg.arg, "param_default", node,
                         getattr(default, "lineno", node.lineno))

    return sites, unresolved


def _adjunct_tokens():
    base = set(CANONICAL) | {"P_structural"}
    return base | {"[" + t + "]" for t in base}


def collect_comparands(rel, tree):
    """Token-first: string constants carrying a canonical or bracketed-canonical
    spelling that sit in a comparison or a prefix test.  Reported apart -- a
    token in a `==`, `in`, `startswith` or `endswith` is not a stray to be
    normalised, it is a site that must move with whatever it reads."""
    exact = _adjunct_tokens()
    prefixes = tuple("[" + t for t in (set(CANONICAL) | {"P_structural"}))
    out = []

    def interesting(text):
        return text in exact or text.startswith(prefixes)

    for node in ast.walk(tree):
        if isinstance(node, ast.Compare):
            for op in [node.left] + list(node.comparators):
                operands = op.elts if isinstance(op, (ast.Tuple, ast.List, ast.Set)) else [op]
                for o in operands:
                    text = const_str(o)
                    if text is not None and interesting(text):
                        out.append({"path": rel, "line": node.lineno, "token": text,
                                    "shape": "compare", "context": snippet(node)})
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) \
                and node.func.attr in ("startswith", "endswith"):
            for arg in node.args:
                targets = arg.elts if isinstance(arg, ast.Tuple) else [arg]
                for t in targets:
                    text = const_str(t)
                    if text is not None and interesting(text):
                        out.append({"path": rel, "line": node.lineno, "token": text,
                                    "shape": node.func.attr, "context": snippet(node)})
    return out


def collect_token_first(rel, tree, counted_keys):
    """Adjunct: every string constant equal to a canonical or bracketed-canonical
    token, whether or not this census counted it as a grade site.  It measures
    the reach of the field-name enumeration; it does not extend it."""
    wanted = _adjunct_tokens()
    out = []
    for node in ast.walk(tree):
        text = const_str(node)
        if text is None or text not in wanted:
            continue
        line = getattr(node, "lineno", -1)
        out.append({"path": rel, "line": line, "token": text,
                    "counted_as_grade_site": (rel, line, text) in counted_keys})
    return out


# ---------------------------------------------------------------------------
# The census
# ---------------------------------------------------------------------------

def run_census(root):
    files = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d != "__pycache__"]
        for fn in sorted(filenames):
            if fn.endswith(".py"):
                files.append(os.path.join(dirpath, fn))
    files.sort()

    sites, unresolved, comparands, parse_errors, rebound = [], [], [], [], []
    parsed = []

    for path in files:
        rel = os.path.relpath(path).replace(os.sep, "/")
        try:
            with open(path, "r", encoding="utf-8") as fh:
                source = fh.read()
            tree = ast.parse(source, filename=path)
        except Exception as exc:
            parse_errors.append({"path": rel,
                                 "error": type(exc).__name__ + ": " + str(exc)[:120]})
            continue
        index = ModuleIndex(tree)
        s, u = collect_sites(rel, index, tree)
        sites.extend(s)
        unresolved.extend(u)
        comparands.extend(collect_comparands(rel, tree))
        # sorted(), not set iteration: a set's order varies with the process hash
        # seed, and a report that changes between runs cannot be a baseline.
        for nm in sorted(index.rebound_names):
            rebound.append({"path": rel, "name": nm})
        parsed.append((rel, tree))

    counted = set((s.path, s.line, s.value) for s in sites)
    token_first = []
    for rel, tree in parsed:
        token_first.extend(collect_token_first(rel, tree, counted))

    return {
        "files_walked": len(files),
        "files_parsed": len(parsed),
        "parse_errors": parse_errors,
        "sites": sites,
        "unresolved": unresolved,
        "comparands": comparands,
        "token_first": token_first,
        "rebound_names": rebound,
    }


def field_group_of(field):
    for label, members in FIELD_GROUPS:
        if field in members:
            return label
    return "other-grade"


def e2_tight(value):
    if value in E2_TIGHT_EXCLUDE:
        return False
    if value in E2_TIGHT_BARE:
        return True
    return bool(E2_TIGHT_SHAPE_RE.match(value))


def build_report(census, root):
    resolved = [s for s in census["sites"] if s.resolution != "ifexp_true_branch"]
    ifexp = [s for s in census["sites"] if s.resolution == "ifexp_true_branch"]

    partition = defaultdict(lambda: defaultdict(int))
    reasons = defaultdict(Counter)
    tokens_by_field = defaultdict(Counter)
    token_bucket = {}
    site_index = defaultdict(list)
    alias_sites = []

    for s in resolved:
        bucket, reason, _base = classify(s.value)
        partition[bucket][s.field] += 1
        reasons[bucket][reason] += 1
        tokens_by_field[s.field][s.value] += 1
        token_bucket[s.value] = bucket
        site_index[s.value].append(s.as_dict())
        if bucket == "NORMALISABLE_ALIAS":
            alias_sites.append(s)

    all_tokens = Counter()
    for counter in tokens_by_field.values():
        all_tokens.update(counter)

    disposition = []
    for label, toks in DISPOSITION_TOKENS:
        by_field = Counter(s.field for s in resolved if s.value in toks)
        disposition.append((label, {"tokens": list(toks), "total": sum(by_field.values()),
                                    "by_field": dict(by_field)}))

    status_flat = [s for s in resolved if s.field in FIELD_STATUS]
    status_ifexp = [s for s in ifexp if s.field in FIELD_STATUS]
    status_unres = [s for s in census["unresolved"] if s.field in FIELD_STATUS]
    status_e2 = [s for s in status_flat if e2_tight(s.value)]

    epi = [s for s in resolved if s.field in FIELD_EPISTEMIC]
    epi_ifexp = [s for s in ifexp if s.field in FIELD_EPISTEMIC]
    epi_unres = [s for s in census["unresolved"] if s.field in FIELD_EPISTEMIC]

    tf = census["token_first"]
    tf_counted = sum(1 for r in tf if r["counted_as_grade_site"])
    tf_uncounted = Counter(r["token"] for r in tf if not r["counted_as_grade_site"])

    return {
        "root": root,
        "files_walked": census["files_walked"],
        "files_parsed": census["files_parsed"],
        "parse_errors": census["parse_errors"],
        "sites_resolved": len(resolved),
        "sites_ifexp": len(ifexp),
        "sites_unresolved": len(census["unresolved"]),
        "distinct_tokens": len(all_tokens),
        "partition": {b: dict(partition[b]) for b in BUCKETS},
        "partition_totals": {b: sum(partition[b].values()) for b in BUCKETS},
        "partition_by_group": {
            b: {label: sum(partition[b].get(f, 0) for f in members)
                for label, members in FIELD_GROUPS}
            for b in BUCKETS
        },
        "bucket_reasons": {b: dict(reasons[b]) for b in BUCKETS},
        "fields": dict(Counter(s.field for s in census["sites"])),
        "dialects": dict(Counter(s.dialect for s in census["sites"])),
        "resolutions": dict(Counter(s.resolution for s in census["sites"])),
        "disposition_populations": dict(disposition),
        "disposition_order": [label for label, _ in disposition],
        "epistemic": {
            "sites": len(epi), "ifexp": len(epi_ifexp), "unresolved": len(epi_unres),
            "distinct_tokens": len(set(s.value for s in epi)),
            "normalisable_alias_ground": sum(1 for s in alias_sites
                                             if s.field in FIELD_EPISTEMIC),
        },
        "status_dialect": {
            "flat_sites": len(status_flat),
            "ifexp_sites": len(status_ifexp),
            "unresolved_sites": len(status_unres),
            "distinct_tokens_flat": len(set(s.value for s in status_flat)),
            "e2_tight_filter_sites": len(status_e2),
            "e2_tight_filter_tokens": len(set(s.value for s in status_e2)),
        },
        "normalisable_alias_ground_all_fields": len(alias_sites),
        "normalisable_alias_by_field": dict(Counter(s.field for s in alias_sites)),
        "normalisable_alias_sites": [s.as_dict() for s in alias_sites],
        "token_inventory": {t: {"sites": n, "bucket": token_bucket.get(t, "?")}
                            for t, n in all_tokens.items()},
        "token_inventory_by_field": {f: dict(c) for f, c in tokens_by_field.items()},
        "comparand_inventory": census["comparands"],
        "rebound_names": census["rebound_names"],
        "ifexp_sites": [s.as_dict() for s in ifexp],
        "unresolved_sites": [s.as_dict() for s in census["unresolved"]],
        "token_first_adjunct": {
            "occurrences": len(tf),
            "counted_as_grade_site": tf_counted,
            "not_counted_by_token": dict(tf_uncounted),
        },
        "_site_index": dict(site_index),
    }


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

def rule(char="=", n=78):
    return char * n


def print_header(rep, root, source_note):
    print(rule())
    print("GRADE-TOKEN CENSUS  --  a reporting tool.  It prints.  It gates nothing.")
    print(rule())
    print("")
    print("AUTHORISATION")
    print("  GT12@2026-08-30, ruled 2026-08-31 (Reference - DECISION - The Grade-Token")
    print("  Docket (2026-08-31), section 2): disposition batches first, reporting tool")
    print("  second, ratchet check not yet.  That ruling is the Corpus-Hygiene-fence")
    print("  ruling for this tool, in the Working Rule 17 shape.  The registered ratchet")
    print("  check remains UNAUTHORISED pending a separate ruling.")
    print("")
    print("STANDING")
    print("  Not a validator, not a gate, not a registered check, not a tripwire.  It")
    print("  writes its report, and its JSON record when asked, and nothing else; it exits")
    print("  0 on every successful run whatever it measures, so no caller can branch on")
    print("  what it found.  Under GT12 nothing may gate on it.  It rules on nothing:")
    print("  each bucket names the dated ruling it implements, and anything no ruling")
    print("  reaches is reported with its reason rather than judged.")
    print("")
    print("SUBJECT")
    print("  root: %s" % root)
    print("  %s" % source_note)
    print("  files walked: %d   parsed: %d   parse errors: %d"
          % (rep["files_walked"], rep["files_parsed"], len(rep["parse_errors"])))
    for pe in rep["parse_errors"]:
        print("    ! %s -- %s" % (pe["path"], pe["error"]))
    print("")
    print("SYNTAX INVENTORY -- the dialects this census resolves")
    for name, desc in SYNTAX_DIALECTS:
        print("  %-26s %s" % (name, desc))
    print("")
    print("VALUE RESOLUTION")
    for name, desc in RESOLUTIONS:
        print("  %-26s %s" % (name, desc))
    print("")
    print("FIELD-NAME ENUMERATION -- what counts as a grade field here")
    for label, members in FIELD_GROUPS:
        print("  %-20s %s" % (label, ", ".join(members)))
    print("")
    print("DECLARED SETS")
    print("  canonical (GT1@2026-08-30(b)): %s" % ", ".join(CANONICAL))
    print("  reserved  (GT9@2026-08-30(a)): %s" % ", ".join(sorted(RESERVED_GT9)))
    print("  run-outcome enumeration (this tool's own, stated not inferred):")
    print("    %s" % ", ".join(sorted(x for x in RUN_OUTCOME_ENUM if x)))
    print("")
    print("STATED LIMITATIONS")
    print("  1. A field-name census cannot see a dialect nobody named.  Section 8's")
    print("     token-first adjunct measures that reach; it does not close it.")
    print("  2. This reads AUTHORED SOURCE, not a loaded REGISTRY.  A grade computed at")
    print("     run time is outside it and is reported unresolved, never guessed.")
    print("  3. Module constants resolve within their own module only; a grade imported")
    print("     from a sibling resolves as unresolved.")
    print("  4. Comments are excluded entirely, and docstring and returned-prose text is")
    print("     excluded from the grade-site census of sections 1-7.  Section 8's adjunct")
    print("     walks every string constant, so a docstring that IS a canonical token")
    print("     verbatim would appear there, in its uncounted population.")
    print("  5. The run-outcome separation for `status` is the enumeration printed above,")
    print("     not a shape test.  Section 4 additionally reproduces the tight grade-shape")
    print("     filter of RETURN_E2_retake_2026-08-30 section 1 so the GT7@2026-08-30(c)")
    print("     figure of record stays comparable; that filter is quoted, not authored.")
    print("  6. Two judgements remain, named rather than hidden.  (i) The identifier-shape")
    print("     test that sends sentence-valued and contract-string grades to MALFORMED is")
    print("     this tool's, not a ruling's.  (ii) The E2 filter of item 5 is a judgement")
    print("     its own author measured in both directions.  Both are reported through")
    print("     named bucket reasons rather than folded into a verdict, because there is")
    print("     no rule saying what a grade-shaped string is -- which is the mapping's own")
    print("     point, and Working Rule 17's.")
    print("")


def print_report(rep):
    print(rule())
    print("1. POPULATION")
    print(rule("-"))
    print("  grade sites, value resolved      %6d" % rep["sites_resolved"])
    print("  grade sites, IfExp dialect       %6d   (GT8@2026-08-30; reported apart)"
          % rep["sites_ifexp"])
    print("  grade sites, unresolved          %6d   (recorded, never guessed)"
          % rep["sites_unresolved"])
    print("  distinct resolved tokens         %6d" % rep["distinct_tokens"])
    print("")
    print("  by field:")
    for field, n in sorted(rep["fields"].items(), key=lambda kv: (-kv[1], kv[0])):
        print("    %-18s %6d   [%s]" % (field, n, field_group_of(field)))
    print("")
    print("  by syntax dialect:")
    for name, _d in SYNTAX_DIALECTS:
        print("    %-26s %6d" % (name, rep["dialects"].get(name, 0)))
    print("")
    print("  by value resolution:")
    for name, _d in RESOLUTIONS:
        print("    %-26s %6d" % (name, rep["resolutions"].get(name, 0)))
    print("")

    print(rule())
    print("2. CONFORMANCE PARTITION, per bucket per field group")
    print(rule("-"))
    groups = [label for label, _ in FIELD_GROUPS]
    print("  %-24s %16s %8s %11s %8s" % ("bucket", groups[0], groups[1], groups[2], "TOTAL"))
    for b in BUCKETS:
        row = rep["partition_by_group"][b]
        print("  %-24s %16d %8d %11d %8d"
              % (b, row[groups[0]], row[groups[1]], row[groups[2]],
                 rep["partition_totals"][b]))
    print("  %-24s %16s %8s %11s %8d"
          % ("(sum)", "", "", "", sum(rep["partition_totals"].values())))
    print("")
    print("  bucket reasons -- what put each site where:")
    for b in BUCKETS:
        rs = rep["bucket_reasons"][b]
        if not rs:
            continue
        print("    %s" % b)
        for reason, n in sorted(rs.items(), key=lambda kv: -kv[1]):
            print("      %6d  %s" % (n, reason))
    print("")

    print(rule())
    print("3. NAMED DISPOSITION POPULATIONS (GT2 / GT3 / GT4 batches)")
    print(rule("-"))
    for label in rep["disposition_order"]:
        rec = rep["disposition_populations"][label]
        detail = ", ".join("%s=%d" % (f, n) for f, n in sorted(rec["by_field"].items()))
        print("  %-46s %5d   %s" % (label, rec["total"], detail or "-"))
    print("")
    print("  regression-gate grounds -- NORMALISABLE_ALIAS sites, per field, so any")
    print("  denominator a ruling names can be read off directly (GTA1@2026-08-31 states")
    print("  its arithmetic in an `epistemic`-only and an all-fields denominator):")
    for field in GRADE_FIELDS:
        print("    %-18s %5d" % (field, rep["normalisable_alias_by_field"].get(field, 0)))
    print("    %-18s %5d" % ("ALL FIELDS", rep["normalisable_alias_ground_all_fields"]))
    for s in rep["normalisable_alias_sites"]:
        print("      %s:%d  field=%s  dialect=%s  value=%r"
              % (s["path"], s["line"], s["field"], s["dialect"], s["value"]))
    print("")

    print(rule())
    print("4. THE `status` DIALECT -- OUT OF SCOPE FOR VOCABULARY per GT7@2026-08-30(c),")
    print("   recorded with its figure so the surface does not become invisible")
    print(rule("-"))
    sd = rep["status_dialect"]
    print("  flat sites, value resolved         %5d" % sd["flat_sites"])
    print("  IfExp sites (GT8@2026-08-30)       %5d" % sd["ifexp_sites"])
    print("  unresolved sites                   %5d" % sd["unresolved_sites"])
    print("  distinct tokens, flat              %5d" % sd["distinct_tokens_flat"])
    print("  reproduction of the E2-retake tight grade-shape filter over the flat sites:")
    print("    sites  %5d      tokens %5d"
          % (sd["e2_tight_filter_sites"], sd["e2_tight_filter_tokens"]))
    print("")
    ep = rep["epistemic"]
    print("  for contrast, the `epistemic` family (the ruled ground):")
    print("    sites %5d   IfExp %5d   unresolved %5d   distinct tokens %5d"
          % (ep["sites"], ep["ifexp"], ep["unresolved"], ep["distinct_tokens"]))
    print("")


def print_inventory(rep, top):
    print(rule())
    print("5. DISTINCT-TOKEN INVENTORY, with per-token site counts")
    print(rule("-"))
    ordered = sorted(rep["token_inventory"].items(),
                     key=lambda kv: (-kv[1]["sites"], kv[0]))
    shown = ordered if top <= 0 else ordered[:top]
    print("  %5s  %-22s %s" % ("sites", "bucket", "token"))
    for token, rec in shown:
        display = " ".join(token.split())
        if display != token.strip() or display == "":
            display = repr(token) if display == "" else display
        if len(display) > 92:
            display = display[:89] + "..."
        print("  %5d  %-22s %s" % (rec["sites"], rec["bucket"], display))
    if len(ordered) > len(shown):
        print("  ... %d further tokens; --top 0 prints all, --json records all"
              % (len(ordered) - len(shown)))
    print("")

    print(rule())
    print("6. COMPARAND INVENTORY -- tokens read, not assigned")
    print(rule("-"))
    print("  A grade token in a `==`, `in`, `startswith` or `endswith` is not a stray to")
    print("  be normalised; it is a site that must move with whatever it reads.  Counted")
    print("  in no bucket above.")
    comps = rep["comparand_inventory"]
    print("  occurrences: %d" % len(comps))
    for token, n in sorted(Counter(c["token"] for c in comps).items(),
                           key=lambda kv: (-kv[1], kv[0])):
        print("    %5d  %s" % (n, token))
    for c in comps:
        print("      %s:%d  [%s]  %s" % (c["path"], c["line"], c["shape"], c["context"][:96]))
    print("")

    print(rule())
    print("7. UNRESOLVED AND IfExp SITES")
    print(rule("-"))
    print("  unresolved %5d      IfExp %5d" % (rep["sites_unresolved"], rep["sites_ifexp"]))
    print("  Both are recorded and neither is folded into section 2.  Per-field:")
    for label, members in FIELD_GROUPS:
        u = sum(1 for s in rep["unresolved_sites"] if s["field"] in members)
        i = sum(1 for s in rep["ifexp_sites"] if s["field"] in members)
        print("    %-20s unresolved %5d   IfExp %5d" % (label, u, i))
    reb = rep["rebound_names"]
    print("  names bound to more than one distinct string in their own file: %d.  Each is"
          % len(reb))
    print("  bound to nothing, so a site reading one resolves as unresolved rather than")
    print("  to a guess.  These are a share of the unresolved population above.")
    for r in reb[:20]:
        print("    %s  %s" % (r["path"], r["name"]))
    if len(reb) > 20:
        print("    ... %d further; the JSON record carries all" % (len(reb) - 20))
    print("")

    print(rule())
    print("8. TOKEN-FIRST ADJUNCT -- the reach of the field-name enumeration")
    print(rule("-"))
    tf = rep["token_first_adjunct"]
    print("  Every string constant in the tree equal to a canonical token, a bracketed")
    print("  canonical token, or `P_structural` in either spelling, whether or not")
    print("  section 1 counted it as a grade site.")
    print("  occurrences                       %5d" % tf["occurrences"])
    print("  counted as a grade site above     %5d" % tf["counted_as_grade_site"])
    print("  not counted, any context          %5d"
          % (tf["occurrences"] - tf["counted_as_grade_site"]))
    print("  not counted, by token:")
    for token, n in sorted(tf["not_counted_by_token"].items(),
                           key=lambda kv: (-kv[1], kv[0])):
        print("    %5d  %s" % (n, token))
    print("  The uncounted population holds comparands, list and tuple members, keys, and")
    print("  values in fields this census does not name.  The number is a reach")
    print("  measurement and nothing follows from it on its own.")
    print("")


def print_footer():
    print(rule())
    print("END OF REPORT.  Nothing above is a verdict.  This tool gates nothing, and no")
    print("number in it may be quoted as a claim about whether any site is correct.")
    print(rule())


def print_diff(rep, baseline, baseline_path):
    print(rule())
    print("BASELINE DIFF")
    print(rule("-"))
    print("  baseline file: %s" % baseline_path)
    print("  baseline root: %s   tool sha256 then: %s"
          % (baseline.get("root", "?"), (baseline.get("_self_sha256") or "-")[:16]))
    print("  this run  root: %s   tool sha256 now : %s"
          % (rep.get("root", "?"), (rep.get("_self_sha256") or "-")[:16]))
    if baseline.get("_self_sha256") and baseline["_self_sha256"] != rep.get("_self_sha256"):
        print("  NOTE: the tool's own bytes differ between the two records.  A delta")
        print("  across two different instruments is not a measurement of the tree.")
    print("")
    print("  %-36s %9s %9s %9s" % ("measure", "baseline", "now", "delta"))

    def row(label, now, before):
        print("  %-36s %9s %9s %+9d" % (label, before, now, now - before))

    row("grade sites, resolved", rep["sites_resolved"], baseline.get("sites_resolved", 0))
    row("grade sites, IfExp", rep["sites_ifexp"], baseline.get("sites_ifexp", 0))
    row("grade sites, unresolved", rep["sites_unresolved"], baseline.get("sites_unresolved", 0))
    row("distinct tokens", rep["distinct_tokens"], baseline.get("distinct_tokens", 0))
    print("")
    print("  per bucket:")
    for b in BUCKETS:
        row("  " + b, rep["partition_totals"][b],
            baseline.get("partition_totals", {}).get(b, 0))
    print("")
    print("  named disposition populations:")
    for label in rep["disposition_order"]:
        before = baseline.get("disposition_populations", {}).get(label, {}).get("total", 0)
        row("  " + label[:34], rep["disposition_populations"][label]["total"], before)
    print("")
    print("  regression-gate grounds (NORMALISABLE_ALIAS), per field:")
    for field in GRADE_FIELDS:
        row("  " + field,
            rep["normalisable_alias_by_field"].get(field, 0),
            baseline.get("normalisable_alias_by_field", {}).get(field, 0))
    row("  ALL FIELDS",
        rep["normalisable_alias_ground_all_fields"],
        baseline.get("normalisable_alias_ground_all_fields", 0))
    print("")
    now_tokens = set(rep["token_inventory"])
    old_tokens = set(baseline.get("token_inventory", {}))
    appeared = sorted(now_tokens - old_tokens)
    vanished = sorted(old_tokens - now_tokens)
    print("  tokens appeared: %d" % len(appeared))
    for t in appeared:
        print("    + %s" % " ".join(t.split())[:96])
    print("  tokens vanished: %d" % len(vanished))
    for t in vanished:
        print("    - %s" % " ".join(t.split())[:96])
    print("")
    print("  The delta is the whole of what this section asserts.  Whether a fall of a")
    print("  given size is the right fall is a question for whoever ruled the batch.")
    print("")


def self_sha256():
    try:
        with open(os.path.abspath(__file__), "rb") as fh:
            return hashlib.sha256(fh.read()).hexdigest()
    except Exception:
        return ""


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Grade-token census: a reporting tool authorised by GT12@2026-08-30. "
                    "It prints; nothing gates on it.")
    ap.add_argument("--root", default="apf", help="tree to census (default: apf)")
    ap.add_argument("--json", dest="json_out", default=None,
                    help="write the full machine record here")
    ap.add_argument("--baseline", default=None,
                    help="a prior --json record; print per-bucket deltas against it")
    ap.add_argument("--top", type=int, default=40,
                    help="tokens printed in the inventory; 0 prints all (default 40)")
    ap.add_argument("--sites-for", default=None,
                    help="also print every site carrying this exact token")
    ap.add_argument("--quiet", action="store_true",
                    help="suppress the header and sections 5-8")
    args = ap.parse_args(argv)

    if not os.path.isdir(args.root):
        sys.stderr.write("grade_token_census: no such directory: %s\n"
                         "Run this from the repository root.\n" % args.root)
        return 2

    census = run_census(args.root)
    rep = build_report(census, args.root)
    site_index = rep.pop("_site_index")
    rep["_tool"] = TOOL_NAME
    rep["_tool_version"] = TOOL_VERSION
    rep["_self_sha256"] = self_sha256()

    source_note = "tool %s v%s, sha256 %s" % (TOOL_NAME, TOOL_VERSION, rep["_self_sha256"][:16])
    if not args.quiet:
        print_header(rep, args.root, source_note)
    print_report(rep)
    if not args.quiet:
        print_inventory(rep, args.top)

    if args.sites_for is not None:
        print(rule())
        print("SITES CARRYING THE EXACT TOKEN: %s" % args.sites_for)
        print(rule("-"))
        hits = site_index.get(args.sites_for, [])
        for s in hits:
            print("  %s:%d  field=%s  dialect=%s  resolution=%s"
                  % (s["path"], s["line"], s["field"], s["dialect"], s["resolution"]))
            print("      %s" % s["context"][:110])
        print("  total: %d" % len(hits))
        print("")

    if args.baseline:
        with open(args.baseline, "r", encoding="utf-8") as fh:
            baseline = json.load(fh)
        print_diff(rep, baseline, args.baseline)

    if not args.quiet:
        print_footer()

    if args.json_out:
        payload = dict(rep)
        payload["site_index"] = site_index
        with open(args.json_out, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(payload, fh, indent=1, sort_keys=True)
            fh.write("\n")
        sys.stderr.write("wrote %s\n" % args.json_out)

    return 0


if __name__ == "__main__":
    sys.exit(main())
