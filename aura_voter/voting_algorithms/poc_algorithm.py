from dataclasses import dataclass
from decimal import Decimal
from typing import Dict


@dataclass
class AlgorithmSettings:
    badger_pools_fixed_vote_weight: Decimal


class POCVoter:
    ALGORITHM_SETTINGS = AlgorithmSettings(
        badger_pools_fixed_vote_weight=Decimal(90)  # In %
    )

    def __init__(self, badger_pools: Dict[str, Decimal]):
        self.badger_pools = badger_pools

    def propose_voting_choices(self) -> Dict[str, Decimal]:
        """
        TBA later
        """
        pass
