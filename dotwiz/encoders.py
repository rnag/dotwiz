"""
Custom JSON encoders.
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
