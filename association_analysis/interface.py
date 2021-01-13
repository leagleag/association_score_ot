#!/usr/bin/env python3

import argparse
import sys

from association_analysis.query_api import query_data_into_df_with_columns
from association_analysis.utils import statistics_with_columns
from association_analysis.utils import load_yaml_parameter_file

def parse_args(args):
    """Parse command line options and arguments.
    The rules are '-t ID' and '-d ID' only.

    :param list args: args list from command line.
    :return: arguments map to their values.
    :rtype: Namespace

    """
    parser = argparse.ArgumentParser(
        description="analysis of opentargets association scores for targets and diseases",
    )
    command_group = parser.add_mutually_exclusive_group(required=True)
    command_group.add_argument("-t", "--target_id", help="run analysis for one target id")
    command_group.add_argument("-d", "--disease_id", help="run analysis for one disease id")

    return parser.parse_args(args)

def run_analysis(target_id, disease_id, **kwargs):
    """Translate each possible command into function calls.

    :param str target_id: valid id for a target.
    :param str disease_id: valid id for a disease.
    :param dict **kwargs: use this to pass config parameters.
    :return: dict containing formatted datasets.
    :rtype: dict

    """
    if target_id is not None:
        # -t ID
        payload = {"target": [target_id], "size": kwargs["max_batch_size"]}
        score_df = query_data_into_df_with_columns(
            kwargs["api_url_base"], kwargs["endpoint"], payload,
            kwargs["json_data_columns"])
    elif disease_id is not None:
        # -d ID
        payload = {"disease": [disease_id], "size": kwargs["max_batch_size"]}
        score_df = query_data_into_df_with_columns(
            kwargs["api_url_base"], kwargs["endpoint"], payload,
            kwargs["json_data_columns"])
    stats_series = statistics_with_columns(
        score_df[kwargs["column_for_stats"]], kwargs["stats_columns"])
    return {"score_df": score_df, "stats_series": stats_series}

def print_analysis(**kwargs):
    """Takes scores and stats from `run_analysis` and print them nicely.

    :param dict **kwargs: data from `run_analysis`.

    """
    print("Found {0} scores:".format(kwargs["score_df"].shape[0]))
    print(kwargs["score_df"].to_string(index=False))
    print("Scores statistics:")
    print(kwargs["stats_series"].to_string(header=False))

if __name__ == "__main__":
    config = load_yaml_parameter_file()
    args = parse_args(sys.argv[1:])
    config.update(vars(args))
    results = run_analysis(**config)
    print_analysis(**results)
