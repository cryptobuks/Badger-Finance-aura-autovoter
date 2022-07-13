from collections import defaultdict
from decimal import Decimal
from typing import Dict
from typing import List
from typing import Optional

from pycoingecko import CoinGeckoAPI
from web3 import Web3

from aura_voter.constants import CURRENCY_USD
from aura_voter.utils import get_abi
from aura_voter.web3 import get_web3

CG_CHAIN_ID = "ethereum"


def extract_pools_with_target_token_included(
        token_addr: str, subgraph_pool_data: List[Dict]
) -> List[Dict]:
    """
    Function that has input data from balancer subgraph and filters out pools with
    target token address
    """
    target_pools = []
    for pool in subgraph_pool_data:
        for token in pool['tokens']:
            if Web3.toChecksumAddress(token['address']) == Web3.toChecksumAddress(token_addr):
                target_pools.append(pool)
                break
    return target_pools


def filter_out_bribes_for_current_proposal(
        bribes: List[Dict], choices: Dict, current_proposal_index: int) -> Optional[
    Dict[str, List[Dict]]
]:
    """
    Processing raw bribes from theGraph and mapping them to the voting choices from Snapshot
    - param: amount_of_gauge_proposals represents latest Snapshot Gauge voting round that HH guys
    set manually for each bribe round
    """
    if not bribes:
        return
    bribes_filtered = defaultdict(list)
    for bribe in bribes:
        for choice_number, pool_name in choices.items():
            # Bribe proposal from subgraph is keccak hash from the voting choice number(BAL pool)
            # and snapshot ordinal number
            if Web3.solidityKeccak(
                    ['uint256', 'uint256'], [current_proposal_index, int(choice_number) - 1]
            ).hex() == bribe['proposal']:
                bribes_filtered[pool_name].append(
                    {'token': bribe['token'], 'amount': bribe['amount']}
                )
    return bribes_filtered


def get_bribes_tokens_prices(bribes_filtered: Dict[str, List[Dict]]) -> Optional[
    Dict[str, Decimal]
]:
    """
    Takes output data from filter_out_bribes_for_current_proposal function then
    - Gather all token addresses into one single list
    - Gets token prices in one query from coingecko
    """
    if not bribes_filtered:
        return
    gecko = CoinGeckoAPI()
    # First, gather all token addresses from bribes to fetch their prices in one single GC query
    token_addresses = set()
    for _, bribes in bribes_filtered.items():
        token_addresses.update([bribe['token'] for bribe in bribes])
    token_prices = gecko.get_token_price(
        id=CG_CHAIN_ID, contract_addresses=list(token_addresses), vs_currencies=CURRENCY_USD
    )  # type: Dict[str, Dict[str, float]]
    # Flatten return dict as we just need only USD price
    return {
        token_addr: Decimal(price_data['usd']) for token_addr, price_data in token_prices.items()
    }


def calculate_dollar_value_of_bribes_per_pool(
        bribes_filtered: Dict[str, List[Dict]], token_prices: Dict[str, Decimal],
) -> Optional[Dict[str, Dict]]:
    """
    Function that calculates total amount of bribes in $ per pool.
    For each pool it returns a dict that contains total amount of bribes in $ and tokens bribed
    """
    if not bribes_filtered or not token_prices:
        return
    web3 = get_web3()
    pool_bribe_totals = defaultdict(dict)
    for pool, bribes in bribes_filtered.items():
        for bribe in bribes:
            token_contract = web3.eth.contract(
                address=web3.toChecksumAddress(
                    web3.toChecksumAddress(bribe['token'])), abi=get_abi("ERC20")
            )
            token_amount = (
                Decimal(bribe['amount']) / 10 ** token_contract.functions.decimals().call()
            )
            bribe_value_in_usd = token_amount * token_prices[bribe['token']]
            if pool_bribe_totals[pool].get('totals'):
                pool_bribe_totals[pool]['totals'] += bribe_value_in_usd
            else:
                pool_bribe_totals[pool]['totals'] = bribe_value_in_usd
            token_symbol = token_contract.functions.symbol().call()
            if pool_bribe_totals[pool].get('tokens'):
                pool_bribe_totals[pool]['tokens'].add(token_symbol)
            else:
                pool_bribe_totals[pool]['tokens'] = {token_symbol}
    return pool_bribe_totals
