import time
from unittest.mock import MagicMock

import pytest

from aura_voter.utils import get_abi
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
            'space': "cvx.eth",
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
