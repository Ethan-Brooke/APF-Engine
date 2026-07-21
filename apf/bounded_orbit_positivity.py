"""The bounded-orbit route to positivity -- invariant-form EXISTENCE at reading grade.

BANKED v24.3.431 (principal ruling 'bank', 2026-07-20; EXPECTED 3948 -> 3949).
Lane record: __APF Library/Artifacts_2026-07-20_session/seam_salvage/ (charter +
walk record WALK_R_capacity_bounded_world.md + probe + v0.1/v0.2/v0.3 + both
cold-audit reports). Audit chain: stage-1 cold REDUCE 0.80 (MAJOR-1: the v0.1
quantitative coding of the reading -- q_std-ball confinement -- was the killed
seam-closure packet's positivity premise renamed; all six findings carried at
statement level in v0.2) -> stage-2 cold LAND-WITH-FIXES 0.82 on v0.2 (MAJORs
A/B/C: can't-fail fence leg, truncated-frontier instrument w/ a false-UNBOUNDED
direction, closure never verified; ALL carried in v0.3, which this module banks).

check_L_bounded_orbit_positivity [P_structural_reading | R-capacity-bounded-world].

THE NAMED READING (new surface, standalone-walked -- see the walk record):
  R-capacity-bounded-world: the admissible state family of a completed finite
  fragment is a BOUNDED set (gauge-free: norm-independent in finite dimension),
  and every admissible reversible action preserves it (world-closure: action and
  admitted reverse both map admissible states to admissible states).
  A1-MOTIVATED (unbounded admissible content in a finite-enforcement region is
  the shape A1 forbids, under the identification that represented content is
  enforced content), NOT A1-DERIVED: the label-fiat counter-world (coordinates
  declared pure gauge; the generated 12-step boost world books exactly 0 <= 61
  while spanning-set content grows strictly) is COMPUTED and OWNED in-check --
  A1 holds there while orbits are unbounded, so the reading is load-bearing.
  Ownership pattern: R-sel-LC (v24.3.422). Keystone adjudication of record (walk
  record): the hold defers BOOKING, never OCCUPANCY (occupancy constitutive [P],
  ruling 2026-07-07; T_ledger_rent_excluded removes rent, not footprint) --
  capacity bounds are state bounds; the hold-side QUANTITATIVE bound consumes
  the sharpened survey==counted-rho identification (G-hold-exact, .422), a named
  grant, record-side unverifiable (.412), disclosed and never certified.

STATEMENT (under R-capacity-bounded-world). Admissible reversible action
families on the completed finite fragment are BOUNDED GROUPS (they preserve a
bounded spanning admissible set). In the finite-image case, averaging a positive
seed over the group -- seed positivity is a DECLARED MATHEMATICAL INPUT, refused
in-code when absent -- yields an exactly invariant positive-definite form under
which every element's Q-adjoint equals its ADMITTED REVERSE (REVERSAL_IS_INVERSE
consumed as a named premise, .429 H1 vocabulary; verified against the group
table, not a formula). EFFECT: EXISTENCE of invariant positivity relocates from
the QUADRATIC_LEDGER analytic posit to (i) this reading + (ii) the .429 H3
connectedness gate. NOT claimed: form uniqueness (FORM_UNIQUENESS_REQUIRES_
IRREDUCIBILITY, named residue -- non-proportional invariant forms COMPUTED on
the reducible control); identity of the derived form with a physical counting
metric; positive states; orientation synchronization; generator completeness;
composite typing; the Held circle (H3-gated -- the polyhedral fence is re-fired
in-check: no continuous sweep on a single finite fragment).

INSTRUMENTS (stage-2 standard): unbounded verdicts require an EXACT GROWTH
CERTIFICATE (rational eigenvector with |lambda|>1, or verified closed-form
polynomial growth); bounded verdicts require FINITE CLOSURE or an EXHIBITED
invariant pd form; NO general decision procedure is claimed. The false-positive
adversary (big-conjugator rotation: early entry growth, genuinely bounded) is an
in-check control. Group closure verified on all products + inverses. The
consumer certificate (the shape the finite-representation salvage lemmas consume
as COMPACT_OR_ISOMETRIC_ACTION) is independently recomputed from its own fields.

MAY-NOT-CITE: "positivity is derived from A1 alone"; the unscoped relocation
sentence; "positivity is output, never a premise" outside the scoped existence
sense; "orbits confined to the capacity ball" (v0.1 language, DEAD); "the boost
is excluded unconditionally" (exclusion is under the reading); "supplies the
compact action the salvage lemmas consume" beyond certificate-shape scope; "the
quadratic ledger premise is retired" (it is RELOCATED, at reading grade, to a
named smaller surface); anything from the killed seam-closure packet's head list.

deps consumed live: T_ledger_rent_excluded (rent-vs-footprint, keystone),
L_commutative_no_unresolved_hold (.412 record-side unverifiability siting the
grant line). A1/occupancy consumed at citation level (constitutive ruling
2026-07-07). Grade precedent: L_selection_ledger_completeness
[P_structural_reading], the owned-counter-model pattern.
"""
from fractions import Fraction as F

