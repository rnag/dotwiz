import json
from os import PathLike
from typing import (
    Callable, Protocol, TypeVar, Union,
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

_Copy = Callable[[dict[_KT, _VT]], dict[_KT, _VT]]


class Encoder(Protocol):
    """
    Represents an encoder for Python object -> JSON, e.g. analogous to
    `json.dumps`
    """

    def __call__(self, obj: _JSONObject | _JSONList,
                 **kwargs) -> AnyStr:
        ...

# Ref: https://stackoverflow.com/a/68392079/10237506
class _Update(Protocol):
    def __call__(self, instance: dict,
                 __m: Mapping[_KT, _VT] | None = None,
                 **kwargs: _T) -> None: ...

class _RawDictGet(Protocol):
    @overload
    def __call__(self, obj: dict, key: _KT) -> _VT | None: ...
    @overload
    def __call__(self, obj: dict, key: _KT, default: _VT | _T) -> _VT | _T: ...


def make_dot_wiz(*args: Iterable[_KT, _VT],
                 **kwargs: _T) -> DotWiz: ...

# noinspection PyDefaultArgument
def __upsert_into_dot_wiz__(self: DotWiz,
                            input_dict: MutableMapping[_KT, _VT] = {},
                            *, check_lists=True,
                            __set_dict=False,
                            **kwargs: _T) -> None: ...

def __setitem_impl__(self: DotWiz,
                     key: _KT,
                     value: _VT,
                     *, check_lists=True) -> None: ...

def __merge_impl_fn__(op: Callable[[dict, dict], dict],
                      *,
                      check_lists=True
                      ) -> Callable[[DotWiz, DotWiz | dict], DotWiz]: ...

def __or_impl__(self: DotWiz,
                other: DotWiz | dict,
                *, check_lists=True
                ) -> DotWiz: ...

def __ror_impl__(self: DotWiz,
                 other: DotWiz | dict,
                 *, check_lists=True
                 ) -> DotWiz: ...

def __ior_impl__(self: DotWiz,
                 other: DotWiz | dict,
                 *, check_lists=True,
                 __update: _Update = dict.update): ...


class DotWiz:

    # noinspection PyDefaultArgument
    def __init__(self,
                 input_dict: MutableMapping[_KT, _VT] = {},
                 *, check_lists=True,
                 __set_dict=False,
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

    @classmethod
    def from_json(cls, json_string: str = ..., *,
                       filename: str | PathLike = ...,
                       encoding: str = ...,
                       errors: str = ...,
                       multiline: bool = False,
                       file_decoder=json.load,
                       decoder=json.loads,
                       **decoder_kwargs
                  ) -> Union[DotWiz, list[DotWiz]]:
        """
        De-serialize a JSON string (or file) into a :class:`DotWiz` instance,
        or a list of :class:`DotWiz` instances.

        :param json_string: The JSON string to de-serialize.
        :param filename: If provided, will instead read from a file.
        :param encoding: File encoding.
        :param errors: How to handle encoding errors.
        :param multiline: If enabled, reads the file in JSONL format,
          i.e. where each line in the file represents a JSON object.
        :param file_decoder: The decoder to use, when `filename` is passed.
        :param decoder: The decoder to de-serialize with, defaults
          to `json.loads`.
        :param decoder_kwargs: The keyword arguments to pass in to the decoder.

        :return: a `DotWiz` instance, or a list of `DotWiz` instances.
        """
        ...

    def to_dict(self) -> dict[_KT, _VT]:
        """
        Recursively convert the :class:`DotWiz` instance back to a ``dict``.
        """
        ...

    def to_json(self, *,
                filename: str | PathLike = ...,
                encoding: str = ...,
                errors: str = ...,
                file_encoder=json.dump,
                encoder: Encoder = json.dumps,
                **encoder_kwargs) -> AnyStr:
        """
        Serialize the :class:`DotWiz` instance as a JSON string.

        :param filename: If provided, will save to a file.
        :param encoding: File encoding.
        :param errors: How to handle encoding errors.
        :param file_encoder: The encoder to use, when `filename` is passed.
        :param encoder: The encoder to serialize with, defaults to `json.dumps`.
        :param encoder_kwargs: The keyword arguments to pass in to the encoder.

        :return: a string in JSON format (if no filename is provided)
        """
        ...

    def clear(self) -> None: ...

    def copy(self,
             *, __copy: _Copy = dict.copy) -> DotWiz: ...

    # noinspection PyUnresolvedReferences
    @classmethod
    def fromkeys(cls: type[DotWiz],
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
               __set_dict=False,
               **kwargs: _T) -> None: ...

    def values(self) -> ValuesView: ...

    def __repr__(self) -> str: ...
