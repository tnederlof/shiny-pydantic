from typing import Type, Dict, List, Any
from pydantic import BaseModel
from shiny.express import ui
from shiny_pydantic import utility
from shiny_pydantic import checks
from htmltools import Tag


def render_single_number_input(key: str, property: Dict[str, Any]) -> Tag:
    return ui.input_numeric(
        key, property.get("title"), value=float(property.get("default", "0"))
    )


def render_single_string_input(key: str, property: Dict[str, Any]) -> Tag:
    return ui.input_text(key, property.get("title"), value=property.get("default", ""))


def render_single_enum_input(
    key: str, property: Dict[str, Any], references: Dict[str, Any]
) -> Tag:
    if property.get("enum"):
        select_options = property.get("enum", [])  # type: List[str]
    else:
        reference_item = utility.get_single_reference_item(property, references)
        select_options = reference_item.get("enum", [])  # type: List[str]

    return ui.input_selectize(
        key,
        property.get("title"),
        choices=select_options,
        selected=property.get("default", None),
    )


def render_property(
    key: str, property: Dict[str, Any], references: Dict[str, Any]
) -> Tag | None:
    if checks.is_single_number_property(property):
        return render_single_number_input(key, property)

    if checks.is_single_string_property(property):
        return render_single_string_input(key, property)

    if checks.is_single_enum_property(property, references):
        return render_single_enum_input(key, property, references)

    return None


def render_ui(output_data: Type[BaseModel]) -> List | None:
    model_schema = output_data.model_json_schema(by_alias=False)

    model_properties = model_schema.get("properties", {})
    references = model_schema.get("$defs", {})

    if model_properties:
        output_list = []
        for property_key in model_properties.keys():
            property_schema = model_properties.get(property_key)
            if not property_schema.get("title"):
                # if title is not set then try to construct one from the key
                property_schema["title"] = (
                    property_key.title().replace("_", " ").strip()
                )

            if property_schema:
                results = render_property(property_key, property_schema, references)
                output_list.append(results)

        return output_list

    return None
