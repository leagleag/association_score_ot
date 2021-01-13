#!/usr/bin/env python3

import pandas as pd
import yaml
import sys

def json_to_df_with_columns(data_json, columns_list):
    try:
        return pd.json_normalize(data_json).loc[:,columns_list]
    except KeyError as e:
        print("""One or more {0} could not be found in json data {1}.
        Probable causes:
        - the id is not a valid target or disease id
        - one or more column names do not exist in the data
        """.format(columns_list, data_json))
        raise

def statistics_with_columns(data_series, columns_list):
    return data_series.describe()[columns_list]

def load_yaml_parameter_file(path="./config.yml"):
    try:
        config = yaml.load(open(path), Loader=yaml.Loader)
    except yaml.YAMLError as e:
        print("error", e)
        raise
    return config
