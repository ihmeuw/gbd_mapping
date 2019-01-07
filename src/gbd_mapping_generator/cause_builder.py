"""Tools for automatically generating the GBD cause mapping."""
from .data import get_cause_list, get_cause_data
from .util import make_import, make_module_docstring, make_record, to_id, SPACING, TAB, TEXTWIDTH, text_wrap
from .base_template_builder import gbd_record_attrs, modelable_entity_attrs

IMPORTABLES_DEFINED = ('Cause', 'causes')


def get_base_types():
    return {
        'Cause': {
            'attrs': (('name', 'str'),
                      ('kind', 'str'),
                      ('gbd_id', 'cid'),
                      ('dismod_id', 'Union[meid, _Unknown]'),
                      ('most_detailed', 'bool'),
                      ('level', 'int'),
                      ('restrictions', 'Restrictions'),
                      ('prevalence_exists', "Union['bool', 'None']"),
                      ('incidence_exists', "Union['bool', 'None']"),
                      ('remission_exists', "Union['bool', 'None']"),
                      ('death_exists', "Union['bool', 'None']"),
                      ('birth_prevalence_exists', 'bool'),
                      ('prevalence_in_range', "Union['bool', 'None']"),
                      ('incidence_in_range', "Union['bool', 'None']"),
                      ('remission_in_range', "Union['bool', 'None']"),
                      ('death_more_than_population', "Union['bool', 'None']"),
                      ('prevalence_consistent', "Union['bool', 'None']"),
                      ('incidence_consistent', "Union['bool', 'None']"),
                      ('death_consistent', "Union['bool', 'None']"),
                      ('prevalence_aggregated', "Union['bool', 'None']"),
                      ('incidence_aggregated', "Union['bool', 'None']"),
                      ('death_aggregated', "Union['bool', 'None']"),
                      ('parent', '"Cause" = None'),
                      ('sub_causes', 'Tuple["Cause", ...] = None'),
                      ('sequelae', 'Tuple[Sequela, ...] = None'),
                      ('etiologies', 'Tuple[Etiology, ...] = None'),),
            'superclass': ('ModelableEntity', modelable_entity_attrs),
            'docstring': 'Container for cause GBD ids and metadata',
        },
        'Causes': {
            'attrs': tuple([(name, 'Cause') for name in get_cause_list()]),
            'superclass': ('GbdRecord', gbd_record_attrs),
            'docstring': 'Container for GBD causes.',
        },
    }


