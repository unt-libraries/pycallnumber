from __future__ import unicode_literals
from builtins import str
import operator

import pytest

from context import unit as u
from context import template as t
from context import exceptions as e
from helpers import generate_params


# SimpleUnit **********************************************************

# Fixtures, factories, and test data

class SUTest_Simple(u.SimpleUnit):

    options_defaults = u.SimpleUnit.options_defaults.copy()
    options_defaults.update({
        'print_value': '[PR]',
    })
    definition = 'SUTest_Simple definition'
    template = t.SimpleTemplate(
        min_length=1,
        max_length=None,
        base_pattern=r'[A-Za-z]',
        base_description='SUTest_Simple description',
        base_description_plural='SUTest_Simple description plural',
        pre_pattern=r'0?',
        pre_description='SUTest_Simple pre_description',
        post_pattern=r'0?',
        post_description='SUTest_Simple post_description',
    )

    def for_print(self):
        return '{}{}'.format(self._string, self.print_value)


test_obj_attributes = ['definition', 'is_separator', 'is_formatting',
                       'print_value']

test_template_attributes = ['min_length', 'max_length', 'base_pattern',
                            'base_description', 'base_description_plural',
                            'pre_pattern', 'pre_description', 'post_pattern',
                            'post_description']


class SUTest_CompSmall(SUTest_Simple):

    """Will always be smaller than an SUTest_Simple Unit"""

    def for_sort(self):
        return '!{}'.format(self._string)


class SUTest_CompLarge(SUTest_Simple):

    """Will always be larger than an SUTest_Simple Unit"""

    def for_sort(self):
        return '~{}'.format(self._string)


SIMPUNIT_CMP_PARAMS = [
    (SUTest_Simple('a'), SUTest_Simple('a'), operator.lt, False),
    (SUTest_Simple('a'), SUTest_Simple('a'), operator.le, True),
    (SUTest_Simple('a'), SUTest_Simple('a'), operator.eq, True),
    (SUTest_Simple('a'), SUTest_Simple('a'), operator.ne, False),
    (SUTest_Simple('a'), SUTest_Simple('a'), operator.ge, True),
    (SUTest_Simple('a'), SUTest_Simple('a'), operator.gt, False),
    (SUTest_Simple('a'), SUTest_Simple('a'), operator.contains, True),
    (SUTest_Simple('a'), SUTest_Simple('b'), operator.lt, True),
    (SUTest_Simple('a'), SUTest_Simple('b'), operator.le, True),
    (SUTest_Simple('a'), SUTest_Simple('b'), operator.eq, False),
    (SUTest_Simple('a'), SUTest_Simple('b'), operator.ne, True),
    (SUTest_Simple('a'), SUTest_Simple('b'), operator.ge, False),
    (SUTest_Simple('a'), SUTest_Simple('b'), operator.gt, False),
    (SUTest_Simple('a'), SUTest_Simple('b'), operator.contains, False),
    (SUTest_Simple('a'), SUTest_CompSmall('b'), operator.lt, False),
    (SUTest_Simple('a'), SUTest_CompSmall('b'), operator.le, False),
    (SUTest_Simple('a'), SUTest_CompSmall('b'), operator.eq, False),
    (SUTest_Simple('a'), SUTest_CompSmall('b'), operator.ne, True),
    (SUTest_Simple('a'), SUTest_CompSmall('b'), operator.ge, True),
    (SUTest_Simple('a'), SUTest_CompSmall('b'), operator.gt, True),
    (SUTest_Simple('b'), SUTest_CompLarge('a'), operator.lt, True),
    (SUTest_Simple('b'), SUTest_CompLarge('a'), operator.le, True),
    (SUTest_Simple('b'), SUTest_CompLarge('a'), operator.eq, False),
    (SUTest_Simple('b'), SUTest_CompLarge('a'), operator.ne, True),
    (SUTest_Simple('b'), SUTest_CompLarge('a'), operator.ge, False),
    (SUTest_Simple('b'), SUTest_CompLarge('a'), operator.gt, False),
    (SUTest_Simple('a'), '', operator.contains, True),
    (SUTest_Simple('abc'), 'a', operator.contains, True),
    (SUTest_Simple('abc'), 'b', operator.contains, True),
    (SUTest_Simple('abc'), 'c', operator.contains, True),
    (SUTest_Simple('abc'), 'ab', operator.contains, True),
    (SUTest_Simple('abc'), 'ac', operator.contains, False),
]


