from typing import Any, Callable, ItemsView, TypeVar

from dotwiz import DotWiz, DotWizPlus


_T = TypeVar('_T')
_D = TypeVar('_D', bound=dict)  # a `dict` subclass
_KT = TypeVar('_KT')
_VT = TypeVar('_VT')

_ItemsFn = Callable[[_D ], ItemsView[_KT, _VT]]


def __add_shared_methods__(name: str,
                           bases: tuple[type, ...],
                           cls_dict: dict[str, Any],
                           *, print_char='*',
                           has_attr_dict=False): ...


def __add_repr__(name: str,
                 bases: tuple[type, ...],
                 cls_dict: dict[str, Any],
                 *, print_char='*'): ...

def __convert_to_dict__(o: dict | DotWiz | DotWizPlus | list | _T,
                        *, __items_fn: _ItemsFn = dict.items) -> dict[_KT, _VT] : ...

def __resolve_value__(value: _T, dict_type: type[DotWiz | DotWizPlus]) -> _T | _D | list[_D]: ...
