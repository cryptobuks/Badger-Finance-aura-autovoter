import os

import pytest

from aura_voter.web3 import EthNodeNotFound
from aura_voter.web3 import get_web3


def test_web3():
    os.environ['ETHNODEURL'] = "some.rpc"
    web3 = get_web3()
    assert not web3.isConnected()


def test_web3_no_env_var():
    os.environ.pop('ETHNODEURL')
    with pytest.raises(EthNodeNotFound):
        get_web3()
