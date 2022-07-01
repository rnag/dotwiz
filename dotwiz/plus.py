"""Dot Wiz Plus module."""
import itertools
import keyword

from pyheck import snake

from .common import (
    __resolve_value__, __add_common_methods__,
)
from .constants import __PY_38_OR_ABOVE__, __PY_39_OR_ABOVE__


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


def __store_in_object__(__self_dict, __self_orig_dict, key, value):
    """
    Helper method to store a key-value pair in an object :param:`self` (a
    ``DotWizPlus`` instance). This implementation stores the key if it's
    already *lower-cased* and a valid *identifier* name in python, else it
    mutates it into a (lowercase) *snake case* key name that conforms.

    The new key-value pair is stored in the object's :attr:`__dict__`, and
    the original key-value is stored in the object's :attr:`__orig_dict__`.

    """
    orig_key = key

    if orig_key in __SPECIAL_KEYS:
        key = __SPECIAL_KEYS[orig_key]

    else:
        # in case of other types, like `int`
        key = str(key)

        lower_key = key.lower()

        # if it's a keyword like `for` or `class`, or overlaps with a `dict`
        # method name such as `items`, add an underscore to key so that
        # attribute access can then work.
        if __IS_KEYWORD(lower_key):
            __SPECIAL_KEYS[orig_key] = key = f'{lower_key}_'

        # handle special cases: if the key is not lowercase, or it's not a
        # valid identifier in python.
        #
        #   examples: `ThisIsATest` | `hey, world!` | `hi-there` | `3D`
        elif not key == lower_key or not key.isidentifier():

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

            __SPECIAL_KEYS[orig_key] = key = lower_snake

    # note: this logic is the same as `DotWizPlus.__setitem__()`
    __self_orig_dict[orig_key] = value
    __self_dict[key] = value


# noinspection PyDefaultArgument
def __upsert_into_dot_wiz_plus__(self, input_dict=None, check_lists=True,
                                 __set=object.__setattr__, **kwargs):
    """
    Helper method to generate / update a :class:`DotWizPlus` (dot-access dict)
    from a Python ``dict`` object, and optional *keyword arguments*.

    """
    if kwargs:
        if input_dict:
            input_dict.update(kwargs)
        else:
            input_dict = kwargs

    elif not input_dict:  # nothing to do.
        return None

    __dict = self.__dict__

    # create `__orig_dict__` attribute on the instance
    __orig_dict = {}
    __set(self, '__orig_dict__', __orig_dict)

    for key in input_dict:
        # note: this logic is the same as `__resolve_value__()`
        #
        # *however*, I decided to inline it because it's actually faster
        # to eliminate a function call here.
        value = input_dict[key]
        t = type(value)

        if t is dict:
            # noinspection PyArgumentList
            value = DotWizPlus(value, check_lists)
        elif check_lists and t is list:
            value = [__resolve_value__(e, DotWizPlus) for e in value]

        __store_in_object__(__dict, __orig_dict, key, value)


def __setattr_impl__(self, item, value, check_lists=True):
    """
    Implementation of `DotWizPlus.__setattr__`, which bypasses mutation of
    the key name and passes through the original key.
    """
    value = __resolve_value__(value, DotWizPlus, check_lists)

    self.__dict__[item] = value
    self.__orig_dict__[item] = value


def __setitem_impl__(self, key, value, check_lists=True):
    """Implementation of `DotWizPlus.__setitem__` to preserve dot access"""
    value = __resolve_value__(value, DotWizPlus, check_lists)

    __store_in_object__(self.__dict__, self.__orig_dict__, key, value)


if __PY_38_OR_ABOVE__:  # pragma: no cover, Python >= 3.8
    def __reversed_impl__(self):
        """Implementation of `__reversed__`, to reverse the keys in a `DotWizPlus` instance."""
        return reversed(self.__orig_dict__)

else:  # Python < 3.8
    # Note: in Python 3.7, `dict` objects are not reversible by default.

    def __reversed_impl__(self):
        """Implementation of `__reversed__`, to reverse the keys in a `DotWizPlus` instance."""
        return reversed(list(self.__orig_dict__))


