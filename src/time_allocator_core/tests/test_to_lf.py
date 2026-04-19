from time_allocator_core.tests.test_data import (
    optional_date_test,
    TestModel,
)
import polars as pl


def test_to_lf() -> None:
    df = TestModel.to_lf_([optional_date_test]).collect()
    col_names = df.columns

    assert df.drop_nulls("optional_date").height == 0
    assert "optional_date" in col_names, "optional_date should be in columns"


def test_schema() -> None:
    df = TestModel.to_lf_([optional_date_test])
    schema = df.collect_schema()
    assert schema["optional_date"] == pl.Datetime
    assert schema["str_list"] == pl.List(pl.String)
    assert schema["optional_nested_model"] == pl.Struct(
        [
            pl.Field("value", pl.Float64),
            pl.Field("optional_date", pl.Datetime),
        ]
    )
    assert schema["nested_model_list"] == pl.List(
        pl.Struct(
            [
                pl.Field("value", pl.Float64),
                pl.Field("optional_date", pl.Datetime),
            ]
        )
    )