# Tests

@pytest.mark.simple
@pytest.mark.parametrize('tstr', ['a', 'ab', 'A', 'AB'])
def test_simpleunit_validate_true(tstr):
    """When passed to a SimpleUnit's ``validate`` method, the given
    test string (tstr) should result in a True value.
    """
    assert bool(SUTest_Simple.validate(tstr)) is True


@pytest.mark.simple
@pytest.mark.parametrize('tstr', ['', 'a ', 'a1'])
def test_simpleunit_validate_error(tstr):
    """When passed to a SimpleUnit's ``validate`` method, the given
    test string (tstr) should raise an InvalidCallNumberStringError.
    """
    with pytest.raises(e.InvalidCallNumberStringError):
        SUTest_Simple.validate(tstr)


@pytest.mark.simple
def test_simpleunit_as_str():
    """Casting a SimpleUnit as a string should return the ``for_print``
    value.
    """
    unit = SUTest_Simple('a')
    assert str(unit) == 'a[PR]'


@pytest.mark.simple
@pytest.mark.comparison
@pytest.mark.parametrize('val1, val2, op, expected', SIMPUNIT_CMP_PARAMS)
def test_simpleunit_comparisons(val1, val2, op, expected):
    """The given values, val1 and val2, should produce the expected
    truth value when compared via the given operator, op."""
    assert op(val1, val2) == expected


@pytest.mark.simple
@pytest.mark.parametrize('attribute, testvalue', [
    ('definition', 'derived definition'),
    ('is_separator', True),
    ('is_formatting', True),
    ('print_value', 'derived print value'),
    ('for_sort', lambda x: True),
    ('custom_attribute', 'custom derived attribute')
])
def test_simpleunit_derive_unit_attributes(attribute, testvalue):
    """Creating a new SimpleUnit using the ``derive`` method and
    specifying the given attribute (found on the Unit class) should
    result in an object attribute with the given testvalue. All
    other object attributes should be the same as the parent unit.
    """
    derived = SUTest_Simple.derive(**{attribute: testvalue})
    derived_unit = derived('a')
    original_unit = SUTest_Simple('a')
    for attr in test_obj_attributes:
        if attr == attribute:
            expected = testvalue
        else:
            expected = getattr(original_unit, attr)
        assert getattr(derived_unit, attr) == expected


@pytest.mark.simple
@pytest.mark.parametrize('attribute, testvalue', [
    ('min_length', 0),
    ('max_length', 5),
    ('base_description', 'derived description'),
    ('base_description_plural', 'derived description plural'),
    ('pre_description', 'derived pre_description'),
    ('post_description', 'derived post_description'),
])
def test_simpleunit_derive_template_attributes(attribute, testvalue):
    """Creating a new SimpleUnit using the ``derive`` method and
    specifying the given attribute (found on the SimpleTemplate object
    that is in the Unit's ``template`` attribute) should result in an
    attribute with the given testvalue on the object's ``template``.
    All other template attributes should be the same as the parent unit
    class.
    """
    derived = SUTest_Simple.derive(**{attribute: testvalue})
    derived_unit = derived('a')
    original_unit = SUTest_Simple('a')
    for attr in test_template_attributes:
        if attr == attribute:
            expected = testvalue
        else:
            expected = getattr(original_unit.template, attr)
        assert getattr(derived_unit.template, attr) == expected


