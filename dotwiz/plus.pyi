import json
from typing import (
    Callable, Protocol, TypeVar,
    Iterable, Iterator, Reversible,
    KeysView, ItemsView, ValuesView,
    Mapping, MutableMapping, AnyStr, Any,
    overload,
)

_T = TypeVar('_T')
_KT = TypeVar('_KT')
_VT = TypeVar('_VT')

# Valid collection types in JSON.
_JSONList = list[Any]
_JSONObject = dict[str, Any]

_Clear = Callable[[dict[_KT, _VT]], None]
_Copy = Callable[[dict[_KT, _VT]], dict[_KT, _VT]]
_SetAttribute = Callable[[DotWizPlus, str, Any], None]


class Encoder(Protocol):
    """
    Represents an encoder for Python object -> JSON, e.g. analogous to
    `json.dumps`
    """

    def __call__(self, obj: _JSONObject | _JSONList,
                 **kwargs) -> AnyStr:
        ...

# Ref: https://stackoverflow.com/a/68392079/10237506
class _DictGet(Protocol):
    @overload
    def __call__(self, key: _KT) -> _VT | None: ...
    @overload
    def __call__(self, key: _KT, default: _VT | _T) -> _VT | _T: ...

class _Update(Protocol):
    def __call__(self, instance: dict,
                 __m: Mapping[_KT, _VT] | None = None,
                 **kwargs: _T) -> None: ...

class _RawDictGet(Protocol):
    @overload
    def __call__(self, obj: dict, key: _KT) -> _VT | None: ...
    @overload
    def __call__(self, obj: dict, key: _KT, default: _VT | _T) -> _VT | _T: ...


__SPECIAL_KEYS: dict[str, str] = ...
__GET_SPECIAL_KEY__: _DictGet = ...
__IS_KEYWORD: Callable[[object], bool] = ...


def make_dot_wiz_plus(*args: Iterable[_KT, _VT],
                      **kwargs: _T) -> DotWizPlus: ...

def __store_in_object__(__self_dict: MutableMapping[_KT, _VT],
                        __self_orig_dict: MutableMapping[_KT, _VT],
                        __self_orig_keys: MutableMapping[str, _KT],
                        key: _KT,
                        value: _VT) -> None: ...

# noinspection PyDefaultArgument
def __upsert_into_dot_wiz_plus__(self: DotWizPlus,
                                 input_dict: MutableMapping[_KT, _VT] = {},
                                 *, check_lists=True,
                                 __skip_init=False,
                                 __set: _SetAttribute = object.__setattr__,
                                 **kwargs: _T) -> None: ...

def __setattr_impl__(self: DotWizPlus,
                     item: str,
                     value: _VT,
                     *, check_lists=True) -> None: ...

def __setitem_impl__(self: DotWizPlus,
                     key: _KT,
                     value: _VT,
                     *, check_lists=True) -> None: ...

def __merge_impl_fn__(op: Callable[[dict, dict], dict],
                      *, check_lists=True,
                      __set: _SetAttribute = object.__setattr__
                      ) -> Callable[[DotWizPlus, DotWizPlus | dict], DotWizPlus]: ...

def __or_impl__(self: DotWizPlus,
                other: DotWizPlus | dict,
                *, check_lists=True,
                __set: _SetAttribute = object.__setattr__) -> DotWizPlus: ...

def __ror_impl__(self: DotWizPlus,
                 other: DotWizPlus | dict,
                 *, check_lists=True,
                 __set: _SetAttribute = object.__setattr__) -> DotWizPlus: ...

def __ior_impl__(self: DotWizPlus,
                 other: DotWizPlus | dict,
                 *, check_lists=True,
                 __update: _Update = dict.update): ...


class DotWizPlus:

    __dict__: dict[_KT, _VT]
    __orig_dict__: dict[_KT, _VT]
    __orig_keys__: dict[str, _KT]

    # noinspection PyDefaultArgument
    def __init__(self,
                 input_dict: MutableMapping[_KT, _VT] = {},
                 *, check_lists=True,
                 __skip_init=False,
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
    def __reversed__(self) -> Reversible: ...

    def __or__(self, other: DotWizPlus | dict) -> DotWizPlus: ...
    def __ior__(self, other: DotWizPlus | dict) -> DotWizPlus: ...
    def __ror__(self, other: DotWizPlus | dict) -> DotWizPlus: ...

    def to_dict(self) -> dict[_KT, _VT]:
        """
        Recursively convert the :class:`DotWizPlus` instance back to a ``dict``.
        """
        ...

    def to_attr_dict(self) -> dict[_KT, _VT]:
        """
        Recursively convert the :class:`DotWizPlus` instance back to a ``dict``,
        while preserving the lower-cased keys used for attribute access.
        """
        ...

    def to_json(self, *,
                encoder: Encoder = json.dumps,
                **encoder_kwargs) -> AnyStr:
        """
        Serialize the :class:`DotWizPlus` instance as a JSON string.

        :param encoder: The encoder to serialize with, defaults to `json.dumps`.
        :param encoder_kwargs: The keyword arguments to pass in to the encoder.
        """
        ...

    def clear(self,
              *, __clear: _Clear = dict.clear) -> None: ...

    def copy(self,
             *, __copy: _Copy = dict.copy,
             __set: _SetAttribute = object.__setattr__) -> DotWizPlus: ...

    # noinspection PyUnresolvedReferences
    @classmethod
    def fromkeys(cls: type[DotWizPlus],
                 seq: Iterable,
                 value: Iterable | None = None,
                 *, __from_keys=dict.fromkeys): ...

    @overload
    def get(self, k: _KT,
            *, __get: _RawDictGet = dict.get) -> _VT | None: ...
    @overload
    def get(self, k: _KT, default: _VT | _T,
            *, __get: _RawDictGet = dict.get) -> _VT | _T: ...

    def keys(self) -> KeysView: ...

    def items(self) -> ItemsView: ...

    @overload
    def pop(self, k: _KT) -> _VT: ...

    @overload
    def pop(self, k: _KT, default: _VT | _T) -> _VT | _T: ...

    def popitem(self) -> tuple[_KT, _VT]: ...

    def setdefault(self, k: _KT, default=None,
                   *, check_lists=True,
                   __get=dict.get) -> _VT: ...

    # noinspection PyDefaultArgument
    def update(self,
               __m: MutableMapping[_KT, _VT] = {},
               *, check_lists=True,
               __skip_init=False,
               **kwargs: _T) -> None: ...

    def values(self) -> ValuesView: ...

    def __dir__(self) -> Iterable[str]: ...
    def __repr__(self) -> str: ...
