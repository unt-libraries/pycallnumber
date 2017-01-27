"""Implement the patterns that Unit objects use."""


from __future__ import unicode_literals
from __future__ import absolute_import
from builtins import str
import re
import collections

from .options import ObjectWithOptions
from .exceptions import InvalidCallNumberStringError, SettingsError,\
                        MethodError
from . import utils as u


class Template(ObjectWithOptions):

    options_defaults = {
        'short_description': None,
        'long_description': None
    }

    def _str_conforms_to_template(self, cnstr, options):
        return True if self.get_regex(True).search(cnstr) else False

    def _generate_short_description(self):
        raise NotImplementedError()

    def _generate_long_description(self):
        raise NotImplementedError()

    @property
    def is_optional(self):
        return bool(self.get_regex().match(''))

    def describe_short(self, include_pattern=False):
        if self.short_description is not None:
            text = self.short_description
        else:
            text = self._generate_short_description()
        if include_pattern:
            pattern = self.get_regex(use_re_groups=True).pattern
            text = '{} -- pattern is /{}/'.format(text, pattern)
        return text

    def describe_long(self, include_pattern=False):
        if self.long_description is not None:
            text = self.long_description
        else:
            text = self._generate_long_description()
        if include_pattern:
            pattern = self.get_regex(use_re_groups=True).pattern
            text = ('{}\n\nThe full pattern for this template is:\n\n/{}/'
                    ''.format(text, pattern))
        return text

    def _generate_pattern(self, match_whole=False, use_re_groups=False):
        raise NotImplementedError()

    @u.memoize
    def get_regex(self, match_whole=False, use_re_groups=False):
        pattern = self._generate_pattern(match_whole, use_re_groups)
        return re.compile(pattern)

    def validate(self, cnstr, options=None):
        if not self._str_conforms_to_template(cnstr, options):
            raise InvalidCallNumberStringError()
        return True


class SimpleTemplate(Template):

    options_defaults = Template.options_defaults.copy()
    options_defaults.update({
        'min_length': 1,
        'max_length': 1,
        'base_pattern': '.*',
        'base_description': None,
        'base_description_plural': None,
        'pre_pattern': '',
        'pre_description': None,
        'post_pattern': '',
        'post_description': None
    })

    def __init__(self, **options):
        super(SimpleTemplate, self).__init__(**options)
        self.min_length = 0 if self.min_length is None else self.min_length
        if self.max_length is not None and self.max_length < self.min_length:
            msg = ('``max_length`` cannot be less than ``min_length.`` Use '
                   'None for ``max_length`` if there is no maximum length.')
            raise SettingsError(msg)

    def _get_base_pattern(self):
        length = u.min_max_to_pattern(self.min_length, self.max_length)
        return '{}{}'.format(self.base_pattern, length)

    def _generate_pattern(self, match_whole=False, use_re_groups=False):
        base_pattern = self._get_base_pattern()
        pattern = '{}{}{}'.format(self.pre_pattern, base_pattern,
                                  self.post_pattern)
        if use_re_groups:
            pattern = r'({})'.format(pattern)
        if match_whole:
            pattern = r'^{}$'.format(pattern)
        return pattern

    def _describe_base(self):
        text = u.min_max_to_text(self.min_length, self.max_length)
        if self.base_description:
            if self.min_length == 1 and self.max_length == 1:
                description = self.base_description
            elif self.base_description_plural:
                description = self.base_description_plural
            else:
                description = '{}{}'.format(self.base_description, 's')
            return '{} {}'.format(text, description)
        else:
            return '{} of /{}/'.format(text, self.base_pattern)

    def _describe_pre(self):
        if self.pre_description:
            return '{} (/{}/)'.format(self.pre_description, self.pre_pattern)
        else:
            return '/{}/'.format(self.pre_pattern)

    def _describe_post(self):
        if self.post_description:
            return '{} (/{}/)'.format(self.post_description, self.post_pattern)
        else:
            return '/{}/'.format(self.post_pattern)

    def _generate_short_description(self):
        text = 'a string with '
        if self.pre_pattern:
            text = '{}{}, followed by '.format(text, self._describe_pre())
        text = '{}{}'.format(text, self._describe_base())
        if self.post_pattern:
            text = '{}, followed by {}'.format(text, self._describe_post())
        return text

    def _generate_long_description(self):
        return 'A SimpleTemplate matching {}.'.format(self.describe_short())


