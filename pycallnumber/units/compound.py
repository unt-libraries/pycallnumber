"""Represent general types of compound call numbers and parts."""


from __future__ import unicode_literals
from __future__ import absolute_import

from pycallnumber.template import CompoundTemplate
from pycallnumber.unit import CompoundUnit
from .simple import Alphabetic, Numeric, Formatting, DEFAULT_SEPARATOR_TYPE


class AlphaNumeric(CompoundUnit):

    options_defaults = Alphabetic.options_defaults.copy()
    options_defaults.update(Numeric.options_defaults)

    template = CompoundTemplate(
        separator_type=None,
        groups=[
            {'name': 'parts', 'min': 1, 'max': None,
             'possible_types': [Alphabetic, Numeric]}
        ]
    )


class AlphaSymbol(CompoundUnit):

    options_defaults = Alphabetic.options_defaults.copy()
    options_defaults.update(Formatting.options_defaults)

    template = CompoundTemplate(
        separator_type=DEFAULT_SEPARATOR_TYPE,
        groups=[
            {'name': 'parts', 'min': 1, 'max': None,
             'possible_types': [Alphabetic, Formatting]}
        ]
    )


class NumericSymbol(CompoundUnit):

    options_defaults = Numeric.options_defaults.copy()
    options_defaults.update(Formatting.options_defaults)

    template = CompoundTemplate(
        separator_type=DEFAULT_SEPARATOR_TYPE,
        groups=[
            {'name': 'parts', 'min': 1, 'max': None,
             'possible_types': [Numeric, Formatting]}
        ]
    )


class AlphaNumericSymbol(CompoundUnit):

    options_defaults = AlphaNumeric.options_defaults.copy()
    options_defaults.update(Formatting.options_defaults)

    template = CompoundTemplate(
        separator_type=DEFAULT_SEPARATOR_TYPE,
        groups=[
            {'name': 'parts', 'min': 1, 'max': None,
             'possible_types': [Alphabetic, Numeric, Formatting]}
        ]
    )
