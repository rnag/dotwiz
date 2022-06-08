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
        def __repr__(self: dict):
            fields = [f'{k}={v!r}' for k, v in self.items()]
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


def __resolve_value__(value, dict_type):
    """Resolve `value`, which can be a complex type like `dict` or `list`"""
    t = type(value)

    if t is dict:
        value = dict_type(value)

    elif t is list:
        value = [__resolve_value__(e, dict_type) for e in value]

    return value
