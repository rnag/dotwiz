from typing import TypeVar, Mapping


_T = TypeVar('_T')
_KT = TypeVar('_KT')
_VT = TypeVar('_VT')


def make_dot_wiz(input_dict: Mapping[_KT, _VT] | None = None,
                 **kwargs) -> DotWiz: ...
def _dotwiz_from_dict(input_dict: Mapping[_KT, _VT]) -> DotWiz: ...

def _resolve_value(value: _T) -> _T | DotWiz | list[DotWiz]: ...


class DotWiz(dict):

    def __getattr__(self, item: str) -> _VT: ...

    @classmethod
    def from_dict(cls, input_dict: Mapping[_KT, _VT]) -> DotWiz: ...

    def update(self,
               __m: Mapping[_KT, _VT],
               __update=dict.update,
               **kwargs: _VT) -> None: ...
