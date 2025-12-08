# Copyright (c) 2012-2025, Cenobit Technologies, Inc. http://cenobit.es/
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# * Neither the name of the Cenobit Technologies nor the names of
#    its contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
from pallets_sphinx_themes import ProjectLink, get_version

project = 'Flask-JSONRPC'
copyright = '2021-2025, Cenobit Technologies, Inc. http://cenobit.es/'
author = 'Nycholas de Oliveira e Oliveira'
release, version = get_version('Flask-JSONRPC')

default_role = 'code'
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.extlinks',
    'sphinx.ext.intersphinx',
    'sphinx.ext.autosummary',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.todo',
    'sphinxcontrib.log_cabinet',
    'sphinx_tabs.tabs',
    # 'sphinx_autodoc_typehints',
    'pallets_sphinx_themes',
]
autodoc_member_order = 'bysource'
autodoc_typehints = 'description'
autodoc_preserve_defaults = True
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
issues_github_path = 'cenobites/flask-jsonrpc'
extlinks = {
    'issue': ('https://github.com/cenobites/flask-jsonrpc/issues/%s', '#%s'),
    'pr': ('https://github.com/cenobites/flask-jsonrpc/pull/%s', '#%s'),
    'ghsa': ('https://github.com/cenobites/flask-jsonrpc/security/advisories/GHSA-%s', 'GHSA-%s'),
}
intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'flask': ('https://flask.palletsprojects.com/', None),
}

html_theme = 'flask'
html_theme_options = {'index_sidebar_logo': False}
html_context = {
    'project_links': [
        ProjectLink('Donate', 'https://github.com/sponsors/nycholas'),
        ProjectLink('PyPI Releases', 'https://pypi.org/project/Flask-JSONRPC/'),
        ProjectLink('Source Code', 'https://github.com/cenobites/flask-jsonrpc/'),
        ProjectLink('Issue Tracker', 'https://github.com/cenobites/flask-jsonrpc/issues/'),
        ProjectLink('Website', 'https://flask-jsonrpc.readthedocs.io/'),
    ]
}
html_sidebars = {
    'index': ['project.html', 'localtoc.html', 'searchbox.html', 'ethicalads.html'],
    '**': ['localtoc.html', 'relations.html', 'searchbox.html', 'ethicalads.html'],
}
singlehtml_sidebars = {'index': ['project.html', 'localtoc.html', 'ethicalads.html']}
html_static_path = ['_static']
html_favicon = '_static/flask-jsonrpc-icon.svg'
html_logo = '_static/flask-jsonrpc-icon.svg'
html_title = f'Flask-JSONRPC Documentation ({version})'
html_show_sourcelink = False

gettext_uuid = True
gettext_compact = False
autosummary_generate = True
napoleon_google_docstring = True
add_module_names = False
