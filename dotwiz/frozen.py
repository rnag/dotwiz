"""Helper utilities (not exported by default)"""


# Raised when an attempt is made to modify a frozen class.
class FrozenDotWizError(AttributeError):
    pass


def __getitem_impl__(self, _):
    return self


def __setitem_impl__(_self, key, _value=None):
    raise FrozenDotWizError(f'cannot assign to key {key!r}, as nested assignment '
                            f'with a missing key in path is not currently supported.')


def __update_impl__(self, *_args, **_kwargs):
    raise FrozenDotWizError(f'cannot update {self!r}, as nested assignment with '
                            f'a missing key in path is not currently supported.')


class NotDotWiz:
    """
    A dummy class that returns ``self`` on attribute lookup.

    The :meth:`__bool__` method ensures that an `if` check returns False:

    >>> from dotwiz.frozen import NotDotWiz
    >>> dw = NotDotWiz()
    >>> if dw:  # this condition is never true
    ...     ...

    Inspired by this clever ``NotDot`` implementation:
        https://gist.github.com/akx/11dddd8fd3027a410ff7a7d228f2cff1

    """
    def __bool__(self):
        return False

    __getattr__ = __getitem__ = __getitem_impl__

    def __repr__(self):
        return '\u2205'

    __setitem__ = __setattr__ = setdefault = __setitem_impl__
    update = __update_impl__


NOT_DOT_WIZ = NotDotWiz()
