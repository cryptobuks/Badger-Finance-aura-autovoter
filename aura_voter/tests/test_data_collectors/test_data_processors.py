from decimal import Decimal
from unittest.mock import MagicMock

from aura_voter.data_collectors.data_processors import _calculate_dollar_value_of_bribes_per_pool  # noqa
from aura_voter.data_collectors.data_processors import _calculate_dollar_vlaura_values  # noqa
from aura_voter.data_collectors.data_processors import _filter_out_bribes_for_current_proposal  # noqa
from aura_voter.data_collectors.data_processors import _get_bribes_tokens_prices  # noqa
from aura_voter.data_collectors.data_processors import extract_pools_with_target_token_included
from aura_voter.tests.test_data.balancer_graph_data import BALANCER_POOLS_DATA
from aura_voter.tests.test_data.bribes_graph_data import AURA_BRIBES_DATA
from aura_voter.tests.test_data.test_data import ACTIVE_PROPOSAL_DATA


EXPECTED_FILTERED_BRIBES = {
    'p-25/25/25/25 WMATIC/USDC/WETH/BAL': [
        {'token': '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48', 'amount': '1672000000'}],
    '50/50 AURA/WETH': [
        {'token': '0x4e3fbd56cd56c3e72c1403e103b45db9da5b9d2b',
         'amount': '10000000000000000000'},
        {'token': '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48',
         'amount': '1000000'},
        {'token': '0xc0c293ce456ff0ed870add98a0828dd4d2903dbf',
         'amount': '100000000000000000000'},
        {'token': '0xc0c293ce456ff0ed870add98a0828dd4d2903dbf',
         'amount': '1000000000000000000'},
        {'token': '0xc0c293ce456ff0ed870add98a0828dd4d2903dbf',
         'amount': '3000000000000000000000'},
        {'token': '0xc0c293ce456ff0ed870add98a0828dd4d2903dbf',
         'amount': '10000000000000000000'},
        {'token': '0xc0c293ce456ff0ed870add98a0828dd4d2903dbf',
         'amount': '284000000000000000000'},
        {'token': '0xc0c293ce456ff0ed870add98a0828dd4d2903dbf',
         'amount': '5000000000000000000000'}],
    'p-MetaStable WMATIC/stMATIC': [
        {'token': '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48',
         'amount': '2227000000'}],
    'p-MetaStable WMATIC/MaticX': [
        {'token': '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48', 'amount': '50000000'},
        {'token': '0x30d20208d987713f46dfd34ef128bb16c404d10f',
         'amount': '11200000000000000000000'},
        {'token': '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48', 'amount': '3540000000'},
        {'token': '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48', 'amount': '9950000000'}],
    'MetaStable wstETH/WETH': [
        {'token': '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48',
         'amount': '10860000000'}],
    'Stable FIAT/DAI/USDC': [
        {'token': '0xed1480d12be41d92f36f5f7bdd88212e381a3677',
         'amount': '100000000000000000000000'}],
    'p-33/33/33 WBTC/USDC/WETH': [
        {'token': '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48', 'amount': '717000000'}],
    '80/20 FDT/WETH': [
        {'token': '0xed1480d12be41d92f36f5f7bdd88212e381a3677',
         'amount': '100000000000000000000000'}],
    '50/50 DFX/WETH': [
        {'token': '0x888888435fde8e7d4c54cab67f206e4199454c60',
         'amount': '10720000000000000000000'}],
    'a-33/33/33 WBTC/WETH/USDC': [
        {'token': '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48', 'amount': '3505000000'}],
    'MetaStable rETH/WETH': [
        {'token': '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48',
         'amount': '1341000000'}]}

EXPECTED_POOL_TOTALS_IN_DOLLAR = {
    'p-25/25/25/25 WMATIC/USDC/WETH/BAL': {'totals': Decimal('1673.65528'), 'tokens': {'TEST'}},
    '50/50 AURA/WETH': {'totals': Decimal('20119450000000001.00099'), 'tokens': {'TEST'}},
    'p-MetaStable WMATIC/stMATIC': {'totals': Decimal('2229.20473'), 'tokens': {'TEST'}},
    'p-MetaStable WMATIC/MaticX': {'totals': Decimal('4822944000013553.40460'),
                                   'tokens': {'TEST'}},
    'MetaStable wstETH/WETH': {'totals': Decimal('10870.75140'), 'tokens': {'TEST'}},
    'Stable FIAT/DAI/USDC': {'totals': Decimal('1368000000000000.00000'), 'tokens': {'TEST'}},
    'p-33/33/33 WBTC/USDC/WETH': {'totals': Decimal('717.70983'), 'tokens': {'TEST'}},
    '80/20 FDT/WETH': {'totals': Decimal('1368000000000000.00000'), 'tokens': {'TEST'}},
    '50/50 DFX/WETH': {'totals': Decimal('5351745600000000.00000'), 'tokens': {'TEST'}},
    'a-33/33/33 WBTC/WETH/USDC': {'totals': Decimal('3508.46995'), 'tokens': {'TEST'}},
    'MetaStable rETH/WETH': {'totals': Decimal('1342.32759'), 'tokens': {'TEST'}}}

