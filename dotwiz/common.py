"""
Common (shared) helpers and utilities.
"""
import json


class DotWizEncoder(json.JSONEncoder):
    """
    Helper class for encoding of (nested) :class:`DotWiz` and
    :class:`DotWizPlus` objects into a standard ``dict``.
    """

    def default(self, o):
        """
        Return the `dict` data of :class:`DotWiz` when possible, or encode
        with standard format otherwise.

        :param o: Input object
        :return: Serializable data

        """
        try:
            return o.__dict__

        except AttributeError:
            return json.JSONEncoder.default(self, o)


def __add_common_methods__(name, bases, cls_dict, *,
                           print_char='*',
                           has_attr_dict=False):
    """
    Metaclass to generate and add common or shared methods --  such
    as :meth:`__repr__` and :meth:`to_json` -- to a class.
    """

    # __repr__(): use attributes defined in the instance's `__dict__`
    def __repr__(self: object):
        fields = [f'{k}={v!r}' for k, v in self.__dict__.items()]
        return f'{print_char}({", ".join(fields)})'

    # add a `__repr__` magic method to the class.
    cls_dict['__repr__'] = __repr__

    # add utility or helper methods to the class, such as:
    #   - `to_dict` - convert an instance to a Python `dict` object.
    #   - `to_json` - serialize an instance as a JSON string.
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

    # we need to add both `to_dict` and `to_attr_dict` in this case.
    if has_attr_dict:

        def __convert_to_dict_preserve_keys__(o, __items=dict.items):
            """
            Recursively convert an object (typically a `dict` subclass) to a
            Python `dict` type, while preserving the lower-cased keys used
            for attribute access.
            """
            if isinstance(o, dict):
                # noinspection PyArgumentList
                return {k: __convert_to_dict_preserve_keys__(v)
                        for k, v in __items(o)}

            if isinstance(o, list):
                return [__convert_to_dict_preserve_keys__(e) for e in o]

            return o

        def to_json(o, encoder=json.dumps, **encoder_kwargs):
            return encoder(o, **encoder_kwargs)

        # add a `to_json` method to the class.
        cls_dict['to_json'] = to_json
        to_json.__doc__ = (
            f'Serialize the :class:`{name}` instance as a JSON string.'
        )

        # add a `to_dict` method to the class.
        cls_dict['to_dict'] = __convert_to_dict_preserve_keys__
        __convert_to_dict_preserve_keys__.__name__ = 'to_dict'
        __convert_to_dict_preserve_keys__.__doc__ = (
            f'Recursively convert the :class:`{name}` instance back to '
            'a ``dict``.'
        )

        # add a `to_attr_dict` method to the class.
        cls_dict['to_attr_dict'] = __convert_to_dict__
        __convert_to_dict__.__name__ = 'to_attr_dict'
        __convert_to_dict__.__doc__ = (
            f'Recursively convert the :class:`{name}` instance back to '
            'a ``dict``, while preserving the lower-cased keys used '
            'for attribute access.'
        )

    # we only need to add a `to_dict` method in this case.
    else:

        def to_json(o, encoder=json.dumps, **encoder_kwargs):
            cls = encoder_kwargs.pop('cls', DotWizEncoder)
            return encoder(o.__dict__, cls=cls, **encoder_kwargs)

        # add a `to_json` method to the class.
        cls_dict['to_json'] = to_json
        to_json.__doc__ = (
            f'Serialize the :class:`{name}` instance as a JSON string.'
        )

        # add a `to_dict` method to the class.
        cls_dict['to_dict'] = __convert_to_dict__
        __convert_to_dict__.__name__ = 'to_dict'
        __convert_to_dict__.__doc__ = (
            f'Recursively convert the :class:`{name}` instance back to '
            f'a ``dict``.'
        )

    # finally, build and return the new class.
    return type(name, bases, cls_dict)


def __resolve_value__(value, dict_type, check_lists=True):
    """Resolve `value`, which can be a complex type like `dict` or `list`"""
    t = type(value)

    if t is dict:
        value = dict_type(value)

    elif check_lists and t is list:
        value = [__resolve_value__(e, dict_type, check_lists) for e in value]

    return value
