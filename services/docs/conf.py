import sys
import os
from datetime import datetime

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# Add project root to path for autodoc
sys.path.insert(0, os.path.abspath('..'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'services.settings')

import django
django.setup()

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Services Project'
now = datetime.now()
copyright = f'{now.year}, Services | Дата формирования: {now.strftime("%d.%m.%Y %H:%M")}'
author = 'Services'

version = '1.0'
release = '1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', '__pycache__', '*.pyc', 'node_modules']
master_doc = 'index'



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# -- Options for LaTeX output -----------------------------------------------
# For PDF generation
latex_elements = {
    'papersize': 'a4',
    'pointsize': '11pt',
    'preamble': r'''
\usepackage[utf8]{inputenc}
\usepackage[russian]{babel}
''',
}

latex_documents = [
    ('index', 'Services.tex', 'Services Project Documentation',
     'Services', 'manual'),
]

# -- Autodoc configuration --------------------------------------------------
autodoc_member_order = 'bysource'
autodoc_typehints = 'description'
