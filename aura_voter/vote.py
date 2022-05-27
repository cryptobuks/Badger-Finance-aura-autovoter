from decimal import Decimal
from typing import Dict
from typing import List

from aura_voter.constants import BADGER
from aura_voter.data_collectors.data_processors import extract_pools_with_target_token_included
from aura_voter.data_collectors.graph_collectors import get_all_balancer_pools
from aura_voter.data_collectors.on_chain_collectors import get_balancer_pool_token_balance
from aura_voter.voting_algorithms.poc_algorithm import POCVoter


def collect_and_vote(dry_run=True):
    locked_token = 123  # TODO: Add this when bveAURA launches
    all_balancer_pools = get_all_balancer_pools()  # type: List[Dict]
    # Extract only pools that have target token
    target_pools = extract_pools_with_target_token_included(
        token_addr=BADGER, subgraph_pool_data=all_balancer_pools
    )
    target_pools_with_balances = []
    for pool in target_pools:
        target_pools_with_balances.append(
            get_balancer_pool_token_balance(BADGER, pool['id'])
        )
    voter = POCVoter(Decimal(locked_token), target_pools_with_balances)
    voter.propose_voting_choices()
