#!/usr/bin/env python

import sys
sys.path.insert(0,'src')

from distutils.core import setup

from quote_net import __author__, __version__, __license__, __email__

setup(name='quote_net',
      version=__version__,
      description='Creates file from templates',
      author=__author__,
      author_email=__email__,
      url='http://areku.kilu.de',

      package_dir={'':'src'},
      scripts=['src/quote_net'],
      py_modules=['quote_net'],
      provides=['quote_net('+__version__+')']
      
     )
