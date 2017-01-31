from __future__ import unicode_literals
from builtins import object
import operator

import pytest

from context import utils as u
from context import units as uns


# Fixtures, factories, and test data

# noargs, args, kwargs, and args_kwargs are factory functions that
# produce memoized functions, where the memo key is generated based on
# the function signature when the function is called.

def noargs():
    @u.memoize
    def f():
        return 'val'
    return f


def args():
    @u.memoize
    def f(arg1, arg2):
        return 'val_{}_{}'.format(arg1, arg2)
    return f


def kwargs():
    @u.memoize
    def f(kwarg1='one', kwarg2='two'):
        return 'val_{}_{}'.format(kwarg1, kwarg2)
    return f


def args_kwargs():
    @u.memoize
    def f(arg1, arg2, kwarg1='one', kwarg2='two'):
        return 'val_{}_{}_{}_{}'.format(arg1, arg2, kwarg1, kwarg2)
    return f


class MemoizeBoundMethodTester(object):

    @u.memoize
    def args_kwargs(self, arg1, arg2, kwarg1='one', kwarg2='two'):
        return 'val_{}_{}_{}_{}'.format(arg1, arg2, kwarg1, kwarg2)


test_unit_low = uns.Alphabetic('A')
test_unit_high = uns.Alphabetic('ZZZZZZZZZZ')


MEMOIZE_PARAMETERS = [
    (noargs, [], {}, ''),
    (args, ['a', 'b'], {}, '_a_b'),
    (kwargs, ['a', 'b'], {}, '_a_b'),
    (kwargs, [], {}, '_one_two'),
    (kwargs, ['a'], {}, '_a_two'),
    (kwargs, [], {'kwarg1': 'a'}, '_a_two'),
    (kwargs, [], {'kwarg2': 'b'}, '_one_b'),
    (kwargs, ['a'], {'kwarg2': 'b'}, '_a_b'),
    (kwargs, [], {'kwarg1': 'a', 'kwarg2': 'b'}, '_a_b'),
    (kwargs, [], {'kwarg2': 'b', 'kwarg1': 'a'}, '_a_b'),
    (args_kwargs, ['a', 'b'], {}, '_a_b_one_two'),
    (args_kwargs, ['a', 'b', 'c'], {}, '_a_b_c_two'),
    (args_kwargs, ['a', 'b', 'c', 'd'], {}, '_a_b_c_d'),
    (args_kwargs, ['a', 'b', 'c'], {'kwarg2': 'd'}, '_a_b_c_d'),
    (args_kwargs, ['a', 'b'], {'kwarg2': 'd'}, '_a_b_one_d'),
    (args_kwargs, ['a', 'b'], {'kwarg1': 'c'}, '_a_b_c_two'),
    (args_kwargs, ['a', 'b'], {'kwarg1': 'c', 'kwarg2': 'd'}, '_a_b_c_d'),
    (args_kwargs, ['a', 'b'], {'kwarg2': 'd', 'kwarg1': 'c'}, '_a_b_c_d'),
]


PRETTY_PARAMETERS = [
    ('1234 12345', 10, 0, 1, '1234 12345'),
    ('1234 12345', 9, 0, 1, '1234\n12345'),
    ('1234 12345', 5, 0, 1, '1234\n12345'),
    ('1234 12345', 4, 0, 1, '1234\n1234\n5'),
    ('1234 12345', 3, 0, 1, '123\n4\n123\n45'),
    ('1234 12345', 2, 0, 1, '12\n34\n12\n34\n5'),
    ('1234 12345', 1, 0, 1, '1\n2\n3\n4\n1\n2\n3\n4\n5'),
    ('1234 12345', 0, 0, 1, '1234 12345'),
    ('1234 12345', 11, 1, 1, ' 1234 12345'),
    ('1234 12345', 11, 2, 1, '  1234\n  12345'),
    ('1234 12345', 11, 1, 2, '  1234\n  12345'),
    ('1234 12345', 11, 6, 1, '      1234\n      12345'),
    ('1234 12345', 11, 3, 2, '      1234\n      12345'),
    ('1234 12345', 11, 2, 3, '      1234\n      12345'),
    ('1234 12345', 11, 7, 1, '       1234\n       1234\n       5'),
    ('1234 12345', 11, 8, 1,
     '        123\n        4\n        123\n        45'),
    ('1234 12345', 11, 9, 1,
     '         12\n         34\n         12\n         34\n         5'),
    ('1234 12345', 11, 10, 1,
     ('          1\n          2\n          3\n          4\n          1\n'
      '          2\n          3\n          4\n          5')),
    ('1234 12345', 11, 11, 1, '           1234 12345'),
    ('1234 12345', 11, 12, 1, '            1234 12345'),
    ('1234 12345\n\n1234 12345', 10, 0, 1, '1234 12345\n\n1234 12345'),
    ('1234 12345\n\n1234 12345', 11, 2, 1,
     '  1234\n  12345\n\n  1234\n  12345')
]

