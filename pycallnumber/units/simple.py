"""Represent the most basic types of call number parts."""

from __future__ import unicode_literals
from builtins import str
import decimal
import math

from pycallnumber import settings
from pycallnumber.template import SimpleTemplate
from pycallnumber.unit import SimpleUnit
from pycallnumber.exceptions import InvalidCallNumberStringError, SettingsError
from pycallnumber import utils as u


class Alphabetic(SimpleUnit):

    options_defaults = SimpleUnit.options_defaults.copy()
    options_defaults.update({
        'display_case': settings.DEFAULT_DISPLAY_CASE,
        'search_case': settings.DEFAULT_SEARCH_CASE,
        'sort_case': settings.DEFAULT_SORT_CASE
    })
    is_alphabetic = True
    template = SimpleTemplate(
        min_length=1,
        max_length=None,
        base_pattern=r'[A-Za-z]',
        base_description='letter'
    )

    def _get_cased_string(self, case):
        if case == 'lower':
            return self._string.lower()
        elif case == 'upper':
            return self._string.upper()
        else:
            return self._string

    def for_sort(self):
        if self._string == '':
            return ' '
        else:
            return self._get_cased_string(self.sort_case)

    def for_search(self):
        return self._get_cased_string(self.search_case)

    def for_print(self):
        return self._get_cased_string(self.display_case)


class Numeric(SimpleUnit):

    options_defaults = SimpleUnit.options_defaults.copy()
    max_numeric_zfill = settings.DEFAULT_MAX_NUMERIC_ZFILL
    numeric_zfill = max_numeric_zfill
    min_val = 0
    max_val = int(math.pow(10, max_numeric_zfill) - 1)
    is_numeric = True
    min_interval = 1
    template = SimpleTemplate(
        min_length=1,
        max_length=None,
        base_pattern=r'\d',
        base_description='digit'
    )

    @classmethod
    def validate(cls, cnstr, instance_options=None):
        validate_result = super(Numeric, cls).validate(cnstr, instance_options)
        cnval = cls.string_to_value(cnstr)
        too_low = cls.min_val is not None and cnval < cls.min_val
        too_high = cls.max_val is not None and cnval > cls.max_val
        if too_low or too_high:
            min_max_text = u.min_max_to_text(cls.min_val, cls.max_val, 'less')
            msg = 'Value for {} must be {}'.format(cls.__name__, min_max_text)
            raise InvalidCallNumberStringError(msg)
        return validate_result

    @classmethod
    def string_to_value(cls, cnstr):
        if cls.max_val < 1:
            cnstr = '.{}'.format(cnstr)
            return cls.create_decimal(cnstr)
        return int(cnstr)

    @classmethod
    def create_decimal(cls, value):
        min_interval = decimal.Decimal(str(cls.min_interval))
        return decimal.Decimal(value).quantize(min_interval)

    @classmethod
    def describe_short(cls, include_pattern=False):
        min_max_text = u.min_max_to_text(cls.min_val, cls.max_val, 'less')
        text = super(Numeric, cls).describe_short(include_pattern)
        return '{} that has a value of {}'.format(text, min_max_text)

    @classmethod
    def describe_long(cls, include_pattern=False):
        min_max_text = u.min_max_to_text(cls.min_val, cls.max_val, 'less')
        text = super(Numeric, cls).describe_long(include_pattern)
        return '{} that has a value of {}'.format(text, min_max_text)

    @classmethod
    def derive(cls, **attr):
        max_zfill = attr.get('max_numeric_zfill', cls.max_numeric_zfill)
        min_val = attr.get('min_val', cls.min_val)
        max_val = attr.get('max_val', cls.max_val)
        min_length = attr.get('min_length', cls.template.min_length)
        if max_val is not None and min_val > max_val:
            raise SettingsError('``min_val`` cannot be > ``max_val``')
        if max_val is not None and max_val <= 0:
            raise SettingsError('``max_val`` cannot be <= 0')
        if min_val < 0:
            raise SettingsError('``min_val`` cannot be < 0')
        if max_val is None or max_val >= 1:
            attr['min_interval'] = 1
            real_max_val = int(math.pow(10, max_zfill) - 1)
            if max_val is None or max_val > real_max_val:
                attr['numeric_zfill'] = max_zfill
                attr['max_val'] = real_max_val
            else:
                attr['numeric_zfill'] = len(str(max_val))
        elif max_val > 0:
            attr['numeric_zfill'] = 0
            attr['min_decimal_places'] = min_length
            attr['max_decimal_places'] = len(str(max_val)) - 2
            attr['min_interval'] = math.pow(10, -attr['max_decimal_places'])
        if 'classname' not in attr:
            classname = '{}__{}To{}'.format(cls.__name__, min_val, max_val)
            attr['classname'] = classname
        return super(Numeric, cls).derive(**attr)

    @property
    def value(self):
        return type(self).string_to_value(self._string)

    def for_sort(self):
        return self._string.zfill(self.numeric_zfill)


class Formatting(SimpleUnit):

    options_defaults = SimpleUnit.options_defaults.copy()
    options_defaults.update({
        'use_formatting_in_search': settings.DEFAULT_USE_FORMATTING_IN_SEARCH,
        'use_formatting_in_sort': settings.DEFAULT_USE_FORMATTING_IN_SORT
    })
    is_formatting = True
    template = SimpleTemplate(
        min_length=1,
        max_length=None,
        base_pattern=r'[^A-Za-z0-9]',
        base_description='non-alphanumeric symbol'
    )

    def for_sort(self):
        return self._string if self.use_formatting_in_sort else ''

    def for_search(self):
        return self._string if self.use_formatting_in_search else ''


DEFAULT_SEPARATOR_TYPE = Formatting.derive(
    classname='DEFAULT_SEPARATOR_TYPE',
    min_length=0,
    max_length=None,
    base_pattern=r'\s',
    short_description='optional whitespace'
)
