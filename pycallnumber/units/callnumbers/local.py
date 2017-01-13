"""Work with any string as a local call number Unit type."""

from __future__ import unicode_literals

from pycallnumber.template import CompoundTemplate
from pycallnumber.units.simple import Alphabetic, Formatting,\
                                      DEFAULT_SEPARATOR_TYPE
from pycallnumber.units.compound import AlphaNumericSymbol
from pycallnumber.units.numbers import Number


class Local(AlphaNumericSymbol):

    definition = 'a local call number with a non-specific structure'

    template = CompoundTemplate(
        short_description=AlphaNumericSymbol.template.short_description,
        groups=[
            {'name': 'parts', 'min': 1, 'max': None,
             'inner_sep_type': DEFAULT_SEPARATOR_TYPE,
             'possible_types': [Alphabetic, Number, Formatting]}
        ]
    )
