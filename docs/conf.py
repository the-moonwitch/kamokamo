# SPDX-License-Identifier: MPL-2.0

"""render linked API documentation and check its examples with Sphinx."""

from importlib.metadata import version as _version
from pathlib import Path

project = "kamokamo"
author = "samhain"
release = _version("kamokamo")
version = release

extensions = [
    "myst_parser",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
]
source_suffix = {".md": "markdown"}
myst_heading_anchors = 2
nitpicky = True
# these names are local type parameters, not importable Python objects.
nitpick_ignore = [("py:class", name) for name in "TEUVFSR"]
intersphinx_mapping = {"python": ("https://docs.python.org/3.14", None)}
doctest_path = [str(Path(__file__).resolve().parent.parent)]
python_maximum_signature_line_length = 72
html_theme = "alabaster"
html_logo = "_static/kamokamo-logo.png"
html_favicon = html_logo
html_theme_options = {
    "font_family": "Georgia, 'Kamokamo Japanese', serif",
    "head_font_family": "'xkcd Script', 'Kamokamo Japanese', sans-serif",
    "link": "#276897",
    "link_hover": "#806000",
    "pre_bg": "#eee",
    "show_relbars": True,
    "extra_nav_links": {
        "GitHub repo": "https://github.com/the-moonwitch/kamokamo"
    },
    "narrow_sidebar_bg": "#fff",
    "narrow_sidebar_fg": "#3e4349",
    "narrow_sidebar_link": "#276897",
}
html_sidebars = {"**": ["navigation.html", "searchbox.html"]}
html_static_path = ["_static"]
html_css_files = ["duck.css"]
html_show_copyright = False
html_show_sourcelink = False
