from dataclasses import fields, is_dataclass, MISSING
from typing import Literal, Type, Any, get_origin, get_args


class DataclassToJsonschemaConverter:
    def to_json_schema(self, dataclass: Type) -> dict:
        if not is_dataclass(dataclass):
            raise ValueError("Input must be a dataclass")

        schema = {
            "type": "object",
            "properties": {
                field.name: self._parse_field(field.type) for field in fields(dataclass)
            },
            "required": [
                f.name for f in fields(dataclass)
                if f.default is MISSING and f.default_factory is MISSING
            ],
            "additionalProperties": False
        }

        return {
            "type": "json_schema",
            "json_schema": {
                "name": self._convert_dataclassname_into_schemaname(dataclass=dataclass),
                "schema": schema,
                "strict": True
            }
        }

    @staticmethod
    def is_dataclass(dataclass: Type) -> bool:
        return is_dataclass(dataclass)

    @staticmethod
    def _convert_dataclassname_into_schemaname(dataclass: Type) -> str:
        return dataclass.__name__[0].lower() + "".join(
            [f"_{c.lower()}" if c.isupper() else c for c in dataclass.__name__[1:]])

    def _parse_field(self, field_type: Any) -> dict:
        origin = get_origin(field_type)
        args = get_args(field_type)

        if origin is list and args:
            return {
                "type": "array",
                "items": self._parse_field(args[0])
            }
        elif origin is None and isinstance(field_type, type):
            if issubclass(field_type, str):
                return {"type": "string"}
            elif issubclass(field_type, bool):
                return {"type": "boolean"}
        elif origin is Literal and args:
            return {
                "type": "string",
                "enum": list(args)
            }
        elif is_dataclass(field_type):
            return {
                "type": "object",
                "properties": {
                    f.name: self._parse_field(f.type) for f in fields(field_type)
                },
                "required": [
                    f.name for f in fields(field_type)
                    if f.default is MISSING and f.default_factory is MISSING
                ],
                "additionalProperties": False
            }
        else:
            raise ValueError(f"Unsupported type: {field_type}")
