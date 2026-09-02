#!/usr/bin/env python3
r"""Contradiction census -- a REPORTING TOOL. Not a check. Not registered.

    python3 scripts/contradiction_census.py
    python3 scripts/contradiction_census.py --papers "<path to Papers>"
    python3 scripts/contradiction_census.py --json out.json --report out.txt
    python3 scripts/contradiction_census.py --idioms      # idiom inventory only
    python3 scripts/contradiction_census.py --controls    # run the two controls

Places where a paper and the executing code -- or two pieces of code, or one
docstring and its own returned record -- state the SAME FACT DIFFERENTLY, inside
a closed vocabulary where "differently" is decidable without judgement.

It reports the disagreement. It never rules which side is right.

WHY THIS IS NARROW, AND WHY IT STAYS NARROW
-------------------------------------------
A general prose-versus-code comparator is dead ground in this corpus. Working
Rule 17: an instrument that infers from syntax what the code never wrote down
is the wrong shape, and its audit findings will be infinite. A seat built
exactly that on 2026-08-06, returned 216 flags, hand-read nine, found six false
positives, and put its own instrument on the may-not-cite list. Two further
instruments in that genre were audited REDUCE twice each and deleted under a
standing do-not-repair ruling.

So this tool works only where BOTH SIDES STATE THE SAME KIND OF FACT IN A
CLOSED, ENUMERABLE VOCABULARY. Four fact types, all of them about the
field-selection sector, because that is where the corpus actually writes both
sides down in a fixed vocabulary:

  FS   a named TEST excludes or admits a named FIELD in {R, C, H}
  TT   the quaternionic composite M_n(H) (x)_R M_m(H) is M_<coef>(<field>),
       and its real dimension
  SD   a named FIELD departs from the tomographic count by a SURPLUS or a
       DEFICIT
  OD   an observable-space dimension: a closed-form formula per field, or the
       (2,2) joint/local pair

If a sentence has to be INTERPRETED to yield one of these, the span is dropped
and recorded in the residual, by site, rather than guessed at.

WHAT IT ASSERTS
---------------
  * a span of normalised text matches one of the named idioms in IDIOMS below,
    at a located line, and therefore states a fact of one of the four types;
  * two such facts share a key and carry different values;
  * the two facts sit in different sources (paper vs code, module vs module),
    or in the same source (an internal disagreement).

That is all. Membership in a bucket is a syntactic fact, not a verdict.

WHAT IT DOES NOT ASSERT, AND WILL NOT
-------------------------------------
  * WHICH SIDE IS RIGHT. Never. A disagreement is handed to a human.
  * That a disagreement is a DEFECT. Two sources can differ because they are
    describing different regimes under different conventions; the named buckets
    below exist for exactly that and are listed rather than hidden.
  * That a span it could not parse is clean. Every unmatched span is named.
  * Anything about a sentence whose meaning had to be inferred. Those are
    dropped, on purpose, and counted.

FOUR LESSONS THIS TOOL IS BUILT NOT TO REPEAT
---------------------------------------------
  * SURVEY THE IDIOMS AND DERIVE THE POPULATION; NEVER GREP ONE SPELLING. A
    census here undercounted by 2.3x that way, and the anchor census found six
    live reference idioms where everyone assumed one. The idioms below were
    enumerated by dumping every TEST-bearing span in both corpora and reading
    them; the inventory is an output of this tool (--idioms), not an
    assumption inside it.
  * REPORT COVERAGE AS A FRACTION, PROMINENTLY, AND NAME THE MISSES.
  * DO NOT DE-DUPLICATE AWAY REAL INSTANCES. Sites are counted individually;
    distinct value-pairs are reported separately from the site count.
  * PARTITION KNOWN-LEGITIMATE NON-MATCHES INTO NAMED BUCKETS AND LIST THEM.
    Changelog text STANDS AS WRITTEN by house convention and is never flagged.
    Retired text quoted inside its own correction is never flagged -- the house
    correction convention quotes the retired sentence, so a gate that flags
    that is structurally guaranteed to false-alarm (Working Rule 18).

WHITESPACE IS NORMALISED BEFORE ANY MATCHING (Working Rule 18: a gate that can
pass by accident of where a line wraps is not a gate). Every match runs against
a whitespace-collapsed string carrying an exact offset map back to the original,
so line numbers stay true.

CONTROLS
--------
POSITIVE: Paper 1 v5.9 (archived, pre-fix) attributed P_tom to H and P_cls to
R; the executing checks say the reverse. The tool MUST fire on v5.9.
NEGATIVE: Paper 1 v5.10 (live, post-fix) must NOT fire at those sites.
A census with no positive control certifies nothing.
"""
import os
import re
import io
import sys
import ast
import json
import bisect
import hashlib
import argparse
import tokenize
import collections
from array import array

# ===========================================================================
# THE CLOSED VOCABULARY
# ===========================================================================
# Derived by enumerating every TEST-bearing span in both corpora on 2026-08-07
# and reading them, not assumed. Re-run --idioms if a paper starts writing a
# verdict a new way; the residual list is where a new spelling shows up.

# --- tests -----------------------------------------------------------------
# canonical id -> the surface forms that name it
TEST_FORMS = {
    'P_tom': [
        r'P_\{\\mathrm\{tom\}\}', r'P\\_tom', r'\bP_tom\b', r'check\\?_P\\?_tom',
        r'\blocal\s+tomograph\w*', r'\bfinite\s+tomographic\s+locality\b',
        r'\btomographic\s+locality\b', r'\btomographic\s+completeness\b',
        r'\btomographic\s+closure\b', r'\btomography\b', r'\btomographic\b',
        r'Wootters[-\u2013\s]*-?\s*Hardy', r'tomographic_locality',
    ],
    'P_cls': [
        r'P_\{\\mathrm\{cls\}\}', r'P\\_cls', r'\bP_cls\b', r'check\\?_P\\?_cls',
        r'\bcompositional\s+closure\b', r'\bcomposite\s+closure\b',
        r'\b(?:finite\s+)?tensor\s+closure\b', r'\bfield-tensor\s+closure\b',
        r'tensor_closure',
    ],
}
# NOTE ON SCOPE. 'local independence' is a THIRD named test in this corpus
# (closed_world_completeness retypes H's departure as a local-INDEPENDENCE
# failure). It is deliberately NOT in the vocabulary: it appears three times in
# the whole tree and never in a paper, so there is no pair to compare and
# including it would only manufacture one-sided facts.

TEST_RE = {k: re.compile('|'.join(v), re.I) for k, v in TEST_FORMS.items()}
ANY_TEST_RE = re.compile('|'.join(f'(?P<{k}>' + '|'.join(v) + ')'
                                  for k, v in TEST_FORMS.items()), re.I)

# --- fields ----------------------------------------------------------------
# Word and symbol forms are unambiguous. BARE SINGLE LETTERS ARE NOT, and the
# corpus is full of Hilbert spaces H, capacities C and result lists R, so a
# bare letter is admitted as a field ONLY in one of the enumerated anchored
# contexts below. That list is part of the idiom inventory this tool reports.
# The adjectival form -- "real bookkeeping", "quaternionic surplus". The noun
# list was enumerated from the corpus, not guessed; a bare adjective is NOT
# admitted, because "real physical failure mode" and "complex structure" are
# everywhere and name no field.
_FNOUN = (r'field|amplitudes?|quantum\s+theory|QM|bookkeeping|sectors?|case|'
          r'branch|system|composite|blocks?|class|algebra|modules?|deficit|'
          r'surplus|theory|numbers|matrix|matrices|division\s+ring|'
          r'observable|dimension|state\s+space|two-qubit')

FIELD_UNAMBIGUOUS = [
    (r'\\mathbb\s*\{\s*R\s*\}|\\mathbb\s+R\b|\u211d', 'R'),
    (r'\\mathbb\s*\{\s*C\s*\}|\\mathbb\s+C\b|\u2102', 'C'),
    (r'\\mathbb\s*\{\s*H\s*\}|\\mathbb\s+H\b|\u210d', 'H'),
    (r'\breal[- ](?:' + _FNOUN + r')\b|\bR-QM\b|\bthe\s+reals\b', 'R'),
    (r'\bcomplex[- ](?:' + _FNOUN + r')\b|\bC-QM\b|\bthe\s+complex\s+numbers\b', 'C'),
    (r'\bquaternionic\b|\bquaternions?\b|\bH-QM\b|'
     r'\bquaternion[- ](?:' + _FNOUN + r')\b', 'H'),
]
FIELD_UNAMBIGUOUS_RE = [(re.compile(p, re.I), f) for p, f in FIELD_UNAMBIGUOUS]

