from __future__ import unicode_literals
import operator

import pytest

from context import utils as u
from context import unit as un
from context import units as uns
from context import template as t
from context import exceptions as e
from context import set as s
from helpers import generate_params, mark_params


# Range ***************************************************************

# Fixtures, factories, and test data

class RangeTestType(un.CompoundUnit):

    template = t.CompoundTemplate(
        separator_type=uns.simple.DEFAULT_SEPARATOR_TYPE,
        groups=[
            {'name': 'letters', 'type': uns.Alphabetic, 'min': 1, 'max': 1},
            {'name': 'numbers', 'type': uns.Numeric, 'min': 1, 'max': 1},
        ]
    )


class AnotherRangeTestType(un.CompoundUnit):

    template = t.CompoundTemplate(
        separator_type=uns.simple.DEFAULT_SEPARATOR_TYPE,
        groups=[
            {'name': 'numbers', 'type': uns.Numeric, 'min': 1, 'max': 1},
            {'name': 'letters', 'type': uns.Alphabetic, 'min': 1, 'max': 1},
        ]
    )


def custom_op(op_name):
    def do_it(*args):
        first, others = args[0], args[1:]
        return getattr(first, op_name)(*others)
    do_it.__name__ = str(op_name)
    return do_it


aa0 = RangeTestType('AA 0')
aa50 = RangeTestType('AA 50')
aa100 = RangeTestType('AA 100')
aa1000 = RangeTestType('AA 1000')
aa9999 = RangeTestType('AA 9999')
ab0 = RangeTestType('AB 0')
ab50 = RangeTestType('AB 50')
ab100 = RangeTestType('AB 100')
ab1000 = RangeTestType('AB 1000')
ab9999 = RangeTestType('AB 9999')
c0 = RangeTestType('C 0')
ca0 = RangeTestType('CA 0')

# This is only for testing mixing Unit types when performing Range and
# RangeSet operations.
_10a = AnotherRangeTestType('10 A')
_100a = AnotherRangeTestType('100 A')

