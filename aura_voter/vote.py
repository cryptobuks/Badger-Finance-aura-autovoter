from decimal import Decimal
from typing import Dict
from typing import List

from aura_voter.data_collectors.data_processors import extract_pools_with_target_token_included
from aura_voter.data_collectors.graph_collectors import get_all_balancer_pools
from aura_voter.data_collectors.on_chain_collectors import get_balancer_pool_token_balance
from aura_voter.voting_algorithms.poc_algorithm import POCVoter


def collect_and_vote(dry_run=True):
    amount_of_locked_target_token = 123  # TODO: Add this when bveAURA launches
    all_balancer_pools = get_all_balancer_pools()  # type: List[Dict]
    # TODO: target target token should be changed to bveAURA once we know the address
    target_token = "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"  # WETH just for testing
    # Extract only pools that have target token
    target_pools = extract_pools_with_target_token_included(
        token_addr=target_token,
        subgraph_pool_data=all_balancer_pools
    )
    target_pools_with_balances = []
    for pool in target_pools:
        target_pools_with_balances.append(
            get_balancer_pool_token_balance(target_token, pool['id'])
        )
    voter = POCVoter(Decimal(amount_of_locked_target_token), target_pools_with_balances)
    voter.propose_voting_choices()
