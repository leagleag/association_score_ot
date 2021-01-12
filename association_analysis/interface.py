#!/usr/bin/env python3

import argparse
import sys

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

if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    results = run_analysis(**args)
    print_analysis(**results)
