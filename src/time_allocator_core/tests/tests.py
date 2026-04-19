from time_allocator_core.tests.test_data import (
    TestModel,
)
from time_allocator_core.dates import now_utc


def test_debug() -> None:
    TestModel(
        value=1000000.23,
        date=now_utc(),
        optional_date=None,
    ).print_debug()
