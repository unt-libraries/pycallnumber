"""Contains utility functions used for test code."""

from __future__ import unicode_literals

from builtins import range
import pytest


DEFAULT = object()


def make_obj_factory(object_type, num_pos_args=0, kwarg_list=None):
    def factory(*args):
        obj_args, obj_kwargs = [], {}
        for i in range(0, num_pos_args):
            obj_args.append(args[i])
        for i, kwarg_name in enumerate(kwarg_list):
            if args[i+num_pos_args] != DEFAULT:
                obj_kwargs[kwarg_name] = args[i+num_pos_args]
        return object_type(*obj_args, **obj_kwargs)
    return factory


def flatten_parameters(params_dict):
    """
    Assuming a dictionary containing test parameters is structured like
    this:

    {
        'lc': [
            ('A', 'AA'),
            ('AA', 'AB'),
        ],
        'sudoc': [
            ('A:', 'AA:'),
            ('AA:', 'AB:'),
        ]
    }

    or this:

    {
        'lc': ['A', 'B', 'C'],
        'sudoc': ['A', 'B', 'C']
    }

    This flattens the dictionary into a list of tuples, suitable for
    passing into a test function parametrized with
    @pytest.mark.parametrize, like this:

    [
        ('lc', 'A', 'AA'),
        ('lc', 'AA', 'AB'),
        ('sudoc', 'A:', 'AA:'),
        ('sudoc', 'AA:', 'AB:')
    ]

    or this:

    [
        ('lc', 'A'),
        ('lc', 'B'),
        ('lc', 'C'),
        ('sudoc', 'A'),
        ('sudoc', 'B'),
        ('sudoc', 'C')
    ]

    Dictionary keys always become the first member of each tuple.
    """
    flattened = []
    for kind, params in params_dict.items():
        for values in params:
            if not isinstance(values, (tuple)):
                values = (values,)
            flattened.extend([(kind,) + values])
    return flattened


def generate_params(data, param_type):
    flattened = []
    for kind, param_sets in data.items():
        markers = [getattr(pytest.mark, m)
                   for m in param_sets.get('markers', [])]
        markers.append(getattr(pytest.mark, param_type))
        param_set = param_sets.get(param_type, [])
        for values in param_set:
            if not isinstance(values, tuple):
                values = (values,)
            params = (kind,) + values
            for m in markers:
                params = m(params)
            flattened.append(params)
    return flattened


def mark_params(params, marker):
    return [marker(p) for p in params]
