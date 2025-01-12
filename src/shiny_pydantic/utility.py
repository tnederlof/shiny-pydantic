from typing import Dict, Any


def resolve_reference(reference: str, references: Dict[str, Any]) -> Dict[str, Any]:
    return references[reference.split("/")[-1]]


def get_single_reference_item(
    property: Dict, references: Dict[str, Any]
) -> Dict[str, Any]:
    reference = property.get("$ref")
    if reference is None:
        reference = property["allOf"][0]["$ref"]
    return resolve_reference(reference, references)
