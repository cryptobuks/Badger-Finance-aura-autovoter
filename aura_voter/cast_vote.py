import time
from copy import deepcopy
from typing import Dict

import requests
import simplejson as json
from web3 import Web3

from aura_voter.aws import get_secret
from aura_voter.constants import ASSUME_ROLE_ARN
from aura_voter.constants import AURA_VOTER_SECRET_ID
from aura_voter.constants import AURA_VOTER_SECRET_KEY
from aura_voter.constants import BADGER_VOTER_ADDRESS
from aura_voter.constants import REGION
from aura_voter.constants import SNAPSHOT_VOTE_API
from aura_voter.rich_logger import logger
from aura_voter.utils import sign_message


class FailedToVoteException(Exception):
    pass


SNAPSHOT_DEFAULT_HEADERS = {
    'Accept': "application/json",
    'Content-Type': "application/json"
}

SNAPSHOT_TYPES = {
    'EIP712Domain': [
        {'name': 'name', 'type': 'string'},
        {'name': 'version', 'type': 'string'},
    ],
    "Vote": [
        {'name': 'from', 'type': 'address'},
        {'name': 'space', 'type': 'string'},
        {'name': 'timestamp', 'type': 'uint64'},
        {'name': 'proposal', 'type': 'bytes32'},
        {'name': 'choice', 'type': 'string'},
        {'name': 'metadata', 'type': 'string'}
    ],
}


SNAPSHOT_SINGLE_CHOICE_TYPES = {
    'EIP712Domain': [
        {'name': 'name', 'type': 'string'},
        {'name': 'version', 'type': 'string'},
    ],
    "Vote": [
        {'name': 'from', 'type': 'address'},
        {'name': 'space', 'type': 'string'},
        {'name': 'timestamp', 'type': 'uint64'},
        {'name': 'proposal', 'type': 'bytes32'},
        {'name': 'choice', 'type': 'uint32'},
        {'name': 'metadata', 'type': 'string'}
    ],
}


SNAPSHOT_DOMAIN = {
    'name': "snapshot",
    'version': "0.1.4",
}


def cast_vote(votes: Dict, snapshot_id: str) -> None:
    types = deepcopy(SNAPSHOT_TYPES)
    private_key = get_secret(
        secret_id=AURA_VOTER_SECRET_ID,
        secret_key=AURA_VOTER_SECRET_KEY,
        region_name=REGION,
        assume_role_arn=ASSUME_ROLE_ARN,
    )
    if not private_key:
        raise FailedToVoteException("Can't fetch private key")
    payload = {
        "domain": SNAPSHOT_DOMAIN,
        "message": {
            'from': Web3.toChecksumAddress(BADGER_VOTER_ADDRESS),
            'space': "aurafinance.eth",
            'timestamp': int(time.time()),
            'proposal': Web3.toBytes(hexstr=snapshot_id),
            'choice': json.dumps(votes, use_decimal=True),
            'metadata': json.dumps({}),
        },
        "primaryType": 'Vote',
        "types": types,
    }
    _vote(payload)


def cast_single_choice_vote(choice: int, snapshot_id: str) -> None:
    """
    Single choice voting function needed for voting on gauges etc
    """
    types = deepcopy(SNAPSHOT_SINGLE_CHOICE_TYPES)
    payload = {
        "domain": SNAPSHOT_DOMAIN,
        "message": {
            'from': Web3.toChecksumAddress(BADGER_VOTER_ADDRESS),
            'space': "aurafinance.eth",
            'timestamp': int(time.time()),
            'proposal': Web3.toBytes(hexstr=snapshot_id),
            'choice': int(choice),
            'metadata': json.dumps({}),
        },
        "primaryType": 'Vote',
        "types": types,
    }
    _vote(payload)


def _vote(payload: Dict) -> None:
    private_key = get_secret(
        secret_id=AURA_VOTER_SECRET_ID,
        secret_key=AURA_VOTER_SECRET_KEY,
        region_name=REGION,
        assume_role_arn=ASSUME_ROLE_ARN,
    )
    if not private_key:
        raise FailedToVoteException("Can't fetch private key")
    signature = sign_message(
        message=payload,
        private_key=private_key
    )
    payload.pop("primaryType")
    payload['types'].pop("EIP712Domain")
    # Convert back bytes32 to string to stringify this to json
    payload['message']['proposal'] = Web3.toHex(payload['message']['proposal'])
    response = requests.post(
        SNAPSHOT_VOTE_API,
        headers=SNAPSHOT_DEFAULT_HEADERS,
        data=json.dumps({
            'address': Web3.toChecksumAddress(BADGER_VOTER_ADDRESS),
            'sig': signature,
            'data': payload,
        }, use_decimal=True)
    )
    if not response.ok:
        logger.error(f"Voting failed on Snapshot. Error: {response.text}")
        raise FailedToVoteException(f"Voting failed on Snapshot. Error: {response.text}")
