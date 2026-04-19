from __future__ import annotations
from time_allocator_core.client import Model
from time_allocator_core.dates import datetime


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


optional_date_test = TestModel(
    value=1,
    date=datetime(2023, 1, 1),
    optional_date=None,
)

test_models = [
    optional_date_test,
]
