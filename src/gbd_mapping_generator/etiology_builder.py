from .data import get_etiology_data, get_etiology_list
from .base_template_builder import modelable_entity_attrs, gbd_record_attrs
from .util import make_import, make_module_docstring, make_record, SPACING, TAB

IMPORTABLES_DEFINED = ('Etiology', 'etiologies')


def get_base_types():
    return {
        'Etiology': {
            'attrs': (('name', 'str'),
                      ('kind', 'str'),
                      ('gbd_id', 'Union[reiid, None]'),
                      ('paf_yll_exist', 'bool'),
                      ('paf_yll_min', 'float'),
                      ('paf_yll_max', 'float'),
                      ('paf_yld_exist', 'bool'),
                      ('paf_yld_min', 'float'),
                      ('paf_yld_max', 'float'),),
            'superclass': ('ModelableEntity', modelable_entity_attrs),
            'docstring': 'Container for etiology GBD ids and metadata.'
        },
        'Etiologies': {
            'attrs': tuple([(name, 'Etiology') for name in get_etiology_list()]),
            'superclass': ('GbdRecord', gbd_record_attrs),
            'docstring': 'Container for GBD etiologies.',
        },
    }


def make_etiology(name, reiid, yll_exist, yll_min, yll_max, yld_exist, yld_min, yld_max):
    out = ""
    out += TAB + f"{name}=Etiology(\n"
    out += TAB*2 + f"name='{name}',\n"
    out += TAB * 2 + f"kind='etiology',\n"
    out += TAB*2 + f"gbd_id=reiid({reiid}),\n"
    out += TAB * 2 + f"paf_yll_exist={yll_exist},\n"
    out += TAB * 2 + f"paf_yll_min={yll_min},\n"
    out += TAB * 2 + f"paf_yll_max={yll_max},\n"
    out += TAB * 2 + f"paf_yld_exist={yld_exist},\n"
    out += TAB * 2 + f"paf_yld_min={yld_min},\n"
    out += TAB * 2 + f"paf_yld_max={yld_max},\n"
    out += TAB + "),\n"
    return out


def make_etiologies(etiology_list):
    out = "etiologies = Etiologies(\n"
    for name, reiid, yll_exist, yll_min, yll_max, yld_exist, yld_min, yld_max in etiology_list:
        out += make_etiology(name, reiid, yll_exist, yll_min, yll_max, yld_exist, yld_min, yld_max)
    out += ")\n"
    return out


def build_mapping_template():
    out = make_module_docstring('Mapping templates for GBD etiologies.', __file__)
    out += make_import('typing', ['Union']) + '\n'
    out += make_import('.id', ['reiid'])
    out += make_import('.base_template', ['ModelableEntity', 'GbdRecord'])

    for entity, info in get_base_types().items():
        out += SPACING
        out += make_record(entity, **info)
    return out


def build_mapping():
    out = make_module_docstring('Mapping of GBD etiologies.', __file__)
    out += make_import('.id', ['reiid'])
    out += make_import('.etiology_template', ['Etiology', 'Etiologies']) + SPACING
    out += make_etiologies(get_etiology_data())
    return out
