from time_allocator_core.tests.test_data import (
    test_models,
    TestModel,
)
from time_allocator_core.client import (
    to_lf,
)
from time_allocator_core.dates import now_utc


def test_to_lf() -> None:
    df = to_lf(test_models).collect()
    assert df is not None  # assert


def test_debug() -> None:
    TestModel(
        value=1000000.23,
        date=now_utc(),
        optional_date=None,
    ).print_debug()
