from __future__ import annotations
from pydantic import BaseModel
from abc import ABC
from typing import Any, Self, Sequence
import polars as pl


class Default(BaseModel, ABC):
    @classmethod
    def from_polars(cls, lf: pl.LazyFrame) -> list[Self]:
        return [cls(**r) for r in lf.collect().to_dicts()]


    def to_dict(self) -> dict[str, Any]:
        return self.model_dump()
    

    def to_lf(self) -> pl.LazyFrame:
        return pl.LazyFrame(self.to_dict())


    def to_str(self) -> str:
        return str(self.model_dump_json())
    

def to_dicts(models: Sequence[Default]) -> list[dict[Any, Any]]:
    return [m.model_dump() for m in models]


def to_lf(models: Sequence[Default]) -> pl.LazyFrame:
    return pl.LazyFrame(to_dicts(models))