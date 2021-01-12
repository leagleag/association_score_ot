#!/usr/bin/env python3

import requests
import json
import pandas as pd

from association_analysis.utils import json_to_df_with_columns

def post_single_payload(api_url_base, endpoint, payload):
    api_url = "{0}{1}".format(api_url_base, endpoint)

    response = requests.post(api_url, json=payload)

    if response.status_code == 200:
        return json.loads(response.content.decode("utf-8"))
    else:
        print("An unhandled error {0} happened".format(response.status_code))
        return None

def post_payload_generator(api_url_base, endpoint, payload):
    first = True
    while first or ("next" in data_dict):
        data_dict = post_single_payload(api_url_base, endpoint, payload)
        if "next" in data_dict:
            payload["next"] = data_dict["next"]
        first = False
        yield data_dict

def query_data_into_df_with_columns(api_url_base, endpoint, payload, columns_list):
    data_df_list = []
    for batch_json in post_payload_generator(api_url_base, endpoint, payload):
        data_df_list.append(json_to_df_with_columns(batch_json["data"], columns_list))
    data_df = pd.concat(data_df_list)
    return data_df
