"""Work with Dewey call numbers as Units."""

from __future__ import unicode_literals
from __future__ import absolute_import

from pycallnumber.template import CompoundTemplate
from pycallnumber.units.simple import Alphabetic, DEFAULT_SEPARATOR_TYPE
from pycallnumber.units.compound import AlphaNumericSymbol
from pycallnumber.units.numbers import Number
from .parts import Cutter, Edition, Item


DeweyClass = Number.derive(
    classname='DeweyClass',
    short_description=('a number between 0 and 999 followed by an '
                       'optional decimal, up to 8 decimal places'),
    max_val=999.99999999,
    max_decimal_places=8
)

DeweyCutter = Cutter.derive(
    classname='DeweyCutter',
    short_description=('a string with 1 to 3 letters, followed by a '
                       'number, followed by an optional alphabetic '
                       'workmark; no whitespace between any of these '
                       'components'),
    separator_type=None,
    groups=[
        {'min': 1, 'max': 1, 'name': 'letters', 'type': Cutter.Letters},
        {'min': 1, 'max': 1, 'name': 'number', 'type': Cutter.StringNumber},
        {'min': 0, 'max': 1, 'name': 'workmark', 'type': Alphabetic}
    ]
)


class Dewey(AlphaNumericSymbol):

    definition = ('a Dewey Decimal call number')

    template = CompoundTemplate(
        separator_type=DEFAULT_SEPARATOR_TYPE,
        groups=[
            {'name': 'classification', 'min': 1, 'max': 1, 'type': DeweyClass},
            {'name': 'cutters', 'min': 1, 'max': 2,
             'inner_sep_type': DEFAULT_SEPARATOR_TYPE, 'type': DeweyCutter},
            {'name': 'edition', 'min': 0, 'max': 1, 'type': Edition},
            {'name': 'item', 'min': 0, 'max': 1, 'type': Item}
        ]
    )
