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

    return __dot_wiz_from_dict__(input_dict)


def __dot_wiz_from_dict__(input_dict, *, __set=dict.__setitem__):
    """
    Helper method to generate and return a `DotWiz` (dot-access dict) from
    a Python `dict` object.

    """
    dw = DotWiz()
    __dict = dw.__dict__

    for key, value in input_dict.items():
        # note: this logic is the same as `__resolve_value__()`
        #
        # *however*, I decided to inline it because it's actually faster
        # to eliminate a function call here.
        t = type(value)

        if t is dict:
            value = __dot_wiz_from_dict__(value)
        elif t is list:
            value = [__resolve_value__(e) for e in value]

        # note: this logic is the same as `DotWiz.__setitem__()`
        __set(dw, key, value)
        __dict[key] = value

    return dw


def __setitem_impl__(self, key, value, __set=dict.__setitem__):
    """Implementation of `DotWiz.__setitem__` to preserve dot access"""
    value = __resolve_value__(value)

    __set(self, key, value)
    self.__dict__[key] = value


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
    __slots__ = ('__dict__', )

    from_dict = __dot_wiz_from_dict__
    from_kwargs = make_dot_wiz

    __delattr__ = __delitem__ = dict.__delitem__
    __setattr__ = __setitem__ = __setitem_impl__

    # def __init__(self, d=None, **kwargs):
    #     if d:
    #         self._parse_input_(d)
    #     if kwargs:
    #         self._parse_input_(kwargs)
        # elif isinstance(arg, list):
        #     for k, v in arg:
        #         self.__setitem__(k, v)
        # elif hasattr(arg, "__iter__"):
        #     for k, v in list(arg):
        #         self.__setitem__(k, v)

    # TODO do we need this to ensure we raise an `AttributeError`?
    # def __getattr__(self, attr):
    #     try:
    #         return self.__dict__[attr]
    #     except KeyError:
    #         raise AttributeError(attr)

    def __getitem__(self, key):
        return self.__dict__[key]

    def update(self, __m=None, *, __set=dict.__setitem__, **kwargs):
        __dict = self.__dict__

        if __m:
            kwargs.update(__m)

        for key, value in kwargs.items():
            value = __resolve_value__(value)
            # note: this logic is the same as `DotWiz.__setitem__()`
            __set(self, key, value)
            __dict[key] = value

    def __repr__(self):
        fields = [f'{k}={v!r}' for k, v in self.items()]
        # we could use `self.__class__.__name__`, but here we already know
        # the name of the class.
        return f'DotWiz({", ".join(fields)})'
