from dataclasses import dataclass
from decimal import Decimal
from typing import Dict
from typing import List

from aura_voter.data_collectors import PoolBalance


@dataclass
class AlgorithmSettings:
    badger_pools_fixed_vote_weight: Decimal


class POCVoter:
    """
    Algorithmic voting for bveAURA on Snapshot
    """
    ALGORITHM_SETTINGS = AlgorithmSettings(
        badger_pools_fixed_vote_weight=Decimal(90)  # In %
    )

    def __init__(
            self, total_locked_aura: Decimal,
            badger_pools_with_balances: List[PoolBalance],
            target_token_address: str,
    ):
        self.badger_pools_with_balances = badger_pools_with_balances
        self.locked_aura = total_locked_aura
        self.target_token_address = target_token_address

    def propose_voting_choices(self) -> Dict[str, Decimal]:
        """
        Distributing votes across badger pools for bveAURA
        """
        # finalized_votes = {}
        # for pool in self.badger_pools_with_balances:
        #     # TODO: Map pool name/id to snapshot pool value
        #     pool_name = list(pool.keys())[0]
        #     pool_balance = list(pool.values())[0][self.target_token_address]
        #     finalized_votes[pool] = (
        #         self.ALGORITHM_SETTINGS.badger_pools_fixed_vote_weight * pool_balance
        #     )
        # return finalized_votes
