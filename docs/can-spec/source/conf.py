# Configuration file for the Sphinx documentation builder.
# CAN Interface Specification - Invi Tech

project = 'CAN Interface Specification'
copyright = '2026, Invi Tech'
author = 'Invi Tech'
release = '1.0.0'
version = '1.0'

extensions = []

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_css_files = ['custom.css']
html_logo = '_static/logo.svg'
html_favicon = None

html_theme_options = {
    'logo_only': True,
    'display_version': True,
    'prev_next_buttons_location': 'both',
    'style_external_links': True,
    'navigation_depth': 4,
    'collapse_navigation': False,
    'sticky_navigation': True,
    'includehidden': True,
    'titles_only': False,
}

html_context = {
    'display_github': False,
}

html_show_sourcelink = False

# Numbering
numfig = True
numfig_format = {
    'figure': 'Figure %s',
    'table': 'Table %s',
    'code-block': 'Listing %s',
}
