#!/usr/bin/env python3
r"""Vacancy census -- a REPORTING TOOL. Not a check. Not registered.

    python3 scripts/vacancy_census.py --discover
    python3 scripts/vacancy_census.py --library "<path to __APF Library>"
    python3 scripts/vacancy_census.py --library "<...>" --json out.json

Every place the CODE names a corpus object -- another check, a module, a
premise constant, an axiom, a reference document, a proposition number --
resolved against this repository and against the library.  A citation either
resolves or it does not.  That is the whole claim.

WHY THIS EXISTS
---------------
`scripts/anchor_census.py` resolves references pointing FROM PAPERS TO CODE.
Nothing resolved references pointing from CODE to CODE, or from CODE to
DOCUMENTS.  Three vacancies were found by hand on 2026-08-07, all three in
that blind spot, one at a time.  This tool makes that search mechanical, so
the list is finite and re-derivable instead of anecdotal.

WHAT IT ASSERTS
---------------
Facts, each decidable without inferring anyone's intent:

  * a cited `check_*` / `T_*` / `L_*` name is the name of a `def` in this
    tree, or it is not;
  * a resolved name is a key in the loaded bank registry under EITHER the
    bare-name or the `check_`-prefixed spelling, or it is not;
  * a cited name is a key of apf/crystal.py's `_DEP_ALIASES`, the corpus's
    own legacy/variant spelling table, whose target resolves -- or it is not;
  * a cited name is PUBLISHED as a keyed sub-clause record inside a check's
    returned structure (`L_cost_C1`, `L_cost_C2`, `L_cost_MAIN`), or it is not;
  * a cited name is a node label DECLARED by a machine-enforced dependency
    graph, or a member of a gate inventory anchored to one, or it is not;
  * a cited name is pinned BY NAME, with an adjudicated genre, in
    apf/ie_export_core_census.py's `FULL_SURFACE_TYPED_ROOTS` -- the
    corpus's own hand-ruled inventory of what resolves nowhere -- or it
    is not;
  * a cited name case-folds onto a live `def` or a live registry key
    (`T_AFFINITY_DERIVATION_EXECUTED` onto
    `check_T_affinity_derivation_executed`), or it does not;
  * a cited `foo.py` is a file in this tree, or it is not;
  * a cited `foo.py` absent from this tree is a file in the LIBRARY -- a
    parked lane, `APF Reference Docs/scripts/`, a closure pack -- or it
    is not.  Exists-but-outside-the-tree is a different fact from
    exists-in-the-tree, so the path it was found at is always reported;
  * a cited ALLCAPS premise constant is ASSIGNED as a Python name somewhere
    in this tree, or it is only ever consumed;
  * a cited `.md` / `.tex` document filename exists in the library, or it
    does not;
  * a cited document LOCATION ("Prop 2.3", "sec:foo") appears in a document
    the same citation names, or the citation names no document at all -- in
    which case it is UNRESOLVABLE BY DESIGN and is counted separately, never
    as a failure.

WHAT IT DOES NOT ASSERT
-----------------------
Whether a citation is APT.  "check_X is cited and no def check_X exists" is a
fact.  "This citation is misleading", "this dependency is the wrong one",
"this leg cannot fail", "this docstring overclaims" are judgements, and none
of them are in this tool.  Two instruments that tried to infer intent from
syntax were deleted on 2026-08-01 under a standing do-not-repair ruling
(Working Rule 17); nothing here reconstructs intent from punctuation.

It also does not FIX anything.  A tool that repairs what it measures has
audited itself.

THE FOUR NUMBERS, REPORTED SEPARATELY, ALWAYS
---------------------------------------------
  (1) POPULATION            reference instances scanned
  (2) COVERAGE              files parsed / files present, as a fraction
  (3) RAW NON-RESOLVERS     instances that did not resolve
  (4) RESIDUE               non-resolvers left after the named buckets

A single figure gets quoted without its unit and then disagrees with the next
measurement for no visible reason.

INSTANCES, NOT NAMES
--------------------
Every match is one instance.  Two citations on one line are two instances.
The anchor census collapsed (file, line, macro) and undercounted its densest
idiom badly; this tool never de-duplicates a site away.  Distinct names are
reported as a second, separately labelled figure.

BOTH REGISTRY SPELLINGS, ALWAYS
-------------------------------
Registry keys exist under bare-name (`'L_foo'`) and `check_`-prefixed
(`'check_L_foo'`) conventions -- ruled D6, no retrofit.  A lookup against one
spelling reports a false ABSENCE.  Every lookup here tries both.

RESOLVER DEFECTS THIS TOOL WAS BORN WITH, FOUND IN ITS OWN OUTPUT, FIXED
-----------------------------------------------------------------------
  * Scanning the TOKEN stream splits implicitly concatenated string literals,
    so a name written across two adjacent literals reads as two truncated
    fragments.  Fixed by scanning `ast.Constant.value`, which is already
    joined, and taking comments from `tokenize` separately.
  * A name wrapped across a LINE inside one docstring (`..._\n    ledger`)
    still fragments.  Not silently rejoined: rejoining is attempted, and a
    rejoin that resolves is bucketed LINE_WRAPPED_NAME and reported, so the
    scanner's own artifacts are visible rather than counted as vacancies.
  * `check_fn`, `check_count`, `check_name` are `check_*`-SHAPED and are
    local variables discussed in prose.  Bucketed BOUND_AS_PYTHON_NAME on the
    decidable test "is this token bound as a Python name anywhere in the
    tree", not on a guess about what it looks like.
  * Matching a module reference on BASENAME alone reports phantom
    resolutions; the anchor census logged ~50.  Here a basename match is
    recorded WITH the path it matched, and paths outside `apf/` are called
    out rather than silently accepted.
  * THE ONE THAT MATTERED.  The first run resolved names against EVERY `.py`
    in the repository.  The repo root carries legacy demo scripts -- among
    them `paper1.py`, which defines `def MD(...)`, `def L_iso(...)` and
    friends.  So `MD` and `check_L_iso` came back RESOLVED, and the tool
    MISSED two of the three vacancies it was built to reproduce.  A citation
    resolves against `apf/` or against the loaded registry; a def that lives
    only outside `apf/` is recorded, named, and bucketed
    DEF_OUTSIDE_APF_ONLY, never counted as a resolution.  This was found by
    the known-vacancy reproduction stage, which is why that stage exists.
  * The document-filename regex matched leftwards through prose, producing
    citations like "For full per-version changelog, see CHANGELOG.md" and
    fragments like "2026-04-26).md" where a filename wrapped across a line.
    Fixed by normalising whitespace before matching (a needle that can miss
    on where a line wraps is not a needle) and by resolving the LONGEST
    match against the library through progressively shorter suffixes, so a
    filename preceded by prose still resolves as the filename.
  * READING ONLY THE FIRST TWO SURFACES. The corpus names one object in at
    least five ways; the first version of this tool knew two of them, and on
    2026-08-07 a seat took its residue as a work list and deleted four
    CORRECT citations to live, well-defended objects. The three further
    resolvers R3 / R4 / R5 are documented at their definitions below, each
    reports its contribution by name and by instance, and each ships a
    negative control that runs on every invocation -- because
    over-resolution is the self-favouring direction, and a resolver written
    loosely enough moves the number without a single citation being repaired.
"""
import ast
import io
import os
import re
import sys
import json
import hashlib
import tokenize
import collections

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APF = os.path.join(REPO, "apf")

# Held out of the bank by design, untracked, no register() -- 2026-08-06.
HELD_FILES = {"carrier_side_dependency_ledger.py"}

# ---------------------------------------------------------------------------
# CARRIERS -- where a citation SITS.  Derived by AST survey (--discover), not
# assumed.  The survey enumerates every dict key and keyword argument in apf/
# whose value is a string or a collection of strings; the entries below are
# the ones that carry corpus identifiers.  Re-run --discover before trusting
# this list on a tree that has moved.
# ---------------------------------------------------------------------------
STRUCTURED_FIELDS = {
    "dependencies", "cross_refs", "premises", "premises_consumed",
    "conditional_on", "premise_stack", "premises_not_consumed",
    "forbidden_premises", "may_not_cite", "coderef", "registry_pointer",
    "engine_module", "runtime_module", "module", "source",
}
PROSE_FIELDS = {"summary", "key_result", "note", "notes", "claim_text",
                "description", "statement", "reason", "claim", "core_claim"}
PREMISE_CONSTS = re.compile(
    r"(PREMIS|CONDITIONAL_ON|FORBIDDEN|MAY_NOT_CITE|CROSS_REFS|DEPEND)")

# ---------------------------------------------------------------------------
# FAMILIES -- what a citation LOOKS LIKE.  Each family names the identifier
# shape and the resolver that decides it.
# ---------------------------------------------------------------------------
FAMILIES = {
    "CHECK":    re.compile(r"\bcheck_[A-Za-z0-9_]+"),
    "THEOREM":  re.compile(r"\bT_[A-Za-z][A-Za-z0-9_]*"),
    "LEMMA":    re.compile(r"\bL_[A-Za-z][A-Za-z0-9_]*"),
    "MODULE":   re.compile(r"\b[A-Za-z_][A-Za-z0-9_]*\.py\b"),
    "DOC_FILE": re.compile(r"[A-Za-z0-9_][A-Za-z0-9 _()\-.,'’&+]{2,140}?\.(?:md|tex)\b"),
    "DOC_LOC":  re.compile(
        r"(?:\b(?:Prop|Proposition|Lemma|Thm|Theorem|Cor|Corollary|Def|Definition"
        r"|Remark|Rem|Axiom|Table|Fig|Figure)\.?\s+\d+(?:\.\d+)+"
        r"|§\s?\d+(?:\.\d+)*"
        r"|\b(?:sec|fig|tab|eq|thm|lem|rem|def|app|alg|prop|cor):[A-Za-z0-9_:-]+)"),
    "PAPER":    re.compile(r"\bPaper\s+\d+(?:\s+Supplement)?"),
}
# These two families are scoped to structured carriers only.  In free prose
# `R1` is a resistor, `A2` is a paper size and `MD` is a US state; counting
# those would drown the report in noise that no reader could act on.
PREMISE_TOKEN = re.compile(r"\b(?:DEF_[A-Z0-9_]+|[A-Z][A-Z0-9]*(?:_[A-Z0-9]+){1,})\b")
AXIOM_TOKEN = re.compile(r"\b(?:A1|A2|MD|BW|FD[1-5]|R[1-9]|occupancy)\b")

STRUCTURED_CARRIER = re.compile(r"^(?:FIELD:(?:%s)|CONST:)" %
                                "|".join(sorted(STRUCTURED_FIELDS)))