# Bare-letter admission contexts. Each is (regex with group 'f', label).
# The label is reported so a reader can see which context admitted a letter.
BARE_CONTEXTS = [
    (r'M_\{?[^(){}]{0,12}\}?\(\s*(?P<f>[RCH])\s*\)', 'MATRIX_ALGEBRA'),
    (r'\b[Oo]ver\s+(?P<f>[RCH])\b', 'OVER_FIELD'),
    (r'\b(?P<f>[RCH])-QM\b', 'FIELD_QM'),
    (r'\b(?:D|F|\\mathbb\{F\})\s*(?:=|\\in|in)\s*\{?\s*(?P<f>[RCH])\b', 'DIVISION_RING_EQ'),
    (r'\{\s*(?P<f>[RCH])\s*,\s*[RCH]\s*(?:,\s*[RCH]\s*)?\}', 'FIELD_SET'),
    (r'\{\s*[RCH]\s*,\s*(?P<f>[RCH])\s*(?:,\s*[RCH]\s*)?\}', 'FIELD_SET'),
    (r'\{\s*[RCH]\s*,\s*[RCH]\s*,\s*(?P<f>[RCH])\s*\}', 'FIELD_SET'),
    (r'(?:rules?\s+out|ruling\s+out|ruled\s+out|excludes?|excluded|excluding|'
     r'eliminates?|eliminated|selects?|selected|admits?)\s+(?P<f>[RCH])\b(?!\w|_)', 'AFTER_VERDICT_VERB'),
    (r'\b(?P<f>[RCH])\s+(?:fails?|failing|passes|passed|pass\b|survives?|violates?|'
     r'is\s+excluded|excluded|admits)', 'BEFORE_VERDICT_VERB'),
    (r'(?:cent(?:er|re))\s*=?\s*(?P<f>[RCH])\b(?!\w|_)', 'CENTRE_EQ'),
    (r'\b(?:the\s+)?(?P<f>[RCH])\s*[:,]?\s+(?:surplus|deficit|shortfall|clause)\b',
     'FIELD_QUANTITY'),
]
BARE_CONTEXTS_RE = [(re.compile(p), lab) for p, lab in BARE_CONTEXTS]

# --- verdict verbs ---------------------------------------------------------
# Orientation A: TEST <verb> FIELD.  Orientation B: FIELD <verb> TEST.
EXCL_A = (r'exclud\w+|eliminat\w+|rules?\s+out|ruling\s+out|ruled\s+out|'
          r'forbid\w*|rejects?|rejected|kills?|killed')
ADMIT_A = r'selects?|selecting|selected|admits?|admitted|permits?|permitted'
EXCL_B = r'fails?|failing|failed|violat\w+|breaks?|does\s+not\s+satisfy'
ADMIT_B = r'passes|passed|pass\b|passing|surviv\w+|holds?|satisf\w+|obeys?'

# --- negation / uncertainty guard -----------------------------------------
# If any of these sits between the two anchors, the polarity is not decidable
# from the surface. Drop and count.
NEGATION = re.compile(
    r'\bnot\b|\bnever\b|\bno\b|\bcannot\b|\bcan\s*not\b|\bwithout\b|\bunless\b|'
    r"\bn't\b|\bnon-?adjudicat\w*|\bmay\s+not\b|\bfails?\s+to\b", re.I)

# ===========================================================================
# BUCKETS -- known-legitimate non-matches, named, ordered, disjoint.
# A fact in ANY bucket is excluded from the headline disagreement count and
# LISTED instead, so nobody chases it. Membership is a syntactic fact.
# ===========================================================================
BUCKET_MARKERS = [
    # Changelog text stands as written by house convention. NEVER flagged.
    ('B_CHANGELOG_REGION', None),           # set structurally, not by marker
    # Working Rule 18: the house correction convention QUOTES the retired
    # sentence inside its own correction. A gate that flags that is
    # structurally guaranteed to false-alarm.
    ('B_QUOTED_RETIRED', re.compile(
        r'\bwas\s+said\s+to\b|\bused\s+to\b|\bpreviously\b|\bpre-corrigendum\b|'
        r'\bcorrigendum\b|\bthis\s+(?:docstring|file|row|note|block)\s+said\b|'
        r'\bRETIRED\b|\bWITHDRAWN\b|\bstale\b|\binverted\b|\bwas\s+wrong\b|'
        r'\bincorrectly\b|\bmistaken\w*\b|\bsuperseded\b|\bcorrected\s+(?:to|from|at)\b|'
        r'\bdrifted\b|\bthe\s+error\b|\bthe\s+defect\b|\bformerly\b', re.I)),
    # A deliberately-wrong string used as a fixture, a countermodel, a mutation
    # target, or a hypothetical the source itself rejects.
    # Kept deliberately NARROW. An earlier marker list included
    # "hypothetical" and "would be", which sit in the ordinary sentence
    # "M_n(H) tensored over R with M_m(H) is real-dimensional 16 n^2 m^2,
    # while a hypothetical quaternionic M_{nm}(H) would have ..." -- an
    # ordinary statement of the computed value, and bucketing it hid a real
    # disagreement. The hypothetical algebra itself is excluded structurally
    # (TT requires an explicit numeric coefficient), not by a word list.
    ('B_HYPOTHETICAL_OR_FIXTURE', re.compile(
        r'\bcountermodel\b|\bnaive\b|\b_naive\w*|\bdemo\b|\bfixture\b|'
        r'\bmutation\b|\bmutant\b|\bescape[ds]?\b|\bnegative\s+control\b|'
        r'\btripwire\b|\bsentinel\b|\bcorrupt\w*\b|\btamper\w*\b|\bseeded\b', re.I)),
    # A different regime / a different counting convention. The corpus really
    # does carry two: full-dimension and trace-one/marginals-plus-correlations.
    ('B_DIFFERENT_REGIME_OR_CONVENTION', re.compile(
        r'\bnormalis\w+\b|\bnormaliz\w+\b|\btrace[-\s]one\b|\btrace-?1\b|'
        r'\bprojective\b|\bbipartite\s+correlations\b|\bmarginal\w*\b|'
        r'\binfinite[-\s]dimensional\b|\bSol\\?[`\']?er\b|\bunder\s+the\s+other\s+convention\b|'
        r'\bconvention\b|\bup\s+to\s+normalis\w+\b|'
        # the marginals-plus-correlations counting, written as an explicit sum
        r'[+]\s*(?:d|K|dim)_', re.I)),
]

# ===========================================================================
# NORMALISATION -- collapse whitespace, keep an exact offset map
# ===========================================================================

def normalise(text):
    """Collapse each run of whitespace to a single space.

    Returns (norm, offsets) with offsets[i] == the ORIGINAL offset of norm[i].
    Working Rule 18: match on `norm`, report through `offsets`.

    Built run-wise, not character-wise: the corpus contains multi-megabyte
    modules and a per-character Python loop over the whole tree does not
    finish. The offset array is `array('l')` for the same reason.
    """
    parts = []
    offs = array('l')
    pos = 0
    for m in re.finditer(r'\s+', text):
        if m.start() > pos:
            parts.append(text[pos:m.start()])
            offs.extend(range(pos, m.start()))
        parts.append(' ')
        offs.append(m.start())
        pos = m.end()
    if pos < len(text):
        parts.append(text[pos:])
        offs.extend(range(pos, len(text)))
    return ''.join(parts), offs


class LineIndex:
    def __init__(self, text):
        self.starts = [0]
        for m in re.finditer('\n', text):
            self.starts.append(m.end())

    def line(self, off):
        return bisect.bisect_right(self.starts, off)


# ===========================================================================
# SOURCE -- a file, normalised, with provenance and region tagging
# ===========================================================================

class Source:
    """One .tex or .py file: normalised text, offset map, provenance regions."""

    def __init__(self, path, label, kind, text):
        self.path = path
        self.label = label            # short display name
        self.kind = kind              # 'PAPER' | 'CODE'
        self.raw = text
        self.norm, self.offs = normalise(text)
        self.li = LineIndex(text)
        self.regions = []             # list of (start, end, tagname) ORIGINAL offsets
        self.defs = []                # code: (start, end, name)
        self.parse_note = None

    def orig(self, i):
        return self.offs[i] if i < len(self.offs) else (self.offs[-1] if self.offs else 0)

    def line_of(self, i):
        return self.li.line(self.orig(i))

    def tags_at(self, i):
        o = self.orig(i)
        return [t for (a, b, t) in self.regions if a <= o < b]

    def def_at(self, i):
        o = self.orig(i)
        best = None
        for (a, b, nm) in self.defs:
            if a <= o < b and (best is None or (b - a) < (best[1] - best[0])):
                best = (a, b, nm)
        return best[2] if best else None


# --- TeX loading -----------------------------------------------------------

def load_tex(path, label):
    with open(path, encoding='utf-8', errors='replace') as f:
        text = f.read()
    s = Source(path, label, 'PAPER', text)
    # LaTeX comment regions: an unescaped % to end of line.
    for m in re.finditer(r'(?<!\\)%[^\n]*', text):
        s.regions.append((m.start(), m.end(), 'TEX_COMMENT'))
    # Changelog sections in the body.
    heads = [m for m in re.finditer(r'\\(?:sub)*section\*?\s*\{([^}]*)\}', text)]
    for i, m in enumerate(heads):
        if re.search(r'change\s*log|revision\s+history|version\s+history', m.group(1), re.I):
            end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
            s.regions.append((m.start(), end, 'TEX_CHANGELOG_SECTION'))
    return s


# --- Python loading --------------------------------------------------------

