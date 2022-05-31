from decimal import Decimal
from unittest.mock import MagicMock

import pytest
from web3 import Web3

from aura_voter.data_collectors.on_chain_collectors import get_balancer_pool_token_balance


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
    assert balance['some_pool_id123123'][Web3.toChecksumAddress(target_token)] == pytest.approx(
        Decimal(
            target_token_balance / 10 ** decimals
        )
    )


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
    assert balance == {}
