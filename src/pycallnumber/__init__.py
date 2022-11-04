"""The pycallnumber top-level package.

This package allows you to work with call numbers (Library of Congress,
Dewey Decimal, US SuDocs, and others)--parse them, normalize them, sort
them.
"""

from __future__ import absolute_import

try:
    from importlib import metadata
except (ImportError, ModuleNotFoundError):
    import importlib_metadata as metadata

from pycallnumber import settings
from pycallnumber.exceptions import CallNumberError, CallNumberWarning,\
                                    InvalidCallNumberStringError,\
                                    SettingsError, MethodError, OptionsError,\
                                    UtilsError, RangeSetError, BadRange
from pycallnumber.options import Options, ObjectWithOptions
from pycallnumber.template import Template, SimpleTemplate, CompoundTemplate,\
                                  Grouping
from pycallnumber.unit import Unit, SimpleUnit, CompoundUnit
from pycallnumber.set import RangeSet
from pycallnumber import units
from pycallnumber import utils
from pycallnumber.factories import callnumber, cnrange, cnset

_md = metadata.metadata('pycallnumber')
__version__ = metadata.version('pycallnumber')
__name__ = 'pycallnumber'
__url__ = _md['Project-url'].split(', ')[1]
__description__ = _md['Summary']
__license__ = 'BSD'
__author__ = _md['Author-email'].split(' <')[0]
__author_email__ = _md['Author-email'].split(' <')[1].rstrip('>')
__maintainer__ = _md['Maintainer']
__keywords__ = _md['Keywords'] 
__all__ = ['settings', 'CallNumberError', 'CallNumberWarning',
           'InvalidCallNumberStringError', 'SettingsError', 'MethodError',
           'OptionsError', 'UtilsError', 'RangeSetError', 'BadRange',
           'Options', 'ObjectWithOptions', 'Template', 'SimpleTemplate',
           'CompoundTemplate', 'Grouping', 'Unit', 'SimpleUnit',
           'CompoundUnit', 'RangeSet', 'units',
           'utils', 'callnumber', 'cnrange', 'cnset']
