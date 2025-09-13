from typing import Tuple, List, Any, Dict
from jsonschema import validate, ValidationError

def validate_json_schema(payload: Any, schema: Dict) -> Tuple[bool, List[str]]:
    try:
        validate(instance=payload, schema=schema)
        return True, []
    except ValidationError as e:
        return False, [str(e)]