def make_cause(name, cid, dismod_id, most_detailed, level, restrictions, prev_exist, inc_exist, remission_exist,
               death_exist, birth_prevalence_exist, prev_in_range, inc_in_range, remission_in_range,
               death_more_than_pop, prev_consistent, inc_consistent, death_consistent, prev_aggregated, inc_aggregated,
               death_aggregated, sequelae=None, etiologies=None):
    out = ""
    out += TAB + f"'{name}': Cause(\n"
    out += TAB * 2 + f"name='{name}',\n"
    out += TAB * 2 + f"kind='cause',\n"
    out += TAB * 2 + f"gbd_id=cid({cid}),\n"
    out += TAB * 2 + f"dismod_id={to_id(dismod_id, 'meid')},\n"
    out += TAB * 2 + f"level={level},\n"
    out += TAB * 2 + f"most_detailed={bool(most_detailed)},\n"
    out += TAB * 2 + f"prevalence_exists={prev_exist},\n"
    out += TAB * 2 + f"incidence_exists={inc_exist},\n"
    out += TAB * 2 + f"remission_exists={remission_exist},\n"
    out += TAB * 2 + f"death_exists={death_exist},\n"
    out += TAB * 2 + f"birth_prevalence_exists={birth_prevalence_exist},\n"
    out += TAB * 2 + f"prevalence_in_range={prev_in_range},\n"
    out += TAB * 2 + f"incidence_in_range={inc_in_range},\n"
    out += TAB * 2 + f"remission_in_range={remission_in_range},\n"
    out += TAB * 2 + f"death_more_than_population={death_more_than_pop},\n"
    out += TAB * 2 + f"prevalence_consistent={prev_consistent},\n"
    out += TAB * 2 + f"incidence_consistent={inc_consistent},\n"
    out += TAB * 2 + f"death_consistent={death_consistent},\n"
    out += TAB * 2 + f"prevalence_aggregated={prev_aggregated},\n"
    out += TAB * 2 + f"incidence_aggregated={inc_aggregated},\n"
    out += TAB * 2 + f"death_aggregated={death_aggregated},\n"
    out += TAB * 2 + f"parent=None,\n"
    out += TAB * 2 + f"restrictions=Restrictions(\n"

    for restriction, value in restrictions:
        if restriction == 'violated_restrictions':
            out += text_wrap(f"{TAB * 3 + restriction}=(", [f"'{v}'" for v in value] + [")"])
        else:
            out += TAB * 3 + f"{restriction}={value},\n"
    out += TAB*2 + "),\n"

    for entity_name, entity in zip(['sequelae', 'etiologies'], [sequelae, etiologies]):
        if entity:
            field = 2*TAB + f'{entity_name}=('
            offset = len(field)

            out += field
            char_count = offset
            for item in entity:
                if entity_name == 'sub_causes':
                    item_name = f"causes.{item}, "
                else:
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
    out = f'causes = Causes(**{{\n'
    for (name, cid, dismod_id, most_detailed, cause_level, parent, restrictions, prev_exist, inc_exist, remission_exist,
         death_exist, birth_prevalence_exist, prev_in_range, inc_in_range, remission_in_range, death_more_than_pop,
         prev_consistent, inc_consistent, death_consistent, prev_aggregated,
         inc_aggregated, death_aggregated, sequelae, etiologies, sub_causes) in causes_list:
        out += make_cause(name, cid, dismod_id, most_detailed, cause_level, restrictions, prev_exist, inc_exist,
                          remission_exist, death_exist, birth_prevalence_exist, prev_in_range, inc_in_range,
                          remission_in_range, death_more_than_pop, prev_consistent, inc_consistent, death_consistent,
                          prev_aggregated, inc_aggregated, death_aggregated, sequelae, etiologies)
    out += "})\n\n"

    for (name, cid, dismod_id, most_detailed, cause_level, parent, restrictions,  prev_exist, inc_exist, remission_exist,
         death_exist, birth_prevalence_exist, prev_in_range, inc_in_range, remission_in_range, death_more_than_pop,
         prev_consistent, inc_consistent, death_consistent, prev_aggregated, inc_aggregated, death_aggregated, sequelae,
         etiologies, sub_causes) in causes_list:

        if name != parent:
            out += f"causes.{name}.parent = causes.{parent}\n"
        if sub_causes:
            if name in sub_causes:
                sub_causes.remove(name)
            out += text_wrap(f'causes.{name}.sub_causes = ', [f'causes.{s}' for s in sub_causes], implicit=True)
        out += '\n'

    return out


def build_mapping_template():
    out = make_module_docstring('Mapping templates for GBD causes.', __file__)
    out += make_import('typing', ['Union', 'Tuple', 'List']) + '\n'
    out += make_import('.id', ['cid', 'meid', '_Unknown'])
    out += make_import('.base_template', ['Restrictions', 'ModelableEntity', 'GbdRecord'])
    out += make_import('.sequela_template', ['Sequela'])
    out += make_import('.etiology_template', ['Etiology'])

    for entity, info in get_base_types().items():
        out += SPACING
        out += make_record(entity, **info)
    return out


def build_mapping():
    out = make_module_docstring('Mapping of GBD causes.', __file__)
    out += make_import('.id', ['cid', 'meid', 'UNKNOWN', 'scalar'])
    out += make_import('.base_template', ['Restrictions'])
    out += make_import('.cause_template', ['Cause', 'Causes'])
    out += make_import('.sequela', ['sequelae'])
    out += make_import('.etiology', ['etiologies']) + SPACING
    out += make_causes(get_cause_data())
    return out