RANGE_DATA = {
    # Range 1    |------------------|
    # Range 2    |------------------|
    ((aa0, aa100), (aa0, aa100)): {
        'comparison': [
            (operator.lt, False),
            (operator.le, True),
            (operator.eq, True),
            (operator.ne, False),
            (operator.ge, True),
            (operator.gt, False),
            (operator.contains, True),
            (custom_op('issubset'), True),
            (custom_op('issuperset'), True),
            (custom_op('overlaps'), True),
            (custom_op('isdisjoint'), False),
            (custom_op('issequential'), False),
            (custom_op('extendshigher'), False),
            (custom_op('extendslower'), False),
            (custom_op('isbefore'), False),
            (custom_op('isafter'), False),
        ],
        'creation': [
            (operator.or_, (s.Range(aa0, aa100),)),
            (operator.and_, s.Range(aa0, aa100)),
            (operator.sub, None),
            (operator.xor, None),
        ],
    },
    ((None, aa100), (None, aa100)): {
        'comparison': [
            (operator.lt, False),
            (operator.le, True),
            (operator.eq, True),
            (operator.ne, False),
            (operator.ge, True),
            (operator.gt, False),
            (operator.contains, True),
            (custom_op('issubset'), True),
            (custom_op('issuperset'), True),
            (custom_op('overlaps'), True),
            (custom_op('isdisjoint'), False),
            (custom_op('issequential'), False),
            (custom_op('extendshigher'), False),
            (custom_op('extendslower'), False),
            (custom_op('isbefore'), False),
            (custom_op('isafter'), False),
        ],
        'creation': [
            (operator.or_, (s.Range(None, aa100),)),
            (operator.and_, s.Range(None, aa100)),
            (operator.sub, None),
            (operator.xor, None),
        ],
    },
    ((aa0, None), (aa0, None)): {
        'comparison': [
            (operator.lt, False),
            (operator.le, True),
            (operator.eq, True),
            (operator.ne, False),
            (operator.ge, True),
            (operator.gt, False),
            (operator.contains, True),
            (custom_op('issubset'), True),
            (custom_op('issuperset'), True),
            (custom_op('overlaps'), True),
            (custom_op('isdisjoint'), False),
            (custom_op('issequential'), False),
            (custom_op('extendshigher'), False),
            (custom_op('extendslower'), False),
            (custom_op('isbefore'), False),
            (custom_op('isafter'), False),
        ],
        'creation': [
            (operator.or_, (s.Range(aa0, None),)),
            (operator.and_, s.Range(aa0, None)),
            (operator.sub, None),
            (operator.xor, None),
        ],
    },
    ((None, None), (None, None)): {
        'comparison': [
            (operator.lt, False),
            (operator.le, True),
            (operator.eq, True),
            (operator.ne, False),
            (operator.ge, True),
            (operator.gt, False),
            (operator.contains, True),
            (custom_op('issubset'), True),
            (custom_op('issuperset'), True),
            (custom_op('overlaps'), True),
            (custom_op('isdisjoint'), False),
            (custom_op('issequential'), False),
            (custom_op('extendshigher'), False),
            (custom_op('extendslower'), False),
            (custom_op('isbefore'), False),
            (custom_op('isafter'), False),
        ],
        'creation': [
            (operator.or_, (s.Range(None, None),)),
            (operator.and_, s.Range(None, None)),
            (operator.sub, None),
            (operator.xor, None),
        ],
    },

    # Range 1    |----------|
    # Range 2    |------------------|
    ((aa0, aa100), (aa0, ab0)): {
        'comparison': [
            (operator.lt, True),
            (operator.le, True),
            (operator.eq, False),
            (operator.ne, True),
            (operator.ge, False),
            (operator.gt, False),
            (operator.contains, False),
            (custom_op('issubset'), True),
            (custom_op('issuperset'), False),
            (custom_op('overlaps'), True),
            (custom_op('isdisjoint'), False),
            (custom_op('issequential'), False),
            (custom_op('extendshigher'), False),
            (custom_op('extendslower'), False),
            (custom_op('isbefore'), False),
            (custom_op('isafter'), False),
        ],
        'creation': [
            (operator.or_, (s.Range(aa0, ab0),)),
            (operator.and_, s.Range(aa0, aa100)),
            (operator.sub, None),
            (operator.xor, (s.Range(aa100, ab0),)),
        ],
    },
    ((aa0, aa100), (aa0, None)): {
        'comparison': [
            (operator.lt, True),
            (operator.le, True),
            (operator.eq, False),
            (operator.ne, True),
            (operator.ge, False),
            (operator.gt, False),
            (operator.contains, False),
            (custom_op('issubset'), True),
            (custom_op('issuperset'), False),
            (custom_op('overlaps'), True),
            (custom_op('isdisjoint'), False),
            (custom_op('issequential'), False),
            (custom_op('extendshigher'), False),
            (custom_op('extendslower'), False),
            (custom_op('isbefore'), False),
            (custom_op('isafter'), False),
        ],
        'creation': [
            (operator.or_, (s.Range(aa0, None),)),
            (operator.and_, s.Range(aa0, aa100)),
            (operator.sub, None),
            (operator.xor, (s.Range(aa100, None),)),
        ],
    },
    ((None, aa100), (None, ab0)): {
        'comparison': [
            (operator.lt, True),
            (operator.le, True),
            (operator.eq, False),
            (operator.ne, True),
            (operator.ge, False),
            (operator.gt, False),
            (operator.contains, False),
            (custom_op('issubset'), True),
            (custom_op('issuperset'), False),
            (custom_op('overlaps'), True),
            (custom_op('isdisjoint'), False),
            (custom_op('issequential'), False),
            (custom_op('extendshigher'), False),
            (custom_op('extendslower'), False),
            (custom_op('isbefore'), False),
            (custom_op('isafter'), False),
        ],
        'creation': [
            (operator.or_, (s.Range(None, ab0),)),
            (operator.and_, s.Range(None, aa100)),
            (operator.sub, None),
            (operator.xor, (s.Range(aa100, ab0),)),
        ],
    },
    ((None, aa100), (None, None)): {
        'comparison': [
            (operator.lt, True),
            (operator.le, True),
            (operator.eq, False),
            (operator.ne, True),
            (operator.ge, False),
            (operator.gt, False),
            (operator.contains, False),
            (custom_op('issubset'), True),
            (custom_op('issuperset'), False),
            (custom_op('overlaps'), True),
            (custom_op('isdisjoint'), False),
            (custom_op('issequential'), False),
            (custom_op('extendshigher'), False),
            (custom_op('extendslower'), False),
            (custom_op('isbefore'), False),
            (custom_op('isafter'), False),
        ],
        'creation': [
            (operator.or_, (s.Range(None, None),)),
            (operator.and_, s.Range(None, aa100)),
            (operator.sub, None),
            (operator.xor, (s.Range(aa100, None),)),
        ],
    },

    # Range 1        |----------|
    # Range 2    |------------------|
    ((aa100, ab0), (aa0, ab100)): {
        'comparison': [
            (operator.lt, True),
            (operator.le, True),
            (operator.eq, False),
            (operator.ne, True),
            (operator.ge, False),
            (operator.gt, False),
            (operator.contains, False),
            (custom_op('issubset'), True),
            (custom_op('issuperset'), False),
            (custom_op('overlaps'), True),
            (custom_op('isdisjoint'), False),
            (custom_op('issequential'), False),
            (custom_op('extendshigher'), False),
            (custom_op('extendslower'), False),
            (custom_op('isbefore'), False),
            (custom_op('isafter'), False),
        ],
        'creation': [
            (operator.or_, (s.Range(aa0, ab100),)),
            (operator.and_, s.Range(aa100, ab0)),
            (operator.sub, None),
            (operator.xor, (s.Range(aa0, aa100), s.Range(ab0, ab100))),
        ],
    },
    ((aa100, ab0), (aa0, None)): {
        'comparison': [
            (operator.lt, True),
            (operator.le, True),
            (operator.eq, False),
            (operator.ne, True),
            (operator.ge, False),
            (operator.gt, False),
            (operator.contains, False),
            (custom_op('issubset'), True),
            (custom_op('issuperset'), False),
            (custom_op('overlaps'), True),
            (custom_op('isdisjoint'), False),
            (custom_op('issequential'), False),
            (custom_op('extendshigher'), False),
            (custom_op('extendslower'), False),
            (custom_op('isbefore'), False),
            (custom_op('isafter'), False),
        ],
        'creation': [
            (operator.or_, (s.Range(aa0, None),)),
            (operator.and_, s.Range(aa100, ab0)),
            (operator.sub, None),
            (operator.xor, (s.Range(aa0, aa100), s.Range(ab0, None))),
        ],
    },
    ((aa100, ab0), (None, ab100)): {
        'comparison': [
            (operator.lt, True),
            (operator.le, True),
            (operator.eq, False),
            (operator.ne, True),
            (operator.ge, False),
            (operator.gt, False),
            (operator.contains, False),
            (custom_op('issubset'), True),
            (custom_op('issuperset'), False),
            (custom_op('overlaps'), True),
            (custom_op('isdisjoint'), False),
            (custom_op('issequential'), False),
            (custom_op('extendshigher'), False),
            (custom_op('extendslower'), False),
            (custom_op('isbefore'), False),
            (custom_op('isafter'), False),
        ],
        'creation': [
            (operator.or_, (s.Range(None, ab100),)),
            (operator.and_, s.Range(aa100, ab0)),
            (operator.sub, None),
            (operator.xor, (s.Range(None, aa100), s.Range(ab0, ab100))),
        ],
    },
    ((aa100, ab0), (None, None)): {
        'comparison': [
            (operator.lt, True),
            (operator.le, True),
            (operator.eq, False),
            (operator.ne, True),
            (operator.ge, False),
            (operator.gt, False),
            (operator.contains, False),
            (custom_op('issubset'), True),
            (custom_op('issuperset'), False),
            (custom_op('overlaps'), True),
            (custom_op('isdisjoint'), False),
            (custom_op('issequential'), False),
            (custom_op('extendshigher'), False),
            (custom_op('extendslower'), False),
            (custom_op('isbefore'), False),
            (custom_op('isafter'), False),
        ],
        'creation': [
            (operator.or_, (s.Range(None, None),)),
            (operator.and_, s.Range(aa100, ab0)),
            (operator.sub, None),
            (operator.xor, (s.Range(None, aa100), s.Range(ab0, None))),
        ],
    },

    # Range 1            |----------|
    # Range 2    |------------------|
    ((aa100, ab0), (aa0, ab0)): {
        'comparison': [
            (operator.lt, True),
            (operator.le, True),
            (operator.eq, False),
            (operator.ne, True),
            (operator.ge, False),
            (operator.gt, False),
            (operator.contains, False),
            (custom_op('issubset'), True),
            (custom_op('issuperset'), False),
            (custom_op('overlaps'), True),
            (custom_op('isdisjoint'), False),
            (custom_op('issequential'), False),
            (custom_op('extendshigher'), False),
            (custom_op('extendslower'), False),
            (custom_op('isbefore'), False),
            (custom_op('isafter'), False),
        ],
        'creation': [
            (operator.or_, (s.Range(aa0, ab0),)),
            (operator.and_, s.Range(aa100, ab0)),
            (operator.sub, None),
            (operator.xor, (s.Range(aa0, aa100),)),
        ],
    },
    ((aa100, ab0), (None, ab0)): {
        'comparison': [
            (operator.lt, True),
            (operator.le, True),
            (operator.eq, False),
            (operator.ne, True),
            (operator.ge, False),
            (operator.gt, False),
            (operator.contains, False),
            (custom_op('issubset'), True),
            (custom_op('issuperset'), False),
            (custom_op('overlaps'), True),
            (custom_op('isdisjoint'), False),
            (custom_op('issequential'), False),
            (custom_op('extendshigher'), False),
            (custom_op('extendslower'), False),
            (custom_op('isbefore'), False),
            (custom_op('isafter'), False),
        ],
        'creation': [
            (operator.or_, (s.Range(None, ab0),)),
            (operator.and_, s.Range(aa100, ab0)),
            (operator.sub, None),
            (operator.xor, (s.Range(None, aa100),)),
        ],
    },
    ((aa100, None), (aa0, None)): {
        'comparison': [
            (operator.lt, True),
            (operator.le, True),
            (operator.eq, False),
            (operator.ne, True),
            (operator.ge, False),
            (operator.gt, False),
            (operator.contains, False),
            (custom_op('issubset'), True),
            (custom_op('issuperset'), False),
            (custom_op('overlaps'), True),
            (custom_op('isdisjoint'), False),
            (custom_op('issequential'), False),
            (custom_op('extendshigher'), False),
            (custom_op('extendslower'), False),
            (custom_op('isbefore'), False),
            (custom_op('isafter'), False),
        ],
        'creation': [
            (operator.or_, (s.Range(aa0, None),)),
            (operator.and_, s.Range(aa100, None)),
            (operator.sub, None),
            (operator.xor, (s.Range(aa0, aa100),)),
        ],
    },
    ((aa100, None), (None, None)): {
        'comparison': [
            (operator.lt, True),
            (operator.le, True),
            (operator.eq, False),
            (operator.ne, True),
            (operator.ge, False),
            (operator.gt, False),
            (operator.contains, False),
            (custom_op('issubset'), True),
            (custom_op('issuperset'), False),
            (custom_op('overlaps'), True),
            (custom_op('isdisjoint'), False),
            (custom_op('issequential'), False),
            (custom_op('extendshigher'), False),
            (custom_op('extendslower'), False),
            (custom_op('isbefore'), False),
            (custom_op('isafter'), False),
        ],
        'creation': [
            (operator.or_, (s.Range(None, None),)),
            (operator.and_, s.Range(aa100, None)),
            (operator.sub, None),
            (operator.xor, (s.Range(None, aa100),)),
        ],
    },

    # Range 1            |------------------|
    # Range 2    |------------------|
    ((aa100, ab100), (aa0, ab0)): {
        'comparison': [
            (operator.lt, False),
            (operator.le, False),
            (operator.eq, False),
            (operator.ne, True),
            (operator.ge, False),
            (operator.gt, False),
            (operator.contains, False),
            (custom_op('issubset'), False),
            (custom_op('issuperset'), False),
            (custom_op('overlaps'), True),
            (custom_op('isdisjoint'), False),
            (custom_op('issequential'), False),
            (custom_op('extendshigher'), True),
            (custom_op('extendslower'), False),
            (custom_op('isbefore'), False),
            (custom_op('isafter'), False),
        ],
        'creation': [
            (operator.or_, (s.Range(aa0, ab100),)),
            (operator.and_, s.Range(aa100, ab0)),
            (operator.sub, (s.Range(ab0, ab100),)),
            (operator.xor, (s.Range(aa0, aa100), s.Range(ab0, ab100))),
        ],
    },
    ((aa100, ab100), (None, ab0)): {
        'comparison': [
            (operator.lt, False),
            (operator.le, False),
            (operator.eq, False),
            (operator.ne, True),
            (operator.ge, False),
            (operator.gt, False),
            (operator.contains, False),
            (custom_op('issubset'), False),
            (custom_op('issuperset'), False),
            (custom_op('overlaps'), True),
            (custom_op('isdisjoint'), False),
            (custom_op('issequential'), False),
            (custom_op('extendshigher'), True),
            (custom_op('extendslower'), False),
            (custom_op('isbefore'), False),
            (custom_op('isafter'), False),
        ],
        'creation': [
            (operator.or_, (s.Range(None, ab100),)),
            (operator.and_, s.Range(aa100, ab0)),
            (operator.sub, (s.Range(ab0, ab100),)),
            (operator.xor, (s.Range(None, aa100), s.Range(ab0, ab100))),
        ],
    },
    ((aa100, None), (aa0, ab0)): {
        'comparison': [
            (operator.lt, False),
            (operator.le, False),
            (operator.eq, False),
            (operator.ne, True),
            (operator.ge, False),
            (operator.gt, False),
            (operator.contains, False),
            (custom_op('issubset'), False),
            (custom_op('issuperset'), False),
            (custom_op('overlaps'), True),
            (custom_op('isdisjoint'), False),
            (custom_op('issequential'), False),
            (custom_op('extendshigher'), True),
            (custom_op('extendslower'), False),
            (custom_op('isbefore'), False),
            (custom_op('isafter'), False),
        ],
        'creation': [
            (operator.or_, (s.Range(aa0, None),)),
            (operator.and_, s.Range(aa100, ab0)),
            (operator.sub, (s.Range(ab0, None),)),
            (operator.xor, (s.Range(aa0, aa100), s.Range(ab0, None))),
        ],
    },
    ((aa100, None), (None, ab0)): {
        'comparison': [
            (operator.lt, False),
            (operator.le, False),
            (operator.eq, False),
            (operator.ne, True),
            (operator.ge, False),
            (operator.gt, False),
            (operator.contains, False),
            (custom_op('issubset'), False),
            (custom_op('issuperset'), False),
            (custom_op('overlaps'), True),
            (custom_op('isdisjoint'), False),
            (custom_op('issequential'), False),
            (custom_op('extendshigher'), True),
            (custom_op('extendslower'), False),
            (custom_op('isbefore'), False),
            (custom_op('isafter'), False),
        ],
        'creation': [
            (operator.or_, (s.Range(None, None),)),
            (operator.and_, s.Range(aa100, ab0)),
            (operator.sub, (s.Range(ab0, None),)),
            (operator.xor, (s.Range(None, aa100), s.Range(ab0, None))),
        ],
    },

    # Range 1                        |------------------|
    # Range 2    |------------------|
    ((aa100, ab0), (aa0, aa100)): {
        'comparison': [
            (operator.lt, False),
            (operator.le, False),
            (operator.eq, False),
            (operator.ne, True),
            (operator.ge, False),
            (operator.gt, False),
            (operator.contains, False),
            (custom_op('issubset'), False),
            (custom_op('issuperset'), False),
            (custom_op('overlaps'), False),
            (custom_op('isdisjoint'), True),
            (custom_op('issequential'), True),
            (custom_op('extendshigher'), True),
            (custom_op('extendslower'), False),
            (custom_op('isbefore'), False),
            (custom_op('isafter'), True),
        ],
        'creation': [
            (operator.or_, (s.Range(aa0, ab0),)),
            (operator.and_, None),
            (operator.sub, (s.Range(aa100, ab0),)),
            (operator.xor, (s.Range(aa0, aa100), s.Range(aa100, ab0))),
        ],
    },
    ((aa100, ab0), (None, aa100)): {
        'comparison': [
            (operator.lt, False),
            (operator.le, False),
            (operator.eq, False),
            (operator.ne, True),
            (operator.ge, False),
            (operator.gt, False),
            (operator.contains, False),
            (custom_op('issubset'), False),
            (custom_op('issuperset'), False),
            (custom_op('overlaps'), False),
            (custom_op('isdisjoint'), True),
            (custom_op('issequential'), True),
            (custom_op('extendshigher'), True),
            (custom_op('extendslower'), False),
            (custom_op('isbefore'), False),
            (custom_op('isafter'), True),
        ],
        'creation': [
            (operator.or_, (s.Range(None, ab0),)),
            (operator.and_, None),
            (operator.sub, (s.Range(aa100, ab0),)),
            (operator.xor, (s.Range(None, aa100), s.Range(aa100, ab0))),
        ],
    },
    ((aa100, None), (aa0, aa100)): {
        'comparison': [
            (operator.lt, False),
            (operator.le, False),
            (operator.eq, False),
            (operator.ne, True),
            (operator.ge, False),
            (operator.gt, False),
            (operator.contains, False),
            (custom_op('issubset'), False),
            (custom_op('issuperset'), False),
            (custom_op('overlaps'), False),
            (custom_op('isdisjoint'), True),
            (custom_op('issequential'), True),
            (custom_op('extendshigher'), True),
            (custom_op('extendslower'), False),
            (custom_op('isbefore'), False),
            (custom_op('isafter'), True),
        ],
        'creation': [
            (operator.or_, (s.Range(aa0, None),)),
            (operator.and_, None),
            (operator.sub, (s.Range(aa100, None),)),
            (operator.xor, (s.Range(aa0, aa100), s.Range(aa100, None))),
        ],
    },
    ((aa100, None), (None, aa100)): {
        'comparison': [
            (operator.lt, False),
            (operator.le, False),
            (operator.eq, False),
            (operator.ne, True),
            (operator.ge, False),
            (operator.gt, False),
            (operator.contains, False),
            (custom_op('issubset'), False),
            (custom_op('issuperset'), False),
            (custom_op('overlaps'), False),
            (custom_op('isdisjoint'), True),
            (custom_op('issequential'), True),
            (custom_op('extendshigher'), True),
            (custom_op('extendslower'), False),
            (custom_op('isbefore'), False),
            (custom_op('isafter'), True),
        ],
        'creation': [
            (operator.or_, (s.Range(None, None),)),
            (operator.and_, None),
            (operator.sub, (s.Range(aa100, None),)),
            (operator.xor, (s.Range(None, aa100), s.Range(aa100, None))),
        ],
    },

    # Range 1                            |------------------|
    # Range 2    |------------------|
    ((ab0, ab100), (aa0, aa100)): {
        'comparison': [
            (operator.lt, False),
            (operator.le, False),
            (operator.eq, False),
            (operator.ne, True),
            (operator.ge, False),
            (operator.gt, False),
            (operator.contains, False),
            (custom_op('issubset'), False),
            (custom_op('issuperset'), False),
            (custom_op('overlaps'), False),
            (custom_op('isdisjoint'), True),
            (custom_op('issequential'), False),
            (custom_op('extendshigher'), True),
            (custom_op('extendslower'), False),
            (custom_op('isbefore'), False),
            (custom_op('isafter'), True),
        ],
        'creation': [
            (operator.or_, (s.Range(aa0, aa100), s.Range(ab0, ab100))),
            (operator.and_, None),
            (operator.sub, (s.Range(ab0, ab100),)),
            (operator.xor, (s.Range(aa0, aa100), s.Range(ab0, ab100))),
        ],
    },
    ((ab0, ab100), (None, aa100)): {
        'comparison': [
            (operator.lt, False),
            (operator.le, False),
            (operator.eq, False),
            (operator.ne, True),
            (operator.ge, False),
            (operator.gt, False),
            (operator.contains, False),
            (custom_op('issubset'), False),
            (custom_op('issuperset'), False),
            (custom_op('overlaps'), False),
            (custom_op('isdisjoint'), True),
            (custom_op('issequential'), False),
            (custom_op('extendshigher'), True),
            (custom_op('extendslower'), False),
            (custom_op('isbefore'), False),
            (custom_op('isafter'), True),
        ],
        'creation': [
            (operator.or_, (s.Range(None, aa100), s.Range(ab0, ab100))),
            (operator.and_, None),
            (operator.sub, (s.Range(ab0, ab100),)),
            (operator.xor, (s.Range(None, aa100), s.Range(ab0, ab100))),
        ],
    },
    ((ab0, None), (aa0, aa100)): {
        'comparison': [
            (operator.lt, False),
            (operator.le, False),
            (operator.eq, False),
            (operator.ne, True),
            (operator.ge, False),
            (operator.gt, False),
            (operator.contains, False),
            (custom_op('issubset'), False),
            (custom_op('issuperset'), False),
            (custom_op('overlaps'), False),
            (custom_op('isdisjoint'), True),
            (custom_op('issequential'), False),
            (custom_op('extendshigher'), True),
            (custom_op('extendslower'), False),
            (custom_op('isbefore'), False),
            (custom_op('isafter'), True),
        ],
        'creation': [
            (operator.or_, (s.Range(aa0, aa100), s.Range(ab0, None))),
            (operator.and_, None),
            (operator.sub, (s.Range(ab0, None),)),
            (operator.xor, (s.Range(aa0, aa100), s.Range(ab0, None))),
        ],
    },
    ((ab0, None), (None, aa100)): {
        'comparison': [
            (operator.lt, False),
            (operator.le, False),
            (operator.eq, False),
            (operator.ne, True),
            (operator.ge, False),
            (operator.gt, False),
            (operator.contains, False),
            (custom_op('issubset'), False),
            (custom_op('issuperset'), False),
            (custom_op('overlaps'), False),
            (custom_op('isdisjoint'), True),
            (custom_op('issequential'), False),
            (custom_op('extendshigher'), True),
            (custom_op('extendslower'), False),
            (custom_op('isbefore'), False),
            (custom_op('isafter'), True),
        ],
        'creation': [
            (operator.or_, (s.Range(None, aa100), s.Range(ab0, None))),
            (operator.and_, None),
            (operator.sub, (s.Range(ab0, None),)),
            (operator.xor, (s.Range(None, aa100), s.Range(ab0, None))),
        ],
    },

    # Range 1    |------------------|
    # Range 2    |----------|
    ((aa0, ab0), (aa0, aa100)): {
        'comparison': [
            (operator.lt, False),
            (operator.le, False),
            (operator.eq, False),
            (operator.ne, True),
            (operator.ge, True),
            (operator.gt, True),
            (operator.contains, True),
            (custom_op('issubset'), False),
            (custom_op('issuperset'), True),
            (custom_op('overlaps'), True),
            (custom_op('isdisjoint'), False),
            (custom_op('issequential'), False),
            (custom_op('extendshigher'), True),
            (custom_op('extendslower'), False),
            (custom_op('isbefore'), False),
            (custom_op('isafter'), False),
        ],
        'creation': [
            (operator.or_, (s.Range(aa0, ab0),)),
            (operator.and_, s.Range(aa0, aa100)),
            (operator.sub, (s.Range(aa100, ab0),)),
            (operator.xor, (s.Range(aa100, ab0),)),
        ],
    },
    ((aa0, None), (aa0, aa100)): {
        'comparison': [
            (operator.lt, False),
            (operator.le, False),
            (operator.eq, False),
            (operator.ne, True),
            (operator.ge, True),
            (operator.gt, True),
            (operator.contains, True),
            (custom_op('issubset'), False),
            (custom_op('issuperset'), True),
            (custom_op('overlaps'), True),
            (custom_op('isdisjoint'), False),
            (custom_op('issequential'), False),
            (custom_op('extendshigher'), True),
            (custom_op('extendslower'), False),
            (custom_op('isbefore'), False),
            (custom_op('isafter'), False),
        ],
        'creation': [
            (operator.or_, (s.Range(aa0, None),)),
            (operator.and_, s.Range(aa0, aa100)),
            (operator.sub, (s.Range(aa100, None),)),
            (operator.xor, (s.Range(aa100, None),)),
        ],
    },
    ((None, ab0), (None, aa100)): {
        'comparison': [
            (operator.lt, False),
            (operator.le, False),
            (operator.eq, False),
            (operator.ne, True),
            (operator.ge, True),
            (operator.gt, True),
            (operator.contains, True),
            (custom_op('issubset'), False),
            (custom_op('issuperset'), True),
            (custom_op('overlaps'), True),
            (custom_op('isdisjoint'), False),
            (custom_op('issequential'), False),
            (custom_op('extendshigher'), True),
            (custom_op('extendslower'), False),
            (custom_op('isbefore'), False),
            (custom_op('isafter'), False),
        ],
        'creation': [
            (operator.or_, (s.Range(None, ab0),)),
            (operator.and_, s.Range(None, aa100)),
            (operator.sub, (s.Range(aa100, ab0),)),
            (operator.xor, (s.Range(aa100, ab0),)),
        ],
    },
    ((None, None), (None, aa100)): {
        'comparison': [
            (operator.lt, False),
            (operator.le, False),
            (operator.eq, False),
            (operator.ne, True),
            (operator.ge, True),
            (operator.gt, True),
            (operator.contains, True),
            (custom_op('issubset'), False),
            (custom_op('issuperset'), True),
            (custom_op('overlaps'), True),
            (custom_op('isdisjoint'), False),
            (custom_op('issequential'), False),
            (custom_op('extendshigher'), True),
            (custom_op('extendslower'), False),
            (custom_op('isbefore'), False),
            (custom_op('isafter'), False),
        ],
        'creation': [
            (operator.or_, (s.Range(None, None),)),
            (operator.and_, s.Range(None, aa100)),
            (operator.sub, (s.Range(aa100, None),)),
            (operator.xor, (s.Range(aa100, None),)),
        ],
    },


    # Range 1    |------------------|
    # Range 2        |----------|
    ((aa0, ab100), (aa100, ab0)): {
        'comparison': [
            (operator.lt, False),
            (operator.le, False),
            (operator.eq, False),
            (operator.ne, True),
            (operator.ge, True),
            (operator.gt, True),
            (operator.contains, True),
            (custom_op('issubset'), False),
            (custom_op('issuperset'), True),
            (custom_op('overlaps'), True),
            (custom_op('isdisjoint'), False),
            (custom_op('issequential'), False),
            (custom_op('extendshigher'), True),
            (custom_op('extendslower'), True),
            (custom_op('isbefore'), False),
            (custom_op('isafter'), False),
        ],
        'creation': [
            (operator.or_, (s.Range(aa0, ab100),)),
            (operator.and_, s.Range(aa100, ab0)),
            (operator.sub, (s.Range(aa0, aa100), s.Range(ab0, ab100))),
            (operator.xor, (s.Range(aa0, aa100), s.Range(ab0, ab100))),
        ],
    },
    ((None, ab100), (aa100, ab0)): {
        'comparison': [
            (operator.lt, False),
            (operator.le, False),
            (operator.eq, False),
            (operator.ne, True),
            (operator.ge, True),
            (operator.gt, True),
            (operator.contains, True),
            (custom_op('issubset'), False),
            (custom_op('issuperset'), True),
            (custom_op('overlaps'), True),
            (custom_op('isdisjoint'), False),
            (custom_op('issequential'), False),
            (custom_op('extendshigher'), True),
            (custom_op('extendslower'), True),
            (custom_op('isbefore'), False),
            (custom_op('isafter'), False),
        ],
        'creation': [
            (operator.or_, (s.Range(None, ab100),)),
            (operator.and_, s.Range(aa100, ab0)),
            (operator.sub, (s.Range(None, aa100), s.Range(ab0, ab100))),
            (operator.xor, (s.Range(None, aa100), s.Range(ab0, ab100))),
        ],
    },
    ((aa0, None), (aa100, ab0)): {
        'comparison': [
            (operator.lt, False),
            (operator.le, False),
            (operator.eq, False),
            (operator.ne, True),
            (operator.ge, True),
            (operator.gt, True),
            (operator.contains, True),
            (custom_op('issubset'), False),
            (custom_op('issuperset'), True),
            (custom_op('overlaps'), True),
            (custom_op('isdisjoint'), False),
            (custom_op('issequential'), False),
            (custom_op('extendshigher'), True),
            (custom_op('extendslower'), True),
            (custom_op('isbefore'), False),
            (custom_op('isafter'), False),
        ],
        'creation': [
            (operator.or_, (s.Range(aa0, None),)),
            (operator.and_, s.Range(aa100, ab0)),
            (operator.sub, (s.Range(aa0, aa100), s.Range(ab0, None))),
            (operator.xor, (s.Range(aa0, aa100), s.Range(ab0, None))),
        ],
    },
    ((None, None), (aa100, ab0)): {
        'comparison': [
            (operator.lt, False),
            (operator.le, False),
            (operator.eq, False),
            (operator.ne, True),
            (operator.ge, True),
            (operator.gt, True),
            (operator.contains, True),
            (custom_op('issubset'), False),
            (custom_op('issuperset'), True),
            (custom_op('overlaps'), True),
            (custom_op('isdisjoint'), False),
            (custom_op('issequential'), False),
            (custom_op('extendshigher'), True),
            (custom_op('extendslower'), True),
            (custom_op('isbefore'), False),
            (custom_op('isafter'), False),
        ],
        'creation': [
            (operator.or_, (s.Range(None, None),)),
            (operator.and_, s.Range(aa100, ab0)),
            (operator.sub, (s.Range(None, aa100), s.Range(ab0, None))),
            (operator.xor, (s.Range(None, aa100), s.Range(ab0, None))),
        ],
    },

    # Range 1    |------------------|
    # Range 2            |----------|
    ((aa0, ab0), (aa100, ab0)): {
        'comparison': [
            (operator.lt, False),
            (operator.le, False),
            (operator.eq, False),
            (operator.ne, True),
            (operator.ge, True),
            (operator.gt, True),
            (operator.contains, True),
            (custom_op('issubset'), False),
            (custom_op('issuperset'), True),
            (custom_op('overlaps'), True),
            (custom_op('isdisjoint'), False),
            (custom_op('issequential'), False),
            (custom_op('extendshigher'), False),
            (custom_op('extendslower'), True),
            (custom_op('isbefore'), False),
            (custom_op('isafter'), False),
        ],
        'creation': [
            (operator.or_, (s.Range(aa0, ab0),)),
            (operator.and_, s.Range(aa100, ab0)),
            (operator.sub, (s.Range(aa0, aa100),)),
            (operator.xor, (s.Range(aa0, aa100),)),
        ],
    },
    ((None, ab0), (aa100, ab0)): {
        'comparison': [
            (operator.lt, False),
            (operator.le, False),
            (operator.eq, False),
            (operator.ne, True),
            (operator.ge, True),
            (operator.gt, True),
            (operator.contains, True),
            (custom_op('issubset'), False),
            (custom_op('issuperset'), True),
            (custom_op('overlaps'), True),
            (custom_op('isdisjoint'), False),
            (custom_op('issequential'), False),
            (custom_op('extendshigher'), False),
            (custom_op('extendslower'), True),
            (custom_op('isbefore'), False),
            (custom_op('isafter'), False),
        ],
        'creation': [
            (operator.or_, (s.Range(None, ab0),)),
            (operator.and_, s.Range(aa100, ab0)),
            (operator.sub, (s.Range(None, aa100),)),
            (operator.xor, (s.Range(None, aa100),)),
        ],
    },
    ((aa0, None), (aa100, None)): {
        'comparison': [
            (operator.lt, False),
            (operator.le, False),
            (operator.eq, False),
            (operator.ne, True),
            (operator.ge, True),
            (operator.gt, True),
            (operator.contains, True),
            (custom_op('issubset'), False),
            (custom_op('issuperset'), True),
            (custom_op('overlaps'), True),
            (custom_op('isdisjoint'), False),
            (custom_op('issequential'), False),
            (custom_op('extendshigher'), False),
            (custom_op('extendslower'), True),
            (custom_op('isbefore'), False),
            (custom_op('isafter'), False),
        ],
        'creation': [
            (operator.or_, (s.Range(aa0, None),)),
            (operator.and_, s.Range(aa100, None)),
            (operator.sub, (s.Range(aa0, aa100),)),
            (operator.xor, (s.Range(aa0, aa100),)),
        ],
    },
    ((None, None), (aa100, None)): {
        'comparison': [
            (operator.lt, False),
            (operator.le, False),
            (operator.eq, False),
            (operator.ne, True),
            (operator.ge, True),
            (operator.gt, True),
            (operator.contains, True),
            (custom_op('issubset'), False),
            (custom_op('issuperset'), True),
            (custom_op('overlaps'), True),
            (custom_op('isdisjoint'), False),
            (custom_op('issequential'), False),
            (custom_op('extendshigher'), False),
            (custom_op('extendslower'), True),
            (custom_op('isbefore'), False),
            (custom_op('isafter'), False),
        ],
        'creation': [
            (operator.or_, (s.Range(None, None),)),
            (operator.and_, s.Range(aa100, None)),
            (operator.sub, (s.Range(None, aa100),)),
            (operator.xor, (s.Range(None, aa100),)),
        ],
    },

    # Range 1    |------------------|
    # Range 2            |------------------|
    ((aa0, ab0), (aa100, ab100)): {
        'comparison': [
            (operator.lt, False),
            (operator.le, False),
            (operator.eq, False),
            (operator.ne, True),
            (operator.ge, False),
            (operator.gt, False),
            (operator.contains, False),
            (custom_op('issubset'), False),
            (custom_op('issuperset'), False),
            (custom_op('overlaps'), True),
            (custom_op('isdisjoint'), False),
            (custom_op('issequential'), False),
            (custom_op('extendshigher'), False),
            (custom_op('extendslower'), True),
            (custom_op('isbefore'), False),
            (custom_op('isafter'), False),
        ],
        'creation': [
            (operator.or_, (s.Range(aa0, ab100),)),
            (operator.and_, s.Range(aa100, ab0)),
            (operator.sub, (s.Range(aa0, aa100),)),
            (operator.xor, (s.Range(aa0, aa100), s.Range(ab0, ab100))),
        ],
    },
    ((aa0, ab0), (aa100, None)): {
        'comparison': [
            (operator.lt, False),
            (operator.le, False),
            (operator.eq, False),
            (operator.ne, True),
            (operator.ge, False),
            (operator.gt, False),
            (operator.contains, False),
            (custom_op('issubset'), False),
            (custom_op('issuperset'), False),
            (custom_op('overlaps'), True),
            (custom_op('isdisjoint'), False),
            (custom_op('issequential'), False),
            (custom_op('extendshigher'), False),
            (custom_op('extendslower'), True),
            (custom_op('isbefore'), False),
            (custom_op('isafter'), False),
        ],
        'creation': [
            (operator.or_, (s.Range(aa0, None),)),
            (operator.and_, s.Range(aa100, ab0)),
            (operator.sub, (s.Range(aa0, aa100),)),
            (operator.xor, (s.Range(aa0, aa100), s.Range(ab0, None))),
        ],
    },
    ((None, ab0), (aa100, ab100)): {
        'comparison': [
            (operator.lt, False),
            (operator.le, False),
            (operator.eq, False),
            (operator.ne, True),
            (operator.ge, False),
            (operator.gt, False),
            (operator.contains, False),
            (custom_op('issubset'), False),
            (custom_op('issuperset'), False),
            (custom_op('overlaps'), True),
            (custom_op('isdisjoint'), False),
            (custom_op('issequential'), False),
            (custom_op('extendshigher'), False),
            (custom_op('extendslower'), True),
            (custom_op('isbefore'), False),
            (custom_op('isafter'), False),
        ],
        'creation': [
            (operator.or_, (s.Range(None, ab100),)),
            (operator.and_, s.Range(aa100, ab0)),
            (operator.sub, (s.Range(None, aa100),)),
            (operator.xor, (s.Range(None, aa100), s.Range(ab0, ab100))),
        ],
    },
    ((None, ab0), (aa100, None)): {
        'comparison': [
            (operator.lt, False),
            (operator.le, False),
            (operator.eq, False),
            (operator.ne, True),
            (operator.ge, False),
            (operator.gt, False),
            (operator.contains, False),
            (custom_op('issubset'), False),
            (custom_op('issuperset'), False),
            (custom_op('overlaps'), True),
            (custom_op('isdisjoint'), False),
            (custom_op('issequential'), False),
            (custom_op('extendshigher'), False),
            (custom_op('extendslower'), True),
            (custom_op('isbefore'), False),
            (custom_op('isafter'), False),
        ],
        'creation': [
            (operator.or_, (s.Range(None, None),)),
            (operator.and_, s.Range(aa100, ab0)),
            (operator.sub, (s.Range(None, aa100),)),
            (operator.xor, (s.Range(None, aa100), s.Range(ab0, None))),
        ],
    },

    # Range 1    |------------------|
    # Range 2                        |------------------|
    ((aa0, aa100), (aa100, ab0)): {
        'comparison': [
            (operator.lt, False),
            (operator.le, False),
            (operator.eq, False),
            (operator.ne, True),
            (operator.ge, False),
            (operator.gt, False),
            (operator.contains, False),
            (custom_op('issubset'), False),
            (custom_op('issuperset'), False),
            (custom_op('overlaps'), False),
            (custom_op('isdisjoint'), True),
            (custom_op('issequential'), True),
            (custom_op('extendshigher'), False),
            (custom_op('extendslower'), True),
            (custom_op('isbefore'), True),
            (custom_op('isafter'), False),
        ],
        'creation': [
            (operator.or_, (s.Range(aa0, ab0),)),
            (operator.and_, None),
            (operator.sub, (s.Range(aa0, aa100),)),
            (operator.xor, (s.Range(aa0, aa100), s.Range(aa100, ab0))),
        ],
    },
    ((aa0, aa100), (aa100, None)): {
        'comparison': [
            (operator.lt, False),
            (operator.le, False),
            (operator.eq, False),
            (operator.ne, True),
            (operator.ge, False),
            (operator.gt, False),
            (operator.contains, False),
            (custom_op('issubset'), False),
            (custom_op('issuperset'), False),
            (custom_op('overlaps'), False),
            (custom_op('isdisjoint'), True),
            (custom_op('issequential'), True),
            (custom_op('extendshigher'), False),
            (custom_op('extendslower'), True),
            (custom_op('isbefore'), True),
            (custom_op('isafter'), False),
        ],
        'creation': [
            (operator.or_, (s.Range(aa0, None),)),
            (operator.and_, None),
            (operator.sub, (s.Range(aa0, aa100),)),
            (operator.xor, (s.Range(aa0, aa100), s.Range(aa100, None))),
        ],
    },
    ((None, aa100), (aa100, ab0)): {
        'comparison': [
            (operator.lt, False),
            (operator.le, False),
            (operator.eq, False),
            (operator.ne, True),
            (operator.ge, False),
            (operator.gt, False),
            (operator.contains, False),
            (custom_op('issubset'), False),
            (custom_op('issuperset'), False),
            (custom_op('overlaps'), False),
            (custom_op('isdisjoint'), True),
            (custom_op('issequential'), True),
            (custom_op('extendshigher'), False),
            (custom_op('extendslower'), True),
            (custom_op('isbefore'), True),
            (custom_op('isafter'), False),
        ],
        'creation': [
            (operator.or_, (s.Range(None, ab0),)),
            (operator.and_, None),
            (operator.sub, (s.Range(None, aa100),)),
            (operator.xor, (s.Range(None, aa100), s.Range(aa100, ab0))),
        ],
    },
    ((None, aa100), (aa100, None)): {
        'comparison': [
            (operator.lt, False),
            (operator.le, False),
            (operator.eq, False),
            (operator.ne, True),
            (operator.ge, False),
            (operator.gt, False),
            (operator.contains, False),
            (custom_op('issubset'), False),
            (custom_op('issuperset'), False),
            (custom_op('overlaps'), False),
            (custom_op('isdisjoint'), True),
            (custom_op('issequential'), True),
            (custom_op('extendshigher'), False),
            (custom_op('extendslower'), True),
            (custom_op('isbefore'), True),
            (custom_op('isafter'), False),
        ],
        'creation': [
            (operator.or_, (s.Range(None, None),)),
            (operator.and_, None),
            (operator.sub, (s.Range(None, aa100),)),
            (operator.xor, (s.Range(None, aa100), s.Range(aa100, None))),
        ],
    },

    # Range 1    |------------------|
    # Range 2                            |------------------|
    ((aa0, aa100), (ab0, ab100)): {
        'comparison': [
            (operator.lt, False),
            (operator.le, False),
            (operator.eq, False),
            (operator.ne, True),
            (operator.ge, False),
            (operator.gt, False),
            (operator.contains, False),
            (custom_op('issubset'), False),
            (custom_op('issuperset'), False),
            (custom_op('overlaps'), False),
            (custom_op('isdisjoint'), True),
            (custom_op('issequential'), False),
            (custom_op('extendshigher'), False),
            (custom_op('extendslower'), True),
            (custom_op('isbefore'), True),
            (custom_op('isafter'), False),
        ],
        'creation': [
            (operator.or_, (s.Range(aa0, aa100), s.Range(ab0, ab100))),
            (operator.and_, None),
            (operator.sub, (s.Range(aa0, aa100),)),
            (operator.xor, (s.Range(aa0, aa100), s.Range(ab0, ab100))),
        ],
    },
    ((aa0, aa100), (ab0, None)): {
        'comparison': [
            (operator.lt, False),
            (operator.le, False),
            (operator.eq, False),
            (operator.ne, True),
            (operator.ge, False),
            (operator.gt, False),
            (operator.contains, False),
            (custom_op('issubset'), False),
            (custom_op('issuperset'), False),
            (custom_op('overlaps'), False),
            (custom_op('isdisjoint'), True),
            (custom_op('issequential'), False),
            (custom_op('extendshigher'), False),
            (custom_op('extendslower'), True),
            (custom_op('isbefore'), True),
            (custom_op('isafter'), False),
        ],
        'creation': [
            (operator.or_, (s.Range(aa0, aa100), s.Range(ab0, None))),
            (operator.and_, None),
            (operator.sub, (s.Range(aa0, aa100),)),
            (operator.xor, (s.Range(aa0, aa100), s.Range(ab0, None))),
        ],
    },
    ((None, aa100), (ab0, ab100)): {
        'comparison': [
            (operator.lt, False),
            (operator.le, False),
            (operator.eq, False),
            (operator.ne, True),
            (operator.ge, False),
            (operator.gt, False),
            (operator.contains, False),
            (custom_op('issubset'), False),
            (custom_op('issuperset'), False),
            (custom_op('overlaps'), False),
            (custom_op('isdisjoint'), True),
            (custom_op('issequential'), False),
            (custom_op('extendshigher'), False),
            (custom_op('extendslower'), True),
            (custom_op('isbefore'), True),
            (custom_op('isafter'), False),
        ],
        'creation': [
            (operator.or_, (s.Range(None, aa100), s.Range(ab0, ab100))),
            (operator.and_, None),
            (operator.sub, (s.Range(None, aa100),)),
            (operator.xor, (s.Range(None, aa100), s.Range(ab0, ab100))),
        ],
    },
    ((None, aa100), (ab0, None)): {
        'comparison': [
            (operator.lt, False),
            (operator.le, False),
            (operator.eq, False),
            (operator.ne, True),
            (operator.ge, False),
            (operator.gt, False),
            (operator.contains, False),
            (custom_op('issubset'), False),
            (custom_op('issuperset'), False),
            (custom_op('overlaps'), False),
            (custom_op('isdisjoint'), True),
            (custom_op('issequential'), False),
            (custom_op('extendshigher'), False),
            (custom_op('extendslower'), True),
            (custom_op('isbefore'), True),
            (custom_op('isafter'), False),
        ],
        'creation': [
            (operator.or_, (s.Range(None, aa100), s.Range(ab0, None))),
            (operator.and_, None),
            (operator.sub, (s.Range(None, aa100),)),
            (operator.xor, (s.Range(None, aa100), s.Range(ab0, None))),
        ],
    },


    # Range 1    |------------------|
    #   Val 2    X
    ((aa0, ab100), aa0): {
        'comparison': [
            (operator.lt, TypeError),
            (operator.le, TypeError),
            (operator.eq, False),
            (operator.ne, True),
            (operator.ge, TypeError),
            (operator.gt, TypeError),
            (operator.contains, True),
            (custom_op('issubset'), TypeError),
            (custom_op('issuperset'), TypeError),
            (custom_op('overlaps'), TypeError),
            (custom_op('isdisjoint'), TypeError),
            (custom_op('issequential'), TypeError),
            (custom_op('extendshigher'), TypeError),
            (custom_op('extendslower'), TypeError),
            (custom_op('isbefore'), False),
            (custom_op('isafter'), False),
        ],
        'creation': [
            (operator.or_, TypeError),
            (operator.and_, TypeError),
            (operator.sub, TypeError),
            (operator.xor, TypeError),
        ],
    },
    ((aa0, None), aa0): {
        'comparison': [
            (operator.contains, True),
            (custom_op('isbefore'), False),
            (custom_op('isafter'), False),
        ],
    },
    ((None, ab100), -u.Infinity()): {
        'comparison': [
            (operator.contains, True),
            (custom_op('isbefore'), False),
            (custom_op('isafter'), False),
        ],
    },
    ((None, None), -u.Infinity()): {
        'comparison': [
            (operator.contains, True),
            (custom_op('isbefore'), False),
            (custom_op('isafter'), False),
        ],
    },

    #   Val 1    X
    # Range 2    |------------------|
    (aa0, (aa0, ab100)): {
        'comparison': [
            (operator.lt, TypeError),
            (operator.le, TypeError),
            (operator.eq, False),
            (operator.ne, True),
            (operator.ge, TypeError),
            (operator.gt, TypeError),
            (operator.contains, False),
            (custom_op('issubset'), AttributeError),
            (custom_op('issuperset'), AttributeError),
            (custom_op('overlaps'), AttributeError),
            (custom_op('isdisjoint'), AttributeError),
            (custom_op('issequential'), AttributeError),
            (custom_op('extendshigher'), AttributeError),
            (custom_op('extendslower'), AttributeError),
            (custom_op('isbefore'), AttributeError),
            (custom_op('isafter'), AttributeError),
        ],
        'creation': [
            (operator.or_, TypeError),
            (operator.and_, TypeError),
            (operator.sub, TypeError),
            (operator.xor, TypeError),
        ],
    },

    # Range 1    |------------------|
    #   Val 2         X
    ((aa0, ab100), aa50): {
        'comparison': [
            (operator.contains, True),
            (custom_op('isbefore'), False),
            (custom_op('isafter'), False),
        ],
    },
    ((aa0, None), aa50): {
        'comparison': [
            (operator.contains, True),
            (custom_op('isbefore'), False),
            (custom_op('isafter'), False),
        ],
    },
    ((None, ab100), aa50): {
        'comparison': [
            (operator.contains, True),
            (custom_op('isbefore'), False),
            (custom_op('isafter'), False),
        ],
    },
    ((None, None), aa50): {
        'comparison': [
            (operator.contains, True),
            (custom_op('isbefore'), False),
            (custom_op('isafter'), False),
        ],
    },


    # Range 1    |------------------|
    #   Val 2                        X
    ((aa0, ab100), ab100): {
        'comparison': [
            (operator.contains, False),
            (custom_op('isbefore'), True),
            (custom_op('isafter'), False),
        ],
    },
    ((None, ab100), ab100): {
        'comparison': [
            (operator.contains, False),
            (custom_op('isbefore'), True),
            (custom_op('isafter'), False),
        ],
    },
    # Conceptually I'm not sure if this makes sense?? Technically the
    # last member in the range <X to <pos infinity>> is infinity-1. But
    # is that less than inifinity? In any case, probably best to avoid
    # doing this or relying on this in any way.
    ((aa0, None), u.Infinity()): {
        'comparison': [
            (operator.contains, False),
            (custom_op('isbefore'), True),
            (custom_op('isafter'), False),
        ],
    },

    # Range 1        |--------------|
    #   Val 2    X
    ((aa100, ab100), aa0): {
        'comparison': [
            (operator.contains, False),
            (custom_op('isbefore'), False),
            (custom_op('isafter'), True),
        ],
    },
    ((aa100, None), aa0): {
        'comparison': [
            (operator.contains, False),
            (custom_op('isbefore'), False),
            (custom_op('isafter'), True),
        ],
    },

    # Range 1    |--------------|
    #   Val 2                       X
    ((aa0, aa100), ab0): {
        'comparison': [
            (operator.contains, False),
            (custom_op('isbefore'), True),
            (custom_op('isafter'), False),
        ],
    },
    ((None, aa100), ab0): {
        'comparison': [
            (operator.contains, False),
            (custom_op('isbefore'), True),
            (custom_op('isafter'), False),
        ],
    },

    # For Ranges that have different Unit types, comparison operators
    # should still work, while creation/manipulation operators should
    # raise a TypeError.
    ((aa0, aa100), (_10a, _100a)): {
        'comparison': [
            (operator.lt, False),
            (operator.le, False),
            (operator.eq, False),
            (operator.ne, True),
            (operator.ge, False),
            (operator.gt, False),
            (operator.contains, False),
            (custom_op('issubset'), False),
            (custom_op('issuperset'), False),
            (custom_op('overlaps'), False),
            (custom_op('isdisjoint'), True),
            (custom_op('issequential'), False),
            (custom_op('extendshigher'), True),
            (custom_op('extendslower'), False),
            (custom_op('isbefore'), False),
            (custom_op('isafter'), True),
        ],
        'creation': [
            (operator.or_, TypeError),
            (operator.and_, TypeError),
            (operator.sub, TypeError),
            (operator.xor, TypeError),
        ],
    },
    ((_10a, _100a), (aa0, aa100)): {
        'comparison': [
            (operator.lt, False),
            (operator.le, False),
            (operator.eq, False),
            (operator.ne, True),
            (operator.ge, False),
            (operator.gt, False),
            (operator.contains, False),
            (custom_op('issubset'), False),
            (custom_op('issuperset'), False),
            (custom_op('overlaps'), False),
            (custom_op('isdisjoint'), True),
            (custom_op('issequential'), False),
            (custom_op('extendshigher'), False),
            (custom_op('extendslower'), True),
            (custom_op('isbefore'), True),
            (custom_op('isafter'), False),
        ],
        'creation': [
            (operator.or_, TypeError),
            (operator.and_, TypeError),
            (operator.sub, TypeError),
            (operator.xor, TypeError),
        ],
    },
}

