from .util import TAB, SPACING, make_module_docstring

ID_TYPES = (('meid', 'Modelable Entity ID'),
            ('reiid', 'Risk-Etiology-Impairment ID'),
            ('cid', 'Cause ID'),
            ('sid', 'Sequela ID'),
            ('covid', 'Covariate ID'),
            ('hsid', 'Health State ID'))

IMPORTABLES_DEFINED = tuple([id_type[0] for id_type in ID_TYPES] + ['scalar', 'UNKNOWN', 'UnknownEntityError'])


def make_unknown_flag():
    out = ''
    out += 'class _Unknown:\n'
    out += TAB + '"""Marker for unknown values."""\n'
    out += TAB + 'def __repr__(self):\n'
    out += 2*TAB + 'return "UNKNOWN"\n' + SPACING
    out += 'UNKNOWN = _Unknown()\n' + SPACING
    out += 'class UnknownEntityError(Exception):\n'
    out += TAB + '"""Exception raised when a quantity is requested from ceam_inputs with an `UNKNOWN` id."""\n'
    out += TAB + 'pass\n'
    return out


def build_mapping():
    out = make_module_docstring('Custom ID types for GBD entities', __file__)
    for k, v in ID_TYPES:
        out += SPACING
        out += f'class {k}(int):\n'
        out += TAB + f'"""{v}"""\n'
        out += TAB + 'def __repr__(self):\n'
        out += 2*TAB + f'return "{k}({{:d}})".format(self)\n'

    out += SPACING
    out += 'class scalar(float):\n'
    out += TAB + '"""Raw Measure Value"""\n'
    out += TAB + 'def __repr__(self):\n'
    out += 2 * TAB + 'return "scalar({:f})".format(self)\n'
    out += SPACING

    out += make_unknown_flag()

    return out
