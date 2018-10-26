from numbers import Number

import numpy as np

from .data import get_coverage_gap_list, get_coverage_gap_data
from .base_template_builder import gbd_record_attrs
from .util import make_import, make_module_docstring, make_record, SPACING, TAB, TEXTWIDTH


IMPORTABLES_DEFINED = ('CoverageGap', 'coverage_gaps')


base_types = {
    'CoverageGap': {
        'attrs': (('name', 'str'),
                  ('kind', 'str'),
                  ('gbd_id', 'Union[reiid, None]'),
                  ('restrictions', 'Restrictions'),
                  ('distribution', 'str'),
                  ('levels', 'Levels'),
                  ('affected_causes', 'Tuple[Cause, ...] = None'),
                  ('affected_risk_factors', 'Tuple[Risk, ...] = None'),),
        'superclass': ('GbdRecord', gbd_record_attrs),
        'docstring': 'Container for coverage gap GBD ids and metadata.'
    },
    'CoverageGaps': {
        'attrs': tuple([(name, 'CoverageGap') for name in get_coverage_gap_list()]),
        'superclass': ('GbdRecord', gbd_record_attrs),
        'docstring': 'Container for coverage gap data.',
    },
}


def make_coverage_gap(name, gbd_id, distribution, restrictions, levels=None, affected_causes=None, affected_risk_factors=None):
    out = ""
    out += TAB + f"{name}=CoverageGap(\n"
    out += 2*TAB + f"name='{name}',\n"
    out += TAB * 2 + "kind='coverage_gap',\n"
    if gbd_id:
        out += 2 * TAB + f"gbd_id=reiid({gbd_id}),\n"
    else:
        out += 2 * TAB + f"gbd_id=None,\n"
    out += 2*TAB + f"distribution='{distribution}',\n"

    for field_class_name, field in zip(['Restrictions', 'Levels', ],  # 'Tmred', 'ExposureParameters'],
                                       [restrictions, levels, ]):  # tmred, exposure_parameters]):
        field_name = 'exposure_parameters' if field_class_name == 'ExposureParameters' else field_class_name.lower()
        if field and not isinstance(field, str):
            out += 2*TAB + f"{field_name}={field_class_name}(\n"
            for subfield_name, subfield in field:
                if isinstance(subfield, str):
                    out += 3*TAB + f"{subfield_name}='{subfield}',\n"
                elif isinstance(subfield, bool) or not isinstance(subfield, Number):
                    out += 3 * TAB + f"{subfield_name}={subfield},\n"
                elif np.isnan(subfield):
                    out += 3 * TAB + f"{subfield_name}=UNKNOWN,\n"
                else:
                    if subfield_name == 'dismod_id':
                        out += 3 * TAB + f"{subfield_name}=meid({subfield}),\n"
                    else:
                        out += 3 * TAB + f"{subfield_name}=scalar({subfield}),\n"
            out += 2*TAB + '),\n'
        elif field:
            out += 2*TAB + f"{field_name}={field},\n"

    for entity_type, entity_list in zip(['causes', 'risk_factors'], [affected_causes, affected_risk_factors]):
        field = 2 * TAB + f"affected_{entity_type}=("
        offset = len(field)

        out += field
        char_count = offset
        if entity_list:
            for entity in entity_list:
                entity_name = f"{entity_type}.{entity}, "
                if char_count == offset:
                    out += entity_name
                    char_count += len(entity_name)
                elif char_count + len(entity_name) > TEXTWIDTH:
                    out += '\n' + ' ' * offset + entity_name
                    char_count = offset + len(entity_name)
                else:
                    out += entity_name
                    char_count += len(entity_name)
        out += '),\n'

    out += TAB + '),\n'
    return out


def make_coverage_gaps(coverage_gap_data):
    out = "coverage_gaps = CoverageGaps(\n"
    for name, gbd_id, distribution, restrictions, levels, affected_causes, affected_risk_factors in coverage_gap_data:
        out += make_coverage_gap(name, gbd_id, distribution, restrictions, levels, affected_causes, affected_risk_factors)
    out += ")\n"
    return out


def build_mapping_template():
    out = make_module_docstring('Mapping templates for coverage gap data.', __file__)
    out += make_import('typing', ['Tuple', 'Union']) + '\n'
    out += make_import('.id', ['reiid'])
    out += make_import('.base_template', ['GbdRecord', 'Levels', 'Restrictions'])
    out += make_import('.cause_template', ['Cause'])
    out += make_import('.risk_template', ['Risk'])

    for entity, info in base_types.items():
        out += SPACING
        out += make_record(entity, **info)
    return out


def build_mapping():
    out = make_module_docstring('Mapping of coverage gaps.', __file__)
    out += make_import('.id', ['reiid'])
    out += make_import('.base_template', ['Levels', 'Restrictions'])
    out += make_import('.coverage_gap_template', ['CoverageGap', 'CoverageGaps'])
    out += make_import('.cause', ['causes'])
    out += make_import('.risk', ['risk_factors']) + SPACING
    out += make_coverage_gaps(get_coverage_gap_data())
    return out
