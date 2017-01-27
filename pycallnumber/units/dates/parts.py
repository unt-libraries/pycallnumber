"""Model various types of date strings as call number parts.

This contains Unit implementations for various pieces of dates.
"""


from __future__ import unicode_literals
from __future__ import absolute_import
from builtins import str
from builtins import range
from datetime import datetime

from pycallnumber.template import SimpleTemplate, CompoundTemplate
from pycallnumber.units.simple import Formatting
from pycallnumber.units.numbers import OrdinalNumber
from .base import AlphaDatePart, NumericDatePart, CompoundDatePart


class Year(NumericDatePart):

    prop_year = datetime.now().year + 6
    _year_pattern = r'|'.join(str(i) for i in range(2000, prop_year))
    category = 'year'

    template = SimpleTemplate(
        min_length=1,
        max_length=1,
        base_description=('2-digit year or 4-digit year, where a 2-digit '
                          'year between 00 and this year + 1 is assumed to be '
                          'a 21st century year, and 4-digit years between '
                          '1000 and this year + 5 are valid'),
        base_pattern=r'(?:1[0-9]{{3}}|{}|[0-9]{{2}})'.format(_year_pattern),
        post_pattern=r'(?![0-9])'
    )

    @classmethod
    def string_to_value(self, cnstr):
        if len(cnstr) == 2:
            next_year = str(datetime.now().year + 1)[-2:]
            if int(cnstr) > int(next_year):
                value = int('19{}'.format(cnstr))
            else:
                value = int('20{}'.format(cnstr))
        else:
            value = int(cnstr)
        return value


class AlphaMonth(AlphaDatePart):

    definition = 'an alphabetic representation of a month of the year'
    numeric_zfill = 2
    months = {'january': 1}
    category = 'month'

    template = SimpleTemplate(
        min_length=1,
        max_length=1,
        post_pattern=r'(?![A-Za-z])',
        post_description='anything but a letter',
    )

    @classmethod
    def derive(cls, **attr):
        months = list(attr['months'].keys())
        months.sort(key=lambda x: int(attr['months'][x]))
        base_pattern = ''
        for month in months:
            first_upper_lower = r'[{}{}]'.format(month[0].lower(),
                                                 month[0].upper())
            month_lower = r'{}{}'.format(first_upper_lower,
                                         month[1:].lower())
            base_pattern = r'{}{}|{}|'.format(base_pattern, month_lower,
                                              month.upper())
        base_pattern = r'(?:{})'.format(base_pattern.strip('|'))
        attr['base_pattern'] = base_pattern
        attr['short_description'] = ('one of the following strings -- {} -- '
                                     'which is all lower case, all upper '
                                     'case, or has just the first letter '
                                     'capitalized').format(', '.join(months))
        return super(AlphaMonth, cls).derive(**attr)

    @property
    def value(self):
        return type(self).months[self._string.lower()]


class Month(CompoundDatePart):

    short_description = 'a numeric or alphabetic month'
    category = 'month'

    Period = Formatting.derive(
        classname='Period',
        short_description='a period',
        min_length=1,
        max_length=1,
        base_pattern=r'\.'
    )

    NumericMonth = NumericDatePart.derive(
        classname='NumericMonth',
        short_description='a numeric month, 1 to 12',
        min_length=1,
        max_length=1,
        base_pattern=r'(?:1[0-2]|0?[1-9])',
        post_pattern=r'(?![0-9])',
        category='month'
    )

    AlphaMonthLong = AlphaMonth.derive(
        classname='AlphaMonthLong',
        months={
            'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5,
            'june': 6, 'july': 7, 'august': 8, 'september': 9, 'october': 10,
            'november': 11, 'december': 12, 'winter': 1, 'spring': 3,
            'summer': 6, 'fall': 9
        },
        category='month'
    )

    AlphaMonthShort = AlphaMonth.derive(
        classname='AlphaMonthShort',
        months={
            'jan': 1, 'feb': 2, 'febr': 2, 'mar': 3, 'apr': 4, 'jun': 6,
            'jul': 7, 'aug': 8, 'sep': 9, 'sept': 9, 'oct': 10, 'nov': 11,
            'dec': 12, 'win': 1, 'wint': 1, 'spr': 3, 'sum': 6, 'summ': 6
        },
        category='month'
    )

    AbbreviatedMonth = CompoundDatePart.derive(
        classname='AbbreviatedMonth',
        short_description='a month abbreviation and optional period',
        separator_type=None,
        groups=[
            {'min': 1, 'max': 1, 'name': 'alphamonth',
             'type': AlphaMonthShort},
            {'min': 0, 'max': 1, 'name': 'period', 'type': Period}
        ],
        category='month',
        value=property(lambda x: x.alphamonth.value)
    )

    template = CompoundTemplate(
        groups=[
            {'min': 1, 'max': 1, 'name': 'fullmonth',
             'possible_types': [NumericMonth, AlphaMonthLong,
                                AbbreviatedMonth]}
        ]
    )

    @property
    def value(self):
        return self.fullmonth.value


class Day(CompoundDatePart):

    short_description = ('cardinal or ordinal number, from 1 to 31, '
                         'representing the day of the month')
    category = 'day'

    NumericDay = NumericDatePart.derive(
        classname='NumericDay',
        short_description='numeric day of the month, 1 to 31',
        min_length=1,
        max_length=1,
        base_pattern=r'(?:[1-2][0-9]|3[0-1]|0?[1-9])',
        category='day'
    )

    template = CompoundTemplate(
        groups=[
            {'min': 1, 'max': 1, 'name': 'wholenumber', 'type': NumericDay},
            {'min': 0, 'max': 1, 'name': 'suffix',
             'type': OrdinalNumber.OrdinalSuffix}
        ]
    )

    @property
    def value(self):
        return self.wholenumber.value
