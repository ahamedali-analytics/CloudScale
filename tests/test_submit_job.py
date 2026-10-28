
import json
import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "backend" / "submit_job"),
)

import app


@pytest.fixture
def lambda_context():
    context = MagicMock()
    context.aws_request_id = "local-test"
    return context


@pytest.fixture
def lambda_event():
    return {
        "body": json.dumps({
            "records": [{"name": "A", "amount": 100}]
        })
    }


def test_rejects_malformed_json(lambda_context):
    result = app.lambda_handler({"body": '{"records":'}, lambda_context)

    assert result["statusCode"] == 400


@pytest.mark.parametrize("body", ['[]', '"hello"', "123", "null"])
def test_rejects_non_object_body(body, lambda_context):
    result = app.lambda_handler({"body": body}, lambda_context)

    assert result["statusCode"] == 400


def test_rejects_empty_records(lambda_context):
    result = app.lambda_handler(
        {"body": json.dumps({"records": []})},
        lambda_context,
    )

    assert result["statusCode"] == 400


def test_rejects_non_object_records(lambda_context):
    result = app.lambda_handler(
        {"body": json.dumps({"records": ["not-an-object"]})},
        lambda_context,
    )

    assert result["statusCode"] == 400
