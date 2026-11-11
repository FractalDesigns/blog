# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Achraf Elafrit"
copyright = '2026, Achraf Elafrit'
author = 'Achraf Elafrit'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'lumina'
html_title = 'Achraf Elafrit'
html_short_title = 'Achraf Elafrit'
html_baseurl = 'https://fractaldesigns.github.io/blog/'

html_theme_options = {
    # 'dark_mode_default': 'auto',  # 'auto', 'light', or 'dark'
    # 'accent_color': '#10b981',     # custom accent color if desired
    'show_attribution': False,
}
html_static_path = ['_static']
