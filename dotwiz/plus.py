"""Dot Wiz Plus module."""
import keyword

from pyheck import snake

from .common import (
    __add_repr__,
    __convert_to_attr_dict__,
    __convert_to_dict__,
    __resolve_value__,
)


# A running cache of special-cased or non-lowercase keys that we've
# transformed before.
__SPECIAL_KEYS = {}


def make_dot_wiz_plus(*args, **kwargs):
    """
    Helper function to create and return a :class:`DotWizPlus` (dot-access dict)
    from an optional *iterable* object and *keyword* arguments.

    Example::

        >>> from dotwiz import make_dot_wiz_plus
        >>> make_dot_wiz_plus([('k1', 11), ('k2', [{'a': 'b'}]), ('k3', 'v3')], y=True)
        ✪(y=True, k1=11, k2=[✪(a='b')], k3='v3')

    """
    kwargs.update(*args)

    return DotWizPlus(kwargs)


def __store_in_object__(self, __self_dict, key, value,
                        __set=dict.__setitem__,
                        __is_keyword=keyword.iskeyword):
    """
    Helper method to store a key-value pair in an object :param:`self` (a
    ``DotWizPlus`` instance). This implementation stores the key if it's
    already *lower-cased* and a valid *identifier* name in python, else it
    mutates it into a (lowercase) *snake case* key name that conforms.

    The new key-value pair is stored in the object's :attr:`__dict__`, and
    the original key-value is stored in the underlying ``dict`` store, via
    :meth:`dict.__setitem__`.

    """
    orig_key = key
    # in case of other types, like `int`
    key = str(key)

    lower_key = key.lower()

    # if it's a keyword like `for` or `class`, add an underscore to key so
    # that attribute access can then work.
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
            lower_snake = snake(key)

            # I've noticed for keys like `a.b.c` or `a'b'c`, the result isn't
            # `a_b_c` as we'd want it to be. So for now, do the conversion
            # ourselves.
            #   See also: https://github.com/kevinheavey/pyheck/issues/10
            for ch in ('.', '\''):
                if ch in lower_snake:
                    lower_snake = lower_snake.replace(ch, '_').replace('__', '_')

            # note: this hurts performance a little, but in any case we need
            # to check for words with a leading digit such as `123test` -
            # since these are not valid identifiers in python, unfortunately.
            ch = lower_snake[0]

            if ch.isdigit():  # the key has a leading digit, which is invalid.
                lower_snake = f'_{ch}{lower_snake[1:]}'

            __SPECIAL_KEYS[key] = key = lower_snake

    # note: this logic is the same as `DotWizPlus.__setitem__()`
    __set(self, orig_key, value)
    __self_dict[key] = value


# noinspection PyDefaultArgument
def __upsert_into_dot_wiz_plus__(self, input_dict={}, **kwargs):
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

        __store_in_object__(self, __dict, key, value)


def __setitem_impl__(self, key, value):
    """Implementation of `DotWizPlus.__setitem__` to preserve dot access"""
    value = __resolve_value__(value, DotWizPlus)
    __store_in_object__(self, self.__dict__, key, value)


class DotWizPlus(dict, metaclass=__add_repr__,
                 print_char='✪',
                 use_attr_dict=True):
    # noinspection PyProtectedMember
    """
    :class:`DotWizPlus` - a blazing *fast* ``dict`` subclass that also
    supports *dot access* notation. This implementation enables you to
    turn special-cased keys into valid *snake_case* words in Python,
    as shown below.

        >>> from dotwiz import DotWizPlus
        >>> dw = DotWizPlus({'Key 1': [{'3D': {'with': 2}}], 'keyTwo': '5', 'r-2!@d.2?': 3.21})
        >>> dw
        ✪(key_1=[✪(_3d=✪(with_=2))], key_two='5', r_2_d_2=3.21)
        >>> assert dw.key_1[0]._3d.with_ == 2
        >>> assert dw.key_two == '5'
        >>> assert dw.r_2_d_2 == 3.21
        >>> dw.to_dict()
        {'Key 1': [{'3D': {'with': 2}}], 'keyTwo': '5', 'r-2!@d.2?': 3.21}
        >>> dw.to_attr_dict()
        {'key_1': [{'_3d': {'with_': 2}}], 'key_two': '5', 'r_2_d_2': 3.21}

    Issues with Invalid Characters
    ******************************

    A key name in the scope of the :class:`DotWizPlus` implementation must be
    a valid, lower-cased *identifier* in python, and also not a reserved
    *keyword* such as ``for`` or ``class``. In the case where your key name
    does not conform, the library will mutate your key to a safe,
    lower-cased format.

    Spaces and invalid characters are replaced with ``_``. In the case
    of a key beginning with an *int*, a leading ``_`` is added.
    In the case of a *keyword*, a trailing ``_`` is added. Keys that appear
    in different cases, such as ``myKey`` or ``My-Key``, will all be converted
    to a *snake case* variant, ``my_key`` in this example.

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
