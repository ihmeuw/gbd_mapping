from .base_template_builder import gbd_record_attrs, modelable_entity_attrs
from .data import get_covariate_data, get_covariate_list
from .globals import ID_TYPES, CovariateDataSeq
from .util import SPACING, TAB, make_import, make_module_docstring, make_record

IMPORTABLES_DEFINED = ("Covariate", "covariates")


def get_base_types():
    cov_attrs = [
        ("name", "str"),
        ("kind", "str"),
        ("gbd_id", f"Union[{ID_TYPES.COV_ID}, None]"),
        ("by_age", "bool"),
        ("by_sex", "bool"),
        ("dichotomous", "bool"),
    ]

    return {
        "Covariate": {
            "attrs": tuple(cov_attrs),
            "superclass": ("ModelableEntity", modelable_entity_attrs),
            "docstring": "Container for covariate GBD ids and metadata.",
        },
        "Covariates": {
            "attrs": tuple([(name, "Covariate") for name in get_covariate_list()]),
            "superclass": ("GbdRecord", gbd_record_attrs),
            "docstring": "Container for GBD covariates.",
        },
    }


def make_covariate(
    name: str, cov_id: float, by_age: bool, by_sex: bool, dichotomous: bool
) -> str:
    """Creates a single Covariate based on the supplied parameters.

    Parameters
    ----------
    name
        Covariate name.
    cov_id
        The numeric id for the covariate.
    by_age
        Adjusted by age
    by_sex
        Adjusted by sex
    dichotomous
        Is dichotomous

    Returns
    -------
    str
        Generated string for a single covariate.

    """
    out = ""
    out += TAB + f"'{name}': Covariate(\n"
    out += TAB * 2 + f"name='{name}',\n"
    out += TAB * 2 + "kind='covariate',\n"
    out += TAB * 2 + f"gbd_id={ID_TYPES.COV_ID}({cov_id}),\n"
    out += TAB * 2 + f"by_age={bool(by_age)},\n"
    out += TAB * 2 + f"by_sex={bool(by_sex)},\n"
    out += TAB * 2 + f"dichotomous={bool(dichotomous)},\n"
    out += TAB + "),\n"

    return out


def make_covariates(covariate_list: CovariateDataSeq) -> str:
    """Generates the list of covariates.

    Parameters
    ----------
    covariate_list
        Sequence of covariate data from which to generate the representation

    Returns
    -------
    str
        Generated string all covariates.

    """
    out = "covariates = Covariates(**{\n"
    for name, cov_id, by_age, by_sex, dichotomous in covariate_list:
        out += make_covariate(name, cov_id, by_age, by_sex, dichotomous)
    out += "})\n"
    return out


def build_mapping_template():
    out = make_module_docstring("Mapping templates for GBD covariates.", __file__)
    out += make_import("typing", ("Union",)) + "\n"
    out += make_import(".id", (ID_TYPES.COV_ID,))
    out += make_import(".base_template", ("ModelableEntity", "GbdRecord"))

    for entity, info in get_base_types().items():
        out += SPACING
        out += make_record(entity, **info)
    return out


def build_mapping():
    out = make_module_docstring("Mapping of GBD covariates.", __file__)
    out += make_import(".id", (ID_TYPES.COV_ID,))
    out += make_import(".covariate_template", ("Covariate", "Covariates")) + SPACING
    out += make_covariates(get_covariate_data())
    return out
