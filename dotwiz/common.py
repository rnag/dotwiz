"""
Common (shared) helpers and utilities.
"""
import json


class DotWizEncoder(json.JSONEncoder):
    """
    Helper class for encoding of (nested) :class:`DotWiz` objects
    into a standard ``dict``.
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


class DotWizPlusEncoder(json.JSONEncoder):
    """
    Helper class for encoding of (nested) :class:`DotWizPlus` objects
    into a standard ``dict``.
    """

    def default(self, o):
        """
        Return the `dict` data of :class:`DotWizPlus` when possible, or encode
        with standard format otherwise.

        :param o: Input object
        :return: Serializable data

        """
        try:
            return o.__orig_dict__

        except AttributeError:
            return json.JSONEncoder.default(self, o)


class DotWizPlusSnakeEncoder(json.JSONEncoder):
    """
    Helper class for encoding of (nested) :class:`DotWizPlus` objects
    into a standard ``dict``.
    """

    def default(self, o):
        """
        Return the snake-cased `dict` data of :class:`DotWizPlus` when
        possible, or encode with standard format otherwise.

        :param o: Input object
        :return: Serializable data

        """
        try:
            __dict = o.__dict__
            return {k.strip('_'): __dict[k] for k in __dict}

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

        def __convert_to_dict_snake_cased__(o, __strip=str.strip):
            """
            Recursively convert an object (typically a custom `dict` type) to
            a Python `dict` type, while preserving snake-cased keys.
            """
            __dict = getattr(o, '__dict__', None)

            if __dict:
                return {k.strip('_'): __convert_to_dict_snake_cased__(v)
                        for k, v in __dict.items()}

            if isinstance(o, list):
                return [__convert_to_dict_snake_cased__(e) for e in o]

            return o

        def __convert_to_dict_preserve_keys__(o, snake=False):
            """
            Recursively convert an object (typically a custom `dict` type) to a
            Python `dict` type, while preserving the lower-cased keys used
            for attribute access.
            """
            if snake:
                return __convert_to_dict_snake_cased__(o)

            __dict = getattr(o, '__orig_dict__', None)

            if __dict:
                return {k: __convert_to_dict_preserve_keys__(v)
                        for k, v in __dict.items()}

            if isinstance(o, list):
                return [__convert_to_dict_preserve_keys__(e) for e in o]

            return o

        def to_json(o, attr=False, snake=False,
                    filename=None, encoding='utf-8', errors='strict',
                    file_encoder=json.dump,
                    encoder=json.dumps, **encoder_kwargs):
            if attr:
                __default_encoder = DotWizEncoder
                __initial_dict = o.__dict__
            elif snake:
                __default_encoder = DotWizPlusSnakeEncoder
                __initial_dict = o.__dict__
            else:
                __default_encoder = DotWizPlusEncoder
                __initial_dict = o.__orig_dict__

            cls = encoder_kwargs.pop('cls', __default_encoder)

            if filename:
                with open(filename, 'w', encoding=encoding, errors=errors) as f:
                    file_encoder(__initial_dict, f, cls=cls, **encoder_kwargs)
            else:
                return encoder(__initial_dict, cls=cls, **encoder_kwargs)

        # add a `to_json` method to the class.
        cls_dict['to_json'] = to_json
        to_json.__doc__ = f"""
Serialize the :class:`{name}` instance as a JSON string.

:param attr: True to return the lower-cased keys used for attribute
  access.
:param snake: True to return the `snake_case` variant of keys,
  i.e. with leading and trailing underscores (_) stripped out.
:param filename: If provided, will save to a file.
:param encoding: File encoding.
:param errors: How to handle encoding errors.
:param file_encoder: The encoder to use, when `filename` is passed.
:param encoder: The encoder to serialize with, defaults to `json.dumps`.
:param encoder_kwargs: The keyword arguments to pass in to the encoder.

:return: a string in JSON format (if no filename is provided)
"""

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

        def to_json(o, filename=None, encoding='utf-8', errors='strict',
                    file_encoder=json.dump,
                    encoder=json.dumps, **encoder_kwargs):

            cls = encoder_kwargs.pop('cls', DotWizEncoder)

            if filename:
                with open(filename, 'w', encoding=encoding, errors=errors) as f:
                    file_encoder(o.__dict__, f, cls=cls, **encoder_kwargs)
            else:
                return encoder(o.__dict__, cls=cls, **encoder_kwargs)

        # add a `to_json` method to the class.
        cls_dict['to_json'] = to_json
        to_json.__doc__ = f"""
Serialize the :class:`{name}` instance as a JSON string.

:param filename: If provided, will save to a file.
:param encoding: File encoding.
:param errors: How to handle encoding errors.
:param file_encoder: The encoder to use, when `filename` is passed.
:param encoder: The encoder to serialize with, defaults to `json.dumps`.
:param encoder_kwargs: The keyword arguments to pass in to the encoder.

:return: a string in JSON format (if no filename is provided)
"""

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
