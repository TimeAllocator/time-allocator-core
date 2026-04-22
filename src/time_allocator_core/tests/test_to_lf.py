from time_allocator_core.dates import dt

from time_allocator_core.tests.test_data import (
    optional_date_test,
    TestModel,
)
import polars as pl


def test_to_lf() -> None:
    df = TestModel.to_lf([optional_date_test]).collect()
    col_names = df.columns

    assert df.drop_nulls("optional_date").height == 0
    assert "optional_date" in col_names, "optional_date should be in columns"

    def test_schema(docs: list[TestModel]) -> None:
        i = TestModel.to_lf(docs).collect_schema()
        assert i["optional_date"] == pl.Datetime(time_zone="UTC")
        assert i["str_list"] == pl.List(pl.String)
        assert i["optional_nested_model"] == pl.Struct(
            [
                pl.Field("value", pl.Float64),
                pl.Field("optional_date", pl.Datetime(time_zone="UTC")),
            ]
        )
        assert i["nested_model_list"] == pl.List(
            pl.Struct(
                [
                    pl.Field("value", pl.Float64),
                    pl.Field("optional_date", pl.Datetime(time_zone="UTC")),
                ]
            )
        )

    test_schema([optional_date_test])
    test_schema([])

    def test_timezone(
        docs: list[TestModel],
    ) -> None:
        i = TestModel.to_lf(
            docs,
            # convert_tz="America/Chicago",
        ).collect_schema()
        # i = pl.LazyFrame(TestModel.to_dicts(docs)).select(
        #     pl.col("date").dt.convert_time_zone("America/New_York")
        # )
        assert i["date"] == pl.Datetime(time_zone="UTC")
        # assert i["optional_date"] == pl.Datetime(timezone="America/New_York")
        # assert i["nested_model_list"] == pl.List(
        #     pl.Struct(
        #         [
        #             pl.Field("value", pl.Float64),
        #             pl.Field("optional_date", pl.Datetime(timezone="America/New_York")),
        #         ]
        #     )
        # )

    test_timezone(
        [
            TestModel(
                value=1000000.23,
                date=dt(2023, 1, 1),
                optional_date=dt(2023, 1, 1),
            )
        ]
    )
