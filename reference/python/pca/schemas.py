from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker, ValidationError
from referencing import Registry, Resource

_SCHEMAS_DIR = Path(__file__).resolve().parents[3] / "schemas"

# RFC 3339 date-time: must include time part (T); default checker has "date" but not "date-time"
_FORMAT_CHECKER = FormatChecker()


@_FORMAT_CHECKER.checks("date-time", raises=ValueError)
def _check_date_time(instance: str) -> bool:
    if not isinstance(instance, str) or "T" not in instance:
        raise ValueError("date-time must be RFC3339 with time part (e.g. 2024-01-01T00:00:00Z)")
    datetime.fromisoformat(instance.replace("Z", "+00:00"))
    return True


def _load_schemas() -> tuple[dict[str, dict], Registry]:
    schemas_by_name: dict[str, dict] = {}
    registry = Registry()

    for schema_path in sorted(_SCHEMAS_DIR.glob("*.schema.json")):
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        schemas_by_name[schema_path.name] = schema

        schema_id = schema.get("$id")
        if isinstance(schema_id, str) and schema_id:
            registry = registry.with_resource(uri=schema_id, resource=Resource.from_contents(schema))

        registry = registry.with_resource(
            uri=schema_path.name,
            resource=Resource.from_contents(schema),
        )

    return schemas_by_name, registry


_SCHEMAS_BY_NAME, _SCHEMA_REGISTRY = _load_schemas()


def validate(instance: dict, schema_name: str) -> None:
    schema = _SCHEMAS_BY_NAME.get(schema_name)
    if schema is None:
        raise ValueError(f"Unknown schema: {schema_name}")

    validator = Draft202012Validator(
        schema=schema,
        registry=_SCHEMA_REGISTRY,
        format_checker=_FORMAT_CHECKER,
    )

    try:
        validator.validate(instance)
    except ValidationError as exc:
        raise ValueError(str(exc)) from exc
