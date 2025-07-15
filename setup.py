#!/usr/bin/env python
import json
import os
import sys

from packaging.version import parse
from setuptools import find_packages, setup

with open("python_versions.json", "r") as f:
    supported_python_versions = json.load(f)

python_versions = [parse(v) for v in supported_python_versions]
min_version = min(python_versions)
max_version = max(python_versions)
if not (
    min_version <= parse(".".join([str(v) for v in sys.version_info[:2]])) <= max_version
):
    py_version = ".".join([str(v) for v in sys.version_info[:3]])
    # NOTE: Python 3.5 does not support f-strings
    error = (
        "\n--------------------------------------------\n"
        "Error: gbd_mapping runs under python {min_version}-{max_version}.\n"
        "You are running python {py_version}.\n".format(
            min_version=min_version.base_version,
            max_version=max_version.base_version,
            py_version=py_version,
        )
        + "--------------------------------------------\n"
    )
    print(error, file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    base_dir = os.path.dirname(__file__)
    src_dir = os.path.join(base_dir, "src")

    about = {}
    with open(os.path.join(src_dir, "gbd_mapping", "__about__.py")) as f:
        exec(f.read(), about)

    with open(os.path.join(base_dir, "README.rst")) as f:
        long_description = f.read()

    install_requirements = [
        "vivarium_build_utils>=1.1.0,<2.0.0",
        "click",
        "numpy",
        "pandas",
        "pyyaml",
    ]

    setup_requires = ["setuptools_scm"]

    data_requires = [
        "vivarium-gbd-access>=4.0.0, <5.0.0",
    ]

    test_requirements = [
        "pytest",
        "pytest-cov",
        "pytest-mock",
    ]

    doc_requirements = [
        "sphinx>=6.2.1, <7.0",
        "sphinx-rtd-theme",
        "sphinx-autodoc-typehints",
    ]

    lint_requirements = [
        "black==22.3.0",
        "isort==5.13.2",
    ]

    setup(
        name=about["__title__"],
        description=about["__summary__"],
        long_description=long_description,
        url=about["__uri__"],
        author=about["__author__"],
        author_email=about["__email__"],
        package_dir={"": "src"},
        packages=find_packages(where="src"),
        include_package_data=True,
        install_requires=install_requirements,
        tests_require=test_requirements,
        extras_require={
            "docs": doc_requirements,
            "test": test_requirements,
            "data": data_requires,
            "dev": doc_requirements + test_requirements + data_requires + lint_requirements,
        },
        entry_points="""
                [console_scripts]
                build_mapping=gbd_mapping_generator.build_mapping:build_mapping
            """,
        zip_safe=False,
        use_scm_version={
            "write_to": "src/gbd_mapping/_version.py",
            "write_to_template": '__version__ = "{version}"\n',
            "tag_regex": r"^(?P<prefix>v)?(?P<version>[^\+]+)(?P<suffix>.*)?$",
        },
        setup_requires=setup_requires,
    )
