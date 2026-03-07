from __future__ import annotations
from pydantic import BaseModel
from abc import ABC
from typing import Any, Self, Sequence
import polars as pl
import json
import math
from decimal import Decimal


class Model(BaseModel, ABC):
    @classmethod
    def from_lf(cls, lf: pl.LazyFrame) -> list[Self]:
        return [cls(**r) for r in lf.collect().to_dicts()]

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump()

    def to_lf(self) -> pl.LazyFrame:
        return pl.LazyFrame(self.to_dict())

    def to_str(self) -> str:
        return str(self.model_dump_json())

    def debug_json(
        self,
        *,
        indent: int = 2,
        sort_keys: bool = False,
        ensure_ascii: bool = False,
    ) -> str:
        return json.dumps(
            self._format_debug_value(self.model_dump()),
            indent=indent,
            sort_keys=sort_keys,
            ensure_ascii=ensure_ascii,
            default=str,
        )

    def print_debug(
        self,
        *,
        indent: int = 2,
        sort_keys: bool = False,
        ensure_ascii: bool = False,
    ) -> str:
        json_str = self.debug_json(
            indent=indent,
            sort_keys=sort_keys,
            ensure_ascii=ensure_ascii,
        )
        print(json_str)
        return json_str

    @classmethod
    def _format_debug_value(cls, value: Any) -> Any:
        if isinstance(value, dict):
            return {k: cls._format_debug_value(v) for k, v in value.items()}
        if isinstance(value, list):
            return [cls._format_debug_value(v) for v in value]
        if isinstance(value, bool):
            return value
        if isinstance(value, int):
            return f"{value:,}"
        if isinstance(value, float):
            return str(value) if not math.isfinite(value) else f"{value:,}"
        if isinstance(value, Decimal):
            return f"{value:,}"
        return value


def to_dicts(models: Sequence[Model]) -> list[dict[str, Any]]:
    return [m.model_dump() for m in models]


def to_lf(models: Sequence[Model]) -> pl.LazyFrame:
    return pl.LazyFrame(to_dicts(models))
