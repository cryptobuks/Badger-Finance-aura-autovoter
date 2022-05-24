from aura_voter.data_collectors.data_processors import extract_pools_with_target_token_included
from aura_voter.tests.test_data.balancer_graph_data import BALANCER_POOLS_DATA


def test_extract_pools_with_target_token_included():
    """
    Test against test data that it returns 4 pools that include WETH token
    """
    res = extract_pools_with_target_token_included(
        '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2',  # WETH
        BALANCER_POOLS_DATA['pools'],
    )
    assert len(res) == 4


def test_extract_pools_with_target_token_included_another():
    """
    Test against test data that it returns 4 pools that include WBTC token
    """
    res = extract_pools_with_target_token_included(
        '0x2260fac5e5542a773aa44fbcfedf7c193bc2c599',  # WBTC
        BALANCER_POOLS_DATA['pools'],
    )
    assert len(res) == 1


def test_extract_pools_with_target_token_included_not_found():
    """
    Test against test data that it returns 4 pools that include Badger token
    Test data doesn't have pools with badger tokens
    """
    res = extract_pools_with_target_token_included(
        '0x3472A5A71965499acd81997a54BBA8D852C6E53d',  # BADGER
        BALANCER_POOLS_DATA['pools'],
    )
    assert len(res) == 0
