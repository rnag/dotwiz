import json
from typing import (
    AnyStr, Any, Callable, Iterable,
    Mapping, MutableMapping,
    Protocol, TypeVar,
)

_T = TypeVar('_T')
_KT = TypeVar('_KT')
_VT = TypeVar('_VT')

# Valid collection types in JSON.
_JSONList = list[Any]
_JSONObject = dict[str, Any]

_SetItem = Callable[[dict, _KT, _VT], None]

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


__SPECIAL_KEYS: dict[str, str] = ...
__IS_KEYWORD: Callable[[object], bool] = ...


def make_dot_wiz_plus(*args: Iterable[_KT, _VT],
                      **kwargs: _T) -> DotWizPlus: ...

def __store_in_object__(self: DotWizPlus,
                        __self_dict: MutableMapping[_KT, _VT],
                        key: _KT,
                        value: _VT,
                        *, __set: _SetItem = dict.__setitem__) -> None: ...

# noinspection PyDefaultArgument
def __upsert_into_dot_wiz_plus__(self: DotWizPlus,
                                 input_dict: MutableMapping[_KT, _VT] = {},
                                 **kwargs: _T) -> None: ...

def __setitem_impl__(self: DotWizPlus,
                     key: _KT,
                     value: _VT) -> None: ...


class DotWizPlus(dict):

    # noinspection PyDefaultArgument
    def __init__(self,
                 input_dict: MutableMapping[_KT, _VT] = {},
                 **kwargs: _T) -> None: ...

    def __delattr__(self, item: str) -> None: ...
    def __delitem__(self, v: _KT) -> None: ...

    def __getattr__(self, item: str) -> _VT: ...
    def __getitem__(self, k: _KT) -> _VT: ...

    def __setattr__(self, item: str, value: _VT) -> None: ...
    def __setitem__(self, k: _KT, v: _VT) -> None: ...

    def to_attr_dict(self) -> dict[_KT, _VT]:
        """
        Recursively convert the :class:`DotWizPlus` instance back to a ``dict``,
        while preserving the lower-cased keys used for attribute access.
        """
        ...

    def to_dict(self) -> dict[_KT, _VT]:
        """
        Recursively convert the :class:`DotWizPlus` instance back to a ``dict``.
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

    # noinspection PyDefaultArgument
    def update(self,
               __m: MutableMapping[_KT, _VT] = {},
               **kwargs: _T) -> None: ...

    def __dir__(self) -> Iterable[str]: ...

    def __repr__(self) -> str: ...
