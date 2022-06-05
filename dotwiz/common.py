"""
Common (shared) helpers and utilities.
"""


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
