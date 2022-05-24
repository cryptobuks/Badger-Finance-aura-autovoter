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