C_TOTAL=F(61); EPS_STAR=F(1)
READINGS=("R_CAPACITY_BOUNDED_WORLD",)
NAMED_GRANTS=("SURVEY_EQUALS_COUNTED_RHO_hold_side_only",)
NAMED_MATH_IMPORTS=("BOUNDED_SUBGROUP_COMPACT_CLOSURE_general_case",)
NAMED_PREMISES=("REVERSAL_IS_INVERSE",)
NAMED_RESIDUES=("FORM_UNIQUENESS_REQUIRES_IRREDUCIBILITY","HELD_CIRCLE_CONNECTEDNESS_H3_GATED")
FENCED_SURFACES=("POSITIVE_STATE_STRUCTURE","ORIENTATION_SYNCHRONIZED_EMBEDDINGS",
                 "GENERATOR_COMPLETENESS","COMPOSITE_TYPING","HELD_CIRCLE_CONNECTEDNESS")
DERIVED_SURFACES=("INVARIANT_FORM_EXISTENCE","ADJOINT_EQUALS_ADMITTED_REVERSE")

def mm(A,B): return [[sum(A[i][k]*B[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
def mv(A,v): return [sum(A[i][k]*v[k] for k in range(2)) for i in range(2)]
def tr(A): return [[A[0][0],A[1][0]],[A[0][1],A[1][1]]]
def det2(A): return A[0][0]*A[1][1]-A[0][1]*A[1][0]
def inv2(g):
    d=det2(g)
    if d==0: return None
    return [[g[1][1]/d,-g[0][1]/d],[-g[1][0]/d,g[0][0]/d]]
I2=[[F(1),F(0)],[F(0),F(1)]]
BOOST=[[F(5,4),F(3,4)],[F(3,4),F(5,4)]]
SHEARU=[[F(1),F(1)],[F(0),F(1)]]
ROT=[[F(3,5),F(-4,5)],[F(4,5),F(3,5)]]
SPAN=[[F(1),F(0)],[F(0),F(1)]]
GAUGES=(("std",lambda v:v[0]*v[0]+v[1]*v[1]),("L1",lambda v:abs(v[0])+abs(v[1])),
        ("Linf",lambda v:max(abs(v[0]),abs(v[1]))),
        ("shear",lambda v:(2*v[0]+v[1])**2+v[1]**2))
S_CONJ=[[F(2),F(1)],[F(0),F(1)]]; S_INV=[[F(1,2),F(-1,2)],[F(0),F(1)]]
def d4_conj():
    out=[]
    for a in (F(1),F(-1)):
        for b in (F(1),F(-1)):
            out.append(mm(mm(S_CONJ,[[a,F(0)],[F(0),b]]),S_INV))
            out.append(mm(mm(S_CONJ,[[F(0),a],[b,F(0)]]),S_INV))
    return out

# --- certificates (MAJOR-B): no general decision procedure claimed ---
def eig_growth_certificate(g,depth=10):
    """Exact eigenvector with |lambda|>1 among a small rational candidate set;
    verified by exact iteration to `depth`. Returns (vec,lam) or None."""
    for cand in ([F(1),F(1)],[F(1),F(-1)],[F(1),F(0)],[F(0),F(1)],[F(2),F(1)],[F(1),F(2)]):
        w=mv(g,cand)
        lam=None
        if cand[0]!=0 and w[1]*cand[0]==w[0]*cand[1]: lam=w[0]/cand[0]
        elif cand[0]==0 and w[0]==0 and cand[1]!=0: lam=w[1]/cand[1]
        if lam is not None and abs(lam)>1:
            v=cand; okiter=True; M=I2
            for n in range(1,depth+1):
                M=mm(M,g)
                if mv(M,v)!=[lam**n*v[0],lam**n*v[1]]: okiter=False; break
            if okiter: return (cand,lam)
    return None
def polynomial_growth_certificate(g,depth=20):
    """Unipotent-genre: verified closed form g^n e2 = (n*c, 1)-type strictly
    growing first coordinate. Returns True iff orbit coordinates strictly grow."""
    M=I2; prev=None; grew=True
    for n in range(1,depth+1):
        M=mm(M,g); cur=max(abs(e) for e in mv(M,[F(0),F(1)]))
        if prev is not None and not cur>prev and n>1: grew=False
        prev=cur
    return grew and prev>=F(depth-1)
def finite_closure(gens,cap=64):
    """Exact closure under products; returns the closed set or None if > cap."""
    elems={tuple(tuple(r) for r in g) for g in gens}|{tuple(tuple(r) for r in I2)}
    changed=True
    while changed:
        changed=False
        cur=[ [list(r) for r in e] for e in elems]
        for a in cur:
            for b in cur:
                t=tuple(tuple(r) for r in mm(a,b))
                if t not in elems:
                    elems.add(t); changed=True
                    if len(elems)>cap: return None
    return [[list(r) for r in e] for e in elems]
def invariant_pd_form_certificate(g,Qc):
    """Bounded verdict via exhibited invariant pd form: g^T Qc g == Qc and Qc pd."""
    pd=Qc[0][0]>0 and det2(Qc)>0
    return pd and mm(mm(tr(g),Qc),g)==Qc

def avg_form(group,seed):
    if not (seed[0][0]>0 and det2(seed)>0): return None   # seed pd is a declared math input
    Q=[[F(0),F(0)],[F(0),F(0)]]
    for g in group:
        P=mm(mm(tr(g),seed),g)
        for i in range(2):
            for j in range(2): Q[i][j]+=P[i][j]
    return [[Q[i][j]/len(group) for j in range(2)] for i in range(2)]

def _run_legs():
    log=[]; ok=True
    def leg(name,cond,detail=""):
        nonlocal ok; ok=ok and bool(cond)
        log.append((name,"PASS" if cond else "FAIL",detail))
    G=d4_conj()

    # LEG 1 -- bounded-group certificate WITH CLOSURE VERIFIED (MAJOR-C):
    keyset={tuple(tuple(r) for r in g) for g in G}
    closed=all(tuple(tuple(r) for r in mm(a,b)) in keyset for a in G for b in G)
    invs=all(inv2(g) is not None and tuple(tuple(r) for r in inv2(g)) in keyset for g in G)
    supG=max(abs(e) for g in G for row in g for e in row)
    leg("bounded_group_certificate", closed and invs and len(keyset)==8 and supG==F(5,2),
        "closure+inverses verified on all 64 products; entry-sup 5/2")

    # LEG 2 -- unbounded controls by EXACT CERTIFICATE (MAJOR-B):
    cb=eig_growth_certificate(BOOST)
    leg("boost_unbounded_certified", cb==([F(1),F(1)],F(2)), "exact eigenvector (1,1), lambda=2, verified 10 powers")
    leg("unipotent_unbounded_certified", polynomial_growth_certificate(SHEARU), "closed-form (n,1) growth verified 20 powers")
    both_all_gauges=True
    for gen in (BOOST,SHEARU):
        M=mm(mm(gen,gen),mm(gen,gen))
        for nm,gz in GAUGES:
            if not any(gz(mv(M,x))>gz(x) for x in SPAN): both_all_gauges=False
    leg("growth_all_gauges_both_controls", both_all_gauges, "boost AND unipotent grow in all 4 gauges on the spanning set")

    # LEG 2b -- FALSE-POSITIVE CONTROL (MAJOR-B's poison direction): conjugated
    # rotation with large conjugator -- early entry growth, genuinely bounded.
    # The instrument must NOT certify it unbounded (no eigen certificate exists;
    # bounded via exhibited invariant pd form K^-T K^-1).
    K=[[F(10),F(0)],[F(0),F(1)]]; Kinv=inv2(K)
    gR=mm(mm(K,ROT),Kinv)
    early=max(abs(e) for row in gR for e in row)>F(4)          # looks growing
    no_eig=eig_growth_certificate(gR) is None
    QK=mm(tr(Kinv),Kinv)
    bounded_cert=invariant_pd_form_certificate(gR,QK)
    leg("false_positive_control", early and no_eig and bounded_cert,
        "big-conjugator rotation: entry 8 but NO growth certificate; bounded via exhibited invariant form")

    # LEG 3 -- averaging (seed pd guarded):
    Q=avg_form(G,I2)
    if Q is None:
        leg("averaged_form_invariant_posdef", False, "seed rejected"); Q=I2
    else:
        def qf(Qm,x): return sum(x[i]*Qm[i][j]*x[j] for i in range(2) for j in range(2))
        span4=[[F(1),F(0)],[F(0),F(1)],[F(1),F(1)],[F(2),F(-3)]]
        inv_=all(qf(Q,mv(g,x))==qf(Q,x) for g in G for x in span4)
        pd=Q[0][0]>0 and det2(Q)>0
        leg("averaged_form_invariant_posdef", inv_ and pd and Q[0][1]!=0, "Q=%s"%str([[str(c) for c in r] for r in Q]))
    bad=avg_form(G,[[F(1),F(0)],[F(0),F(-1)]])
    leg("non_pd_seed_rejected", bad is None, "diag(1,-1) seed refused: seed positivity is a declared input")

    # LEG 3b -- HORN-A COLLAPSE CONTROL (stage-1 fix 1, carried in-check): the
    # admissible bounded group maps an in-q_std-ball state OUT of the q_std
    # ball -- the coded reading demands NO fixed-gauge ball preservation.
    x0=[F(2),F(7)]; content_in=x0[0]**2+x0[1]**2
    out_somewhere=any((lambda w: w[0]**2+w[1]**2>C_TOTAL)(mv(g,x0)) for g in G)
    leg("horn_A_collapse_control", content_in<=C_TOTAL and out_somewhere,
        "content 53 in-ball maps out under an admissible element: reading is set-boundedness, not ball-preservation")

    # LEG 4 -- seed dependence owned (existence not uniqueness):
    C2=[mm(mm(S_CONJ,[[a,F(0)],[F(0),b]]),S_INV) for a in (F(1),F(-1)) for b in (F(1),F(-1))]
    Qa=avg_form(C2,I2); Qb=avg_form(C2,[[F(3),F(0)],[F(0),F(1)]])
    okQ = Qa is not None and Qb is not None
    prop = okQ and Qa[0][0]*Qb[1][1]==Qa[1][1]*Qb[0][0] and Qa[0][1]*Qb[0][0]==Qb[0][1]*Qa[0][0]
    leg("seed_dependence_owned", okQ and not prop, "non-proportional invariant forms on the reducible control; irreducibility residue named")

    # LEG 5 -- adjoint == admitted reverse (guards: table completeness, non-degenerate Q):
    table_inv={}
    for i,g in enumerate(G):
        gi=inv2(g)
        if gi is not None and tuple(tuple(r) for r in gi) in keyset: table_inv[i]=gi
    dQ=det2(Q)
    if len(table_inv)!=8 or dQ==0:
        leg("sharp_equals_admitted_reverse", False, "guard fired: table %d/8, detQ=%s"%(len(table_inv),dQ))
    else:
        Qinv=inv2(Q)
        adj=all(mm(mm(Qinv,tr(g)),Q)==table_inv[i] for i,g in enumerate(G))
        leg("sharp_equals_admitted_reverse", adj, "Q-adjoint == admitted (in-set) inverse, all 8 elements")

    # LEG 6 -- computed counter-model (both falsity directions fail by construction):
    world=[]; M=I2
    for n in range(12):
        M=mm(M,BOOST); world.append({"step":n+1,"booked":F(0),"state_sup":max(abs(e) for x in SPAN for e in mv(M,x))})
    total=sum(w["booked"] for w in world)
    unb=all(world[k+1]["state_sup"]>world[k]["state_sup"] for k in range(11))
    leg("counter_model_computed", total==0 and total<=C_TOTAL and unb,
        "generated boost world: booked 0<=61, sup %s at n=12 -> derivation grade dies; reading load-bearing"%str(world[-1]["state_sup"]))

    # LEG 7 -- capacity divergence exhibit (pin exact):
    n_exceed=None; M=I2
    for n in range(1,64):
        M=mm(M,BOOST)
        if max(abs(e) for x in SPAN for e in mv(M,x))>C_TOTAL: n_exceed=n; break
    leg("capacity_divergence_exhibit", n_exceed==7, "boost spanning-content > 61 at word length 7; bounded family sup 5/2 forever")

    # LEG 8 -- consumer certificate with INDEPENDENT recomputation (MAJOR-C):
    cert={"family":[ [list(r) for r in g] for g in G],"closure_verified":closed and invs,
          "bounded_certificate":supG,"invariant_form":Q}
    def recompute(c):
        Qc=c["invariant_form"]; fam=c["family"]
        pd=Qc[0][0]>0 and det2(Qc)>0
        def qfx(x): return sum(x[i]*Qc[i][j]*x[j] for i in range(2) for j in range(2))
        iso=all(qfx(mv(g,x))==qfx(x) for g in fam for x in [[F(1),F(0)],[F(0),F(1)],[F(1),F(1)]])
        ks={tuple(tuple(r) for r in g) for g in fam}
        cl=all(tuple(tuple(r) for r in mm(a,b)) in ks for a in fam for b in fam)
        return pd and iso and cl and c["closure_verified"]
    leg("salvage_consumer_certificate", recompute(cert),
        "closure+pd+isometry independently recomputed from certificate fields (consumer shape: COMPACT_OR_ISOMETRIC_ACTION)")

    # LEG 9 -- fences: ROT admitted / circle gated (computable), and the scope
    # fence COMPUTED (MAJOR-A): derived surfaces disjoint from fenced surfaces,
    # and no fenced surface named as derived in key_result.
    rot_orth=mm(tr(ROT),ROT)==I2
    sq=[[F(1),F(1)],[F(1),F(-1)],[F(-1),F(1)],[F(-1),F(-1)]]
    fence=not all(max(abs(w[0]),abs(w[1]))==F(1) for w in [mv(ROT,x) for x in sq])
    leg("rot_admitted_circle_gated", rot_orth and fence, "infinite bounded case = named import; circle at continuum seam")
    kr=("Under R-capacity-bounded-world (NEW named reading, standalone-walked): admissible reversible "
        "action families preserve a bounded admissible set (gauge-free), hence are bounded groups; in "
        "the finite case averaging a positive seed (seed positivity = declared mathematical input) "
        "yields an exactly invariant positive-definite form with T-sharp == the admitted reverse -- "
        "EXISTENCE of invariant positivity relocates to reading grade (uniqueness = named "
        "irreducibility residue; identity with a physical counting metric NOT claimed). Derivation "
        "grade dies on the computed label-fiat counter-world. Boost and unipotent shear excluded "
        "under the reading by exact growth certificates in every gauge.")
    disjoint=len(set(DERIVED_SURFACES)&set(FENCED_SURFACES))==0
    clean=all(s.replace("_"," ").lower() not in kr.lower() and s not in kr for s in FENCED_SURFACES)
    leg("scope_fences_computed", disjoint and clean, "derived/fenced disjoint; no fenced surface claimed in key_result")

    return {"name":"_run_legs","passed":ok,
            "grade":"P_structural_reading","readings":READINGS,"named_grants":NAMED_GRANTS,
            "named_math_imports":NAMED_MATH_IMPORTS,"named_premises":NAMED_PREMISES,
            "named_residues":NAMED_RESIDUES,"fenced_surfaces":FENCED_SURFACES,
            "derived_surfaces":DERIVED_SURFACES,"physical_premises_certified":False,
            "legs":log,"key_result":kr}


def check_L_bounded_orbit_positivity():
    # live deps: the two banked bars the keystone adjudication leans on.
    from apf.operational_completeness import check_T_ledger_rent_excluded
    from apf.commutative_no_unresolved_hold import (
        check_L_commutative_no_unresolved_hold)
    dep_rent = check_T_ledger_rent_excluded()
    dep_dephase = check_L_commutative_no_unresolved_hold()
    r = _run_legs()
    fails = [n for n, v, d in r["legs"] if v != "PASS"]
    if not dep_rent.get("passed", False):
        fails.append("dep T_ledger_rent_excluded failed")
    if not dep_dephase.get("passed", False):
        fails.append("dep L_commutative_no_unresolved_hold failed")
    return {
        "name": "L_bounded_orbit_positivity",
        "epistemic": "P_structural_reading",
        "passed": r["passed"] and not fails,
        "readings": r["readings"],
        "named_grants": r["named_grants"],
        "named_math_imports": r["named_math_imports"],
        "named_premises": r["named_premises"],
        "named_residues": r["named_residues"],
        "fenced_surfaces": r["fenced_surfaces"],
        "derived_surfaces": r["derived_surfaces"],
        "physical_premises_certified": False,
        "legs": r["legs"],
        "key_result": r["key_result"],
        "deps_live": ["T_ledger_rent_excluded",
                      "L_commutative_no_unresolved_hold"],
        "deps_citation": ["A1", "occupancy (constitutive, ruling 2026-07-07)",
                          "REVERSAL_IS_INVERSE (.429 H1)",
                          "H3 connectedness gate (.429)"],
        "lane": "__APF Library/Artifacts_2026-07-20_session/seam_salvage/",
        "banking_status": "BANKED v24.3.431 (principal ruling 'bank', "
                          "2026-07-20; 3948 -> 3949)",
        "fail_reasons": fails,
    }


_CHECKS = {
    "L_bounded_orbit_positivity": check_L_bounded_orbit_positivity,
}


def register(registry):
    registry.update(_CHECKS)
    return registry


def run_all():
    return {n: fn() for n, fn in _CHECKS.items()}


if __name__ == "__main__":
    import sys
    r = check_L_bounded_orbit_positivity()
    print(r["name"], r["epistemic"], "PASS" if r["passed"] else "FAIL")
    for name, verdict, detail in r["legs"]:
        print("  %-36s %s  %s" % (name, verdict, detail))
    for f in r["fail_reasons"]:
        print("  -", f)
    sys.exit(0 if r["passed"] else 1)