@pytest.mark.simple
@pytest.mark.parametrize('attr_prefix, testvalue', [
    ('base', r'aa'),
    ('pre', r'a'),
    ('post', r'a'),
])
def test_simpleunit_derive_template_patterns(attr_prefix, testvalue):
    """Creating a new SimpleUnit using the ``derive`` method and
    specifying one of the *_pattern attributes (found on the object's
    ``template`` object) should result in an attribute with the given
    testvalue on the object's template. The corresponding *_description
    attribute, in addition, should become None. All other template
    attributes should be the same as the parent unit class.
    """
    attribute = '{}_pattern'.format(attr_prefix)
    attr_description = '{}_description'.format(attr_prefix)
    attr_desc_plural = '{}_description_plural'.format(attr_prefix)
    derived = SUTest_Simple.derive(**{attribute: testvalue})
    derived_unit = derived('aa')
    original_unit = SUTest_Simple('aa')
    for attr in test_template_attributes:
        if attr == attribute:
            expected = testvalue
        elif attr == attr_description or attr == attr_desc_plural:
            expected = None
        else:
            expected = getattr(original_unit.template, attr)
        assert getattr(derived_unit.template, attr) == expected


# CompoundUnit ********************************************************

# Fixtures, factories, and test data

alpha_utype = u.SimpleUnit.derive(base_pattern=r'[A-Za-z]', max_length=None)
digit_utype = u.SimpleUnit.derive(base_pattern=r'[0-9]', max_length=None)
pipe_utype = u.SimpleUnit.derive(base_pattern=r'\|', min_length=0,
                                 is_formatting=True)
dot_utype = u.SimpleUnit.derive(base_pattern=r'\.', min_length=0,
                                is_formatting=True)
dash_utype = u.SimpleUnit.derive(base_pattern=r'\-', min_length=0,
                                 is_formatting=True)
space_utype = u.SimpleUnit.derive(base_pattern=r' ', min_length=0,
                                  is_formatting=True)


class AlphaCustomForMethods(alpha_utype):

    options_defaults = u.SimpleUnit.options_defaults.copy()
    options_defaults.update({
        'print_value': '[PR]',
        'search_value': '[SE]',
        'sort_value': '[SO]'
    })

    def for_print(self):
        return '{}{}'.format(self._string, self.print_value)

    def for_search(self):
        return '{}{}'.format(self._string, self.search_value)

    def for_sort(self):
        return '{}{}'.format(self._string, self.sort_value)


class HideFormattingForSort(u.SimpleUnit):

    is_formatting = True

    def for_sort(self):
        return ''


pipehide_utype = HideFormattingForSort.derive(base_pattern=r'\|', min_length=0)
dothide_utype = HideFormattingForSort.derive(base_pattern=r'\.', min_length=0)
dashhide_utype = HideFormattingForSort.derive(base_pattern=r'\-', min_length=0)
spacehide_utype = HideFormattingForSort.derive(base_pattern=r' ', min_length=0)


class CUTest_Simple(u.CompoundUnit):

    template = t.CompoundTemplate(
        separator_type=pipe_utype,
        groups=[
            {'name': 'letter1', 'min': 0, 'max': None, 'type': alpha_utype,
             'inner_sep_type': dot_utype},
            {'name': 'digit', 'min': 0, 'max': None, 'type': digit_utype,
             'inner_sep_type': dot_utype},
            {'name': 'letter2', 'min': 0, 'max': None, 'type': alpha_utype,
             'inner_sep_type': dot_utype},

        ]
    )


class CUTest_Simple_SortHideFormatting(u.CompoundUnit):

    template = t.CompoundTemplate(
        separator_type=pipehide_utype,
        groups=[
            {'name': 'letter1', 'min': 0, 'max': None, 'type': alpha_utype,
             'inner_sep_type': dothide_utype},
            {'name': 'digit', 'min': 0, 'max': None, 'type': digit_utype,
             'inner_sep_type': dothide_utype},
            {'name': 'letter2', 'min': 0, 'max': None, 'type': alpha_utype,
             'inner_sep_type': dothide_utype},

        ]
    )