# ===================================================================== index
def index_repo(repo):
    """defs, module paths, every bound Python name, and parse coverage.

    `defs` is scoped to apf/. `defs_other` holds the rest of the repo and is
    reported, never used to resolve -- see the resolver-defect note above."""
    defs = collections.defaultdict(list)
    defs_other = collections.defaultdict(list)
    modules = collections.defaultdict(list)      # basename -> [relpath]
    allfiles = set()                             # every file basename in repo
    relpaths = set()
    bound = set()
    parsed, failed = [], []
    for root, dirs, names in os.walk(repo):
        dirs[:] = [d for d in dirs
                   if d not in ("__pycache__", ".git", ".pytest_cache", "Old")]
        for n in sorted(names):
            allfiles.add(n)
            if not n.endswith(".py"):
                continue
            p = os.path.join(root, n)
            rel = os.path.relpath(p, repo).replace(os.sep, "/")
            relpaths.add(rel)
            modules[n].append(rel)
            in_apf = rel.startswith("apf/")
            try:
                src = open(p, encoding="utf-8", errors="replace").read()
                tree = ast.parse(src)
            except Exception as e:                                   # noqa
                failed.append((rel, type(e).__name__))
                continue
            parsed.append(rel)
            for nd in ast.walk(tree):
                if isinstance(nd, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    (defs if in_apf else defs_other)[nd.name].append((rel, nd.lineno))
                    if isinstance(nd, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        for a in list(nd.args.args) + list(nd.args.kwonlyargs) + \
                                 list(nd.args.posonlyargs):
                            if in_apf:
                                bound.add(a.arg)
                    if in_apf:
                        bound.add(nd.name)
                elif not in_apf:
                    continue
                elif isinstance(nd, ast.Assign):
                    for t in nd.targets:
                        for s in ast.walk(t):
                            if isinstance(s, ast.Name):
                                bound.add(s.id)
                elif isinstance(nd, (ast.AnnAssign, ast.AugAssign)):
                    for s in ast.walk(nd.target):
                        if isinstance(s, ast.Name):
                            bound.add(s.id)
                elif isinstance(nd, (ast.Import, ast.ImportFrom)):
                    for a in nd.names:
                        bound.add((a.asname or a.name).split(".")[0])
                elif isinstance(nd, (ast.For, ast.comprehension)):
                    tgt = nd.target
                    for s in ast.walk(tgt):
                        if isinstance(s, ast.Name):
                            bound.add(s.id)
    return dict(defs=defs, defs_other=defs_other, modules=dict(modules),
                relpaths=relpaths, allfiles=allfiles,
                bound=bound, parsed=parsed, failed=failed)


# The library lives on a Drive stream mount. Two subtrees make a full walk
# take longer than the rest of this tool put together -- `Codebase/` (the
# frozen mirror plus snapshot zips) and `Evidence/` (16k files) -- and neither
# holds a document that code cites by name. They are PRUNED, and the pruning
# is printed, because a document that exists only under a pruned root would
# read here as not-found.
LIB_PRUNE = {"Codebase", "Evidence", "__pycache__", ".git", ".obsidian",
             "node_modules", ".pytest_cache"}


def index_library(lib):
    """Document filenames in the library. Filename -> [relpath]."""
    docs = collections.defaultdict(list)
    if not lib or not os.path.isdir(lib):
        return dict(docs={}, root=lib, present=False, pruned=sorted(LIB_PRUNE))
    for root, dirs, names in os.walk(lib):
        dirs[:] = [d for d in dirs if d not in LIB_PRUNE]
        for n in names:
            if n.endswith((".md", ".tex", ".pdf")):
                docs[n].append(os.path.relpath(os.path.join(root, n), lib))
    return dict(docs=dict(docs), root=lib, present=True, pruned=sorted(LIB_PRUNE))


def load_registry(repo):
    try:
        sys.path.insert(0, repo)
        from apf import bank as _bank                                # noqa
        _bank._load()
        reg = set(_bank.REGISTRY)
        reg |= {k[6:] for k in list(reg) if k.startswith("check_")}
        reg |= {"check_" + k for k in list(reg)}
        return reg, len(_bank.REGISTRY), _bank.EXPECTED_THEOREM_COUNT
    except Exception as e:                                            # noqa
        return None, None, f"{type(e).__name__}: {e}"


def load_manifest(repo):
    try:
        sys.path.insert(0, repo)
        from apf import _module_manifest as m                         # noqa
        return (set(m.ARCHITECTURE_ONLY_MODULES),
                set(m.STANDALONE_LEMMA_MODULES),
                set(m.BANK_REGISTRY_MODULES))
    except Exception:                                                 # noqa
        return set(), set(), set()


# ============================================================ carrier labels
def carrier_map(tree):
    """(lineno, col) intervals -> carrier label, for every string Constant.

    Keyed by the AST node's own span, so an implicitly concatenated literal is
    ONE entry covering the whole group.  That is the point: `.value` is the
    joined text, which is what a name split across two adjacent literals needs.
    """
    out = {}

    def mark(node, label):
        out[(node.lineno, node.col_offset)] = label

    def walk(node, label):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            mark(node, label)
            return
        if isinstance(node, ast.Call):
            walk(node.func, label)
            for a in node.args:
                walk(a, label)
            for kw in node.keywords:
                walk(kw.value, ("FIELD:" + kw.arg) if kw.arg else label)
            return
        if isinstance(node, ast.Dict):
            for k, v in zip(node.keys, node.values):
                if k is not None:
                    walk(k, label)
                lab = ("FIELD:" + k.value
                       if isinstance(k, ast.Constant) and isinstance(k.value, str)
                       else label)
                walk(v, lab)
            return
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            tgts = node.targets if isinstance(node, ast.Assign) else [node.target]
            nm = None
            for t in tgts:
                if isinstance(t, ast.Name):
                    nm = t.id
            lab = ("CONST:" + nm) if (nm and nm.isupper()) else label
            if node.value is not None:
                walk(node.value, lab)
            return
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef,
                             ast.ClassDef)):
            body = list(node.body)
            if body and isinstance(body[0], ast.Expr) and \
               isinstance(body[0].value, ast.Constant) and \
               isinstance(body[0].value.value, str):
                mark(body[0].value, "DOCSTRING")
                body = body[1:]
            for ch in ast.iter_child_nodes(node):
                if isinstance(ch, ast.Expr) and ch not in body and \
                   isinstance(ch.value, ast.Constant):
                    continue
                walk(ch, label)
            return
        for ch in ast.iter_child_nodes(node):
            walk(ch, label)

    walk(tree, "STRING")
    return out


def const_dict_keys(tree):
    """CONSTNAME -> {string keys of any dict under it}.

    A module-level constant that is a graph or a table DECLARES its own node
    names as dict keys. A `T_*`-shaped token inside `CONST:DEPENDENCY_GRAPH`
    that is also a key of `DEPENDENCY_GRAPH` is naming that graph's own node,
    not citing a bank theorem. Keys only -- a VALUE naming a node the graph
    does not declare stays in the residue, which is the interesting case."""
    out = collections.defaultdict(set)
    for nd in ast.walk(tree):
        # AnnAssign, not just Assign. Omitting it was a real defect: the
        # corpus writes `DEPENDENCY_GRAPH: Dict[str, ...] = {...}`, so the
        # largest graphs in the tree declared no keys and their own nodes
        # were reported as vacancies.
        if not isinstance(nd, (ast.Assign, ast.AnnAssign)):
            continue
        nm = None
        for t in (nd.targets if isinstance(nd, ast.Assign) else [nd.target]):
            if isinstance(t, ast.Name) and t.id.isupper():
                nm = t.id
        if not nm or nd.value is None:
            continue
        for sub in ast.walk(nd.value):
            if isinstance(sub, ast.Dict):
                for k in sub.keys:
                    if isinstance(k, ast.Constant) and isinstance(k.value, str):
                        out[nm].add(k.value)
    return dict(out)


def scan_file(rel, src):
    """Yield (lineno, carrier, text) prose units: string constants + comments."""
    units = []
    try:
        tree = ast.parse(src)
    except Exception:                                                 # noqa
        return units, False, {}
    labels = carrier_map(tree)
    for nd in ast.walk(tree):
        if isinstance(nd, ast.Constant) and isinstance(nd.value, str):
            lab = labels.get((nd.lineno, nd.col_offset), "STRING")
            units.append((nd.lineno, lab, nd.value))
    try:
        for tok in tokenize.generate_tokens(io.StringIO(src).readline):
            if tok.type == tokenize.COMMENT:
                units.append((tok.start[0], "COMMENT", tok.string))
    except Exception:                                                 # noqa
        pass
    return units, True, const_dict_keys(tree)


# ================================================================= resolvers
def resolves_name(name, defs, reg, defs_other=None):
    """A name resolves against apf/ or against the loaded registry. A def that
    lives ONLY elsewhere in the repo is evidence, never a resolution."""
    for cand in (name, "check_" + name):
        if cand in defs:
            rel, ln = defs[cand][0]
            return True, f"{rel}:{ln}"
    if reg is not None and (name in reg or ("check_" + name) in reg):
        return True, "registry-only (no def found under apf/)"
    if defs_other:
        for cand in (name, "check_" + name):
            if cand in defs_other:
                rel, ln = defs_other[cand][0]
                return False, f"OUTSIDE apf/: {rel}:{ln}"
    return False, ""


def normalize_ws(text):
    """Whitespace-collapsed copy plus a position map back into the original.

    Working Rule 18: a needle that can miss because of where a line wraps is
    not a needle. A document filename inside a docstring routinely wraps."""
    out, idx = [], []
    prev_ws = False
    for i, ch in enumerate(text):
        if ch.isspace():
            if not prev_ws:
                out.append(" ")
                idx.append(i)
            prev_ws = True
        else:
            out.append(ch)
            idx.append(i)
            prev_ws = False
    return "".join(out), idx


def resolve_doc(raw, docnames):
    """Longest match, then progressively shorter space-delimited suffixes.

    The regex matches leftwards into prose ("see CHANGELOG.md"), and a
    filename genuinely contains spaces here ("Reference - Foo (2026-01-01).md").
    Trying suffixes decides both without guessing where the prose stops."""
    words = raw.strip().split(" ")
    for i in range(len(words)):
        cand = " ".join(words[i:]).strip(" ([{-")
        if cand in docnames:
            return cand, docnames[cand]
    # Nothing matched. Report from the last corpus-document marker if the run
    # carries one, so a real citation is not buried under the prose in front
    # of it. Display only -- it changes no verdict.
    for i in range(len(words) - 1, -1, -1):
        if words[i].strip("([{-").startswith(("Reference", "Paper", "APF")):
            return " ".join(words[i:]).strip(" ([{-"), None
    return raw.strip(), None


def prefix_of_existing(name, defs):
    # A name already ending in `_` is written that way at `startswith(...)`
    # filter sites -- `name.startswith("check_T_bottom_msbar_")`. Appending a
    # second underscore made every one of those read as a vacancy.
    pre = ((name, "check_" + name) if name.endswith("_")
           else (name + "_", "check_" + name + "_"))
    for d in defs:
        if d.startswith(pre[0]) or d.startswith(pre[1]):
            return d
    return None


# A `T_`/`L_` token whose tail carries no underscore and is at most three
# characters: T_R (a colour factor), T_t (a scale), L_L (a fermion class),
# T_CMB, L_a. The identifier families here are SHAPES, and these shapes are
# also standard physics notation. This is a shape rule, not a judgement about
# any particular token, and every name in the bucket is listed in full below
# so a genuinely missing short-named lemma is still visible.
SHORT_SYMBOL = re.compile(r"^[TL]_[A-Za-z0-9]{1,3}$")


