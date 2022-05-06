from pallets_sphinx_themes import ProjectLink

# -- Project information -----------------------------------------------------

project = 'Flask-JSONRPC'
copyright = '2021, Nycholas de Oliveira e Oliveira'  # pylint: disable=W0622
author = 'Nycholas de Oliveira e Oliveira'
release = '2.2.0'
version = '2.2.0'

# -- General configuration ---------------------------------------------------

master_doc = 'index'
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinxcontrib.log_cabinet',
    'pallets_sphinx_themes',
    'sphinx_issues',
    'sphinx_tabs.tabs',
]
autodoc_typehints = 'description'
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
issues_github_path = 'cenobites/flask-jsonrpc'

# -- Options for HTML output -------------------------------------------------

html_theme = 'flask'
html_theme_options = {'index_sidebar_logo': False}
html_context = {
    'project_links': [
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
# html_favicon = '_static/flask-jsonrpc-icon.png'
# html_logo = '_static/flask-jsonrpc-icon.png'
html_title = f'Flask-JSONRPC Documentation ({version})'
html_show_sourcelink = False

# LaTeX ----------------------------------------------------------------

latex_documents = [(master_doc, f'Flask-JSONRPC-{version}.tex', html_title, author, 'manual')]
