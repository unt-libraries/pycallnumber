"""Implement objects with intelligently overridable options."""


from __future__ import unicode_literals
from __future__ import absolute_import
from builtins import object
from .exceptions import OptionsError


class Options(dict):

    def __init__(self, parent_class, useropts=None, override_class_opts=False,
                 **argopts):
        useropts = useropts or argopts
        self.reset_options(parent_class, useropts, override_class_opts)

    def reset_options(self, parent_class, useropts=None,
                      override_class_opts=False):
        useropts = useropts or {}
        self.parent_classname = parent_class.__name__
        self.classopts = parent_class.get_classopts()
        self.defopts = parent_class.options_defaults
        self.sources = {}
        self.validate_options(useropts)
        for option, default in self.defopts.items():
            if option in useropts:
                value = useropts[option]
                is_from_defaults = False
            else:
                value = default
                is_from_defaults = True
            self.set_option(option, value, is_from_defaults,
                            override_class_opts)

    def validate_option(self, option):
        if option not in self.defopts:
            msg = ('``{}`` is not a valid option for class {}.'
                   ''.format(option, self.parent_classname))
            raise OptionsError(msg)

    def validate_options(self, useropts):
        for option in list(useropts.keys()):
            self.validate_option(option)

    def set_option(self, option, value, is_from_defaults=False,
                   override_class_opts=False):
        self.validate_option(option)
        if not override_class_opts and option in self.classopts:
            self[option] = self.classopts[option]
            self.sources[option] = 'class'
        else:
            self[option] = value
            if is_from_defaults:
                self.sources[option] = 'defaults'
            else:
                self.sources[option] = 'argument'


class ObjectWithOptions(object):

    options_defaults = {}

    def __init__(self, override_class_opts=False, **useropts):
        self.reset_options(useropts, override_class_opts=override_class_opts)

    @classmethod
    def get_classopts(cls):
        return {opt: getattr(cls, opt) for opt in cls.options_defaults
                if hasattr(cls, opt)}

    @classmethod
    def filter_valid_useropts(cls, useropts):
        """Filter an opts dict to opts only in cls.options_defaults.

        Pass a dictionary of user-supplied options (``useropts``) to
        this method, and get back a dictionary containing only the
        key/value pairs where a key is present in options_defaults.
        """
        outopts = {}
        for opt in list(cls.options_defaults.keys()):
            if opt in useropts:
                outopts[opt] = useropts[opt]
        return outopts

    def copy_option_values_to_other(self, other, protect_opts_set_by=None):
        """Copy option values to another ObjectWithOptions object.

        Pass in another ObjectWithOptions object (``other``), and this
        method will copy option values from this object to the other,
        *only* for keys that exist in both objects' options dict.

        Use ``protect_opts_set_by`` to protect options on the other
        object from being overwritten based on where they were last set
        from--pass in a list containing 'defaults', 'class', or
        'argument'.
        """
        protect_opts_set_by = protect_opts_set_by or []
        for option, value in other.options.items():
            opt_src = other.get_option_source(option)
            if opt_src not in protect_opts_set_by:
                other.set_option(option, self.options.get(option, value))

    def reset_options(self, useropts=None, override_class_opts=False):
        self.options = Options(type(self), useropts, override_class_opts)
        self.apply_options_to_self()

    def get_option_source(self, option):
        return self.options.sources[option]

    def set_option(self, option, value, override_class_opts=False):
        self.options.set_option(option, value,
                                override_class_opts=override_class_opts)
        setattr(self, option, self.options[option])

    def apply_options_to_self(self):
        for option, value in self.options.items():
            setattr(self, option, value)