RANGE_CMP_PARAMS = mark_params(generate_params(RANGE_DATA, 'comparison'),
                               pytest.mark.two)
RANGE_CREATE_PARAMS = mark_params(generate_params(RANGE_DATA, 'creation'),
                                  pytest.mark.two)

MULTI_RANGE_PARAMS = [
    (((aa0, aa50), (aa100, aa9999), (aa50, aa1000), aa0),
     custom_op('union'),
     TypeError),
    (((aa0, aa50), (aa100, aa9999), (aa50, aa1000), (_10a, _100a)),
     custom_op('union'),
     TypeError),
    (((aa0, aa50), (aa100, aa9999), (aa50, aa1000)),
     custom_op('union'),
     (s.Range(aa0, aa9999),)),
    (((aa0, aa50), (aa100, aa9999), (ab100, c0), (c0, ca0)),
     custom_op('union'),
     (s.Range(aa0, aa50), s.Range(aa100, aa9999), s.Range(ab100, ca0))),
    (((aa50, ab100), (aa0, ab0), (aa0, aa50), (aa100, aa9999), (c0, ca0)),
     custom_op('union'),
     (s.Range(aa0, ab100), s.Range(c0, ca0))),
    (((aa0, aa50), (aa0, ab0), (aa0, c0), aa0),
     custom_op('intersection'),
     TypeError),
    (((aa0, aa50), (aa0, ab0), (aa0, c0), (_10a, _100a)),
     custom_op('intersection'),
     TypeError),
    (((aa0, aa50), (aa0, ab0), (aa0, c0)),
     custom_op('intersection'),
     s.Range(aa0, aa50)),
    (((aa0, aa50), (aa0, ab0), (aa0, c0), (c0, ca0)),
     custom_op('intersection'),
     None),
    (((aa0, ab0), (aa50, aa1000), (aa100, aa9999)),
     custom_op('intersection'),
     s.Range(aa100, aa1000)),
    (((aa0, aa50), (aa50, aa100), (ab100, c0), aa0),
     custom_op('difference'),
     TypeError),
    (((aa0, aa50), (aa50, aa100), (ab100, c0), (_10a, _100a)),
     custom_op('difference'),
     TypeError),
    (((aa0, aa50), (aa50, aa100), (ab100, c0)),
     custom_op('difference'),
     (s.Range(aa0, aa50),)),
    (((aa0, ab0), (aa50, aa1000), (aa100, aa9999)),
     custom_op('difference'),
     (s.Range(aa0, aa50), s.Range(aa9999, ab0))),
    (((ab0, c0), (aa0, aa1000), (aa100, ab100)),
     custom_op('difference'),
     (s.Range(ab100, c0),)),
    (((ab0, c0), (aa0, aa1000), (aa100, ab100), (aa0, c0)),
     custom_op('difference'),
     None),
    (((aa0, c0), (aa50, aa100), (ab0, ab100)),
     custom_op('difference'),
     (s.Range(aa0, aa50), s.Range(aa100, ab0), s.Range(ab100, c0))),
]
MULTI_RANGE_PARAMS = mark_params(MULTI_RANGE_PARAMS, pytest.mark.multiple)

