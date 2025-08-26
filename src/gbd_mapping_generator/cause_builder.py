"""Tools for automatically generating the GBD cause mapping."""
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from .base_template_builder import gbd_record_attrs, modelable_entity_attrs
from .data import get_cause_data, get_cause_list
from .globals import ID_TYPES
from .util import to_id

IMPORTABLES_DEFINED = ("Cause", "causes")

# Initialize Jinja2 environment
TEMPLATE_DIR = Path(__file__).parent / "templates"
jinja_env = Environment(loader=FileSystemLoader(TEMPLATE_DIR), trim_blocks=True, lstrip_blocks=True)


def get_base_types():
    cause_attrs = [
        ("name", "str"),
        ("kind", "str"),
        ("gbd_id", ID_TYPES.C_ID),
        ("me_id", f"{ID_TYPES.ME_ID} | Unknown"),
        ("most_detailed", "bool"),
        ("level", "int"),
        ("restrictions", "Restrictions"),
    ]
    cause_attrs += [
        ("parent", "Cause | None = None"),
        ("sub_causes", "tuple[Cause, ...] | None = None"),
        ("sequelae", "tuple[Sequela, ...] | None = None"),
        ("etiologies", "tuple[Etiology, ...] | None = None"),
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


class CauseData:
    """Helper class to format cause data for Jinja2 templates."""
    
    def __init__(self, name, c_id, me_id, most_detailed, level, parent, restrictions, 
                 sequelae=None, etiologies=None, sub_causes=None):
        self.name = name
        self.c_id = c_id
        self.me_id_formatted = to_id(me_id, ID_TYPES.ME_ID)
        self.most_detailed = bool(most_detailed)
        self.level = level
        self.parent = parent
        self.restrictions = restrictions
        self.sequelae = sequelae or []
        self.etiologies = etiologies or []
        self.sub_causes = [sc for sc in (sub_causes or []) if sc != name]


def prepare_causes_data():
    """Transform raw cause data into template-friendly format."""
    raw_data = get_cause_data()
    causes_data = []
    
    for (name, c_id, me_id, most_detailed, cause_level, parent, 
         restrictions, sequelae, etiologies, sub_causes) in raw_data:
        
        cause_data = CauseData(
            name=name,
            c_id=c_id,
            me_id=me_id,
            most_detailed=most_detailed,
            level=cause_level,
            parent=parent,
            restrictions=restrictions,
            sequelae=sequelae,
            etiologies=etiologies,
            sub_causes=sub_causes
        )
        causes_data.append(cause_data)
    
    return causes_data


def build_mapping_template():
    """Generate cause_template.py using Jinja2."""
    template = jinja_env.get_template("cause_template.py.j2")
    base_types = get_base_types()
    
    context = {
        "cause_attrs": base_types["Cause"]["attrs"],
        "cause_names": [name for name, _ in base_types["Causes"]["attrs"]],
        "c_id_type": ID_TYPES.C_ID,
        "me_id_type": ID_TYPES.ME_ID,
    }
    
    return template.render(**context)


def build_mapping():
    """Generate cause.py using Jinja2."""
    template = jinja_env.get_template("cause.py.j2")
    causes_data = prepare_causes_data()
    
    context = {
        "causes_data": causes_data,
        "c_id_type": ID_TYPES.C_ID,
        "me_id_type": ID_TYPES.ME_ID,
    }
    
    return template.render(**context)
