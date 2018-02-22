"""Use factories to generate call number units and ranges."""
from __future__ import absolute_import

from . import settings
from .utils import create_unit, load_class
from .exceptions import InvalidCallNumberStringError, SettingsError


def callnumber(cnstr, name='', useropts=None, unittypes=None):
    """Create a Unit object from a callnumber string.

    This function generates a Unit object that best matches the
    provided call number string (``cnstr``), based on a list of Unit
    types.

    Use ``name`` to specify the name of the resulting Unit object.
    Defaults to an empty string. It generally isn't important that this
    is specified, unless your code makes heavy use of the Unit.name.

    Use ``useropts`` to pass sets of Unit-specific options to the
    resulting Unit object (as a dict).

    Use ``unittypes`` to specify the list of valid Unit types to use
    to generate Unit objects. The first Unit type found that matches
    the given call number string is returned, so order matters.
    Defaults are found in settings.DEFAULT_UNIT_TYPES. Pass your own
    list to override the default.
    """
    useropts = useropts or {}
    utypes = unittypes or [load_class(t) for t in settings.DEFAULT_UNIT_TYPES]
    cn_unit = create_unit(cnstr, utypes, useropts, name)
    if cn_unit is None:
        types_str = ', '.join(['{}'.format(ut.__name__) for ut in utypes])
        msg = ('The provided call number string \'{}\' did not match any '
               'of the following known call number types: {}'
               ''.format(cnstr, types_str))
        raise InvalidCallNumberStringError(msg)
    return cn_unit


def cnrange(start, end, startname='', endname='', useropts=None,
            unittypes=None, rangesettype=None):
    """Create a contiguous RangeSet-type object.

    This function generates a RangeSet (or subclass) object that
    represents a single contiguous call number range, using a ``start``
    and an ``end`` value. These values may be call number strings or
    they may be Unit objects. If they are strings, they are first
    passed to the ``callnumber`` factory to generate Unit objects. They
    must both be or generate the same Unit type, and start must be less
    than end.

    Note that range start value is always considered inside the range,
    (inclusive) and the range end value is always considered outside
    the range (exclusive). This matches the behavior of the built-in
    ``range`` function. For example, if you want to model the LC class
    range that might commonly be written as 'MS 0000' to
    'MS 9999.9999', your range should be 'MS 0' to 'MT 0'.

    The kwargs ``startname,`` ``endname,`` ``useropts,`` and
    ``unittypes`` are used to generate Unit objects if start and/or end
    are strings. (See ``callnumber`` for information about these args.)
    They are ignored if start and end are both Units.

    Use the ``rangesettype`` kwarg to specify what type of object you
    want to generate. The default is settings.DEFAULT_RANGESET_TYPE,
    which defaults to RangeSet. If you provide your own class, it must
    be a subclass of RangeSet.
    """
    useropts = useropts or {}
    utypes = unittypes or [load_class(t) for t in settings.DEFAULT_UNIT_TYPES]
    rangesettype = rangesettype or load_class(settings.DEFAULT_RANGESET_TYPE)
    try:
        start = callnumber(start, startname, useropts, utypes)
    except TypeError:
        pass
    try:
        end = callnumber(end, endname, useropts, utypes)
    except TypeError:
        pass
    return rangesettype((start, end))


def cnset(ranges, names=None, useropts=None, unittypes=None,
          rangesettype=None):
    """Create a single RangeSet-type object from multiple ranges.

    This function generates a RangeSet (or subclass) object that
    represents a set of call numbers, not necessarily a contiguous
    range, comprising multiple ranges. Use this if, for example, you
    need to model a call number category that includes multiple
    ranges.

    As with ``cnrange``, ranges within the set have an inclusive start
    value and an exclusive end value.

    The ``ranges`` argument is a list or tuple, and it must contain
    either of the following:

    * RangeSet (or subclass) objects.
    * Lists or tuples, each of which has two items--the start and end
      value of a range. These values are passed to ``cn_range`` to
      generate RangeSet (or subclass) objects, so they may be Unit
      objects or call number strings.

    The other kwargs: ``names,`` ``useropts,`` ``unittypes,`` and
    ``rangesettype`` are as the kwargs used for ``callnumber`` and
    ``cnrange.``

    Note about ``names``: if you use call number strings in ``ranges,``
    and you want the resulting Units to have names, then the ``names``
    kwarg should be a list or tuple of lists or tuples that matches
    up with ranges. E.g.:

        ranges = [('AB 100', 'AB 150'), ('CA 0', 'CA 1300')]
        names = [('R1 Start', 'R1 End'), ('R2 Start', 'R2 End')]

    It will raise a SettingsError if the ``names`` kwarg is provided
    but doesn't parse correctly--e.g., if an IndexError is raised and
    caught while trying to parse it.

    """
    useropts = useropts or {}
    utypes = unittypes or [load_class(t) for t in settings.DEFAULT_UNIT_TYPES]
    rangesettype = rangesettype or load_class(settings.DEFAULT_RANGESET_TYPE)
    rangeset = rangesettype()
    for i, r in enumerate(ranges):
        try:
            rangeset |= r
        except TypeError:
            try:
                startname, endname = names[i][0], names[i][1]
            except IndexError:
                msg = ('The ``names`` kwarg should be a list or tuple of '
                       'lists or tuples that matches up with the provided '
                       'ranges so that each endpoint in the resulting '
                       'rangeset has a name specified. E.g., if ranges is '
                       '[(\'AB 100\', \'AB 150\'), (\'CA 0\', \'CA 1300\')] '
                       'then names might be [(\'R1 Start\', \'R1 End\'), '
                       '(\'R2 Start\', \'R2 End\')].')
                raise SettingsError(msg)
            except TypeError:
                startname, endname = '', ''
            rangeset |= cnrange(r[0], r[1], startname, endname, useropts,
                                utypes, rangesettype)
    return rangeset
