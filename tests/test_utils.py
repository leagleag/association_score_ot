import pandas as pd
import statistics as st

from association_analysis import utils

def test_json_to_df_with_columns():
    input_json = {
        "level0": {"deeper": {"column_i_want":2, "not_this_one":42}},
        "level1": {"deeper": {"column_i_want":3, "not_this_one":42}}}
    columns_list = ["level0.deeper.column_i_want", "level1.deeper.column_i_want"]
    expected_df = pd.DataFrame(data=[[2,3]], columns=columns_list)
    df = utils.json_to_df_with_columns(input_json, columns_list)
    pd.testing.assert_frame_equal(expected_df, df)

def test_statistics_with_columns():
    input_series = pd.Series([1.0, 2.0, 3.0, 4.0])
    columns_list = ["min", "max", "mean", "std"]
    expected_series = pd.Series(index=columns_list,
        data=[1, 4, st.mean(input_series.values), st.stdev(input_series.values)])
    out_series = utils.statistics_with_columns(input_series, columns_list)
    pd.testing.assert_series_equal(expected_series, out_series)
