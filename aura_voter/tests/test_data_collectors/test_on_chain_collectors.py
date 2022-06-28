from decimal import Decimal
from unittest.mock import MagicMock

import pytest
from web3 import Web3

from aura_voter.constants import ZERO_ADDRESS
from aura_voter.data_collectors.on_chain_collectors import does_pool_have_gauge
from aura_voter.data_collectors.on_chain_collectors import get_balancer_pool_token_balance
from aura_voter.data_collectors.on_chain_collectors import get_locked_graviaura_amount


def test_get_locked_aura_amount(mocker):
    balance = 10000000000000000000
    decimals = 18
    mocker.patch(
        "aura_voter.data_collectors.on_chain_collectors.get_web3",
        return_value=MagicMock(eth=MagicMock(
            contract=MagicMock(
                return_value=MagicMock(
                    functions=MagicMock(
                        getVotes=MagicMock(return_value=MagicMock(
                            call=MagicMock(return_value=balance)
                        )),
                        decimals=MagicMock(return_value=MagicMock(
                            call=MagicMock(return_value=decimals)
                        )),
                    )
                )
            )
        ))
    )
    bve_cvx_locked = get_locked_graviaura_amount()
    assert bve_cvx_locked == balance / 10 ** decimals


def test_get_balancer_pool_token_balance(mocker):
    target_token = "0x2260fac5e5542a773aa44fbcfedf7c193bc2c599"
    target_token_balance = 7352281
    decimals = 18
    mocker.patch(
        "aura_voter.data_collectors.on_chain_collectors.get_web3",
        return_value=MagicMock(
            eth=MagicMock(
                contract=MagicMock(
                    return_value=MagicMock(
                        functions=MagicMock(
                            decimals=MagicMock(return_value=MagicMock(
                                call=MagicMock(return_value=decimals)
                            )),
                            getPoolTokens=MagicMock(return_value=MagicMock(
                                call=MagicMock(return_value=(
                                    [
                                        '0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599',
                                        '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2'
                                    ],
                                    [target_token_balance, 1209179159767278994],
                                    100000
                                ),
                                )
                            ))
                        )
                    )
                )
            ),
            toChecksumAddress=Web3.toChecksumAddress)
    )
    balance = get_balancer_pool_token_balance(
        target_token=target_token,
        balancer_pool_id="some_pool_id123123",
    )
    assert balance.balance == pytest.approx(
        Decimal(
            target_token_balance / 10 ** decimals
        )
    )
    assert balance.target_token == target_token
    assert balance.pool_id == 'some_pool_id123123'


def test_get_balancer_pool_token_balance_no_token_balance(mocker):
    target_token_balance = 7352281
    decimals = 18
    mocker.patch(
        "aura_voter.data_collectors.on_chain_collectors.get_web3",
        return_value=MagicMock(
            eth=MagicMock(
                contract=MagicMock(
                    return_value=MagicMock(
                        functions=MagicMock(
                            decimals=MagicMock(return_value=MagicMock(
                                call=MagicMock(return_value=decimals)
                            )),
                            getPoolTokens=MagicMock(return_value=MagicMock(
                                call=MagicMock(return_value=(
                                    [
                                        '0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599',
                                        '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2'
                                    ],
                                    [target_token_balance, 1209179159767278994],
                                    100000
                                ),
                                )
                            ))
                        )
                    )
                )
            ),
            toChecksumAddress=Web3.toChecksumAddress)
    )
    balance = get_balancer_pool_token_balance(
        # Pass the token that is not in the pool
        target_token="0xfd05D3C7fe2924020620A8bE4961bBaA747e6305",
        balancer_pool_id="some_pool_id123123",
    )
    assert balance is None


