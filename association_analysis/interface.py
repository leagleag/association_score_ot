#!/usr/bin/env python3

import argparse
import sys

from association_analysis.query_api import query_data_into_df_with_columns
from association_analysis.utils import statistics_with_columns
def parse_args(args):
    """define the set of possible cl commands"""
    parser = argparse.ArgumentParser(
        # prog="getscore",
        description="analysis of opentargets association scores for targets and diseases",
    )
    command_group = parser.add_mutually_exclusive_group(required=True)
    command_group.add_argument("-t", "--target_id", help="run analysis for one target id")
    command_group.add_argument("-d", "--disease_id", help="run analysis for one disease id")

    return parser.parse_args(args)

def run_analysis(target_id, disease_id, stats_on_column):
    """translate each possible command into function calls"""
    if target_id is not None:
        # -t ID
        payload = {"target": [target_id], "size": max_batch_size}
        score_df = query_data_into_df_with_columns(api_url_base, endpoint, payload, json_data_columns)
    elif disease_id is not None:
        # -d ID
        payload = {"disease": [disease_id], "size": max_batch_size}
        score_df = query_data_into_df_with_columns(api_url_base, endpoint, payload, json_data_columns)
    stats_series = statistics_with_columns(score_df[stats_on_column], stats_columns)
    return {"score_df": score_df, "stats_series": stats_series}
if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    results = run_analysis(**args, stats_on_column=stats_on_column)
    print_analysis(**results)
