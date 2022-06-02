from typing import TypeVar, Mapping


_T = TypeVar('_T')
_KT = TypeVar('_KT')
_VT = TypeVar('_VT')


def make_dot_dict(input_dict: Mapping[_KT, _VT]) -> DotDict: ...

def _resolve_value(value: _T) -> _T | DotDict | list[DotDict]: ...


class DotDict(dict):

    def __getattr__(self, item: str) -> _VT: ...

    @classmethod
    def from_dict(cls, input_dict: Mapping[_KT, _VT]) -> DotDict: ...

    def update(self,
               __m: Mapping[_KT, _VT],
               __update=dict.update,
               **kwargs: _VT) -> None: ...
