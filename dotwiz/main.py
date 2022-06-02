"""Main module."""


def make_dot_wiz(input_dict=None, **kwargs):
    """
    Helper method to generate and return a `DotWiz` (dot-access dict) from
    an optional Python `dict` object and *keyword arguments*.

    """
    if input_dict:
        kwargs.update(input_dict)

    return _dotwiz_from_dict(kwargs)


def _dotwiz_from_dict(input_dict):
    """
    Helper method to generate and return a `DotWiz` (dot-access dict) from
    a Python `dict` object.

    """
    return DotWiz(
        (
            k,
            _dotwiz_from_dict(v) if isinstance(v, dict)
            else [_resolve_value(e) for e in v] if isinstance(v, list)
            else v
        ) for k, v in input_dict.items()
    )


def _set_item(self, key, value, __set=dict.__setitem__):
    value = _resolve_value(value)
    # noinspection PyArgumentList
    __set(self, key, value)


class DotWiz(dict):
    __getattr__ = dict.__getitem__
    __delattr__ = dict.__delitem__
    __setattr__ = _set_item

    from_dict = _dotwiz_from_dict

    def update(self, __m, __update=dict.update, **kwargs):
        if __m:
            __m = _dotwiz_from_dict(__m)

        if kwargs:
            kwargs = _dotwiz_from_dict(kwargs)

        # noinspection PyArgumentList
        __update(self, __m, **kwargs)

    def __repr__(self):
        fields = [f'{k}={v!r}' for k, v in self.items()]
        return f'{self.__class__.__name__}({", ".join(fields)})'


def _resolve_value(value):
    t = type(value)

    if t is dict:
        value = _dotwiz_from_dict(value)

    elif t is list:
        value = [_resolve_value(e) for e in value]

    return value
