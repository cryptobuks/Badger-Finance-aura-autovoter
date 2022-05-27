from dataclasses import dataclass
from decimal import Decimal
from typing import Dict
from typing import List


@dataclass
class AlgorithmSettings:
    badger_pools_fixed_vote_weight: Decimal


class POCVoter:
    ALGORITHM_SETTINGS = AlgorithmSettings(
        badger_pools_fixed_vote_weight=Decimal(90)  # In %
    )

    def __init__(
            self, total_locked_aura: Decimal, badger_pools_with_balances: List[Dict[str, Decimal]]
    ):
        self.badger_pools_with_balances = badger_pools_with_balances
        self.locked_aura = total_locked_aura

    def propose_voting_choices(self) -> Dict[str, Decimal]:
        """
        TBA later
        """
        pass
