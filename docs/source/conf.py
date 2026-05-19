"""Sphinx configuration for the archived ``gbd_mapping`` docs.

This package is archived. The latest version of these docs is a single landing
page pointing at the new location; older tagged versions still build with the
original conf.py. Keep this file minimal to avoid breaking when the package
itself is uninstallable (the shim release contains no importable code).
"""

import datetime

project = "gbd_mapping"
author = "The vivarium developers"
copyright = f"2023-{datetime.date.today().year}, Institute for Health Metrics and Evaluation"

extensions = [
    "sphinx.ext.intersphinx",
]

templates_path = ["_templates"]
source_suffix = ".rst"
master_doc = "index"
language = "en"
exclude_patterns = []
pygments_style = "sphinx"

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

intersphinx_mapping = {
    "vivarium-gbd-mapping": (
        "https://vivarium-gbd-mapping.readthedocs.io/en/latest/",
        None,
    ),
}
