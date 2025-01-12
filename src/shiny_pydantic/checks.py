from typing import Dict
from shiny_pydantic import utility


def is_single_string_property(property: Dict) -> bool:
    return property.get("type") == "string"


def is_single_number_property(property: Dict) -> bool:
    return property.get("type") in ["integer", "number"]


def is_single_enum_property(property: Dict, references: Dict) -> bool:
    if property.get("enum"):
        return True
    try:
        _ = utility.get_single_reference_item(property, references)["enum"]
        return True
    except Exception:
        return False
