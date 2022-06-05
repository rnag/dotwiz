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


def make_dot_wiz(*args: Iterable[_KT, _VT],
                 **kwargs: _T) -> DotWiz: ...

# noinspection PyDefaultArgument
def __upsert_into_dot_wiz__(self: DotWiz,
                            input_dict: MutableMapping[_KT, _VT] = {},
                            *, __set: _SetItem =dict.__setitem__,
                            **kwargs: _T) -> None: ...

def __setitem_impl__(self: DotWiz, key: _KT, value: _VT, __set: _SetItem = dict.__setitem__): ...

def __resolve_value__(value: _T) -> _T | DotWiz | list[DotWiz]: ...

def __convert_to_dict__(o: dict | DotWiz | list | _T) -> dict[_KT, _VT] : ...


class DotWiz(dict):

    # noinspection PyDefaultArgument
    def __init__(self,
                 input_dict: MutableMapping[_KT, _VT] = {},
                 **kwargs: _T) -> None: ...

    # @classmethod
    # def from_kwargs(cls, input_dict: Mapping[_KT, _VT] | None = None,
    #                 **kwargs: _T) -> DotWiz: ...

    def __delattr__(self, item: str) -> None: ...
    def __delitem__(self, v: _KT) -> None: ...

    def __getattr__(self, item: str) -> _VT: ...
    def __getitem__(self, k: _KT) -> _VT: ...

    def __setattr__(self, item: str, value: _VT) -> None: ...
    def __setitem__(self, k: _KT, v: _VT) -> None: ...

    def to_dict(self) -> dict[_KT, _VT]:
        """
        Recursively convert the :class:`DotWiz` instance back to a ``dict``.
        """
        ...

    # noinspection PyDefaultArgument
    def update(self,
               __m: MutableMapping[_KT, _VT] = {},
               *, __set: _SetItem = dict.__setitem__,
               **kwargs: _T) -> None: ...

    def __repr__(self) -> str: ...
