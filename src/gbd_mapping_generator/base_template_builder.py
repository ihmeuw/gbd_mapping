from .util import make_module_docstring, make_import, make_record, SPACING

IMPORTABLES_DEFINED = ('GbdRecord', 'ModelableEntity', 'Restrictions', 'Tmred', 'Levels', 'ExposureParameters')


gbd_record_attrs = ()
modelable_entity_attrs = (('name', 'str'),
                          ('kind', 'str'),
                          ('gbd_id', 'Union[cid, sid, hsid, meid, covid, reiid, None]'),)
restrictions_attrs = (('male_only', 'bool'),
                      ('female_only', 'bool'),
                      ('yll_only', 'bool'),
                      ('yld_only', 'bool'),
                      ('yll_age_start', 'scalar = None'),
                      ('yll_age_end', 'scalar = None'),
                      ('yld_age_start', 'scalar = None'),
                      ('yld_age_end', 'scalar = None'),)
tmred_attrs = (('distribution', 'str'),
               ('min', 'scalar'),
               ('max', 'scalar'),
               ('inverted', 'bool'),)
levels_attrs = tuple([('cat1', 'str'), ('cat2', 'str')] + [(f'cat{i}', 'str = None') for i in range(3, 60)])
exposure_parameters_attrs = (('scale', 'scalar = None'),
                             ('max_rr', 'scalar = None'),)


base_types = {
    'GbdRecord': {
        'attrs': gbd_record_attrs,
        'superclass': (None, ()),
        'docstring': 'Base class for entities modeled in the GBD.',
    },
    'ModelableEntity': {
        'attrs': modelable_entity_attrs,
        'superclass': ('GbdRecord', gbd_record_attrs),
        'docstring': 'Container for general GBD ids and metadata.',
    },
    'Restrictions': {
        'attrs': restrictions_attrs,
        'superclass': ('GbdRecord', gbd_record_attrs),
        'docstring': 'Container for information about sub-populations the entity describes.',
    },
    'Tmred': {
        'attrs': tmred_attrs,
        'superclass': ('GbdRecord', gbd_record_attrs),
        'docstring': 'Container for theoretical minimum risk exposure distribution data.'
    },
    'Levels': {
        'attrs': levels_attrs,
        'superclass': ('GbdRecord', gbd_record_attrs),
        'docstring': 'Container for categorical risk exposure levels.'
    },
    'ExposureParameters': {
        'attrs': exposure_parameters_attrs,
        'superclass': ('GbdRecord', gbd_record_attrs),
        'docstring': 'Container for continuous risk exposure distribution parameters'
    },
}


def make_gbd_record():
    out = '''class GbdRecord:
    """Base class for entities modeled in the GBD."""
    __slots__ = ()
    
    def to_dict(self):
        out = {}
        for item in self.__slots__:
            attr = getattr(self, item)
            if isinstance(attr, GbdRecord):
                out[item] = attr.to_dict()
            elif isinstance(attr, Tuple):
                if isinstance(attr[0], GbdRecord):
                    out[item] = tuple(r.to_dict() for r in attr)
            else:
                out[item] = attr
        return out        

    def __contains__(self, item):
        return item in self.__slots__

    def __getitem__(self, item):
        if item in self:
            return getattr(self, item)
        else:
            raise KeyError(item)

    def __iter__(self):
        for item in self.__slots__:
            yield getattr(self, item)

    def __repr__(self):
        out = f'{self.__class__.__name__}('
        for i, slot in enumerate(self.__slots__):
            attr = self[slot]
            if i != 0:
                out += ','
            out += f'\\n{slot}='
            if isinstance(attr, tuple):
                out += '['+','.join([entity.name for entity in attr]) + ']'
            else:
                out += repr(attr)
        return out + ')'
'''
    return out


def build_mapping():
    templates = make_module_docstring('Template classes for GBD entities', __file__)
    templates += make_import('typing', ['Union', 'Tuple',])
    templates += make_import('.id', ['cid', 'sid', 'hsid', 'meid', 'covid', 'reiid', 'scalar', ]) + SPACING
    templates += make_gbd_record()

    for entity, info in base_types.items():
        if entity == 'GbdRecord':
            continue
        templates += SPACING
        templates += make_record(entity, **info)

    return templates
