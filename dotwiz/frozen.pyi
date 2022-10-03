from .main import DotWiz
from dataclasses

# Raised when an attempt is made to modify a frozen class.
class FrozenDotWizError(AttributeError): ...


def __setitem_impl__(_self, key, _value=None): ...

def __update_impl__(self, *_args, **_kwargs): ...


class FrozenDotWiz(DotWiz):

    __setitem__ = __setattr__ = setdefault = __setitem_impl__
    update = __update_impl__
