from time_allocator_core.tests.test_data import (
    optional_date_test,
    test_models,
    TestModel,
)
from time_allocator_core.client import (
    to_dicts,
    to_lf,
)
from time_allocator_core.dates import now_utc


def test_include_none() -> None:
    i = to_dicts([optional_date_test])[0]

    keys = i.keys()
    assert "optional_date" in keys, "optional_date should be included"


def test_exclude_none() -> None:
    i = to_dicts([optional_date_test], include_none=False)[0]

    keys = i.keys()
    assert "optional_date" not in keys, "optional_date should not be included"


def test_to_lf() -> None:
    df = to_lf(test_models).collect()
    assert df is not None  # assert


def test_debug() -> None:
    TestModel(
        value=1000000.23,
        date=now_utc(),
        optional_date=None,
    ).print_debug()


if __name__ == "__main__":
    test_debug()
    test_exclude_none()
    test_include_none()
