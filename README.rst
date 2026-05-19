GBD Mapping
===========

** NOTE: This repository has been archived.**

The ``gbd_mapping`` package has been renamed and migrated into the
`vivarium-suite monorepo <https://github.com/ihmeuw/vivarium-suite>`_.

What changed
------------

- **PyPI distribution:** ``gbd_mapping`` -> ``vivarium-gbd-mapping``
- **Import paths:**
  - ``gbd_mapping`` -> ``vivarium.gbd_mapping``
  - ``gbd_mapping_generator`` -> ``vivarium.gbd_mapping_generator``
- **Source:** ``ihmeuw/gbd_mapping`` (archived) ->
  ``ihmeuw/vivarium-suite`` (under ``libs/gbd-mapping/``)
- **Docs:** https://vivarium-gbd-mapping.readthedocs.io/

What this last release (v5.1.0) is
----------------------------------

A backward-compatibility shim. It contains no code; installing it pulls in:

- ``vivarium-gbd-mapping>=6.0.0`` - the real implementation under the new import
  paths. Also provides the ``build_mapping`` console script.
- ``vivarium-compat>=0.5.0`` - an import hook that lets ``import gbd_mapping`` and
  ``import gbd_mapping_generator`` continue to work, emitting a ``DeprecationWarning``.
  Update your imports before the hook is removed.

If you depend on a specific pre-rename version (e.g. ``gbd_mapping==5.0.4``),
pin to that version - those earlier releases still ship the original modules
and continue to install standalone.

To migrate fully to the new package
-----------------------------------

.. image:: https://badge.fury.io/py/gbd-mapping.svg
    :target: https://badge.fury.io/py/gbd-mapping

.. image:: https://github.com/ihmeuw/gbd_mapping/actions/workflows/build.yml/badge.svg?branch=main
    :target: https://github.com/ihmeuw/gbd_mapping
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


`Check out the docs! <https://vivarium.readthedocs.io/projects/gbd-mapping/en/latest/>`_
----------------------------------------------------------------------------------------
