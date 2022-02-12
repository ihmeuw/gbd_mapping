from typing import List

from .base_template_builder import gbd_record_attrs, modelable_entity_attrs
from .data import get_sequela_data, get_sequela_list
from .globals import ID_TYPES
from .util import SPACING, TAB, make_import, make_module_docstring, make_record, to_id

IMPORTABLES_DEFINED = ("Sequela", "Healthstate", "sequelae")


def get_base_types():
    sequela_attrs = [
        ("name", "str"),
        ("kind", "str"),
        ("gbd_id", ID_TYPES.S_ID),
        ("me_id", ID_TYPES.ME_ID),
    ]
    sequela_attrs += [
        ("healthstate", "Healthstate"),
    ]
    return {
        "Healthstate": {
            "attrs": (
                ("name", "str"),
                ("kind", "str"),
                ("gbd_id", ID_TYPES.HS_ID),
            ),
            "superclass": ("ModelableEntity", modelable_entity_attrs),
            "docstring": "Container for healthstate GBD ids and metadata.",
        },
        "Sequela": {
            "attrs": tuple(sequela_attrs),
            "superclass": ("ModelableEntity", modelable_entity_attrs),
            "docstring": "Container for sequela GBD ids and metadata.",
        },
        "Sequelae": {
            "attrs": tuple([(name, "Sequela") for name in get_sequela_list()]),
            "superclass": ("GbdRecord", gbd_record_attrs),
            "docstring": "Container for GBD sequelae.",
        },
    }


def make_sequela(name: str, s_id: float, mei_id: float, hs_name: str, hs_id: float) -> str:
    hs_name = "UNKNOWN" if hs_name == "nan" else f"'{hs_name}'"
    out = ""
    out += TAB + f"'{name}': Sequela(\n"
    out += TAB * 2 + f"name='{name}',\n"
    out += TAB * 2 + f"kind='sequela',\n"
    out += TAB * 2 + f"gbd_id={to_id(s_id, ID_TYPES.S_ID)},\n"
    out += TAB * 2 + f"me_id={to_id(mei_id, ID_TYPES.ME_ID)},\n"
    out += TAB * 2 + f"healthstate=Healthstate(\n"

    out += TAB * 3 + f"name={hs_name},\n"
    out += TAB * 3 + f"kind='healthstate',\n"
    out += TAB * 3 + f"gbd_id={to_id(hs_id, ID_TYPES.HS_ID)},\n"
    out += TAB * 2 + f"),\n"
    out += TAB + f"),\n"
    return out


def make_sequelae(sequela_list: List[str]) -> str:
    out = "sequelae = Sequelae(**{\n"
    for (name, sid, mei_id, hs_name, hsid) in sequela_list:
        out += make_sequela(name, sid, mei_id, hs_name, hsid)
    out += "})\n"
    return out


def build_mapping_template() -> str:
    out = make_module_docstring("Mapping templates for GBD sequelae.", __file__)
    out += make_import(".id", (ID_TYPES.S_ID, ID_TYPES.ME_ID, ID_TYPES.HS_ID))
    out += make_import(".base_template", ("ModelableEntity", "GbdRecord"))

    for entity, info in get_base_types().items():
        out += SPACING
        out += make_record(entity, **info)
    return out


def build_mapping() -> str:
    out = make_module_docstring("Mapping of GBD sequelae.", __file__)
    out += make_import(".id", (ID_TYPES.S_ID, ID_TYPES.HS_ID, ID_TYPES.ME_ID))
    out += make_import(".sequela_template", ("Healthstate", "Sequela", "Sequelae")) + SPACING
    out += make_sequelae(get_sequela_data())
    return out
