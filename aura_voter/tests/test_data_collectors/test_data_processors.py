from decimal import Decimal
from unittest.mock import MagicMock

from aura_voter.data_collectors.data_processors import calculate_dollar_value_of_bribes_per_pool
from aura_voter.data_collectors.data_processors import extract_pools_with_target_token_included
from aura_voter.data_collectors.data_processors import filter_out_bribes_for_current_proposal
from aura_voter.data_collectors.data_processors import get_bribes_tokens_prices
from aura_voter.tests.test_data.balancer_graph_data import BALANCER_POOLS_DATA
from aura_voter.tests.test_data.bribes_graph_data import AURA_BRIBES_DATA

# Test choices for snapshot round 0x515649bddfb0e0d637745e8654616b03b371bb444f90f327064e7eee6052aff8
TEST_CHOICES = {'1': 'veBAL', '2': '50/50 AURA/WETH', '3': 'Stable auraBAL/B-80BAL-20WETH',
                '4': 'Stable DAI/USDC/USDT', '5': '50/50 SNX/WETH', '6': '60/40 WETH/DAI',
                '7': '50/50 YFI/WETH', '8': 'MetaStable rETH/WETH', '9': '80/20 D2D/USDC',
                '10': 'MetaStable wstETH/WETH', '11': '80/20 VITA/WETH', '12': '50/50 USDT/WETH',
                '13': '80/20 UNN/WETH', '14': '50/50 Silo/WETH', '15': '50/50 NOTE/WETH',
                '16': '80/20 GRO/WETH', '17': 'bb-a-USDT/bb-a-DAI/bb-a-USDC', '18': '50/50 D2D/BAL',
                '19': '70/30 WETH/FEI', '20': '50/50 USDC/WETH', '21': '80/20 TCR/DAI',
                '22': '50/50 MATIC/WETH', '23': '50/50 WBTC/WETH', '24': '50/50 VITA/WETH',
                '25': '80/20 LDO/WETH', '26': '80/20 MTA/WETH', '27': '50/50 LINK/WETH',
                '28': '50/50 REN/WETH', '29': '50/50 COMP/WETH', '30': '80/20 GNO/WETH',
                '31': '50/50 UMA/USDC', '32': 'Stable WBTC/renBTC/sBTC', '33': '80/20 HAUS/WETH',
                '34': '50/50 GNO/COW', '35': '50/50 COW/WETH', '36': '50/25/25 OHM/DAI/WETH',
                '37': '80/20 FDT/WETH', '38': '80/20 BADGER/WBTC', '39': '80/20 NOTE/WETH',
                '40': '80/20 WNCG/WETH', '41': '80/20 CREAM/WETH', '42': '80/20 PAL/USDC',
                '43': '50/50 DFX/WETH', '44': 'Stable B-80BAL-20WETH/sdBal',
                '45': 'Stable FIAT/DAI/USDC', '46': '33/33/33 auraBAL/graviAURA/WETH',
                '47': 'a-33/33/33 DPX/RDPX/WETH', '48': 'a-33/33/33 WBTC/WETH/USDC',
                '49': 'a-Stable VST/DAI/USDT/USDC', '50': 'a-80/20 MAGIC/WETH',
                '51': 'a-80/20 PICKLE/WETH', '52': 'a-80/20 LINK/WETH', '53': 'a-80/20 GMX/WETH',
                '54': 'a-Stable MAI/USDT/USDC', '55': 'a-50/50 VSTA/WETH', '56': 'a-80/20 TCR/WETH',
                '57': 'a-Stable DAI/USDT/USDC', '58': 'a-80/20 GNO/WETH', '59': 'a-60/40 MCB/WETH',
                '60': 'a-60/40 BAL/WETH', '61': 'a-80/20 CRE8R/WETH',
                '62': 'p-25/25/25/25 WMATIC/USDC/WETH/BAL', '63': 'p-33/33/33 WBTC/USDC/WETH',
                '64': 'p-50/50 BAL/TEL', '65': 'p-40/40/20 WMATIC/MTA/WETH',
                '66': 'p-33/33/33 AVAX/WETH/SOL', '67': 'p-Stable USDC/FRAX/USDT/UST',
                '68': 'p-Stable USDC/TUSD/DAI/USDT', '69': 'p-Stable USDC/DAI/miMATIC/USDT',
                '70': 'p-MetaStable WMATIC/stMATIC', '71': 'p-Stable WBTC/renBTC',
                '72': 'p-50/50 WBTC/WETH', '73': 'p-80/20 BANK/WETH', '74': 'p-80/20 SAND/WMATIC',
                '75': 'p-50/50 USDC/WETH', '76': 'p-20/20/20/20/20 USDC/LINK/WETH/BAL/AAVE',
                '77': 'p-80/20 VISION/WETH', '78': 'p-80/20 THX/USDC',
                '79': 'p-60/20/20 TEL/USDC/BAL', '80': 'p-25/25/25/25 LINK/WETH/BAL/AAVE',
                '81': 'p-MetaStable WMATIC/MaticX', '82': 'p-40/40/20 TEL/DFX/USDC'}

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
    bribes = filter_out_bribes_for_current_proposal(
        AURA_BRIBES_DATA['bribes'],
        TEST_CHOICES, current_proposal_index=TEST_PROPOSAL_HH_INDEX
    )
    assert dict(bribes) == EXPECTED_FILTERED_BRIBES


def test_filter_out_bribes_for_current_proposal_empty():
    """
    Test that incorrect voting round index returns no bribes
    """
    assert dict(filter_out_bribes_for_current_proposal(
        AURA_BRIBES_DATA['bribes'], TEST_CHOICES, current_proposal_index=135
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
    prices = get_bribes_tokens_prices(EXPECTED_FILTERED_BRIBES)
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
    prices = get_bribes_tokens_prices(EXPECTED_FILTERED_BRIBES)
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
    pool_bribes = calculate_dollar_value_of_bribes_per_pool(
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
    assert dict(pool_bribes) == {
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


def test_calculate_dollar_value_of_bribes_per_pool_no_bribes():
    assert not calculate_dollar_value_of_bribes_per_pool({}, {})
