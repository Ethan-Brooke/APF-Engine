"""APF DERIVED IDENTITY MAP -- H5 step 2, the derive-only gate.

A REPORTING TOOL. It declares nothing, repairs nothing, and asserts nothing
about whether any citation is correct. It answers one question: given the
live registry, what set of strings does each banked object demonstrably
answer to WITHOUT anyone writing a declaration?

SPEC: Artifacts_2026-08-07_session/returns/SPEC_H5_declaration_layer_2026-08-07.md
      section 6.3 step 2. Ruled by Ethan 2026-08-11.

WHAT IS DERIVED (never declared):
  * the live registry key, both spellings (bare and check_-prefixed)
  * fn.__name__, both spellings
  * the epistemic-suffix genre: a def carrying a trailing _P / _C / _P_local
    etc. whose key drops it

WHAT IS NOT HERE, BY DESIGN: CITABLE_AS, PUBLISHES, namespace markers. Those
are the DECLARED half (spec sections 3.1-3.4) and are a separate decision.
Declaring what is already derivable is the mechanical-retrofit shape the spec
forbids, so this file writes no declaration and reads none.
"""
import collections
import io
import contextlib
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_EPISTEMIC = re.compile(r"_(P|C|P_local|P_math|P_structural|P_regime|P_boundary)$")


def load_registry():
    sys.path.insert(0, REPO)
    from apf import bank as _bank                                    # noqa
    with contextlib.redirect_stdout(io.StringIO()):
        _bank._load()
    return _bank.REGISTRY


def spellings(s):
    """Both spellings of one name. D6@2026-08-03: two keying conventions
    coexist permanently, so every by-name surface checks both, forever."""
    out = {s}
    out.add(s[6:] if s.startswith("check_") else "check_" + s)
    return out


def factory_def_names(registry):
    """def names that back MORE THAN ONE registry key.

    THE DEFECT THIS EXISTS TO CLOSE, found by building the map rather than by
    reading the spec. SPEC clause 1 is INJECTIVITY, and a map that admits every
    `fn.__name__` as an alias is NOT injective: one helper `def` is registered
    under many keys by the adapter factories, so its name identifies a family
    rather than an object. `_check_payload_closure_kind` backs 17 registry
    entries; `_check_atlas_routes_to_identity_status` backs 12.

    A factory-minted closure's `__name__` is the FACTORY's name, not the
    object's identity. Admitting it makes the map ambiguous exactly where
    clause 1 forbids ambiguity, so it is excluded -- and the exclusion is
    COUNTED and REPORTED rather than applied silently, because dropping names
    until a collision count reaches zero is the self-favouring direction.
    """
    seen = collections.Counter()
    for key, fn in registry.items():
        dn = getattr(fn, "__name__", None)
        if dn:
            seen[dn] += 1
    return {dn for dn, c in seen.items() if c > 1}


def derived_map(registry, exclude_factory=True):
    """key -> set of strings this object demonstrably answers to.

    Every member is READ off a live object. Nothing is minted.

    `exclude_factory=False` reproduces the pre-fix, NON-INJECTIVE map and
    exists so the fix has a negative control: the caller can show the
    collisions return when the exclusion is lifted.
    """
    shared = factory_def_names(registry) if exclude_factory else set()
    m = {}
    for key, fn in registry.items():
        names = set()
        names |= spellings(key)
        dn = getattr(fn, "__name__", None)
        if dn and dn not in shared:
            names |= spellings(dn)
            stripped = _EPISTEMIC.sub("", dn)
            if stripped != dn:
                names |= spellings(stripped)
        m[key] = names
    return m


def main(argv):
    reg = load_registry()
    shared = factory_def_names(reg)
    dm = derived_map(reg)

    all_names = set()
    for v in dm.values():
        all_names |= v

    # injectivity, reported not enforced -- this tool makes no claim
    owner = collections.defaultdict(set)
    for k, v in dm.items():
        for n in v:
            owner[n].add(k)
    collisions = {n: sorted(ks) for n, ks in owner.items() if len(ks) > 1}

    # how much of the map is NOT already the trivial key spellings
    beyond_key = set()
    for k, v in dm.items():
        beyond_key |= (v - spellings(k))

    print(f"registry keys                {len(reg)}")
    print(f"distinct derived strings     {len(all_names)}")
    print(f"  of which beyond the key    {len(beyond_key)}"
          f"   <- what a key-only resolver cannot see")
    print(f"factory def names EXCLUDED   {len(shared)}"
          f"   <- one def registered under many keys; its name identifies a"
          f" FAMILY, not an object (SPEC clause 1)")
    print(f"collisions (same string, >1 object)  {len(collisions)}")
    for n, ks in sorted(collisions.items())[:10]:
        print(f"    {n}  ->  {', '.join(ks)}")
    return dm, all_names, beyond_key


if __name__ == "__main__":
    main(sys.argv)
