from __future__ import unicode_literals

import pytest

from context import unit as un
from context import units as uns
from context import template as t
from context import exceptions as e
from context import set as s
from context import factories as f


# Fixtures, factories, and test data

class FactoryTestType(un.CompoundUnit):

    options_defaults = uns.AlphaNumeric.options_defaults.copy()
    options_defaults.update({
        'test_option': True,
    })

    template = t.CompoundTemplate(
        separator_type=uns.simple.DEFAULT_SEPARATOR_TYPE,
        groups=[
            {'name': 'letters', 'type': uns.Alphabetic, 'min': 1, 'max': 1},
            {'name': 'numbers', 'type': uns.Numeric, 'min': 1, 'max': 1},
        ]
    )


class AnotherFactoryTestType(un.CompoundUnit):

    template = t.CompoundTemplate(
        separator_type=uns.simple.DEFAULT_SEPARATOR_TYPE,
        groups=[
            {'name': 'numbers', 'type': uns.Numeric, 'min': 1, 'max': 1},
            {'name': 'letters', 'type': uns.Alphabetic, 'min': 1, 'max': 1},
        ]
    )


class FactoryTestRangeSetType(s.RangeSet):
    pass


aa0 = FactoryTestType('AA 0')
aa50 = FactoryTestType('AA 50')
aa100 = FactoryTestType('AA 100')
aa1000 = FactoryTestType('AA 1000')
ab0 = FactoryTestType('AB 0')
_10a = AnotherFactoryTestType('10 A')
_100a = AnotherFactoryTestType('100 A')


# Tests

@pytest.mark.callnumber_factory
def test_callnumber_selects_correct_type_using_unittype_kwarg():
    """Calls to the ``callnumber`` factory should return the correct
    Unit type when a specific type list is provided via the
    ``unittypes`` kwarg.
    """
    types = [FactoryTestType, AnotherFactoryTestType]
    assert f.callnumber('AA 0', unittypes=types) == FactoryTestType('AA 0')


@pytest.mark.callnumber_factory
def test_callnumber_raises_error_using_unittype_kwarg():
    """Calls to the ``callnumber`` factory should raise an
    InvalidCallNumberStringError when the given call number string does
    not match any of the Unit types given, when a specific type list is
    provided via the ``unittypes`` kwarg.
    """
    types = [FactoryTestType, AnotherFactoryTestType]
    with pytest.raises(e.InvalidCallNumberStringError):
        f.callnumber('AA 0 AA 0', unittypes=types)


@pytest.mark.callnumber_factory
def test_callnumber_sets_correct_options_using_useropts_kwarg():
    """Calls to the ``callnumber`` factory should utilize a set of
    custom options when one is provided via the ``useropts`` kwarg.
    """
    opts = {'test_option': False}
    types = [FactoryTestType]
    default = f.callnumber('AA 0', unittypes=types)
    custom = f.callnumber('AA 0', useropts=opts, unittypes=types)
    assert default.test_option is True and custom.test_option is False


@pytest.mark.callnumber_factory
def test_callnumber_sets_unitname_using_name_kwarg():
    """Calls to the ``callnumber`` factory should generate a Unit
    object with a ``name`` attribute matching the value passed to the
    ``name`` kwarg.
    """
    types = [FactoryTestType]
    custom = f.callnumber('AA 0', name='test_unit', unittypes=types)
    assert custom.name == 'test_unit'


@pytest.mark.cnrange_factory
@pytest.mark.parametrize('start, end, expected', [
    ('AA 0', 'AA 100', s.RangeSet((aa0, aa100))),
    ('AA 0', aa100, s.RangeSet((aa0, aa100))),
    (aa0, 'AA 100', s.RangeSet((aa0, aa100))),
    (aa0, aa100, s.RangeSet((aa0, aa100))),
    ('10 A', 'AA 0', e.BadRange),
])
def test_cnrange_returns_object_or_raises_error(start, end, expected):
    """Calls to the ``cnrange`` factory should successfully create the
    expected RangeSet object or raise the expected error, based on the
    provided start and end values.
    """
    types = [FactoryTestType, AnotherFactoryTestType]
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            f.cnrange(start, end, unittypes=types)
    else:
        assert f.cnrange(start, end, unittypes=types) == expected


@pytest.mark.cnrange_factory
def test_cnrange_returns_correct_type_using_rangesettype_kwarg():
    """Calls to the ``cnrange`` factory that provide a custom RangeSet
    type via the ``rangesettype`` kwarg should return the correct type
    of object.
    """
    types = [FactoryTestType]
    rng = f.cnrange('AA 0', 'AA 100', unittypes=types,
                    rangesettype=FactoryTestRangeSetType)
    assert isinstance(rng, FactoryTestRangeSetType)


@pytest.mark.cnset_factory
@pytest.mark.parametrize('ranges, expected', [
    ((('AA 0', 'AA 50'), ('AA 100', 'AB 0')),
     s.RangeSet((aa0, aa50), (aa100, ab0))),
    ((('AA 0', 'AA 100'), ('AA 100', 'AB 0')),
     s.RangeSet((aa0, ab0))),
    ((s.RangeSet((aa0, aa50)), ('AA 100', 'AB 0')),
     s.RangeSet((aa0, aa50), (aa100, ab0))),
    ((('AA 0', 'AA 50'), s.RangeSet((aa100, ab0))),
     s.RangeSet((aa0, aa50), (aa100, ab0))),
    ((('AA 0', 'AA 50'), ('10 A', '100 A')), TypeError),
])
def test_cnset_returns_object_or_raises_error(ranges, expected):
    """Calls to the ``cnset`` factory should successfully create the
    expected RangeSet object or raise the expected error, based on the
    provided values for ranges.
    """
    types = [FactoryTestType, AnotherFactoryTestType]
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            f.cnset(ranges, unittypes=types)
    else:
        assert f.cnset(ranges, unittypes=types) == expected


@pytest.mark.cnset_factory
def test_cnset_assigns_unit_names_correctly_with_names_kwarg():
    """Calls to the ``cnset`` factory should produce a RangeSet object
    with internal Unit objects representing RangeSet endpoints that
    have correct names based on the provided ``names`` kwarg.
    """
    types = [FactoryTestType]
    ranges = [('AB 100', 'AB 150'), ('CA 0', 'CA 1300')]
    names = [('R1 Start', 'R1 End'), ('R2 Start', 'R2 End')]
    myset = f.cnset(ranges, names=names, unittypes=types)
    assert (myset.ranges[0].start.name == 'R1 Start' and
            myset.ranges[0].end.name == 'R1 End' and
            myset.ranges[1].start.name == 'R2 Start' and
            myset.ranges[1].end.name == 'R2 End')


@pytest.mark.cnset_factory
def test_cnset_raises_SettingsError_if_names_kwarg_causes_errors():
    """Calls to the ``cnset`` factory should produce a RangeSet object
    with internal Unit objects representing RangeSet endpoints that
    have blank names if the provided ``names`` kwarg .
    """
    types = [FactoryTestType]
    ranges = [('AB 100', 'AB 150'), ('CA 0', 'CA 1300')]
    names = [('R1 Start', 'R1 End')]
    with pytest.raises(e.SettingsError):
        f.cnset(ranges, names=names, unittypes=types)
