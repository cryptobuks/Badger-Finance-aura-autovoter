from collections import defaultdict
from typing import Dict
from typing import List

from web3 import Web3


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
        bribes: List[Dict], choices: Dict, amount_of_gauge_proposals: int) -> Dict[str, List[Dict]]:
    """
    Processing raw bribes from theGraph and mapping them to the voting choices from Snapshot
    - param: amount_of_gauge_proposals represents latest Snapshot Gauge voting round that HH guys
    set manually for each bribe round
    """
    bribes_filtered = defaultdict(list)
    for bribe in bribes:
        for choice_number, pool_name in choices.items():
            # Bribe proposal from subgraph is keccak hash from the voting choice number(BAL pool)
            # and snapshot ordinal number
            if Web3.solidityKeccak(
                ['uint256', 'uint256'], [amount_of_gauge_proposals, int(choice_number) - 1]
            ).hex() == bribe['proposal']:
                bribes_filtered[pool_name].append(
                    {'token': bribe['token'], 'amount': bribe['amount']}
                )
    return bribes_filtered
