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

_SetAttribute = Callable[[DotWiz, str, Any], None]


# Ref: https://stackoverflow.com/a/68392079/10237506
class _Update(Protocol):
    def __call__(self, instance: dict,
                 __m: Mapping[_KT, _VT] | None = None,
                 **kwargs: _T) -> None: ...

class Encoder(Protocol):
    """
    Represents an encoder for Python object -> JSON, e.g. analogous to
    `json.dumps`
    """

    def __call__(self, obj: _JSONObject | _JSONList,
                 **kwargs) -> AnyStr:
        ...


def make_dot_wiz(*args: Iterable[_KT, _VT],
                 **kwargs: _T) -> DotWiz: ...

# noinspection PyDefaultArgument
def __upsert_into_dot_wiz__(self: DotWiz,
                            input_dict: MutableMapping[_KT, _VT] = {},
                            *, check_lists=True,
                            **kwargs: _T) -> None: ...

def __setitem_impl__(self: DotWiz,
                     key: _KT,
                     value: _VT,
                     *, check_lists=True) -> None: ...

def __merge_impl_fn__(op: Callable[[dict, dict], dict],
                      *, check_lists=True,
                      __set: _SetAttribute = object.__setattr__
                      ) -> Callable[[DotWiz, DotWiz | dict], DotWiz]: ...

def __imerge_impl__(self: DotWiz,
                    other: DotWiz | dict,
                    *, check_lists=True,
                    __update: _Update = dict.update): ...


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
    def __reversed__(self) -> Reversible: ...

    def __or__(self, other: DotWiz | dict) -> DotWiz: ...
    def __ior__(self, other: DotWiz | dict) -> DotWiz: ...
    def __ror__(self, other: DotWiz | dict) -> DotWiz: ...

    def to_dict(self) -> dict[_KT, _VT]:
        """
        Recursively convert the :class:`DotWiz` instance back to a ``dict``.
        """
        ...

    def to_json(self, *,
                encoder: Encoder = json.dumps,
                **encoder_kwargs) -> AnyStr:
        """
        Serialize the :class:`DotWiz` instance as a JSON string.

        :param encoder: The encoder to serialize with, defaults to `json.dumps`.
        :param encoder_kwargs: The keyword arguments to pass in to the encoder.
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

    @overload
    def pop(self, k: _KT) -> _VT: ...

    @overload
    def pop(self, k: _KT, default: _VT | _T) -> _VT | _T: ...

    def popitem(self) -> tuple[_KT, _VT]: ...

    def setdefault(self, k: _KT, default=None) -> _VT: ...

    # noinspection PyDefaultArgument
    def update(self,
               __m: MutableMapping[_KT, _VT] = {},
               *, check_lists=True,
               **kwargs: _T) -> None: ...

    def values(self) -> ValuesView: ...

    def __repr__(self) -> str: ...
