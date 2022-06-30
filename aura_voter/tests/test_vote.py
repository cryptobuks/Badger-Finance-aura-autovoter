from unittest.mock import MagicMock

from web3 import Web3

from aura_voter.tests.test_data.balancer_graph_data import BALANCER_POOLS_DATA
from aura_voter.tests.test_data.test_data import PROPOSAL_TEST_DATA
from aura_voter.vote import collect_and_vote


def test_voter(mocker):
    """
    Dummy test to make sure everything works
    """
    discord = mocker.patch(
        "aura_voter.vote.send_message_to_discord"
    )
    mocker.patch(
        "aura_voter.vote.send_code_block_to_discord"
    )
    client = mocker.patch(
        'aura_voter.data_collectors.graph_collectors.make_gql_client',
        return_value=MagicMock(
            execute=MagicMock(
                return_value=BALANCER_POOLS_DATA,
            )
        )
    )
    mocker.patch(
        'aura_voter.vote.get_gauge_weight_snapshot',
        return_value=PROPOSAL_TEST_DATA['proposals'][0]
    )
    cast_vote = mocker.patch('aura_voter.vote.cast_weighed_vote')
    target_token = "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"  # WETH for testing
    target_token_balance = 735228173522811111
    decimals = 18
    mocker.patch(
        "aura_voter.data_collectors.on_chain_collectors.get_web3",
        return_value=MagicMock(
            eth=MagicMock(
                contract=MagicMock(
                    return_value=MagicMock(
                        functions=MagicMock(
                            getVotes=MagicMock(return_value=MagicMock(
                                call=MagicMock(return_value=24004620088791137751441867)
                            )),
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
                            )),
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
    collect_and_vote(dry_run=False)
    client.return_value.execute.assert_called_once()
    assert discord.called
    assert cast_vote.called
