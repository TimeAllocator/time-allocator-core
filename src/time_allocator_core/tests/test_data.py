from __future__ import annotations
from time_allocator_core.client import Model
from time_allocator_core.dates import dt, datetime
from pydantic import Field
from typing import Literal


class NestedModel(Model):
    value: float = 1.0
    optional_date: datetime | None = None


class TestModel(Model):
    value: float
    date: datetime
    optional_date: datetime | None = None
    str_list: list[str] = []
    optional_nested_model: NestedModel | None = NestedModel()
    nested_model_list: list[NestedModel] = [NestedModel()]
    str_field: str = Field(default="default")
    kind: Kind = "test"

    type Kind = Literal["kind1", "kind2"]


optional_date_test = TestModel(
    value=1,
    date=dt(2023, 1, 1),
    optional_date=None,
)

test_models = [
    optional_date_test,
]
