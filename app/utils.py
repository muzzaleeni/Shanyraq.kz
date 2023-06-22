import importlib
import os
from datetime import datetime
from typing import Any, Callable
from zoneinfo import ZoneInfo

import orjson
from bson.objectid import ObjectId
from pydantic import BaseModel, root_validator


def orjson_dumps(v: Any, *, default: Callable[[Any], Any] | None) -> str:
    return orjson.dumps(v, default=default).decode()


def convert_datetime_to_gmt(dt: datetime) -> str:
    if not dt.tzinfo:
        dt = dt.replace(tzinfo=ZoneInfo("UTC"))

    return dt.strftime("%Y-%m-%dT%H:%M:%S%z")


class AppModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
        json_encoders = {datetime: convert_datetime_to_gmt, ObjectId: str}
        allow_population_by_field_name = True

    @root_validator()
    def set_null_microseconds(cls, data: dict[str, Any]) -> dict[str, Any]:
        datetime_fields = {
            k: v.replace(microsecond=0)
            for k, v in data.items()
            if isinstance(k, datetime)
        }

        return {**data, **datetime_fields}


def import_routers_from_folder(folder_path, router):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".py") and file != "__init__.py":
                module_path = os.path.join(root, file).replace("/", ".")[:-3]
                try:
                    router_module = importlib.import_module(module_path)
                    router.include_router(router_module.router)
                except Exception as e:
                    print(f"Failed to import {module_path}, error: {e}")
