"""Model and work with call number ranges and sets."""


from __future__ import unicode_literals
from __future__ import absolute_import
from builtins import object
import operator
import copy

from .exceptions import RangeSetError, BadRange
from .unit import Unit
from . import utils as u
from functools import reduce


class NonDiscreteSet(object):

    @property
    def iscontiguous(self):
        raise NotImplementedError()

    @property
    def full_typename(self):
        try:
            unittype_name = '{} '.format(self.unittype.__name__)
        except AttributeError:
            unittype_name = ''
        return '{}{}'.format(unittype_name, type(self).__name__)

    @property
    def _range_str_repr(self):
        raise NotImplementedError()

    def raise_op_type_error(self, other, optext):
        try:
            other_name = other.full_typename
        except AttributeError:
            other_name = type(other).__name__
        msg = ('Cannot use {} with {} and {} objects.'
               ''.format(optext, self.full_typename, other_name))
        raise TypeError(msg)

    def _is_valid_arg_for_set_manipulation(self, other):
        same_type = isinstance(other, type(self))
        try:
            my_ut_general = self.unittype in (u.Infinity, None)
            other_ut_general = other.unittype in (u.Infinity, None)
            same_ut = self.unittype == other.unittype
        except AttributeError:
            my_ut_general, other_ut_general, same_ut = False, False, False
        return same_type and (my_ut_general or other_ut_general or same_ut)

    def __repr__(self):
        return '<{} {}>'.format(self.full_typename, self._range_str_repr)

    def __eq__(self, other):
        raise NotImplementedError()

    def __ne__(self, other):
        return not self == other

    def __gt__(self, other):
        if not isinstance(other, NonDiscreteSet):
            self.raise_op_type_error(other, '< > <= or >=')
        return other in self and self != other

    def __ge__(self, other):
        if not isinstance(other, NonDiscreteSet):
            self.raise_op_type_error(other, '< > <= or >=')
        return other in self

    def __lt__(self, other):
        if not isinstance(other, NonDiscreteSet):
            self.raise_op_type_error(other, '< > <= or >=')
        return self in other and self != other

    def __le__(self, other):
        if not isinstance(other, NonDiscreteSet):
            self.raise_op_type_error(other, '< > <= or >=')
        return self in other

    def __contains__(self, other):
        raise NotImplementedError()

    def __or__(self, other):
        raise NotImplementedError()

    def __and__(self, other):
        raise NotImplementedError()

    def __sub__(self, other):
        raise NotImplementedError()

    def __xor__(self, other):
        raise NotImplementedError()

    def issubset(self, other):
        try:
            return self <= other
        except TypeError:
            self.raise_op_type_error(other, '``issubset``')

    def issuperset(self, other):
        try:
            return self >= other
        except TypeError:
            self.raise_op_type_error(other, '``issuperset``')

    def overlaps(self, other):
        raise NotImplementedError()

    def isdisjoint(self, other):
        try:
            return not self.overlaps(other)
        except TypeError:
            self.raise_op_type_error(other, '``isdisjoint``')

    def issequential(self, other):
        try:
            return self.end == other.start or self.start == other.end
        except AttributeError:
            self.raise_op_type_error(other, '``issequential``')

    def extendshigher(self, other):
        try:
            return self.end > other.end
        except AttributeError:
            self.raise_op_type_error(other, '``extendshigher``')

    def extendslower(self, other):
        try:
            return self.start < other.start
        except AttributeError:
            self.raise_op_type_error(other, '``extendslower``')

    def isafter(self, other):
        try:
            return self.start >= other.end
        except AttributeError:
            return self.start > other

    def isbefore(self, other):
        try:
            return self.end <= other.start
        except AttributeError:
            return self.end <= other

    def union(self, *others):
        raise NotImplementedError()

    def intersection(self, *others):
        raise NotImplementedError()

    def difference(self, *others):
        raise NotImplementedError()

    def copy(self):
        return copy.deepcopy(self)


