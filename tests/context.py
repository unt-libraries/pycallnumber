"""Provides imports for all test scripts.

This is used so that tests can be run without having to have the
pycallnumber package installed, from directories other than tests.
"""

import os
import sys


current_path = os.path.dirname(os.path.realpath(__file__))
pycn_path = os.path.abspath('{}/..'.format(current_path))
sys.path.insert(0, pycn_path)


import pycallnumber
from pycallnumber import exceptions
from pycallnumber import factories
from pycallnumber import options
from pycallnumber import set
from pycallnumber import settings
from pycallnumber import template
from pycallnumber import unit
from pycallnumber import units
from pycallnumber import utils
