from typing import Any, Callable, ItemsView, TypeVar

from dotwiz import DotWiz, DotWizPlus


_T = TypeVar('_T')
_D = TypeVar('_D', bound=dict)  # a `dict` subclass
_KT = TypeVar('_KT')
_VT = TypeVar('_VT')

_ItemsFn = Callable[[_D ], ItemsView[_KT, _VT]]


def __add_common_methods__(name: str,
                           bases: tuple[type, ...],
                           cls_dict: dict[str, Any],
                           *, print_char='*',
                           has_attr_dict=False): ...


def __resolve_value__(value: _T,
                      dict_type: type[DotWiz | DotWizPlus],
                      check_lists=True) -> _T | _D | list[_D]: ...