class Range(NonDiscreteSet):

    def __init__(self, start=None, end=None):
        start, end = start or -u.Infinity(), end or u.Infinity()
        try:
            self._validate(start, end)
        except BadRange as e:
            raise BadRange('The range {} to {} did not validate: {}'
                           ''.format(start, end, e))
        self.start, self.end = start, end
        utype = type(start) if type(start) != u.Infinity else type(end)
        self.unittype = utype

    def _validate(self, start, end):
        start_provided = not isinstance(start, u.Infinity)
        end_provided = not isinstance(end, u.Infinity)
        if start_provided and not isinstance(start, Unit):
            raise BadRange('The range\'s ``start`` argument, if provided, '
                           'must be a Unit-derived object.')
        if end_provided and not isinstance(end, Unit):
            raise BadRange('The range\'s ``end`` argument, if provided, must '
                           'be a Unit-derived object.')
        if start_provided and end_provided and type(start) != type(end):
            raise BadRange('The range\'s ``start`` and ``end`` arguments, '
                           'if both are provided, must have the same type.')
        if start >= end:
            raise BadRange('The range\'s ``start`` argument must be less than '
                           'its ``end`` argument.')

    @property
    def iscontiguous(self):
        return True

    @property
    def _range_str_repr(self):
        return '\'{}\' to \'{}\''.format(self.start, self.end)

    def __eq__(self, other):
        try:
            return self.start == other.start and self.end == other.end
        except AttributeError:
            return False

    def __contains__(self, other):
        try:
            return self.start <= other.start and self.end >= other.end
        except AttributeError:
            return self.start <= other and self.end > other

    def __or__(self, other):
        try:
            if not self._is_valid_arg_for_set_manipulation(other):
                raise TypeError
            disjoint = self.isdisjoint(other) and not self.issequential(other)
        except TypeError:
            self.raise_op_type_error(other, 'bitwise ``or`` (|)')
        mytype = type(self)
        outer_start = self.start if self.extendslower(other) else other.start
        outer_end = self.end if self.extendshigher(other) else other.end
        if disjoint:
            inner_start = self.start if self.isafter(other) else other.start
            inner_end = self.end if self.isbefore(other) else other.end
            return (mytype(outer_start, inner_end),
                    mytype(inner_start, outer_end))
        return (mytype(outer_start, outer_end),)

    def __and__(self, other):
        try:
            if not self._is_valid_arg_for_set_manipulation(other):
                raise TypeError
            overlaps = self.overlaps(other)
        except TypeError:
            self.raise_op_type_error(other, 'bitwise ``and`` (&)')
        mytype = type(self)
        if overlaps:
            start = self.start if other.extendslower(self) else other.start
            end = self.end if other.extendshigher(self) else other.end
            return mytype(start, end)
        return None

    def __sub__(self, other):
        try:
            if not self._is_valid_arg_for_set_manipulation(other):
                raise TypeError
            issubset = self.issubset(other)
        except TypeError:
            self.raise_op_type_error(other, 'subtraction (-)')
        mytype = type(self)
        if issubset:
            return None
        if self.extendslower(other) and self.extendshigher(other):
            return (mytype(self.start, other.start),
                    mytype(other.end, self.end))

        use_self_start = self.extendslower(other) or self.isdisjoint(other)
        use_self_end = self.extendshigher(other) or self.isdisjoint(other)
        start = self.start if use_self_start else other.end
        end = self.end if use_self_end else other.start
        return (mytype(start, end),)

    def __xor__(self, other):
        if self == other:
            return None
        try:
            if not self._is_valid_arg_for_set_manipulation(other):
                raise AttributeError
            points = [self.start, other.start, self.end, other.end]
            points.sort()
        except AttributeError:
            self.raise_op_type_error(other, 'xor (^)')
        mytype = type(self)
        if points[0] == points[1]:
            return (mytype(points[2], points[3]),)
        if points[2] == points[3]:
            return (mytype(points[0], points[1]),)
        return (mytype(points[0], points[1]), mytype(points[2], points[3]))

    def overlaps(self, other):
        try:
            issub_or_superset = self.issubset(other) or self.issuperset(other)
        except TypeError:
            self.raise_op_type_error(other, '``overlaps``')
        self_end_overlaps = self.end > other.start and self.end < other.end
        other_end_overlaps = other.end > self.start and other.end < self.end
        return issub_or_superset or self_end_overlaps or other_end_overlaps

    def union(self, *others):
        if any(not self._is_valid_arg_for_set_manipulation(other)
               for other in others):
            msg = ('All args passed to ``union`` must be the same type and '
                   'use the same Unit type.')
            raise TypeError(msg)
        rsort_others = tuple(sort((self,) + others, reverse=True))
        results, ranges = (rsort_others[0],), rsort_others[1:]
        for range_ in ranges:
            if not range_.issubset(results[0]):
                results = (results[0] | range_) + results[1:]
        return results

    def intersection(self, *others):
        if any(not self._is_valid_arg_for_set_manipulation(other)
               for other in others):
            msg = ('All args passed to ``intersection`` must be the same type '
                   'and use the same Unit type.')
            raise TypeError(msg)
        results = self
        for range_ in others:
            results &= range_
            if results is None:
                break
        return results

    def difference(self, *others):
        if any(not self._is_valid_arg_for_set_manipulation(other)
               for other in others):
            msg = ('All args passed to ``difference`` must be the same type '
                   'and use the same Unit type.')
            raise TypeError(msg)
        results = (self,)
        for range_ in others:
            temp_results = []
            for res in results:
                diff = res - range_
                if diff is not None:
                    temp_results.extend(diff)
            if not temp_results:
                results = None
                break
            results = tuple(temp_results)
        return results


