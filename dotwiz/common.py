"""
Common (shared) helpers and utilities.
"""


def __add_repr__(name, bases, cls_dict, *, print_char='*', use_attr_dict=False):
    """
    Metaclass to generate and add a `__repr__` to a class.
    """

    # if `use_attr_dict` is true, use attributes defined in the instance's
    # `__dict__` instead.
    if use_attr_dict:
        def __repr__(self: dict):
            fields = [f'{k}={v!r}' for k, v in self.__dict__.items()]
            return f'{print_char}({", ".join(fields)})'

    else:
        def __repr__(self: dict, items_fn=dict.items):
            # noinspection PyArgumentList
            fields = [f'{k}={v!r}' for k, v in items_fn(self)]
            return f'{print_char}({", ".join(fields)})'

    cls_dict['__repr__'] = __repr__

    return type(name, bases, cls_dict)


def __convert_to_attr_dict__(o):
    """
    Recursively convert an object (typically a `dict` subclass) to a
    Python `dict` type, while preserving the lower-cased keys used
    for attribute access.
    """
    if isinstance(o, dict):
        return {k: __convert_to_attr_dict__(v) for k, v in o.__dict__.items()}

    if isinstance(o, list):
        return [__convert_to_attr_dict__(e) for e in o]

    return o


def __convert_to_dict__(o, __items_fn=dict.items):
    """
    Recursively convert an object (typically a `dict` subclass) to a
    Python `dict` type.
    """
    if isinstance(o, dict):
        # use `dict.items(o)` instead of `o.items()`, to work around this issue:
        #   https://github.com/rnag/dotwiz/issues/4
        return {k: __convert_to_dict__(v) for k, v in __items_fn(o)}

    if isinstance(o, list):
        return [__convert_to_dict__(e) for e in o]

    return o


def __resolve_value__(value, dict_type):
    """Resolve `value`, which can be a complex type like `dict` or `list`"""
    t = type(value)

    if t is dict:
        value = dict_type(value)

    elif t is list:
        value = [__resolve_value__(e, dict_type) for e in value]

    return value


def __set_nested_dot_key__(self, key, value, dict_type, __store):
    """
    Helper method to set a *dotted* ``key`` (such as ``'a.b.c'``) on ``self``,
    by creating and chaining any *missing* intermediate levels along the way.

    :param self: a ``DotWiz`` or ``DotWizPlus`` instance to modify.
    :param key: a dotted ``str`` key, i.e. one that contains a ``.``
    :param value: the value to set at the end of the dotted key.
    :param dict_type: ``DotWiz`` or ``DotWizPlus`` - the type used to
        instantiate any missing intermediate levels.
    :param __store: a callable that stores a key-value pair in an instance
        of ``dict_type``.

    """
    keys = key.split('.')

    if '' in keys:
        raise ValueError(
            f'Invalid key {key!r}: a dotted key cannot contain an empty '
            f'segment, such as a leading, trailing, or repeated dot.')

    # first, walk the existing path to validate it. Doing this up front means
    # that an invalid key does not leave `self` in a partially-modified state.
    container = self

    for k in keys[:-1]:
        if k not in container:
            break

        child = container[k]

        if not isinstance(child, dict):
            raise TypeError(
                f'Cannot set {key!r} because {k!r} is not a dict, but an '
                f'instance of {type(child).__name__!r}.')

        container = child

    # then, create and chain the missing intermediate levels.
    container = self

    for k in keys[:-1]:
        if k in container:
            child = container[k]

            if not isinstance(child, dict_type):
                # replace a plain `dict` level with a `dict_type` instance,
                # so that dot access keeps working for the new keys as well.
                child = dict_type(child)
                __store(container, k, child)

        else:
            child = dict_type()
            __store(container, k, child)

        container = child

    __store(container, keys[-1], value)