class CUTest_Compound_1GroupInnerSep(u.CompoundUnit):

    template = t.CompoundTemplate(
        separator_type=None,
        groups=[
            {'name': 'parts', 'min': 0, 'max': None,
             'type': CUTest_Simple, 'inner_sep_type': dash_utype}
        ]
    )


class CUTest_CustomForMethods(u.CompoundUnit):

    template = t.CompoundTemplate(
        separator_type=None,
        groups=[
            {'name': 'letter', 'min': 0, 'max': None,
             'type': AlphaCustomForMethods},
            {'name': 'digit', 'min': 0, 'max': None, 'type': digit_utype}
        ]
    )


class CUTest_ForCmpP1(u.CompoundUnit):

    template = t.CompoundTemplate(
        separator_type=dashhide_utype,
        groups=[
            {'name': 'letter1', 'min': 1, 'max': 1, 'type': alpha_utype},
            {'name': 'letter2', 'min': 1, 'max': 1, 'type': alpha_utype},
        ]
    )


class CUTest_ForCmpP2(u.CompoundUnit):

    template = t.CompoundTemplate(
        separator_type=dothide_utype,
        groups=[
            {'name': 'digit1', 'min': 1, 'max': 1, 'type': digit_utype},
            {'name': 'digit2', 'min': 1, 'max': 1, 'type': digit_utype},
        ]
    )


class CUTest_ForCmp(u.CompoundUnit):

    template = t.CompoundTemplate(
        separator_type=spacehide_utype,
        groups=[
            {'name': 'part1', 'min': 1, 'max': 1, 'type': CUTest_ForCmpP1},
            {'name': 'part2', 'min': 0, 'max': 1, 'type': CUTest_ForCmpP2},
            {'name': 'part3', 'min': 0, 'max': None,
             'possible_types': [dot_utype, pipe_utype, dash_utype]},
        ]
    )


COMPOUND_UNIT_DATA = {
    CUTest_Simple: {
        'valid': ['', 'a', 'a1', 'a1a', 'aaa', 'aa11aa', 'a|1|a', 'aa|11|aa',
                  'a|a', 'a.a|1.1|a.a'],
        'invalid': ['a1a1', 'a.1', 'a.|1', 'a.', 'a|', '|1', '.1', '|a', '.a'],
        'attribute': [
            ('a', [('letter1', 'a'),
                   ('digit', None),
                   ('letter2', None)]),
            ('aa', [('letter1', 'aa'),
                    ('digit', None),
                    ('letter2', None)]),
            ('a.a', [('letter1', 'a.a'),
                     ('letter1', ['a', 'a']),
                     ('digit', None),
                     ('letter2', None)]),
            ('a|1', [('letter1', 'a'),
                     ('digit', '1'),
                     ('letter2', None)]),
            ('a|a', [('letter1', 'a'),
                     ('digit', None),
                     ('letter2', 'a')]),
            ('a|1|a', [('letter1', 'a'),
                       ('digit', '1'),
                       ('letter2', 'a')]),
            ('a1a', [('letter1', 'a'),
                     ('digit', '1'),
                     ('letter2', 'a')]),
        ],
        'for_sort': [('a', 'a'), ('a.a', 'a.a'), ('a|a', 'a|a'),
                     ('a|1', 'a|1'), ('a|1|a', 'a|1|a'), ('aa', 'aa'),
                     ('a1a', 'a!1!a'), ('aa11aa', 'aa!11!aa'),
                     ('a.a|1.1|a.a', 'a.a|1.1|a.a')]
    },
    CUTest_Simple_SortHideFormatting: {
        'for_sort': [('a', 'a'), ('a.a', 'a!a'), ('a|a', 'a!a'),
                     ('a|1', 'a!1'), ('a|1|a', 'a!1!a'), ('aa', 'aa'),
                     ('a1a', 'a!1!a'), ('aa11aa', 'aa!11!aa'),
                     ('a.a|1.1|a.a', 'a!a!1!1!a!a')]
    },
    CUTest_Compound_1GroupInnerSep: {
        'valid': ['', 'a', 'a-a', 'aa-a', 'aa11|a-aa', 'a.a11|a-a1a-a'],
        'invalid': ['a-', 'a-|', '-a', '|-a'],
        'attribute': [
            ('a', [('parts', 'a')]),
            ('a-a', [
                ('parts', 'a-a'),
                ('parts', ['a', 'a']),
                ('parts', [
                    (('letter1', 'a'),
                     ('digit', None),
                     ('letter2', None)),
                    (('letter1', 'a'),
                     ('digit', None),
                     ('letter2', None))
                ])
            ]),
            ('a.a|1.1|a.a-b.b|2.2|b.b', [
                ('parts', 'a.a|1.1|a.a-b.b|2.2|b.b'),
                ('parts', ['a.a|1.1|a.a', 'b.b|2.2|b.b']),
                ('parts', [
                    (('letter1', 'a.a'),
                     ('letter1', ['a', 'a']),
                     ('digit', '1.1'),
                     ('digit', ['1', '1']),
                     ('letter2', 'a.a'),
                     ('letter2', ['a', 'a'])),
                    (('letter1', 'b.b'),
                     ('letter1', ['b', 'b']),
                     ('digit', '2.2'),
                     ('digit', ['2', '2']),
                     ('letter2', 'b.b'),
                     ('letter2', ['b', 'b']))
                ])
            ])
        ],
    }
}

