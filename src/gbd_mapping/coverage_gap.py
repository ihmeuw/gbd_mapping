"""Mapping of coverage gaps.

This code is automatically generated by gbd_mapping_generator/coverage_gap_builder.py

Any manual changes will be lost.
"""
from .id import reiid
from .base_template import Levels, Restrictions
from .coverage_gap_template import CoverageGap, CoverageGaps
from .cause import causes
from .risk import risk_factors


coverage_gaps = CoverageGaps(
    lack_of_vitamin_a_fortification=CoverageGap(
        name='lack_of_vitamin_a_fortification',
        kind='coverage_gap',
        gbd_id=None,
        distribution='dichotomous',
        restrictions=Restrictions(
            female_only=False,
            male_only=False,
            yld_only=False,
            yll_only=False,
        ),
        levels=Levels(
            cat1='exposed',
            cat2='unexposed',
        ),
        affected_causes=(),
        affected_risk_factors=(risk_factors.vitamin_a_deficiency, ),
    ),
)
