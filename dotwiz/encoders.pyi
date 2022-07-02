import json
from typing import Any


class DotWizEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any: ...

class DotWizPlusEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any: ...

class DotWizPlusSnakeEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any: ...