# ===========================================================================
# THREE FURTHER SURFACES THE CORPUS NAMES AN OBJECT ON.
#
# The two resolvers above -- a `def` under apf/, a key in the loaded registry
# -- are not the only places the corpus PUBLISHES a name.  Reading only those
# two is a demonstrated defect: on 2026-08-07 a seat took this tool's residue
# as a work list and deleted four correct citations to live objects.  Three
# more surfaces, each decidable, each reported separately, each shipping a
# negative control that runs every time:
#
#   R3  ALIAS_TABLE_RESOLVED     apf/crystal.py's `_DEP_ALIASES` maps legacy
#                                and variant dependency spellings onto live
#                                registered checks.  A key of that table
#                                resolves TO its target -- and only if the
#                                target itself resolves.
#   R4  PUBLISHED_SUBCLAUSE      a check publishes keyed sub-lemmas with their
#                                own record fields INSIDE its returned
#                                structure (`L_cost_C1/C2/MAIN` in
#                                check_L_cost).  Neither a def nor a registry
#                                key; addressable and cross-referred anyway.
#   R5  GRAPH_OR_INVENTORY_NODE  a machine-enforced dependency graph declares
#                                its own node labels, and a pinned gate
#                                inventory lists them.  `T_CENTRAL_J` is not a
#                                def and was never meant to be one; it is a
#                                node of FULL_PARALLEL_GRAPH.
#
# OVER-RESOLUTION IS THE SELF-FAVOURING DIRECTION.  Every one of these can be
# written loosely enough to make the number fall without a single citation
# being repaired -- "any name in any list resolves" would make an allowlist of
# foreign names resolve to itself.  Each resolver therefore carries a shape
# test that a payload dict or an unanchored allowlist FAILS, and a negative
# control that demonstrates the failure on synthetic input.
# ===========================================================================

# R4: the clause key must be citation-shaped, and its parent prefix must be a
# citation-shaped name in its own right -- not the bare marker `T`/`L`/`check`,
# which resolve as ordinary defs in this tree and would swallow `T_munu`.
SUBCLAUSE_SHAPE = re.compile(r"^(?:check_|T_|L_)[A-Za-z0-9_]+$")
PARENT_SHAPE = re.compile(r"^(?:check_|T_|L_)[A-Za-z0-9][A-Za-z0-9_]*$")


def load_dep_aliases(repo):
    """apf/crystal.py's `_DEP_ALIASES`, read from the module -- never invented
    here.  Live import if the registry load already brought it in, AST literal
    otherwise, and an honest UNAVAILABLE if neither works."""
    try:
        mod = sys.modules.get("apf.crystal")
        if mod is None:
            sys.path.insert(0, repo)
            import importlib
            mod = importlib.import_module("apf.crystal")
        tab = getattr(mod, "_DEP_ALIASES", None)
        if isinstance(tab, dict) and tab:
            return dict(tab), "imported apf.crystal"
    except Exception:                                                 # noqa
        pass
    try:
        tree = ast.parse(open(os.path.join(repo, "apf", "crystal.py"),
                              encoding="utf-8", errors="replace").read())
        for nd in tree.body:
            tg = (nd.targets if isinstance(nd, ast.Assign)
                  else [nd.target] if isinstance(nd, ast.AnnAssign) else [])
            if any(isinstance(t, ast.Name) and t.id == "_DEP_ALIASES" for t in tg):
                return dict(ast.literal_eval(nd.value)), "parsed apf/crystal.py"
    except Exception:                                                 # noqa
        pass
    return {}, "UNAVAILABLE"


def resolve_alias(name, alias, defs, reg):
    """(alias_key, target, target_evidence) or None.

    Both registry spellings are tried on the LOOKUP (D6, 2026-08-03).  A
    DANGLING alias -- one whose target does not itself resolve -- is NOT a
    resolution; that is the third negative-control leg."""
    for key in (name, name[6:] if name.startswith("check_") else None,
                "check_" + name):
        if key and key in alias:
            tgt = alias[key]
            ok, ev = resolves_name(tgt, defs, reg)
            if ok:
                return key, tgt, ev
            return None
    return None


def build_subclause_index(sources, resolves):
    """name -> [binding sites], for sub-clauses PUBLISHED as keyed records
    inside a check.

    THE SHAPE, three clauses, all decidable:
      (i)   the key sits in a dict literal lexically inside a function whose
            own name resolves (a check);
      (ii)  its VALUE is a dict -- a record with its own fields.  A key whose
            value is a scalar is a data field, not a published object;
      (iii) the key reads `<parent>_<clause>` where `<parent>` is a
            citation-shaped name that RESOLVES.  The longest such prefix wins.
    A name that already resolves is not a sub-clause and is skipped."""
    idx = collections.defaultdict(list)
    for rel, tree in sources:
        for fn in ast.walk(tree):
            if not isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            if not resolves(fn.name):
                continue
            for nd in ast.walk(fn):
                if not isinstance(nd, ast.Dict):
                    continue
                for k, v in zip(nd.keys, nd.values):
                    if not (isinstance(k, ast.Constant)
                            and isinstance(k.value, str)):
                        continue
                    key = k.value
                    if not SUBCLAUSE_SHAPE.match(key) or resolves(key):
                        continue
                    if not isinstance(v, ast.Dict):          # (ii)
                        continue
                    parts = key.split("_")
                    parent = None
                    for i in range(len(parts) - 1, 0, -1):
                        cand = "_".join(parts[:i])
                        if len(cand) > 2 and PARENT_SHAPE.match(cand) \
                           and resolves(cand):
                            parent = cand
                            break
                    if parent is None:                       # (iii)
                        continue
                    idx[key].append(dict(
                        file=rel, published_by=fn.name, line=k.lineno,
                        parent=parent,
                        fields=sorted(kk.value for kk in v.keys
                                      if isinstance(kk, ast.Constant)
                                      and isinstance(kk.value, str))))
    return dict(idx)


def _string_seq(node):
    """The string members of a list/tuple/set literal, or None if any member
    is not a plain string."""
    if not isinstance(node, (ast.List, ast.Tuple, ast.Set)):
        return None
    out = []
    for e in node.elts:
        if isinstance(e, ast.Constant) and isinstance(e.value, str):
            out.append(e.value)
        else:
            return None
    return out


def _graph_dict(d):
    """(keys, members) if this dict literal is a DEPENDENCY GRAPH, else None.

    TWO clauses.  The first -- at least two values are all-string collections
    -- is not enough on its own: a returned `artifacts={...}` payload carrying
    `scope_in` / `scope_out` / `scope_suggestive` passes it, and its data-field
    keys would then read as theorem nodes.  The second clause is the machine
    test for a graph: at least one member of those collections is itself one
    of the dict's own keys -- an edge that lands on a declared node."""
    keys = {k.value for k in d.keys
            if isinstance(k, ast.Constant) and isinstance(k.value, str)}
    if len(keys) < 2:
        return None
    colls = [c for c in (_string_seq(v) for v in d.values) if c is not None]
    if len(colls) < 2:
        return None
    members = {m for c in colls for m in c}
    if not (members & keys):
        return None
    return keys, members


def _owner_map(tree):
    """id(node) -> the name of the assignment target whose value contains it."""
    out = {}
    for nd in ast.walk(tree):
        if not isinstance(nd, (ast.Assign, ast.AnnAssign)) or nd.value is None:
            continue
        tg = nd.targets if isinstance(nd, ast.Assign) else [nd.target]
        nm = None
        for t in tg:
            if isinstance(t, ast.Name):
                nm = t.id
        if nm:
            for sub in ast.walk(nd.value):
                out.setdefault(id(sub), nm)
    return out


def build_graph_node_index(sources):
    """name -> [binding sites], for labels DECLARED by a dependency graph.

    Both roles count: a dict KEY (the node) and a member of a value collection
    (the node an edge points at).  Graphs are found by shape, so the ones
    built inside a function -- `_dependency_graph()` in irrational_gate_holonomy
    -- count exactly like the module-level constants."""
    idx = collections.defaultdict(list)
    for rel, tree in sources:
        owner = _owner_map(tree)
        for nd in ast.walk(tree):
            if not isinstance(nd, ast.Dict):
                continue
            g = _graph_dict(nd)
            if g is None:
                continue
            struct = owner.get(id(nd), "(dict literal)")
            for k, v in zip(nd.keys, nd.values):
                if isinstance(k, ast.Constant) and isinstance(k.value, str):
                    idx[k.value].append(dict(file=rel, structure=struct,
                                             role="node key", line=k.lineno))
                sv = _string_seq(v)
                if sv:
                    for m in sv:
                        idx[m].append(dict(file=rel, structure=struct,
                                           role="edge member", line=v.lineno))
    return dict(idx)


def build_inventory_index(sources, graph_nodes):
    """name -> [binding sites], for members of a PINNED GATE INVENTORY.

    An inventory is a module-level ALLCAPS constant carrying string
    collections.  THE ANCHOR CLAUSE decides which ones count: the constant's
    own subtree must bind at least one name that the graph index already
    declares.  Without it every allowlist in the tree would resolve its own
    members to itself -- `PACKET_SOURCE_ALLOWLIST` names ten checks that live
    in an external packet and in no graph, and it stays in the residue because
    it carries no anchor.  This is the anti-tautology clause and the third
    negative-control leg tests it."""
    idx = collections.defaultdict(list)
    for rel, tree in sources:
        for nd in tree.body:
            if not isinstance(nd, (ast.Assign, ast.AnnAssign)) or nd.value is None:
                continue
            tg = nd.targets if isinstance(nd, ast.Assign) else [nd.target]
            cn = None
            for t in tg:
                if isinstance(t, ast.Name) and t.id.upper() == t.id \
                   and any(c.isalpha() for c in t.id):
                    cn = t.id
            if not cn:
                continue
            members, anchored = [], False
            for sub in ast.walk(nd.value):
                sv = _string_seq(sub)
                if sv:
                    for m in sv:
                        members.append((m, sub.lineno))
                        if m in graph_nodes:
                            anchored = True
                if isinstance(sub, ast.Dict):
                    for k in sub.keys:
                        if isinstance(k, ast.Constant) and \
                           isinstance(k.value, str) and k.value in graph_nodes:
                            anchored = True
            if not anchored:
                continue
            for m, ln in members:
                idx[m].append(dict(file=rel, structure=cn,
                                   role="inventory member", line=ln))
    return dict(idx)


# ===========================================================================
# THREE FURTHER SURFACES AGAIN -- S6 / S7 / S9.
#
# A blinded hand-adjudication of 40 residue instances (2026-08-08) put the
# genuine-defect rate at roughly one in eight.  The rest were not defects:
# the corpus names an object in more ways than the five resolvers above
# read.  Three more, each decidable, each reported alone, each shipping a
# negative control that runs on every invocation:
#
#   S6  ADJUDICATED_TYPED_ROOT   apf/ie_export_core_census.py carries
#                                FULL_SURFACE_TYPED_ROOTS -- a hand-ruled,
#                                hand-re-pinned inventory of EXACTLY the
#                                names the full-surface closure walk leaves
#                                unresolved, each typed into one of seven
#                                genres.  A name carried there has already
#                                been adjudicated by the corpus as declared
#                                debt.  ITS GENRE IS REPORTED, because a
#                                reader must be able to tell adjudicated
#                                debt from unnoticed vacancy, and because
#                                "named_unregistered" and "premise" are not
#                                the same fact about a citation.
#   S7  CASE_VARIANT_OF_LIVE     a check routinely reports itself under a
#                                result name whose CASE differs from its
#                                own def -- Check("T_AFFINITY_DERIVATION_
#                                EXECUTED") returned by
#                                check_T_affinity_derivation_executed;
#                                L_spectral_action_Higgs written one line
#                                above def check_L_spectral_action_higgs.
#                                WHAT IT MATCHED IS REPORTED, always.
#   S9  LIBRARY_PY_ARTIFACT      the tool resolves .md/.tex against the
#                                mounted library but .py against the repo
#                                ONLY.  So a parked lane's witness script is
#                                a guaranteed non-resolver even when it sits
#                                exactly where its docstring says -- under
#                                "The Turning (parked)/", "APF Reference
#                                Docs/scripts/", a closure pack beneath
#                                "Codebase/".  THE PATH IS REPORTED, because
#                                "exists but outside the tree" is a
#                                different fact from "exists in the tree"
#                                and a reader needs to see which.
#
# THE SAME HAZARD GOVERNS ALL THREE.  Over-resolution is the self-favouring
# direction: it makes the residue fall without a single citation being
# repaired.  S6 therefore matches EXACTLY, never by prefix or family (the
# inventory carries L_hierarchy; the corpus separately cites
# L_hierarchy_tightened, which is a different name and stays in the
# residue).  S7 tries the case-folded form only AFTER the exact form has
# failed, and never a substring.  S9 refuses vendored third-party trees --
# the library carries whole virtualenvs, and apf_utils.py's citations of its
# own _helpers.py / _constants.py / _linalg.py would otherwise "resolve"
# against numpy, pandas and scipy internals.  That is the basename-phantom
# defect this tool already has on record, one tree further out.
# ===========================================================================

