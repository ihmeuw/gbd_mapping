GBD Mapping
===========

.. image:: https://badge.fury.io/py/gbd-mapping.svg
    :target: https://badge.fury.io/py/gbd-mapping

.. image:: https://travis-ci.org/ihmeuw/gbd_mapping.svg?branch=master
    :target: https://travis-ci.org/ihmeuw/gbd_mapping
    :alt: Latest Version

.. image:: https://readthedocs.org/projects/gbd_mapping/badge/?version=latest
    :target: https://gbd_mapping.readthedocs.io/en/latest/?badge=latest
    :alt: Latest Docs

Mapping of Global Burden of Disease (GBD) entities to their metadata.

There are two packages offered in this distribution.  The first, the ``gbd_mapping_generator``
is a set of scripts that define templates and data gathering code used to produce the second, the ``gbd_mapping``.
The ``gbd_mapping_generator`` package will not function without access to the IHME cluster and some of our
internally used data access libraries. Mapping updates are managed by an automated toolchain, so this shouldn't
be an issue.

The ``gbd_mapping`` is a programmatically accessible (and TAB-complete-able) set of mappings for GBD entities
including:

 - Causes
 - Risks
 - Covariates
 - Etiologies
 - Sequelae

You can install ``gbd_mapping`` from PyPI with pip:

  ``> pip install gbd_mapping``

or build it from source with

  ``> git clone https://github.com/ihmeuw/gbd_mapping.git``

  ``> cd gbd_mapping``

  ``> pip install .``


Development and Mapping Generation
++++++++++++++++++++++++++++++++++

In order to generate or regenerate the mappings from data, you must have access to
the Institute for Health Metrics and Evaluation cluster and internal PyPI server.
Contact <collijk@uw.edu> if you need further instructions on that.

Given proper permissions, you can set up this library in development mode with

    ``> git clone https://github.com/ihmeuw/gbd_mapping.git``

    ``> cd gbd_mapping``

    ``> pip install -e .['dev']``
