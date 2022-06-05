import keyword
from typing import TypeVar, Callable, Protocol, Mapping, MutableMapping, Iterable

_T = TypeVar('_T')
_KT = TypeVar('_KT')
_VT = TypeVar('_VT')

_SetItem = Callable[[dict, _KT, _VT], None]

# Ref: https://stackoverflow.com/a/68392079/10237506
class _Update(Protocol):
    def __call__(self, instance: dict,
                 __m: Mapping[_KT, _VT] | None = None,
                 **kwargs: _T) -> None: ...

class _DictGet(Protocol):
    def __call__(self, __key: str, default: str | None = None) -> str:...


def to_snake_case(string: str,
                  *, __letter: _DictGet = None,
                  __default: str | None = None) -> str: ...

def make_dot_wiz_plus(*args: Iterable[_KT, _VT],
                      **kwargs: _T) -> DotWizPlus: ...

# noinspection PyDefaultArgument
def __upsert_into_dot_wiz_plus__(self: DotWizPlus,
                                 input_dict: MutableMapping[_KT, _VT] = {},
                                 *, __set: _SetItem =dict.__setitem__,
                                 __is_keyword=keyword.iskeyword,
                                 **kwargs: _T) -> None: ...

def __setitem_impl__(self: DotWizPlus,
                     key: _KT,
                     value: _VT,
                     *, __set: _SetItem = dict.__setitem__,
                     __is_keyword=keyword.iskeyword): ...


class DotWizPlus(dict):

    # noinspection PyDefaultArgument
    def __init__(self,
                 input_dict: MutableMapping[_KT, _VT] = {},
                 **kwargs: _T) -> None: ...

    def __delattr__(self, item: str) -> None: ...
    def __delitem__(self, v: _KT) -> None: ...

    def __getattr__(self, item: str) -> _VT: ...
    def __getitem__(self, k: _KT) -> _VT: ...

    def __setattr__(self, item: str, value: _VT) -> None: ...
    def __setitem__(self, k: _KT, v: _VT) -> None: ...

    def to_dict(self) -> dict[_KT, _VT]:
        """
        Recursively convert the :class:`DotWizPlus` instance back to a ``dict``.
        """
        ...

    # noinspection PyDefaultArgument
    def update(self,
               __m: MutableMapping[_KT, _VT] = {},
               *, __set: _SetItem = dict.__setitem__,
               **kwargs: _T) -> None: ...

    def __repr__(self) -> str: ...
