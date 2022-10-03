from .main import DotWiz


# Raised when an attempt is made to modify a frozen class.
class FrozenDotWizError(AttributeError):
    pass


def __setitem_impl__(_self, key, _value=None):
    raise FrozenDotWizError(f'cannot assign to key {key!r}, as nested assignment '
                            f'with a missing key in path is not currently supported.')


def __update_impl__(self, *_args, **_kwargs):
    raise FrozenDotWizError(f'cannot update {self!r}, as nested assignment with '
                            f'a missing key in path is not currently supported.')


class FrozenDotWiz(DotWiz):

    __setitem__ = __setattr__ = setdefault = __setitem_impl__
    update = __update_impl__
