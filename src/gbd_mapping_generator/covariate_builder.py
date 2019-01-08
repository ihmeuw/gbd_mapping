from .data import get_covariate_data, get_covariate_list
from .base_template_builder import modelable_entity_attrs, gbd_record_attrs
from .util import make_import, make_module_docstring, make_record, SPACING, TAB

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
                      ('data_exist', 'bool'),
                      ('low_value_exists', 'bool'),
                      ('upper_value_exists', 'bool'),
                      ('mean_value_exists', 'bool'),
                      ('sex_restriction_violated', 'Union[bool, None]'),
                      ('age_restriction_violated', 'Union[bool, None]')),
            'superclass': ('ModelableEntity', modelable_entity_attrs),
            'docstring': 'Container for covariate GBD ids and metadata.'
        },
        'Covariates': {
            'attrs': tuple([(name, 'Covariate') for name in get_covariate_list()]),
            'superclass': ('GbdRecord', gbd_record_attrs),
            'docstring': 'Container for GBD covariates.',
        },
    }


def make_covariate(name, covid, by_age, by_sex, dichotomous, data_exist, low_val_exist,
                   upper_val_exist, mean_exist, sex_restriction, age_restriction):
    out = ""
    out += TAB + f"'{name}': Covariate(\n"
    out += TAB*2 + f"name='{name}',\n"
    out += TAB * 2 + "kind='covariate',\n"
    out += TAB*2 + f"gbd_id=covid({covid}),\n"
    out += TAB*2 + f"by_age={bool(by_age)},\n"
    out += TAB*2 + f"by_sex={bool(by_sex)},\n"
    out += TAB*2 + f"dichotomous={bool(dichotomous)},\n"
    out += TAB * 2 + f"data_exist={data_exist},\n"
    out += TAB * 2 + f"low_value_exists={low_val_exist},\n"
    out += TAB * 2 + f"upper_value_exists={upper_val_exist},\n"
    out += TAB * 2 + f"mean_value_exists={mean_exist},\n"
    out += TAB * 2 + f"sex_restriction_violated={sex_restriction},\n"
    out += TAB * 2 + f"age_restriction_violated={age_restriction},\n"
    out += TAB + "),\n"
    return out


def make_covariates(covariate_list):
    out = "covariates = Covariates(**{\n"
    for name, covid, by_age, by_sex, dichotomous, data_exist, low_val_exist, upper_val_exist, \
        mean_exist, sex_restriction, age_restriction in covariate_list:
        out += make_covariate(name, covid, by_age, by_sex, dichotomous, data_exist, low_val_exist,
                              upper_val_exist, mean_exist, sex_restriction, age_restriction)
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