class RangeSet(NonDiscreteSet):

    def __init__(self, *user_ranges):
        ranges = []
        for rg in user_ranges:
            try:
                ranges.append(Range(*rg))
            except TypeError:
                if isinstance(rg, Range):
                    ranges.append(rg)
                else:
                    msg = '``__init__`` args must be tuples or Ranges.'
                    raise RangeSetError(msg)
        try:
            self.ranges = join(ranges) or []
        except TypeError:
            msg = '``__init__`` range args must all use the same Unit type.'
            raise RangeSetError(msg)
        try:
            self.unittype = self.ranges[0].unittype
        except IndexError:
            self.unittype = None

    @property
    def ranges(self):
        return self._ranges

    @ranges.setter
    def ranges(self, user_ranges):
        self._ranges = sort(user_ranges)
        if self._ranges:
            self.start, self.end = self._ranges[0].start, self._ranges[-1].end
        else:
            self.start, self.end = None, None

    @property
    def iscontiguous(self):
        return len(self.ranges) == 1

    @property
    def _range_str_repr(self):
        return ', '.join([r._range_str_repr for r in self.ranges])

    def __eq__(self, other):
        try:
            o_rngs = other.ranges
        except (AttributeError, IndexError):
            return False
        o_rngs_in_self = (r == o_rngs[i] for i, r in enumerate(self.ranges))
        return len(o_rngs) == len(self.ranges) and all(o_rngs_in_self)

    def __contains__(self, other):
        try:
            other_list = other.ranges
        except AttributeError:
            other_list = [other]
        # All ranges in other must be in at least one of self's ranges
        return all(any(o in r for r in self.ranges) for o in other_list)

    def __or__(self, other):
        try:
            if not self._is_valid_arg_for_set_manipulation(other):
                raise TypeError
            joined = other.ranges + self.ranges
        except (TypeError, AttributeError):
            self.raise_op_type_error(other, 'bitwise ``or`` (|)')
        mytype = type(self)
        return mytype(*joined)

    def __and__(self, other):
        try:
            if not self._is_valid_arg_for_set_manipulation(other):
                raise TypeError
            intersected = [r & o for r in self.ranges for o in other.ranges]
        except (TypeError, AttributeError):
            self.raise_op_type_error(other, 'bitwise ``and`` (&)')
        mytype = type(self)
        return mytype(*[r for r in intersected if r is not None])

    def __sub__(self, other):
        try:
            if not self._is_valid_arg_for_set_manipulation(other):
                raise TypeError
            diff = [r.difference(*other.ranges) for r in self.ranges]
        except (TypeError, AttributeError):
            self.raise_op_type_error(other, 'subtraction (-)')
        mytype = type(self)
        return mytype(*[r for tup in diff if tup is not None for r in tup])

    def __xor__(self, other):
        try:
            if not self._is_valid_arg_for_set_manipulation(other):
                raise TypeError
            sub = self - other
        except TypeError:
            self.raise_op_type_error(other, 'xor (^)')
        revsub = other - self
        return sub | revsub

    def overlaps(self, other):
        try:
            other_list = other.ranges
        except AttributeError:
            other_list = [other]
        try:
            return any(r.overlaps(o) for r in self.ranges for o in other_list)
        except TypeError:
            self.raise_op_type_error(other, '``overlaps``')

    def union(self, *others):
        try:
            return reduce(lambda rs, other: rs | other, others, self)
        except TypeError:
            msg = ('All args passed to ``union`` must be the same type and '
                   'use the same Unit type.')
            raise TypeError(msg)

    def intersection(self, *others):
        try:
            return reduce(lambda rs, other: rs & other, others, self)
        except TypeError:
            msg = ('All args passed to ``intersection`` must be the same type '
                   'and use the same Unit type.')
            raise TypeError(msg)

    def difference(self, *others):
        try:
            return reduce(lambda rs, other: rs - other, others, self)
        except TypeError:
            msg = ('All args passed to ``difference`` must be the same type '
                   'and use the same Unit type.')
            raise TypeError(msg)


# Range/RangeSet Utility functions

def sort(sets, reverse=False):
    nr = not reverse
    try:
        start_desc = sorted(sets, key=operator.attrgetter('start'), reverse=nr)
    except AttributeError:
        msg = ('Items passed to ``sort`` via the ``sets`` argument must all '
               'be NonDiscreteSet type items.')
        raise TypeError(msg)
    return sorted(start_desc, key=operator.attrgetter('end'), reverse=reverse)


def join(sets):
    try:
        return sets[0].union(*sets[1:])
    except IndexError:
        return None
    except TypeError:
        msg = ('Objects passed to ``join`` must all have the same type and '
               'use the same Unit type.')
        raise TypeError(msg)


def intersect(sets):
    try:
        return sets[0].intersection(*sets[1:])
    except IndexError:
        return None
    except TypeError:
        msg = ('Objects passed to ``intersect`` must all have the same type '
               'and use the same Unit type.')
        raise TypeError(msg)


def subtract(sets):
    try:
        return sets[0].difference(*sets[1:])
    except IndexError:
        return None
    except TypeError:
        msg = ('Objects passed to ``subtract`` must all have the same type '
               'and use the same Unit type.')
        raise TypeError(msg)