RANGES_FOR_SORT = [s.Range(aa0, ab0), s.Range(aa0, aa50), s.Range(c0, ca0),
                   s.Range(ab100, c0), s.Range(aa50, aa1000),
                   s.Range(aa100, aa9999), s.Range(aa50, ab100),
                   s.Range(aa0, c0)]


# Tests

@pytest.mark.range
@pytest.mark.parametrize('start, end', [
    ('AA 100', 'AA 101'),
    ('AA 100', RangeTestType('AA 101')),
    (RangeTestType('AA 100'), 'AA 101'),
    (RangeTestType('AA 100'), AnotherRangeTestType('10 A')),
    (RangeTestType('AA 100'), RangeTestType('AA 100')),
    (RangeTestType('AB 100'), RangeTestType('AA 100')),
    (RangeTestType('AA 101'), RangeTestType('AA 100')),
])
def test_range_init_start_and_end_must_be_valid(start, end):
    """When a range object is initialized, the ``start`` and ``end``
    parameters must have the following characteristics: both must be
    Unit-derived objects; both must be of the same type; and the start
    value must be less than the end value. If any of these conditions
    aren't met, a BadRange exception should be raised.
    """
    with pytest.raises(e.BadRange):
        s.Range(start, end)


@pytest.mark.range
@pytest.mark.parametrize('val_args, op, expected', (RANGE_CMP_PARAMS +
                                                    RANGE_CREATE_PARAMS +
                                                    MULTI_RANGE_PARAMS))
