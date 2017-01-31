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

__version__ = '0.1'
__author__ = 'Jason Thomale'
__all__ = [settings, CallNumberError, CallNumberWarning,
           InvalidCallNumberStringError, SettingsError, MethodError,
           OptionsError, UtilsError, RangeSetError, BadRange, Options,
           ObjectWithOptions, Template, SimpleTemplate, CompoundTemplate,
           Grouping, Unit, SimpleUnit, CompoundUnit, RangeSet, units,
           utils, callnumber, cnrange, cnset]
