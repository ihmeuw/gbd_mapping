from .data import get_covariate_data, get_covariate_list
from .base_template_builder import modelable_entity_attrs, gbd_record_attrs
from .util import make_import, make_module_docstring, make_record, text_wrap, SPACING, TAB

IMPORTABLES_DEFINED = ('Covariate', 'covariates')


def get_base_types():
    return {
        'Covariate': {
            'attrs': (('name', 'str'),
                      ('kind', 'str'),
                      ('gbd_id', 'Union[covid, None]'),
                      ('by_age', 'bool'),
                      ('by_sex', 'bool'),
                      ('dichotomous', 'bool'),
                      ('mean_value_exists', 'Union[bool, None]'),
                      ('uncertainty_exists', 'Union[bool, None]'),
                      ('by_age_violated', 'bool'),
                      ('by_sex_violated', 'bool')),
            'superclass': ('ModelableEntity', modelable_entity_attrs),
            'docstring': 'Container for covariate GBD ids and metadata.'
        },
        'Covariates': {
            'attrs': tuple([(name, 'Covariate') for name in get_covariate_list()]),
            'superclass': ('GbdRecord', gbd_record_attrs),
            'docstring': 'Container for GBD covariates.',
        },
    }


def make_covariate(name, covid, by_age, by_sex, dichotomous, mean_value_exists, uncertainty_exists,
                   by_age_violated, by_sex_violated):
    out = ""
    out += TAB + f"'{name}': Covariate(\n"
    out += TAB * 2 + f"name='{name}',\n"
    out += TAB * 2 + "kind='covariate',\n"
    out += TAB * 2 + f"gbd_id=covid({covid}),\n"
    out += TAB * 2 + f"by_age={bool(by_age)},\n"
    out += TAB * 2 + f"by_sex={bool(by_sex)},\n"
    out += TAB * 2 + f"dichotomous={bool(dichotomous)},\n"
    out += TAB * 2 + f"mean_value_exists={mean_value_exists},\n"
    out += TAB * 2 + f"uncertainty_exists={uncertainty_exists},\n"
    out += TAB * 2 + f"by_age_violated={by_age_violated},\n"
    out += TAB * 2 + f"by_sex_violated={by_sex_violated},\n"
    out += TAB + "),\n"

    return out


def make_covariates(covariate_list):
    out = "covariates = Covariates(**{\n"
    for name, covid, by_age, by_sex, dichotomous, mean_value_exists, uncertainty_exists, by_age_violated, by_sex_violated in covariate_list:
        out += make_covariate(name, covid, by_age, by_sex, dichotomous, mean_value_exists, uncertainty_exists,
                              by_age_violated, by_sex_violated)
    out += "})\n"
    return out


def build_mapping_template():
    out = make_module_docstring('Mapping templates for GBD covariates.', __file__)
    out += make_import('typing', ['Union']) + '\n'
    out += make_import('.id', ['covid'])
    out += make_import('.base_template', ['ModelableEntity', 'GbdRecord'])

    for entity, info in get_base_types().items():
        out += SPACING
        out += make_record(entity, **info)
    return out


def build_mapping():
    out = make_module_docstring('Mapping of GBD covariates.', __file__)
    out += make_import('.id', ['covid'])
    out += make_import('.covariate_template', ['Covariate', 'Covariates']) + SPACING
    out += make_covariates(get_covariate_data())
    return out
