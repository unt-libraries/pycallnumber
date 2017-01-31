"""Represent a call number or part of a call number."""


from __future__ import unicode_literals
from __future__ import absolute_import
import inspect

from .options import ObjectWithOptions
from .exceptions import InvalidCallNumberStringError
from .template import Template, SimpleTemplate, CompoundTemplate
from . import utils as u


class Unit(u.ComparableObjectMixin, ObjectWithOptions):

    options_defaults = {
        'definition': None,
        'is_separator': False
    }
    template = Template()
    is_formatting = False
    is_simple = False
    is_alphabetic = False
    is_numeric = False

    def __init__(self, cnstr, name='', **useropts):
        super(Unit, self).__init__(**useropts)
        self._validate_result = type(self).validate(cnstr, self.options)
        self._string = str(cnstr)
        self.name = name

    @classmethod
    def _get_derive_calling_module_name(cls, stacklevel):
        caller_frm = inspect.stack()[stacklevel+1][0]
        try:
            name = inspect.getmodule(caller_frm).__name__
        except Exception:
            name = None
        finally:
            del caller_frm
        return name

    @classmethod
    def derive(cls, stacklevel=1, **attributes):
        new_template_opts = {}
        template, template_class = cls.template, type(cls.template)
        exclude_template_opts = ['short_description']
        for prefix in ['base', 'pre', 'post']:
            if '{}_pattern'.format(prefix) in attributes:
                exclude_template_opts.append('{}_description'.format(prefix))
                exclude_template_opts.append('{}_description_plural'
                                             ''.format(prefix))
        for opt, val in template.options.items():
            val = None if opt in exclude_template_opts else val
            new_template_opts[opt] = attributes.pop(opt, val)
        attributes['template'] = template_class(**new_template_opts)
        cname = attributes.pop('classname', 'Derived{}'.format(cls.__name__))
        newclass = type(str(cname), (cls,), attributes)
        mname = cls._get_derive_calling_module_name(stacklevel)
        if mname is not None:
            newclass.__module__ = mname
        return newclass

    @classmethod
    def validate(cls, cnstr, instance_options=None):
        instance_options = instance_options or cls.options_defaults.copy()
        try:
            validate_result = cls.template.validate(cnstr, instance_options)
        except InvalidCallNumberStringError as e:
            msg = ('\'{}\' is not a valid {} Unit. It should be {}.'
                   '').format(cnstr, cls.__name__, cls.describe_short(False))
            if str(e):
                msg = '{}\n\n{}'.format(msg, e)
            raise InvalidCallNumberStringError(msg)
        return validate_result

    @classmethod
    def describe_short(cls, include_pattern=False):
        t_desc = cls.template.describe_short(include_pattern)
        text = ''
        if getattr(cls, 'definition', None) is not None:
            text = '{}; it is structured as '.format(cls.definition)
        return '{}{}'.format(text, t_desc)

    @classmethod
    def describe_long(cls, include_pattern=False):
        t_desc = cls.template.describe_long(include_pattern)
        text = 'The ``{}`` Unit type '.format(cls.__name__)
        if getattr(cls, 'definition', None) is not None:
            text = '{}represents {}. It '.format(text, cls.definition)
        return '{}uses the following template.\n\n{}'.format(text, t_desc)

    @classmethod
    def get_template_pattern(cls, match_whole=False, use_re_groups=False):
        return cls.template.get_regex(match_whole, use_re_groups).pattern

    @classmethod
    def get_template_regex(cls, match_whole=False, use_re_groups=False):
        return cls.template.get_regex(match_whole, use_re_groups)

    def __str__(self):
        """Return the string value for this object."""
        return self.for_print()

    def __repr__(self):
        """Return a string representation of this object."""
        return '<{} \'{}\'>'.format(type(self).__name__, str(self))

    def __contains__(self, other):
        return True if str(other) in str(self) else False

    def for_sort(self):
        return self._string

    def for_search(self):
        return self._string

    def for_print(self):
        return self._string

    def cmp_key(self, other, op):
        return self.for_sort()


class SimpleUnit(Unit):

    template = SimpleTemplate()
    options_defaults = Unit.options_defaults.copy()
    is_simple = True


class CompoundUnit(Unit):

    template = CompoundTemplate(
        groups=[
            {'name': 'default', 'type': SimpleUnit}
        ]
    )
    options_defaults = Unit.options_defaults.copy()
    sort_break = '!'

    def __init__(self, cnstr, name='default', **options):
        super(CompoundUnit, self).__init__(cnstr, name, **options)
        self._generate_parts_and_attributes()

    def _generate_parts_and_attributes(self):
        self._parts = []
        self.part_names = []
        self.has_part_names = True
        for name in self._validate_result._fields:
            value = getattr(self._validate_result, name)
            if isinstance(value, list):
                value = MultiUnitWrapper(value, value[0].name)
            if not getattr(value, 'is_separator', False):
                setattr(self, name, value)
                self.part_names.append(name)
            if value is not None:
                self._parts.append(value)

    def __contains__(self, other):
        if isinstance(other, type):
            return other == type(self) or self._contains_part_with_type(other)

        if isinstance(other, Unit):
            return ((type(other) == type(self) and other == self) or
                    self._contains_part(other))
        return super(CompoundUnit, self).__contains__(other)

    def _contains_part_with_type(self, other):
        return any([other == type(p) or other in p for p in self._parts])

    def _contains_part(self, other):
        return any([(type(other) == type(p) and other == p or
                     type(other) in p and other in p) for p in self._parts])

    def for_sort(self):
        strings, join = ([], False)
        for p in self._parts:
            for_sort = p.for_sort()
            is_sep_or_formatting = p.is_separator or p.is_formatting
            if (is_sep_or_formatting and for_sort) or join:
                strings[-1] = '{}{}'.format(strings[-1], for_sort)
            elif for_sort:
                strings.append(for_sort)
            join = True if is_sep_or_formatting and for_sort else False
        return self.sort_break.join(strings)

    def for_search(self):
        return ''.join([p.for_search() for p in self._parts])

    def for_print(self):
        return ''.join([p.for_print() for p in self._parts])


class MultiUnitWrapper(CompoundUnit):

    def __init__(self, parts, name='', is_separator=False):
        self.name = name
        self.is_separator = is_separator
        self._parts = parts
        self._parts_without_separators = self._remove_separators(self._parts)
        self.has_part_names = False

    def __len__(self):
        return len(self._parts_without_separators)

    def __getitem__(self, key):
        return self._parts_without_separators[key]

    def _remove_separators(self, parts):
        return [part for part in parts if not part.is_separator]
