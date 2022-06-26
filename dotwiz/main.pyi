from typing import (
    Callable, Protocol, TypeVar,
    Iterable, Iterator,
    KeysView, ItemsView, ValuesView,
    Mapping, MutableMapping,
)

_T = TypeVar('_T')
_KT = TypeVar('_KT')
_VT = TypeVar('_VT')

_SetItem = Callable[[dict, _KT, _VT], None]

# Ref: https://stackoverflow.com/a/68392079/10237506
class _Update(Protocol):
    def __call__(self, instance: dict,
                 __m: Mapping[_KT, _VT] | None = None,
                 **kwargs: _T) -> None: ...


def make_dot_wiz(*args: Iterable[_KT, _VT],
                 **kwargs: _T) -> DotWiz: ...

# noinspection PyDefaultArgument
def __upsert_into_dot_wiz__(self: DotWiz,
                            input_dict: MutableMapping[_KT, _VT] = {},
                            *, __set: _SetItem =dict.__setitem__,
                            **kwargs: _T) -> None: ...

def __setitem_impl__(self: DotWiz,
                     key: _KT,
                     value: _VT,
                     *, __set: _SetItem = dict.__setitem__) -> None: ...


class DotWiz:

    # noinspection PyDefaultArgument
    def __init__(self,
                 input_dict: MutableMapping[_KT, _VT] = {},
                 *, check_lists=True,
                 **kwargs: _T) -> None: ...

    def __bool__(self) -> bool: ...
    def __contains__(self, item: _KT) -> bool: ...

    def __eq__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...

    def __delattr__(self, item: str) -> None: ...
    def __delitem__(self, v: _KT) -> None: ...

    def __getattr__(self, item: str) -> _VT: ...
    def __getitem__(self, k: _KT) -> _VT: ...

    def __setattr__(self, item: str, value: _VT) -> None: ...
    def __setitem__(self, k: _KT, v: _VT) -> None: ...

    def __iter__(self) -> Iterator: ...
    def __len__(self) -> int: ...

    def to_dict(self) -> dict[_KT, _VT]:
        """
        Recursively convert the :class:`DotWiz` instance back to a ``dict``.
        """
        ...

    def to_json(self) -> str:
        """
        Serialize the :class:`DotWiz` instance as a JSON string.
        """
        ...

    def clear(self) -> None: ...

    def copy(self) -> DotWiz: ...

    @classmethod
    def fromkeys(cls: type[DotWiz],
                 seq: Iterable,
                 value: Iterable | None = None,
                 *, __from_keys=dict.fromkeys): ...

    def get(self, k: _KT, default=None) -> _VT | None: ...

    def keys(self) -> KeysView: ...

    def items(self) -> ItemsView: ...

    def pop(self, k: _KT) -> _VT: ...

    def popitem(self) -> tuple[_KT, _VT]: ...

    def setdefault(self, k: _KT, default=None) -> _VT: ...

    # noinspection PyDefaultArgument
    def update(self,
               __m: MutableMapping[_KT, _VT] = {},
               *, check_lists=True,
               __set: _SetItem = dict.__setitem__,
               **kwargs: _T) -> None: ...

    def values(self) -> ValuesView: ...

    def __repr__(self) -> str: ...
