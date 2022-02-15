from .util import SPACING, make_import, make_module_docstring, make_record

IMPORTABLES_DEFINED = ("GbdRecord", "ModelableEntity", "Restrictions", "Tmred", "Categories")


gbd_record_attrs = ()
modelable_entity_attrs = (
    ("name", "str"),
    ("kind", "str"),
    ("gbd_id", "Union[c_id, s_id, hs_id, me_id, cov_id, rei_id, None]"),
)
restrictions_attrs = (
    ("male_only", "bool"),
    ("female_only", "bool"),
    ("yll_only", "bool"),
    ("yld_only", "bool"),
    ("yll_age_group_id_start", "int = None"),
    ("yll_age_group_id_end", "int = None"),
    ("yld_age_group_id_start", "int = None"),
    ("yld_age_group_id_end", "int = None"),
)
tmred_attrs = (
    ("distribution", "str"),
    ("inverted", "bool"),
    ("min", "scalar = None"),
    ("max", "scalar = None"),
)
categories_attrs = tuple([(f"cat{i}", "str = None") for i in range(1, 150)])


def get_base_types():
    return {
        "ModelableEntity": {
            "attrs": modelable_entity_attrs,
            "superclass": ("GbdRecord", gbd_record_attrs),
            "docstring": "Container for general GBD ids and metadata.",
        },
        "Restrictions": {
            "attrs": restrictions_attrs,
            "superclass": ("GbdRecord", gbd_record_attrs),
            "docstring": "Container for information about sub-populations the entity describes.",
        },
        "Tmred": {
            "attrs": tmred_attrs,
            "superclass": ("GbdRecord", gbd_record_attrs),
            "docstring": "Container for theoretical minimum risk exposure distribution data.",
        },
        "Categories": {
            "attrs": categories_attrs,
            "superclass": ("GbdRecord", gbd_record_attrs),
            "docstring": "Container for categorical risk exposure levels.",
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
            elif isinstance(attr, Tuple) and attr:
                if isinstance(attr[0], GbdRecord):
                    out[item] = tuple(r.to_dict() for r in attr)
            elif attr is not None:
                out[item] = attr
            else:
                continue
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
            
    def __eq__(self, other):
        return all([getattr(self, item) == getattr(other, item) for item in self.__slots__
                    if not isinstance(getattr(self, item), GbdRecord)])

    def __repr__(self):
        out = f'{self.__class__.__name__}('
        for i, slot in enumerate(self.__slots__):
            attr = self[slot]
            if attr is None:
                continue
            if i != 0:
                out += ','
            out += f'\\n{slot}='
            if isinstance(attr, tuple):
                out += '['+', '.join([entity.name if hasattr(entity, "name") else entity for entity in attr]) + ']'
            elif hasattr(attr, "name"):
                out += attr.name
            else:
                out += repr(attr)
        return out + ')'
'''
    return out


def build_mapping() -> str:
    """
    Generate string representations of class definitions.

    Returns
    -------
    str
        String representation of the base classes.

    """
    templates = make_module_docstring("Template classes for GBD entities", __file__)
    templates += make_import("typing", ["Union", "Tuple"])
    templates += (
        make_import(
            ".id",
            [
                "c_id",
                "s_id",
                "hs_id",
                "me_id",
                "cov_id",
                "rei_id",
                "scalar",
            ],
        )
        + SPACING
    )
    templates += make_gbd_record()

    for entity, info in get_base_types().items():
        templates += SPACING
        templates += make_record(entity, **info)

    return templates
