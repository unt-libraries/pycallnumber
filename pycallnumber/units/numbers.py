"""Represent numeric parts of call numbers."""


from __future__ import unicode_literals
from __future__ import absolute_import
from builtins import str
import decimal
import math
import copy

from pycallnumber import settings
from pycallnumber.exceptions import InvalidCallNumberStringError, SettingsError
from pycallnumber.template import CompoundTemplate
import pycallnumber.utils as u
from .simple import Alphabetic, Numeric, Formatting
from .compound import AlphaNumericSymbol


ThreeDigits = Numeric.derive(
    classname='ThreeDigits',
    min_val=0,
    max_val=999,
    min_length=3,
    max_length=3
)

UpToThreeDigits = Numeric.derive(
    classname='UpToThreeDigits',
    min_val=0,
    max_val=999,
    min_length=1,
    max_length=3
)

UpToThreeDigits__1To999 = UpToThreeDigits.derive(
    min_val=1,
    max_val=999
)

USGBThousandsSeparator = Formatting.derive(
    classname='USGBThousandsSeparator',
    short_description='a comma',
    min_length=1,
    max_length=1,
    base_pattern=r',',
    use_formatting_in_search=False,
    use_formatting_in_sort=False
)

USGBDecimalSeparator = Formatting.derive(
    classname='USGBDecimalSeparator',
    short_description='a decimal point',
    min_length=1,
    max_length=1,
    base_pattern=r'\.',
    use_formatting_in_search=True,
    use_formatting_in_sort=True,
)

Decimal = Numeric.derive(
    classname='Decimal',
    short_description=('a numeric string representing 1 or more decimal '
                       'places'),
    min_val=0,
    max_val=.999999999,
    min_length=1,
    max_length=9
)


class BaseCompoundNumber(AlphaNumericSymbol):

    max_numeric_zfill = settings.DEFAULT_MAX_NUMERIC_ZFILL
    min_val = 0
    max_val = int(math.pow(10, max_numeric_zfill) - 1)
    numeric_zfill = max_numeric_zfill
    min_interval = 1
    is_whole_number = True
    min_decimal_places = 0
    max_decimal_places = 0

    @classmethod
    def validate(cls, cnstr, instance_options=None):
        too_low, too_high = False, False
        try:
            cnval = cls.string_to_value(cnstr)
            too_low = cls.min_val is not None and cnval < cls.min_val
            too_high = cls.max_val is not None and cnval > cls.max_val
        except Exception:
            pass
        if too_low or too_high:
            min_max_text = u.min_max_to_text(cls.min_val, cls.max_val, 'less')
            msg = 'Value for {} must be {}'.format(cls.__name__, min_max_text)
            raise InvalidCallNumberStringError(msg)
        return super(BaseCompoundNumber, cls).validate(cnstr, instance_options)

    @classmethod
    def string_to_value(cls, cnstr):
        raise NotImplementedError()

    @classmethod
    def create_decimal(cls, value):
        min_interval = decimal.Decimal(str(cls.min_interval))
        return decimal.Decimal(value).quantize(min_interval)

    @classmethod
    def describe_short(cls, include_pattern=False):
        min_max_text = u.min_max_to_text(cls.min_val, cls.max_val, 'less')
        text = super(BaseCompoundNumber, cls).describe_short(include_pattern)
        return '{}; has an overall value of {}'.format(text, min_max_text)

    @classmethod
    def describe_long(cls, include_pattern=False):
        min_max_text = u.min_max_to_text(cls.min_val, cls.max_val, 'less')
        text = super(BaseCompoundNumber, cls).describe_long(include_pattern)
        return '{}. It has an overall value of {}'.format(text, min_max_text)

    @classmethod
    def derive(cls, **attr):
        max_zfill = attr.get('max_numeric_zfill', cls.max_numeric_zfill)
        min_val = attr.get('min_val', cls.min_val)
        max_val = attr.get('max_val', cls.max_val)
        min_str, max_str = str(min_val), str(max_val)
        min_parts = min_str.split('.') if '.' in min_str else [min_str, '0']
        max_parts = max_str.split('.') if '.' in max_str else [max_str, '0']
        user_whole_number = attr.get('is_whole_number', False)
        user_min_decimal_places = attr.get('min_decimal_places', 0)
        user_max_decimal_places = attr.get('max_decimal_places', 0)

        if max_val is not None and min_val > max_val:
            raise SettingsError('``min_val`` cannot be > ``max_val``')
        if max_val is not None and max_val <= 0:
            raise SettingsError('``max_val`` cannot be <= 0')
        if min_val < 0:
            raise SettingsError('``min_val`` cannot be < 0')
        if user_min_decimal_places > user_max_decimal_places:
            msg = '``min_decimal_places`` cannot be > ``max_decimal_places``'
            raise SettingsError(msg)

        if '.' in '{}{}'.format(min_val, max_val):
            if user_whole_number:
                msg = ('``min_val`` and ``max_val`` must be integers if '
                       '``is_whole_number`` is True')
                raise SettingsError(msg)
            if len(min_parts[1]) > len(max_parts[1]):
                max_decimal_places = len(min_parts[1])
            else:
                max_decimal_places = len(max_parts[1])
            if user_max_decimal_places > max_decimal_places:
                max_decimal_places = user_max_decimal_places
            min_interval = math.pow(10, -max_decimal_places)
            attr['is_whole_number'] = False
            attr['min_interval'] = min_interval
            attr['max_decimal_places'] = max_decimal_places
        else:
            attr['is_whole_number'] = attr.get('is_whole_number', True)
            attr['min_interval'] = attr.get('min_interval', 1)
            attr['min_decimal_places'] = attr.get('min_decimal_places', 0)
            attr['max_decimal_places'] = attr.get('max_decimal_places', 0)

        if max_val is None or max_val >= 1:
            real_max_val = int(math.pow(10, max_zfill) - 1)
            if max_val is None or max_val > real_max_val:
                attr['max_val'] = real_max_val
                attr['numeric_zfill'] = len(str(real_max_val))
            else:
                attr['numeric_zfill'] = len(max_parts[0])
        elif max_val > 0:
            attr['numeric_zfill'] = 0

        if 'classname' not in attr:
            min_val = attr.get('min_val', cls.min_val)
            max_val = attr.get('max_val', cls.max_val)
            classname = '{}__{}To{}'.format(cls.__name__, min_val, max_val)
            attr['classname'] = classname
        return super(BaseCompoundNumber, cls).derive(**attr)

    @property
    def value(self):
        return type(self).string_to_value(self._string)


