"""Main module."""


def make_dot_wiz(input_dict=None, **kwargs):
    """
    Helper method to generate and return a `DotWiz` (dot-access dict) from
    an optional Python `dict` object and *keyword arguments*.

    """
    if kwargs:
        if input_dict is not None:
            input_dict.update(kwargs)
        else:
            input_dict = kwargs

    return DotWiz(input_dict)


# noinspection PyDefaultArgument
def __upsert_into_dot_wiz__(self, input_dict={},
                            *, __set=dict.__setitem__,
                            **kwargs):
    """
    Helper method to generate and return a `DotWiz` (dot-access dict) from
    a Python `dict` object.

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
            value = [__resolve_value__(e) for e in value]

        # note: this logic is the same as `DotWiz.__setitem__()`
        __set(self, key, value)
        __dict[key] = value


def __setitem_impl__(self, key, value, __set=dict.__setitem__):
    """Implementation of `DotWiz.__setitem__` to preserve dot access"""
    value = __resolve_value__(value)

    __set(self, key, value)
    self.__dict__[key] = value


def __resolve_value__(value):
    """Resolve `value`, which can be a complex type like `dict` or `list`"""
    t = type(value)

    if t is dict:
        value = DotWiz(value)

    elif t is list:
        value = [__resolve_value__(e) for e in value]

    return value


def __convert_to_dict__(o):
    """
    Recursively convert an object (typically a `dict` subclass) to a
    Python `dict` type.
    """
    if isinstance(o, dict):
        return {k: __convert_to_dict__(v) for k, v in o.items()}

    if isinstance(o, list):
        return [__convert_to_dict__(e) for e in o]

    return o


class DotWiz(dict):
    """
    :class:`DotWiz` - a ``dict`` subclass that also supports dot access
    notation.

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

    # TODO do we need this to ensure we raise an `AttributeError`?
    # def __getattr__(self, attr):
    #     try:
    #         return self.__dict__[attr]
    #     except KeyError:
    #         raise AttributeError(attr)

    def __getitem__(self, key):
        return self.__dict__[key]

    def __repr__(self):
        fields = [f'{k}={v!r}' for k, v in self.items()]
        # we could use `self.__class__.__name__`, but here we already know
        # the name of the class.
        return f'DotWiz({", ".join(fields)})'

    to_dict = __convert_to_dict__
    to_dict.__doc__ = 'Recursively convert the :class:`DotWiz` instance ' \
                      'back to a ``dict``.'
