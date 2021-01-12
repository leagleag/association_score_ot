#!/usr/bin/env python3

import pandas as pd
import yaml

def json_to_df_with_columns(data_json, columns_list):
    return pd.json_normalize(data_json).loc[:,columns_list]

def statistics_with_columns(data_series, columns_list):
    return data_series.describe()[columns_list]

def load_yaml_parameter_file(path="./config.yml"):
    try:
        config = yaml.load(open(path), Loader=yaml.Loader)
    except yaml.YAMLError as e:
        print("error", e)
        raise
    return config
