from unittest import TestCase
from unittest.mock import patch
import pytest
import requests
import pandas as pd
import itertools

import responses

from association_analysis import query_api

api_url_base = "https://platform-api.opentargets.io/v3/platform"
# endpoint to use for association analysis
endpoint = "/public/association/filter"

@pytest.mark.parametrize(
    "url_endpoint,payload,expected_response",
    [
        ("{0}{1}".format(api_url_base, endpoint), {"target": ["ENSG00000197386"], "size": 1}, (200, 1, "application/json")),
        ("{0}{1}".format(api_url_base, endpoint), {"disease": ["Orphanet_399"], "size": 1}, (200, 1, "application/json")),
        ("{0}{1}".format(api_url_base, endpoint), {"target": ["Orphanet_oh_no"], "size": 1}, (200, 0, "application/json")),
    ]
)
def test_post_single_payload(url_endpoint, payload, expected_response):
    response = requests.post(url_endpoint, json=payload)
    response_body = response.json()
    assert (
        response.status_code,
        len(response_body["data"]),
        response.headers["Content-Type"]) == expected_response

@responses.activate
def test_post_single_payload_when_response_is_ok():
    expected_dict = {"dummy": "payload"}
    responses.add(
        responses.POST,
        "https://www.host.com/fake/base/url/fake/endpoint",
        json=expected_dict,
        status=200,
    )
    data_dict = query_api.post_single_payload("https://www.host.com/fake/base/url", "/fake/endpoint", "s")
    TestCase().assertDictEqual(data_dict, expected_dict)

@responses.activate
def test_post_single_payload_when_response_is_not_ok():
    expected_dict = {"dummy": "payload"}
    responses.add(
        responses.POST,
        "https://www.host.com/fake/base/url/fake/endpoint",
        json=expected_dict,
        status=400,
    )
    data_dict = query_api.post_single_payload("https://www.host.com/fake/base/url", "/fake/endpoint", "s")
    assert data_dict is None

@pytest.mark.parametrize(
    "data_dict,expected",
    [
        ({"data": "OMG"}, ({"data": "OMG"},)),
        ({"data": "OMG", "next": "here"}, ({"data": "OMG", "next": "here"},{"data": "OMG", "next": "here"}))
    ]
)
def test_post_payload_generator(data_dict, expected):
    with patch("association_analysis.query_api.post_single_payload", return_value=data_dict):
        g = query_api.post_payload_generator("/fake/base/url", "/fake/endpoint", {"dummy": "payload"})
        assert tuple(itertools.islice(g, 2)) == expected

def test_query_data_into_df_with_columns():
    expected_df = pd.DataFrame(index=[0, 0], data=[1, 2], columns=["column_i_want"])
    with patch(
        "association_analysis.query_api.post_payload_generator",
        return_value=[{"data": {"column_i_want":1, "no":42}}, {"data": {"column_i_want":2, "yes":42}}]
    ):
        data_df = query_api.query_data_into_df_with_columns("/url/base", "/endpoint", {"some": "payload"}, ["column_i_want"])
    pd.testing.assert_frame_equal(expected_df, data_df)
