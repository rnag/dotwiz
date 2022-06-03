"""Main module."""
from .constants import __PY_VERSION__, __DICT_METHODS__


def make_dot_wiz(input_dict=None, **kwargs):
    """
    Helper method to generate and return a `DotWiz` (dot-access dict) from
    an optional Python `dict` object and *keyword arguments*.

    """
    if input_dict:
        kwargs.update(input_dict)

    return __dot_wiz_from_dict__(kwargs)


if __PY_VERSION__ > (3, 7):  # Python 3.8+
    def __dot_wiz_from_dict__(input_dict):
        """
        Helper method to generate and return a `DotWiz` (dot-access dict) from
        a Python `dict` object.

        """
        return DotWiz(
            (
                k,
                # 3.8 introduces the walrus `:=` operator, which is useful here
                __dot_wiz_from_dict__(v) if (t := type(v)) is dict
                else [__resolve_value__(e) for e in v] if t is list
                else v
            ) for k, v in input_dict.items()
        )
else:  # pragma: no cover
    def __dot_wiz_from_dict__(input_dict):
        """
        Helper method to generate and return a `DotWiz` (dot-access dict) from
        a Python `dict` object.

        """
        return DotWiz(
            (
                k,
                __dot_wiz_from_dict__(v) if type(v) is dict
                else [__resolve_value__(e) for e in v] if type(v) is list
                else v
            ) for k, v in input_dict.items()
        )


def __setitem_impl__(self, key, value, __set=dict.__setitem__):
    """Implementation of `dict.__setitem__` to preserve dot access"""
    value = __resolve_value__(value)
    __set(self, key, value)


def __resolve_value__(value):
    """Resolve `value`, which can be a complex type like `dict` or `list`"""
    t = type(value)

    if t is dict:
        value = __dot_wiz_from_dict__(value)

    elif t is list:
        value = [__resolve_value__(e) for e in value]

    return value


class DotWiz(dict):
    """
    :class:`DotWiz` - a ``dict`` subclass that also supports dot access
    notation.

    Usage::

    >>> from dotwiz import DotWiz
    >>> dw = DotWiz.from_dict({'key_1': [{'k': 'v'}], 'keyTwo': '5', 'key-3': 3.21})
    >>> assert dw.key_1[0].k == 'v'
    >>> assert dw.keyTwo == '5'
    >>> assert dw['key-3'] == 3.21

    """
    __slots__ = ()

    from_dict = __dot_wiz_from_dict__
    from_kwargs = make_dot_wiz

    __delattr__ = __delitem__ = dict.__delitem__
    __getitem__ = dict.__getitem__
    __setattr__ = __setitem__ = __setitem_impl__

    def __getattribute__(self, key,
                         __attr=dict.__getattribute__,
                         __item=dict.__getitem__):
        return __attr(self, key) if key in __DICT_METHODS__ else __item(self, key)

    def update(self, __m=None, __update=dict.update, **kwargs):
        if kwargs:
            kwargs = __dot_wiz_from_dict__(kwargs)

        if __m:
            kwargs.update(__dot_wiz_from_dict__(__m))

        __update(self, kwargs)

    def __repr__(self):
        fields = [f'{k}={v!r}' for k, v in self.items()]
        # we could use `self.__class__.__name__`, but here we already know
        # the name of the class.
        return f'DotWiz({", ".join(fields)})'
