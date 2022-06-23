from decimal import Decimal
from typing import Dict
from typing import List

from rich.console import Console

from aura_voter.constants import BOT_USERNAME
from aura_voter.constants import GRAVIAURA
from aura_voter.data_collectors.data_processors import extract_pools_with_target_token_included
from aura_voter.data_collectors.graph_collectors import get_all_balancer_pools
from aura_voter.data_collectors.on_chain_collectors import does_pool_have_gauge
from aura_voter.data_collectors.on_chain_collectors import get_balancer_pool_token_balance
from aura_voter.data_collectors.on_chain_collectors import get_locked_graviaura_amount
from aura_voter.data_collectors.snapshot_collectors import get_gauge_weight_snapshot
from aura_voter.discord import send_message_to_discord
from aura_voter.voting_algorithms.poc_algorithm import POCVoter

console = Console(width=100000, height=10000)


def collect_and_vote(dry_run=True):
    # TODO: Add this when bveAURA launches
    amount_of_locked_aura = get_locked_graviaura_amount()
    send_message_to_discord(
        "🗳️🗳️🗳️🗳️ New voting round AURA 🗳️🗳️🗳️🗳️",
        username=BOT_USERNAME
    )
    send_message_to_discord(
        f"> Locked AURA amount is: {round(amount_of_locked_aura, 2)}",
        username=BOT_USERNAME
    )
    snapshot = get_gauge_weight_snapshot()
    if snapshot:
        send_message_to_discord(
            f"> Fetched gauge proposal snapshot: {snapshot['id']}",
            username=BOT_USERNAME,
        )
    else:
        send_message_to_discord("> No active proposal found", username=BOT_USERNAME)
        return
    all_balancer_pools = get_all_balancer_pools()  # type: List[Dict]
    # TODO: target target token should be changed to bveAURA once we know the address
    target_token = GRAVIAURA
    # Extract only pools that have target token
    target_pools = extract_pools_with_target_token_included(
        token_addr=target_token,
        subgraph_pool_data=all_balancer_pools
    )
    # Filter out pools without gauges
    pools_with_gauges = [pool for pool in target_pools if does_pool_have_gauge(pool['id'])]
    target_pools_with_balances = []
    for pool in pools_with_gauges:
        target_pools_with_balances.append(
            get_balancer_pool_token_balance(target_token, pool['id'])
        )
    # TODO: Before passing pools to algorithm we have to map it to the pool names on Snapsot
    voter = POCVoter(
        Decimal(amount_of_locked_aura), target_pools_with_balances,
    )
    votes = voter.propose_voting_choices()
    console.print(votes)