# --------------------------------------------------------------------- S6
def load_typed_roots(repo):
    """apf/ie_export_core_census.py's FULL_SURFACE_TYPED_ROOTS, read from the
    module -- never restated here.  Live import first, AST literal second, an
    honest UNAVAILABLE third.  Reading it live is the point: the inventory is
    re-pinned by hand at landings that move it, and a copy taken here would
    be a receipt whose object had moved under it."""
    try:
        mod = sys.modules.get("apf.ie_export_core_census")
        if mod is None:
            sys.path.insert(0, repo)
            import importlib
            mod = importlib.import_module("apf.ie_export_core_census")
        tab = getattr(mod, "FULL_SURFACE_TYPED_ROOTS", None)
        if isinstance(tab, dict) and tab:
            return dict(tab), "imported apf.ie_export_core_census"
    except Exception:                                                 # noqa
        pass
    try:
        tree = ast.parse(open(os.path.join(repo, "apf",
                                           "ie_export_core_census.py"),
                              encoding="utf-8", errors="replace").read())
        for nd in tree.body:
            tg = (nd.targets if isinstance(nd, ast.Assign)
                  else [nd.target] if isinstance(nd, ast.AnnAssign) else [])
            if any(isinstance(t, ast.Name) and
                   t.id == "FULL_SURFACE_TYPED_ROOTS" for t in tg):
                return dict(ast.literal_eval(nd.value)), \
                    "parsed apf/ie_export_core_census.py"
    except Exception:                                                 # noqa
        pass
    return {}, "UNAVAILABLE"


def resolve_typed_root(name, roots):
    """The adjudicated GENRE, or None.

    TWO clauses, both decidable:
      (i)  EXACT key match.  No prefix, no case-fold, no `check_` spelling
           juggling.  The inventory is an adjudication of named rows, not a
           family allowlist, and a prefix rule here would silence every
           longer name that merely starts with an adjudicated one.
      (ii) the pinned value must be a NON-EMPTY STRING genre.  The inventory
           carries a placeholder key whose value is None (deleted at module
           level, but present in the AST literal); an untyped row has not
           been adjudicated and is not a resolution."""
    g = roots.get(name)
    if isinstance(g, str) and g:
        return g
    return None


# --------------------------------------------------------------------- S7
def build_casefold_index(defs, reg):
    """casefolded name -> [live names], over defs under apf/ and registry keys."""
    fdefs = collections.defaultdict(list)
    for d in defs:
        fdefs[d.lower()].append(d)
    freg = collections.defaultdict(list)
    for k in (reg or ()):
        freg[k.lower()].append(k)
    return dict(fdefs), dict(freg)


def resolve_case_variant(name, defs, reg, fdefs, freg):
    """(what it matched, evidence) or None.

    The exact form is tried FIRST and a hit there means this is not a case
    variant at all -- it is a resolution the tool already made, and this
    resolver must stay out of it.  Both registry spellings are tried on the
    fold (D6, 2026-08-03).  Equality of the case-folded strings, never a
    prefix and never a substring."""
    for cand in (name, "check_" + name):
        if cand in defs or (reg is not None and cand in reg):
            return None
    for cand in (name, "check_" + name):
        lc = cand.lower()
        if lc in fdefs:
            live = sorted(fdefs[lc])
            rel, ln = defs[live[0]][0]
            extra = ("  [%d live names share this fold]" % len(live)
                     if len(live) > 1 else "")
            return ("def " + live[0], f"{rel}:{ln}{extra}")
        if lc in freg:
            live = sorted(freg[lc])
            extra = ("  [%d registry keys share this fold]" % len(live)
                     if len(live) > 1 else "")
            return ("registry key " + live[0],
                    "registry-only (no def found under apf/)" + extra)
    return None


# --------------------------------------------------------------------- S9
# A vendored dependency is not a corpus artifact, and an archived copy under
# Old/ is not where a docstring says a script lives.  Path COMPONENTS, so the
# rule is decidable and does not depend on where a tree was rooted.  `Old` is
# excluded for the same reason index_repo() prunes it.
LIB_PY_SCOPE_EXCLUDE = {".venv", "venv", "site-packages", "dist-packages",
                        "node_modules", ".tox", ".eggs", "__pycache__",
                        ".git", ".pytest_cache", ".obsidian",
                        "Old", "_to_delete"}
# The DOCUMENT index prunes Codebase/ and Evidence/ for speed. This index does
# NOT: the closure packs beneath Codebase/ are exactly one of the three places
# a cited .py legitimately lives. The difference is printed.
LIB_PY_WALK_PRUNE = {"__pycache__", ".git", ".pytest_cache", ".obsidian"}


def _lib_py_in_scope(relpath):
    parts = relpath.replace(os.sep, "/").split("/")[:-1]
    return not any(p in LIB_PY_SCOPE_EXCLUDE for p in parts)


def index_library_py(lib):
    """.py basename -> [library relpath].  A SEPARATE walk from the document
    index, with a different prune set, so neither can move the other."""
    if not lib or not os.path.isdir(lib):
        return dict(py={}, present=False, files=0,
                    walk_pruned=sorted(LIB_PY_WALK_PRUNE),
                    scope_excluded=sorted(LIB_PY_SCOPE_EXCLUDE))
    py = collections.defaultdict(list)
    n = 0
    for root, dirs, names in os.walk(lib):
        dirs[:] = [d for d in dirs if d not in LIB_PY_WALK_PRUNE]
        for nm in names:
            if nm.endswith(".py"):
                n += 1
                py[nm].append(os.path.relpath(os.path.join(root, nm), lib)
                              .replace(os.sep, "/"))
    return dict(py=dict(py), present=True, files=n,
                walk_pruned=sorted(LIB_PY_WALK_PRUNE),
                scope_excluded=sorted(LIB_PY_SCOPE_EXCLUDE))


def resolve_library_py(name, libpy):
    """[in-scope library paths] or None.  Basename match, and the PATH comes
    back with it -- a basename match whose path is not reported is the
    phantom-resolution defect this tool has on record."""
    if not name.endswith(".py"):
        return None
    # SORTED: os.walk order is filesystem order, and a reported path that
    # changes between two runs over an unchanged tree is not a receipt.
    hits = sorted(p for p in libpy.get(name, ()) if _lib_py_in_scope(p))
    return hits or None


# --------------------------------------------------------- NEGATIVE CONTROLS
# Each resolver must still report ABSENT a name that is genuinely absent.
# These run on every invocation and their result is printed.  A control that
# reads FAILED means the resolver over-resolves and its contribution below may
# not be believed.
_NC_SUBCLAUSE_SRC = (
    'def check_L_cost():\n'
    '    payload = {\n'
    '        "L_cost_CONTROL_FLAT": "a scalar field, not a published record",\n'
    '        "L_control_absent_parent_C1": {"status": "P"},\n'
    '    }\n'
    '    return payload\n'
)

_NC_GRAPH_SRC = (
    'ARTIFACT_PAYLOAD = {\n'
    '    "T_CONTROL_PAYLOAD_FIELD": 0.5,\n'
    '    "T_CONTROL_OTHER_FIELD": 1.0,\n'
    '    "scope_in": ["rho_b", "rho_c"],\n'
    '    "scope_out": ["eta"],\n'
    '}\n'
    'CONTROL_UNANCHORED_ALLOWLIST = (\n'
    '    "check_T_control_foreign_packet_name",\n'
    '    "T_CONTROL_FOREIGN_NODE",\n'
    ')\n'
)


