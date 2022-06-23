import time
from unittest.mock import MagicMock

import pytest

from aura_voter.tests.test_data.test_data import PROPOSAL_TEST_DATA
from aura_voter.utils import get_abi
from aura_voter.utils import map_choice_id_to_pool_name
from aura_voter.utils import reverse_choice_to_pool_name
from aura_voter.utils import sign_message


def test_get_abi():
    abi = get_abi("ERC20")
    assert abi[0]['outputs'] is not None


def test_get_abi_raises():
    with pytest.raises(FileNotFoundError):
        get_abi("unknown_abi")


def test_sign_message(mocker):
    mocker.patch(
        "aura_voter.utils.get_web3",
        return_value=MagicMock(eth=MagicMock(
            account=MagicMock(
                sign_message=MagicMock(return_value={
                    'signature': b"\x9d\xa7\x12P\xaf\xd0\xb6'\
                    x9b\x06\xc5\xfd/\xb9\x83y'\xb3\xff\x9e\x05\xcf"}
                )
            )
        ))
    )
    msg = {
        "domain": {
            "chainId": 1,
            "name": 'snapshot',
            "verifyingContract": '0xCcCCccccCCCCcCCCCCCcCcCccCcCCCcCcccccccC',
            "version": '0.1.4',
        },
        "message": {
            'from': "0x12d8E12e981be773cb777Be342a528228b3c7661",
            'space': "unknown.eth",
            'timestamp': int(time.time()),
            'proposal': "QmetYVgwr8MXEBVg4gHNNK2D5Jre18vtJgC14VhDirh4VJ",
            'choice': "pogger",
            'metadata': "",
        },
        "primaryType": 'Vote',
        "types": {
            'EIP712Domain': [
                {'name': 'name', 'type': 'string'},
                {'name': 'version', 'type': 'string'},
                {'name': 'chainId', 'type': 'uint256'},
                {'name': 'verifyingContract', 'type': 'address'},
            ],
            "Vote": [
                {'name': 'from', 'type': 'address'},
                {'name': 'space', 'type': 'string'},
                {'name': 'timestamp', 'type': 'uint64'},
                {'name': 'proposal', 'type': 'string'},
                {'name': 'choice', 'type': 'string'},
                {'name': 'metadata', 'type': 'string'}
            ],
        },
    }
    signature = sign_message(
        message=msg,
        # Some random pk
        private_key="123"
    )
    assert signature == '9da71250afd0b62720202020202020202020202020202' \
                        '0202020202078396206c5fd2fb9837927b3ff9e05cf'


def test_map_choice_id_to_pool_name():
    gauge_pool_snapshot = PROPOSAL_TEST_DATA['proposals'][0]
    mapped_pools = map_choice_id_to_pool_name(gauge_pool_snapshot['choices'])
    assert len(mapped_pools) == len(gauge_pool_snapshot['choices'])


def test_reverse_choice_to_pool_name():
    gauge_pool_snapshot = PROPOSAL_TEST_DATA['proposals'][0]
    mapped_pools = map_choice_id_to_pool_name(gauge_pool_snapshot['choices'])
    reversed_pools = reverse_choice_to_pool_name(mapped_pools)
    assert len(reversed_pools) == len(gauge_pool_snapshot['choices'])


def test_test_map_choice_id_to_pool_name_empty():
    assert map_choice_id_to_pool_name([]) == {}
