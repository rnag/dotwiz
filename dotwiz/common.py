"""
Common (shared) helpers and utilities.
"""
import json


class DotWizEncoder(json.JSONEncoder):
    """
    Helper class for encoding of nested DotWiz and DotWizPlus dicts into standard dict
    """

    def default(self, o):
        """Return dict data of DotWiz when possible or encode with standard format

        :param o: Input object

        :return: Serializable data
        """
        try:
            return o.__dict__

        except AttributeError:
            return json.JSONEncoder.default(self, o)


def __add_shared_methods__(name, bases, cls_dict, *, print_char='*', has_attr_dict=False):
    """
    Add shared methods to a class, such as :meth:`__repr__` and :meth:`to_json`.
    """

    # use attributes defined in the instance's `__dict__`.
    def __repr__(self: object):
        fields = [f'{k}={v!r}' for k, v in self.__dict__.items()]
        return f'{print_char}({", ".join(fields)})'

    # add a `__repr__` magic method to the class.
    cls_dict['__repr__'] = __repr__

    # add common methods to the class, such as:
    #   - `to_dict`
    #   - `to_json`
    #   - `to_attr_dict` - optional, only if `has_attr_dict` is specified.

    def __convert_to_dict__(o):
        """
        Recursively convert an object (typically a custom `dict` type) to a
        Python `dict` type.
        """
        __dict = getattr(o, '__dict__', None)

        if __dict:
            return {k: __convert_to_dict__(v) for k, v in __dict.items()}

        if isinstance(o, list):
            return [__convert_to_dict__(e) for e in o]

        return o

    if has_attr_dict:
        def to_dict(o, __items=dict.items):
            """
            Recursively convert an object (typically a `dict` subclass) to a
            Python `dict` type, while preserving the lower-cased keys used
            for attribute access.
            """
            if isinstance(o, dict):
                # noinspection PyArgumentList
                return {k: to_dict(v) for k, v in __items(o)}

            if isinstance(o, list):
                return [to_dict(e) for e in o]

            return o

        def to_json(o):
            return json.dumps(o)

        cls_dict['to_json'] = to_json
        to_json.__doc__ = f'Serialize the :class:`{name}` instance as a JSON string.'

        cls_dict['to_dict'] = to_dict
        to_dict.__doc__ = f'Recursively convert the :class:`{name}` instance ' \
                          'back to a ``dict``.'

        cls_dict['to_attr_dict'] = __convert_to_dict__
        __convert_to_dict__.__name__ = 'to_attr_dict'
        __convert_to_dict__.__doc__ = f'Recursively convert the :class:`{name}` ' \
                                      'instance back to a ``dict``, while ' \
                                      'preserving the lower-cased keys used ' \
                                      'for attribute access.'

    else:
        def to_json(o):
            return json.dumps(o.__dict__, cls=DotWizEncoder)

        cls_dict['to_json'] = to_json
        to_json.__doc__ = f'Serialize the :class:`{name}` instance as a JSON string.'

        cls_dict['to_dict'] = __convert_to_dict__
        __convert_to_dict__.__name__ = 'to_dict'
        __convert_to_dict__.__doc__ = f'Recursively convert the :class:`{name}` ' \
                                      'instance back to a ``dict``.'

    return type(name, bases, cls_dict)


def __add_repr__(name, bases, cls_dict, *, print_char='*'):
    """
    Metaclass to generate and add a `__repr__` to a class.
    """

    # use attributes defined in the instance's __dict__`.
    def __repr__(self: object):
        fields = [f'{k}={v!r}' for k, v in self.__dict__.items()]
        return f'{print_char}({", ".join(fields)})'

    cls_dict['__repr__'] = __repr__

    return type(name, bases, cls_dict)


def __resolve_value__(value, dict_type):
    """Resolve `value`, which can be a complex type like `dict` or `list`"""
    t = type(value)

    if t is dict:
        value = dict_type(value)

    elif t is list:
        value = [__resolve_value__(e, dict_type) for e in value]

    return value
