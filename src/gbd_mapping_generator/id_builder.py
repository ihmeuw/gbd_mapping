from .globals import ID_TYPES
from .util import SPACING, TAB, make_module_docstring

_ID_TYPES = (
    (ID_TYPES.ME_ID, "Modelable Entity ID"),
    (ID_TYPES.REI_ID, "Risk-Etiology-Impairment ID"),
    (ID_TYPES.C_ID, "Cause ID"),
    (ID_TYPES.S_ID, "Sequela ID"),
    (ID_TYPES.COV_ID, "Covariate ID"),
    (ID_TYPES.HS_ID, "Health State ID"),
)

IMPORTABLES_DEFINED = tuple(
    [id_type[0] for id_type in _ID_TYPES] + ["scalar", "UNKNOWN", "UnknownEntityError"]
)


def make_unknown_flag():
    out = ""
    out += "class Unknown:\n"
    out += TAB + '"""Marker for unknown values."""\n'
    out += TAB + "def __repr__(self):\n"
    out += 2 * TAB + 'return "UNKNOWN"\n' + SPACING
    out += "UNKNOWN = Unknown()\n" + SPACING
    out += "class UnknownEntityError(Exception):\n"
    out += (
        TAB
        + '"""Exception raised when a quantity is requested from vivarium_inputs with an `UNKNOWN` id."""\n'
    )
    out += TAB + "pass\n"
    return out


def build_mapping():
    out = make_module_docstring("Custom ID types for GBD entities", __file__)
    for k, v in _ID_TYPES:
        out += SPACING
        out += f"class {k}(int):\n"
        out += TAB + f'"""{v}"""\n'
        out += TAB + "def __repr__(self):\n"
        out += 2 * TAB + f'return "{k}({{:d}})".format(self)\n'

    out += SPACING
    out += "class scalar(float):\n"
    out += TAB + '"""Raw Measure Value"""\n'
    out += TAB + "def __repr__(self):\n"
    out += 2 * TAB + 'return "scalar({:f})".format(self)\n'
    out += SPACING

    out += make_unknown_flag()

    return out