INFINITY_COMP_PARAMS = [
    ((u.Infinity(), u.Infinity()), operator.lt, False),
    ((u.Infinity(), u.Infinity()), operator.le, True),
    ((u.Infinity(), u.Infinity()), operator.eq, True),
    ((u.Infinity(), u.Infinity()), operator.ne, False),
    ((u.Infinity(), u.Infinity()), operator.gt, False),
    ((u.Infinity(), u.Infinity()), operator.ge, True),
    ((-u.Infinity(), u.Infinity()), operator.lt, True),
    ((-u.Infinity(), u.Infinity()), operator.le, True),
    ((-u.Infinity(), u.Infinity()), operator.eq, False),
    ((-u.Infinity(), u.Infinity()), operator.ne, True),
    ((-u.Infinity(), u.Infinity()), operator.gt, False),
    ((-u.Infinity(), u.Infinity()), operator.ge, False),
    ((-u.Infinity(), -u.Infinity()), operator.lt, False),
    ((-u.Infinity(), -u.Infinity()), operator.le, True),
    ((-u.Infinity(), -u.Infinity()), operator.eq, True),
    ((-u.Infinity(), -u.Infinity()), operator.ne, False),
    ((-u.Infinity(), -u.Infinity()), operator.gt, False),
    ((-u.Infinity(), -u.Infinity()), operator.ge, True),
    ((u.Infinity(), -u.Infinity()), operator.lt, False),
    ((u.Infinity(), -u.Infinity()), operator.le, False),
    ((u.Infinity(), -u.Infinity()), operator.eq, False),
    ((u.Infinity(), -u.Infinity()), operator.ne, True),
    ((u.Infinity(), -u.Infinity()), operator.gt, True),
    ((u.Infinity(), -u.Infinity()), operator.ge, True),
    ((u.Infinity(), 'ZZZZZZZZZZ9999999999'), operator.lt, False),
    ((u.Infinity(), 'ZZZZZZZZZZ9999999999'), operator.le, False),
    ((u.Infinity(), 'ZZZZZZZZZZ9999999999'), operator.eq, False),
    ((u.Infinity(), 'ZZZZZZZZZZ9999999999'), operator.ne, True),
    ((u.Infinity(), 'ZZZZZZZZZZ9999999999'), operator.gt, True),
    ((u.Infinity(), 'ZZZZZZZZZZ9999999999'), operator.ge, True),
    ((u.Infinity(), test_unit_high), operator.lt, False),
    ((u.Infinity(), test_unit_high), operator.le, False),
    ((u.Infinity(), test_unit_high), operator.eq, False),
    ((u.Infinity(), test_unit_high), operator.ne, True),
    ((u.Infinity(), test_unit_high), operator.gt, True),
    ((u.Infinity(), test_unit_high), operator.ge, True),
    ((-u.Infinity(), ' '), operator.lt, True),
    ((-u.Infinity(), ' '), operator.le, True),
    ((-u.Infinity(), ' '), operator.eq, False),
    ((-u.Infinity(), ' '), operator.ne, True),
    ((-u.Infinity(), ' '), operator.gt, False),
    ((-u.Infinity(), ' '), operator.ge, False),
    ((-u.Infinity(), test_unit_low), operator.lt, True),
    ((-u.Infinity(), test_unit_low), operator.le, True),
    ((-u.Infinity(), test_unit_low), operator.eq, False),
    ((-u.Infinity(), test_unit_low), operator.ne, True),
    ((-u.Infinity(), test_unit_low), operator.gt, False),
    ((-u.Infinity(), test_unit_low), operator.ge, False),
]


