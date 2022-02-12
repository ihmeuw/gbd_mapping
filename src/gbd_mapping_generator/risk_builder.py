from typing import List

from .base_template_builder import gbd_record_attrs, modelable_entity_attrs
from .data import get_risk_data, get_risk_list
from .globals import ID_TYPES
from .util import (
    SPACING,
    TAB,
    TEXTWIDTH,
    format_string_none,
    make_import,
    make_module_docstring,
    make_record,
    text_wrap,
)

IMPORTABLES_DEFINED = ("RiskFactor", "risk_factors")


def get_base_types():
    risk_attrs = [
        ("name", "str"),
        ("kind", "str"),
        ("gbd_id", ID_TYPES.REI_ID),
        ("level", "int"),
        ("most_detailed", "bool"),
        ("distribution", "Union[str, None]"),
        ("population_attributable_fraction_calculation_type", "str"),
        ("restrictions", "Restrictions"),
    ]

    risk_attrs += [
        ("affected_causes", "Tuple[Cause, ...]"),
        ("population_attributable_fraction_of_one_causes", "Tuple[Cause, ...]"),
        ("parent", 'Union["RiskFactor", None] = None'),
        ("sub_risk_factors", 'Tuple["RiskFactor", ...] = None'),
        ("affected_risk_factors", 'Tuple["RiskFactor", ...] = None'),
        ("categories", "Categories = None"),
        ("tmred", "Tmred = None"),
        ("relative_risk_scalar", "scalar = None"),
    ]
    return {
        "RiskFactor": {
            "attrs": tuple(risk_attrs),
            "superclass": ("ModelableEntity", modelable_entity_attrs),
            "docstring": "Container for risk GBD ids and metadata.",
        },
        "RiskFactors": {
            "attrs": tuple([(name, "RiskFactor") for name in get_risk_list()]),
            "superclass": ("GbdRecord", gbd_record_attrs),
            "docstring": "Container for GBD risks.",
        },
    }


def make_risk(
    name,
    rei_id,
    most_detailed,
    level,
    paf_calculation_type,
    affected_causes,
    paf_of_one_causes,
    distribution,
    levels,
    tmred,
    scalar,
    restrictions,
) -> str:
    out = ""
    out += TAB + f"{name}=RiskFactor(\n"
    out += TAB * 2 + f"name='{name}',\n"
    out += TAB * 2 + f"kind='risk_factor',\n"
    out += TAB * 2 + f"gbd_id={ID_TYPES.REI_ID}({rei_id}),\n"
    out += TAB * 2 + f"level={level},\n"
    out += TAB * 2 + f"most_detailed={bool(most_detailed)},\n"
    out += TAB * 2 + f"distribution={format_string_none(distribution)},\n"
    out += (
        TAB * 2
        + f"population_attributable_fraction_calculation_type='{paf_calculation_type}',\n"
    )
    out += 2 * TAB + "restrictions=Restrictions(\n"
    for name, r in restrictions:
        if r is not None:
            out += 3 * TAB + f"{name}={r},\n"
    out += 2 * TAB + "),\n"

    out += make_entity_list("affected_causes", affected_causes, "cause")
    out += make_entity_list(
        "population_attributable_fraction_of_one_causes", paf_of_one_causes, "cause"
    )

    if levels:
        out += 2 * TAB + "categories=Categories(\n"
        for cat, name in levels:
            out += 3 * TAB + f"{cat}='{name}',\n"
        out += 2 * TAB + "),\n"

    if tmred:
        out += 2 * TAB + "tmred=Tmred(\n"
        for name, val in tmred:
            if val is not None:
                if name == "distribution":
                    val = f"'{val}'"
                elif name in ["min", "max"]:
                    val = f"scalar({val})"
                out += 3 * TAB + f"{name}={val},\n"
        out += 2 * TAB + "),\n"

    if scalar:
        out += 2 * TAB + f"relative_risk_scalar=scalar({scalar}),\n"

    out += TAB + "),\n"
    return out


def make_entity_list(name, entity_list: List, entity_type: str) -> str:
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
            out += "\n" + " " * offset + entity_name
            char_count = offset + len(entity_name)
        else:
            out += entity_name
            char_count += len(entity_name)
    out += "),\n"
    return out


def make_risks(risk_list: List) -> str:
    out = "risk_factors = RiskFactors(\n"
    for (
        name,
        rei_id,
        most_detailed,
        level,
        paf_calculation_type,
        affected_causes,
        paf_of_one_causes,
        distribution,
        levels,
        tmred,
        scalar,
        restrictions,
        *_,
    ) in risk_list:
        out += make_risk(
            name,
            rei_id,
            most_detailed,
            level,
            paf_calculation_type,
            affected_causes,
            paf_of_one_causes,
            distribution,
            levels,
            tmred,
            scalar,
            restrictions,
        )

    out += ")\n"

    for (name, *_, parent, sub_risks, affected_risks) in risk_list:

        if name != parent:
            out += f"risk_factors.{name}.parent = risk_factors.{parent}\n"
            if sub_risks:
                if name in sub_risks:
                    sub_risks.remove(name)
                out += text_wrap(
                    f"risk_factors.{name}.sub_risk_factors = (",
                    [f"risk_factors.{s}" for s in sub_risks] + [")"],
                )
            if affected_risks:
                out += text_wrap(
                    f"risk_factors.{name}.affected_risk_factors = (",
                    [f"risk_factors.{s}" for s in affected_risks] + [")"],
                )
            out += "\n"

    return out


def build_mapping_template():
    out = make_module_docstring("Mapping templates for GBD risk factors.", __file__)
    out += make_import("typing", ("Tuple", "Union")) + "\n"
    out += make_import(".id", (ID_TYPES.REI_ID, "scalar"))
    out += make_import(
        ".base_template",
        ("ModelableEntity", "GbdRecord", "Categories", "Tmred", "Restrictions"),
    )
    out += make_import(".cause_template", ("Cause",))

    for entity, info in get_base_types().items():
        out += SPACING
        out += make_record(entity, **info)
    return out


def build_mapping() -> str:
    out = make_module_docstring("Mapping of GBD risk factors.", __file__)
    out += make_import(".id", (ID_TYPES.REI_ID, "scalar"))
    out += make_import(".base_template", ("Categories", "Tmred", "Restrictions"))
    out += make_import(".risk_factor_template", ("RiskFactor", "RiskFactors"))
    out += make_import(".cause", ("causes",)) + SPACING
    out += make_risks(get_risk_data())
    return out
