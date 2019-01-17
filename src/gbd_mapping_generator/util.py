import os
from pathlib import Path

import numpy as np


TEXTWIDTH = 118  # type: int
TAB = '    '  # type: str
SPACING = '\n\n'  # type: str


def make_module_docstring(description, file):
    here = Path(file).resolve()
    out = f'"""{description}\n\n'
    out += f'This code is automatically generated by {Path(*here.parts[-2:])}\n\n'
    out += 'Any manual changes will be lost.\n"""\n'
    return out


def make_import(module_to_import, imports=()):
    if not imports:
        out = f"import {module_to_import}"
    else:
        out = text_wrap(f'from {module_to_import} import ', imports, implicit=True)

    return out


def text_wrap(start_string, items, sep=', ', implicit=False):
    if len(start_string + sep.join(items)) <= TEXTWIDTH:
        out = start_string + sep.join(items) + '\n'
        if implicit:
            out = f"({out})"
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


def clean_entity_list(raw_entity_series):
    replace_with_underscore_chars = ['/', '(', ')', ' – ', ' - ', '-', ' ', ',', '–', '____', '___', '__', '=']
    replace_chars = {char: '_' for char in replace_with_underscore_chars}
    replace_chars.update({"'": '',
                          '’': '',
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
                          'PM2.5': 'pm_2_5'})
    cleaned_up_entities = []
    for entity in list(raw_entity_series):
        entity = str(entity)
        # Clean up the string
        for char, rep_char in replace_chars.items():
            entity = entity.replace(char, rep_char)

        entity = entity.lower().rstrip().rstrip('_')
        cleaned_up_entities.append(entity)
    return cleaned_up_entities


def to_id(number, id_type):
    if np.isnan(number):
        return 'UNKNOWN'
    else:
        return id_type + f'({int(number)})'


def make_class_sig(name, superclass=None, docstring=None):
    out = f'class {name}'
    if superclass[0]:
        out += f'({superclass[0]})'
    out += ':\n'
    if docstring:
        out += TAB + f'"""{docstring}"""\n'
    return out


def make_slots(field_list):
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


def make_init(field_dtype_tuples):
    declaration = TAB + 'def __init__('
    offset = len(declaration)

    out = declaration + 'self,'

    if len(field_dtype_tuples) > 255:
        out += ' ' + '**kwargs):\n'
    else:
        out += '\n'
        for field_name, data_type in field_dtype_tuples:
            out += ' '*offset + field_name + ': ' + data_type + ',\n'
        out = out[:-1] + ' ):\n'
    return out


def make_super_call(superclass):
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


def make_attribute_assignment(field_names):
    offset = 8

    out = ''
    if len(field_names) > 255:
        for field in field_names:
            out += ' '*offset + f"self.{field} = kwargs.get('{field}')\n"
    else:
        for field in field_names:
            out += ' '*offset + f'self.{field} = {field}\n'
    return out


def make_record(name, attrs=None, superclass=None, docstring=None):
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
