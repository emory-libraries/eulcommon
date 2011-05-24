# eulcore documentation build configuration file

import eulcommon

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.intersphinx']

#templates_path = ['templates']
exclude_trees = ['build']
source_suffix = '.rst'
master_doc = 'index'

project = 'EULcommon'
copyright = '2010, Emory University Libraries'
version = '%d.%d' % eulcommon.__version_info__[:2]
release = eulcommon.__version__
modindex_common_prefix = ['eulcommon.']

pygments_style = 'sphinx'

html_style = 'default.css'
#html_static_path = ['static']
htmlhelp_basename = 'eulcoredoc'

latex_documents = [
  ('index', 'eulcore.tex', 'EULcore Documentation',
   'Emory University Libraries', 'manual'),
]


# configuration for intersphinx: refer to the Python standard library, django
intersphinx_mapping = {
    'python': ('http://docs.python.org/', None),
    'django': ('http://django.readthedocs.org/en/latest/', None),
}
