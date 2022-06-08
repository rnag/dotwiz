"""Main module."""

from .common import (
    __add_repr__,
    __convert_to_dict__,
    __resolve_value__,
)


def make_dot_wiz(*args, **kwargs):
    """
    Helper function to create and return a :class:`DotWiz` (dot-access dict)
    from an optional *iterable* object and *keyword* arguments.

    Example::

        >>> from dotwiz import make_dot_wiz
        >>> make_dot_wiz([('k1', 11), ('k2', [{'a': 'b'}]), ('k3', 'v3')], y=True)
        ✫(y=True, k1=11, k2=[✫(a='b')], k3='v3')

    """
    kwargs.update(*args)

    return DotWiz(kwargs)


# noinspection PyDefaultArgument
def __upsert_into_dot_wiz__(self, input_dict={},
                            __set=dict.__setitem__,
                            **kwargs):
    """
    Helper method to generate / update a :class:`DotWiz` (dot-access dict)
    from a Python ``dict`` object, and optional *keyword arguments*.

    """
    __dict = self.__dict__

    if kwargs:
        # avoids the potential pitfall of a "mutable default argument" -
        # only update or modify `input_dict` if the param is passed in.
        if input_dict:
            input_dict.update(kwargs)
        else:
            input_dict = kwargs

    for key in input_dict:
        # note: this logic is the same as `__resolve_value__()`
        #
        # *however*, I decided to inline it because it's actually faster
        # to eliminate a function call here.
        value = input_dict[key]
        t = type(value)

        if t is dict:
            value = DotWiz(value)
        elif t is list:
            value = [__resolve_value__(e, DotWiz) for e in value]

        # note: this logic is the same as `DotWiz.__setitem__()`
        __set(self, key, value)
        __dict[key] = value


def __setitem_impl__(self, key, value, __set=dict.__setitem__):
    """Implementation of `DotWiz.__setitem__` to preserve dot access"""
    value = __resolve_value__(value, DotWiz)

    __set(self, key, value)
    self.__dict__[key] = value


class DotWiz(dict, metaclass=__add_repr__, print_char='✫'):
    """
    :class:`DotWiz` - a blazing *fast* ``dict`` subclass that also supports
    *dot access* notation.

    Usage::

        >>> from dotwiz import DotWiz
        >>> dw = DotWiz({'key_1': [{'k': 'v'}], 'keyTwo': '5', 'key-3': 3.21})
        >>> assert dw.key_1[0].k == 'v'
        >>> assert dw.keyTwo == '5'
        >>> assert dw['key-3'] == 3.21

    """
    __slots__ = ('__dict__', )

    __init__ = update = __upsert_into_dot_wiz__

    __delattr__ = __delitem__ = dict.__delitem__
    __setattr__ = __setitem__ = __setitem_impl__

    def __getitem__(self, key):
        return self.__dict__[key]

    to_dict = __convert_to_dict__
    to_dict.__doc__ = 'Recursively convert the :class:`DotWiz` instance ' \
                      'back to a ``dict``.'
