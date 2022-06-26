"""Main module."""

from .common import (
    __resolve_value__, __add_common_methods__,
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
                            check_lists=True, **kwargs):
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
            # noinspection PyArgumentList
            value = DotWiz(value, check_lists)
        elif check_lists and t is list:
            value = [__resolve_value__(e, DotWiz) for e in value]

        # note: this logic is the same as `DotWiz.__setitem__()`
        __dict[key] = value


def __setitem_impl__(self, key, value):
    """Implementation of `DotWiz.__setitem__` to preserve dot access"""
    value = __resolve_value__(value, DotWiz)

    self.__dict__[key] = value


class DotWiz(metaclass=__add_common_methods__,
             print_char='✫'):
    """
    :class:`DotWiz` - a blazing *fast* ``dict`` wrapper that also supports
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

    def __bool__(self):
        return True if self.__dict__ else False

    def __contains__(self, item):
        # assuming that item is usually a `str`, this is actually faster
        # than simply: `item in self.__dict__`
        try:
            _ = getattr(self, item)
            return True
        except AttributeError:
            return False
        except TypeError:  # item is not a `str`
            return item in self.__dict__

    def __eq__(self, other):
        return self.__dict__ == other

    def __ne__(self, other):
        return self.__dict__ != other

    def __delitem__(self, key):
        # in general, this is little faster than simply: `self.__dict__[key]`
        try:
            delattr(self, key)
        except TypeError:  # key is not a `str`
            del self.__dict__[key]

    def __getitem__(self, key):
        # in general, this is little faster than simply: `self.__dict__[key]`
        try:
            return getattr(self, key)
        except TypeError:  # key is not a `str`
            return self.__dict__[key]

    __setattr__ = __setitem__ = __setitem_impl__

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def clear(self):
        return self.__dict__.clear()

    def copy(self):
        """
        Returns a shallow copy of the `dict` wrapped in :class:`DotWiz`.

        :return: DotWiz instance
        """
        return DotWiz(self.__dict__.copy())

    # noinspection PyIncorrectDocstring
    @classmethod
    def fromkeys(cls, seq, value=None, __from_keys=dict.fromkeys):
        """
        Create a new dictionary with keys from `seq` and values set to `value`.

        New created dictionary is wrapped in :class:`DotWiz`.

        :param seq: Sequence of elements which is to be used as keys for
          the new dictionary.
        :param value: Value which is set to each element of the dictionary.
        :return: DotWiz instance
        """
        return cls(__from_keys(seq, value))

    def get(self, k, default=None):
        """
        Get value from :class:`DotWiz` instance, or default if the key
        does not exist.
        """
        try:
            return self.__dict__[k]
        except KeyError:
            return default

    def keys(self):
        return self.__dict__.keys()

    def items(self):
        return self.__dict__.items()

    def pop(self, k):
        return self.__dict__.pop(k)

    def popitem(self):
        return self.__dict__.popitem()

    def setdefault(self, k, default=None):
        return self.__dict__.setdefault(k, default)

    def values(self):
        return self.__dict__.values()
