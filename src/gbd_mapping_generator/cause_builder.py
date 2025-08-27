"""Tools for automatically generating the GBD cause mapping."""
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from .data import get_cause_data, get_cause_list
from .globals import ID_TYPES

IMPORTABLES_DEFINED = ("Cause", "causes")

# Initialize Jinja2 environment
TEMPLATE_DIR = Path(__file__).parent / "templates"
jinja_env = Environment(loader=FileSystemLoader(TEMPLATE_DIR), trim_blocks=True, lstrip_blocks=True)


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
        "causes_data": get_cause_data(),
        "c_id_type": ID_TYPES.C_ID,
        "me_id_type": ID_TYPES.ME_ID,
    }
    
    return template.render(**context)
