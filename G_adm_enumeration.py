"""
G_adm: The Admissible Interaction Graph of the Standard Model
Complete edge enumeration and matching complex computation.
APF Series — computed 2026-03-04

RESULTS SUMMARY:
  Channels: 61 (45 fermions + 16 bosons)
  K_61 edges (all possible): 1830
  Admissible edges |G_adm|:   626 (34.2% of K_61)
  Forbidden edges:            1204 (65.8% of K_61)

  |M(G_adm)| = 446,863,402,335,236,446,328,320
             = 10^23.6502
             = e^54.4565 nats

  Maximum matching size: 8 pairs (all 16 bosons engaged)
  Maximum matching count: 6,300

ADMISSIBLE EDGES BY TYPE:
  fermion-gluon:    288  (36 colored fermions × 8 gluons)
  Yukawa (f-Higgs): 168  (42 Yukawa-capable fermions × 4 Higgs)
  fermion-W:         72  (24 SU(2) doublets × 3 W bosons)
  fermion-B:         45  (45 fermions, all Y≠0, × 1 B boson)
  gluon-gluon:       28  (C(8,2))
  gauge-Higgs:       16  (4 EW bosons × 4 Higgs)
  Higgs-self:         6  (C(4,2))
  W-W:                3  (C(3,2))
  TOTAL:            626

MATCHING COMPLEX M(G_adm) BY SIZE k (active pairs):
  k= 0:  408,948,226,678,235,438,196,226  (91.515%)
  k= 1:   36,784,255,965,664,162,510,982  ( 8.232%)
  k= 2:    1,116,340,435,916,285,215,978  ( 0.250%)
  k= 3:       14,493,531,270,030,520,770  ( 0.003%)
  k= 4:           85,500,753,850,842,954
  k= 5:              223,162,685,968,530
  k= 6:                  233,920,903,230
  k= 7:                       72,163,350
  k= 8:                            6,300
  TOTAL: 446,863,402,335,236,446,328,320

ENTROPY HIERARCHY:
  ln M(G_adm)         =  54.457 nats  (actual bulk configs)
  61 × ln(42)         = 227.998 nats  (unconstrained vacuum)
  61 × ln(102) = S_dS = 282.123 nats  (de Sitter horizon)
  Gap: gauge cost     = 173.541 nats  (cost of admissibility)
  Gap: interaction pot=  54.125 nats  (S_dS - 61×ln42)
"""

# The matching complex was computed using:
# - Occupation-number DP for bipartite (fermion-boson) matchings
# - Explicit enumeration of EW+Higgs boson-boson matchings (536 total)
# - Exact gluon-gluon matching polynomial from K_8
# - Independence of gluon and EW sectors

MATCHING_COMPLEX_TOTAL = 446_863_402_335_236_446_328_320
MATCHING_COMPLEX_BY_SIZE = {
    0: 408_948_226_678_235_438_196_226,
    1:  36_784_255_965_664_162_510_982,
    2:   1_116_340_435_916_285_215_978,
    3:      14_493_531_270_030_520_770,
    4:          85_500_753_850_842_954,
    5:             223_162_685_968_530,
    6:                 233_920_903_230,
    7:                      72_163_350,
    8:                           6_300,
}

GADM_EDGES = 626
GADM_EDGES_BY_TYPE = {
    'fermion-gluon': 288,
    'Yukawa': 168,
    'fermion-W': 72,
    'fermion-B': 45,
    'gluon-gluon': 28,
    'gauge-Higgs': 16,
    'Higgs-self': 6,
    'W-W': 3,
}

MAX_SIMULTANEOUS_PAIRS = 8   # all 16 bosons engaged
MAX_MATCHING_COUNT = 6_300
COMPLEX_DIMENSION = 7        # (max_pairs - 1)
EFFECTIVE_CHOICES_PER_BOSON = 30.07  # M^(1/16)