COMPUNIT_VALID_PARAMS = generate_params(COMPOUND_UNIT_DATA, 'valid')
COMPUNIT_INVALID_PARAMS = generate_params(COMPOUND_UNIT_DATA, 'invalid')
COMPUNIT_ATTR_PARAMS = generate_params(COMPOUND_UNIT_DATA, 'attribute')
COMPUNIT_FOR_SORT_PARAMS = generate_params(COMPOUND_UNIT_DATA, 'for_sort')

COMPUNIT_CMP_PARAMS = [
    (CUTest_ForCmpP1('a-a'), CUTest_ForCmpP1('a-a'), operator.lt, False),
    (CUTest_ForCmpP1('a-a'), CUTest_ForCmpP1('a-a'), operator.le, True),
    (CUTest_ForCmpP1('a-a'), CUTest_ForCmpP1('a-a'), operator.eq, True),
    (CUTest_ForCmpP1('a-a'), CUTest_ForCmpP1('a-a'), operator.ne, False),
    (CUTest_ForCmpP1('a-a'), CUTest_ForCmpP1('a-a'), operator.ge, True),
    (CUTest_ForCmpP1('a-a'), CUTest_ForCmpP1('a-a'), operator.gt, False),
    (CUTest_ForCmpP1('a-a'), CUTest_ForCmpP1('a-a'), operator.contains, True),
    (CUTest_ForCmpP1('a-a'), CUTest_ForCmpP1('aa'), operator.lt, False),
    (CUTest_ForCmpP1('a-a'), CUTest_ForCmpP1('aa'), operator.le, True),
    (CUTest_ForCmpP1('a-a'), CUTest_ForCmpP1('aa'), operator.eq, True),
    (CUTest_ForCmpP1('a-a'), CUTest_ForCmpP1('aa'), operator.ne, False),
    (CUTest_ForCmpP1('a-a'), CUTest_ForCmpP1('aa'), operator.ge, True),
    (CUTest_ForCmpP1('a-a'), CUTest_ForCmpP1('aa'), operator.gt, False),
    (CUTest_ForCmpP1('a-a'), CUTest_ForCmpP1('aa'), operator.contains, True),
    (CUTest_ForCmpP1('a-a'), CUTest_ForCmpP1('a-b'), operator.lt, True),
    (CUTest_ForCmpP1('a-a'), CUTest_ForCmpP1('a-b'), operator.le, True),
    (CUTest_ForCmpP1('a-a'), CUTest_ForCmpP1('a-b'), operator.eq, False),
    (CUTest_ForCmpP1('a-a'), CUTest_ForCmpP1('a-b'), operator.ne, True),
    (CUTest_ForCmpP1('a-a'), CUTest_ForCmpP1('a-b'), operator.ge, False),
    (CUTest_ForCmpP1('a-a'), CUTest_ForCmpP1('a-b'), operator.gt, False),
    (CUTest_ForCmpP1('a-a'), CUTest_ForCmpP1('a-b'), operator.contains, False),
    (CUTest_ForCmp('a-a 1.1'), CUTest_ForCmp('a-a 1.2'), operator.lt, True),
    (CUTest_ForCmp('a-a 1.1'), CUTest_ForCmp('a-a 1.2'), operator.le, True),
    (CUTest_ForCmp('a-a 1.1'), CUTest_ForCmp('a-a 1.2'), operator.eq, False),
    (CUTest_ForCmp('a-a 1.1'), CUTest_ForCmp('a-a 1.2'), operator.ne, True),
    (CUTest_ForCmp('a-a 1.1'), CUTest_ForCmp('a-a 1.2'), operator.ge, False),
    (CUTest_ForCmp('a-a 1.1'), CUTest_ForCmp('a-a 1.2'), operator.gt, False),
    (CUTest_ForCmp('a-a 1.1'), CUTest_ForCmpP1('a-b'), operator.lt, True),
    (CUTest_ForCmp('a-a 1.1'), CUTest_ForCmpP1('a-b'), operator.le, True),
    (CUTest_ForCmp('a-a 1.1'), CUTest_ForCmpP1('a-b'), operator.eq, False),
    (CUTest_ForCmp('a-a 1.1'), CUTest_ForCmpP1('a-b'), operator.ne, True),
    (CUTest_ForCmp('a-a 1.1'), CUTest_ForCmpP1('a-b'), operator.ge, False),
    (CUTest_ForCmp('a-a 1.1'), CUTest_ForCmpP1('a-b'), operator.gt, False),
    (CUTest_ForCmp('a-a 1.1'), CUTest_ForCmpP1('a-a'), operator.contains,
     True),
    (CUTest_ForCmp('a-a 1.1'), alpha_utype, operator.contains, True),
    (CUTest_ForCmp('a-a 1.1'), digit_utype, operator.contains, True),
    (CUTest_ForCmp('a-a 1.1'), CUTest_ForCmp, operator.contains, True),
    (CUTest_ForCmp('a-a 1.1'), CUTest_ForCmpP1, operator.contains, True),
    (CUTest_ForCmp('a-a 1.1'), CUTest_ForCmpP2, operator.contains, True),
    (CUTest_ForCmp('a-a 1.1'), dashhide_utype, operator.contains, True),
    (CUTest_ForCmp('a-a 1.1'), dothide_utype, operator.contains, True),
    (CUTest_ForCmp('a-a 1.1'), spacehide_utype, operator.contains, True),
    (CUTest_ForCmp('a-a 1.1'), dash_utype, operator.contains, False),
    (CUTest_ForCmp('a-a 1.1'), dot_utype, operator.contains, False),
    (CUTest_ForCmp('a-a 1.1'), pipe_utype, operator.contains, False),
    (CUTest_ForCmp('a-a 1.1|'), pipe_utype, operator.contains, True),
    (CUTest_ForCmp('a-a 1.1|'), CUTest_ForCmpP1('a-a'), operator.contains,
     True),
    (CUTest_ForCmp('a-a 1.1|'), CUTest_ForCmpP1('a-b'), operator.contains,
     False),
    (CUTest_ForCmp('a-a 1.1|'), CUTest_ForCmpP2('1.1'), operator.contains,
     True),
    (CUTest_ForCmp('a-a 1.1|'), CUTest_ForCmpP2('1.2'), operator.contains,
     False),
    (CUTest_ForCmp('a-a 1.1|'), alpha_utype('a'), operator.contains, True),
    (CUTest_ForCmp('a-a 1.1|'), alpha_utype('b'), operator.contains, False),
    (CUTest_ForCmp('a-a 1.1|'), digit_utype('1'), operator.contains, True),
    (CUTest_ForCmp('a-a 1.1|'), digit_utype('2'), operator.contains, False),
    (CUTest_ForCmp('a-a 1.1|'), dothide_utype('.'), operator.contains, True),
]


