# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Nix Verfeles'
copyright = '2022, Nix Verfeles'
author = 'Nix Verfeles'
release = '1.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['myst_parser']

templates_path = ['_templates']
exclude_patterns = []

language = 'ja'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
myst_number_code_blocks = ["python"]

html_static_path = ['_static']

github_css = r"https://cdnjs.cloudflare.com/ajax/libs/highlight.js/9.9.0/styles/github.min.css"

diff2html_css = r"https://cdn.jsdelivr.net/npm/diff2html/bundles/css/diff2html.min.css"
diff2html_js = r"https://cdn.jsdelivr.net/npm/diff2html/bundles/js/diff2html-ui-slim.min.js"

html_css_files = [github_css, diff2html_css]
html_js_files = [diff2html_js, 'd2hset.js']