class Grouping(ObjectWithOptions):

    options_defaults = {
        'min': 1,
        'max': 1,
        'types': None,
        'name': None,
        'inner_sep_type': None,
        'outer_sep_group': None,
        'outer_sep_placement': None,
    }

    def __init__(self, **options):
        super(Grouping, self).__init__(**options)
        if not bool(self.types):
            raise SettingsError('The ``types`` kwarg is required.')
        if not self.name:
            raise SettingsError('The ``name`` kwarg cannot be None or blank.')

    def __str__(self):
        """Return the string value for this object."""
        return self.get_full_regex(True).pattern

    def __repr__(self):
        """Return a string representation of this object."""
        return '{}{}'.format(type(self), str(self))

    def describe(self):
        if self.min == 0:
            contains = 'is optional and may have'
        else:
            contains = 'should contain'
        size = u.min_max_to_text(self.min, self.max)
        types_descs = []
        for t in self.types:
            types_descs.append('{} -- {}'.format(t.__name__,
                                                 t.describe_short(False)))
        types = '\n\n'.join(types_descs)
        text = ('The ``{}`` grouping {} {} of the following Units:'
                ''.format(self.name, contains, size))
        text = '{}\n\n{}'.format(text, u.pretty(types, indent_level=1))
        return text

    @property
    def is_optional(self):
        return self.min == 0

    @u.memoize
    def get_inner_separator_regex(self):
        if self.inner_sep_type is None:
            return re.compile('')
        else:
            return self.inner_sep_type.get_template_regex()

    @u.memoize
    def get_outer_separator_regex(self, include_re_group=False):
        if self.outer_sep_group is None:
            return re.compile('')
        else:
            return self.outer_sep_group.get_full_regex(include_re_group)

    @u.memoize
    def get_base_regex(self):
        patterns = []
        for t in self.types:
            p = t.get_template_pattern()
            patterns.append(p)
        pattern = r'|'.join(patterns)
        pattern = u.convert_re_groups_to_noncapturing(pattern)
        return re.compile(pattern)

    @u.memoize
    def get_full_regex(self, include_re_group=False):
        pattern = self._generate_pattern_with_inner_sep()
        if self.outer_sep_group is not None:
            pattern = self._add_outer_sep_to_pattern(pattern)
        if include_re_group:
            pattern = u.add_label_to_pattern(self.name, pattern)
        else:
            pattern = r'(?:{})'.format(pattern)
        if self.is_optional:
            pattern = r'{}?'.format(pattern)
        return re.compile(pattern)

    def _generate_pattern_with_inner_sep(self):
        pattern = ''
        base_p = self.get_base_regex().pattern
        if (self.max is None or self.max > 1) and self.inner_sep_type:
            sep_p = self.get_inner_separator_regex().pattern
            first_min = self.min - 1 if self.min > 0 else 0
            first_max = self.max - 1 if self.max else None
            len_p = u.min_max_to_pattern(first_min, first_max)
            pattern = r'(?:(?:{0}){1}(?={0})){2}'.format(base_p, sep_p, len_p)
            remainder = r'(?:{})'.format(base_p)
        else:
            min_ = 1 if self.min == 0 else self.min
            len_p = u.min_max_to_pattern(min_, self.max)
            remainder = r'(?:{0}){1}'.format(base_p, len_p)
        pattern = r'{}{}'.format(pattern, remainder)
        return pattern

    def _add_outer_sep_to_pattern(self, pattern):
        outer_sep_p = self.get_outer_separator_regex().pattern
        if self.outer_sep_placement == 'before':
            pattern = r'{}{}'.format(outer_sep_p, pattern)
        elif self.outer_sep_placement == 'after':
            pattern = r'{}{}'.format(pattern, outer_sep_p)
        return pattern

    def cnstr_to_units(self, string, useropts):
        parts, outer_sep_part = [], None
        if self.outer_sep_group:
            outer_sep_part, string = self._split_outer_sep(string, useropts)
        parts = self._split_string(string, useropts)
        if len(parts) == 0:
            parts = None
        elif self.max == 1:
            parts = parts[0]
        if self.outer_sep_group:
            if self.outer_sep_placement == 'before':
                return outer_sep_part, parts
            elif self.outer_sep_placement == 'after':
                return parts, outer_sep_part
        return (parts,)

    def _split_outer_sep(self, string, useropts):
        pattern = self.get_outer_separator_regex().pattern
        if self.outer_sep_placement == 'before':
            pattern = r'^{}'.format(pattern)
        elif self.outer_sep_placement == 'after':
            pattern = r'{}$'.format(pattern)
        unit = None
        match = re.search(pattern, string)
        match_str = match.group(0) if match else ''
        if match_str:
            unit = u.create_unit(match_str, self.outer_sep_group.types,
                                 useropts, self.outer_sep_group.name, True)
            if unit is None:
                msg = ('Could not create outer_sep Unit object from string '
                       '\'{}\' based on allowable outer_sep unit types: {}.'
                       ''.format(match_str,
                                 ', '.join(self.outer_sep_group.types)))
                raise InvalidCallNumberStringError(msg)
            string = re.sub(pattern, '', string)
        return (unit, string)

    def _split_string(self, string, useropts):
        parts = []
        is_first, is_last = True, False
        while string:
            match_str = self._get_split_part_regex().match(string).group(0)
            if not match_str:
                msg = ('Could not match \'{}\' to /{}/.'
                       ''.format(string, self._get_split_part_regex().pattern))
                raise InvalidCallNumberStringError(msg)
            unit = u.create_unit(match_str, self.types, useropts, self.name)
            if unit is None:
                msg = ('Could not create Unit object for \'{}\' based on '
                       'allowable unit types: {}.'
                       ''.format(match_str, str(self.types)))
                raise InvalidCallNumberStringError(msg)
            parts.append(unit)
            remove = re.escape(match_str)
            string = re.sub(r'^{}'.format(remove), '', string)
            if is_first and match_str:
                is_first = False

            if string:
                sep = self.get_inner_separator_regex().match(string).group(0)
                if sep:
                    string = re.sub(r'^{}'.format(re.escape(sep)), '', string)
                    if not string:
                        is_last = True
                    if is_first or is_last:
                        msg = ('A grouping cannot begin or end with an inner '
                               'separator.')
                        raise InvalidCallNumberStringError(msg)
                    unit = u.create_unit(sep, [self.inner_sep_type], useropts,
                                         is_separator=True)
                    if unit is None:
                        msg = ('Could not create inner_sep Unit object of '
                               'type {} from string \'{}\'.'
                               ''.format(self.inner_sep_type, sep))
                        raise InvalidCallNumberStringError(msg)
                    parts.append(unit)
        return parts

    @u.memoize
    def _get_split_part_regex(self):
        base_p = self.get_base_regex().pattern
        next_p = self.get_inner_separator_regex().pattern or base_p
        pattern = r'(?:(?:{0})$|(?:{0})(?=(?:{1})))'.format(base_p, next_p)
        return re.compile(pattern)