if __PY_39_OR_ABOVE__:  # pragma: no cover, Python >= 3.9
    def __merge_impl_fn__(op, check_lists=True, __set=object.__setattr__):
        """Implementation of `__or__` and `__ror__`, to merge `DotWizPlus` and `dict` objects."""

        def __merge_impl__(self, other):
            __other_dict = getattr(other, '__dict__', None)

            if __other_dict is None:  # other is not a `DotWizPlus` instance
                other = DotWizPlus(other, check_lists=check_lists)
                __other_dict = other.__dict__

            __merged_dict = op(self.__dict__, __other_dict)
            __merged_orig_dict = op(self.__orig_dict__, other.__orig_dict__)

            __merged = DotWizPlus()
            __set(__merged, '__dict__', __merged_dict)
            __set(__merged, '__orig_dict__', __merged_orig_dict)

            return __merged

        return __merge_impl__

    __or_impl__ = __merge_impl_fn__(dict.__or__)
    __ror_impl__ = __merge_impl_fn__(dict.__ror__)

else:  # Python < 3.9
    # Note: this is *before* Union operators were introduced to `dict`,
    # in https://peps.python.org/pep-0584/

    def __or_impl__(self, other, check_lists=True, __set=object.__setattr__):
        """Implementation of `__or__` to merge `DotWizPlus` and `dict` objects."""
        __other_dict = getattr(other, '__dict__', None)

        if __other_dict is None:  # other is not a `DotWizPlus` instance
            other = DotWizPlus(other, check_lists=check_lists)
            __other_dict = other.__dict__

        __merged_dict = {**self.__dict__, **__other_dict}
        __merged_orig_dict = {**self.__orig_dict__, **other.__orig_dict__}

        __merged = DotWizPlus()
        __set(__merged, '__dict__', __merged_dict)
        __set(__merged, '__orig_dict__', __merged_orig_dict)

        return __merged

    def __ror_impl__(self, other, check_lists=True, __set=object.__setattr__):
        """Implementation of `__ror__` to merge `DotWizPlus` and `dict` objects."""
        __other_dict = getattr(other, '__dict__', None)

        if __other_dict is None:  # other is not a `DotWizPlus` instance
            other = DotWizPlus(other, check_lists=check_lists)
            __other_dict = other.__dict__

        __merged_dict = {**__other_dict, **self.__dict__}
        __merged_orig_dict = {**other.__orig_dict__, **self.__orig_dict__}

        __merged = DotWizPlus()
        __set(__merged, '__dict__', __merged_dict)
        __set(__merged, '__orig_dict__', __merged_orig_dict)

        return __merged


def __imerge_impl__(self, other, check_lists=True, __update=dict.update):
    """Implementation of `__ior__` to incrementally update a `DotWizPlus` instance."""
    __dict = self.__dict__
    __orig_dict = self.__orig_dict__

    __other_dict = getattr(other, '__dict__', None)

    if __other_dict is not None:  # other is a `DotWizPlus` instance
        __update(__dict, __other_dict)
        __update(__orig_dict, other.__orig_dict__)

    else:  # other is a `dict` instance
        for key in other:
            value = __resolve_value__(other[key], DotWizPlus, check_lists)
            __store_in_object__(__dict, __orig_dict, key, value)

    return self


