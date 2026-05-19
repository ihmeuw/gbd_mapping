"""Backward-compatibility shim for the standalone ``gbd_mapping`` package.

The real code has moved to ``vivarium-gbd-mapping`` (importable as
``vivarium.gbd_mapping``; the generator subpackage is at
``vivarium.gbd_mapping_generator``). This empty wheel exists so that

    pip install gbd_mapping

continues to resolve and pulls in the new package plus the ``vivarium-compat``
import hook. The hook redirects ``import gbd_mapping`` and
``import gbd_mapping_generator`` to their ``vivarium.*`` equivalents with a
``DeprecationWarning``. The ``build_mapping`` console script is provided by
``vivarium-gbd-mapping`` directly, so it continues to work via the transitive
install.

See https://github.com/ihmeuw/vivarium-suite for the new location.
"""

from setuptools import setup

setup(
    name="gbd_mapping",
    description=(
        "Backward-compatibility shim. The real package is now "
        "vivarium-gbd-mapping."
    ),
    long_description=open("README.rst").read(),
    long_description_content_type="text/x-rst",
    url="https://github.com/ihmeuw/vivarium-suite",
    author="The vivarium developers",
    author_email="vivarium.dev@gmail.com",
    license="BSD-3-Clause",
    classifiers=[
        "Development Status :: 7 - Inactive",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Libraries",
    ],
    packages=[],
    py_modules=[],
    install_requires=[
        "vivarium-gbd-mapping>=6.0.0",
        "vivarium-compat>=0.5.0",
    ],
    python_requires=">=3.10",
    # Version is derived from the git tag at build time (e.g. v5.1.0 -> 5.1.0).
    # Tag, then `python -m build`, then `twine upload`.
    use_scm_version={
        "tag_regex": r"^(?P<prefix>v)?(?P<version>[^\+]+)(?P<suffix>.*)?$",
    },
    setup_requires=["setuptools_scm"],
)
