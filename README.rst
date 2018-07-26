GBD Mapping
===========

Mapping of GBD entities to their metadata.

There are two packages offered in this distribution.  The first, the ``gbd_mapping_generator``
is a set of scripts that define templates and data gathering code used to produce the second, the ``gbd_mapping``.
The ``gbd_mapping_generator`` package will not function without access to the IHME cluster and some of our
internally used data access libraries.

The ``gbd_mapping`` is a programmatically accessible (and TAB-complete-able) set of mappings for GBD entities
including:

 - Causes
 - Risks
 - Covariates
 - Etiologies
 - Sequelae

There are additional mappings for objects mostly built around custom data.  The primary instance of this is the
``coverage_gap`` mapping.  Coverage Gaps are non-GBD entities representing the lack of coverage of interventions
to particular GBD causes and risks.

You can install ``gbd_mapping`` from PyPI with pip:

  ``> pip install gbd_mapping``

or build it from source with

  ``> git clone https://github.com/ihmeuw/gbd_mapping.git``

  ``> cd gbd_mapping``

  ``> python setup.py install``

