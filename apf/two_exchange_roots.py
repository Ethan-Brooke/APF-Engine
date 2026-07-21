"""Root manifest for the two-exchange Held-holonomy front end.

Split from the consuming module ``apf.two_exchange_holonomy`` deliberately
(cold-audit finding m4 / mutation M7): the dependency-contract check compares
the graph-generated root inventory against this manifest, so a coordinated
deletion must now touch two files to pass silently.

``INTERTWINER_REVERSAL_IS_INVERSE`` is the .429 H1-genre gate (cold-audit
MAJOR-1): representing the conjugation loop C X C^{-1} requires that the
reversed intertwiner path be represented by the inverse C^{-1}; reversal
admission alone yields only a monoid.
"""

PHYSICAL_ROOTS = (
    "ADMITTED_SECOND_BINARY_PRESENTATION",
    "CODESPACE_TO_SECOND_PRESENTATION_FIXED_LINE",
    "EFFECTIVE_FIRST_CONTENDER_EXCHANGE",
    "EFFECTIVE_SECOND_CONTENDER_EXCHANGE",
    "EXACT_345_FIXED_LINE_OVERLAP",
    "INTERTWINER_REVERSAL_IS_INVERSE",
    "LATER_RECOMBINATION_WITNESS_FOR_EACH_EXCHANGE",
    "SAME_CARRIER_RETURN",
    "UNIVERSAL_EXCHANGE_NATURALITY_ON_ADMITTED_PRESENTATIONS",
)
