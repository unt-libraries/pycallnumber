"""Miscellaneous utility functions and classes."""
from __future__ import unicode_literals
from __future__ import absolute_import

from builtins import str
from builtins import range
from builtins import object
import functools
import inspect
import re
import struct
import importlib
import types

from .exceptions import InvalidCallNumberStringError


def memoize(function):
    """Decorate a function/method so it caches its return value.

    If the function is called as a method, then the cache is attached
    to the object used as the first arg passed to the method (e.g.,
    ``self`` or ``cls``) and can be accessed directly via a ``_cache``
    attribute on the object.

    If the function passed does not have a first argument named
    ``self`` or ``cls``, then it's assumed that it's not a method, and
    the cache is attached to the function itself via a ``_cache``
    attribute.

    Cache keys are calculated based on the argument values--both
    positional and keyword. In cases where a function uses default
    values for kwargs, the key will be the same no matter whether the
    call to the method includes the kwargs or relies on the default
    values. Order of args in the key will follow the order in the
    function's signature, even if kwargs are called out of order.
    """
    argnames, _, _, _ = inspect.getargspec(function)
    if len(argnames) > 0 and argnames[0] in ('self', 'cls'):
        function_is_method = True
        argnames = argnames[1:]
    else:
        function_is_method = False
        function._cache = {}

    def generate_key(base, args, kwargs):
        argsmap = inspect.getcallargs(function, *args, **kwargs)
        argvals_as_strings = [str(argsmap[argname]) for argname in argnames]
        argstr = '_{}'.format('_'.join(argvals_as_strings)) if argnames else ''
        return '{}{}'.format(base, argstr)

    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        if function_is_method:
            obj = args[0]
        else:
            obj = function
        cache = getattr(obj, '_cache', {})
        key = generate_key(function.__name__, args, kwargs)
        if key not in cache:
            cache[key] = function(*args, **kwargs)
            obj._cache = cache
        return obj._cache[key]

    return wrapper


def min_max_to_pattern(min_, max_):
    if min_ == 0 and max_ is None:
        return '*'
    if min_ == 0 and max_ == 1:
        return '?'
    if min_ == 1 and max_ is None:
        return '+'
    if min_ == 1 and max_ == 1:
        return ''
    if min_ > 1 and max_ is None:
        return '{{{},}}'.format(min_)
    if min_ == max_:
        return '{{{}}}'.format(min_)
    return '{{{},{}}}'.format(min_, max_)


def min_max_to_text(min_, max_, lower_word='fewer'):
    if min_ is None and max_ is None:
        return 'any number'
    if max_ is None:
        return '{} or more'.format(min_)
    if min_ is None:
        return '{} or {}'.format(max_, lower_word)
    if min_ == max_:
        return '{}'.format(min_)
    return '{} to {}'.format(min_, max_)


def list_to_text(list_, conjunction='or'):
    if len(list_) == 1:
        return list_[0]
    if len(list_) == 2:
        return '{} {} {}'.format(list_[0], conjunction, list_[1])
    return '{}, {} {}'.format(', '.join(list_[0:-1]), conjunction, list_[-1])


def convert_re_groups_to_noncapturing(re_str):
    """Convert groups in a re string to noncapturing.

    Adds ?: to capturing groups after the opening parentheses to
    convert them to noncapturing groups and returns the resulting re
    string.

    """
    return re.sub(r'(?<!\\)\((?!\?)', '(?:', re_str)


def add_label_to_pattern(label, pattern):
    return r'(?P<{}>{})'.format(label, pattern)


def load_class(class_string):
    split = class_string.split('.')
    module, class_ = '.'.join(split[0:-1]), split[-1]
    return getattr(importlib.import_module(module), class_)


def create_unit(cnstr, possible_types, useropts, name='', is_separator=False):
    useropts = useropts or {}
    for t in possible_types:
        opts = t.filter_valid_useropts(useropts)
        opts['is_separator'] = is_separator
        try:
            unit = t(cnstr, name=name, **opts)
        except InvalidCallNumberStringError:
            pass
        else:
            return unit
    return None


def get_terminal_size(default_width=100, default_height=50):
    try:
        terminal_size = _get_terminal_size_unixlike()
    except (IOError, ImportError):
        try:
            terminal_size = _get_terminal_size_windows()
        except (IOError, ImportError):
            terminal_size = default_width, default_height
    return terminal_size


