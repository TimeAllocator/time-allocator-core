from time_allocator_core.tests.test_data import (
    optional_date_test,
)
from time_allocator_core.client import (
    to_lf,
)


def test_to_lf() -> None:
    df = to_lf([optional_date_test]).collect()
    col_names = df.columns

    assert df.drop_nulls("optional_date").height == 0
    assert "optional_date" in col_names, "optional_date should be in columns"
