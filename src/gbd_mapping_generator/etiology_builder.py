from .base_template_builder import gbd_record_attrs, modelable_entity_attrs
from .data import get_etiology_data, get_etiology_list
from .globals import ID_TYPES
from .util import (
    DOUBLE_SPACING,
    SINGLE_SPACING,
    TAB,
    make_import,
    make_module_docstring,
    make_record,
)

IMPORTABLES_DEFINED = ("Etiology", "etiologies")


def get_base_types():
    etiology_attrs = [
        ("name", "str"),
        ("kind", "str"),
        ("gbd_id", f"{ID_TYPES.REI_ID} | None"),
    ]

    return {
        "Etiology": {
            "attrs": tuple(etiology_attrs),
            "superclass": ("ModelableEntity", modelable_entity_attrs),
            "docstring": "Container for etiology GBD ids and metadata.",
        },
        "Etiologies": {
            "attrs": tuple([(name, "Etiology") for name in get_etiology_list()]),
            "superclass": ("GbdRecord", gbd_record_attrs),
            "docstring": "Container for GBD etiologies.",
        },
    }


def make_etiology(name: str, rei_id: float) -> str:
    out = ""
    out += TAB + f"{name}=Etiology(\n"
    out += TAB * 2 + f"name='{name}',\n"
    out += TAB * 2 + f"kind='etiology',\n"
    out += TAB * 2 + f"gbd_id={ID_TYPES.REI_ID}({rei_id}),\n"
    out += TAB + "),\n"
    return out


def make_etiologies(etiology_list: list[tuple[str, float]]) -> str:
    out = "etiologies = Etiologies(\n"
    for name, rei_id in etiology_list:
        out += make_etiology(name, rei_id)
    out += ")\n"
    return out


def build_mapping_template() -> str:
    out = make_module_docstring("Mapping templates for GBD etiologies.", __file__)
    out += make_import(".base_template", ("GbdRecord", "ModelableEntity"))
    out += make_import(".id", (ID_TYPES.REI_ID,))

    for entity, info in get_base_types().items():
        out += DOUBLE_SPACING
        out += make_record(entity, **info)
    return out


def build_mapping() -> str:
    out = make_module_docstring("Mapping of GBD etiologies.", __file__)
    out += make_import(".etiology_template", ("Etiologies", "Etiology"))
    out += make_import(".id", (ID_TYPES.REI_ID,)) + SINGLE_SPACING
    out += make_etiologies(get_etiology_data())
    return out
