"""Template classes for GBD entities

This code is automatically generated by gbd_mapping_generator/base_template_builder.py

Any manual changes will be lost.
"""
from typing import Union, Tuple
from .id import cid, sid, hsid, meid, covid, reiid, scalar


class GbdRecord:
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
            elif attr:
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

    def __repr__(self):
        out = f'{self.__class__.__name__}('
        for i, slot in enumerate(self.__slots__):
            attr = self[slot]
            if attr is None:
                continue
            if i != 0:
                out += ','
            out += f'\n{slot}='
            if isinstance(attr, tuple):
                out += '['+','.join([entity.name for entity in attr]) + ']'
            else:
                out += repr(attr)
        return out + ')'


class ModelableEntity(GbdRecord):
    """Container for general GBD ids and metadata."""
    __slots__ = ('name', 'kind', 'gbd_id', )

    def __init__(self,
                 name: str,
                 kind: str,
                 gbd_id: Union[cid, sid, hsid, meid, covid, reiid, None], ):
        super().__init__()
        self.name = name
        self.kind = kind
        self.gbd_id = gbd_id


class Restrictions(GbdRecord):
    """Container for information about sub-populations the entity describes."""
    __slots__ = ('male_only', 'female_only', 'yll_only', 'yld_only', 'yll_age_group_id_start',
                 'yll_age_group_id_end', 'yld_age_group_id_start', 'yld_age_group_id_end', )

    def __init__(self,
                 male_only: bool,
                 female_only: bool,
                 yll_only: bool,
                 yld_only: bool,
                 yll_age_group_id_start: int = None,
                 yll_age_group_id_end: int = None,
                 yld_age_group_id_start: int = None,
                 yld_age_group_id_end: int = None, ):
        super().__init__()
        self.male_only = male_only
        self.female_only = female_only
        self.yll_only = yll_only
        self.yld_only = yld_only
        self.yll_age_group_id_start = yll_age_group_id_start
        self.yll_age_group_id_end = yll_age_group_id_end
        self.yld_age_group_id_start = yld_age_group_id_start
        self.yld_age_group_id_end = yld_age_group_id_end


class Tmred(GbdRecord):
    """Container for theoretical minimum risk exposure distribution data."""
    __slots__ = ('distribution', 'min', 'max', 'inverted', )

    def __init__(self,
                 distribution: str,
                 inverted: bool, 
                 min: scalar = None,
                 max: scalar = None,):
        super().__init__()
        self.distribution = distribution
        self.min = min
        self.max = max
        self.inverted = inverted


