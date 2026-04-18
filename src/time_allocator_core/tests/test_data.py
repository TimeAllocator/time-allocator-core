from time_allocator_core.client import Model
from time_allocator_core.dates import datetime


class TestModel(Model):
    value: float
    date: datetime
    optional_date: datetime | None = None


optional_date_test = TestModel(
    value=1,
    date=datetime(2023, 1, 1),
    optional_date=None,
)
test_models = [
    optional_date_test,
]