def test_range_operations(val_args, op, expected):
    """The given param val_args should contain two tuples or one tuple
    and one non-tuple. The tuples translate into Ranges, and non-tuples
    are used as-is. Passing the two resulting objs through the given
    operator, op, should produce the expected value (or exception).
    """
    test_vals = [s.Range(*r_args) if isinstance(r_args, tuple) else r_args
                 for r_args in val_args]
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            op(*test_vals)
    else:
        assert op(*test_vals) == expected


@pytest.mark.range
def test_sort_ranges():
    """A list of ranges passed to ``sort_ranges`` should result in a
    sorted list of ranges.
    """
    ranges = RANGES_FOR_SORT
    sranges = s.sort(ranges)
    assert sranges == [s.Range(aa0, aa50), s.Range(aa50, aa1000),
                       s.Range(aa100, aa9999), s.Range(aa0, ab0),
                       s.Range(aa50, ab100), s.Range(ab100, c0),
                       s.Range(aa0, c0), s.Range(c0, ca0)]


@pytest.mark.range
def test_sort_ranges_reverse():
    """A list of ranges passed to ``sort_ranges`` using the ``reverse``
    flag should result in a list of ranges sorted in reverse order.
    """
    ranges = RANGES_FOR_SORT
    sranges = s.sort(ranges, reverse=True)
    assert sranges == [s.Range(c0, ca0), s.Range(aa0, c0), s.Range(ab100, c0),
                       s.Range(aa50, ab100), s.Range(aa0, ab0),
                       s.Range(aa100, aa9999), s.Range(aa50, aa1000),
                       s.Range(aa0, aa50)]