def load_py(path, label):
    with open(path, encoding='utf-8', errors='replace') as f:
        text = f.read()
    s = Source(path, label, 'CODE', text)
    li = s.li
    starts = li.starts

    def off(row, col):
        return starts[row - 1] + col if 0 < row <= len(starts) else 0

    # provenance by tokenize: COMMENT / STRING (the rest is executable code)
    try:
        for tok in tokenize.generate_tokens(io.StringIO(text).readline):
            if tok.type == tokenize.COMMENT:
                s.regions.append((off(*tok.start), off(*tok.end), 'PY_COMMENT'))
            elif tok.type == tokenize.STRING:
                s.regions.append((off(*tok.start), off(*tok.end), 'PY_STRING'))
    except Exception as e:                                  # noqa: BLE001
        s.parse_note = 'tokenize failed: %s' % e

    # defs and docstrings by AST
    try:
        tree = ast.parse(text)
    except Exception as e:                                  # noqa: BLE001
        s.parse_note = (s.parse_note or '') + ' ast failed: %s' % e
        return s

    def docstring_interval(node):
        b = getattr(node, 'body', None)
        if not b:
            return None
        first = b[0]
        if isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant) \
                and isinstance(first.value.value, str):
            return (off(first.lineno, first.col_offset),
                    off(first.end_lineno, first.end_col_offset))
        return None

    iv = docstring_interval(tree)
    if iv:
        s.regions.append((iv[0], iv[1], 'PY_MODULE_DOCSTRING'))
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            a = off(node.lineno, node.col_offset)
            b = off(node.end_lineno, node.end_col_offset)
            if isinstance(node, ast.ClassDef):
                s.regions.append((a, b, 'PY_CLASS'))
            else:
                s.defs.append((a, b, node.name))
            iv = docstring_interval(node)
            if iv:
                s.regions.append((iv[0], iv[1], 'PY_DOCSTRING'))

    # changelog narrative inside code: a version-and-date header owns the text
    # that follows it until the next blank-line-separated block.
    for m in re.finditer(r'^\s*#{0,3}\s*###?\s*v\d+[\d.]*\s+changes.*$', text, re.M | re.I):
        s.regions.append((m.start(), min(len(text), m.end() + 4000), 'PY_CHANGELOG'))
    # A per-version narrative comment -- `# v24.3.463 (2026-07-31): ...` -- is a
    # changelog entry wherever it lives, and a changelog entry stands as written.
    # `_module_manifest.py` carries the corpus's longest one, on a single line.
    for a, b, tag in list(s.regions):
        if tag != 'PY_COMMENT':
            continue
        if re.search(r'#\s*v\d+\.\d+[\d.]*\s*\(\d{4}-\d{2}-\d{2}\)', text[a:b]):
            s.regions.append((a, b, 'PY_CHANGELOG'))
    return s


# ===========================================================================
# TOKEN SCANNING inside a normalised string
# ===========================================================================

def find_tests(norm):
    out = []
    for m in ANY_TEST_RE.finditer(norm):
        tid = m.lastgroup
        if tid in TEST_FORMS:
            out.append((m.start(), m.end(), tid))
    return out


def find_fields(norm):
    """Every field-denoting token, with the idiom that admitted it."""
    out = []
    for rx, f in FIELD_UNAMBIGUOUS_RE:
        for m in rx.finditer(norm):
            out.append((m.start(), m.end(), f, 'UNAMBIGUOUS'))
    for rx, lab in BARE_CONTEXTS_RE:
        for m in rx.finditer(norm):
            a, b = m.span('f')
            out.append((a, b, m.group('f').upper(), 'BARE:' + lab))
    # de-overlap: keep the longest match starting at each offset, but keep
    # distinct offsets (instances, not lines)
    out.sort(key=lambda t: (t[0], -(t[1] - t[0])))
    kept = []
    for t in out:
        if kept and t[0] == kept[-1][0]:
            continue
        kept.append(t)
    return kept


# ===========================================================================
# FACTS
# ===========================================================================

class SrcRef:
    """What a fact keeps of its source once the Source object is freed.

    Every .tex and .py file is normalised into a full-length offset array, so
    holding every Source in memory at once exhausts the box. Sources are
    processed one at a time and each fact detaches to one of these."""
    __slots__ = ('label', 'kind', 'path')

    def __init__(self, src):
        self.label, self.kind, self.path = src.label, src.kind, src.path


class Fact:
    __slots__ = ('kind', 'key', 'value', 'idiom', 'src', 'line', 'norm_start',
                 'context', 'provenance', 'defname', 'buckets', 'field_idiom')

    def __init__(self, kind, key, value, idiom, src, ns, context,
                 provenance, defname, buckets, field_idiom=''):
        self.kind = kind
        self.key = key
        self.value = value
        self.idiom = idiom
        self.src = src
        self.line = src.line_of(ns)
        self.norm_start = ns
        self.context = context
        self.provenance = provenance
        self.defname = defname
        self.buckets = buckets
        self.field_idiom = field_idiom

    def detach(self):
        self.src = SrcRef(self.src)
        return self

    def site(self):
        return '%s:%d%s' % (self.src.label, self.line,
                            (' ' + self.defname) if self.defname else '')

    def as_dict(self):
        return dict(kind=self.kind, key=list(self.key), value=list(self.value),
                    idiom=self.idiom, source=self.src.label,
                    source_kind=self.src.kind, path=self.src.path,
                    line=self.line, context=self.context,
                    provenance=self.provenance, defname=self.defname,
                    buckets=self.buckets, field_idiom=self.field_idiom)


CTX = 170


