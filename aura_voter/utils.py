import json
import os
from collections.abc import Mapping
from decimal import Decimal
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

from eth_account._utils.structured_data.hashing import hash_domain  # noqa
from eth_account._utils.structured_data.hashing import hash_message as hash_eip712_message  # noqa
from eth_account._utils.structured_data.hashing import load_and_validate_structured_message  # noqa
from eth_account._utils.structured_data.validation import validate_structured_data  # noqa
from eth_account.messages import SignableMessage
from eth_utils.curried import to_text
from hexbytes import HexBytes

from aura_voter.web3 import get_web3


def get_abi(contract_name: str) -> Union[Dict, List[Dict]]:
    project_root_dir = os.path.abspath(os.path.dirname(__file__))
    with open(f"{project_root_dir}/abi/{contract_name}.json") as f:
        return json.load(f)


def _encode_structured_data(
        primitive: Union[bytes, int, Mapping] = None,
        *,
        hexstr: str = None,
        text: str = None) -> SignableMessage:
    """
    TODO: this is copypasted code from newer eth-account library that we cannot use it since our
    TODO: web3 version doesn't support it. Migrate to newer v ASAP once web3 is released
    """
    if isinstance(primitive, Mapping):
        validate_structured_data(primitive)
        structured_data = primitive
    else:
        message_string = to_text(primitive, hexstr=hexstr, text=text)
        structured_data = load_and_validate_structured_message(message_string)
    return SignableMessage(
        HexBytes(b'\x01'),
        hash_domain(structured_data),
        hash_eip712_message(structured_data),
    )


def sign_message(message: Dict, private_key: str) -> str:
    """
    EIP712 message signing
    """
    web3 = get_web3()
    encoded_data = _encode_structured_data(primitive=message)
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


def extract_pools_voting_power(choices: List, scores: List) -> Optional[Dict[str, Decimal]]:
    """
    Extract voting power for each pool in snapshot
    """
    pool_voting_results = {}
    if not choices or not scores:
        return
    for index, choice in enumerate(choices):
        pool_voting_results[choice] = Decimal(scores[index])

    return pool_voting_results


reverse_choice_to_pool_name = lambda choices: {v: k for k, v in choices.items()}