# RangeSet *****************************************************************

# Fixtures, factories, and test data

RSET_DATA = {
    # RangeSet 1    |------|        |------|
    # RangeSet 2    |------|        |------|
    (((aa0, aa100), (ab0, ab100)),
     ((aa0, aa100), (ab0, ab100))): {
        'comparison': [
            (operator.lt, False),
            (operator.le, True),
            (operator.eq, True),
            (operator.ne, False),
            (operator.ge, True),
            (operator.gt, False),
            (operator.contains, True),
            (custom_op('issubset'), True),
            (custom_op('issuperset'), True),
            (custom_op('overlaps'), True),
            (custom_op('isdisjoint'), False),
            (custom_op('issequential'), False),
            (custom_op('extendshigher'), False),
            (custom_op('extendslower'), False),
            (custom_op('isbefore'), False),
            (custom_op('isafter'), False),
        ],
        'creation': [
            (operator.or_, s.RangeSet((aa0, aa100), (ab0, ab100))),
            (operator.and_, s.RangeSet((aa0, aa100), (ab0, ab100))),
            (operator.sub, s.RangeSet()),
            (operator.xor, s.RangeSet()),
        ],
    },
    (((ab0, ab100), (aa0, aa100)),
     ((aa0, aa100), (ab0, ab100))): {
        'comparison': [
            (operator.lt, False),
            (operator.le, True),
            (operator.eq, True),
            (operator.ne, False),
            (operator.ge, True),
            (operator.gt, False),
            (operator.contains, True),
            (custom_op('issubset'), True),
            (custom_op('issuperset'), True),
            (custom_op('overlaps'), True),
            (custom_op('isdisjoint'), False),
            (custom_op('issequential'), False),
            (custom_op('extendshigher'), False),
            (custom_op('extendslower'), False),
            (custom_op('isbefore'), False),
            (custom_op('isafter'), False),
        ],
        'creation': [
            (operator.or_, s.RangeSet((aa0, aa100), (ab0, ab100))),
            (operator.and_, s.RangeSet((aa0, aa100), (ab0, ab100))),
            (operator.sub, s.RangeSet()),
            (operator.xor, s.RangeSet()),
        ],
    },
    (((aa0, aa50), (ab0, ab100), (aa0, aa100)),
     ((aa0, aa100), (ab0, ab100))): {
        'comparison': [
            (operator.lt, False),
            (operator.le, True),
            (operator.eq, True),
            (operator.ne, False),
            (operator.ge, True),
            (operator.gt, False),
            (operator.contains, True),
            (custom_op('issubset'), True),
            (custom_op('issuperset'), True),
            (custom_op('overlaps'), True),
            (custom_op('isdisjoint'), False),
            (custom_op('issequential'), False),
            (custom_op('extendshigher'), False),
            (custom_op('extendslower'), False),
            (custom_op('isbefore'), False),
            (custom_op('isafter'), False),
        ],
        'creation': [
            (operator.or_, s.RangeSet((aa0, aa100), (ab0, ab100))),
            (operator.and_, s.RangeSet((aa0, aa100), (ab0, ab100))),
            (operator.sub, s.RangeSet()),
            (operator.xor, s.RangeSet()),
        ],
    },

    # RangeSet 1    |------|        |------|
    # RangeSet 2    |------|
    (((aa0, aa100), (ab0, ab100)),
     ((aa0, aa100),)): {
        'comparison': [
            (operator.lt, False),
            (operator.le, False),
            (operator.eq, False),
            (operator.ne, True),
            (operator.ge, True),
            (operator.gt, True),
            (operator.contains, True),
            (custom_op('issubset'), False),
            (custom_op('issuperset'), True),
            (custom_op('overlaps'), True),
            (custom_op('isdisjoint'), False),
            (custom_op('issequential'), False),
            (custom_op('extendshigher'), True),
            (custom_op('extendslower'), False),
            (custom_op('isbefore'), False),
            (custom_op('isafter'), False),
        ],
        'creation': [
            (operator.or_, s.RangeSet((aa0, aa100), (ab0, ab100))),
            (operator.and_, s.RangeSet((aa0, aa100))),
            (operator.sub, s.RangeSet((ab0, ab100))),
            (operator.xor, s.RangeSet((ab0, ab100))),
        ],
    },
    # Note: here the second set (aa0, aa100) will actually be tested as
    # a Range object
    (((aa0, aa100), (ab0, ab100)),
     (aa0, aa100)): {
        'comparison': [
            (operator.lt, False),
            (operator.le, False),
            (operator.eq, False),
            (operator.ne, True),
            (operator.ge, True),
            (operator.gt, True),
            (operator.contains, True),
            (custom_op('issubset'), False),
            (custom_op('issuperset'), True),
            (custom_op('overlaps'), True),
            (custom_op('isdisjoint'), False),
            (custom_op('issequential'), False),
            (custom_op('extendshigher'), True),
            (custom_op('extendslower'), False),
            (custom_op('isbefore'), False),
            (custom_op('isafter'), False),
        ],
        'creation': [
            (operator.or_, TypeError),
            (operator.and_, TypeError),
            (operator.sub, TypeError),
            (operator.xor, TypeError),
        ],
    },

    # RangeSet 1    |------|        |------|
    # RangeSet 2                    |------|
    (((aa0, aa100), (ab0, ab100)),
     ((ab0, ab100),)): {
        'comparison': [
            (operator.lt, False),
            (operator.le, False),
            (operator.eq, False),
            (operator.ne, True),
            (operator.ge, True),
            (operator.gt, True),
            (operator.contains, True),
            (custom_op('issubset'), False),
            (custom_op('issuperset'), True),
            (custom_op('overlaps'), True),
            (custom_op('isdisjoint'), False),
            (custom_op('issequential'), False),
            (custom_op('extendshigher'), False),
            (custom_op('extendslower'), True),
            (custom_op('isbefore'), False),
            (custom_op('isafter'), False),
        ],
        'creation': [
            (operator.or_, s.RangeSet((aa0, aa100), (ab0, ab100))),
            (operator.and_, s.RangeSet((ab0, ab100))),
            (operator.sub, s.RangeSet((aa0, aa100))),
            (operator.xor, s.RangeSet((aa0, aa100))),
        ],
    },
    # Note: here the second set (ab0, ab100) will actually be tested as
    # a Range object
    (((aa0, aa100), (ab0, ab100)),
     (ab0, ab100)): {
        'comparison': [
            (operator.lt, False),
            (operator.le, False),
            (operator.eq, False),
            (operator.ne, True),
            (operator.ge, True),
            (operator.gt, True),
            (operator.contains, True),
            (custom_op('issubset'), False),
            (custom_op('issuperset'), True),
            (custom_op('overlaps'), True),
            (custom_op('isdisjoint'), False),
            (custom_op('issequential'), False),
            (custom_op('extendshigher'), False),
            (custom_op('extendslower'), True),
            (custom_op('isbefore'), False),
            (custom_op('isafter'), False),
        ],
        'creation': [
            (operator.or_, TypeError),
            (operator.and_, TypeError),
            (operator.sub, TypeError),
            (operator.xor, TypeError),
        ],
    },

    # RangeSet 1    |------|        |------|
    # RangeSet 2        |--|        |------|
    (((aa0, aa100), (ab0, ab100)),
     ((aa50, aa100), (ab0, ab100))): {
        'comparison': [
            (operator.lt, False),
            (operator.le, False),
            (operator.eq, False),
            (operator.ne, True),
            (operator.ge, True),
            (operator.gt, True),
            (operator.contains, True),
            (custom_op('issubset'), False),
            (custom_op('issuperset'), True),
            (custom_op('overlaps'), True),
            (custom_op('isdisjoint'), False),
            (custom_op('issequential'), False),
            (custom_op('extendshigher'), False),
            (custom_op('extendslower'), True),
            (custom_op('isbefore'), False),
            (custom_op('isafter'), False),
        ],
        'creation': [
            (operator.or_, s.RangeSet((aa0, aa100), (ab0, ab100))),
            (operator.and_, s.RangeSet((aa50, aa100), (ab0, ab100))),
            (operator.sub, s.RangeSet((aa0, aa50))),
            (operator.xor, s.RangeSet((aa0, aa50))),
        ],
    },

    # RangeSet 1    |------|        |------|
    # RangeSet 2        |--|        |----------|
    (((aa0, aa100), (ab0, ab100)),
     ((aa50, aa100), (ab0, ab1000))): {
        'comparison': [
            (operator.lt, False),
            (operator.le, False),
            (operator.eq, False),
            (operator.ne, True),
            (operator.ge, False),
            (operator.gt, False),
            (operator.contains, False),
            (custom_op('issubset'), False),
            (custom_op('issuperset'), False),
            (custom_op('overlaps'), True),
            (custom_op('isdisjoint'), False),
            (custom_op('issequential'), False),
            (custom_op('extendshigher'), False),
            (custom_op('extendslower'), True),
            (custom_op('isbefore'), False),
            (custom_op('isafter'), False),
        ],
        'creation': [
            (operator.or_, s.RangeSet((aa0, aa100), (ab0, ab1000))),
            (operator.and_, s.RangeSet((aa50, aa100), (ab0, ab100))),
            (operator.sub, s.RangeSet((aa0, aa50))),
            (operator.xor, s.RangeSet((aa0, aa50), (ab100, ab1000))),
        ],
    },

    # RangeSet 1    |------|        |------|
    # RangeSet 2              |----|        |------|
    (((aa0, aa100), (ab0, ab100)),
     ((aa1000, aa9999), (ab100, ab1000))): {
        'comparison': [
            (operator.lt, False),
            (operator.le, False),
            (operator.eq, False),
            (operator.ne, True),
            (operator.ge, False),
            (operator.gt, False),
            (operator.contains, False),
            (custom_op('issubset'), False),
            (custom_op('issuperset'), False),
            (custom_op('overlaps'), False),
            (custom_op('isdisjoint'), True),
            (custom_op('issequential'), False),
            (custom_op('extendshigher'), False),
            (custom_op('extendslower'), True),
            (custom_op('isbefore'), False),
            (custom_op('isafter'), False),
        ],
        'creation': [
            (operator.or_, s.RangeSet((aa0, aa100), (aa1000, aa9999),
                                      (ab0, ab1000))),
            (operator.and_, s.RangeSet()),
            (operator.sub, s.RangeSet((aa0, aa100), (ab0, ab100))),
            (operator.xor, s.RangeSet((aa0, aa100), (aa1000, aa9999),
                                      (ab0, ab1000))),
        ],
    },

    # RangeSet 1    |------|        |------|
    # RangeSet 2                            |------|        |------|
    (((aa0, aa100), (ab0, ab100)),
     ((ab100, ab1000), (c0, ca0))): {
        'comparison': [
            (operator.lt, False),
            (operator.le, False),
            (operator.eq, False),
            (operator.ne, True),
            (operator.ge, False),
            (operator.gt, False),
            (operator.contains, False),
            (custom_op('issubset'), False),
            (custom_op('issuperset'), False),
            (custom_op('overlaps'), False),
            (custom_op('isdisjoint'), True),
            (custom_op('issequential'), True),
            (custom_op('extendshigher'), False),
            (custom_op('extendslower'), True),
            (custom_op('isbefore'), True),
            (custom_op('isafter'), False),
        ],
        'creation': [
            (operator.or_, s.RangeSet((aa0, aa100), (ab0, ab1000), (c0, ca0))),
            (operator.and_, s.RangeSet()),
            (operator.sub, s.RangeSet((aa0, aa100), (ab0, ab100))),
            (operator.xor, s.RangeSet((aa0, aa100), (ab0, ab1000), (c0, ca0))),
        ],
    },

    # RangeSet 1    |------|        |------|
    # RangeSet 2                                    |-------------|
    (((aa0, aa100), (ab0, ab100)),
     ((ab1000, ca0),)): {
        'comparison': [
            (operator.lt, False),
            (operator.le, False),
            (operator.eq, False),
            (operator.ne, True),
            (operator.ge, False),
            (operator.gt, False),
            (operator.contains, False),
            (custom_op('issubset'), False),
            (custom_op('issuperset'), False),
            (custom_op('overlaps'), False),
            (custom_op('isdisjoint'), True),
            (custom_op('issequential'), False),
            (custom_op('extendshigher'), False),
            (custom_op('extendslower'), True),
            (custom_op('isbefore'), True),
            (custom_op('isafter'), False),
        ],
        'creation': [
            (operator.or_, s.RangeSet((aa0, aa100), (ab0, ab100),
                                      (ab1000, ca0))),
            (operator.and_, s.RangeSet()),
            (operator.sub, s.RangeSet((aa0, aa100), (ab0, ab100))),
            (operator.xor, s.RangeSet((aa0, aa100), (ab0, ab100),
                                      (ab1000, ca0))),
        ],
    },
    # Note: here the second set (ab1000, ca0) will actually be tested as
    # a Range object
    (((aa0, aa100), (ab0, ab100)),
     (ab1000, ca0)): {
        'comparison': [
            (operator.lt, False),
            (operator.le, False),
            (operator.eq, False),
            (operator.ne, True),
            (operator.ge, False),
            (operator.gt, False),
            (operator.contains, False),
            (custom_op('issubset'), False),
            (custom_op('issuperset'), False),
            (custom_op('overlaps'), False),
            (custom_op('isdisjoint'), True),
            (custom_op('issequential'), False),
            (custom_op('extendshigher'), False),
            (custom_op('extendslower'), True),
            (custom_op('isbefore'), True),
            (custom_op('isafter'), False),
        ],
        'creation': [
            (operator.or_, TypeError),
            (operator.and_, TypeError),
            (operator.sub, TypeError),
            (operator.xor, TypeError),
        ],
    },

    # RangeSet 1    |------|
    # RangeSet 2    |------|        |------|
    (((aa0, aa100),),
     ((aa0, aa100), (ab0, ab100))): {
        'comparison': [
            (operator.lt, True),
            (operator.le, True),
            (operator.eq, False),
            (operator.ne, True),
            (operator.ge, False),
            (operator.gt, False),
            (operator.contains, False),
            (custom_op('issubset'), True),
            (custom_op('issuperset'), False),
            (custom_op('overlaps'), True),
            (custom_op('isdisjoint'), False),
            (custom_op('issequential'), False),
            (custom_op('extendshigher'), False),
            (custom_op('extendslower'), False),
            (custom_op('isbefore'), False),
            (custom_op('isafter'), False),
        ],
        'creation': [
            (operator.or_, s.RangeSet((aa0, aa100), (ab0, ab100))),
            (operator.and_, s.RangeSet((aa0, aa100))),
            (operator.sub, s.RangeSet()),
            (operator.xor, s.RangeSet((ab0, ab100))),
        ],
    },
    # Note: here the first set (aa0, aa100) will actually be tested as
    # a Range object
    ((aa0, aa100),
     ((aa0, aa100), (ab0, ab100))): {
        'comparison': [
            (operator.lt, True),
            (operator.le, True),
            (operator.eq, False),
            (operator.ne, True),
            (operator.ge, False),
            (operator.gt, False),
            (operator.contains, False),
            (custom_op('issubset'), True),
            (custom_op('issuperset'), False),
            (custom_op('overlaps'), True),
            (custom_op('isdisjoint'), False),
            (custom_op('issequential'), False),
            (custom_op('extendshigher'), False),
            (custom_op('extendslower'), False),
            (custom_op('isbefore'), False),
            (custom_op('isafter'), False),
        ],
        'creation': [
            (operator.or_, TypeError),
            (operator.and_, TypeError),
            (operator.sub, TypeError),
            (operator.xor, TypeError),
        ],
    },

    # RangeSet 1                    |------|
    # RangeSet 2    |------|        |------|
    (((ab0, ab100),),
     ((aa0, aa100), (ab0, ab100))): {
        'comparison': [
            (operator.lt, True),
            (operator.le, True),
            (operator.eq, False),
            (operator.ne, True),
            (operator.ge, False),
            (operator.gt, False),
            (operator.contains, False),
            (custom_op('issubset'), True),
            (custom_op('issuperset'), False),
            (custom_op('overlaps'), True),
            (custom_op('isdisjoint'), False),
            (custom_op('issequential'), False),
            (custom_op('extendshigher'), False),
            (custom_op('extendslower'), False),
            (custom_op('isbefore'), False),
            (custom_op('isafter'), False),
        ],
        'creation': [
            (operator.or_, s.RangeSet((aa0, aa100), (ab0, ab100))),
            (operator.and_, s.RangeSet((ab0, ab100))),
            (operator.sub, s.RangeSet()),
            (operator.xor, s.RangeSet((aa0, aa100))),
        ],
    },
    # Note: here the first set (ab0, ab100) will actually be tested as
    # a Range object
    ((ab0, ab100),
     ((aa0, aa100), (ab0, ab100))): {
        'comparison': [
            (operator.lt, True),
            (operator.le, True),
            (operator.eq, False),
            (operator.ne, True),
            (operator.ge, False),
            (operator.gt, False),
            (operator.contains, False),
            (custom_op('issubset'), True),
            (custom_op('issuperset'), False),
            (custom_op('overlaps'), True),
            (custom_op('isdisjoint'), False),
            (custom_op('issequential'), False),
            (custom_op('extendshigher'), False),
            (custom_op('extendslower'), False),
            (custom_op('isbefore'), False),
            (custom_op('isafter'), False),
        ],
        'creation': [
            (operator.or_, TypeError),
            (operator.and_, TypeError),
            (operator.sub, TypeError),
            (operator.xor, TypeError),
        ],
    },

    # RangeSet 1        |--|        |------|
    # RangeSet 2    |------|        |------|
    (((aa50, aa100), (ab0, ab100)),
     ((aa0, aa100), (ab0, ab100))): {
        'comparison': [
            (operator.lt, True),
            (operator.le, True),
            (operator.eq, False),
            (operator.ne, True),
            (operator.ge, False),
            (operator.gt, False),
            (operator.contains, False),
            (custom_op('issubset'), True),
            (custom_op('issuperset'), False),
            (custom_op('overlaps'), True),
            (custom_op('isdisjoint'), False),
            (custom_op('issequential'), False),
            (custom_op('extendshigher'), False),
            (custom_op('extendslower'), False),
            (custom_op('isbefore'), False),
            (custom_op('isafter'), False),
        ],
        'creation': [
            (operator.or_, s.RangeSet((aa0, aa100), (ab0, ab100))),
            (operator.and_, s.RangeSet((aa50, aa100), (ab0, ab100))),
            (operator.sub, s.RangeSet()),
            (operator.xor, s.RangeSet((aa0, aa50))),
        ],
    },

    # RangeSet 1        |--|        |----------|
    # RangeSet 2    |------|        |------|
    (((aa50, aa100), (ab0, ab1000)),
     ((aa0, aa100), (ab0, ab100))): {
        'comparison': [
            (operator.lt, False),
            (operator.le, False),
            (operator.eq, False),
            (operator.ne, True),
            (operator.ge, False),
            (operator.gt, False),
            (operator.contains, False),
            (custom_op('issubset'), False),
            (custom_op('issuperset'), False),
            (custom_op('overlaps'), True),
            (custom_op('isdisjoint'), False),
            (custom_op('issequential'), False),
            (custom_op('extendshigher'), True),
            (custom_op('extendslower'), False),
            (custom_op('isbefore'), False),
            (custom_op('isafter'), False),
        ],
        'creation': [
            (operator.or_, s.RangeSet((aa0, aa100), (ab0, ab1000))),
            (operator.and_, s.RangeSet((aa50, aa100), (ab0, ab100))),
            (operator.sub, s.RangeSet((ab100, ab1000))),
            (operator.xor, s.RangeSet((aa0, aa50), (ab100, ab1000))),
        ],
    },

    # RangeSet 1              |----|        |------|
    # RangeSet 2    |------|        |------|
    (((aa1000, aa9999), (ab100, ab1000)),
     ((aa0, aa100), (ab0, ab100))): {
        'comparison': [
            (operator.lt, False),
            (operator.le, False),
            (operator.eq, False),
            (operator.ne, True),
            (operator.ge, False),
            (operator.gt, False),
            (operator.contains, False),
            (custom_op('issubset'), False),
            (custom_op('issuperset'), False),
            (custom_op('overlaps'), False),
            (custom_op('isdisjoint'), True),
            (custom_op('issequential'), False),
            (custom_op('extendshigher'), True),
            (custom_op('extendslower'), False),
            (custom_op('isbefore'), False),
            (custom_op('isafter'), False),
        ],
        'creation': [
            (operator.or_, s.RangeSet((aa0, aa100), (aa1000, aa9999),
                                      (ab0, ab1000))),
            (operator.and_, s.RangeSet()),
            (operator.sub, s.RangeSet((aa1000, aa9999), (ab100, ab1000))),
            (operator.xor, s.RangeSet((aa0, aa100), (aa1000, aa9999),
                                      (ab0, ab1000))),
        ],
    },

    # RangeSet 1                            |------|        |------|
    # RangeSet 2    |------|        |------|
    (((ab100, ab1000), (c0, ca0)),
     ((aa0, aa100), (ab0, ab100))): {
        'comparison': [
            (operator.lt, False),
            (operator.le, False),
            (operator.eq, False),
            (operator.ne, True),
            (operator.ge, False),
            (operator.gt, False),
            (operator.contains, False),
            (custom_op('issubset'), False),
            (custom_op('issuperset'), False),
            (custom_op('overlaps'), False),
            (custom_op('isdisjoint'), True),
            (custom_op('issequential'), True),
            (custom_op('extendshigher'), True),
            (custom_op('extendslower'), False),
            (custom_op('isbefore'), False),
            (custom_op('isafter'), True),
        ],
        'creation': [
            (operator.or_, s.RangeSet((aa0, aa100), (ab0, ab1000), (c0, ca0))),
            (operator.and_, s.RangeSet()),
            (operator.sub, s.RangeSet((ab100, ab1000), (c0, ca0))),
            (operator.xor, s.RangeSet((aa0, aa100), (ab0, ab1000), (c0, ca0))),
        ],
    },

    # RangeSet 1                                    |-------------|
    # RangeSet 2    |------|        |------|
    (((ab1000, ca0),),
     ((aa0, aa100), (ab0, ab100))): {
        'comparison': [
            (operator.lt, False),
            (operator.le, False),
            (operator.eq, False),
            (operator.ne, True),
            (operator.ge, False),
            (operator.gt, False),
            (operator.contains, False),
            (custom_op('issubset'), False),
            (custom_op('issuperset'), False),
            (custom_op('overlaps'), False),
            (custom_op('isdisjoint'), True),
            (custom_op('issequential'), False),
            (custom_op('extendshigher'), True),
            (custom_op('extendslower'), False),
            (custom_op('isbefore'), False),
            (custom_op('isafter'), True),
        ],
        'creation': [
            (operator.or_, s.RangeSet((aa0, aa100), (ab0, ab100),
                                      (ab1000, ca0))),
            (operator.and_, s.RangeSet()),
            (operator.sub, s.RangeSet((ab1000, ca0))),
            (operator.xor, s.RangeSet((aa0, aa100), (ab0, ab100),
                                      (ab1000, ca0))),
        ],
    },
    # Note: here the first set (ab1000, ca0) will actually be tested as
    # a Range object
    ((ab1000, ca0),
     ((aa0, aa100), (ab0, ab100))): {
        'comparison': [
            (operator.lt, False),
            (operator.le, False),
            (operator.eq, False),
            (operator.ne, True),
            (operator.ge, False),
            (operator.gt, False),
            (operator.contains, False),
            (custom_op('issubset'), False),
            (custom_op('issuperset'), False),
            (custom_op('overlaps'), False),
            (custom_op('isdisjoint'), True),
            (custom_op('issequential'), False),
            (custom_op('extendshigher'), True),
            (custom_op('extendslower'), False),
            (custom_op('isbefore'), False),
            (custom_op('isafter'), True),
        ],
        'creation': [
            (operator.or_, TypeError),
            (operator.and_, TypeError),
            (operator.sub, TypeError),
            (operator.xor, TypeError),
        ],
    },

    # RangeSet 1        |--|        |------|
    #      Val 2    X
    (((aa50, aa100), (ab0, ab100)),
     aa0): {
        'comparison': [
            (operator.lt, TypeError),
            (operator.le, TypeError),
            (operator.eq, False),
            (operator.ne, True),
            (operator.ge, TypeError),
            (operator.gt, TypeError),
            (operator.contains, False),
            (custom_op('issubset'), TypeError),
            (custom_op('issuperset'), TypeError),
            (custom_op('overlaps'), TypeError),
            (custom_op('isdisjoint'), TypeError),
            (custom_op('issequential'), TypeError),
            (custom_op('extendshigher'), TypeError),
            (custom_op('extendslower'), TypeError),
            (custom_op('isbefore'), False),
            (custom_op('isafter'), True),
        ],
        'creation': [
            (operator.or_, TypeError),
            (operator.and_, TypeError),
            (operator.sub, TypeError),
            (operator.xor, TypeError),
        ],
    },

    #      Val 1    X
    # RangeSet 2    |------------------|
    (aa0, ((aa0, aa100), (ab0, ab100))): {
        'comparison': [
            (operator.lt, TypeError),
            (operator.le, TypeError),
            (operator.eq, False),
            (operator.ne, True),
            (operator.ge, TypeError),
            (operator.gt, TypeError),
            (operator.contains, False),
            (custom_op('issubset'), AttributeError),
            (custom_op('issuperset'), AttributeError),
            (custom_op('overlaps'), AttributeError),
            (custom_op('isdisjoint'), AttributeError),
            (custom_op('issequential'), AttributeError),
            (custom_op('extendshigher'), AttributeError),
            (custom_op('extendslower'), AttributeError),
            (custom_op('isbefore'), AttributeError),
            (custom_op('isafter'), AttributeError),
        ],
        'creation': [
            (operator.or_, TypeError),
            (operator.and_, TypeError),
            (operator.sub, TypeError),
            (operator.xor, TypeError),
        ],
    },

    # RangeSet 1    |------|        |------|
    #      Val 2    X
    (((aa0, aa100), (ab0, ab100)),
     aa0): {
        'comparison': [
            (operator.contains, True),
            (custom_op('isbefore'), False),
            (custom_op('isafter'), False),
        ],
    },

    # RangeSet 1    |------|        |------|
    #      Val 2            X
    (((aa0, aa100), (ab0, ab100)),
     aa100): {
        'comparison': [
            (operator.contains, False),
            (custom_op('isbefore'), False),
            (custom_op('isafter'), False),
        ],
    },

    # RangeSet 1    |------|        |------|
    #      Val 2                        X
    (((aa0, aa100), (ab0, ab100)),
     ab50): {
        'comparison': [
            (operator.contains, True),
            (custom_op('isbefore'), False),
            (custom_op('isafter'), False),
        ],
    },

    # RangeSet 1    |------|        |------|
    #      Val 2                               X
    (((aa0, aa100), (ab0, ab100)),
     ab1000): {
        'comparison': [
            (operator.contains, False),
            (custom_op('isbefore'), True),
            (custom_op('isafter'), False),
        ],
    },

    # For RangeSets that have different Unit types, like for Ranges,
    # comparison operators should still work, but creation/manipulation
    # operators should raise a TypeError.
    (((aa0, aa100), (ab0, ab100)),
     ((_10a, _100a),)): {
        'comparison': [
            (operator.lt, False),
            (operator.le, False),
            (operator.eq, False),
            (operator.ne, True),
            (operator.ge, False),
            (operator.gt, False),
            (operator.contains, False),
            (custom_op('issubset'), False),
            (custom_op('issuperset'), False),
            (custom_op('overlaps'), False),
            (custom_op('isdisjoint'), True),
            (custom_op('issequential'), False),
            (custom_op('extendshigher'), True),
            (custom_op('extendslower'), False),
            (custom_op('isbefore'), False),
            (custom_op('isafter'), True),
        ],
        'creation': [
            (operator.or_, TypeError),
            (operator.and_, TypeError),
            (operator.sub, TypeError),
            (operator.xor, TypeError),
        ],
    },
    (((_10a, _100a),),
     ((aa0, aa100), (ab0, ab100))): {
        'comparison': [
            (operator.lt, False),
            (operator.le, False),
            (operator.eq, False),
            (operator.ne, True),
            (operator.ge, False),
            (operator.gt, False),
            (operator.contains, False),
            (custom_op('issubset'), False),
            (custom_op('issuperset'), False),
            (custom_op('overlaps'), False),
            (custom_op('isdisjoint'), True),
            (custom_op('issequential'), False),
            (custom_op('extendshigher'), False),
            (custom_op('extendslower'), True),
            (custom_op('isbefore'), True),
            (custom_op('isafter'), False),
        ],
        'creation': [
            (operator.or_, TypeError),
            (operator.and_, TypeError),
            (operator.sub, TypeError),
            (operator.xor, TypeError),
        ],
    },
}