class WholeNumUSGB1000sSep(BaseCompoundNumber):

    min_val = 1000
    template = CompoundTemplate(
        short_description=('a string representing a whole number that is '
                           '>=1000 and uses a comma as the thousands '
                           'separator'),
        groups=[
            {'name': 'thousand1', 'min': 1, 'max': 1,
             'type': UpToThreeDigits__1To999},
            {'name': 'thousand_sep1', 'min': 1, 'max': 1,
             'type': USGBThousandsSeparator, 'is_separator': True},
            {'name': 'last_groups', 'min': 1, 'max': None, 'type': ThreeDigits,
             'inner_sep_type': USGBThousandsSeparator}
        ]
    )

    @classmethod
    def string_to_value(cls, cnstr):
        return int(''.join(cnstr.split(',')))

    def for_sort(self):
        return str(int(self.value)).zfill(self.numeric_zfill)


class Number(BaseCompoundNumber):

    definition = ('a non-negative integer or floating point number, formatted '
                  'based on US or British conventions: a period is used as a '
                  'decimal point, if needed, and commas may be used as '
                  'thousands separators (but are optional)')

    max_numeric_zfill = settings.DEFAULT_MAX_NUMERIC_ZFILL
    min_val = 0
    max_val = float(math.pow(10, max_numeric_zfill) - 1) + .999999999
    min_interval = .000000001
    is_whole_number = False
    min_decimal_places = 0
    max_decimal_places = 9

    template = CompoundTemplate(
        separator_type=USGBDecimalSeparator,
        groups=[
            {'name': 'wholenumber', 'min': 1, 'max': 1,
             'possible_types': [WholeNumUSGB1000sSep, Numeric]},
            {'name': 'decimal', 'min': 0, 'max': 1, 'type': Decimal}
        ]
    )

    @classmethod
    def string_to_value(cls, cnstr):
        val = float(''.join(cnstr.split(',')))
        if val.is_integer():
            return int(val)
        return cls.create_decimal(val)

    @classmethod
    def derive(cls, **attr):
        thousands = attr.pop('thousands', 'optional')
        min_dec_places = attr.pop('min_decimal_places', 0)
        max_dec_places = attr.pop('max_decimal_places', 9)
        mn, mx = str(attr.get('min_val', 0)), str(attr.get('max_val', None))
        min_val, min_dec = mn.split('.') if '.' in mn else (mn, '0')
        max_val, max_dec = mx.split('.') if '.' in mx else (mx, 'None')
        min_val, min_dec = int(min_val), int(min_dec)
        max_val = None if max_val == 'None' else int(max_val)
        max_dec = None if max_dec == 'None' else int(max_dec)
        separator_type = USGBDecimalSeparator
        groups = copy.deepcopy(cls.template.groups)

        types = []
        if thousands in ('required', 'optional'):
            if max_val is None and min_val < 1000:
                types.append(WholeNumUSGB1000sSep)
            elif max_val > 999 and min_val < 1000:
                types.append(WholeNumUSGB1000sSep.derive(max_val=max_val))
            elif max_val > 999 and min_val > 999:
                types.append(WholeNumUSGB1000sSep.derive(max_val=max_val,
                                                         min_val=min_val))
            if min_val == 0:
                types.append(UpToThreeDigits)
            elif min_val < 1000 and (max_val is None or max_val > 999):
                types.append(UpToThreeDigits.derive(min_val=min_val))
            elif min_val < 1000 and max_val < 1000:
                types.append(UpToThreeDigits.derive(min_val=min_val,
                                                    max_val=max_val))
        if thousands in (None, 'optional'):
            types.append(Numeric.derive(min_val=min_val, max_val=max_val))

        groups[0] = groups[0] = {'name': 'wholenumber', 'min': 1, 'max': 1,
                                 'possible_types': types}

        if max_dec_places == 0:
            separator_type = None
            del groups[1]
        else:
            attr['max_decimal_places'] = max_dec_places
            min_max_text = u.min_max_to_text(min_dec_places or 1,
                                             max_dec_places)
            min_val = 0 if min_val == 0 else float('.{}'.format(min_dec))
            max_val = None if max_dec is None else float('.{}'.format(max_dec))
            NewDecimal = Decimal.derive(
                short_description=('a numeric string representing {} decimal '
                                   'places'.format(min_max_text)),
                min_length=min_dec_places or 1,
                max_length=max_dec_places,
                min_val=min_val,
                max_val=max_val
            )
            group_min = 0 if min_dec_places == 0 else 1
            groups[1] = {'name': 'decimal', 'min': group_min, 'max': 1,
                         'type': NewDecimal}

        attr['separator_type'] = separator_type
        attr['groups'] = groups
        return super(Number, cls).derive(**attr)

    def for_sort(self):
        sortval = super(Number, self).for_sort()
        if '.' in sortval:
            (whole, dec) = sortval.split('.')
            if int(dec) == 0:
                return whole
        return sortval


class OrdinalNumber(BaseCompoundNumber):

    definition = 'an ordinal number (1st, 2nd, 3rd, 4th ... 1,000th, etc.)'
    min_val = 1
    max_decimal_places = 0

    WholeNumber = Number.derive(
        classname='WholeNumber',
        definition=('a non-negative whole number, formatted based on US or '
                    'British conventions, with a comma as an optional '
                    'thousands separator'),
        max_decimal_places=0,
        min_val=1,
    )

    OrdinalSuffix = Alphabetic.derive(
        classname='OrdinalSuffix',
        short_description=('a 2-character string: \'st\', \'nd\', \'rd\', or '
                           '\'th\''),
        min_length=1,
        max_length=1,
        base_pattern=r'(?:[sS][tT]|[nNrR][dD]|[tT][hH])',
        for_sort=lambda x: '',
    )

    template = CompoundTemplate(
        separator_type=None,
        groups=[
            {'min': 1, 'max': 1, 'name': 'wholenumber', 'type': WholeNumber},
            {'min': 1, 'max': 1, 'name': 'suffix', 'type': OrdinalSuffix}
        ]
    )
