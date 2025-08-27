"""Tools for automatically generating the GBD cause mapping."""
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from .data import get_cause_data, get_cause_list
from .globals import ID_TYPES
from .util import to_id

IMPORTABLES_DEFINED = ("Cause", "causes")

# Initialize Jinja2 environment
TEMPLATE_DIR = Path(__file__).parent / "templates"
jinja_env = Environment(loader=FileSystemLoader(TEMPLATE_DIR), trim_blocks=True, lstrip_blocks=True)


class CauseData:
    """Helper class to format cause data for Jinja2 templates."""

    def __init__(self, name: str, c_id: int, me_id: int, most_detailed: int, level: int, parent: str, restrictions: tuple[tuple[str, bool| int], ...],
                 sequelae: list[str] | None = None, etiologies: list[str] | None = None, sub_causes: list[str] | None = None):
        self.name = name
        self.c_id = c_id
        self.me_id_formatted = to_id(me_id, ID_TYPES.ME_ID)
        self.most_detailed = bool(most_detailed)
        self.level = level
        self.parent = parent
        self.restrictions = restrictions
        self.sequelae = sequelae or []
        self.etiologies = [etiology.rstrip(".") for etiology in self.etiologies] if etiologies else []
        self.sub_causes = [sc for sc in (sub_causes or []) if sc != name]


def prepare_causes_data() -> list[CauseData]:
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


def build_mapping_template() -> str:
    """Generate cause_template.py using Jinja2."""
    template = jinja_env.get_template("cause_template.py.j2")
    
    context = {
        "cause_names": get_cause_list(),
        "c_id_type": ID_TYPES.C_ID,
        "me_id_type": ID_TYPES.ME_ID,
    }
    
    return template.render(**context)


def build_mapping() -> str:
    """Generate cause.py using Jinja2."""
    template = jinja_env.get_template("cause.py.j2")
    
    context = {
        "causes_data": prepare_causes_data(),
        "c_id_type": ID_TYPES.C_ID,
        "me_id_type": ID_TYPES.ME_ID,
    }
    
    return template.render(**context)
