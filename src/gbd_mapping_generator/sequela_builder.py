from .data import get_sequela_list, get_sequela_data
from .base_template_builder import modelable_entity_attrs, gbd_record_attrs
from .util import make_import, make_module_docstring, make_record, to_id, SPACING, TAB

IMPORTABLES_DEFINED = ('Sequela', 'Healthstate', 'sequelae')


def get_base_types(with_survey):
    sequela_attrs = [('name', 'str'),
                      ('kind', 'str'),
                      ('gbd_id', 'sid'),
                      ('dismod_id', 'meid')]
    if with_survey:
        sequela_attrs += [('incidence_exists', 'bool'),
                          ('prevalence_exists', 'bool'),
                          ('birth_prevalence_exists', 'bool'),
                          ('incidence_in_range', 'Union[bool, None]'),
                          ('prevalence_in_range', 'Union[bool, None]'),
                          ('birth_prevalence_in_range', 'Union[bool, None]')]
    sequela_attrs += [('healthstate', 'Healthstate'),]
    return {
        'Healthstate': {
            'attrs': (('name', 'str'),
                      ('kind', 'str'),
                      ('gbd_id', 'hsid'),
                      ('disability_weight_exists', 'bool'),),
            'superclass': ('ModelableEntity', modelable_entity_attrs),
            'docstring': 'Container for healthstate GBD ids and metadata.',
        },
        'Sequela': {
            'attrs': tuple(sequela_attrs),
            'superclass': ('ModelableEntity', modelable_entity_attrs),
            'docstring': 'Container for sequela GBD ids and metadata.'
        },
        'Sequelae': {
            'attrs': tuple([(name, 'Sequela') for name in get_sequela_list()]),
            'superclass': ('GbdRecord', gbd_record_attrs),
            'docstring': 'Container for GBD sequelae.',
        },
    }


def make_sequela(name, sid, mei_id, hs_name, hsid, dw_exists, inc_exists, prev_exists, birth_prev_exists,
                 inc_in_range, prev_in_range, birth_prev_in_range, with_survey):
    hs_name = 'UNKNOWN' if hs_name == 'nan' else f"'{hs_name}'"
    out = ""
    out += TAB + f"'{name}': Sequela(\n"
    out += TAB*2 + f"name='{name}',\n"
    out += TAB * 2 + f"kind='sequela',\n"
    out += TAB*2 + f"gbd_id={to_id(sid, 'sid')},\n"
    out += TAB*2 + f"dismod_id={to_id(mei_id, 'meid')},\n"
    if with_survey:
        out += TAB * 2 + f"incidence_exists={inc_exists},\n"
        out += TAB * 2 + f"prevalence_exists={prev_exists},\n"
        out += TAB * 2 + f"birth_prevalence_exists={birth_prev_exists},\n"
        out += TAB * 2 + f"incidence_in_range={inc_in_range},\n"
        out += TAB * 2 + f"prevalence_in_range={prev_in_range},\n"
        out += TAB * 2 + f"birth_prevalence_in_range={birth_prev_in_range},\n"
    out += TAB*2 + f"healthstate=Healthstate(\n"

    out += TAB*3 + f"name={hs_name},\n"
    out += TAB*3 + f"kind='healthstate',\n"
    out += TAB*3 + f"gbd_id={to_id(hsid, 'hsid')},\n"
    out += TAB * 3 + f"disability_weight_exists={dw_exists},\n"
    out += TAB*2 + f"),\n"
    out += TAB + f"),\n"
    return out


def make_sequelae(sequela_list, with_survey):
    out = "sequelae = Sequelae(**{\n"
    for (name, sid, mei_id, hs_name, hsid, dw_exists, inc_exists, prev_exists,
         birth_prev_exists, inc_in_range, prev_in_range, birth_prev_in_range) in sequela_list:
        out += make_sequela(name, sid, mei_id, hs_name, hsid, dw_exists, inc_exists, prev_exists,
                            birth_prev_exists, inc_in_range, prev_in_range, birth_prev_in_range, with_survey)
    out += "})\n"
    return out


def build_mapping_template(with_survey):
    out = make_module_docstring('Mapping templates for GBD sequelae.', __file__)
    out += make_import('typing', ['Union']) + '\n'
    out += make_import('.id', ['sid', 'meid', 'hsid'])
    out += make_import('.base_template', ['ModelableEntity', 'GbdRecord'])

    for entity, info in get_base_types(with_survey).items():
        out += SPACING
        out += make_record(entity, **info)
    return out


def build_mapping(with_survey):
    out = make_module_docstring('Mapping of GBD sequelae.', __file__)
    out += make_import('.id', ['sid', 'hsid', 'meid'])
    out += make_import('.sequela_template', ['Healthstate', 'Sequela', 'Sequelae']) + SPACING
    out += make_sequelae(get_sequela_data(with_survey), with_survey)
    return out
