from typing import Any, Dict, List, TypeAlias, Union
from typing_extensions import NotRequired, TypedDict


class OptionDict(TypedDict):
    label: NotRequired[str]
    value: NotRequired[str]


DictStrAny: TypeAlias = Dict[str, Any]
DictStr: TypeAlias = Dict[str, str]
Expression: TypeAlias = str
OptionsType: TypeAlias = List[Union[OptionDict, str, DictStr]]
DataMapping: TypeAlias = str