STALE_TOKEN_PRICES = {'0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48': {'usd': 1.001},
                      '0x4e3fbd56cd56c3e72c1403e103b45db9da5b9d2b': {'usd': 5.54},
                      '0xc0c293ce456ff0ed870add98a0828dd4d2903dbf': {'usd': 2.39},
                      '0x888888435fde8e7d4c54cab67f206e4199454c60': {'usd': 0.499231},
                      '0x30d20208d987713f46dfd34ef128bb16c404d10f': {'usd': 0.430622},
                      '0xed1480d12be41d92f36f5f7bdd88212e381a3677': {'usd': 0.01368017}}

TEST_PROPOSAL_HH_INDEX = 3


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


def test_filter_out_bribes_for_current_proposal_happy():
    """
    Test against stale dataset for 3rd round of bribes
    """
    bribes = _filter_out_bribes_for_current_proposal(
        AURA_BRIBES_DATA['bribes'],
        ACTIVE_PROPOSAL_DATA['proposals'][0]['choices'],
        current_proposal_index=TEST_PROPOSAL_HH_INDEX
    )
    assert dict(bribes) == EXPECTED_FILTERED_BRIBES


def test_filter_out_bribes_for_current_proposal_empty():
    """
    Test that incorrect voting round index returns no bribes
    """
    assert dict(_filter_out_bribes_for_current_proposal(
        AURA_BRIBES_DATA['bribes'],
        ACTIVE_PROPOSAL_DATA['proposals'][0]['choices'], current_proposal_index=135
    )) == {}


def test_get_bribes_tokens_prices(mocker):
    """
    Checking that prices for all bribe tokens are returned
    """
    mocker.patch(
        "aura_voter.data_collectors.data_processors.CoinGeckoAPI",
        return_value=MagicMock(get_token_price=MagicMock(
            # Returning some fixed prices as of 13 July 2022
            return_value=STALE_TOKEN_PRICES)
        )
    )
    prices = _get_bribes_tokens_prices(EXPECTED_FILTERED_BRIBES)
    for _, bribes in EXPECTED_FILTERED_BRIBES.items():
        for bribe in bribes:
            # Make sure that each token is priced
            assert bribe['token'] in prices


def test_get_bribes_tokens_prices_empty(mocker):
    """
    Case when some weird token is bribed without price on CG
    """
    mocker.patch(
        "aura_voter.data_collectors.data_processors.CoinGeckoAPI",
        return_value=MagicMock(get_token_price=MagicMock(
            return_value={}
        ))
    )
    prices = _get_bribes_tokens_prices(EXPECTED_FILTERED_BRIBES)
    assert prices == {}


def test_calculate_dollar_value_of_bribes_per_pool(mocker):
    """
    Checking cumulative amount of bribes in $ per pool
    """
    mocker.patch(
        "aura_voter.data_collectors.data_processors.get_web3",
        return_value=MagicMock(eth=MagicMock(
            contract=MagicMock(
                return_value=MagicMock(
                    functions=MagicMock(
                        decimals=MagicMock(return_value=MagicMock(
                            call=MagicMock(return_value=6)
                        )),
                        symbol=MagicMock(return_value=MagicMock(
                            call=MagicMock(return_value="TEST")
                        )),
                    )
                )
            )
        ))
    )
    pool_bribes = _calculate_dollar_value_of_bribes_per_pool(
        bribes_filtered=EXPECTED_FILTERED_BRIBES,
        token_prices={
            '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48': Decimal('1.00099'),
            '0x4e3fbd56cd56c3e72c1403e103b45db9da5b9d2b': Decimal('5.54000'),
            '0xc0c293ce456ff0ed870add98a0828dd4d2903dbf': Decimal('2.39000'),
            '0x888888435fde8e7d4c54cab67f206e4199454c60': Decimal('0.49923'),
            '0x30d20208d987713f46dfd34ef128bb16c404d10f': Decimal('0.43062'),
            '0xed1480d12be41d92f36f5f7bdd88212e381a3677': Decimal('0.01368')
        },
    )
    assert dict(pool_bribes) == EXPECTED_POOL_TOTALS_IN_DOLLAR


def test_calculate_dollar_value_of_bribes_per_pool_no_bribes():
    assert not _calculate_dollar_value_of_bribes_per_pool({}, {})


def test_calculate_dollar_vlaura_values():
    final_pool_info = _calculate_dollar_vlaura_values(
        total_bribes_per_pool=EXPECTED_POOL_TOTALS_IN_DOLLAR,
        choices=ACTIVE_PROPOSAL_DATA['proposals'][0]['choices'],
        scores=ACTIVE_PROPOSAL_DATA['proposals'][0]['scores']
    )
    # Cherrypick one of the pools to check if data is correct
    assert final_pool_info['p-33/33/33 WBTC/USDC/WETH'] == {
        'tokens': {'TEST'},
        'totals_in_$': Decimal('717.70983'),
        '$/vlAURA': Decimal('0.05301878113117229370856000411')
    }


def test_calculate_dollar_vlaura_values_empty():
    assert not _calculate_dollar_vlaura_values(
        total_bribes_per_pool=EXPECTED_POOL_TOTALS_IN_DOLLAR,
        choices=ACTIVE_PROPOSAL_DATA['proposals'][0]['choices'],
        scores=[]
    )