class DotWizPlus(metaclass=__add_common_methods__,
                 print_char='✪',
                 has_attr_dict=True):
    # noinspection PyProtectedMember
    """
    :class:`DotWizPlus` - a blazing *fast* ``dict`` wrapper that also
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

    **Issues with Invalid Characters**

    A key name in the scope of the ``DotWizPlus`` implementation must be:

    * a valid, *lower-* and *snake-* cased `identifier`_ in python.
    * not a reserved *keyword*, such as ``for`` or ``class``.
    * not override ``dict`` method declarations, such as ``items``, ``get``, or ``values``.

    In the case where your key name does not conform, the library will mutate
    your key to a safe, snake-cased format.

    Spaces and invalid characters are replaced with ``_``. In the case
    of a key beginning with an *int*, a leading ``_`` is added.
    In the case of a *keyword* or a ``dict`` method name, a trailing
    ``_`` is added. Keys that appear in different cases, such
    as ``myKey`` or ``My-Key``, will all be converted to
    a *snake case* variant, ``my_key`` in this example.

    Finally, check out `this example`_ which brings home all
    that was discussed above.

    .. _identifier: https://www.askpython.com/python/python-identifiers-rules-best-practices
    .. _this example: https://dotwiz.readthedocs.io/en/latest/usage.html#complete-example

    """
    __slots__ = (
        '__dict__',
        '__orig_dict__',
    )

    __init__ = update = __upsert_into_dot_wiz_plus__

    def __dir__(self):
        """
        Add a ``__dir__()`` method, so that tab auto-completion and
        attribute suggestions work as expected in IPython and Jupyter.

        For more info, check out `this post`_.

        .. _this post: https://stackoverflow.com/q/51917470/10237506
        """
        super_dir = super().__dir__()
        string_keys = [k for k in self.__dict__ if type(k) is str]
        return super_dir + [k for k in string_keys if k not in super_dir]

    def __bool__(self):
        return True if self.__dict__ else False

    def __contains__(self, item):
        return item in self.__orig_dict__

    def __eq__(self, other):
        return self.__orig_dict__ == other

    def __ne__(self, other):
        return self.__orig_dict__ != other

    def __delattr__(self, item):
        del self.__dict__[item]
        # TODO
        del self.__orig_dict__[item]

    def __delitem__(self, key):
        del self.__orig_dict__[key]
        try:
            del self.__dict__[key]
        except KeyError:
            # in case of other types, like `int`
            key = str(key)
            lower_key = key.lower()

            # if it's a keyword like `for` or `class`, or overlaps with a `dict`
            # method name such as `items`, add an underscore to key so that
            # attribute access can then work.
            if __IS_KEYWORD(lower_key):
                key = f'{lower_key}_'
            else:
                key = __SPECIAL_KEYS[key]

            del self.__dict__[key]

    # __getattr__: Use the default `object.__getattr__` implementation.

    def __getitem__(self, key):
        return self.__orig_dict__[key]

    __setattr__ = __setattr_impl__
    __setitem__ = __setitem_impl__

    def __iter__(self):
        return iter(self.__orig_dict__)

    def __len__(self):
        return len(self.__orig_dict__)

    __or__ = __or_impl__
    __ior__ = __imerge_impl__
    __ror__ = __ror_impl__

    __reversed__ = __reversed_impl__

    def clear(self, __clear=dict.clear):
        __clear(self.__orig_dict__)
        return __clear(self.__dict__)

    def copy(self):
        """
        Returns a shallow copy of the `dict` wrapped in :class:`DotWizPlus`.

        :return: DotWizPlus instance
        """
        return DotWizPlus(self.__dict__.copy(), check_lists=False)

    # noinspection PyIncorrectDocstring
    @classmethod
    def fromkeys(cls, seq, value=None, __from_keys=dict.fromkeys):
        """
        Create a new dictionary with keys from `seq` and values set to `value`.

        New created dictionary is wrapped in :class:`DotWizPlus`.

        :param seq: Sequence of elements which is to be used as keys for
          the new dictionary.
        :param value: Value which is set to each element of the dictionary.

        :return: DotWizPlus instance
        """
        return cls(__from_keys(seq, value))

    def get(self, k, default=None):
        """
        Get value from :class:`DotWizPlus` instance, or default if the key
        does not exist.
        """
        try:
            return self.__orig_dict__[k]
        except KeyError:
            return default

    def keys(self):
        return self.__orig_dict__.keys()

    def items(self):
        return self.__orig_dict__.items()

    def pop(self, key, *args):
        return self.__orig_dict__.pop(key, *args)

    def popitem(self):
        return self.__orig_dict__.popitem()

    def setdefault(self, k, default=None):
        return self.__orig_dict__.setdefault(k, default)

    def values(self):
        return self.__orig_dict__.values()


def to_blah(o):
    """
    Recursively convert an object (typically a custom `dict` type) to a
    Python `dict` type.
    """
    __dict = getattr(o, '__dict__', None)

    if __dict:
        __orig_dict = o.__orig_dict__
        return {__orig_dict[k]: to_blah(__dict[k]) for k in __dict}

    if isinstance(o, list):
        return [to_blah(e) for e in o]

    return o


DotWizPlus.to_blah = to_blah


# A list of the public-facing methods in `DotWizPlus`
__PUB_METHODS = (m for m in dir(DotWizPlus) if not m.startswith('_')
                 and callable(getattr(DotWizPlus, m)))

# A list of *lower-cased* reserved keywords. Note that we first lower-case an
# input key name and do a lookup using `__IS_KEYWORD`, so the `contains` check
# will only work for similar-cased keywords; any other keywords, such as `None`
# or `False`, likely won't match anyway, so we don't include them.
__LOWER_KWLIST = (kw for kw in keyword.kwlist if kw.islower())

# Callable used to check if any key names are reserved keywords.
__IS_KEYWORD = frozenset(itertools.chain(__LOWER_KWLIST, __PUB_METHODS)).__contains__
