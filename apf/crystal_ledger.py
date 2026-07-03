"""The crystal strengthening ledger -- grade census + dispositioned sub-[P]
ranking over the CORE (spine) view. Dashboard data source (Wave 8+,
2026-07-02); consumed by scripts/gen_ie_onboarding_dashboard_data.py
--with-crystal and the apf-ie-onboarding-coverage artifact.

NOT a bank module (no register()): analysis layer over apf.crystal +
apf.crystal_metrics. The disposition map below is CURATED (2026-07-02,
the strengthening-ledger session): sub-[P] on the spine is not a defect
list -- most entries are deliberate fences (the T27d seam / the w~g^2
dictionary), bespoke tokens, or the permanent IJC empirical import. The
ledger exists to separate those from the genuine strengthening programs:
(1) the T27d seam -> the effective-angle transport program (the largest
single grade-uplift available; 64% of the spine downstream);
(2) L_singlet_Gram -> the a=b common-demand identity [C];
(3, candidate) the IJC reading-exhaustiveness walk.
"""
from __future__ import annotations
import collections
from typing import Dict, List

LEDGER_DISPOSITIONS_EXACT = {
    'T27d': ('THE PRIZE: 64% of the spine downstream; seam fence by design '
             '(w~g^2 dictionary, Paper 42); promotion = the effective-angle '
             'transport program'),
    'T24': 'seam fence by design; rides the T27d program',
    'T_sin2theta': ('seam fence by design (the ledger share is [P] via '
                    'check_T_ew_load_placement_P); rides the T27d program'),
    'T_sin2theta_higgs_record': 'seam family; rides the T27d program',
    'L_crossing_self_energy': 'seam family; rides the T27d program',
    'L_crossing_depletion_capacity_measure': 'seam family; rides the T27d program',
    'L_singlet_Gram': ('NAMED ROUTE: prove the a=b common-demand identity [C] '
                       '(open kernel, .330/.338)'),
    'L_singlet_Gram_exchangeable_form': ('the .330 witness at its natural grade; '
                                         'promotion rides the a=b identity'),
    'T_no_IJC_no_noncommutativity': ('CANDIDATE WALK: no-third-reading '
                                     'exhaustiveness (the .284 pattern)'),
    'T_IJC_dichotomy': 'candidate walk: rides the reading-exhaustiveness family',
    'T_which_v_no_registered_interior_reader': 'drift-net instrument at natural grade (.318)',
    'T_vglobal_slot_identification_no_go': 'no-go at natural grade (.326); never cite as open',
    'T_vglobal_offdiagonal_blocks_scalar_typed': 'drift-net instrument at natural grade (.339)',
    'T_vacuum_content_typing_status': ('typing pin at natural grade (.321); slot-level '
                                       'relocated to the broken basis (.326)'),
    'T_FormalKernel_VLambda_uniqueness': 'executable witness at natural grade',
    'T_four_input_declaration': 'foundational declaration; grade is the honest form',
    'T_partition_rigidity_coverage_v69': 'bespoke exhaustive token by design',
}

def _disposition(nid: str, grade: str) -> str:
    if nid in LEDGER_DISPOSITIONS_EXACT:
        return LEDGER_DISPOSITIONS_EXACT[nid]
    if grade == 'P+IJC':
        return ('PERMANENT IMPORT: IJC = the empirical QAC (keystone '
                'settlement 2026-06-26); not a theorem gap')
    if grade == 'P_regime':
        return 'regime-scoped by design; disposition check optional'
    if grade == 'P_structural_reading':
        return 'reading grade; exhaustiveness open (candidate-walk family)'
    if grade == 'P_structural_seam':
        return 'seam family; rides the T27d program'
    if grade in ('P_comp', 'P_structural_exhaustive'):
        return 'bespoke composition/exhaustive token by design'
    return 'structural grade; no named promotion route (disposition owed)'

_BARE = ('P', 'AXIOM', 'AXIOM_COROLLARY', '[P]')

def crystal_dashboard_section(preset: str = 'CORE') -> Dict:
    """Grade census + dispositioned sub-[P] ledger. Requires a populated
    bank REGISTRY (the caller loads modules; verify_all/native runs have it;
    the dashboard generator registers first)."""
    from apf import _module_manifest as mm, bank
    if not bank.REGISTRY:
        import importlib
        for m in list(mm.BANK_REGISTRY_MODULES):
            try:
                mod = importlib.import_module(m)
                if hasattr(mod, 'register'):
                    mod.register(bank.REGISTRY)
            except Exception:
                pass
    from apf.crystal import build_crystal
    from apf.crystal_metrics import betweenness_centrality
    c = build_crystal(preset, do_prelude=False)
    g = c['full_graph']
    items = list(g.nodes.items()) if isinstance(g.nodes, dict) else [(n.id, n) for n in g.nodes]
    nd = {nid: (n if isinstance(n, dict) else n.__dict__) for nid, n in items}
    children: Dict[str, set] = collections.defaultdict(set)
    for nid, d in nd.items():
        for p in (d.get('dependencies') or ()):
            if p in nd:
                children[p].add(nid)
    memo: Dict[str, set] = {}
    onstack: set = set()
    def desc(u):
        if u in memo:
            return memo[u]
        if u in onstack:
            return set()
        onstack.add(u)
        s: set = set()
        for v in children.get(u, ()):
            s.add(v)
            s |= desc(v)
        onstack.discard(u)
        memo[u] = s
        return s
    bc = betweenness_centrality(g)
    rows: List[Dict] = []
    for nid, d in nd.items():
        if d['epistemic'] in _BARE:
            continue
        rows.append({
            'id': nid, 'grade': d['epistemic'],
            'module': str(d['module']).replace('apf.', ''),
            'desc': len(desc(nid)), 'betw': round(bc.get(nid, 0.0), 4),
            'disposition': _disposition(nid, d['epistemic']),
        })
    rows.sort(key=lambda r: (-r['desc'], -r['betw'], r['id']))
    grades = collections.Counter(d['epistemic'] for d in nd.values())
    return {
        'view': preset + ' (spine) -- the Paper 20 canonical view; EXTENDED rides a native run',
        'spine_nodes': len(nd),
        'grade_counts': dict(grades.most_common()),
        'sub_p_count': len(rows),
        'strengthening_programs': [
            'T27d seam -> the effective-angle transport program (167 spine descendants)',
            'L_singlet_Gram -> the a=b common-demand identity [C]',
            'candidate: the IJC reading-exhaustiveness walk',
        ],
        'ledger': rows,
        'honesty': ('curated dispositions 2026-07-02; sub-[P] is NOT a defect '
                    'list -- most entries are deliberate fences, bespoke tokens, '
                    'or the permanent IJC empirical import; the ledger separates '
                    'those from the genuine strengthening programs'),
    }
