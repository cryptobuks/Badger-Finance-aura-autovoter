import json

import boto3
from moto import mock_secretsmanager
from moto import mock_sts

from aura_voter.aws import get_secret
from aura_voter.constants import ASSUME_ROLE_ARN
from aura_voter.constants import AURA_VOTER_SECRET_ID
from aura_voter.constants import AURA_VOTER_SECRET_KEY
from aura_voter.constants import REGION


@mock_secretsmanager
def test_get_secret_happy():
    secret_value = "private_key"
    conn = boto3.client("secretsmanager", region_name=REGION)
    conn.create_secret(
        Name=AURA_VOTER_SECRET_ID, SecretString=json.dumps({
            AURA_VOTER_SECRET_KEY: secret_value
        })
    )
    assert get_secret(
        secret_id=AURA_VOTER_SECRET_ID,
        secret_key=AURA_VOTER_SECRET_KEY,
    ) == secret_value


@mock_secretsmanager
@mock_sts
def test_get_secret_assume_role_happy():
    secret_value = "private_key"
    conn = boto3.client("secretsmanager", region_name=REGION)
    conn.create_secret(
        Name=AURA_VOTER_SECRET_ID, SecretString=json.dumps({
            AURA_VOTER_SECRET_KEY: secret_value
        })
    )
    get_secret(
        secret_id=AURA_VOTER_SECRET_ID,
        secret_key=AURA_VOTER_SECRET_KEY,
        assume_role_arn=ASSUME_ROLE_ARN,
    )
    assert get_secret(
        secret_id=AURA_VOTER_SECRET_ID,
        secret_key=AURA_VOTER_SECRET_KEY,
    ) == secret_value


@mock_secretsmanager
def test_get_secret_binary_happy():
    secret_value = "private_key"
    conn = boto3.client("secretsmanager", region_name=REGION)
    conn.create_secret(
        Name=AURA_VOTER_SECRET_ID, SecretBinary=json.dumps({
            AURA_VOTER_SECRET_KEY: secret_value
        }).encode()
    )
    assert get_secret(
        secret_id=AURA_VOTER_SECRET_ID,
        secret_key=AURA_VOTER_SECRET_KEY,
    ) == secret_value


@mock_secretsmanager
def test_get_secret_unhappy():
    assert get_secret(
        secret_id=AURA_VOTER_SECRET_ID,
        secret_key=AURA_VOTER_SECRET_KEY,
    ) is None
