import os
import re
from pathlib import Path

from typing import Union, Tuple, List, Dict, Any

import numpy as np
import pandas as pd


TEXTWIDTH = 118  # type: int
TAB = '    '  # type: str
SPACING = '\n\n'  # type: str

# In Python 3.7 and newer, there is no limit. This limit applies to positional and keyword arguments.
MAX_PYTHON_3_6_ARG_COUNT = 255 # type: int


def make_module_docstring(description: str, file: Union[str, Path]) -> str:
    """Generates standard header with additional information from the description.

    Parameters
    ----------
    description
        Custom header text for the generated file.
    file
        Path to python module that generates the target module.

    Returns
    -------
    str
        String representation of module doc string.

    """
    here = Path(file).resolve()
    out = f'"""{description}\n\n'
    out += f'This code is automatically generated by {Path(*here.parts[-2:])}\n\n'
    out += 'Any manual changes will be lost.\n"""\n'
    return out


def make_import(module_to_import: str, imports: Tuple[str, ...] = ()) -> str:
    """Generates the necessary imports. Smart about importing modules or names.

    Parameters
    ----------
    module_to_import
        Name of the module.
    imports
        Named items to import. If empty import the module name.

    Returns
    -------
    str
        Generated string for necessary imports.

    """
    if not imports:
        out = f"import {module_to_import}"
    else:
        out = text_wrap(f'from {module_to_import} import ', imports, implicit=True)

    return out


def text_wrap(start_string, items, sep=', ', implicit=False):
    if len(start_string + sep.join(items)) <= TEXTWIDTH:
        out = start_string + sep.join(items) + '\n'
    else:
        out = start_string
        if implicit:
            out += '('

        char_count = len(out)
        padding = ' ' * char_count

        out += items[0] + ', '
        char_count += len(items[0]) + 2

        for i in items[1:]:
            if char_count + len(i) > TEXTWIDTH:  # wrap
                out = out[:-1] + '\n'
                out += padding + i + ', '
                char_count = len(padding + i + ', ')
            else:
                out += i + ', '
                char_count += len(i) + 2

        out = out[:-2]
        if implicit:
            out += ')'
        out += '\n'

    return out


def replace_numeric_prefix(name: str) -> str:
    """Variables cannot start with numeric characters. Replace with the word.
    This only occurs 3 times using GBD 2019 data.

    Parameters
    ----------
    name
        The name of the member variable.

    Returns
    -------
    str
        Input string transformed to non-numeric prefix.

    """
    number_sub_map = {
        '2': 'two',
        '4': 'four',
        '12': 'twelve'
    }
    m = re.search('^[0-9]+', name)
    if m:
        name = f'{number_sub_map[m.group()]}_{name[m.span()[1]:]}'
    return name


def clean_entity_list(raw_entity_series) -> List[str]:
    replace_with_underscore_chars = ['/', '(', ')', ' – ', ' - ', '-', ' ', ',', '–', '____', '___', '__', '=']
    replace_chars = {char: '_' for char in replace_with_underscore_chars}
    replace_chars.update({"'": '',
                          '’': '',
                          '[': '',
                          ']': '',
                          '^': '',
                          'é': 'e',
                          '<': 'less_than_',
                          '>': 'greater_than_',
                          '+': '_and_up',
                          'I$': 'income',
                          '%': '_percent',
                          '90th': 'ninetieth',
                          '*': 'x',
                          ':': '',
                          ';': '',
                          '#': '',
                          '&': 'and',
                          '10_year': 'ten_year',
                          'year.': 'year',
                          'PM_2.5': 'pm_2_5',
                          'PM2.5': 'pm_2_5'})
    cleaned_up_entities = []
    for entity in list(raw_entity_series):
        entity = str(entity)
        # Clean up the string
        for char, rep_char in replace_chars.items():
            entity = entity.replace(char, rep_char)

        entity = replace_numeric_prefix(entity)
        entity = entity.lower().rstrip().rstrip('_')
        cleaned_up_entities.append(entity)
    return cleaned_up_entities


def to_id(number: float, id_type: str) -> str:
    """Wrap the id value with the id type. Be mindful of NaN values.

    Parameters
    ----------
    number
        The id value.
    id_type
        The id type.

    Returns
    -------
    str
        String with the id type wrapping the value in parentheses.

    """
    if np.isnan(number):
        return 'UNKNOWN'
    else:
        return id_type + f'({int(number)})'


