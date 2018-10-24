from .data import get_covariate_data, get_covariate_list
from .base_template_builder import modelable_entity_attrs, gbd_record_attrs
from .util import make_import, make_module_docstring, make_record, SPACING, TAB

IMPORTABLES_DEFINED = ('Covariate', 'covariates')


base_types = {
    'Covariate': {
        'attrs': (('name', 'str'),
                  ('kind', 'str'),
                  ('gbd_id', 'Union[covid, None]'),
                  ('group', 'str'),
                  ('status', 'str'),
                  ('by_age', 'bool'),
                  ('by_sex', 'bool'),
                  ('dichotomous', 'bool')),
        'superclass': ('ModelableEntity', modelable_entity_attrs),
        'docstring': 'Container for covariate GBD ids and metadata.'
    },
    'Covariates': {
        'attrs': tuple([(name, 'Covariate') for name in get_covariate_list()]),
        'superclass': ('GbdRecord', gbd_record_attrs),
        'docstring': 'Container for GBD covariates.',
    },
}


def make_covariate(name, covid, group, cov_type, by_age, by_sex, dichotomous):
    out = ""
    out += TAB + f"'{name}': Covariate(\n"
    out += TAB*2 + f"name='{name}',\n"
    out += TAB * 2 + "kind='covariate',\n"
    out += TAB*2 + f"gbd_id=covid({covid}),\n"
    out += TAB*2 + f"group='{group}',\n"
    out += TAB*2 + f"status='{cov_type}',\n"
    out += TAB*2 + f"by_age={bool(by_age)},\n"
    out += TAB*2 + f"by_sex={bool(by_sex)},\n"
    out += TAB*2 + f"dichotomous={bool(dichotomous)},\n"
    out += TAB + "),\n"
    return out


def make_covariates(covariate_list):
    out = "covariates = Covariates(**{\n"
    for name, covid, group, cov_type, by_age, by_sex, dichotomous in covariate_list:
        out += make_covariate(name, covid, group, cov_type, by_age, by_sex, dichotomous)
    out += "})\n"
    return out


def build_mapping_template():
    out = make_module_docstring('Mapping templates for GBD covariates.', __file__)
    out += make_import('typing', ['Union']) + '\n'
    out += make_import('.id', ['covid'])
    out += make_import('.base_template', ['ModelableEntity', 'GbdRecord'])

    for entity, info in base_types.items():
        out += SPACING
        out += make_record(entity, **info)
    return out


def build_mapping():
    out = make_module_docstring('Mapping of GBD covariates.', __file__)
    out += make_import('.id', ['covid'])
    out += make_import('.covariate_template', ['Covariate', 'Covariates']) + SPACING
    out += make_covariates(get_covariate_data())
    return out