RSET_CMP_PARAMS = mark_params(generate_params(RSET_DATA, 'comparison'),
                              pytest.mark.two)
RSET_CREATE_PARAMS = mark_params(generate_params(RSET_DATA, 'creation'),
                                 pytest.mark.two)
MULTI_RSET_PARAMS = [
    ((((aa0, aa50),), ((aa100, aa9999),), (aa50, aa1000)),
     custom_op('union'),
     TypeError),
    ((((aa0, aa50),), ((aa100, aa9999),), ((_10a, _100a),)),
     custom_op('union'),
     TypeError),
    ((((aa0, aa50),), ((aa100, aa9999),), ((aa50, aa1000),)),
     custom_op('union'),
     s.RangeSet((aa0, aa9999))),
    ((((aa100, aa9999),), ((aa50, aa1000),), ((aa0, aa50),)),
     custom_op('union'),
     s.RangeSet((aa0, aa9999))),
    ((((aa0, aa50), (aa100, aa9999)), ((aa0, aa1000), (ab0, ab50)),
      ((ab100, ab1000), (aa9999, ab0))),
     custom_op('union'),
     s.RangeSet((aa0, ab50), (ab100, ab1000))),
    ((((aa0, aa50),), (aa0, ab0), ((aa0, c0),)),
     custom_op('intersection'),
     TypeError),
    ((((aa0, aa50),), ((_10a, _100a),), ((aa0, c0),)),
     custom_op('intersection'),
     TypeError),
    ((((aa0, aa50),), ((aa0, ab0),), ((aa0, c0),)),
     custom_op('intersection'),
     s.RangeSet((aa0, aa50))),
    ((((aa0, aa50),), ((aa0, ab0),), ((aa0, c0),), ((c0, ca0),)),
     custom_op('intersection'),
     s.RangeSet()),
    ((((aa0, aa50), (aa100, ab0)), ((aa1000, ab0), (ab0, ab100)),
      ((aa50, aa100), (aa9999, ab100))),
     custom_op('intersection'),
     s.RangeSet((aa9999, ab0))),
    ((((aa0, aa50), (aa100, ca0)), ((aa1000, aa9999), (ab0, c0)),
      ((aa50, aa100), (ab50, ab100), (ab1000, c0))),
     custom_op('intersection'),
     s.RangeSet((ab50, ab100), (ab1000, c0))),
    (((aa0, aa50), ((aa50, aa100),), ((ab100, c0),)),
     custom_op('difference'),
     TypeError),
    ((((_10a, _100a),), ((aa50, aa100),), ((ab100, c0),)),
     custom_op('difference'),
     TypeError),
    ((((aa0, aa50),), ((aa50, aa100),), ((ab100, c0),)),
     custom_op('difference'),
     s.RangeSet((aa0, aa50))),
    ((((aa0, aa100),), ((aa50, aa100),), ((aa0, aa50),)),
     custom_op('difference'),
     s.RangeSet()),
    ((((aa0, aa100), (aa1000, ab100)), ((aa50, aa100), (ab0, ab50)),
      ((aa0, aa50), (aa9999, ab0))),
     custom_op('difference'),
     s.RangeSet((aa1000, aa9999), (ab50, ab100))),
    ((((aa0, aa100), (aa1000, ab100)), ((aa50, aa100), (ab0, ab50)),
      ((aa50, aa100), (aa9999, ab0), (c0, ca0))),
     custom_op('difference'),
     s.RangeSet((aa0, aa50), (aa1000, aa9999), (ab50, ab100))),
]
MULTI_RSET_PARAMS = mark_params(MULTI_RSET_PARAMS, pytest.mark.multiple)