def _ctx(src, a, b):
    lo = max(0, a - CTX // 2)
    hi = min(len(src.norm), b + CTX)
    return src.norm[lo:hi].strip()


def _prov(src, i):
    tags = src.tags_at(i)
    if src.kind == 'PAPER':
        if 'TEX_CHANGELOG_SECTION' in tags:
            return 'TEX_CHANGELOG_SECTION'
        if 'TEX_COMMENT' in tags:
            return 'TEX_COMMENT'
        return 'TEX_BODY'
    if 'PY_MODULE_DOCSTRING' in tags:
        return 'PY_MODULE_DOCSTRING'
    if 'PY_DOCSTRING' in tags:
        return 'PY_DOCSTRING'
    if 'PY_COMMENT' in tags:
        return 'PY_COMMENT'
    if 'PY_STRING' in tags:
        return 'PY_STRING'
    return 'PY_CODE'


CHANGELOG_PROV = {'TEX_CHANGELOG_SECTION', 'TEX_COMMENT', 'PY_CHANGELOG'}
# TEX_COMMENT is where the changelog lives in every paper in this corpus: the
# per-version block at the head of the file is a run of `%` lines. Treating
# every %-comment as changelog is deliberately over-inclusive -- it costs a
# small number of genuine body-adjacent notes and it guarantees that a
# changelog entry, which STANDS AS WRITTEN by house convention, is never
# flagged.


def buckets_for(src, ns, ne, context):
    out = []
    tags = src.tags_at(ns)
    if 'TEX_CHANGELOG_SECTION' in tags or 'TEX_COMMENT' in tags or 'PY_CHANGELOG' in tags:
        out.append('B_CHANGELOG_REGION')
    for name, rx in BUCKET_MARKERS:
        if rx is None:
            continue
        if rx.search(context):
            out.append(name)
    return out


def _mkfact(kind, key, value, idiom, src, ns, ne, field_idiom=''):
    ctx = _ctx(src, ns, ne)
    return Fact(kind, key, value, idiom, src, ns, ctx, _prov(src, ns),
                src.def_at(ns), buckets_for(src, ns, ne, ctx), field_idiom)


# ---------------------------------------------------------------------------
# FS -- field selection verdicts. Ten named idioms, enumerated from the corpus.
# ---------------------------------------------------------------------------
IDIOMS = {
    'I1_TEST_VERB_FIELD':     'TEST ... <excludes|eliminates|rules out> FIELD',
    'I2_TEST_PAREN_FIELD':    'TEST ( <excludes|eliminates> FIELD )',
    'I3_FIELD_VERB_TEST':     'FIELD <fails|violates|passes> TEST',
    'I4_FIELD_PASSIVE_TEST':  'FIELD <excluded|ruled out> by TEST',
    'I5_HEADING_EXCLUSION':   r'\textbf{$\mathbb{F}$-exclusion} ... names one TEST',
    'I6_ENCLOSING_DEF':       'inside def check_P_x: "Over FIELD: <test> fails|holds"',
    'I7_RESPECTIVELY':        'TEST1 + TEST2 ... ruling out FIELD1 and FIELD2 respectively',
    'I8_CANNOT_SUPPLY':       'TEST ... is what a FIELD field cannot supply',
    'I9_ONLY_FIELDS_PASS':    'only FIELD(s) pass TEST',
    'I10_TEST_SELECTS_FIELD': 'TEST ... selects FIELD',
}

GAP = 220           # normalised chars allowed between the two anchors
GAP_TIGHT = 70


def _no_crossing(seg, tests, fields):
    """The gap must not contain another TEST or another FIELD."""
    return not (ANY_TEST_RE.search(seg) or any(rx.search(seg) for rx, _ in FIELD_UNAMBIGUOUS_RE))


def extract_FS(src, tests, fields):
    facts = []
    consumed = set()
    n = src.norm

    def emit(kind, key, val, idiom, a, b, fidiom=''):
        f = _mkfact(kind, key, val, idiom, src, a, b, fidiom)
        facts.append(f)
        consumed.add((a, b))
        return f

    fmap = {(a, b): (fld, fid) for a, b, fld, fid in fields}

    # --- I1 / I2 / I10 : TEST <gap> VERB FIELD --------------------------
    for ta, tb, tid in tests:
        for fa, fb, fld, fid in fields:
            if not (tb <= fa <= tb + GAP):
                continue
            gap = n[tb:fa]
            # A DIFFERENT test in the gap means the anchors do not belong to
            # each other. The SAME test restated is an aside -- "P_tom (local
            # tomographic completeness, from L_loc) eliminates R" -- and
            # rejecting it costs the most common idiom in the corpus.
            if any(t != tid for _, _, t in find_tests(gap)):
                continue
            # Symmetric guard: another FIELD between the two anchors means
            # they do not belong to each other. Without it, "tomographic
            # locality ruling out R). Soler closes the classification to
            # {R, C, H}; the split selects C" binds `selects C` to
            # `tomographic locality`, whose subject is `the split`.
            if any(rx.search(gap) for rx, _ in FIELD_UNAMBIGUOUS_RE):
                continue
            # ... and no sentence boundary. Same site, second guard.
            if re.search(r'\.\s', gap):
                continue
            # `[^A-Za-z0-9]{0,6}$` rather than `\s*$`: in a paper the verb and
            # the field are separated by LaTeX markup -- "eliminates $\mathbb{R}$"
            # puts a literal `$` between them, and a whitespace-only tail
            # silently misses every maths-mode field token in the corpus.
            m = re.search(r'(?:' + EXCL_A + r')[^A-Za-z0-9]{0,6}$', gap, re.I)
            pol = 'EXCLUDES'
            if not m:
                m = re.search(r'(?:' + ADMIT_A + r')[^A-Za-z0-9]{0,6}$', gap, re.I)
                pol = 'ADMITS'
            if not m:
                continue
            pre = gap[:m.start()]
            if NEGATION.search(pre[-40:]):
                continue
            idiom = ('I2_TEST_PAREN_FIELD' if re.match(r'\s*\(', gap)
                     else ('I10_TEST_SELECTS_FIELD' if pol == 'ADMITS'
                           else 'I1_TEST_VERB_FIELD'))
            emit('FS', ('FS', tid, fld), (pol,), idiom, ta, fb, fid)

    # --- I3 : FIELD <gap> VERB TEST ------------------------------------
    for fa, fb, fld, fid in fields:
        for ta, tb, tid in tests:
            if not (fb <= ta <= fb + GAP_TIGHT):
                continue
            gap = n[fb:ta]
            if any(rx.search(gap) for rx, _ in FIELD_UNAMBIGUOUS_RE):
                continue
            m = re.search(r'(?:' + EXCL_B + r')[^.;]{0,25}$', gap, re.I)
            pol = 'EXCLUDES'
            if not m:
                m = re.search(r'(?:' + ADMIT_B + r')[^.;]{0,25}$', gap, re.I)
                pol = 'ADMITS'
            if not m:
                continue
            if NEGATION.search(gap[:m.start()][-40:]):
                continue
            emit('FS', ('FS', tid, fld), (pol,), 'I3_FIELD_VERB_TEST', fa, tb, fid)

    # --- I4 : FIELD <excluded|ruled out> by TEST ------------------------
    for fa, fb, fld, fid in fields:
        for ta, tb, tid in tests:
            if not (fb <= ta <= fb + GAP_TIGHT):
                continue
            gap = n[fb:ta]
            if any(rx.search(gap) for rx, _ in FIELD_UNAMBIGUOUS_RE):
                continue
            pol = None
            if re.search(r'(?:is|are)?\s*(?:' + EXCL_A + r')\s+(?:by|via)\s+'
                         r'(?:the\s+)?[^.;]{0,30}$', gap, re.I):
                pol = 'EXCLUDES'
            elif re.search(r'(?:is|are)?\s*(?:' + ADMIT_A + r')\s+(?:by|via)\s+'
                           r'(?:the\s+)?[^.;]{0,30}$', gap, re.I):
                pol = 'ADMITS'
            if pol is None or NEGATION.search(gap):
                continue
            emit('FS', ('FS', tid, fld), (pol,), 'I4_FIELD_PASSIVE_TEST', fa, tb, fid)

    # --- I5 : \textbf{$\mathbb{F}$-exclusion} heading -------------------
    for m in re.finditer(
            r'\\textbf\s*\{\s*\$?\\mathbb\s*\{\s*([RCH])\s*\}\s*\$?\s*-\s*?exclusion',
            n, re.I):
        fld = m.group(1).upper()
        window = n[m.end():m.end() + 1400]
        # stop at the next such heading
        stop = re.search(r'\\textbf\s*\{\s*\$?\\mathbb', window)
        if stop:
            window = window[:stop.start()]
        seen = {t for _, _, t in find_tests(window)}
        if len(seen) == 1:
            emit('FS', ('FS', seen.pop(), fld), ('EXCLUDES',),
                 'I5_HEADING_EXCLUSION', m.start(), m.end())

    # --- I6 : enclosing def binds the test ------------------------------
    if src.kind == 'CODE':
        for (a, b, name) in src.defs:
            tid = None
            for k in TEST_FORMS:
                if re.search(r'(?:^|_)' + k.lower() + r'(?:$|_)', name.lower()):
                    tid = k
            if not tid:
                continue
            # normalised offsets covering this def
            lo = bisect.bisect_left(src.offs, a)
            hi = bisect.bisect_left(src.offs, b)
            body = n[lo:hi]
            for mm in re.finditer(
                    r'[Oo]ver\s+([RCH])\s*[:,]\s*([^."\']{0,90})', body):
                fld = mm.group(1).upper()
                tail = mm.group(2)
                # NEGATION IS TESTED FIRST. "# Over R: local measurements do
                # NOT determine joint state" contains `determine`, and an
                # ADMITS-before-negation ordering reads it as R PASSING the
                # very test the comment says it fails.
                neg = re.search(r'\b(?:do(?:es)?\s+not|cannot|can\s*not|never|'
                                r'no\s+longer)\b', tail, re.I)
                admit = re.search(r'\b(?:' + ADMIT_B + r')\b|determine', tail, re.I)
                excl = re.search(r'\b(?:' + EXCL_B + r')\b|invisible|blind', tail, re.I)
                if neg and admit and not excl:
                    pol = 'EXCLUDES'          # "do NOT determine"
                elif neg:
                    continue                  # a negated failure: undecidable here
                elif excl:
                    pol = 'EXCLUDES'
                elif admit:
                    pol = 'ADMITS'
                else:
                    continue
                emit('FS', ('FS', tid, fld), (pol,), 'I6_ENCLOSING_DEF',
                     lo + mm.start(), lo + mm.end())

    # --- I7 : "... respectively" ----------------------------------------
    for m in re.finditer(r'respectively', n, re.I):
        lo = max(0, m.start() - 400)
        seg = n[lo:m.start()]
        ts = [t for _, _, t in find_tests(seg)]
        fs = [f for _, _, f, _ in find_fields(seg)]
        # exactly two DISTINCT tests and two DISTINCT fields, in order
        if len(ts) == 2 and len(set(ts)) == 2 and len(fs) == 2 and len(set(fs)) == 2:
            if re.search(r'(?:' + EXCL_A + r')', seg, re.I):
                emit('FS', ('FS', ts[0], fs[0]), ('EXCLUDES',), 'I7_RESPECTIVELY',
                     lo, m.end())
                emit('FS', ('FS', ts[1], fs[1]), ('EXCLUDES',), 'I7_RESPECTIVELY',
                     lo, m.end())

    # --- I8 : "is what a FIELD field cannot supply" ----------------------
    for m in re.finditer(
            r'is\s+what\s+an?\s+(real|complex|quaternionic)\s+field\s+cannot\s+supply', n, re.I):
        fld = {'real': 'R', 'complex': 'C', 'quaternionic': 'H'}[m.group(1).lower()]
        lo = max(0, m.start() - 300)
        seg = n[lo:m.start()]
        seen = [t for _, _, t in find_tests(seg)]
        if len(set(seen)) == 1:
            emit('FS', ('FS', seen[-1], fld), ('EXCLUDES',), 'I8_CANNOT_SUPPLY',
                 m.start(), m.end())

    # --- I9 : "only C passes / only C survives ... TEST" -----------------
    for m in re.finditer(r'\bonly\s+([RCH])\s+(?:' + ADMIT_B + r')', n):
        fld = m.group(1).upper()
        window = n[max(0, m.start() - 200):m.end() + 200]
        seen = {t for _, _, t in find_tests(window)}
        if len(seen) == 1:
            emit('FS', ('FS', seen.pop(), fld), ('ADMITS',),
                 'I9_ONLY_FIELDS_PASS', m.start(), m.end())

    return facts


# ---------------------------------------------------------------------------
# TT -- the quaternionic composite target
# ---------------------------------------------------------------------------
QUAT_CUE = re.compile(
    r'M_\{?n\}?\s*\(\s*(?:\\mathbb\s*\{\s*H\s*\}|H)\s*\)|'
    r'M_\{?m\}?\s*\(\s*(?:\\mathbb\s*\{\s*H\s*\}|H)\s*\)|'
    r'M_\{?k\}?\s*\(\s*(?:\\mathbb\s*\{\s*H\s*\}|H)\s*\)|quaternionic', re.I)

TT_TARGET = re.compile(
    r'M_\{\s*([0-9]*\s*[a-z]{1,3})\s*\}\s*\(\s*(?:\\mathbb\s*\{\s*([RCH])\s*\}|([RCH]))\s*\)|'
    r'M_([0-9]+[a-z]{1,3})\s*\(\s*([RCH])\s*\)')

TT_REALDIM = re.compile(
    r'real\s+dimension\s+\$?\s*([0-9]*\s*n\s*\^?\{?2\}?\s*m\s*\^?\{?2\}?)|'
    r'\b([0-9]+)\s*n\^\{?2\}?\s*m\^\{?2\}?')


def _canon_coef(c):
    c = re.sub(r'\s+', '', c)
    m = re.match(r'^(\d*)([a-z]+)$', c)
    if not m:
        return c
    return (m.group(1) or '1') + ''.join(sorted(m.group(2)))


def extract_TT(src):
    facts = []
    n = src.norm
    for m in TT_TARGET.finditer(n):
        coef = m.group(1) or m.group(4)
        fld = (m.group(2) or m.group(3) or m.group(5) or '').upper()
        if not coef or not fld:
            continue
        cc = _canon_coef(coef)
        # An EXPLICIT numeral is required. `M_{nm}(H)` and `M_{nm}(R)` name the
        # hypothetical quaternionic composite and the internal real one -- two
        # different objects from the one this fact type is about -- so a bare
        # `nm` is dropped rather than normalised to `1mn`.
        if not re.match(r'^[2-9]\d*mn$', cc):
            continue
        lo = max(0, m.start() - 260)
        if not QUAT_CUE.search(n[lo:m.start() + 40]):
            continue
        facts.append(_mkfact('TT_TARGET', ('TT_TARGET',), (cc, fld),
                             'TT1_COMPOSITE_ALGEBRA', src, m.start(), m.end()))
    for m in TT_REALDIM.finditer(n):
        expr = (m.group(1) or '').strip()
        coefficient = m.group(2)
        if expr:
            mm = re.match(r'^(\d*)\s*n', re.sub(r'\s+', '', expr))
            coefficient = (mm.group(1) or '1') if mm else None
        if not coefficient:
            continue
        lo = max(0, m.start() - 300)
        if not QUAT_CUE.search(n[lo:m.start() + 60]):
            continue
        facts.append(_mkfact('TT_REALDIM', ('TT_REALDIM',), (coefficient + 'n^2m^2',),
                             'TT2_COMPOSITE_REAL_DIMENSION', src, m.start(), m.end()))
    return facts


# ---------------------------------------------------------------------------
# SD -- surplus vs deficit, per field
# ---------------------------------------------------------------------------
SD_WORD = re.compile(r'\b(surplus|deficit|shortfall|over-?count|under-?count)\b', re.I)
SD_DIR = {'surplus': 'SURPLUS', 'overcount': 'SURPLUS', 'over-count': 'SURPLUS',
          'deficit': 'DEFICIT', 'shortfall': 'DEFICIT', 'undercount': 'DEFICIT',
          'under-count': 'DEFICIT'}


def extract_SD(src, tests, fields):
    facts = []
    n = src.norm
    tpos = [a for a, _, _ in tests]
    for m in SD_WORD.finditer(n):
        direction = SD_DIR[m.group(1).lower().replace('\u2013', '-')]
        # gate: a named test must be within +/- 400 normalised chars
        if not any(abs(p - m.start()) <= 400 for p in tpos):
            continue
        # the nearest field token within a tight window, with no other between
        best = None
        mprov = _prov(src, m.start())
        for fa, fb, fld, fid in fields:
            # A field token and a direction word in DIFFERENT text objects --
            # a string literal and the comment after it -- are not talking
            # about each other. Without this the matcher reads
            # `f"C-QM must pass ..." ) # ---- H: deficit` as (C, DEFICIT).
            if _prov(src, fa) != mprov:
                continue
            if fb <= m.start() and m.start() - fb <= 90:
                seg = n[fb:m.start()]
                if any(rx.search(seg) for rx, _ in FIELD_UNAMBIGUOUS_RE):
                    continue
                if NEGATION.search(seg):
                    continue
                # No SENTENCE boundary between the field and the direction
                # word. Without this the matcher reads "Delta_H(n,m) < 0. \]
                # Real bookkeeping runs a forced deficit" as (H, DEFICIT),
                # which is a clean false positive: the sentence says R.
                # A bare colon is NOT a boundary here -- it is the format spec
                # inside an f-string, `{deficit_H:+d}`, and rejecting on it
                # drops the code's own statement of the direction.
                if re.search(r'[.;]\s|\\\]|\\\[', seg):
                    continue
                d = m.start() - fb
                if best is None or d < best[0]:
                    best = (d, fld, fa, fid)
            elif fa >= m.end() and fa - m.end() <= 40:
                seg = n[m.end():fa]
                if NEGATION.search(seg):
                    continue
                if not re.match(r'\s*(?:of|for|in|is|,)?\s*$', seg):
                    continue
                d = fa - m.end()
                if best is None or d < best[0]:
                    best = (d, fld, fa, fid)
        if best is None:
            continue
        _, fld, fa, fid = best
        facts.append(_mkfact('SD', ('SD', fld), (direction,), 'SD1_FIELD_DIRECTION',
                             src, min(fa, m.start()), max(m.end(), fa), fid))
    return facts


# ---------------------------------------------------------------------------
# OD -- observable-space dimensions
# ---------------------------------------------------------------------------
OD_FORMULA = {
    'n(n+1)/2': 'R', 'n(n+1)2': 'R', 'N(N+1)/2': 'R',
    'n^2': 'C', 'N^2': 'C',
    'n(2n-1)': 'H', 'N(2N-1)': 'H', '2n^2-n': 'H',
}
OD_DFN = re.compile(
    r'(?:d|K|dim)_?\{?\s*(?:\\mathbb\s*\{\s*([RCH])\s*\}|([RCH]))\s*\}?\s*'
    r'\(\s*(\d)\s*\)\s*(?:=|\\ge|\\le|>|<)\s*(\d+)')
OD_JOINTLOCAL = re.compile(
    r'K_(joint|local)\s*\(\s*([RCH])\s*\)\s*=\s*(\d+)|'
    r'\b(joint|local)\s*=\s*(\d+)')


def extract_OD(src, tests, fields):
    facts = []
    n = src.norm
    tpos = [a for a, _, _ in tests]
    for m in OD_DFN.finditer(n):
        fld = (m.group(1) or m.group(2) or '').upper()
        arg, val = m.group(3), m.group(4)
        if not any(abs(p - m.start()) <= 600 for p in tpos):
            continue
        # `d(2) . d(2) + d(2) + d(2) = 15` ends in a term that LOOKS like
        # `d(2) = 15`. The 15 is the value of the sum, not of d(2). Reject a
        # match whose own term is the tail of an arithmetic chain.
        if re.search(r'(?:[+\-*/]|\\cdot|\\times)\s*$', n[max(0, m.start() - 14):m.start()]):
            continue
        facts.append(_mkfact('OD_DIM', ('OD_DIM', fld, arg), (val,),
                             'OD1_DIMENSION_FUNCTION', src, m.start(), m.end()))
    for m in re.finditer(r'K_(joint|local)\s*\(\s*([RCH])\s*\)\s*=\s*(\d+)', n):
        which, fld, val = m.group(1).upper(), m.group(2).upper(), m.group(3)
        facts.append(_mkfact('OD_22', ('OD_22', fld, which), (val,),
                             'OD2_JOINT_LOCAL_PAIR', src, m.start(), m.end()))
    for m in re.finditer(
            r'([RCH])\s+(?:fails?|passes)\s*\(?\s*joint\s*=\s*(\d+)\s*,\s*local\s*=\s*(\d+)', n):
        fld = m.group(1).upper()
        facts.append(_mkfact('OD_22', ('OD_22', fld, 'JOINT'), (m.group(2),),
                             'OD2_JOINT_LOCAL_PAIR', src, m.start(), m.end()))
        facts.append(_mkfact('OD_22', ('OD_22', fld, 'LOCAL'), (m.group(3),),
                             'OD2_JOINT_LOCAL_PAIR', src, m.start(), m.end()))
    return facts


# ===========================================================================
# CORPUS
# ===========================================================================

def classify_tex(path, root):
    parts = os.path.relpath(path, root).split(os.sep)
    if 'Old' in parts:
        return 'OLD'
    if '_to_delete' in parts:
        return 'TO_DELETE'
    if 'Reviews' in parts:
        return 'REVIEWS'
    if 'good reviews' in parts:
        return 'REVIEWS'
    return 'LIVE' if len(parts) == 2 else 'ANCILLARY'


def gather_papers(root):
    """(live_paths, other_classified, unreadable) -- PATHS, not loaded files."""
    live, other = [], []
    for dp, dn, fn in os.walk(root):
        dn.sort()
        for f in sorted(fn):
            if not f.endswith('.tex'):
                continue
            p = os.path.join(dp, f)
            cls = classify_tex(p, root)
            (live if cls == 'LIVE' else other).append((cls, p))
    return live, other, []


def gather_code(root):
    out = []
    for dp, dn, fn in os.walk(root):
        dn.sort()
        if '__pycache__' in dp:
            continue
        for f in sorted(fn):
            if not f.endswith('.py'):
                continue
            out.append(os.path.join(dp, f))
    return sorted(out), []


def analyse(src):
    """Return (facts, candidate_spans, matched_span_starts)."""
    tests = find_tests(src.norm)
    fields = find_fields(src.norm)
    facts = []
    facts += extract_FS(src, tests, fields)
    facts += extract_TT(src)
    facts += extract_SD(src, tests, fields)
    facts += extract_OD(src, tests, fields)

    # candidate spans: a TEST occurrence with a FIELD token within +/-300.
    # Same-id tokens within 120 normalised characters are ONE candidate -- the
    # corpus habitually restates a test inside its own aside ("P_tom (local
    # tomographic completeness ...)"), and counting that twice inflates both
    # the population and the residual with a duplicate of one sentence.
    fpos = [(a, b) for a, b, _, _ in fields]
    cands = []
    last = {}
    for ta, tb, tid in tests:
        if tid in last and ta - last[tid] <= 120:
            last[tid] = tb
            continue
        last[tid] = tb
        if any(abs(fa - ta) <= 300 for (fa, fb) in fpos):
            cands.append((ta, tb, tid))
    # a candidate is COVERED if a fact was produced whose norm_start sits within
    # 400 chars of the test token
    starts = sorted(f.norm_start for f in facts)
    covered = []
    for ta, tb, tid in cands:
        i = bisect.bisect_left(starts, ta - 420)
        ok = False
        while i < len(starts) and starts[i] <= ta + 420:
            ok = True
            break
        covered.append(ok)
    for f in facts:
        f.detach()
    return facts, cands, covered


# ===========================================================================
# DISAGREEMENT
# ===========================================================================

def disagreements(facts):
    """Group by key; a disagreement is two facts on the SAME key carrying
    DIFFERENT values. One record per distinct value-pair, carrying every site
    on both sides -- instances are counted, never collapsed.

    An FS key is (FS, test, field), so an FS disagreement here is a POLARITY
    conflict: one source says the test excludes that field and another says it
    admits it. Two facts about DIFFERENT fields are not a disagreement -- a
    test excluding R and admitting C is one coherent statement, and an earlier
    version of this function that keyed on the test alone reported exactly
    that as a conflict, 450 times.
    """
    by_key = collections.defaultdict(lambda: collections.defaultdict(list))
    for f in facts:
        by_key[f.key][f.value].append(f)
    out = []
    for key, vals in sorted(by_key.items()):
        if len(vals) < 2:
            continue
        vv = sorted(vals)
        for i in range(len(vv)):
            for j in range(i + 1, len(vv)):
                a, b = vv[i], vv[j]
                out.append(dict(key=list(key),
                                form=('POLARITY' if key[0] == 'FS' else 'VALUE'),
                                value_a=list(a), value_b=list(b),
                                sites_a=vals[a], sites_b=vals[b]))
    return out


def inversions(facts):
    """THE ATTRIBUTION TEST, and it is deliberately narrow.

    Two sources INVERT each other when they pair the same two tests with the
    same two fields the opposite way round: source A says T1 excludes F1 and
    T2 excludes F2, source B says T1 excludes F2 and T2 excludes F1.

    This is decidable and it needs no judgement. Note what it does NOT do: a
    source stating only that T1 excludes F1, where another states T1 excludes
    F2, is NOT reported -- a test may in principle exclude more than one
    field, and reporting that difference as a conflict would be an inference.
    The full crossing pattern is the thing that cannot be read any other way.

    Self-pairs are included: a single file that carries both pairings
    contradicts itself, and that is worth reporting on its own.
    """
    excl = collections.defaultdict(lambda: collections.defaultdict(list))
    for f in facts:
        if f.kind == 'FS' and f.value[0] == 'EXCLUDES':
            excl[f.src.path][(f.key[1], f.key[2])].append(f)
    paths = sorted(excl)
    out = []
    for i, pa in enumerate(paths):
        for pb in paths[i:]:
            A, B = excl[pa], excl[pb]
            seen = set()
            for (t1, f1) in A:
                for (t2, f2) in A:
                    if t1 == t2 or f1 == f2:
                        continue
                    if (t1, f2) in B and (t2, f1) in B:
                        sig = (pa, pb, tuple(sorted([t1, t2])), tuple(sorted([f1, f2])))
                        if sig in seen:
                            continue
                        seen.add(sig)
                        out.append(dict(
                            source_a=pa, source_b=pb,
                            assignment_a={t1: f1, t2: f2},
                            assignment_b={t1: f2, t2: f1},
                            sites_a=A[(t1, f1)] + A[(t2, f2)],
                            sites_b=B[(t1, f2)] + B[(t2, f1)],
                            self_pair=(pa == pb)))
    return out


def scope_of(fa, fb):
    if fa.src.kind != fb.src.kind:
        return 'PAPER_vs_CODE'
    if fa.src.path != fb.src.path:
        return 'CODE_vs_CODE' if fa.src.kind == 'CODE' else 'PAPER_vs_PAPER'
    if fa.defname and fa.defname == fb.defname:
        return 'WITHIN_ONE_CHECK'
    return 'WITHIN_ONE_FILE'


def pairs_of(d):
    out = []
    for fa in d['sites_a']:
        for fb in d['sites_b']:
            out.append((fa, fb))
    return out


# ===========================================================================
# EXCLUSIVE FORM -- does a source state its assignment as a bijection?
# ===========================================================================
EXCLUSIVE_RE = re.compile(
    r'(?:two\s+conditions|two\s+exclusions|both\s+legs|the\s+split|'
    r'respectively|;\s*P_|and\s+P_)', re.I)


def is_exclusive(f):
    """The source itself pairs BOTH tests with BOTH fields in one span."""
    ctx = f.context
    ts = {t for _, _, t in find_tests(ctx)}
    fs = {x for _, _, x, _ in find_fields(ctx)}
    return len(ts) >= 2 and len(fs) >= 2


# ===========================================================================
# REPORT
# ===========================================================================
HR = '=' * 78


def fmt_val(kind, v):
    return ' / '.join(str(x) for x in v)


def write_report(out, R):
    w = out.write
    w("APF CONTRADICTION CENSUS -- paper-vs-code disagreement in a closed vocabulary\n")
    w("A REPORTING TOOL. It reports that two sources state the same fact\n")
    w("differently. It asserts NOTHING about which side is right, and nothing\n")
    w("about whether a disagreement is a defect. A human rules.\n\n")
    w("generated against: bank %s, head %s\n" % (R['bank'], R['head']))
    w("papers root:       %s\n" % R['papers_root'])
    w("code root:         %s\n\n" % R['code_root'])

    w(HR + "\nTHE FOUR NUMBERS, kept separate on purpose\n" + HR + "\n")
    w("  population              %6d  candidate spans -- a TEST token from the\n"
      "                                  closed vocabulary with a FIELD token\n"
      "                                  within 300 normalised characters\n" % R['population'])
    w("  coverage                %6d  of %d = %.1f%% -- candidate spans from which\n"
      "                                  at least one fact was extracted\n"
      % (R['covered'], R['population'], R['coverage_pct']))
    w("  raw disagreements       %6d  disagreeing fact-site PAIRS, before any\n"
      "                                  bucketing\n" % R['raw_pairs'])
    w("  after partitioning      %6d  pairs left once facts in the named\n"
      "                                  buckets are set aside\n" % R['net_pairs'])
    w("\n  field-selection inversions: %d (a separate, sharper test -- see below)\n"
      % R['n_inversions'])
    w("\n  distinct value-disagreements: %d raw / %d after partitioning\n"
      % (R['raw_distinct'], R['net_distinct']))
    w("  facts extracted: %d  (paper %d / code %d)\n"
      % (R['n_facts'], R['n_facts_paper'], R['n_facts_code']))
    w("  sources read:    %d live papers, %d code modules\n\n"
      % (R['n_live_papers'], R['n_code']))

    w(HR + "\nTHE VOCABULARY\n" + HR + "\n")
    w("  TESTS   %s\n" % ', '.join(sorted(TEST_FORMS)))
    w("  FIELDS  R, C, H\n")
    w("  FACT TYPES\n")
    for k, v in [('FS', 'a named TEST excludes or admits a named FIELD'),
                 ('TT_TARGET', 'the quaternionic composite is M_<coef>(<field>)'),
                 ('TT_REALDIM', 'its real dimension'),
                 ('SD', 'a FIELD departs by a SURPLUS or a DEFICIT'),
                 ('OD_DIM/OD_22', 'an observable-space dimension, joint or local')]:
        w("    %-12s %s\n" % (k, v))
    w("\n  Deliberately OUT of the vocabulary: 'local independence' (3 sites in\n"
      "  the tree, 0 in any paper -- no pair to compare, so including it would\n"
      "  only manufacture one-sided facts).\n\n")

    w(HR + "\nIDIOM INVENTORY -- a finding in its own right\n" + HR + "\n")
    w("Every previous sweep in this corpus grepped ONE spelling. There are\n"
      "%d live idioms for stating a field-selection verdict and they do not\n"
      "agree on word order: some make the TEST the subject and some make the\n"
      "FIELD the subject. A sweep written for either orientation alone reads\n"
      "half the corpus and silently reports the other half as clean.\n\n"
      % len([k for k in R['idiom_counts'] if k.startswith('I')]))
    w("  %-28s %6s %6s   %s\n" % ('idiom', 'papers', 'code', 'what it matches'))
    for k in sorted(R['idiom_counts'], key=lambda x: -sum(R['idiom_counts'][x].values())):
        c = R['idiom_counts'][k]
        w("  %-28s %6d %6d   %s\n" % (k, c.get('PAPER', 0), c.get('CODE', 0),
                                      IDIOMS.get(k, R['idiom_desc'].get(k, ''))))
    w("\nORIENTATION SPLIT (field-selection idioms only)\n")
    w("  TEST is the subject  (I1, I2, I7, I8, I10) : %d sites\n" % R['orient_A'])
    w("  FIELD is the subject (I3, I4, I5, I6, I9)  : %d sites\n" % R['orient_B'])

    w("\nBARE-LETTER ADMISSION CONTEXTS\n")
    w("  A bare R, C or H is a field ONLY inside one of these anchored forms.\n"
      "  The corpus is full of Hilbert spaces H, capacities C and result lists\n"
      "  R; without this list a token co-occurrence sweep is unusable.\n")
    for k, v in sorted(R['field_idioms'].items(), key=lambda kv: -kv[1]):
        w("    %-34s %5d\n" % (k, v))

    w("\n" + HR + "\nCOVERAGE -- what could not be reached, BY NAME\n" + HR + "\n")
    w("  unreadable .tex files      %d\n" % len(R['unreadable_tex']))
    for p, e in R['unreadable_tex']:
        w("     %s  (%s)\n" % (p, e))
    w("  .py files that did not fully parse   %d\n" % len(R['parse_notes']))
    for p, e in R['parse_notes']:
        w("     %s  (%s)\n" % (p, e))
    w("  candidate spans that produced NO fact  %d\n" % len(R['residual']))
    w("  -- these are spans naming a TEST with a FIELD nearby that this tool\n"
      "     could not reduce to a fact without inferring what the sentence\n"
      "     means. They are NOT clean; they are UNREAD. Listed by site.\n")
    byfile = collections.Counter(s['source'] for s in R['residual'])
    for f, c in byfile.most_common():
        w("     %-72s %4d\n" % (f, c))

    w("\n" + HR + "\nBUCKETS -- known-legitimate non-matches, named and listed\n" + HR + "\n")
    w("  Membership is a SYNTACTIC fact, not a verdict. A fact in a bucket is\n"
      "  set aside from the headline count and printed here so nobody chases it.\n\n")
    for k, v in sorted(R['bucket_counts'].items(), key=lambda kv: -kv[1]):
        w("    %-36s %5d facts\n" % (k, v))
    w("""
    B_CHANGELOG_REGION           a changelog entry STANDS AS WRITTEN by house
                                 convention and is never flagged. In these
                                 papers the changelog is the run of `%` lines
                                 at the head of the file, so every LaTeX
                                 comment is bucketed -- deliberately
                                 over-inclusive.
    B_QUOTED_RETIRED             Working Rule 18: the house correction
                                 convention QUOTES the retired sentence inside
                                 its own correction. A gate that flags that is
                                 structurally guaranteed to false-alarm.
    B_HYPOTHETICAL_OR_FIXTURE    a deliberately-wrong string used as a test
                                 fixture, a countermodel, or a mutation target.
    B_DIFFERENT_REGIME_OR_CONVENTION
                                 the corpus carries two counting conventions
                                 (full-dimension and trace-one / marginals-
                                 plus-correlations). Two sources under
                                 different conventions are not in conflict.
""")

    w("\n" + HR + "\nDISAGREEMENTS\n" + HR + "\n")
    w("Ordered by fact type. For each DISTINCT value-disagreement, every site\n"
      "on both sides is listed -- instances are counted, not collapsed.\n")
    for d in R['disagreements']:
        w("\n" + '-' * 78 + "\n")
        w("[%s] %s   form=%s   scopes=%s\n"
          % (d['kind'], '/'.join(d['key']), d['form'], ','.join(sorted(d['scopes']))))
        w("  side A: %s   (%d site%s)\n"
          % (fmt_val(d['kind'], d['value_a']), len(d['sites_a']),
             '' if len(d['sites_a']) == 1 else 's'))
        for s in d['sites_a']:
            w("     %-64s [%s/%s]\n        %s\n"
              % (s['site'], s['idiom'], s['provenance'], s['context'][:210]))
        w("  side B: %s   (%d site%s)\n"
          % (fmt_val(d['kind'], d['value_b']), len(d['sites_b']),
             '' if len(d['sites_b']) == 1 else 's'))
        for s in d['sites_b']:
            w("     %-64s [%s/%s]\n        %s\n"
              % (s['site'], s['idiom'], s['provenance'], s['context'][:210]))
        w("  pairs: %d\n" % d['n_pairs'])

    w("\n" + HR + "\nFIELD-SELECTION INVERSIONS\n" + HR + "\n")
    w("Two sources pairing the SAME two tests with the SAME two fields the\n"
      "opposite way round. This is the one attribution pattern that cannot be\n"
      "read as an additional exclusion. A source paired with ITSELF means one\n"
      "file carries both pairings.\n")
    if not R['inversions']:
        w("\n  none\n")
    for iv in R['inversions']:
        w("\n" + '-' * 78 + "\n")
        w("  %s\n  %s%s\n" % (iv['source_a'], iv['source_b'],
                               '   [SAME FILE]' if iv['self_pair'] else ''))
        w("    A: %s\n" % ', '.join('%s excludes %s' % kv
                                     for kv in sorted(iv['assignment_a'].items())))
        w("    B: %s\n" % ', '.join('%s excludes %s' % kv
                                     for kv in sorted(iv['assignment_b'].items())))
        for tag, ss in (('A', iv['sites_a']), ('B', iv['sites_b'])):
            for x in ss:
                w("      %s %-58s [%s]\n         %s\n"
                  % (tag, x['site'], x['idiom'], x['context'][:190]))

    if R['bucketed_disagreements']:
        w("\n" + HR + "\nSET ASIDE BY BUCKET (listed, not flagged)\n" + HR + "\n")
        for d in R['bucketed_disagreements']:
            w("\n[%s] %s   %s  vs  %s   buckets=%s\n"
              % (d['kind'], '/'.join(d['key']), fmt_val(d['kind'], d['value_a']),
                 fmt_val(d['kind'], d['value_b']), ','.join(sorted(d['buckets']))))
            for s in d['sites_a'] + d['sites_b']:
                w("     %-64s [%s]\n" % (s['site'], ','.join(s['buckets']) or '-'))

    if R.get('controls'):
        w("\n" + HR + "\nCONTROLS\n" + HR + "\n")
        for c in R['controls']:
            w("\n  %-10s %s\n" % (c['role'], c['path']))
            w("    expected: %s\n" % c['expected'])
            w("    FS disagreements against the code: %d  (of which inversions: %d)\n"
              % (c['n_fs'], c.get('n_inversions', 0)))
            w("    VERDICT: %s\n" % c['verdict'])
            for line in c['detail']:
                w("      %s\n" % line)


# ===========================================================================
# MAIN
# ===========================================================================

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


_LIB = _resolve_library_root()
DEF_PAPERS = os.path.join(_LIB, "Papers") if _LIB else None
DEF_CODE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'apf')