def negative_controls(alias, alias_src, sub_idx, graph_idx, inv_idx,
                      defs, reg, resolves,
                      roots, fdefs, freg, libpy):
    """Executable demonstrations that a genuinely absent name stays absent."""
    legs = []

    # ------------------------------------------------------------------ R3
    legs.append(("R3", "a name absent from the alias table does not resolve",
                 resolve_alias("L_control_absent_from_alias_table",
                               alias, defs, reg) is None))
    near = sorted(alias)[0] if alias else "L_x"
    legs.append(("R3", "an alias key plus a suffix (%s_control) does not "
                 "resolve -- exact key match, no prefix matching" % near,
                 resolve_alias(near + "_control", alias, defs, reg) is None))
    dangling = {"L_control_alias_src": "L_control_alias_target_that_is_absent"}
    legs.append(("R3", "an alias whose TARGET does not itself resolve is not "
                 "a resolution (dangling alias)",
                 resolve_alias("L_control_alias_src", dangling,
                               defs, reg) is None))

    # ------------------------------------------------------------------ R4
    legs.append(("R4", "a perfectly shaped but never-published clause "
                 "(L_cost_CONTROL_ABSENT_CLAUSE) is absent from the index",
                 "L_cost_CONTROL_ABSENT_CLAUSE" not in sub_idx))
    nc = build_subclause_index([("<control>", ast.parse(_NC_SUBCLAUSE_SRC))],
                               resolves)
    legs.append(("R4", "a clause key whose value is a scalar, not a record, "
                 "is not indexed", "L_cost_CONTROL_FLAT" not in nc))
    legs.append(("R4", "a clause key whose parent does not resolve is not "
                 "indexed", "L_control_absent_parent_C1" not in nc))

    # ------------------------------------------------------------------ R5
    legs.append(("R5", "a node label bound in no graph and no inventory "
                 "(T_CONTROL_ABSENT_NODE) is absent from both indexes",
                 "T_CONTROL_ABSENT_NODE" not in graph_idx
                 and "T_CONTROL_ABSENT_NODE" not in inv_idx))
    ncsrc = [("<control>", ast.parse(_NC_GRAPH_SRC))]
    ncg = build_graph_node_index(ncsrc)
    legs.append(("R5", "a payload dict carrying two string lists but no edge "
                 "landing on its own key is NOT a graph",
                 "T_CONTROL_PAYLOAD_FIELD" not in ncg))
    nci = build_inventory_index(ncsrc, ncg)
    legs.append(("R5", "an inventory anchored to no graph node does not "
                 "resolve its own members",
                 "T_CONTROL_FOREIGN_NODE" not in nci
                 and "check_T_control_foreign_packet_name" not in nci))
    live = "check_T_operational_norm_invariant_pairing_from_complete_readouts"
    legs.append(("R5", "LIVE PROBE: PACKET_SOURCE_ALLOWLIST carries no anchor, "
                 "so its ten foreign packet names stay in the residue "
                 "(probe: " + live[:40] + "...)",
                 live not in graph_idx and live not in inv_idx))

    # ------------------------------------------------------------------ S6
    legs.append(("S6", "a name absent from FULL_SURFACE_TYPED_ROOTS does not "
                 "resolve (L_control_absent_from_typed_roots)",
                 resolve_typed_root("L_control_absent_from_typed_roots",
                                    roots) is None))
    legs.append(("S6", "EXACT match only, no prefix and no family rule -- "
                 "LIVE PROBE: 'L_hierarchy' IS pinned in the inventory and "
                 "'L_hierarchy_tightened' is NOT, so the longer name stays "
                 "in the residue",
                 ("L_hierarchy" in roots)
                 and resolve_typed_root("L_hierarchy_tightened", roots) is None))
    legs.append(("S6", "an inventory row carrying no genre string is not an "
                 "adjudication and does not resolve",
                 resolve_typed_root("L_control_untyped",
                                    {"L_control_untyped": None,
                                     "L_control_blank": ""}) is None
                 and resolve_typed_root("L_control_blank",
                                        {"L_control_blank": ""}) is None))
    legs.append(("S6", "an UNAVAILABLE inventory resolves nothing at all "
                 "(the resolver is inert, never permissive, when it cannot "
                 "read its source)",
                 resolve_typed_root("L_crossing_correction", {}) is None))

    # ------------------------------------------------------------------ S7
    legs.append(("S7", "a name with no live case-variant "
                 "(T_CONTROL_ABSENT_CASE_VARIANT) does not resolve",
                 resolve_case_variant("T_CONTROL_ABSENT_CASE_VARIANT",
                                      defs, reg, fdefs, freg) is None))
    legs.append(("S7", "a name differing by MORE than case does not resolve "
                 "(check_T_affinity_derivation_executedd, one letter added)",
                 resolve_case_variant("check_T_affinity_derivation_executedd",
                                      defs, reg, fdefs, freg) is None))
    legs.append(("S7", "the fold is EQUALITY, not prefix or substring: "
                 "T_KNEE_CONTROL_SUFFIX does not resolve even though a live "
                 "T_knee exists",
                 resolve_case_variant("T_KNEE_CONTROL_SUFFIX",
                                      defs, reg, fdefs, freg) is None))
    legs.append(("S7", "LIVE PROBE: L_hierarchy_tightened case-folds onto no "
                 "live def or registry key and stays in the residue",
                 resolve_case_variant("L_hierarchy_tightened",
                                      defs, reg, fdefs, freg) is None))

    # ------------------------------------------------------------------ S9
    legs.append(("S9", "a .py name absent from the library does not resolve "
                 "(control_absent_witness_script.py)",
                 resolve_library_py("control_absent_witness_script.py",
                                    libpy) is None))
    absent = ["witness_2_delta_reader_pricing.py",
              "dictionary_typing_walk_witness.py",
              "build_interface_atlas.py"]
    legs.append(("S9", "LIVE PROBE: three scripts cited from apf/ as living "
                 "in lane folders THAT DO NOT EXIST are still reported absent "
                 "(" + ", ".join(absent) + ")",
                 all(resolve_library_py(a, libpy) is None for a in absent)))
    vendored = ["_helpers.py", "_constants.py", "_linalg.py"]
    present_somewhere = [v for v in vendored if libpy.get(v)]
    legs.append(("S9", "LIVE PROBE: apf_utils.py's own _helpers/_constants/"
                 "_linalg are present in the library ONLY inside vendored "
                 "virtualenvs (%d of 3 seen on disk) and are NOT resolved "
                 "against numpy/pandas/scipy internals"
                 % len(present_somewhere),
                 all(resolve_library_py(v, libpy) is None for v in vendored)))
    legs.append(("S9", "a script present ONLY under an archival Old/ path is "
                 "not where a docstring says it lives and does not resolve",
                 resolve_library_py(
                     "control_archived_only.py",
                     {"control_archived_only.py":
                      ["APF Reference Docs/Old/control_archived_only.py"]})
                 is None))
    legs.append(("S9", "the same script one directory up, OUTSIDE Old/, does "
                 "resolve -- the exclusion is the path, not the name "
                 "(positive counterpart, so the leg above cannot pass "
                 "vacuously)",
                 resolve_library_py(
                     "control_archived_only.py",
                     {"control_archived_only.py":
                      ["APF Reference Docs/control_archived_only.py"]})
                 == ["APF Reference Docs/control_archived_only.py"]))
    return legs



def _resolve_library_root():
    """Locate the mounted __APF Library WITHOUT hardcoding a sandbox session id.

    THE DEFECT THIS REPLACES, recorded because it silently disabled a control.
    This module previously defaulted to a literal
    `/sessions/<some-old-session>/mnt/__APF Library/...` path. Sandbox session
    ids are minted PER SESSION, so that path is dead the moment the session
    that wrote it ends. Run with defaults thereafter, the tool read ZERO papers
    and still printed a plausible-looking number, and both of its controls
    reported FILE NOT FOUND -- CONTROL DID NOT RUN. A tool whose positive
    control cannot run cannot demonstrate that it detects anything.

    Order: explicit env var, then any live sandbox mount by GLOB (never a
    literal id), then the two known Windows usernames. Returns None if nothing
    resolves -- the caller must say so rather than proceed silently.
    """
    import glob as _glob
    env = os.environ.get("APF_LIBRARY_ROOT")
    if env and os.path.isdir(env):
        return env
    for pat in ("/sessions/*/mnt/__APF Library",
                "/sessions/*/mnt/*/__APF Library"):
        for hit in sorted(_glob.glob(pat)):
            if os.path.isdir(hit):
                return hit
    for guess in (os.path.expanduser("~/My Drive/__APF Library"),
                  r"C:\Users\EthanBrooke\My Drive\__APF Library",
                  r"C:\Users\brook\My Drive\__APF Library"):
        if os.path.isdir(guess):
            return guess
    return None