def make_class_sig(name, superclass=None, docstring=None) -> str:
    """Generate class signature from a name and additional information.

    Parameters
    ----------
    name
        Name of the generated class.
    superclass
        Parent class.
    docstring
        Documentation for the generated class.

    Returns
    -------
    str
        String representation of named class.

    """
    out = f'class {name}'
    if superclass[0]:
        out += f'({superclass[0]})'
    out += ':\n'
    if docstring:
        out += TAB + f'"""{docstring}"""\n'
    return out


def make_slots(field_list: List[str]) -> str:
    """Generate explicit object attributes using slots (instead of dict).

    Parameters
    ----------
    field_list
        Names for the slot attributes.

    Returns
    -------
    str
        String representation of slot attributes.

    """
    declaration = TAB + '__slots__ = ('
    offset = len(declaration)

    out = declaration
    char_count = offset

    for field in field_list:
        field = f"'{field}', "
        field_width = len(field)
        if char_count == offset:
            out += field
            char_count += field_width
        elif char_count + field_width > TEXTWIDTH:
            out = out[:-1] + '\n' + ' '*offset + field
            char_count = offset + field_width
        else:
            out += field
            char_count += field_width

    out += ')\n\n'

    return out


def make_init(field_dtype_tuples: Tuple[Tuple[str, str], ...]) -> str:
    """Generate the __init__ function as part of class generation.

    Parameters
    ----------
    field_dtype_tuples
        Collection of name / value pairs that are used to create the
        the __init__ function with the specified parameters. Parameters
        are type hinted.

    Returns
    -------
    str
        String representation of the __init__ function.

    """
    declaration = TAB + 'def __init__('
    offset = len(declaration)

    out = declaration + 'self,'

    if len(field_dtype_tuples) > MAX_PYTHON_3_6_ARG_COUNT:
        out += ' ' + '**kwargs):\n'
    else:
        out += '\n'
        for field_name, data_type in field_dtype_tuples:
            out += ' '*offset + field_name + ': ' + data_type + ',\n'
        out = out[:-1] + ' ):\n'
    return out


def make_super_call(superclass: Tuple[str, Tuple[Tuple[str, str], ...]]) -> str:
    """Generate the call to initialize the parent class.

    Parameters
    ----------
    superclass
        Nested tuples composed of name and attributes for the superclass.

    Returns
    -------
    str
        String representation of the call to the superclass.

    """
    field_names = [attr[0] for attr in superclass[1]]
    declaration = 2*TAB + 'super().__init__('
    if not field_names:
        return declaration + ')\n'

    offset = len(declaration)
    out = declaration
    for field in field_names:
        out += f'{field}={field},\n'
        out += ' '*offset

    out = out[:-offset-2] + ')\n'
    return out


def make_attribute_assignment(field_names: List[str]) -> str:
    """Generate the class attributes and initialize them.

    Parameters
    ----------
    field_names
        List of class attribute names.

    Returns
    -------
    str
        String representation of the initialized attributes.

    """
    offset = 8

    out = ''
    if len(field_names) > MAX_PYTHON_3_6_ARG_COUNT:
        for field in field_names:
            out += ' '*offset + f"self.{field} = kwargs.get('{field}')\n"
    else:
        for field in field_names:
            out += ' '*offset + f'self.{field} = {field}\n'
    return out


def make_record(name: str,
                attrs: Tuple[Tuple[str, str], ...] = None,
                superclass: Tuple[str, Tuple[Tuple[str, str], ...]] = None,
                docstring: str = None):
    """Generate class definitions from a name and additional information.

    Parameters
    ----------
    name
        Name of the generated class.
    attrs
        Class attributes.
    superclass
        Parent class.
    docstring
        Documentation for the generated class.

    Returns
    -------
    str
        String representation of named class.

    """
    out = ''
    out += make_class_sig(name, superclass, docstring)
    out += make_slots([attr[0] for attr in attrs])
    out += make_init(attrs)
    if superclass:
        out += make_super_call(superclass)
    out += make_attribute_assignment([attr[0] for attr in attrs])
    return out


def get_default_output_directory():
    here = os.path.realpath(__file__)
    return os.path.realpath(os.path.dirname(here) + '/../ceam_inputs/gbd_mapping/')


def format_string_none(value):
    if value is None:
        return None
    else:
        return f"'{value}'"


def make_empty_survey(flags, index):
    return pd.DataFrame(dict(zip(flags, [None]*len(flags))), index=index)
