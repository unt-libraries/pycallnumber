"""Work with structures commonly found in many call number types."""

from __future__ import unicode_literals

from pycallnumber.template import CompoundTemplate
from pycallnumber.unit import CompoundUnit
from pycallnumber.units.simple import Alphabetic, Numeric, Formatting,\
                                      DEFAULT_SEPARATOR_TYPE
from pycallnumber.units.compound import AlphaNumeric, AlphaNumericSymbol
from pycallnumber.units.numbers import Number, OrdinalNumber
from pycallnumber.units.dates.datestring import DateString


class Cutter(AlphaNumericSymbol):

    definition = ('a compact alphanumeric code used to arrange things '
                  'alphabetically')

    Letters = Alphabetic.derive(
        classname='Cutter.Letters',
        short_description='1 to 3 letters',
        min_length=1,
        max_length=3
    )

    StringNumber = Numeric.derive(
        classname='Cutter.StringNumber',
        short_description='a number that sorts as a decimal',
        max_val=.99999999
    )

    template = CompoundTemplate(
        short_description=('a string with 1 to 3 letters followed by a '
                           'number; the alphabetic and numeric portions '
                           'can be separated by optional whitespace'),
        separator_type=DEFAULT_SEPARATOR_TYPE,
        groups=[
            {'name': 'letters', 'min': 1, 'max': 1, 'type': Letters},
            {'name': 'number', 'min': 1, 'max': 1, 'type': StringNumber}
        ]
    )


class Edition(AlphaNumeric):

    definition = 'information identifying the edition of an item'

    Year = Numeric.derive(
        classname='Edition.Year',
        min_length=4,
        max_length=4
    )

    template = CompoundTemplate(
        short_description=('a 4-digit year, optionally followed by one or '
                           'more letters (no whitespace between them)'),
        separator_type=None,
        groups=[
            {'min': 1, 'max': 1, 'name': 'year', 'type': Year},
            {'min': 0, 'max': 1, 'name': 'letters', 'type': Alphabetic}
        ]
    )


class Item(AlphaNumericSymbol):

    definition = ('information such as volume number, copy number, opus '
                  'number, etc., that may be included at the end of a call '
                  'number to help further differentiate an item from others '
                  'with the same call number')

    Separator = Formatting.derive(
        min_length=1,
        max_length=None
    )

    FormattingNoSpace = Formatting.derive(
        classname='Item.FormattingNoSpace',
        short_description='any non-alphanumeric, non-whitespace character',
        min_length=1,
        max_length=None,
        base_pattern=r'[^A-Za-z0-9\s]',
        use_formatting_in_sort=False,
        use_formatting_in_search=False
    )

    SpaceOrPeriod = Formatting.derive(
        classname='Item.SpaceOrPeriod',
        short_description='a period followed by optional whitespace',
        min_length=1,
        max_length=1,
        base_pattern=r'(?:(?:\.|\s)\s*)'
    )

    Space = Formatting.derive(
        classname='Item.Space',
        short_description='whitespace',
        min_length=1,
        max_length=1,
        base_pattern=r'\s'
    )

    AnythingButSpace = AlphaNumericSymbol.derive(
        classname='Item.AnythingButSpace',
        short_description=('any combination of letters, symbols, and numbers '
                           'with no whitespace'),
        groups=[
            {'min': 1, 'max': None, 'name': 'parts', 'inner_sep_type': None,
             'possible_types': [Alphabetic, Numeric, FormattingNoSpace]}
        ]
    )

    Label = Alphabetic.derive(
        classname='Item.Label',
        for_sort=lambda x: '',
        for_search=lambda x: ''
    )

    IdString = AlphaNumericSymbol.derive(
        classname='Item.IdString',
        short_description=('a string with at least one number; can have any '
                           'characters except whitespace'),
        separator_type=None,
        groups=[
            {'min': 0, 'max': None, 'name': 'pre_number',
             'inner_sep_type': None,
             'possible_types': [Alphabetic, FormattingNoSpace]},
            {'min': 1, 'max': 1, 'name': 'first_number', 'type': Number},
            {'min': 0, 'max': None, 'name': 'everything_else',
             'inner_sep_type': None,
             'possible_types': [Alphabetic, Number, FormattingNoSpace]}
        ]
    )

    LabelThenNumber = AlphaNumericSymbol.derive(
        classname='Item.LabelThenNumber',
        short_description=('a string with a one-word label (which can contain '
                           'formatting), followed by a period and/or '
                           'whitespace, followed by one or more numbers (and '
                           'possibly letters and formatting), such as '
                           '\'Op. 1\', \'volume 1a\', or \'no. A-1\'; when '
                           'sorting, the label is ignored so that, e.g., '
                           '\'Volume 1\' sorts before \'vol 2\''),
        separator_type=SpaceOrPeriod,
        groups=[
            {'min': 0, 'max': None, 'name': 'label', 'inner_sep_type': None,
             'possible_types': [Label, FormattingNoSpace]},
            {'min': 1, 'max': 1, 'name': 'number', 'type': IdString},
        ],
        for_sort=lambda x: '{}{}'.format(CompoundUnit.sort_break,
                                         AlphaNumericSymbol.for_sort(x))
    )

    NumberThenLabel = AlphaNumericSymbol.derive(
        classname='Item.NumberThenLabel',
        short_description=('a string with an ordinal number and then a one-'
                           'word label, like \'101st Congress\' or \'2nd '
                           'vol.\'; when sorting, the label is ignored so '
                           'that, e.g., \'1st Congress\' sorts before \'2nd '
                           'CONG.\''),
        separator_type=Space,
        groups=[
            {'min': 1, 'max': 1, 'name': 'number', 'type': OrdinalNumber},
            {'min': 1, 'max': 1, 'name': 'label', 'type': Label}
        ],
        for_sort=lambda x: '{}{}'.format(CompoundUnit.sort_break,
                                         AlphaNumericSymbol.for_sort(x))
    )

    template = CompoundTemplate(
        short_description=('a string (any string) that gets parsed into '
                           'groups of labeled numbers and other groups of '
                           'words, symbols, and dates, where labels are '
                           'ignored for sorting; \'Volume 1 Copy 1\' sorts '
                           'before \'v. 1 c. 2\', which sorts before '
                           '\'VOL 1 CP 2 SUPP\'; dates are normalized to '
                           'YYYYMMDD format for sorting'),
        groups=[
            {'min': 1, 'max': None, 'name': 'parts',
             'inner_sep_type': Separator,
             'possible_types': [DateString, NumberThenLabel,
                                LabelThenNumber, AnythingButSpace]}
        ]
    )