def main(argv):
    lib = None
    if "--library" in argv:
        lib = argv[argv.index("--library") + 1]
    else:
        # Resolve the mount; never hardcode a sandbox session id. A literal
        # /sessions/<id>/ path is dead the moment that session ends, and this
        # tool then reports "library index 0" and proceeds -- every library
        # -facing classification silently wrong, no error raised.
        lib = _resolve_library_root()
    out_json = (argv[argv.index("--json") + 1] if "--json" in argv
                else os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                  "vacancy_census.json"))

    idx = index_repo(REPO)
    defs, modules, bound = idx["defs"], idx["modules"], idx["bound"]
    defs_other = idx["defs_other"]
    reg, reg_n, reg_exp = load_registry(REPO)
    arch, standalone, bankmods = load_manifest(REPO)
    libidx = index_library(lib)

    # --------------------------------------------------------- DISCOVER pass
    if "--discover" in argv:
        return discover(idx)

    print("=" * 78)
    print("VACANCY CENSUS -- a reporting tool.  No claim, no judgement.")
    print("=" * 78)
    print(f"repo             {REPO}")
    print("library          " + (lib if libidx["present"]
                                 else "(NOT MOUNTED -- document stage degraded)"))
    if libidx["present"]:
        print("library pruned   " + ", ".join(libidx["pruned"]) +
              "  (a doc living ONLY under one of these reads as not-found)")
    print(f"registry         {reg_n} loaded / EXPECTED {reg_exp}"
          if reg is not None else f"registry         UNAVAILABLE ({reg_exp})")
    print(f"code index       {len(defs)} distinct def names under apf/, "
          f"{len(idx['relpaths'])} .py files, {len(bound)} bound Python names")
    print(f"                 {len(defs_other)} further def names elsewhere in the "
          f"repo -- REPORTED, never used to resolve")
    print(f"library index    {len(libidx['docs'])} distinct .md/.tex/.pdf filenames")

    # documents resolve against the library AND this repo (REVIEWER_ATLAS.md,
    # CHANGELOG.md and friends live here, not in the library).
    docnames = dict(libidx["docs"])
    for n in idx["allfiles"]:
        docnames.setdefault(n, ["(this repo)"])

    # ------------------------------------------------------------ (2) COVERAGE
    apf_files = sorted(r for r in idx["relpaths"] if r.startswith("apf/"))
    apf_failed = [r for r, _ in idx["failed"] if r.startswith("apf/")]
    apf_parsed = [r for r in idx["parsed"] if r.startswith("apf/")]
    print()
    print(f"(2) COVERAGE     {len(apf_parsed)}/{len(apf_files)} files under apf/ "
          f"parsed = {100.0*len(apf_parsed)/max(1,len(apf_files)):.2f}%")
    if apf_failed:
        print("    FILES NOT PARSED (named, every one):")
        for r in apf_failed:
            print(f"      {r}")
    else:
        print("    FILES NOT PARSED: none.")
    other_failed = [r for r, _ in idx["failed"] if not r.startswith("apf/")]
    if other_failed:
        print(f"    (outside apf/, indexed for resolution only, {len(other_failed)} "
              f"unparsed: {', '.join(other_failed[:6])}"
              f"{' ...' if len(other_failed) > 6 else ''})")

    # ------------------------------------------------- R3 / R4 / R5 indexes
    # Built once, over the same parsed apf/ set the scan uses.  These decide
    # only rows that would otherwise have fallen through to RESIDUE; they are
    # consulted after every pre-existing bucket test, so no existing bucket
    # can lose a row to them.
    def _resolves(nm):
        return resolves_name(nm, defs, reg)[0]

    apf_sources = []
    for _rel in apf_parsed:
        try:
            apf_sources.append((_rel, ast.parse(
                open(os.path.join(REPO, _rel), encoding="utf-8",
                     errors="replace").read())))
        except Exception:                                             # noqa
            continue
    dep_alias, alias_src = load_dep_aliases(REPO)
    subclause_idx = build_subclause_index(apf_sources, _resolves)
    graph_idx = build_graph_node_index(apf_sources)
    inventory_idx = build_inventory_index(apf_sources, graph_idx)
    print()
    print(f"R3 alias table    {len(dep_alias)} entries ({alias_src})")
    print(f"R4 subclause idx  {len(subclause_idx)} published sub-clauses")
    print(f"R5 graph idx      {len(graph_idx)} declared graph node labels; "
          f"{len(inventory_idx)} anchored inventory members")
    typed_roots, roots_src = load_typed_roots(REPO)
    fold_defs, fold_reg = build_casefold_index(defs, reg)
    libpyidx = index_library_py(lib)
    libpy = libpyidx["py"]
    root_genres = collections.Counter(
        g for g in typed_roots.values() if isinstance(g, str) and g)
    print(f"S6 typed roots    {len(typed_roots)} pinned rows ({roots_src}); "
          f"genres " + ", ".join(f"{g}={n}" for g, n in
                                 sorted(root_genres.items())))
    print(f"S7 casefold idx   {len(fold_defs)} folded def names, "
          f"{len(fold_reg)} folded registry keys")
    if libpyidx["present"]:
        print(f"S9 library .py   {len(libpy)} distinct .py basenames over "
              f"{libpyidx['files']} files -- SEPARATE walk from the document "
              f"index, which prunes Codebase/ and Evidence/; this one does "
              f"not, because a closure pack under Codebase/ is one of the "
              f"three places a cited .py legitimately lives.")
        print(f"                  scope-excluded path components: "
              + ", ".join(libpyidx["scope_excluded"]))
    else:
        print("S9 library .py    library NOT MOUNTED -- resolver inert, "
              "contributes 0")

    # ------------------------------------------------------------- (1) SCAN
    rows = []
    by_carrier = collections.Counter()
    by_family = collections.Counter()
    const_keys = {}
    for rel in apf_parsed:
        src = open(os.path.join(REPO, rel), encoding="utf-8", errors="replace").read()
        units, ok, ckeys = scan_file(rel, src)
        const_keys[rel] = ckeys
        for base_ln, carrier, text in units:
            structured = bool(STRUCTURED_CARRIER.match(carrier))
            norm, nmap = normalize_ws(text)
            for fam, pat in FAMILIES.items():
                # DOC_FILE / DOC_LOC are matched on the whitespace-collapsed
                # copy: both routinely wrap across lines inside one docstring.
                use_norm = fam in ("DOC_FILE", "DOC_LOC", "PAPER")
                hay = norm if use_norm else text
                for m in pat.finditer(hay):
                    name = m.group(0).strip()
                    start = nmap[m.start()] if use_norm else m.start()
                    end = nmap[min(m.end(), len(nmap) - 1)] if use_norm else m.end()
                    ln = base_ln + text.count("\n", 0, start)
                    rows.append(dict(file=rel, line=ln, carrier=carrier,
                                     family=fam, name=name,
                                     tail=text[end:end + 60]))
            if structured or carrier.startswith("CONST:") or \
               PREMISE_CONSTS.search(carrier):
                for m in PREMISE_TOKEN.finditer(text):
                    nm = m.group(0)
                    if nm in ("TODO", "NOTE", "XXX"):
                        continue
                    rows.append(dict(file=rel, line=base_ln + text.count("\n", 0, m.start()),
                                     carrier=carrier, family="PREMISE_CONST",
                                     name=nm, tail=""))
                for m in AXIOM_TOKEN.finditer(text):
                    rows.append(dict(file=rel, line=base_ln + text.count("\n", 0, m.start()),
                                     carrier=carrier, family="AXIOM_ID",
                                     name=m.group(0), tail=""))
            # DEF_* is a declared premise shape wherever it appears, prose included.
            if not (structured or carrier.startswith("CONST:")):
                for m in re.finditer(r"\bDEF_[A-Z0-9_]+", text):
                    rows.append(dict(file=rel, line=base_ln + text.count("\n", 0, m.start()),
                                     carrier=carrier, family="PREMISE_CONST",
                                     name=m.group(0), tail=""))

    for r in rows:
        by_carrier[r["carrier"]] += 1
        by_family[r["family"]] += 1

    print()
    print(f"(1) POPULATION   {len(rows)} citation instances, "
          f"{len({(r['family'], r['name']) for r in rows})} distinct (family, name) pairs")
    print("    Instances, not names.  Two citations on one line are two instances.")

    # ------------------------------------------------------- IDIOM INVENTORY
    print()
    print("IDIOM INVENTORY -- the carriers a citation actually rides in.")
    print("Derived by AST survey, not assumed.  Re-run --discover on a moved tree.")
    print(f"{'carrier':<34s}{'instances':>10s}{'share':>9s}")
    tot = max(1, len(rows))
    for c, n in by_carrier.most_common(24):
        print(f"  {c:<32s}{n:>10d}{100.0*n/tot:>8.1f}%")
    if len(by_carrier) > 24:
        rest = sum(n for _, n in by_carrier.most_common()[24:])
        print(f"  {'... %d further carriers' % (len(by_carrier)-24):<32s}{rest:>10d}"
              f"{100.0*rest/tot:>8.1f}%")
    print()
    print("IDENTIFIER FAMILIES")
    for f, n in by_family.most_common():
        d = len({r['name'] for r in rows if r['family'] == f})
        print(f"  {f:<16s}{n:>8d} inst  {d:>6d} distinct")

    # ------------------------------------------------------------- RESOLVE
    unres = []
    for r in rows:
        fam, nm = r["family"], r["name"]
        if fam in ("CHECK", "THEOREM", "LEMMA"):
            ok, ev = resolves_name(nm, defs, reg, defs_other)
        elif fam == "MODULE":
            paths = modules.get(nm, [])
            inapf = [p for p in paths if p.startswith("apf/")]
            if inapf:
                ok, ev = True, inapf[0]
            elif paths:
                ok, ev = False, "OUTSIDE apf/: " + paths[0]
            else:
                ok, ev = False, ""
        elif fam == "PREMISE_CONST":
            ok = nm in bound
            ev = "assigned as a Python name" if ok else ""
        elif fam == "AXIOM_ID":
            ok, ev = resolves_name(nm, defs, reg, defs_other)
        elif fam == "DOC_FILE":
            cand, hits = resolve_doc(nm, docnames)
            r["name"] = nm = cand
            ok, ev = bool(hits), (hits[0] if hits else "")
            if not libidx["present"]:
                ok, ev = None, "library not mounted"
        elif fam == "DOC_LOC":
            ok, ev = None, "no document named at this site"
        elif fam == "PAPER":
            ok, ev = None, "paper reference"
        else:
            ok, ev = None, ""
        r["resolved"] = ok
        r["evidence"] = ev
        if ok is False:
            unres.append(r)

    print()
    print(f"(3) RAW NON-RESOLVERS   {len(unres)} instances, "
          f"{len({(r['family'], r['name']) for r in unres})} distinct")

    # -------------------------------------------------------------- BUCKETS
    # Named, decidable, applied in order.  Everything the corpus legitimately
    # leaves unresolved goes into a bucket that SAYS SO, so nobody hunts for
    # a check that was never meant to exist.  The anchor census's first run
    # reported ~109 axiom and premise IDs as failures; that is the mistake
    # these buckets exist to prevent.
    BUCKET_DOC = {
        "LINE_WRAPPED_NAME":
            "scanner artifact: the name is wrapped across a line inside one "
            "docstring; rejoining across the break resolves it.",
        "BOUND_AS_PYTHON_NAME":
            "the token is bound as a variable, parameter or import somewhere "
            "in the tree -- prose naming a local, not citing a corpus object.",
        "AXIOM_ID_NO_CODE_HOME":
            "an axiom / foundational-assumption identifier carried in a "
            "dependency list. It names a premise, not a def. Reported per name "
            "below because the corpus is not uniform here.",
        "CONSUMED_LEAF":
            "an ALLCAPS premise constant that is cited and never assigned. The "
            "corpus's own term. Population reported; nothing is ruled.",
        "PREFIX_OF_EXISTING_NAME":
            "no def of this exact name, but a longer def begins with it -- a "
            "family prefix used in prose ('the T_ACC identities').",
        "DEF_OUTSIDE_APF_ONLY":
            "a def of this name exists in the repo but NOT under apf/ -- root "
            "demo scripts, scripts/, harnesses. The defect that made the first "
            "run miss two known vacancies; now visible instead of resolved.",
        "LOCAL_GRAPH_NODE":
            "the token is a dict KEY of the same module-level constant that "
            "cites it -- a graph naming its own node, not citing the bank.",
        "SHORT_SYMBOL_SHAPE":
            "a T_/L_ token whose tail is <=3 characters and carries no "
            "underscore -- T_R, T_t, L_L, T_CMB. The identifier families are "
            "SHAPES and these shapes are also standard physics notation. "
            "Listed in full below, so a genuinely missing short-named lemma "
            "stays visible.",
        "OUTSIDE_APF":
            "a module that exists in this repo outside apf/ (scripts/, "
            "standalone/, harnesses). Present, just not where a reader assumes.",
        "EXTERNAL_DOCUMENT":
            "a document filename matching none of the corpus naming forms "
            "('Reference - ...', 'Paper...', 'APF...'): external literature "
            "sources and generated artifacts. Listed in full below.",
        "ALIAS_TABLE_RESOLVED":
            "R3: the name is a key of apf/crystal.py's _DEP_ALIASES, the "
            "corpus's own legacy/variant spelling table, and its target "
            "resolves. Listed below with what it resolves TO.",
        "PUBLISHED_SUBCLAUSE":
            "R4: the name is a sub-clause PUBLISHED as a keyed record with "
            "its own fields inside a check's returned structure -- neither a "
            "def nor a registry key, but a real addressable object. Listed "
            "below with its publishing check and its fields.",
        "GRAPH_OR_INVENTORY_NODE":
            "R5: the name is a node label DECLARED by a machine-enforced "
            "dependency graph, or a member of a gate inventory anchored to "
            "one. It was never meant to be a def. Listed below with where it "
            "is bound.",
        "ADJUDICATED_TYPED_ROOT":
            "S6: the name is pinned BY NAME in apf/ie_export_core_census.py's "
            "FULL_SURFACE_TYPED_ROOTS -- the hand-ruled inventory of exactly "
            "the names the full-surface closure walk leaves unresolved, each "
            "typed into one of seven genres. Adjudicated declared debt, not "
            "unnoticed vacancy. Listed below WITH ITS GENRE, because "
            "'premise' and 'named_unregistered' are not the same fact.",
        "CASE_VARIANT_OF_LIVE_NAME":
            "S7: no def or registry key of this exact spelling, but the "
            "case-folded form is a live def or a live registry key -- a check "
            "reporting itself under an ALLCAPS result name, or a citation "
            "capitalising a word its def does not. Listed below with what it "
            "matched.",
        "LIBRARY_PY_ARTIFACT":
            "S9: a cited .py that is not in this repo but IS in the mounted "
            "library -- a parked lane's witness script, a reference-docs "
            "script, a closure pack. EXISTS BUT OUTSIDE THE TREE is a "
            "different fact from exists in the tree; the path it was found "
            "at is listed below so a reader can see which.",
        "RESIDUE":
            "cited, no bucket applies, does not resolve. THIS IS THE LIST.",
    }
    CORPUS_DOC = re.compile(r"^(?:Reference\b|Paper[_ ]|APF[_ ])")

    def bucket(r):
        fam, nm = r["family"], r["name"]
        if fam in ("CHECK", "THEOREM", "LEMMA"):
            if nm.endswith("_"):
                tail = re.match(r"[ \t]*\n?[ \t]*([A-Za-z0-9_]+)", r.get("tail", ""))
                if tail:
                    joined = nm + tail.group(1)
                    if resolves_name(joined, defs, reg)[0]:
                        r["rejoined"] = joined
                        return "LINE_WRAPPED_NAME"
            if r["evidence"].startswith("OUTSIDE apf/"):
                return "DEF_OUTSIDE_APF_ONLY"
            if nm in bound:
                return "BOUND_AS_PYTHON_NAME"
            if r["carrier"].startswith("CONST:") and \
               nm in const_keys.get(r["file"], {}).get(r["carrier"][6:], ()):
                return "LOCAL_GRAPH_NODE"
            if prefix_of_existing(nm, defs):
                r["prefix_example"] = prefix_of_existing(nm, defs)
                return "PREFIX_OF_EXISTING_NAME"
            if SHORT_SYMBOL.match(nm):
                return "SHORT_SYMBOL_SHAPE"
            # R3 / R4 / R5.  Consulted LAST, so every pre-existing bucket
            # keeps every row it already had; only what would have been
            # RESIDUE can move.
            hit = resolve_alias(nm, dep_alias, defs, reg)
            if hit:
                r["resolver"] = "R3"
                r["resolves_to"] = hit[1]
                r["resolver_evidence"] = f"_DEP_ALIASES['{hit[0]}'] -> {hit[1]}"
                return "ALIAS_TABLE_RESOLVED"
            if nm in subclause_idx:
                site = subclause_idx[nm][0]
                r["resolver"] = "R4"
                r["resolves_to"] = site["parent"]
                r["resolver_evidence"] = (
                    f"published by {site['published_by']} at {site['file']}:"
                    f"{site['line']} as a record keyed under parent "
                    f"{site['parent']}, fields {site['fields']}")
                return "PUBLISHED_SUBCLAUSE"
            if nm in graph_idx or nm in inventory_idx:
                site = (graph_idx.get(nm) or inventory_idx.get(nm))[0]
                r["resolver"] = "R5"
                r["resolves_to"] = site["structure"]
                r["resolver_evidence"] = (
                    f"bound as {site['role']} of {site['structure']} at "
                    f"{site['file']}:{site['line']}")
                return "GRAPH_OR_INVENTORY_NODE"
            # S7 before S6: a name that case-folds onto a LIVE object is
            # resolved by that object, and only a name resolving nowhere can
            # be adjudicated debt. (No name on this tree is both; the order
            # is recorded so it stays decidable if one ever is.)
            cv = resolve_case_variant(nm, defs, reg, fold_defs, fold_reg)
            if cv:
                r["resolver"] = "S7"
                r["resolves_to"] = cv[0]
                r["resolver_evidence"] = f"case-folds onto {cv[0]} at {cv[1]}"
                return "CASE_VARIANT_OF_LIVE_NAME"
            genre = resolve_typed_root(nm, typed_roots)
            if genre:
                r["resolver"] = "S6"
                r["resolves_to"] = genre
                r["genre"] = genre
                r["resolver_evidence"] = (
                    f"pinned in FULL_SURFACE_TYPED_ROOTS "
                    f"({roots_src}) with adjudicated genre '{genre}'")
                return "ADJUDICATED_TYPED_ROOT"
            return "RESIDUE"
        if fam == "AXIOM_ID":
            if r["evidence"].startswith("OUTSIDE apf/"):
                return "DEF_OUTSIDE_APF_ONLY"
            return "AXIOM_ID_NO_CODE_HOME"
        if fam == "PREMISE_CONST":
            return "CONSUMED_LEAF"
        if fam == "MODULE":
            if r["evidence"].startswith("OUTSIDE apf/"):
                return "OUTSIDE_APF"
            paths = resolve_library_py(nm, libpy)
            if paths:
                r["resolver"] = "S9"
                r["resolves_to"] = paths[0]
                r["library_paths"] = paths[:6]
                r["resolver_evidence"] = (
                    "not in this repo; found in the library at "
                    + paths[0]
                    + (f"  (+{len(paths)-1} further copies)"
                       if len(paths) > 1 else ""))
                return "LIBRARY_PY_ARTIFACT"
            return "RESIDUE"
        if fam == "DOC_FILE" and not CORPUS_DOC.match(r["name"].strip()):
            return "EXTERNAL_DOCUMENT"
        return "RESIDUE"

    for r in unres:
        r["bucket"] = bucket(r)

    bcount = collections.Counter(r["bucket"] for r in unres)
    residue = [r for r in unres if r["bucket"] == "RESIDUE"]

    print()
    print("NAMED BUCKETS -- non-resolvers the corpus leaves open by design or")
    print("that this scanner produced itself.  Named so nobody hunts for them.")
    for b, n in bcount.most_common():
        d = len({r["name"] for r in unres if r["bucket"] == b})
        print(f"  {b:<26s}{n:>7d} inst {d:>5d} distinct")
        print(f"    {BUCKET_DOC[b]}")

    ss = sorted({r["name"] for r in unres if r["bucket"] == "SHORT_SYMBOL_SHAPE"})
    if ss:
        print("  SHORT_SYMBOL_SHAPE names, in full:")
        for i in range(0, len(ss), 8):
            print("    " + "  ".join(f"{x:<9s}" for x in ss[i:i + 8]))

    # -------------------------------------------- R3 / R4 / R5 CONTRIBUTIONS
    print()
    print("=" * 78)
    print("R3 / R4 / R5 / S6 / S7 / S9 -- THE SIX FURTHER SURFACES THE CORPUS")
    print("NAMES AN OBJECT ON, EACH REPORTED ALONE.  Every instance below LEFT")
    print("the residue under exactly one resolver, resolving to exactly the")
    print("object named.  Reconcile the movement here.")
    print("=" * 78)
    nc_legs = negative_controls(dep_alias, alias_src, subclause_idx, graph_idx,
                                inventory_idx, defs, reg, _resolves,
                                typed_roots, fold_defs, fold_reg, libpy)
    print("NEGATIVE CONTROLS -- a genuinely absent name must STILL be reported")
    print("absent while the resolver is live.  Over-resolution is the")
    print("self-favouring direction: it moves the number with nothing repaired.")
    for tag, desc, ok in nc_legs:
        print(f"  [{tag}] {'PASS' if ok else 'FAILED -- OVER-RESOLVES'}  {desc}")
    nc_failed = [l for l in nc_legs if not l[2]]
    print(f"  {len(nc_legs) - len(nc_failed)}/{len(nc_legs)} controls PASS."
          + ("" if not nc_failed else
             "  ONE OR MORE FAILED -- the contributions below MAY NOT BE "
             "BELIEVED."))

    contrib = {}
    for label, tag in (("ALIAS_TABLE_RESOLVED", "R3"),
                       ("PUBLISHED_SUBCLAUSE", "R4"),
                       ("GRAPH_OR_INVENTORY_NODE", "R5"),
                       ("ADJUDICATED_TYPED_ROOT", "S6"),
                       ("CASE_VARIANT_OF_LIVE_NAME", "S7"),
                       ("LIBRARY_PY_ARTIFACT", "S9")):
        rs = [r for r in unres if r["bucket"] == label]
        names = collections.Counter(r["name"] for r in rs)
        contrib[tag] = dict(bucket=label, instances=len(rs),
                            distinct=len(names),
                            names={k: v for k, v in names.items()})
        if tag == "S6":
            gc = collections.Counter(r.get("genre") for r in rs)
            contrib[tag]["genres"] = dict(gc)
        print()
        print(f"{tag}  {label}: {len(rs)} instances left the residue, "
              f"{len(names)} distinct names.")
        if tag == "S6":
            gc = collections.Counter(r.get("genre") for r in rs)
            print("      ADJUDICATED GENRES: " +
                  (", ".join(f"{g} = {c} inst" for g, c in sorted(gc.items()))
                   if gc else "(none)"))
        for nmx, c in names.most_common():
            ex = next(r for r in rs if r["name"] == nmx)
            sites = ", ".join(f"{x['file'].split('/')[-1]}:{x['line']}"
                              for x in rs if x["name"] == nmx)
            print(f"  {c:4d}x  {nmx}")
            print(f"          RESOLVES TO: {ex.get('resolver_evidence', '')}")
            print(f"          sites: {sites[:300]}"
                  f"{' ...' if len(sites) > 300 else ''}")

    print()
    print(f"(4) RESIDUE      {len(residue)} instances, "
          f"{len({(r['family'], r['name']) for r in residue})} distinct")

    # ------------------------------------------------------- residue listing
    print()
    print("=" * 78)
    print("RESIDUE -- cited inside apf/, does not resolve, no bucket applies.")
    print("=" * 78)
    print("STRUCTURED carriers first: a name in a dependency / cross_refs /")
    print("premise field is a machine-readable citation, not prose.")
    grouped = collections.defaultdict(list)
    for r in residue:
        grouped[(r["family"], r["name"])].append(r)

    def sortkey(kv):
        (fam, nm), rs = kv
        struct = any(STRUCTURED_CARRIER.match(x["carrier"]) for x in rs)
        return (not struct, -len(rs), fam, nm)

    for (fam, nm), rs in sorted(grouped.items(), key=sortkey):
        struct = sorted({x["carrier"] for x in rs
                         if STRUCTURED_CARRIER.match(x["carrier"])})
        tag = ("  [STRUCTURED: " + ", ".join(struct) + "]") if struct else ""
        sites = ", ".join(f"{x['file'].split('/')[-1]}:{x['line']}" for x in rs[:4])
        more = f" (+{len(rs)-4})" if len(rs) > 4 else ""
        print(f"  {len(rs):4d}x  {fam:<9s} {nm}{tag}")
        print(f"            {sites}{more}")

    # ------------------------------------------ per-name axiom / premise detail
    print()
    print("=" * 78)
    print("AXIOM IDs CARRIED AS DEPENDENCIES -- per name, because the corpus")
    print("is not uniform.  RESOLVED means a def of that name exists.")
    print("=" * 78)
    ax = collections.Counter(r["name"] for r in rows if r["family"] == "AXIOM_ID")
    for nm, c in ax.most_common():
        ok, ev = resolves_name(nm, defs, reg, defs_other)
        print(f"  {nm:<14s}{c:>6d} inst   "
              f"{('RESOLVED  ' + ev) if ok else ('NO CODE HOME UNDER apf/' + ('  [' + ev + ']' if ev else ''))}")

    print()
    print("=" * 78)
    print("PREMISE CONSTANTS -- cited, and whether ever ASSIGNED as a Python")
    print("name anywhere in this tree.  A name only ever consumed is what the")
    print("corpus calls a CONSUMED LEAF.  Population reported; nothing ruled.")
    print("=" * 78)
    pc = collections.Counter(r["name"] for r in rows if r["family"] == "PREMISE_CONST")
    never = [(n, c) for n, c in pc.most_common() if n not in bound]
    print(f"  {len(pc)} distinct premise constants cited; "
          f"{len(never)} are never assigned ({sum(c for _, c in never)} instances).")
    for n, c in never[:40]:
        print(f"    {c:5d}  {n}")
    if len(never) > 40:
        print(f"    ... {len(never)-40} more (see JSON)")

    # ----------------------------------------------------- DOCUMENT stage
    print()
    print("=" * 78)
    print("DOCUMENTS CITED FROM CODE")
    print("=" * 78)
    dfs = [r for r in rows if r["family"] == "DOC_FILE"]
    dmiss = [r for r in dfs if r["resolved"] is False]
    print(f"  {len(dfs)} document-filename citations, "
          f"{len({r['name'].strip() for r in dfs})} distinct.")
    if libidx["present"]:
        corpus = [r for r in dmiss if r.get("bucket") != "EXTERNAL_DOCUMENT"]
        ext = [r for r in dmiss if r.get("bucket") == "EXTERNAL_DOCUMENT"]
        print(f"  NOT FOUND: {len(dmiss)} instances, "
              f"{len({r['name'].strip() for r in dmiss})} distinct "
              f"-- of which {len(corpus)} carry a corpus document name "
              f"('Reference - ...', 'Paper...', 'APF...') and {len(ext)} do not.")
        for label, group in (("CORPUS DOCUMENT NAMES NOT FOUND", corpus),
                             ("EXTERNAL / GENERATED FILENAMES NOT FOUND", ext)):
            seen = collections.defaultdict(list)
            for r in group:
                seen[r["name"].strip()].append(r)
            print(f"    -- {label} ({len(seen)} distinct) --")
            for nm, rs in sorted(seen.items(), key=lambda kv: -len(kv[1])):
                print(f"    {len(rs):3d}x  {nm}")
                print(f"          {rs[0]['file']}:{rs[0]['line']}")
    else:
        print("  Library not mounted; this stage did not run.")

    dl = [r for r in rows if r["family"] == "DOC_LOC"]
    print()
    print(f"  DOCUMENT LOCATIONS ('Prop 2.3', '§2.4', 'sec:foo'): {len(dl)} "
          f"instances, {len({r['name'] for r in dl})} distinct.")
    print("  UNRESOLVABLE BY DESIGN and counted separately, never as failures:")
    print("  a section number resolves only against a named document, and most")
    print("  of these sites name none.  Where a site DOES name a document, the")
    print("  document's own existence is decided above.")
    dfl = collections.defaultdict(set)
    for d in dfs:
        dfl[d["file"]].add(d["line"])
    near = [r for r in dl
            if any((r["line"] + k) in dfl.get(r["file"], ()) for k in (-2, -1, 0, 1, 2))]
    print(f"  Of those, {len(near)} sit within 2 lines of a document filename "
          f"(the only ones a resolver could chase).")

    pap = [r for r in rows if r["family"] == "PAPER"]
    print(f"  PAPER references: {len(pap)} instances, "
          f"{len({r['name'] for r in pap})} distinct -- also unresolvable by "
          f"design at this granularity.")

    # ------------------------------------------------------ REGISTRATION
    if reg is not None:
        print()
        print("=" * 78)
        print("REGISTRATION -- a cited name whose def EXISTS but which the bank")
        print("does not register.  NOT automatically a defect: helpers, record")
        print("factories, apf/standalone/ and the 53 architecture-only modules")
        print("register nothing BY DESIGN.  Sub-bucketed for that reason.")
        print("=" * 78)
        cited = [r for r in rows
                 if r["family"] in ("CHECK", "THEOREM", "LEMMA") and r["resolved"]]
        unreg = [r for r in cited
                 if r["name"] not in reg and ("check_" + r["name"]) not in reg]
        sub = collections.Counter()
        for r in unreg:
            home = defs.get(r["name"], defs.get("check_" + r["name"], [("", 0)]))[0][0]
            mod = home.replace("/", ".")[:-3] if home.endswith(".py") else home
            if home.startswith("apf/standalone/"):
                r["sub"] = "STANDALONE"
            elif os.path.basename(home) in HELD_FILES:
                r["sub"] = "HELD_OUT_OF_BANK"
            elif mod in arch:
                r["sub"] = "ARCHITECTURE_ONLY"
            elif not r["name"].startswith(("check_", "T_", "L_")):
                r["sub"] = "NOT_A_CHECK_NAME"
            else:
                r["sub"] = "UNREGISTERED_RESIDUE"
            sub[r["sub"]] += 1
        print(f"  {len(cited)} resolved name citations; {len(unreg)} name a def "
              f"the bank does not register ({len({r['name'] for r in unreg})} distinct).")
        for k, v in sub.most_common():
            d = len({r['name'] for r in unreg if r['sub'] == k})
            print(f"    {k:<24s}{v:>7d} inst {d:>5d} distinct")
        resid_names = sorted({r["name"] for r in unreg
                              if r["sub"] == "UNREGISTERED_RESIDUE"})
        print(f"  UNREGISTERED_RESIDUE names ({len(resid_names)}):")
        for i in range(0, len(resid_names), 2):
            print("     " + "  ".join(f"{x:<48s}" for x in resid_names[i:i + 2]))

    # ------------------------------------------- PAPERS PLAIN-TEXT SWEEP
    paper_rows = []
    if libidx["present"]:
        papers_root = os.path.join(lib, "Papers")
        paper_rows = sweep_papers(papers_root, defs, reg, defs_other)
        print()
        print("=" * 78)
        print("PAPERS, PLAIN-TEXT SWEEP -- complements scripts/anchor_census.py,")
        print("which reads ANCHOR MACROS only.  A check name typeset with plain")
        print("\\texttt{} or bare in a table row is invisible to it.  This stage")
        print("reads check-shaped names in LIVE .tex REGARDLESS of macro.")
        print("=" * 78)
        miss = [r for r in paper_rows if not r["resolved"]]
        print(f"  {len(paper_rows)} check-shaped names in live .tex; "
              f"{len(miss)} do not resolve "
              f"({len({r['name'] for r in miss})} distinct).")
        g = collections.defaultdict(list)
        for r in miss:
            g[r["name"]].append(r)
        for nm, rs in sorted(g.items(), key=lambda kv: -len(kv[1])):
            outside = [x for x in rs if not x["in_anchor"]]
            tag = "  <- NOT inside any anchor macro" if outside else ""
            print(f"    {len(rs):3d}x  {nm}{tag}")
            print(f"          {rs[0]['paper']}:{rs[0]['line']}")

    # ------------------------------------------------------------- SELF-CHECK
    print()
    print("=" * 78)
    print("KNOWN-VACANCY REPRODUCTION -- three vacancies found by hand on")
    print("2026-08-07, before this tool existed.  Missing any of them is a")
    print("DEFECT IN THIS TOOL and is printed as one.")
    print("=" * 78)
    v1 = [r for r in dmiss if "Conservation as the Shadow" in r["name"]]
    print(f"  (a) Prop 2.3's stated source document, cited from apf/core.py: "
          f"{'REPRODUCED' if v1 else 'MISSED -- DEFECT'}")
    for r in v1[:2]:
        print(f"      {r['file']}:{r['line']}  {r['name'].strip()}")
    v2 = [r for r in rows if r["family"] == "AXIOM_ID" and r["name"] == "MD"
          and r["resolved"] is False]
    print(f"  (b) MD carried as a dependency with no code home: "
          f"{'REPRODUCED' if v2 else 'MISSED -- DEFECT'}"
          f"  ({len(v2)} instances)")
    v3 = [r for r in paper_rows if r["name"] in ("check_L_iso", "check_MD")
          and not r["resolved"]]
    print(f"  (c) check_L_iso / check_MD cited in a live paper, absent from the "
          f"codebase: {'REPRODUCED' if v3 else 'MISSED -- DEFECT'}")
    for r in v3:
        print(f"      {r['paper']}:{r['line']}  {r['name']}"
              f"  (in anchor macro: {r['in_anchor']})")

    print()
    print("SUMMARY -- FOUR NUMBERS, SEPARATELY")
    print(f"  (1) POPULATION          {len(rows)}")
    print(f"  (2) COVERAGE            {len(apf_parsed)}/{len(apf_files)} = "
          f"{100.0*len(apf_parsed)/max(1,len(apf_files)):.2f}%")
    print(f"  (3) RAW NON-RESOLVERS   {len(unres)}")
    print(f"  (4) RESIDUE             {len(residue)}")

    payload = dict(
        repo=REPO, library=lib,
        registry_loaded=reg_n, registry_expected=reg_exp,
        coverage=dict(apf_files=len(apf_files), parsed=len(apf_parsed),
                      failed=[r for r, _ in idx["failed"]]),
        population=len(rows), raw_non_resolvers=len(unres),
        residue=len(residue),
        buckets={k: v for k, v in bcount.items()},
        resolver_contributions=contrib,
        resolver_indexes=dict(alias_entries=len(dep_alias),
                              alias_source=alias_src,
                              subclauses=len(subclause_idx),
                              graph_nodes=len(graph_idx),
                              inventory_members=len(inventory_idx),
                              typed_roots=len(typed_roots),
                              typed_roots_source=roots_src,
                              typed_root_genres=dict(root_genres),
                              casefold_defs=len(fold_defs),
                              casefold_registry=len(fold_reg),
                              library_py_basenames=len(libpy),
                              library_py_files=libpyidx["files"],
                              library_py_present=libpyidx["present"],
                              library_py_walk_pruned=libpyidx["walk_pruned"],
                              library_py_scope_excluded=libpyidx["scope_excluded"]),
        negative_controls=[dict(resolver=t, description=d, passed=bool(o))
                           for t, d, o in nc_legs],
        by_carrier=dict(by_carrier), by_family=dict(by_family),
        rows=sorted(rows, key=lambda r: (r["file"], r["line"], r["family"], r["name"])),
        paper_rows=sorted(paper_rows, key=lambda r: (r["paper"], r["line"], r["name"])),
    )
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=1, sort_keys=True)
    print(f"\nwrote {out_json}")
    print("\nThis tool reports whether a cited thing EXISTS.  It does not report")
    print("whether the citation is apt.  It fixes nothing.")
    return 0


