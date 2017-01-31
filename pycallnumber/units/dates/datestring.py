"""Represent (almost) any kind of date string as a call number part."""


from __future__ import unicode_literals
from __future__ import absolute_import

from pycallnumber.template import CompoundTemplate
from pycallnumber.units.simple import Formatting, DEFAULT_SEPARATOR_TYPE
from .base import BaseDate
from .parts import Year, Month, Day


Separator = Formatting.derive(
    classname='Separator',
    short_description=('a space, forward slash, period, hyphen, or comma '
                       'plus space'),
    min_length=1,
    max_length=1,
    base_pattern=r'(?:[\s.\-/]|,\s?)'
)


DateMDY = BaseDate.derive(
    classname='DateMDY',
    separator_type=Separator,
    short_description='a date with the month first, day, and then year',
    groups=[
        {'min': 1, 'max': 1, 'name': 'prop_month', 'type': Month},
        {'min': 1, 'max': 1, 'name': 'prop_day', 'type': Day},
        {'min': 1, 'max': 1, 'name': 'prop_year', 'type': Year}
    ],
)

DateDMY = BaseDate.derive(
    classname='DateDMY',
    separator_type=Separator,
    short_description='a date with the day first, month, and then year',
    groups=[
        {'min': 1, 'max': 1, 'name': 'prop_day', 'type': Day},
        {'min': 1, 'max': 1, 'name': 'prop_month', 'type': Month},
        {'min': 1, 'max': 1, 'name': 'prop_year', 'type': Year}
    ]
)

DateYMD = BaseDate.derive(
    classname='DateYMD',
    separator_type=Separator,
    short_description='a date with the year first, month, and then day',
    groups=[
        {'min': 1, 'max': 1, 'name': 'prop_year', 'type': Year},
        {'min': 1, 'max': 1, 'name': 'prop_month', 'type': Month},
        {'min': 1, 'max': 1, 'name': 'prop_day', 'type': Day},
    ]
)

DateYDM = BaseDate.derive(
    classname='DateYMD',
    separator_type=Separator,
    short_description='a date with the year first, day, and then month',
    groups=[
        {'min': 1, 'max': 1, 'name': 'prop_year', 'type': Year},
        {'min': 1, 'max': 1, 'name': 'prop_day', 'type': Day},
        {'min': 1, 'max': 1, 'name': 'prop_month', 'type': Month},
    ]
)

DateMY = BaseDate.derive(
    classname='DateMY',
    separator_type=Separator,
    short_description='a date with the month then the year; no day',
    groups=[
        {'min': 1, 'max': 1, 'name': 'prop_month', 'type': Month},
        {'min': 1, 'max': 1, 'name': 'prop_year', 'type': Year},
    ]
)

DateYM = BaseDate.derive(
    classname='DateYM',
    separator_type=Separator,
    short_description='a date with the year then the month; no day',
    groups=[
        {'min': 1, 'max': 1, 'name': 'prop_year', 'type': Year},
        {'min': 1, 'max': 1, 'name': 'prop_month', 'type': Month},
    ]
)


class DateString(BaseDate):

    definition = 'any string that represents a date, in a non-specific format'

    template = CompoundTemplate(
        separator_type=DEFAULT_SEPARATOR_TYPE,
        groups=[
            {'min': 1, 'max': 1, 'name': 'date',
             'possible_types': [DateMDY, DateDMY, DateYMD, DateYDM,
                                DateMY, DateYM, Month.AlphaMonthLong,
                                Month.AbbreviatedMonth]}
        ]
    )

    def _get_date_prop(self, prop):
        if hasattr(self.date, prop):
            return getattr(self.date, prop)
        elif self.date.category == prop:
            return self.date
        else:
            return None
