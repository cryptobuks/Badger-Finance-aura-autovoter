from unittest.mock import MagicMock

from web3 import Web3

from aura_voter.tests.test_data.balancer_graph_data import BALANCER_POOLS_DATA
from aura_voter.vote import collect_and_vote


def test_voter(mocker):
    """
    Dummy test to make sure everything works
    """
    client = mocker.patch(
        'aura_voter.data_collectors.graph_collectors.make_gql_client',
        return_value=MagicMock(
            execute=MagicMock(
                return_value=BALANCER_POOLS_DATA,
            )
        )
    )
    target_token = "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"  # WETH for testing
    target_token_balance = 73522817352281
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
                                        target_token,
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
    collect_and_vote()
    client.return_value.execute.assert_called_once()
