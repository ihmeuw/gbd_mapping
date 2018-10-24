from numbers import Number

import numpy as np

from .data import get_risk_data, get_risk_list
from .base_template_builder import modelable_entity_attrs, gbd_record_attrs
from .util import make_import, make_module_docstring, make_record, SPACING, TAB, TEXTWIDTH


IMPORTABLES_DEFINED = ('Risk', 'risk_factors')


base_types = {
    'Risk': {
        'attrs': (('name', 'str'),
                  ('kind', 'str'),
                  ('gbd_id', 'reiid'),
                  ('distribution', 'str'),
                  ('affected_causes', 'Tuple[Cause, ...]'),
                  ('restrictions', 'Restrictions'),
                  ('levels', 'Levels = None'),
                  ('tmred', 'Tmred = None'),
                  ('exposure_parameters', 'ExposureParameters = None'),),
        'superclass': ('ModelableEntity', modelable_entity_attrs),
        'docstring': 'Container for risk GBD ids and metadata.'
    },
    'Risks': {
        'attrs': tuple([(name, 'Risk') for name in get_risk_list()]),
        'superclass': ('GbdRecord', gbd_record_attrs),
        'docstring': 'Container for GBD risks.',
    },
}


def make_risk(name, reiid, distribution, restrictions, cause_list,
                     levels=None, tmred=None, exposure_parameters=None):
    out = ""
    out += TAB + f"{name}=Risk(\n"
    out += 2*TAB + f"name='{name}',\n"
    out += TAB * 2 + f"kind='risk_factor',\n"
    out += 2*TAB + f"gbd_id=reiid({reiid}),\n"
    distribution = "UNKNOWN" if distribution == 'unknown' else f"'{distribution}'"
    out += 2*TAB + f"distribution={distribution},\n"

    for field_class_name, field in zip(['Restrictions', 'Levels', 'Tmred', 'ExposureParameters'],
                                       [restrictions, levels, tmred, exposure_parameters]):
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

    field = 2*TAB + "affected_causes=("
    offset = len(field)

    out += field
    char_count = offset
    for cause in cause_list:
        cause_name = f"causes.{cause}, "

        if char_count == offset:
            out += cause_name
            char_count += len(cause_name)
        elif char_count + len(cause_name) > TEXTWIDTH:
            out += '\n' + ' ' * offset + cause_name
            char_count = offset + len(cause_name)
        else:
            out += cause_name
            char_count += len(cause_name)
    out += '),\n'

    out += TAB + '),\n'
    return out


def make_risks(riskfactor_data):
    out = "risk_factors = Risks(\n"
    for name, reiid, distribution, restrictions, cause_list, levels, tmred, exposure_parameters in riskfactor_data:
        out += make_risk(name, reiid, distribution, restrictions, cause_list,
                                levels, tmred, exposure_parameters)
    out += ")\n"
    return out


def build_mapping_template():
    out = make_module_docstring('Mapping templates for GBD etiologies.', __file__)
    out += make_import('typing', ['Tuple']) + '\n'
    out += make_import('.id', ['reiid'])
    out += make_import('.base_template', ['ModelableEntity', 'GbdRecord', 'Levels',
                                          'Tmred', 'ExposureParameters', 'Restrictions'])
    out += make_import('.cause_template', ['Cause'])

    for entity, info in base_types.items():
        out += SPACING
        out += make_record(entity, **info)
    return out


def build_mapping():
    out = make_module_docstring('Mapping of GBD etiologies.', __file__)
    out += make_import('.id', ['reiid', 'meid', 'scalar', 'UNKNOWN'])
    out += make_import('.base_template', ['Levels', 'Tmred', 'ExposureParameters', 'Restrictions'])
    out += make_import('.risk_template', ['Risk', 'Risks'])
    out += make_import('.cause', ['causes']) + SPACING
    out += make_risks(get_risk_data())
    return out
