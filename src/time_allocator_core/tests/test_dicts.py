from time_allocator_core.tests.test_data import (
    optional_date_test,
    TestModel,
)


def test_include_none() -> None:
    i = TestModel.to_dicts([optional_date_test])[0]

    keys = i.keys()
    assert "optional_date" in keys, "optional_date should be included"


def test_exclude_none() -> None:
    i = TestModel.to_dicts([optional_date_test], include_none=False)[0]

    keys = i.keys()
    assert "optional_date" not in keys, "optional_date should not be included"