RSETS_FOR_SORT = [s.RangeSet((aa0, ab0)), s.RangeSet((aa0, aa50)),
                  s.RangeSet((c0, ca0)), s.RangeSet((ab100, c0)),
                  s.RangeSet((aa50, aa1000)), s.RangeSet((aa100, aa9999)),
                  s.RangeSet((aa50, ab100)), s.RangeSet((aa0, c0))]


# Tests

@pytest.mark.rangeset
@pytest.mark.parametrize('val_args, op, expected', (RSET_CMP_PARAMS +
                                                    RSET_CREATE_PARAMS +
                                                    MULTI_RSET_PARAMS))
def test_rangeset_operations(val_args, op, expected):
    """The given param val_args should contain two tuples or one tuple
    and one non-tuple. A tuple of tuples translates into a RangeSet; a tuple
    of Units translates into a Range; and a bare Unit is used as-is.
    Passing the two resulting objs through the given operator, op,
    should produce the expected value (or exception).
    """
    test_vals = [s.RangeSet(*s_args) if isinstance(s_args, tuple) and
                 isinstance(s_args[0], tuple) else s.Range(*s_args) if
                 isinstance(s_args, tuple) else s_args for s_args in val_args]
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            op(*test_vals)
    else:
        assert op(*test_vals) == expected


@pytest.mark.rangeset
def test_sort_rangesets():
    """A list of rangesets passed to ``sort`` should result in a
    sorted list of rangesets.
    """
    rangesets = RSETS_FOR_SORT
    srangesets = s.sort(rangesets)
    assert srangesets == [s.RangeSet((aa0, aa50)), s.RangeSet((aa50, aa1000)),
                          s.RangeSet((aa100, aa9999)), s.RangeSet((aa0, ab0)),
                          s.RangeSet((aa50, ab100)), s.RangeSet((ab100, c0)),
                          s.RangeSet((aa0, c0)), s.RangeSet((c0, ca0))]


@pytest.mark.rangeset
def test_sort_rangesets_reverse():
    """A list of rangesets passed to ``sort`` using the ``reverse``
    flag should result in a list of rangesets sorted in reverse order.
    """
    rangesets = RSETS_FOR_SORT
    srangesets = s.sort(rangesets, reverse=True)
    assert srangesets == [s.RangeSet((c0, ca0)), s.RangeSet((aa0, c0)),
                          s.RangeSet((ab100, c0)), s.RangeSet((aa50, ab100)),
                          s.RangeSet((aa0, ab0)), s.RangeSet((aa100, aa9999)),
                          s.RangeSet((aa50, aa1000)), s.RangeSet((aa0, aa50))]