def _get_terminal_size_unixlike():
    import fcntl
    import termios
    # this try/except block detects and works around a Py2.7.5 bug with
    # passing a unicode value as the first arg to struct methods
    try:
        struct.pack('HH', 0, 0)
    except TypeError:
        fmt = types.StringType('HHHH')
    else:
        fmt = 'HHHH'

    winsize_struct = struct.pack(fmt, 0, 0, 0, 0)
    packed_winsize = fcntl.ioctl(0, termios.TIOCGWINSZ, winsize_struct)
    height, width, _, _ = struct.unpack(fmt, packed_winsize)
    return width, height


def _get_terminal_size_windows():
    from ctypes import windll, create_string_buffer
    # stdin handle is -10
    # stdout handle is -11
    # stderr handle is -12
    handle = windll.kernel32.GetStdHandle(-12)
    csbi = create_string_buffer(22)
    res = windll.kernel32.GetConsoleScreenBufferInfo(handle, csbi)
    # Windows and Unix-like systems have different ways of going about finding
    # terminal size. Throw an IOError on failure to stay similar to the
    # Unix-like API (ioctl throws IOError on failure).
    if res:
        (_, _, _, _, _,
         left, top, right, bottom,
         _, _) = struct.unpack("hhhhHhhhhhh", csbi.raw)
        width = right - left + 1
        height = bottom - top + 1
        return width, height
    raise IOError


def _pretty_paragraph(in_str, adjusted_line_width, indent):
    out_paragraph, i = '', 0
    while i < len(in_str):
        next_i = i + adjusted_line_width
        words = in_str[i:next_i].split(' ')
        next_char = in_str[next_i] if next_i < len(in_str) else ''
        if next_char == ' ' or next_char == '':
            next_i += 1
        elif words[-1] and len(words) > 1:
            next_i -= len(words[-1])
        line = in_str[i:next_i].rstrip()
        lbreak = '\n' if i > 0 else ''
        out_paragraph = '{}{}{}{}'.format(out_paragraph, lbreak, indent, line)
        i = next_i
    return out_paragraph


def pretty(in_data, max_line_width=None, indent_level=0,
           tab_width=4):
    if max_line_width is None:
        max_line_width = get_terminal_size()[0]
    in_str = str(in_data)
    indent_length = tab_width * indent_level
    indent = ''.join(' ' for _ in range(0, indent_length))
    adjusted_line_width = max_line_width - indent_length
    if adjusted_line_width <= 0:
        adjusted_line_width = 20
    blocks = in_str.splitlines()
    out = [_pretty_paragraph(b, adjusted_line_width, indent) for b in blocks]
    return '\n'.join(out)


class ComparableObjectMixin(object):

    def _compare(self, other, op, compare):
        try:
            return compare(self.cmp_key(other, op), self._get_other(other, op))
        except (TypeError, AttributeError):
            return NotImplemented

    def _get_other(self, other, op):
        return other.cmp_key(self, op)

    def __eq__(self, other):
        return self._compare(other, 'eq', lambda s, o: s == o)

    def __ne__(self, other):
        return self._compare(other, 'ne', lambda s, o: s != o)

    def __gt__(self, other):
        return self._compare(other, 'gt', lambda s, o: s > o)

    def __ge__(self, other):
        return self._compare(other, 'ge', lambda s, o: s >= o)

    def __lt__(self, other):
        return self._compare(other, 'lt', lambda s, o: s < o)

    def __le__(self, other):
        return self._compare(other, 'le', lambda s, o: s <= o)

    def __hash__(self):
        return super(ComparableObjectMixin, self).__hash__()

    def cmp_key(self, other, op):
        return str(self)


class Infinity(ComparableObjectMixin, object):

    def __init__(self):
        self.sign = 'pos'

    def __repr__(self):
        return '<{} infinity>'.format(self.sign)

    def __neg__(self):
        ret = Infinity()
        ret.sign = 'neg' if self.sign == 'pos' else 'pos'
        return ret

    def _get_other(self, other, op):
        str_other = '{}'.format(other)
        return getattr(other, 'cmp_key', lambda ot, op: str_other)(self, op)

    def cmp_key(self, other, op):
        """
        Return a string key to use for comparisons.

        Unless you're comparing two Infinity objects to each other,
        positive Infinity should be greater than any other string, and
        negative Infinity should be less than any other string. If pos,
        it takes the other key and adds a space to the end, ensuring
        that this cmp_key will always be larger; if neg, it returns an
        empty string.
        """
        if isinstance(other, Infinity):
            return str(self)
        if self.sign == 'pos':
            okey = self._get_other(other, op)
            selfkey = '{} '.format(okey)
            return selfkey
        return ''