# Tests

@pytest.mark.parametrize('factory, args, kwargs, suffix', MEMOIZE_PARAMETERS)
def test_memoize_vals(factory, args, kwargs, suffix):
    """The memoized function produced by ``factory`` should produce a
    value with the given ``suffix`` when passed the given ``args`` and
    ``kwargs`` values, and it should return the same value when called
    multiple times with the same arguments.
    """
    function = factory()
    test_val = 'val{}'.format(suffix)
    return_val1 = function(*args, **kwargs)
    return_val2 = function(*args, **kwargs)
    assert return_val1 == test_val and return_val2 == test_val


@pytest.mark.parametrize('factory, args, kwargs, suffix', MEMOIZE_PARAMETERS)
def test_memoize_keys_key_generation(factory, args, kwargs, suffix):
    """The memoized function produced by ``factory`` should have a
    ``_cache`` dictionary attribute that has a key with the given
    ``suffix`` when passed the given ``args`` and ``kwargs`` values.
    """
    function = factory()
    test_key = 'f{}'.format(suffix)
    function(*args, **kwargs)
    assert test_key in function._cache


def test_memoize_bound_method_value():
    """Memoizing a bound method should produce the correct value when
    called multiple times with the same arguments.
    """
    test_object = MemoizeBoundMethodTester()
    return_val1 = test_object.args_kwargs('1', '2', kwarg2='3')
    return_val2 = test_object.args_kwargs('1', '2', kwarg2='3')
    test_val = 'val_1_2_one_3'
    assert return_val1 == test_val and return_val2 == test_val


def test_memoize_bound_method_key():
    """Memoizing a bound method should attach the ``_cache`` dict to
    the object the method is bound to rather than the function, with
    the correct key.
    """
    test_object = MemoizeBoundMethodTester()
    test_object.args_kwargs('1', '2', kwarg2='3')
    test_key = 'args_kwargs_1_2_one_3'
    assert test_key in test_object._cache
    assert not hasattr(MemoizeBoundMethodTester.args_kwargs, '_cache')


def test_memoize_multiple_calls():
    """The memoized function produced by, e.g., the ``args_kwargs``
    factory function should have a ``_cache`` dictionary attribute that
    retains key/value pairs whenever the function is called multiple
    times with different arguments. Calling the function multiple times
    with the same arguments should return the same result.
    """
    function = args_kwargs()
    return_val1 = function('a', 'b')
    length1 = len(function._cache)
    return_val2 = function('1', '2', '3', '4')
    length2 = len(function._cache)
    return_val3 = function('a', 'b')
    length3 = len(function._cache)
    return_val4 = function('1', '2', '3', '4')
    length4 = len(function._cache)
    assert (return_val1 == return_val3 and return_val1 != return_val2 and
            return_val2 == return_val4 and length1 == 1 and length2 == 2 and
            length3 == 2 and length4 == 2)


@pytest.mark.parametrize('x, max_line_width, indent_level, tab_width, y',
                         PRETTY_PARAMETERS)
def test_pretty_output(x, max_line_width, indent_level, tab_width, y):
    """The u.pretty function should give the output ``y`` when
    passed input text ``x`` and the given parameters:
    ``max_line_width``, ``indent_level``, and ``tab_width``.

    """
    teststr = u.pretty(x, max_line_width, indent_level, tab_width)
    assert teststr == y


@pytest.mark.parametrize('values, op, expected', INFINITY_COMP_PARAMS)
def test_infinity_comparisons(values, op, expected):
    """The given values tuple should produce the expected truth value
    when compared via the given operator, op."""
    assert op(*values) == expected
