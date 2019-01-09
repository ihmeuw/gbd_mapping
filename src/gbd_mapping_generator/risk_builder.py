from .data import get_risk_data, get_risk_list
from .base_template_builder import modelable_entity_attrs, gbd_record_attrs
from .util import make_import, make_module_docstring, make_record, SPACING, TAB, TEXTWIDTH, text_wrap


IMPORTABLES_DEFINED = ('RiskFactor', 'risk_factors')


def get_base_types():
    return {
        'RiskFactor': {
            'attrs': (('name', 'str'),
                      ('kind', 'str'),
                      ('gbd_id', 'reiid'),
                      ('level', 'int'),
                      ('most_detailed', 'bool'),
                      ('distribution', 'str'),
                      ('paf_calculation_type', 'str'),
                      ('restrictions', 'Restrictions'),
                      ("missing_exposure", "Union['bool', 'None']"),
                      ("missing_rr", "Union['bool', 'None']"),
                      ("rr_less_than_1", "Union['bool', 'None']"),
                      ("missing_paf", "Union['bool', 'None']"),
                      ("paf_outside_0_1", "Union['bool', 'None']"),
                      ('affected_causes', 'Tuple[Cause, ...]'),
                      ('paf_of_one_causes', 'Tuple[Cause, ...]'),
                      ('parent', 'Union["RiskFactor", None] = None'),
                      ('sub_risk_factors', 'Tuple["RiskFactor", ...] = None'),
                      ('affected_risk_factors', 'Tuple["RiskFactor", ...] = None'),
                      ('categories', 'Categories = None'),
                      ('tmred', 'Tmred = None'),
                      ('rr_scalar', 'scalar = None')),
            'superclass': ('ModelableEntity', modelable_entity_attrs),
            'docstring': 'Container for risk GBD ids and metadata.'
        },
        'RiskFactors': {
            'attrs': tuple([(name, 'RiskFactor') for name in get_risk_list()]),
            'superclass': ('GbdRecord', gbd_record_attrs),
            'docstring': 'Container for GBD risks.',
        },
    }


def make_risk(name, rei_id, most_detailed, level, paf_calculation_type,
              affected_causes, paf_of_one_causes,
              distribution, levels, tmred, scalar,
              missing_exposure, missing_rr, rr_less_than_1,
              missing_paf, paf_outside_0_1,
              restrictions):
    out = ""
    out += TAB + f"{name}=RiskFactor(\n"
    out += TAB * 2 + f"name='{name}',\n"
    out += TAB * 2 + f"kind='risk_factor',\n"
    out += TAB * 2 + f"gbd_id=reiid({rei_id}),\n"
    out += TAB * 2 + f"level={level},\n"
    out += TAB * 2 + f"most_detailed={bool(most_detailed)},\n"
    out += TAB * 2 + f"distribution='{distribution}',\n"
    out += TAB * 2 + f"paf_calculation_type='{paf_calculation_type}',\n"
    out += TAB * 2 + f"missing_exposure={missing_exposure},\n"
    out += TAB * 2 + f"missing_rr={missing_rr},\n"
    out += TAB * 2 + f"rr_less_than_1={rr_less_than_1},\n"
    out += TAB * 2 + f"missing_paf={missing_paf},\n"
    out += TAB * 2 + f"paf_outside_0_1={paf_outside_0_1},\n"


    out += 2*TAB + "restrictions=Restrictions(\n"
    for name, r in restrictions:
        if name == "violated_restrictions":
            out += text_wrap(f"{TAB * 3 + name}=(", [f"'{v}'" for v in r] + [")"])
        elif r is not None:
            out += 3*TAB + f"{name}={r},\n"
    out += 2 * TAB + '),\n'

    out += make_entity_list('affected_causes', affected_causes, 'cause')
    out += make_entity_list('paf_of_one_causes', paf_of_one_causes, 'cause')

    if levels:
        out += 2*TAB + "categories=Categories(\n"
        for cat, name in levels:
            out += 3*TAB + f"{cat}='{name}',\n"
        out += 2*TAB + '),\n'

    if tmred:
        out += 2*TAB + "tmred=Tmred(\n"
        for name, val in tmred:
            if val is not None:
                if name == 'distribution':
                    val = f"'{val}'"
                elif name in ['min', 'max']:
                    val = f"scalar({val})"
                out += 3*TAB + f"{name}={val},\n"
        out += 2*TAB + '),\n'

    if scalar:
        out += 2*TAB + f'rr_scalar=scalar({scalar}),\n'

    out += TAB + '),\n'
    return out


def make_entity_list(name, entity_list, entity_type):
    field = 2 * TAB + f"{name}=("
    if not entity_list:
        return field + "),\n"
    offset = len(field)

    out = field
    char_count = offset
    for entity in entity_list:
        entity_name = f"{entity_type}s.{entity}, "

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
    return out


def make_risks(risk_list):
    out = "risk_factors = RiskFactors(\n"
    for (name, rei_id, most_detailed, level, paf_calculation_type,
         affected_causes, paf_of_one_causes,
         distribution, levels, tmred, scalar,
         missing_exposure, missing_rr, rr_less_than_1,
         missing_paf, paf_outside_0_1,
         restrictions, *_) in risk_list:
        out += make_risk(name, rei_id, most_detailed, level, paf_calculation_type,
                         affected_causes, paf_of_one_causes,
                         distribution, levels, tmred, scalar,
                         missing_exposure, missing_rr, rr_less_than_1,
                         missing_paf, paf_outside_0_1,
                         restrictions)

    out += ")\n"

    for (name, *_, parent, sub_risks, affected_risks) in risk_list:

        if name != parent:
            out += f"risk_factors.{name}.parent = risk_factors.{parent}\n"
            if sub_risks:
                if name in sub_risks:
                    sub_risks.remove(name)
                out += text_wrap(f'risk_factors.{name}.sub_risk_factors = ',
                                 [f'risk_factors.{s}' for s in sub_risks], implicit=True)
            if affected_risks:
                out += text_wrap(f'risk_factors.{name}.affected_risk_factors = ',
                                 [f'risk_factors.{s}' for s in affected_risks], implicit=True)
            out += '\n'

    return out


def build_mapping_template():
    out = make_module_docstring('Mapping templates for GBD risk factors.', __file__)
    out += make_import('typing', ['Tuple', 'Union']) + '\n'
    out += make_import('.id', ['reiid', 'scalar'])
    out += make_import('.base_template', ['ModelableEntity', 'GbdRecord', 'Categories',
                                          'Tmred', 'Restrictions'])
    out += make_import('.cause_template', ['Cause'])

    for entity, info in get_base_types().items():
        out += SPACING
        out += make_record(entity, **info)
    return out


def build_mapping():
    out = make_module_docstring('Mapping of GBD risk factors.', __file__)
    out += make_import('.id', ['reiid', 'scalar'])
    out += make_import('.base_template', ['Categories', 'Tmred', 'Restrictions'])
    out += make_import('.risk_factor_template', ['RiskFactor', 'RiskFactors'])
    out += make_import('.cause', ['causes']) + SPACING
    out += make_risks(get_risk_data())
    return out