def test_does_pool_have_gauge_happy(mocker):
    """
    Happy path when balancer pool has gauge so we can vote for it
    """
    mocker.patch(
        "aura_voter.data_collectors.on_chain_collectors.get_web3",
        return_value=MagicMock(
            eth=MagicMock(
                contract=MagicMock(
                    return_value=MagicMock(
                        functions=MagicMock(
                            getPool=MagicMock(return_value=MagicMock(
                                call=MagicMock(return_value=(
                                    "0x0BF37157d30dFe6f56757DCadff01AEd83b08cD6",
                                    2,
                                ))
                            )),
                            getPoolGauge=MagicMock(return_value=MagicMock(
                                call=MagicMock(
                                    return_value="0xb460DAa847c45f1C4a41cb05BFB3b51c92e41B36"
                                )
                            )),
                            is_killed=MagicMock(return_value=MagicMock(
                                call=MagicMock(
                                    return_value=False
                                )
                            )),
                            working_supply=MagicMock(return_value=MagicMock(
                                call=MagicMock(
                                    return_value=123123
                                )
                            )),
                        )
                    )
                )
            ),
            toChecksumAddress=Web3.toChecksumAddress)
    )
    assert does_pool_have_gauge(
        "0xb460daa847c45f1c4a41cb05bfb3b51c92e41b36000200000000000000000194"
    ) is True


def test_does_pool_have_gauge_no_gauge(mocker):
    """
    Checking that pool has no gauge
    """
    mocker.patch(
        "aura_voter.data_collectors.on_chain_collectors.get_web3",
        return_value=MagicMock(
            eth=MagicMock(
                contract=MagicMock(
                    return_value=MagicMock(
                        functions=MagicMock(
                            getPool=MagicMock(return_value=MagicMock(
                                call=MagicMock(return_value=(
                                    "0x0BF37157d30dFe6f56757DCadff01AEd83b08cD6",
                                    2,
                                ))
                            )),
                            getPoolGauge=MagicMock(return_value=MagicMock(
                                call=MagicMock(
                                    return_value=ZERO_ADDRESS
                                )
                            ))
                        )
                    )
                )
            ),
            toChecksumAddress=Web3.toChecksumAddress)
    )
    assert does_pool_have_gauge(
        "0xb460daa847c45f1c4a41cb05bfb3b51c92e41b36000200000000000000000149"
    ) is False


def test_does_pool_have_gauge_no_gauge__zero_supply(mocker):
    """
    Checking that pool has no gauge
    """
    mocker.patch(
        "aura_voter.data_collectors.on_chain_collectors.get_web3",
        return_value=MagicMock(
            eth=MagicMock(
                contract=MagicMock(
                    return_value=MagicMock(
                        functions=MagicMock(
                            getPool=MagicMock(return_value=MagicMock(
                                call=MagicMock(return_value=(
                                    "0x0BF37157d30dFe6f56757DCadff01AEd83b08cD6",
                                    2,
                                ))
                            )),
                            getPoolGauge=MagicMock(return_value=MagicMock(
                                call=MagicMock(
                                    return_value="0xb460DAa847c45f1C4a41cb05BFB3b51c92e41B36"
                                )
                            )),
                            is_killed=MagicMock(return_value=MagicMock(
                                call=MagicMock(
                                    return_value=True
                                )
                            )),
                            working_supply=MagicMock(return_value=MagicMock(
                                call=MagicMock(
                                    return_value=0
                                )
                            )),
                        )
                    )
                )
            ),
            toChecksumAddress=Web3.toChecksumAddress)
    )
    assert does_pool_have_gauge(
        "0xb460daa847c45f1c4a41cb05bfb3b51c92e41b36000200000000000000000149"
    ) is False


def test_does_pool_have_gauge_invalid_pool_id(mocker):
    """
    Test case when BAL pool id is mistaken for address
    In this case exception will be raised
    """
    mocker.patch(
        "aura_voter.data_collectors.on_chain_collectors.get_web3",
    )
    with pytest.raises(ValueError) as exc:
        does_pool_have_gauge("0x0BF37157d30dFe6f56757DCadff01AEd83b08cD6")
    assert str(exc.value) == "balancer_pool_id should not be an address"
