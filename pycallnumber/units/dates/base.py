"""Model various types of date strings as call number parts.

This contains some base classes and a mixin to allow dates to be
represented as Units more easily.
"""


from __future__ import unicode_literals

from builtins import str
from builtins import object
from pycallnumber.template import CompoundTemplate
from pycallnumber.unit import SimpleUnit
from pycallnumber.units.simple import Alphabetic, Numeric
from pycallnumber.units.compound import AlphaNumeric, AlphaNumericSymbol


class DatePartMixin(object):

    category = None  # 'year' or 'month' or 'day'

    @property
    def value(self):
        try:
            return super(DatePartMixin, self).value
        except AttributeError:
            raise NotImplementedError()

    def for_sort(self):
        numeric_opts = Numeric.filter_valid_useropts(self.options)
        return Numeric(str(self.value), **numeric_opts).for_sort()


class AlphaDatePart(DatePartMixin, Alphabetic):

    options_defaults = AlphaNumeric.options_defaults.copy()


class NumericDatePart(DatePartMixin, Numeric):
    pass


class CompoundDatePart(DatePartMixin, AlphaNumericSymbol):
    pass


class BaseDate(AlphaNumericSymbol):

    template = CompoundTemplate(
        separator_type=None,
        groups=[
            {'min': 1, 'max': 1, 'name': 'prop_month', 'type': SimpleUnit},
            {'min': 0, 'max': 1, 'name': 'prop_day', 'type': SimpleUnit},
            {'min': 1, 'max': 1, 'name': 'prop_year', 'type': SimpleUnit}
        ]
    )

    def _get_date_prop(self, prop):
        prop = 'prop_{}'.format(prop)
        if hasattr(self, prop):
            return getattr(self, prop)
        else:
            return None

    @property
    def year(self):
        return self._get_date_prop('year')

    @property
    def month(self):
        return self._get_date_prop('month')

    @property
    def day(self):
        return self._get_date_prop('day')

    @property
    def normalized_datestring(self):
        if not hasattr(self, '_normalized_datestring'):
            parts = []
            for category in ['year', 'month', 'day']:
                part = getattr(self, category) or 0
                if part:
                    part = part.value
                parts.append(part)
            self._normalized_datestring = '{:04d}{:02d}{:02d}'.format(*parts)
        return self._normalized_datestring

    def for_sort(self):
        numeric_opts = Numeric.filter_valid_useropts(self.options)
        return Numeric(self.normalized_datestring, **numeric_opts).for_sort()
