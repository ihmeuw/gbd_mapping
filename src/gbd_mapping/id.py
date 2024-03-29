"""Custom ID types for GBD entities

This code is automatically generated by gbd_mapping_generator/id_builder.py

Any manual changes will be lost.
"""


class me_id(int):
    """Modelable Entity ID"""
    def __repr__(self):
        return "me_id({:d})".format(self)


class rei_id(int):
    """Risk-Etiology-Impairment ID"""
    def __repr__(self):
        return "rei_id({:d})".format(self)


class c_id(int):
    """Cause ID"""
    def __repr__(self):
        return "c_id({:d})".format(self)


class s_id(int):
    """Sequela ID"""
    def __repr__(self):
        return "s_id({:d})".format(self)


class cov_id(int):
    """Covariate ID"""
    def __repr__(self):
        return "cov_id({:d})".format(self)


class hs_id(int):
    """Health State ID"""
    def __repr__(self):
        return "hs_id({:d})".format(self)


class scalar(float):
    """Raw Measure Value"""
    def __repr__(self):
        return "scalar({:f})".format(self)


class Unknown:
    """Marker for unknown values."""
    def __repr__(self):
        return "UNKNOWN"


UNKNOWN = Unknown()


class UnknownEntityError(Exception):
    """Exception raised when a quantity is requested from vivarium_inputs with an `UNKNOWN` id."""
    pass