# ================================================================== papers
ANCHOR_MACROS = ("coderef", "coderefbrk", "coderefcap", "codeid", "checkid", "bank")


def sweep_papers(papers_root, defs, reg, defs_other=None):
    """check-shaped names in LIVE .tex, regardless of the macro carrying them."""
    rows = []
    if not os.path.isdir(papers_root):
        return rows
    pat = re.compile(r"check(?:\\_|_)[A-Za-z0-9_\\]+")
    # \allowbreak and friends are typesetting inside a name, not part of it.
    tex_cs = re.compile(r"\\(?:allowbreak|linebreak|hspace|,|;|:|!|/|-)")
    anchor = re.compile(r"\\(?:%s)\b" % "|".join(ANCHOR_MACROS))
    for root, dirs, names in os.walk(papers_root):
        dirs[:] = [d for d in dirs if d not in ("Old", "_to_delete", "Reviews")]
        for n in sorted(names):
            if not n.endswith(".tex"):
                continue
            p = os.path.join(root, n)
            parts = os.path.relpath(p, papers_root).split(os.sep)
            if len(parts) != 2:                  # LIVE = paper-folder top level
                continue
            s = open(p, encoding="utf-8", errors="replace").read()
            anchors = [(m.start(), m.end()) for m in anchor.finditer(s)]
            for m in pat.finditer(s):
                nm = tex_cs.sub("", m.group(0)).replace("\\_", "_").rstrip("_\\")
                if nm in ("check", "check_"):
                    continue
                ok, ev = resolves_name(nm, defs, reg, defs_other)
                in_anchor = any(a <= m.start() <= b + 90 for a, b in anchors)
                rows.append(dict(paper=parts[0], file=parts[1],
                                 line=s.count("\n", 0, m.start()) + 1,
                                 name=nm, resolved=ok, evidence=ev,
                                 in_anchor=in_anchor))
    return rows


