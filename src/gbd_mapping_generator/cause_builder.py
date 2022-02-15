"""Tools for automatically generating the GBD cause mapping."""
from .base_template_builder import gbd_record_attrs, modelable_entity_attrs
from .data import get_cause_data, get_cause_list
from .globals import ID_TYPES
from .util import (
    SPACING,
    TAB,
    TEXTWIDTH,
    make_import,
    make_module_docstring,
    make_record,
    text_wrap,
    to_id,
)

IMPORTABLES_DEFINED = ("Cause", "causes")


def get_base_types():
    cause_attrs = [
        ("name", "str"),
        ("kind", "str"),
        ("gbd_id", ID_TYPES.C_ID),
        ("me_id", f"Union[{ID_TYPES.ME_ID}, Unknown]"),
        ("most_detailed", "bool"),
        ("level", "int"),
        ("restrictions", "Restrictions"),
    ]
    cause_attrs += [
        ("parent", '"Cause" = None'),
        ("sub_causes", 'Tuple["Cause", ...] = None'),
        ("sequelae", "Tuple[Sequela, ...] = None"),
        ("etiologies", "Tuple[Etiology, ...] = None"),
    ]

    return {
        "Cause": {
            "attrs": tuple(cause_attrs),
            "superclass": ("ModelableEntity", modelable_entity_attrs),
            "docstring": "Container for cause GBD ids and metadata",
        },
        "Causes": {
            "attrs": tuple([(name, "Cause") for name in get_cause_list()]),
            "superclass": ("GbdRecord", gbd_record_attrs),
            "docstring": "Container for GBD causes.",
        },
    }


def make_cause(
    name, c_id, me_id, most_detailed, level, restrictions, sequelae=None, etiologies=None
):
    out = ""
    out += TAB + f"'{name}': Cause(\n"
    out += TAB * 2 + f"name='{name}',\n"
    out += TAB * 2 + f"kind='cause',\n"
    out += TAB * 2 + f"gbd_id={ID_TYPES.C_ID}({c_id}),\n"
    out += TAB * 2 + f"me_id={to_id(me_id, ID_TYPES.ME_ID)},\n"
    out += TAB * 2 + f"level={level},\n"
    out += TAB * 2 + f"most_detailed={bool(most_detailed)},\n"
    out += TAB * 2 + f"parent=None,\n"
    out += TAB * 2 + f"restrictions=Restrictions(\n"

    for restriction, value in restrictions:
        out += TAB * 3 + f"{restriction}={value},\n"
    out += TAB * 2 + "),\n"

    for entity_name, entity in zip(["sequelae", "etiologies"], [sequelae, etiologies]):
        field = 2 * TAB + f"{entity_name}=("
        offset = len(field)

        out += field
        if entity:
            char_count = offset
            for item in entity:
                if entity_name == "sub_causes":
                    item_name = f"causes.{item}, "
                else:
                    item_name = f"{entity_name}.{item}, "

                if char_count == offset:
                    out += item_name
                    char_count += len(item_name)
                elif char_count + len(item_name) > TEXTWIDTH:
                    out += "\n" + " " * offset + item_name
                    char_count = offset + len(item_name)
                else:
                    out += item_name
                    char_count += len(item_name)
        out += "),\n"

    out += TAB + "),\n"
    return out


def make_causes(causes_list):
    out = f"causes = Causes(**{{\n"
    for (
        name,
        c_id,
        me_id,
        most_detailed,
        cause_level,
        parent,
        restrictions,
        sequelae,
        etiologies,
        sub_causes,
    ) in causes_list:
        out += make_cause(
            name, c_id, me_id, most_detailed, cause_level, restrictions, sequelae, etiologies
        )
    out += "})\n\n"

    for (
        name,
        c_id,
        me_id,
        most_detailed,
        cause_level,
        parent,
        restrictions,
        sequelae,
        etiologies,
        sub_causes,
    ) in causes_list:

        if name != parent:
            out += f"causes.{name}.parent = causes.{parent}\n"
        if sub_causes:
            if name in sub_causes:
                sub_causes.remove(name)
            out += text_wrap(
                f"causes.{name}.sub_causes = (", [f"causes.{s}" for s in sub_causes] + [")"]
            )
        out += "\n"

    return out


def build_mapping_template():
    out = make_module_docstring("Mapping templates for GBD causes.", __file__)
    out += make_import("typing", ("Union", "Tuple")) + "\n"
    out += make_import(".id", (ID_TYPES.C_ID, ID_TYPES.ME_ID, "Unknown"))
    out += make_import(".base_template", ("Restrictions", "ModelableEntity", "GbdRecord"))
    out += make_import(".sequela_template", ("Sequela",))
    out += make_import(".etiology_template", ("Etiology",))

    for entity, info in get_base_types().items():
        out += SPACING
        out += make_record(entity, **info)
    return out


def build_mapping():
    out = make_module_docstring("Mapping of GBD causes.", __file__)
    out += make_import(".id", (ID_TYPES.C_ID, ID_TYPES.ME_ID, "UNKNOWN"))
    out += make_import(".base_template", ("Restrictions",))
    out += make_import(".cause_template", ("Cause", "Causes"))
    out += make_import(".sequela", ("sequelae",))
    out += make_import(".etiology", ("etiologies",)) + SPACING
    out += make_causes(get_cause_data())
    return out
