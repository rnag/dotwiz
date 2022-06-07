"""Main module."""
import keyword

from pyheck import snake

from .common import (
    __add_repr__,
    __convert_to_attr_dict__,
    __convert_to_dict__,
    __resolve_value__,
)


# A running cache of special cases that we've transformed based on above.
__SPECIAL_KEYS = {}


def make_dot_wiz_plus(*args, **kwargs):
    """
    Helper function to create and return a :class:`DotWizPlus` (dot-access dict)
    from an optional *iterable* object and *keyword* arguments.

    Example::

        >>> from dotwiz import make_dot_wiz_plus
        >>> make_dot_wiz_plus([('k1', 11), ('k2', [{'a': 'b'}]), ('k3', 'v3')], y=True)
        DotWizPlus(y=True, k1=11, k2=[DotWizPlus(a='b')], k3='v3')

    """
    kwargs.update(*args)

    return DotWizPlus(kwargs)


def __store_in_dot_wiz__(self, key: str, value,
                         __dict,
                         __set=dict.__setitem__,
                         __is_keyword=keyword.iskeyword):

    orig_key = key
    lower_key = key.lower()

    # if it's a keyword like `for` or `class`, and an underscore to key so
    # that attribute access still works.
    if __is_keyword(lower_key):
        key = f'{lower_key}_'

    # handle special cases: if the key is not lowercase, or it's not a
    # valid identifier in python.
    #
    #   examples: `ThisIsATest` | `hey, world!` | `hi-there` | `3D`
    elif not key == lower_key or not key.isidentifier():

        if key in __SPECIAL_KEYS:
            key = __SPECIAL_KEYS[key]
        else:
            # transform key to `snake case` and cache the result.
            key = snake(key)

            # I've noticed for keys like 'a.b.c' or a'b'c, the result isn't
            # `a_b_c` as we'd want it to be. So for now, do the conversion
            # ourselves.
            for ch in ('.', '\''):
                if ch in key:
                    key = key.replace(ch, '_').replace('__', '_')

            # note: this hurts performance a little, but in any case we need
            # to check for words with a leading digit such as `123test` -
            # since these are not valid identifiers in python, unfortunately.
            ch = key[0]

            if ch.isdigit():  # the key has a leading digit
                key = f'_{ch}{key[1:]}'

            __SPECIAL_KEYS[key] = key

    # note: this logic is the same as `DotWizPlus.__setitem__()`
    __set(self, orig_key, value)
    __dict[key] = value


# noinspection PyDefaultArgument
def __upsert_into_dot_wiz_plus__(self, input_dict={},
                                 __set=dict.__setitem__,
                                 __is_keyword=keyword.iskeyword,
                                 **kwargs):
    """
    Helper method to generate / update a :class:`DotWizPlus` (dot-access dict)
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
            value = DotWizPlus(value)
        elif t is list:
            value = [__resolve_value__(e, DotWizPlus) for e in value]

        __store_in_dot_wiz__(self, key, value, __dict)


def __setitem_impl__(self, key, value,
                     __set=dict.__setitem__,
                     __is_keyword=keyword.iskeyword):
    """Implementation of `DotWizPlus.__setitem__` to preserve dot access"""
    value = __resolve_value__(value, DotWizPlus)
    __store_in_dot_wiz__(self, key, value, self.__dict__)


class DotWizPlus(dict, metaclass=__add_repr__, use_attr_dict=True):
    """
    :class:`DotWizPlus` - a blazing *fast* ``dict`` subclass that also
    supports *dot access* notation.

    Usage::

        >>> from dotwiz import DotWizPlus
        >>> dw = DotWizPlus({'Key 1': [{'3D': {'with': 2}}], 'keyTwo': '5', 'r-2!@d.2?': 3.21})
        >>> dw
        DotWizPlus(key_1=[DotWizPlus(_3d=DotWizPlus(with_=2))], key_two='5', r_2_d_2=3.21)
        >>> assert dw.key_1[0]._3d.with_ == 2
        >>> assert dw.key_two == '5'
        >>> assert dw.r_2_d_2 == 3.21
        >>> dw.to_dict()
        {'Key 1': [{'3D': {'with': 2}}], 'keyTwo': '5', 'r-2!@d.2?': 3.21}
        >>> dw.to_attr_dict()
        {'key_1': [{'_3d': {'with_': 2}}], 'key_two': '5', 'r_2_d_2': 3.21}

    """
    __slots__ = ('__dict__', )

    __init__ = update = __upsert_into_dot_wiz_plus__

    # __getattr__: Use the default `object.__getattr__` implementation.
    # __getitem__: Use the default `dict.__getitem__` implementation.

    __delattr__ = __delitem__ = dict.__delitem__
    __setattr__ = __setitem__ = __setitem_impl__

    to_attr_dict = __convert_to_attr_dict__
    to_attr_dict.__doc__ = 'Recursively convert the :class:`DotWizPlus` instance ' \
                           'back to a ``dict``, while preserving the lower-cased ' \
                           'keys used for attribute access.'

    to_dict = __convert_to_dict__
    to_dict.__doc__ = 'Recursively convert the :class:`DotWizPlus` instance ' \
                      'back to a ``dict``.'
