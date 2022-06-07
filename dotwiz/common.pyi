from typing import TypeVar

from dotwiz import DotWiz, DotWizPlus

_T = TypeVar('_T')
_D = TypeVar('_D', bound=dict)  # a `dict` subclass
_KT = TypeVar('_KT')
_VT = TypeVar('_VT')

def __convert_to_attr_dict__(o: dict | DotWiz | DotWizPlus | list | _T) -> dict[_KT, _VT] : ...

def __convert_to_dict__(o: dict | DotWiz | DotWizPlus | list | _T) -> dict[_KT, _VT] : ...

def __resolve_value__(value: _T, dict_type: type[_D]) -> _T | _D | list[_D]: ...
