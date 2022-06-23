import json
import os
from typing import Dict
from typing import List
from typing import Union

from eth_account.messages import encode_structured_data

from aura_voter.web3 import get_web3


def get_abi(contract_name: str) -> Union[Dict, List[Dict]]:
    project_root_dir = os.path.abspath(os.path.dirname(__file__))
    with open(f"{project_root_dir}/abi/{contract_name}.json") as f:
        return json.load(f)


def sign_message(message: Dict, private_key: str) -> str:
    """
    EIP712 message signing
    """
    web3 = get_web3()
    encoded_data = encode_structured_data(primitive=message)
    signed_message = web3.eth.account.sign_message(encoded_data, private_key)
    return signed_message['signature'].hex()


def map_choice_id_to_pool_name(choices: List) -> Dict:
    """
    Function to map choice ids to real pool names.

    Reason for that is Snapshot vote query doesn't return real choice pool names, but
    just ids like "40" or "87", so we need to map those ids manually to pool names.

    Note: choice indexes start from 1, not from 0
    """
    snapshot_map = {}
    if not choices:
        return snapshot_map
    # choice indexes start from 1, not from 0
    for index, choice in enumerate(choices):
        snapshot_map[str(index + 1)] = choice
    return snapshot_map


reverse_choice_to_pool_name = lambda choices: {v: k for k, v in choices.items()}