# BOTH control targets are ARCHIVED paths, and that is load-bearing.
# CONTROL_NEG previously named the LIVE top-level file; the house archive
# convention moves a superseded version into Old/ on every version bump, so
# that constant went dead and the negative control silently stopped running
# while the tool kept printing a number. An Old/ path is never renamed or
# overwritten by that convention (a name collision there takes a suffix),
# so it survives paper versioning. Do not re-point either at a live path.
CONTROL_POS = ("Paper 01 - The Enforceability of Distinction/Old/"
               "Paper_1_Enforceability_of_Distinction_v5.9.tex")
CONTROL_NEG = ("Paper 01 - The Enforceability of Distinction/Old/"
               "Paper_1_Enforceability_of_Distinction_v5.10.tex")


def fact_rows(facts):
    return [dict(site=f.site(), source=f.src.label, line=f.line, idiom=f.idiom,
                 provenance=f.provenance, defname=f.defname or '',
                 buckets=f.buckets, context=f.context, field_idiom=f.field_idiom)
            for f in facts]


def run_controls(papers_root, code_facts):
    out = []
    for role, rel, expect_fire in (
            ('POSITIVE', CONTROL_POS, True),
            ('NEGATIVE', CONTROL_NEG, False)):
        p = os.path.join(papers_root, rel)
        if not os.path.exists(p):
            out.append(dict(role=role, path=p, expected='n/a', n_fs=0,
                            n_inversions=0,
                            verdict='FILE NOT FOUND -- CONTROL DID NOT RUN',
                            detail=[]))
            continue
        s = load_tex(p, os.path.basename(p))
        facts, _, _ = analyse(s)
        fs = [f for f in facts if f.kind == 'FS' and not f.buckets]
        pool = fs + [f for f in code_facts if f.kind == 'FS' and not f.buckets]
        detail = []

        # (a) polarity conflicts with one side in the control file
        real = []
        for d in disagreements(pool):
            for fa, fb in pairs_of(d):
                if fa.src.path != fb.src.path and \
                        (fa.src.path == p or fb.src.path == p):
                    real.append((d, fa, fb))
        seen = set()
        for d, fa, fb in real:
            k = (tuple(d['key']), tuple(d['value_a']), tuple(d['value_b']))
            if k in seen:
                continue
            seen.add(k)
            detail.append("POLARITY %s: %s vs %s"
                          % ('/'.join(d['key']), d['value_a'][0], d['value_b'][0]))
            detail.append("    %s:%d  %s" % (fa.src.label, fa.line, fa.context[:150]))
            detail.append("    %s:%d  %s" % (fb.src.label, fb.line, fb.context[:150]))

        # (b) inversions with one side in the control file
        invs = [iv for iv in inversions(pool)
                if not iv['self_pair'] and (iv['source_a'] == p or iv['source_b'] == p)]
        for iv in invs:
            ctl_is_a = (iv['source_a'] == p)
            ca = iv['assignment_a'] if ctl_is_a else iv['assignment_b']
            cb = iv['assignment_b'] if ctl_is_a else iv['assignment_a']
            other = iv['source_b'] if ctl_is_a else iv['source_a']
            detail.append("INVERSION vs %s" % os.path.basename(other))
            detail.append("    control: " + ', '.join('%s excludes %s' % kv
                                                      for kv in sorted(ca.items())))
            detail.append("    code:    " + ', '.join('%s excludes %s' % kv
                                                      for kv in sorted(cb.items())))
            for x in (iv['sites_a'] + iv['sites_b']):
                detail.append("    %s:%d [%s] %s" % (x.src.label, x.line, x.idiom,
                                                     x.context[:130]))
        real = real + invs
        fired = len(real) > 0
        ok = (fired == expect_fire)
        out.append(dict(
            role=role, path=p,
            expected=('MUST FIRE -- v5.9 is the pre-fix text'
                      if expect_fire else
                      'MUST STAY SILENT -- v5.10 is the corrected text'),
            n_fs=len(real), n_inversions=len(invs),
            verdict=('PASS -- ' + ('fired as required' if fired else 'silent as required'))
                    if ok else
                    ('FAIL -- ' + ('fired when it must not' if fired
                                   else 'DID NOT FIRE. THE TOOL DOES NOT WORK.')),
            detail=detail))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--papers', default=DEF_PAPERS)
    ap.add_argument('--code', default=DEF_CODE)
    ap.add_argument('--json', default=None)
    ap.add_argument('--report', default=None)
    ap.add_argument('--idioms', action='store_true')
    ap.add_argument('--no-controls', action='store_true')
    args = ap.parse_args()

    live, other, unreadable_tex = gather_papers(args.papers)
    code, unreadable_py = gather_code(args.code)

    all_facts = []
    population = covered = 0
    residual = []
    parse_notes = []

    n_live = n_code = 0
    for cls, p in live:
        try:
            s = load_tex(p, os.path.relpath(p, args.papers))
        except Exception as e:                              # noqa: BLE001
            unreadable_tex.append((p, str(e)))
            continue
        n_live += 1
        f, cands, cov = analyse(s)
        all_facts += f
        population += len(cands)
        covered += sum(1 for c in cov if c)
        for (ta, tb, tid), ok in zip(cands, cov):
            if not ok:
                residual.append(dict(source=s.label, line=s.line_of(ta), test=tid,
                                     context=_ctx(s, ta, tb)[:220]))
        del s
    for p in code:
        try:
            s = load_py(p, os.path.relpath(p, os.path.dirname(args.code)))
        except Exception as e:                              # noqa: BLE001
            unreadable_py.append((p, str(e)))
            continue
        n_code += 1
        if s.parse_note:
            parse_notes.append((s.path, s.parse_note))
        f, cands, cov = analyse(s)
        all_facts += f
        population += len(cands)
        covered += sum(1 for c in cov if c)
        for (ta, tb, tid), ok in zip(cands, cov):
            if not ok:
                residual.append(dict(source=s.label, line=s.line_of(ta), test=tid,
                                     context=_ctx(s, ta, tb)[:220]))
        del s

    # ---- idiom inventory ----
    idiom_counts = collections.defaultdict(collections.Counter)
    for f in all_facts:
        idiom_counts[f.idiom][f.src.kind] += 1
    field_idioms = collections.Counter(f.field_idiom for f in all_facts if f.field_idiom)
    bucket_counts = collections.Counter()
    for f in all_facts:
        for b in f.buckets:
            bucket_counts[b] += 1

    A = {'I1_TEST_VERB_FIELD', 'I2_TEST_PAREN_FIELD', 'I7_RESPECTIVELY',
         'I8_CANNOT_SUPPLY', 'I10_TEST_SELECTS_FIELD'}
    B = {'I3_FIELD_VERB_TEST', 'I4_FIELD_PASSIVE_TEST', 'I5_HEADING_EXCLUSION',
         'I6_ENCLOSING_DEF', 'I9_ONLY_FIELDS_PASS'}
    orient_A = sum(sum(idiom_counts[k].values()) for k in A)
    orient_B = sum(sum(idiom_counts[k].values()) for k in B)

    # ---- disagreements ----
    raw = disagreements(all_facts)
    raw_pairs = sum(len(d['sites_a']) * len(d['sites_b']) for d in raw)
    clean_facts = [f for f in all_facts if not f.buckets]
    net = disagreements(clean_facts)
    net_pairs = sum(len(d['sites_a']) * len(d['sites_b']) for d in net)

    def pack(dlist):
        out = []
        for d in dlist:
            scopes = {scope_of(a, b) for a, b in pairs_of(d)}
            buckets = sorted({x for f in d['sites_a'] + d['sites_b'] for x in f.buckets})
            out.append(dict(kind=d['key'][0], key=[str(x) for x in d['key']],
                            form=d['form'],
                            value_a=list(d['value_a']), value_b=list(d['value_b']),
                            sites_a=fact_rows(d['sites_a']),
                            sites_b=fact_rows(d['sites_b']),
                            n_pairs=len(d['sites_a']) * len(d['sites_b']),
                            scopes=sorted(scopes), buckets=buckets,
                            exclusive_form=any(is_exclusive(f)
                                               for f in d['sites_a'] + d['sites_b'])))
        return out

    invs = inversions(clean_facts)
    invs_packed = [dict(source_a=os.path.relpath(iv['source_a'], os.path.dirname(args.code))
                        if iv['source_a'].endswith('.py') else iv['source_a'],
                        source_b=os.path.relpath(iv['source_b'], os.path.dirname(args.code))
                        if iv['source_b'].endswith('.py') else iv['source_b'],
                        assignment_a=iv['assignment_a'], assignment_b=iv['assignment_b'],
                        sites_a=fact_rows(iv['sites_a']), sites_b=fact_rows(iv['sites_b']),
                        self_pair=iv['self_pair']) for iv in invs]
    net_packed = pack(net)
    raw_packed = pack(raw)
    net_keys = {(tuple(d['key']), tuple(d['value_a']), tuple(d['value_b']))
                for d in net_packed}
    bucketed = [d for d in raw_packed
                if (tuple(d['key']), tuple(d['value_a']), tuple(d['value_b'])) not in net_keys]

    # ---- bank / head, read not assumed ----
    repo = os.path.dirname(os.path.abspath(args.code))
    bank = head = 'unknown'
    try:
        sys.path.insert(0, repo)
        from apf import bank as _b
        _b._load()
        bank = '%d/%d' % (len(_b.REGISTRY), _b.EXPECTED_THEOREM_COUNT)
    except Exception as e:                                  # noqa: BLE001
        bank = 'not read (%s)' % type(e).__name__
    try:
        with open(os.path.join(repo, '.git', 'HEAD')) as f:
            ref = f.read().strip()
        if ref.startswith('ref:'):
            with open(os.path.join(repo, '.git', ref[5:].strip())) as f:
                head = f.read().strip()[:7]
        else:
            head = ref[:7]
    except Exception:                                       # noqa: BLE001
        pass

    controls = None if args.no_controls else run_controls(
        args.papers, [f for f in all_facts if f.src.kind == 'CODE'])

    R = dict(
        bank=bank, head=head, papers_root=args.papers, code_root=args.code,
        population=population, covered=covered,
        coverage_pct=(100.0 * covered / population if population else 0.0),
        raw_pairs=raw_pairs, net_pairs=net_pairs,
        raw_distinct=len(raw_packed), net_distinct=len(net_packed),
        n_facts=len(all_facts),
        n_facts_paper=sum(1 for f in all_facts if f.src.kind == 'PAPER'),
        n_facts_code=sum(1 for f in all_facts if f.src.kind == 'CODE'),
        n_live_papers=n_live, n_code=n_code,
        idiom_counts={k: dict(v) for k, v in idiom_counts.items()},
        idiom_desc={'TT1_COMPOSITE_ALGEBRA': 'M_n(H) (x)_R M_m(H) is M_<coef>(<field>)',
                    'TT2_COMPOSITE_REAL_DIMENSION': 'its real dimension <c>n^2m^2',
                    'SD1_FIELD_DIRECTION': 'FIELD departs by a SURPLUS or a DEFICIT',
                    'OD1_DIMENSION_FUNCTION': 'd_F(n) = v',
                    'OD2_JOINT_LOCAL_PAIR': 'joint=, local= for a field'},
        orient_A=orient_A, orient_B=orient_B,
        field_idioms=dict(field_idioms), bucket_counts=dict(bucket_counts),
        unreadable_tex=unreadable_tex,
        parse_notes=parse_notes + [(p, e) for p, e in unreadable_py],
        residual=residual,
        disagreements=net_packed, bucketed_disagreements=bucketed,
        inversions=invs_packed, n_inversions=len(invs_packed),
        facts=[f.as_dict() for f in all_facts],
        controls=controls,
        excluded_from_population=dict(
            OLD=sum(1 for c, _ in other if c == 'OLD'),
            REVIEWS=sum(1 for c, _ in other if c == 'REVIEWS'),
            TO_DELETE=sum(1 for c, _ in other if c == 'TO_DELETE'),
            ANCILLARY=sum(1 for c, _ in other if c == 'ANCILLARY')),
    )

    here = os.path.dirname(os.path.abspath(__file__))
    jpath = args.json or os.path.join(here, 'contradiction_census.json')
    with open(jpath, 'w', encoding='utf-8') as f:
        json.dump(R, f, indent=1, sort_keys=True, ensure_ascii=False)

    buf = io.StringIO()
    write_report(buf, R)
    txt = buf.getvalue()
    if args.report:
        with open(args.report, 'w', encoding='utf-8', newline='\n') as f:
            f.write(txt)
    sys.stdout.write(txt)


if __name__ == '__main__':
    main()
