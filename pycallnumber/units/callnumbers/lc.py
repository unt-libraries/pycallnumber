"""Work with Library of Congress call numbers as Units."""

from __future__ import unicode_literals
from __future__ import absolute_import

from pycallnumber.template import CompoundTemplate
from pycallnumber.units.simple import Alphabetic, Formatting,\
                                      DEFAULT_SEPARATOR_TYPE
from pycallnumber.units.compound import AlphaNumericSymbol
from pycallnumber.units.numbers import Number
from .parts import Cutter, Edition, Item


class LcClass(AlphaNumericSymbol):

    short_description = ('a string with 1 to 3 letters followed by a number '
                         'with up to 4 digits and optionally up to 4 '
                         'decimal places; the alphabetic and numeric parts '
                         'may optionally be separated by whitespace')

    ClassLetters = Alphabetic.derive(
        classname='LcClass.ClassLetters',
        min_length=1,
        max_length=3
    )

    ClassNumber = Number.derive(
        classname='LcClass.ClassNumber',
        definition=('A number between 1 and 9999.9999, with 0 to 4 decimal '
                    'places'),
        max_val=9999.9999,
        max_decimal_places=4,
        thousands=None
    )

    template = CompoundTemplate(
        separator_type=DEFAULT_SEPARATOR_TYPE,
        groups=[
            {'min': 1, 'max': 1, 'name': 'letters', 'type': ClassLetters},
            {'min': 1, 'max': 1, 'name': 'number', 'type': ClassNumber}
        ]
    )


CutterPeriod = Formatting.derive(
    classname='CutterPeriod',
    short_description=('the whitespace and/or period before the Cutters'),
    min_length=1,
    max_length=1,
    base_pattern=r'(?:\s*\.?)',
)


class LC(AlphaNumericSymbol):

    definition = 'a Library of Congress call number'

    Space = DEFAULT_SEPARATOR_TYPE.derive(
        min_length=1
    )

    template = CompoundTemplate(
        separator_type=DEFAULT_SEPARATOR_TYPE,
        groups=[
            {'name': 'classification', 'min': 1, 'max': 1, 'type': LcClass},
            {'name': 'period', 'min': 0, 'max': 1, 'type': CutterPeriod,
             'is_separator': True},
            {'name': 'cutters', 'min': 1, 'max': None,
             'inner_sep_type': DEFAULT_SEPARATOR_TYPE, 'type': Cutter},
            {'name': 'edition', 'min': 0, 'max': 1, 'type': Edition},
            {'name': 'space', 'min': 1, 'max': 1, 'type': Space,
             'is_separator': True},
            {'name': 'item', 'min': 0, 'max': 1, 'type': Item}
        ]
    )
