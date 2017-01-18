"""The pycallnumber top-level package.

This package allows you to work with call numbers (Library of Congress,
Dewey Decimal, US SuDocs, and others)--parse them, normalize them, sort
them.
"""

from __future__ import unicode_literals

__version__ = '0.1'
__author__ = 'Jason Thomale'

import settings
from exceptions import CallNumberError, CallNumberWarning,\
                       InvalidCallNumberStringError, SettingsError,\
                       MethodError, OptionsError, UtilsError, RangeSetError,\
                       BadRange
from options import Options, ObjectWithOptions
from template import Template, SimpleTemplate, CompoundTemplate, Grouping
from unit import Unit, SimpleUnit, CompoundUnit
from set import RangeSet
import units
import utils
from factories import callnumber, cnrange, cnset
