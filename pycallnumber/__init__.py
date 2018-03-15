"""The pycallnumber top-level package.

This package allows you to work with call numbers (Library of Congress,
Dewey Decimal, US SuDocs, and others)--parse them, normalize them, sort
them.
"""

from __future__ import unicode_literals
from __future__ import absolute_import

from . import settings
from .exceptions import CallNumberError, CallNumberWarning,\
                       InvalidCallNumberStringError, SettingsError,\
                       MethodError, OptionsError, UtilsError, RangeSetError,\
                       BadRange
from .options import Options, ObjectWithOptions
from .template import Template, SimpleTemplate, CompoundTemplate, Grouping
from .unit import Unit, SimpleUnit, CompoundUnit
from .set import RangeSet
from . import units
from . import utils
from .factories import callnumber, cnrange, cnset

__all__ = [settings, CallNumberError, CallNumberWarning,
           InvalidCallNumberStringError, SettingsError, MethodError,
           OptionsError, UtilsError, RangeSetError, BadRange, Options,
           ObjectWithOptions, Template, SimpleTemplate, CompoundTemplate,
           Grouping, Unit, SimpleUnit, CompoundUnit, RangeSet, units,
           utils, callnumber, cnrange, cnset]

__version__ = '0.1.2'
__name__ = 'pycallnumber'
__url__ = 'https://github.com/unt-libraries/pycallnumber'
__description__ = 'A Python library for parsing call numbers.'
__license__ = 'BSD'
__author__ = 'Jason Thomale'
__author_email__ = 'jason.thomale@unt.edu'
__maintainer__ = 'University of North Texas Libraries'
__keywords__ = 'python, callnumber, callnumbers, call number, call numbers'
