"""Default settings for pycallnumber package."""

DEFAULT_UNIT_TYPES = [
    'pycallnumber.units.Dewey',
    'pycallnumber.units.DeweyClass',
    'pycallnumber.units.LC',
    'pycallnumber.units.LcClass',
    'pycallnumber.units.SuDoc',
    'pycallnumber.units.Local'
]

DEFAULT_RANGESET_TYPE = 'pycallnumber.set.RangeSet'

# Default Unit Options
DEFAULT_DISPLAY_CASE = ''
DEFAULT_SEARCH_CASE = 'lower'
DEFAULT_SORT_CASE = 'lower'
DEFAULT_USE_FORMATTING_IN_SEARCH = False
DEFAULT_USE_FORMATTING_IN_SORT = False
DEFAULT_MAX_NUMERIC_ZFILL = 10

DEFAULT_UNIT_OPTIONS = {
    'display_case': DEFAULT_DISPLAY_CASE,
    'search_case': DEFAULT_SEARCH_CASE,
    'sort_case': DEFAULT_SORT_CASE,
}
