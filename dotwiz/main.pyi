from typing import TypeVar, Mapping, Callable

_T = TypeVar('_T')
_KT = TypeVar('_KT')
_VT = TypeVar('_VT')

_SetItemType = Callable[[dict, _KT, _VT], None]


def make_dot_wiz(input_dict: Mapping[_KT, _VT] | None = None,
                 **kwargs) -> DotWiz: ...

def __dot_wiz_from_dict__(input_dict: Mapping[_KT, _VT]) -> DotWiz: ...


def __setitem_impl__(self: DotWiz, key: _KT, value: _VT, __set: _SetItemType = dict.__setitem__): ...

def __resolve_value__(value: _T) -> _T | DotWiz | list[DotWiz]: ...


class DotWiz(dict):

    def __getattr__(self, item: str) -> _VT: ...

    @classmethod
    def from_dict(cls, input_dict: Mapping[_KT, _VT]) -> DotWiz: ...

    def update(self,
               __m: Mapping[_KT, _VT],
               __update=dict.update,
               **kwargs: _VT) -> None: ...
