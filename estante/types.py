from typing import Any, Dict, List, Tuple, Union

Item = Tuple[str, Dict[str, Any]]
Items = List[Item]

Number = Union[float, int]
AnyValidValue = Union[dict, list, str, Number, None]
