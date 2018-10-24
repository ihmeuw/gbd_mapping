"""Tools for automatically generating the GBD cause mapping."""
from .data import get_cause_list, get_cause_data
from .util import make_import, make_module_docstring, make_record, to_id, SPACING, TAB, TEXTWIDTH
from .base_template_builder import gbd_record_attrs, modelable_entity_attrs

IMPORTABLES_DEFINED = ('Cause', 'causes')

base_types = {
    'Cause': {
        'attrs': (('name', 'str'),
                  ('kind', 'str'),
                  ('gbd_id', 'cid'),
                  ('dismod_id', 'Union[meid, _Unknown]'),
                  ('restrictions', 'Restrictions'),
                  ('sequelae', 'Tuple[Sequela, ...] = None'),
                  ('etiologies', 'Tuple[Etiology, ...] = None'),),
        'superclass': ('ModelableEntity', modelable_entity_attrs),
        'docstring': 'Container for cause GBD ids and metadata',
    },
    'Causes': {
        'attrs': tuple([(name, 'Cause') for name in get_cause_list() if name is not 'none']),
        'superclass': ('GbdRecord', gbd_record_attrs),
        'docstring': 'Container for GBD causes.',
    },
}


def make_cause(name, cid, dismod_id, restrictions, sequelae=None, etiologies=None):
    out = ""
    out += TAB + f"'{name}': Cause(\n"
    out += TAB*2 + f"name='{name}',\n"
    out += TAB * 2 + f"kind='cause',\n"
    out += TAB*2 + f"gbd_id=cid({cid}),\n"
    out += TAB*2 + f"dismod_id={to_id(dismod_id, 'meid')},\n"
    out += TAB*2 + f"restrictions=Restrictions(\n"
    for restriction, value in restrictions:
        if isinstance(value, bool):
            out += TAB*3 + f"{restriction}={value},\n"
        else:
            out += TAB * 3 + f"{restriction}=scalar({value}),\n"
    out += TAB*2 + "),\n"

    for entity_name, entity in zip(['sequelae', 'etiologies'], [sequelae, etiologies]):
        if entity:
            field = 2*TAB + f'{entity_name}=('
            offset = len(field)

            out += field
            char_count = offset
            for item in entity:
                item_name = f"{entity_name}.{item}, "

                if char_count == offset:
                    out += item_name
                    char_count += len(item_name)
                elif char_count + len(item_name) > TEXTWIDTH:
                    out += '\n' + ' '*offset + item_name
                    char_count = offset + len(item_name)
                else:
                    out += item_name
                    char_count += len(item_name)
            out += '),\n'

    out += TAB + "),\n"
    return out


def make_causes(causes_list):
    out = "causes = Causes(**{\n"
    for name, cid, dismod_id, restrictions, seq_id, etiol_id in causes_list:
        out += make_cause(name, cid, dismod_id, restrictions, seq_id, etiol_id)
    out += "})\n"
    return out


def build_mapping_template():
    out = make_module_docstring('Mapping templates for GBD causes.', __file__)
    out += make_import('typing', ['Union', 'Tuple']) + '\n'
    out += make_import('.id', ['cid', 'meid', '_Unknown'])
    out += make_import('.base_template', ['Restrictions', 'ModelableEntity', 'GbdRecord'])
    out += make_import('.sequela_template', ['Sequela'])
    out += make_import('.etiology_template', ['Etiology'])

    for entity, info in base_types.items():
        out += SPACING
        out += make_record(entity, **info)
    return out


def build_mapping():
    out = make_module_docstring('Mapping of GBD causes.', __file__)
    out += make_import('.id', ['cid', 'meid', 'UNKNOWN', 'scalar'])
    out += make_import('.base_template', ['Restrictions'])
    out += make_import('.cause_template', ['Cause', 'Causes']) + SPACING
    out += make_import('.sequela', ['sequelae'])
    out += make_import('.etiology', ['etiologies'])
    out += make_causes(get_cause_data())
    return out
