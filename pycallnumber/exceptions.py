"""Exceptions for pycallnumber package."""


from __future__ import unicode_literals


class CallNumberError(Exception):
    """Base pycallnumber Exception."""
    pass


class CallNumberWarning(Warning):
    """Base CallNumber Warning."""
    pass


class InvalidCallNumberStringError(CallNumberError):
    """Call number string format does not conform to expectations."""
    pass


class SettingsError(CallNumberError):
    """General problem with settings passed to a Template or Unit."""
    pass


class MethodError(CallNumberError):
    """General problem with use of a pycallnumber method."""
    pass


class UtilsError(CallNumberError):
    """Problem with a Utility function."""
    pass


class OptionsError(SettingsError):
    """Problem with an Options or related object."""
    pass


class RangeSetError(CallNumberError):
    """General problem with a Set or Range object or method."""
    pass


class BadRange(RangeSetError):
    """A range is invalid."""
    pass
