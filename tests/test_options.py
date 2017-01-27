from __future__ import unicode_literals


from context import options


# Fixtures, factories, and test data

class TObjectWithOptions(options.ObjectWithOptions):

    options_defaults = {
        'opt1': 'A',
        'opt2': 'A',
    }
    opt2 = 'B'


# Tests

def test_OWO_init_normal_option_via_default():
    """Initializing an ObjectWithOptions class (or subclass) with no
    options arguments provided should generate appropriate values
    for options based on the ``options_defaults`` class attribute
    and any options overridden individually as class attributes
    themselves. The object's options.sources dictionary should also
    correctly identify the source of each option value (whether it came
    from a default, a class definition, or an argument).
    """
    t = TObjectWithOptions()
    assert (t.opt1 == 'A' and t.options.sources['opt1'] == 'defaults' and
            t.opt2 == 'B' and t.options.sources['opt2'] == 'class')


def test_OWO_init_normal_option_via_argument():
    """Initializing an ObjectWithOptions class (or subclass) with
    options arguments provided should generate appropriate values
    for options based on the ``options_defaults`` class attribute
    and any options overridden individually as class attributes
    themselves. The object's options.sources dictionary should also
    correctly identify the source of each option value (whether it came
    from a default, a class definition, or an argument).
    """
    t = TObjectWithOptions(opt1='C')
    assert (t.opt1 == 'C' and t.options.sources['opt1'] == 'argument' and
            t.opt2 == 'B' and t.options.sources['opt2'] == 'class')


def test_OWO_init_class_option_via_argument_without_override():
    """If the ``override_class_opts`` kwarg provided upon initializing
    an ObjectWithOptions object is False, then attempts to override
    an option value specified as a class attribute using an argument
    passed to __init__ should fail. The class attribute value should
    override the argument value for that option/attribute on the
    object.
    """
    t = TObjectWithOptions(opt2='C', override_class_opts=False)
    assert (t.opt1 == 'A' and t.options.sources['opt1'] == 'defaults' and
            t.opt2 == 'B' and t.options.sources['opt2'] == 'class')


def test_OWO_init_class_option_via_argument_with_override():
    """If the ``override_class_opts`` kwarg provided upon initializing
    an ObjectWithOptions object is True, then attempts to override
    an option value specified as a class attribute using an argument
    passed to __init__ should succeed. The argument value should
    override the class attribute value for that option/attribute on the
    object. (It should still not change the class attribute value.)
    """
    t = TObjectWithOptions(opt2='C', override_class_opts=True)
    assert (t.opt1 == 'A' and t.options.sources['opt1'] == 'defaults' and
            t.opt2 == 'C' and t.options.sources['opt2'] == 'argument' and
            t.options.classopts['opt2'] == 'B')


def test_OWO_set_normal_option_via_argument():
    """Using the ``set_option`` method of an ObjectWithOptions object
    to set the value of a particular option on an object should work
    by default--it should set the option/value based on the args passed
    to the method and set the ``sources`` dictionary for that option to
    reflect that the source of the value is an argument.
    """
    t = TObjectWithOptions()
    t.set_option('opt1', 'C')
    assert (t.opt1 == 'C' and t.options.sources['opt1'] == 'argument' and
            t.opt2 == 'B' and t.options.sources['opt2'] == 'class')


def test_OWO_set_class_option_via_argument_without_override():
    """Trying to use the ``set_option`` method of an ObjectWithOptions
    object to set the value of a particular option on an object while
    passing an ``override_class_opts`` value of False should fail to
    set the option on the object if that option has a value specified
    as a class attribute. The value contained in the class attribute
    should override the value provided via the ``set_option`` method.
    """
    t = TObjectWithOptions()
    t.set_option('opt2', 'C', override_class_opts=False)
    assert (t.opt1 == 'A' and t.options.sources['opt1'] == 'defaults' and
            t.opt2 == 'B' and t.options.sources['opt2'] == 'class')


def test_OWO_set_class_option_via_argument_with_override():
    """Trying to use the ``set_option`` method of an ObjectWithOptions
    object to set the value of a particular option on an object while
    passing an ``override_class_opts`` value of True should succeed in
    setting the option on the object, even if that option has a value
    specified as a class attribute. The value contained in the class
    attribute should not change, however.
    """
    t = TObjectWithOptions()
    t.set_option('opt2', 'C', override_class_opts=True)
    assert (t.opt1 == 'A' and t.options.sources['opt1'] == 'defaults' and
            t.opt2 == 'C' and t.options.sources['opt2'] == 'argument' and
            t.options.classopts['opt2'] == 'B')