# ================================================================ discover
def discover(idx):
    """Idiom survey.  Enumerate the carriers before measuring anything.

    A census that greps ONE spelling undercounts.  This corpus has that on
    record twice: a leg-inventory census off by 2.3x, and an anchor sweep
    reading 40.8% of its own sites.  Run this first."""
    keys = collections.Counter()
    kws = collections.Counter()
    consts = collections.Counter()
    for rel in idx["parsed"]:
        if not rel.startswith("apf/"):
            continue
        try:
            t = ast.parse(open(os.path.join(REPO, rel), encoding="utf-8",
                               errors="replace").read())
        except Exception:                                            # noqa
            continue
        for nd in ast.walk(t):
            if isinstance(nd, ast.Dict):
                for k, v in zip(nd.keys, nd.values):
                    if isinstance(k, ast.Constant) and isinstance(k.value, str):
                        if isinstance(v, (ast.List, ast.Tuple, ast.Set)) and v.elts \
                           and all(isinstance(e, ast.Constant) and isinstance(e.value, str)
                                   for e in v.elts):
                            keys["LIST " + k.value] += 1
                        elif isinstance(v, ast.Constant) and isinstance(v.value, str):
                            keys["STR  " + k.value] += 1
            if isinstance(nd, ast.Call):
                for kw in nd.keywords:
                    if kw.arg:
                        kws[kw.arg] += 1
            if isinstance(nd, ast.Assign):
                for t2 in nd.targets:
                    if isinstance(t2, ast.Name) and t2.id.isupper():
                        consts[t2.id] += 1
    print("IDIOM SURVEY -- carriers, by live occurrence.  Marked entries are in")
    print("the tool's carrier lists; anything unmarked and frequent is a gap.")
    print("\n== keyword arguments ==")
    for k, c in kws.most_common(30):
        mark = ("  <- STRUCTURED" if k in STRUCTURED_FIELDS else
                "  <- PROSE" if k in PROSE_FIELDS else "")
        print(f"  {c:7d}  {k}{mark}")
    print("\n== dict keys carrying strings / string lists ==")
    for k, c in keys.most_common(40):
        bare = k[5:]
        mark = ("  <- STRUCTURED" if bare in STRUCTURED_FIELDS else
                "  <- PROSE" if bare in PROSE_FIELDS else "")
        print(f"  {c:7d}  {k}{mark}")
    print("\n== ALLCAPS module constants matching the premise shape ==")
    for k, c in consts.most_common(400):
        if PREMISE_CONSTS.search(k):
            print(f"  {c:7d}  {k}  <- PREMISE_CONSTS")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