class CompoundTemplate(Template):

    options_defaults = Template.options_defaults.copy()
    options_defaults.update({
        'separator_type': None,
        'groups': None
    })

    default_separator_name = 'sep'

    def __init__(self, **options):
        super(CompoundTemplate, self).__init__(**options)
        sep_type = self.separator_type
        groups = self.groups
        msg = None
        if sep_type is not None and not hasattr(sep_type, 'template'):
            msg = 'The ``separator_type`` kwarg must be None or a Unit type.'
        elif groups is None or not isinstance(groups, (list, tuple)):
            msg = ('The ``groups`` kwarg is required--it must be a list or '
                   'tuple of dicts, where each dict represents one named '
                   'grouping within this CompoundTemplate\'s pattern, with '
                   'parameters: max (int), min (int), name (str), types '
                   '(list of Unit subclasses), is_separator (bool), and '
                   'separator_type (Unit subclass).')
        else:
            try:
                names = [g['name'] for g in groups
                         if not g.get('is_separator', False)]
            except KeyError:
                msg = ('Definitions for each group provided by the ``groups`` '
                       'kwarg must have a ``name`` element if the group is '
                       'not a separator.')
            else:
                if len(set(names)) != len(names):
                    msg = 'Each group ``name`` must be unique.'
        if (msg):
            raise SettingsError(msg)
        self.groupings = self._generate_groupings(sep_type, groups)
        parts_names = self.generate_parts_names(include_separators=True)
        self.partlist_type = collections.namedtuple('PartList', parts_names)

    def _generate_groupings(self, separator_type, group_defs):
        groupings = []
        all_prev_groups_are_optional = True
        dsep_count = 0
        dsep_name = '{}{}'.format(self.default_separator_name, dsep_count)
        default_sep = Grouping(name=dsep_name, types=[separator_type])
        for i, grdef in enumerate(group_defs):
            gr_is_optional = not grdef.get('min', 1)
            prev = group_defs[i-1] if i > 0 else {}
            next_ = group_defs[i+1] if i + 1 < len(group_defs) else {}
            self._check_grouping(grdef, prev, next_)

            gr_is_separator = grdef.get('is_separator', False)
            next_is_separator = next_.get('is_separator', False)
            prev_is_separator = prev.get('is_separator', False)
            osep, osep_placement = None, None

            # Hello spaghetti! Got to figure out a better way to do this.
            if not gr_is_separator:
                if len(group_defs) > 1:
                    if all_prev_groups_are_optional:
                        if gr_is_optional and next_:
                            if next_is_separator:
                                osep_kws = self._grouping_def_to_kwargs(next_)
                                osep = Grouping(**osep_kws)
                            elif separator_type is not None:
                                osep = default_sep
                            osep_placement = 'after'
                        else:
                            all_prev_groups_are_optional = False
                    else:
                        if prev_is_separator:
                            osep_kws = self._grouping_def_to_kwargs(prev)
                            osep = Grouping(**osep_kws)
                        elif separator_type is not None:
                            osep = default_sep
                        osep_placement = 'before'
                    if osep == default_sep:
                        dsep_count += 1
                        dsep_name = '{}{}'.format(self.default_separator_name,
                                                  dsep_count)
                        default_sep = Grouping(name=dsep_name,
                                               types=[separator_type])

                kwargs = self._grouping_def_to_kwargs(grdef)
                # kwargs['inner_sep_type'] = separator_type
                kwargs['outer_sep_group'] = osep
                kwargs['outer_sep_placement'] = osep_placement
                groupings.append(Grouping(**kwargs))
        return groupings

    def _check_grouping(self, grdef, prev_gr, next_gr):
        gr_is_first = False if prev_gr else True
        gr_is_last = False if next_gr else True
        gr_is_separator = grdef.get('is_separator', False)
        if gr_is_separator and (gr_is_first or gr_is_last):
            msg = ('A CompoundTemplate cannot begin or end with a '
                   'separator grouping.')
            raise SettingsError(msg)
        elif gr_is_separator and prev_gr.get('is_separator', False):
            msg = ('A CompoundTemplate cannot have multiple separator '
                   'groupings in a row.')
            raise SettingsError(msg)

    def _grouping_def_to_kwargs(self, grdef):
        kwargs = grdef.copy()
        if 'possible_types' in kwargs:
            kwargs['types'] = kwargs.pop('possible_types')
        elif 'type' in kwargs:
            kwargs['types'] = [kwargs.pop('type')]
        return Grouping.filter_valid_useropts(kwargs)

    def generate_parts_names(self, include_separators=False):
        names = []
        for g in self.groupings:
            if g.outer_sep_group and g.outer_sep_placement == 'before':
                names.extend([g.outer_sep_group.name, g.name])
            elif g.outer_sep_group and g.outer_sep_placement == 'after':
                names.extend([g.name, g.outer_sep_group.name])
            else:
                names.append(g.name)
        return names

    def validate(self, cnstr, u_opts=None):
        try:
            parts = self.cnstr_to_parts(cnstr, u_opts)
        except InvalidCallNumberStringError as e:
            msg = ('**** Here is what was found while attempting to parse '
                   '\'{}\' ****\n\n{}').format(cnstr, e)
            raise InvalidCallNumberStringError(msg)
        return parts

    def _generate_pattern(self, match_whole=False, use_re_groups=False):
        pattern = ''.join([g.get_full_regex(use_re_groups).pattern
                           for g in self.groupings])
        if match_whole:
            pattern = r'^{}$'.format(pattern)
        return pattern

    def cnstr_to_parts(self, cnstr, u_opts):
        partlist, msg, blank_so_far = [], '', True
        for i, g in enumerate(self.groupings):
            match = self._get_right_anchored_grouping_regex(g, i).match(cnstr)
            match_str, cnstr = self._process_part_match(match, cnstr, g.name)
            if match_str is None:
                error_text = self._generate_non_match_error(cnstr, g, i)
                msg = '{}{}'.format(msg, error_text)
                raise InvalidCallNumberStringError(msg)
            try:
                parts = g.cnstr_to_units(match_str, u_opts)
            except InvalidCallNumberStringError as e:
                msg = ('{}While parsing the {} grouping, \'{}\' was found to '
                       'be invalid. {} {}'
                       ''.format(msg, g.name, match_str, e.args[0],
                                 g.describe()))
                raise InvalidCallNumberStringError(msg)
            partlist.extend(parts)
            msg = ('{}\'{}\' matched the {} grouping.\n'
                   ''.format(msg, match_str, g.name))

            is_last = match_str and not cnstr
            is_first = match_str and blank_so_far
            blank_so_far = False if is_first else blank_so_far
            if not self._part_separator_is_valid(parts, is_first, is_last):
                msg = ('{}While parsing the {} grouping, \'{}\' was found to '
                       'contain a separator that was not valid: separators '
                       'must not appear at the beginning or end of a call '
                       'number string, and the grouping immediately preceding '
                       'or following the separator must exist.'
                       ''.format(msg, g.name, match_str))
                raise InvalidCallNumberStringError(msg)

        return self.partlist_type(*partlist)

    @u.memoize
    def _get_right_anchored_grouping_regex(self, grouping, grouping_index):
        pattern = grouping.get_full_regex(True).pattern
        next_patterns, anchored = [], False
        for i, g in enumerate(self.groupings[grouping_index+1:]):
            next_patterns.append(g.get_full_regex().pattern)
            if not g.is_optional:
                anchored = True
                break
        if not anchored:
            next_patterns.append('$')
        if next_patterns:
            pattern = '{}(?={})'.format(pattern, ''.join(next_patterns))
        return re.compile(pattern)

    def _generate_non_match_error(self, cnstr, grouping, grouping_index):
        err_group, msg = None, ''
        for i, g in enumerate(self.groupings[grouping_index:]):
            match = g.get_full_regex(True).match(cnstr)
            match_str, cnstr = self._process_part_match(match, cnstr, g.name)
            if match_str is None:
                err_group = g
                break
            msg = ('{}\'{}\' matched the ``{}`` grouping.\n'
                   ''.format(msg, match_str, g.name))
        if cnstr:
            msg = ('{}\'{}\' does not match any grouping.'.format(msg, cnstr))
        elif err_group:
            msg = ('{}\'{}\' does not appear to be or begin with a valid '
                   '``{}`` grouping. {}'
                   ''.format(msg, cnstr, err_group.name, err_group.describe()))
        else:
            method_msg = ('Oops! Something went wrong. All groupings matched '
                          'perfectly in _generate_non_match_error method.')
            raise MethodError(method_msg)
        return msg

    def _process_part_match(self, match, cnstr, group_name):
        match_str = None
        if match:
            match_str = match.group(group_name) or ''
            if match_str:
                cnstr = re.sub(r'^{}'.format(re.escape(match_str)), '', cnstr)
        return (match_str, cnstr)

    def _part_separator_is_valid(self, parts, is_first, is_last):
        if len(parts) == 2:
            if parts[0] is None and getattr(parts[1], 'is_separator', False):
                return False
            if parts[1] is None and getattr(parts[0], 'is_separator', False):
                return False
            if is_first and getattr(parts[0], 'is_separator', False):
                return False
            if is_last and getattr(parts[1], 'is_separator', False):
                return False
        return True

    def _generate_short_description(self):
        groupings_desc_list = []
        for g in self.groupings:
            min_max_text = u.min_max_to_text(g.min, g.max)
            s = '' if g.min == 1 and g.max == 1 else 's'
            gdesc_text = '{} ``{}`` grouping{}'.format(min_max_text, g.name, s)
            groupings_desc_list.append(gdesc_text)
        gdesc_text = u.list_to_text(groupings_desc_list, 'and')
        if self.separator_type is not None:
            sep_description = self.separator_type.describe_short(False)
            sep_text = ', separated by {}'.format(sep_description)
        else:
            sep_text = ''
        return 'a string with {}{}'.format(gdesc_text, sep_text)

    def _generate_long_description(self):
        groupings_name_list = []
        groupings_desc_list = []
        for g in self.groupings:
            groupings_name_list.append('``{}``'.format(g.name))
            groupings_desc_list.append(g.describe())
        gname_text = u.list_to_text(groupings_name_list, 'and')
        gdesc_text = '\n\n'.join(groupings_desc_list)
        if self.separator_type is not None:
            separator_min_length = self.separator_type.template.min_length
            to_be = 'can be' if separator_min_length == 0 else 'are'
            sep_description = self.separator_type.describe_short(False)
            sep_text = ('\n\nGroupings {} separated by {}.'
                        ''.format(to_be, sep_description))
        else:
            sep_text = ''
        s = '' if len(self.groupings) == 1 else 's'
        return ('A CompoundTemplate with grouping{} {}.\n\n{}{}'
                ''.format(s, gname_text, gdesc_text, sep_text))
