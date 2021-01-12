import os
import pytest
import pandas as pd

from unittest.mock import patch

from association_analysis import interface as cli

def test_cli_entrypoint():
    assert os.system("python association_analysis/interface.py -h") == 0

def test_cli_correct_help_message_logic(capsys):
    with pytest.raises(SystemExit) as e:
        cli.parse_args(["-h"])
    captured = capsys.readouterr()
    assert "usage: __main__.py [-h] (-t TARGET_ID | -d DISEASE_ID)" in captured.out
    assert e.value.code == 0

def test_cli_correct_target_call():
    parser = cli.parse_args(["-t", "target_id"])
    assert parser.target_id == "target_id"

def test_cli_correct_disease_call():
    parser = cli.parse_args(["-d", "disease_id"])
    assert parser.disease_id == "disease_id"

def test_cli_incorrect_no_option(capsys):
    with pytest.raises(SystemExit) as e:
        cli.parse_args(["an_id_only"])
    captured = capsys.readouterr()
    assert "error: one of the arguments -t/--target_id -d/--disease_id is required" in captured.err
    assert e.value.code == 2

def test_cli_incorrect_dual_option(capsys):
    with pytest.raises(SystemExit) as e:
        cli.parse_args(["-d", "-t", "some_id"])
    captured = capsys.readouterr()
    assert "error: argument -d/--disease_id: expected one argument" in captured.err
    assert e.value.code == 2

@pytest.mark.parametrize(
    "target_id, disease_id",
    [
        ("exists",None),
        (None,"exists")
    ]
)
def test_run_analysis(target_id, disease_id):
    expected_df = pd.DataFrame(["tid", "", "scores"], columns=["scores_column"])
    expected_series = pd.Series(["stats"])
    with patch("association_analysis.interface.query_data_into_df_with_columns", return_value=expected_df), \
        patch("association_analysis.interface.statistics_with_columns", return_value=expected_series):
        out_dict = cli.run_analysis(target_id, disease_id, "scores_column")
    pd.testing.assert_frame_equal(out_dict["score_df"], expected_df)
    pd.testing.assert_series_equal(out_dict["stats_series"], expected_series)
