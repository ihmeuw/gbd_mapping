from .data import get_etiology_data, get_etiology_list
from .base_template_builder import modelable_entity_attrs, gbd_record_attrs
from .util import make_import, make_module_docstring, make_record, SPACING, TAB

IMPORTABLES_DEFINED = ('Etiology', 'etiologies')


def get_base_types(with_survey):
    etiology_attrs = [('name', 'str'),
                      ('kind', 'str'),
                      ('gbd_id', 'Union[reiid, None]')]
    if with_survey:
        etiology_attrs += [('population_attributable_fraction_yll_exists', 'bool'),
                           ('population_attributable_fraction_yld_exists', 'bool'),
                           ('population_attributable_fraction_yll_in_range', 'bool'),
                           ('population_attributable_fraction_yld_in_range', 'bool'),]

    return {
        'Etiology': {
            'attrs': tuple(etiology_attrs),
            'superclass': ('ModelableEntity', modelable_entity_attrs),
            'docstring': 'Container for etiology GBD ids and metadata.'
        },
        'Etiologies': {
            'attrs': tuple([(name, 'Etiology') for name in get_etiology_list()]),
            'superclass': ('GbdRecord', gbd_record_attrs),
            'docstring': 'Container for GBD etiologies.',
        },
    }


def make_etiology(name, reiid, yll_exist, yld_exist, yll_in_range, yld_in_range, with_survey):
    out = ""
    out += TAB + f"{name}=Etiology(\n"
    out += TAB*2 + f"name='{name}',\n"
    out += TAB * 2 + f"kind='etiology',\n"
    out += TAB*2 + f"gbd_id=reiid({reiid}),\n"
    if with_survey:
        out += TAB * 2 + f"population_attributable_fraction_yll_exists={yll_exist},\n"
        out += TAB * 2 + f"population_attributable_fraction_yld_exists={yld_exist},\n"
        out += TAB * 2 + f"population_attributable_fraction_yll_in_range={yll_in_range},\n"
        out += TAB * 2 + f"population_attributable_fraction_yld_in_range={yld_in_range},\n"
    out += TAB + "),\n"
    return out


def make_etiologies(etiology_list, with_survey):
    out = "etiologies = Etiologies(\n"
    for name, reiid, yll_exist, yld_exist, yll_in_range, yld_in_range in etiology_list:
        out += make_etiology(name, reiid, yll_exist, yld_exist, yll_in_range, yld_in_range, with_survey)
    out += ")\n"
    return out


def build_mapping_template(with_survey):
    out = make_module_docstring('Mapping templates for GBD etiologies.', __file__)
    out += make_import('typing', ['Union']) + '\n'
    out += make_import('.id', ['reiid'])
    out += make_import('.base_template', ['ModelableEntity', 'GbdRecord'])

    for entity, info in get_base_types(with_survey).items():
        out += SPACING
        out += make_record(entity, **info)
    return out


def build_mapping(with_survey):
    out = make_module_docstring('Mapping of GBD etiologies.', __file__)
    out += make_import('.id', ['reiid'])
    out += make_import('.etiology_template', ['Etiology', 'Etiologies']) + SPACING
    out += make_etiologies(get_etiology_data(with_survey), with_survey)
    return out
