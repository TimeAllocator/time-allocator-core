from __future__ import annotations
from polars._typing import PolarsDataType

import json
import math
from decimal import Decimal
from typing import (
    Self,
    Sequence,
    Any,
    get_args,
    get_origin,
    Union,
)
from abc import ABC
from datetime import date, datetime, time
from enum import Enum
import polars as pl
from pydantic import BaseModel
from pydantic.v1.schema import schema


class Model(BaseModel, ABC):
    @classmethod
    def polars_schema(cls) -> pl.Schema:
        return pl.Schema(
            {
                name: cls._annotation_to_polars_dtype(field.annotation)
                for name, field in cls.model_fields.items()
            }
        )

    @classmethod
    def _annotation_to_polars_dtype(cls, annotation: Any) -> PolarsDataType:
        origin = get_origin(annotation)
        args = get_args(annotation)

        if annotation is str:
            return pl.String()
        if annotation is int:
            return pl.Int64()
        if annotation is float:
            return pl.Float64()
        if annotation is bool:
            return pl.Boolean()
        if annotation is datetime:
            return pl.Datetime()
        if annotation is date:
            return pl.Date()
        if annotation is time:
            return pl.Time()

        if origin is list:
            inner = args[0] if args else Any
            return pl.List(cls._annotation_to_polars_dtype(inner))

        if origin is dict:
            return pl.Object()

        if origin is Union:
            non_none_args = [a for a in args if a is not type(None)]
            if len(non_none_args) == 1:
                return cls._annotation_to_polars_dtype(non_none_args[0])

        if isinstance(annotation, type) and issubclass(annotation, Enum):
            return pl.String()

        if isinstance(annotation, type) and issubclass(annotation, BaseModel):
            return pl.Struct(
                {
                    name: cls._annotation_to_polars_dtype(field.annotation)
                    for name, field in annotation.model_fields.items()
                }
            )

        return pl.Object()

    @classmethod
    def from_lf(cls, lf: pl.LazyFrame) -> list[Self]:
        return [cls(**r) for r in lf.collect().to_dicts()]

    def to_dict(self, include_none: bool = True) -> dict[str, Any]:
        return self.model_dump(exclude_none=not include_none)

    def to_lf(self) -> pl.LazyFrame:
        return pl.LazyFrame(
            schema=self.polars_schema(),
            data=self.to_dict(),
        )

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

    @classmethod
    def to_lf_(
        cls,
        models: Sequence[Self],
    ) -> pl.LazyFrame:
        return pl.LazyFrame(
            schema=cls.polars_schema(),
            data=cls.to_dicts(models, include_none=True),
        )

    @classmethod
    def to_dicts(
        cls,
        models: Sequence[Self],
        include_none: bool = True,
    ) -> list[dict[str, Any]]:
        return [m.to_dict(include_none) for m in models]