# Tests

@pytest.mark.compound
@pytest.mark.parametrize('unit_type, tstr', COMPUNIT_VALID_PARAMS)
def test_compoundunit_validate_true(unit_type, tstr):
    """When passed to the given unit_type's ``validate`` method, the
    given test string (tstr) should result in a True value.
    """
    assert bool(unit_type.validate(tstr)) is True


@pytest.mark.compound
@pytest.mark.parametrize('unit_type, tstr', COMPUNIT_INVALID_PARAMS)
def test_compoundunit_validate_error(unit_type, tstr):
    """When passed to the given unit_type's ``validate`` method, the
    given test string (tstr) should raise an
    InvalidCallNumberStringError.
    """
    with pytest.raises(e.InvalidCallNumberStringError):
        unit_type.validate(tstr)


@pytest.mark.compound
@pytest.mark.parametrize('unit_type, tstr, expected', COMPUNIT_ATTR_PARAMS)
def test_compoundunit_attributes(unit_type, tstr, expected):
    """When the given unit_type is instantiated using the given test
    string (tstr), the resulting object should have attributes that
    follow from what's present in ``expected.``
    """
    def check_attributes(unit, attrlist):
        for attr, val in attrlist:
            if isinstance(val, tuple):
                subunit = getattr(unit, attr)
                check_attributes(subunit, val)
            elif isinstance(val, list):
                if isinstance(val[0], str):
                    valstrings = [str(v) for v in val]
                    assert [str(v) for v in getattr(unit, attr)] == valstrings
                elif isinstance(val[0], tuple):
                    multiunit = getattr(unit, attr)
                    for i, subattrlist in enumerate(val):
                        subunit = multiunit[i]
                        check_attributes(subunit, subattrlist)
            else:
                assert str(getattr(unit, attr)) == str(val)

    unit = unit_type(tstr)
    check_attributes(unit, expected)


