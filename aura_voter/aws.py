from typing import Optional
from typing import Union

import boto3
import simplejson as json
from botocore.errorfactory import ClientError
from aura_voter.constants import REGION

from aura_voter.rich_logger import logger

VOTE_BUCKET_NAME = "badger-voting-bot"


def get_assume_role_credentials(assume_role_arn: str, session_name: str = "AssumeRoleSession1"):
    sts_client = boto3.client("sts")

    assumed_role_object = sts_client.assume_role(
        RoleArn=assume_role_arn, RoleSessionName=session_name
    )
    credentials = assumed_role_object["Credentials"]

    return credentials


def get_secret(
    secret_id: str,
    secret_key: str,
    region_name: str = REGION,
    assume_role_arn: Optional[str] = None,
) -> Optional[Union[str, bytes]]:
    if assume_role_arn:
        logger.info("Assume role given, try to get assume role creds")
        credentials = get_assume_role_credentials(assume_role_arn)
        # Use the temporary credentials that AssumeRole returns to create session
        session = boto3.session.Session(
            aws_access_key_id=credentials["AccessKeyId"],
            aws_secret_access_key=credentials["SecretAccessKey"],
            aws_session_token=credentials["SessionToken"],
        )
        client = session.client(
            service_name="secretsmanager",
            region_name=region_name,
            aws_access_key_id=credentials["AccessKeyId"],
            aws_secret_access_key=credentials["SecretAccessKey"],
            aws_session_token=credentials["SessionToken"],
        )
    else:
        session = boto3.session.Session()
        client = session.client(
            service_name="secretsmanager",
            region_name=region_name,
        )
    try:
        secret_value = client.get_secret_value(SecretId=secret_id)
    except ClientError as e:
        logger.error(f"get secret value response error: {e}")
    else:
        if "SecretString" in secret_value:
            return json.loads(secret_value["SecretString"])[secret_key]
        else:
            return json.loads(secret_value["SecretBinary"].decode())[secret_key]
    return None
