import sys
import os
mod_path = os.path.abspath(os.path.join(os.path.dirname(__file__),'../'))
sys.path.insert(0, mod_path)
import shout

extensions = [
    'sphinx.ext.intersphinx',
    'sphinx.ext.autodoc'
]
source_suffix = '.rst'
master_doc = 'index'
project = u'Shout'
copyright = u'2014, {0}'.format(shout.__author__)
version = shout.__version__
release = shout.__version__
pygments_style = 'sphinx'
intersphinx_mapping = {'http://docs.python.org/': None}
