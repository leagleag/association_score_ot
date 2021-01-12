#!/usr/bin/env python3

import pandas as pd

def json_to_df_with_columns(data_json, columns_list):
    return pd.json_normalize(data_json).loc[:,columns_list]

def statistics_with_columns(data_series, columns_list):
    return data_series.describe()[columns_list]