@pytest.mark.compound
@pytest.mark.comparison
@pytest.mark.parametrize('val1, val2, op, expected', COMPUNIT_CMP_PARAMS)
def test_compoundunit_comparisons(val1, val2, op, expected):
    """The given values, val1 and val2, should produce the expected
    truth value when compared via the given operator, op."""
    assert op(val1, val2) == expected


@pytest.mark.compound
@pytest.mark.parametrize('unit_type, tstr, expected', COMPUNIT_FOR_SORT_PARAMS)
def test_compoundunit_for_sort(unit_type, tstr, expected):
    """When the given unit_type is instantiated using the given test
    string (tstr), calling the ``for_sort`` method on the resulting
    object should produce the ``expected`` value.
    """
    unit = unit_type(tstr)
    assert unit.for_sort() == expected


@pytest.mark.compound
def test_compoundunit_custom_for_print():
    """When the ``for_print`` method is called on a
    CUTest_CustomForMethods object, the ``letter`` grouping's custom
    ``for_print`` method should be used to formulate the return value.
    """
    unit = CUTest_CustomForMethods('aa11')
    assert unit.for_print() == 'aa[PR]11'


@pytest.mark.compound
def test_compoundunit_custom_for_search():
    """When the ``for_search`` method is called on a
    CUTest_CustomForMethods object, the ``letter`` grouping's custom
    ``for_search`` method should be used to formulate the return value.
    """
    unit = CUTest_CustomForMethods('aa11')
    assert unit.for_search() == 'aa[SE]11'


@pytest.mark.compound
def test_compoundunit_custom_for_sort():
    """When the ``for_sort`` method is called on a
    CUTest_CustomForMethods object, the ``letter`` grouping's custom
    ``for_sort`` method should be used to formulate the return value.
    """
    unit = CUTest_CustomForMethods('aa11')
    assert unit.for_sort() == 'aa[SO]!11'
