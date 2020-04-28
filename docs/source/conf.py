# import recommonmark
from recommonmark.transform import AutoStructify
import os
import sys
from recommonmark.parser import CommonMarkParser

sys.path.insert(0, os.path.abspath('../../'))  # for autodoc

project = 'sympathor'
copyright = '2020'
author = 'Armin Steinhauser'
release = 'v0.0.1'

extensions = [
    'recommonmark',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.napoleon',
    'sphinx.ext.githubpages',
    'sphinx.ext.mathjax',
    'sphinx.ext.viewcode',
]
# napoleon_google_docstring = True
# autosummary_generate = True

templates_path = ['_templates']
exclude_patterns = []

source_parsers = {'.md': CommonMarkParser}

# HTML
html_theme = 'sphinx_rtd_theme'
# html_static_path = ['_static']
html_context = {
    'source_url_prefix': "https://github.com/asteinh/sympathor/blob/master/docs/source/",
    "display_github": True,  # Integrate GitHub
    "github_user": "asteinh",  # Username
    "github_repo": "sympathor",  # Repo name
    "github_version": "master",  # Version
    "conf_py_path": "/docs/source/",
}

source_suffix = ['.rst', '.md']


def setup(app):
    app.add_config_value('recommonmark_config', {
            'enable_math': True,
            'enable_eval_rst': True,
            'auto_code_block': True,
            }, True)
    app.add_transform(AutoStructify)
