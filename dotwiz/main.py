"""Main module."""
from typing import ItemsView, ValuesView

from .common import (
    __resolve_value__, __add_shared_methods__,
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
        __dict[key] = value


def __setitem_impl__(self, key, value):
    """Implementation of `DotWiz.__setitem__` to preserve dot access"""
    value = __resolve_value__(value, DotWiz)

    self.__dict__[key] = value


class DotWiz(metaclass=__add_shared_methods__,
             print_char='✫'):
    """
    :class:`DotWiz` - a blazing *fast* ``dict`` type that also supports
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

    __setattr__ = __setitem__ = __setitem_impl__

    def __getitem__(self, key):
        return getattr(self, key)

    def __delitem__(self, key):
        return delattr(self, key)

    def __eq__(self, other) -> bool:
        return self.__dict__ == other

    def __contains__(self, item):
        # TODO: maybe use `hasattr`?
        return item in self.__dict__

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self) -> int:
        return len(self.__dict__)

    def items(self) -> ItemsView:
        return self.__dict__.items()

    def values(self) -> ValuesView:
        return self.__dict__.values()

    def copy(self):
        """Returns a shallow copy of dictionary wrapped in DotWiz.

        :return: Dotty instance
        """
        return DotWiz(self.__dict__.copy())

    @staticmethod
    def fromkeys(seq, value=None):
        """Create a new dictionary with keys from seq and values set to value.

        New created dictionary is wrapped in Dotty.

        :param seq: Sequence of elements which is to be used as keys for the new dictionary
        :param value: Value which is set to each element of the dictionary
        :return: Dotty instance
        """
        return DotWiz(dict.fromkeys(seq, value))

    def get(self, key, default=None):
        """Get value from deep key or default if key does not exist.
        """
        try:
            return self.__dict__[key]
        except KeyError:
            return default
