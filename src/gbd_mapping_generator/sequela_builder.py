from .data import get_sequela_list, get_sequela_data
from .base_template_builder import modelable_entity_attrs, gbd_record_attrs
from .util import make_import, make_module_docstring, make_record, to_id, SPACING, TAB

IMPORTABLES_DEFINED = ('Sequela', 'Healthstate', 'sequelae')


base_types = {
    'Healthstate': {
        'attrs': (('name', 'str'),
                  ('kind', 'str'),
                  ('gbd_id', 'hsid'),),
        'superclass': ('ModelableEntity', modelable_entity_attrs),
        'docstring': 'Container for healthstate GBD ids and metadata.',
    },
    'Sequela': {
        'attrs': (('name', 'str'),
                  ('kind', 'str'),
                  ('gbd_id', 'sid'),
                  ('dismod_id', 'meid'),
                  ('healthstate', 'Healthstate'),),
        'superclass': ('ModelableEntity', modelable_entity_attrs),
        'docstring': 'Container for sequela GBD ids and metadata.'
    },
    'Sequelae': {
        'attrs': tuple([(name, 'Sequela') for name in get_sequela_list()]),
        'superclass': ('GbdRecord', gbd_record_attrs),
        'docstring': 'Container for GBD sequelae.',
    },
}


def make_sequela(name, sid, mei_id, hs_name, hsid):
    hs_name = 'UNKNOWN' if hs_name == 'nan' else f"'{hs_name}'"
    out = ""
    out += TAB + f"'{name}': Sequela(\n"
    out += TAB*2 + f"name='{name}',\n"
    out += TAB * 2 + f"kind='sequela',\n"
    out += TAB*2 + f"gbd_id={to_id(sid, 'sid')},\n"
    out += TAB*2 + f"dismod_id={to_id(mei_id, 'meid')},\n"
    out += TAB*2 + f"healthstate=Healthstate(\n"

    out += TAB*3 + f"name={hs_name},\n"
    out += TAB*3 + f"kind='healthstate',\n"
    out += TAB*3 + f"gbd_id={to_id(hsid, 'hsid')},\n"
    out += TAB*2 + f"),\n"
    out += TAB + f"),\n"
    return out


def make_sequelae(sequela_list):
    out = "sequelae = Sequelae(**{\n"
    for name, sid, mei_id, hs_name, hsid in sequela_list:
        out += make_sequela(name, sid, mei_id, hs_name, hsid)
    out += "})\n"
    return out


def build_mapping_template():
    out = make_module_docstring('Mapping templates for GBD sequelae.', __file__)
    out += make_import('.id', ['sid', 'meid', 'hsid'])
    out += make_import('.base_template', ['ModelableEntity', 'GbdRecord'])

    for entity, info in base_types.items():
        out += SPACING
        out += make_record(entity, **info)
    return out


def build_mapping():
    out = make_module_docstring('Mapping of GBD sequelae.', __file__)
    out += make_import('.id', ['sid', 'hsid', 'meid'])
    out += make_import('.sequela_template', ['Healthstate', 'Sequela', 'Sequelae']) + SPACING
    out += make_sequelae(get_sequela_data())
    return out
