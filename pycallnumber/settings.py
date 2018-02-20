"""Default settings for pycallnumber package.

This module provides packagewide defaults. Generally, you can override
them on an individual basis by passing the appropriate parameters to
various functions and object methods, as explained below.

DO NOT override them by changing these values directly.

"""

# ************** OVERRIDABLE UNIT OPTIONS
# These are default options controlling unit type normalization.
# Generally, you shouldn't have to override the defaults. But, in case
# you do, here's what the options are and how to override them.
#
# Alphabetic types provide options for controlling how to normalize
# case. Formatting types provide options for controlling whether or not
# formatting characters appear in sort and search normalizations.
#
# Compound Unit types that contain an Alphabetic and/or Formatting type
# inherit their options. AlphaNumeric types therefore have only case
# options; AlphaSymbol types have case and formatting options, for
# example.
#
# HOW TO OVERRIDE THESE
#
# There are four ways to override options, listed here in order of
# strength or precedence.
#
# 1.  Set the relevant class attribute for a unit type to FORCE that
#     unit type to use the particular setting. Overrides everything.
#     Example: units.Cutter.sort_case = 'upper'
#
# 2.  Set the option for an individual object by passing the option via
#     a kwarg when you initialize the object. This will override any
#     options defaults (see 4) but NOT forced class attributes (see 1).
#     Example: units.Cutter('c35', sort_case='upper')
#
# 3.  If using one of the factories.py functions, such as `callnumber`,
#     you can pass options in using a dict in the `useropts` kwarg.
#     This passes your options on when the correct unit object is
#     initialized, as in option 2a.
#
# 4.  Set or change the default value for an option by setting the
#     relevant option in the `options_defaults` class attribute (dict).
#     This changes the default for that unit type, which is used IF
#     nothing else overrides it. Caveat: be careful that you create a
#     copy of the `options_defaults` dict before making changes.
#     Otherwise you will end up changing defaults for other unit types.
#     Example: units.Cutter.options_defaults = units.Cutter\
#                 .options_defaults.copy()
#              units.Cutter.options_defaults['sort_case'] = 'upper'
#
# ALPHABETIC `CASE` Options
# -------------------------
# Options are: `display_case` (controls case when using the `for_print`
# unit method), `search_case` (controls case when using the
#  `for_search` unit method), and `sort_case` (controls case when using
# the `for_sort` unit method).
#
# Use 'lower' for lowercase, 'upper' for uppercase, and anything
# else for retaining the original case.
DEFAULT_DISPLAY_CASE = ''
DEFAULT_SEARCH_CASE = 'lower'
DEFAULT_SORT_CASE = 'lower'

# FORMATTING `USE IN` Options
# ---------------------------
# Options are: `use_formatting_in_search` (controls whether formatting
# appears at all when using the `for_search` unit method) and
# `use_formatting_in_sort` (controls whether formatting appears at all
# when using the `for_sort` unit method).
#
# Use True to include formatting in a normalized string or False to
# hide it.
DEFAULT_USE_FORMATTING_IN_SEARCH = False
DEFAULT_USE_FORMATTING_IN_SORT = False


# ************** NON-OVERRIDABLE DEFAULTS
# DEFAULT_MAX_NUMERIC_ZFILL is used by Numeric and derived classes. You
# cannot change this directly, but if you specify that a Numeric unit
# type has a maximum value that would require more than the default
# number of digits, it will be adjusted accordingly for that type.
DEFAULT_MAX_NUMERIC_ZFILL = 10


# ************** `FACTORIES` SETTINGS
# DEFAULT_UNIT_TYPES is used by the factories.py functions to specify
# exactly what types of call numbers these functions should recognize.
# You can override this setting by passing your own custom list via the
# `unittypes` kwarg of these functions.
#
# Example:
#   my_unit_list = [local_module.MyDewey, local_module.MyLC]
#   pycallnumber.callnumber('my_string', unittypes=my_unit_list)
#
# Note that DEFAULT_UNIT_TYPES contains path strings. Your custom list
# (passed to pycallnumber.callnumber via `unittypes`) should contain
# the unit types themselves, not strings.
DEFAULT_UNIT_TYPES = [
    'pycallnumber.units.Dewey',
    'pycallnumber.units.DeweyClass',
    'pycallnumber.units.LC',
    'pycallnumber.units.LcClass',
    'pycallnumber.units.SuDoc',
    'pycallnumber.units.Local'
]

# DEFAULT_RANGESET_TYPE is used by the factories.py `cnrange` and
# `cnset` functions to determine the class that implements call number
# ranges. If you create your own RangeSet class, you can pass the type
# directly via the `rangesettype` kwarg.
#
# Note, like DEFAULT_UNIT_TYPES, DEFAULT_RANGESET_TYPE contains a path
# string, while your `rangessettype` kwarg should be a type/class.
DEFAULT_RANGESET_TYPE = 'pycallnumber.set.RangeSet'
