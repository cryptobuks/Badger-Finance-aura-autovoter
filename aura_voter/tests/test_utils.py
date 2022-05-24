import pytest

from aura_voter.utils import get_abi


def test_get_abi():
    abi = get_abi("ERC20")
    assert abi[0]['outputs'] is not None


def test_get_abi_raises():
    with pytest.raises(FileNotFoundError):
        get_abi("unknown_abi")
