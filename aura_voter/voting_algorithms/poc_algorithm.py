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
        badger_pools_fixed_vote_weight=Decimal(0.9)  # In %
    )

    def __init__(
            self, total_badger_locked_aura: Decimal,
            badger_pools_with_balances: List[PoolBalance],
    ):
        self.badger_pools_with_balances = badger_pools_with_balances
        self.badger_locked_aura = total_badger_locked_aura

    def propose_voting_choices(self) -> Dict[str, Decimal]:
        """
        Distributing votes across badger pools for bveAURA
        """
        finalized_votes = {}
        for pool in self.badger_pools_with_balances:
            # TODO: Map pool name/id to snapshot pool value
            pool_name = pool.pool_id
            pool_balance = pool.balance
            # For each pool we should vote badger_pools_fixed_vote_weight of bveAURA locked in that
            # pool
            finalized_votes[pool_name] = ((
                self.ALGORITHM_SETTINGS.badger_pools_fixed_vote_weight * pool_balance
            ) / self.badger_locked_aura) * Decimal(100)
        # The rest is voting for badger/wbtc
        # TODO: Here will be bribes voting later on
        finalized_votes['badger_wbtc'] = Decimal(100) - sum(finalized_votes.values())
        return finalized_votes