class Categories(GbdRecord):
    """Container for categorical risk exposure levels."""
    __slots__ = ('cat1', 'cat2', 'cat3', 'cat4', 'cat5', 'cat6', 'cat7', 'cat8', 'cat9', 'cat10', 'cat11', 'cat12',
                 'cat13', 'cat14', 'cat15', 'cat16', 'cat17', 'cat18', 'cat19', 'cat20', 'cat21', 'cat22', 'cat23',
                 'cat24', 'cat25', 'cat26', 'cat27', 'cat28', 'cat29', 'cat30', 'cat31', 'cat32', 'cat33', 'cat34',
                 'cat35', 'cat36', 'cat37', 'cat38', 'cat39', 'cat40', 'cat41', 'cat42', 'cat43', 'cat44', 'cat45',
                 'cat46', 'cat47', 'cat48', 'cat49', 'cat50', 'cat51', 'cat52', 'cat53', 'cat54', 'cat55', 'cat56',
                 'cat57', 'cat58', 'cat59', 'cat60', 'cat61', 'cat62', 'cat63', 'cat64', 'cat65', 'cat66', 'cat67',
                 'cat68', 'cat69', 'cat70', 'cat71', 'cat72', 'cat73', 'cat74', 'cat75', 'cat76', 'cat77', 'cat78',
                 'cat79', 'cat80', 'cat81', 'cat82', 'cat83', 'cat84', 'cat85', 'cat86', 'cat87', 'cat88', 'cat89',
                 'cat90', 'cat91', 'cat92', 'cat93', 'cat94', 'cat95', 'cat96', 'cat97', 'cat98', 'cat99', 'cat100',
                 'cat101', 'cat102', 'cat103', 'cat104', 'cat105', 'cat106', 'cat107', 'cat108', 'cat109', 'cat110',
                 'cat111', 'cat112', 'cat113', 'cat114', 'cat115', 'cat116', 'cat117', 'cat118', 'cat119', 'cat120',
                 'cat121', 'cat122', 'cat123', 'cat124', 'cat125', 'cat126', 'cat127', 'cat128', 'cat129', 'cat130',
                 'cat131', 'cat132', 'cat133', 'cat134', 'cat135', 'cat136', 'cat137', 'cat138', 'cat139', 'cat140',
                 'cat141', 'cat142', 'cat143', 'cat144', 'cat145', 'cat146', 'cat147', 'cat148', 'cat149', )

    def __init__(self,
                 cat1: str,
                 cat2: str,
                 cat3: str = None,
                 cat4: str = None,
                 cat5: str = None,
                 cat6: str = None,
                 cat7: str = None,
                 cat8: str = None,
                 cat9: str = None,
                 cat10: str = None,
                 cat11: str = None,
                 cat12: str = None,
                 cat13: str = None,
                 cat14: str = None,
                 cat15: str = None,
                 cat16: str = None,
                 cat17: str = None,
                 cat18: str = None,
                 cat19: str = None,
                 cat20: str = None,
                 cat21: str = None,
                 cat22: str = None,
                 cat23: str = None,
                 cat24: str = None,
                 cat25: str = None,
                 cat26: str = None,
                 cat27: str = None,
                 cat28: str = None,
                 cat29: str = None,
                 cat30: str = None,
                 cat31: str = None,
                 cat32: str = None,
                 cat33: str = None,
                 cat34: str = None,
                 cat35: str = None,
                 cat36: str = None,
                 cat37: str = None,
                 cat38: str = None,
                 cat39: str = None,
                 cat40: str = None,
                 cat41: str = None,
                 cat42: str = None,
                 cat43: str = None,
                 cat44: str = None,
                 cat45: str = None,
                 cat46: str = None,
                 cat47: str = None,
                 cat48: str = None,
                 cat49: str = None,
                 cat50: str = None,
                 cat51: str = None,
                 cat52: str = None,
                 cat53: str = None,
                 cat54: str = None,
                 cat55: str = None,
                 cat56: str = None,
                 cat57: str = None,
                 cat58: str = None,
                 cat59: str = None,
                 cat60: str = None,
                 cat61: str = None,
                 cat62: str = None,
                 cat63: str = None,
                 cat64: str = None,
                 cat65: str = None,
                 cat66: str = None,
                 cat67: str = None,
                 cat68: str = None,
                 cat69: str = None,
                 cat70: str = None,
                 cat71: str = None,
                 cat72: str = None,
                 cat73: str = None,
                 cat74: str = None,
                 cat75: str = None,
                 cat76: str = None,
                 cat77: str = None,
                 cat78: str = None,
                 cat79: str = None,
                 cat80: str = None,
                 cat81: str = None,
                 cat82: str = None,
                 cat83: str = None,
                 cat84: str = None,
                 cat85: str = None,
                 cat86: str = None,
                 cat87: str = None,
                 cat88: str = None,
                 cat89: str = None,
                 cat90: str = None,
                 cat91: str = None,
                 cat92: str = None,
                 cat93: str = None,
                 cat94: str = None,
                 cat95: str = None,
                 cat96: str = None,
                 cat97: str = None,
                 cat98: str = None,
                 cat99: str = None,
                 cat100: str = None,
                 cat101: str = None,
                 cat102: str = None,
                 cat103: str = None,
                 cat104: str = None,
                 cat105: str = None,
                 cat106: str = None,
                 cat107: str = None,
                 cat108: str = None,
                 cat109: str = None,
                 cat110: str = None,
                 cat111: str = None,
                 cat112: str = None,
                 cat113: str = None,
                 cat114: str = None,
                 cat115: str = None,
                 cat116: str = None,
                 cat117: str = None,
                 cat118: str = None,
                 cat119: str = None,
                 cat120: str = None,
                 cat121: str = None,
                 cat122: str = None,
                 cat123: str = None,
                 cat124: str = None,
                 cat125: str = None,
                 cat126: str = None,
                 cat127: str = None,
                 cat128: str = None,
                 cat129: str = None,
                 cat130: str = None,
                 cat131: str = None,
                 cat132: str = None,
                 cat133: str = None,
                 cat134: str = None,
                 cat135: str = None,
                 cat136: str = None,
                 cat137: str = None,
                 cat138: str = None,
                 cat139: str = None,
                 cat140: str = None,
                 cat141: str = None,
                 cat142: str = None,
                 cat143: str = None,
                 cat144: str = None,
                 cat145: str = None,
                 cat146: str = None,
                 cat147: str = None,
                 cat148: str = None,
                 cat149: str = None, ):
        super().__init__()
        self.cat1 = cat1
        self.cat2 = cat2
        self.cat3 = cat3
        self.cat4 = cat4
        self.cat5 = cat5
        self.cat6 = cat6
        self.cat7 = cat7
        self.cat8 = cat8
        self.cat9 = cat9
        self.cat10 = cat10
        self.cat11 = cat11
        self.cat12 = cat12
        self.cat13 = cat13
        self.cat14 = cat14
        self.cat15 = cat15
        self.cat16 = cat16
        self.cat17 = cat17
        self.cat18 = cat18
        self.cat19 = cat19
        self.cat20 = cat20
        self.cat21 = cat21
        self.cat22 = cat22
        self.cat23 = cat23
        self.cat24 = cat24
        self.cat25 = cat25
        self.cat26 = cat26
        self.cat27 = cat27
        self.cat28 = cat28
        self.cat29 = cat29
        self.cat30 = cat30
        self.cat31 = cat31
        self.cat32 = cat32
        self.cat33 = cat33
        self.cat34 = cat34
        self.cat35 = cat35
        self.cat36 = cat36
        self.cat37 = cat37
        self.cat38 = cat38
        self.cat39 = cat39
        self.cat40 = cat40
        self.cat41 = cat41
        self.cat42 = cat42
        self.cat43 = cat43
        self.cat44 = cat44
        self.cat45 = cat45
        self.cat46 = cat46
        self.cat47 = cat47
        self.cat48 = cat48
        self.cat49 = cat49
        self.cat50 = cat50
        self.cat51 = cat51
        self.cat52 = cat52
        self.cat53 = cat53
        self.cat54 = cat54
        self.cat55 = cat55
        self.cat56 = cat56
        self.cat57 = cat57
        self.cat58 = cat58
        self.cat59 = cat59
        self.cat60 = cat60
        self.cat61 = cat61
        self.cat62 = cat62
        self.cat63 = cat63
        self.cat64 = cat64
        self.cat65 = cat65
        self.cat66 = cat66
        self.cat67 = cat67
        self.cat68 = cat68
        self.cat69 = cat69
        self.cat70 = cat70
        self.cat71 = cat71
        self.cat72 = cat72
        self.cat73 = cat73
        self.cat74 = cat74
        self.cat75 = cat75
        self.cat76 = cat76
        self.cat77 = cat77
        self.cat78 = cat78
        self.cat79 = cat79
        self.cat80 = cat80
        self.cat81 = cat81
        self.cat82 = cat82
        self.cat83 = cat83
        self.cat84 = cat84
        self.cat85 = cat85
        self.cat86 = cat86
        self.cat87 = cat87
        self.cat88 = cat88
        self.cat89 = cat89
        self.cat90 = cat90
        self.cat91 = cat91
        self.cat92 = cat92
        self.cat93 = cat93
        self.cat94 = cat94
        self.cat95 = cat95
        self.cat96 = cat96
        self.cat97 = cat97
        self.cat98 = cat98
        self.cat99 = cat99
        self.cat100 = cat100
        self.cat101 = cat101
        self.cat102 = cat102
        self.cat103 = cat103
        self.cat104 = cat104
        self.cat105 = cat105
        self.cat106 = cat106
        self.cat107 = cat107
        self.cat108 = cat108
        self.cat109 = cat109
        self.cat110 = cat110
        self.cat111 = cat111
        self.cat112 = cat112
        self.cat113 = cat113
        self.cat114 = cat114
        self.cat115 = cat115
        self.cat116 = cat116
        self.cat117 = cat117
        self.cat118 = cat118
        self.cat119 = cat119
        self.cat120 = cat120
        self.cat121 = cat121
        self.cat122 = cat122
        self.cat123 = cat123
        self.cat124 = cat124
        self.cat125 = cat125
        self.cat126 = cat126
        self.cat127 = cat127
        self.cat128 = cat128
        self.cat129 = cat129
        self.cat130 = cat130
        self.cat131 = cat131
        self.cat132 = cat132
        self.cat133 = cat133
        self.cat134 = cat134
        self.cat135 = cat135
        self.cat136 = cat136
        self.cat137 = cat137
        self.cat138 = cat138
        self.cat139 = cat139
        self.cat140 = cat140
        self.cat141 = cat141
        self.cat142 = cat142
        self.cat143 = cat143
        self.cat144 = cat144
        self.cat145 = cat145
        self.cat146 = cat146
        self.cat147 = cat147
        self.cat148 = cat148
        self.cat149 = cat149
