from dataclasses import dataclass
from decimal import Decimal


@dataclass
class PoolBalance:
    target_token: str
    pool_id: str
    balance: Decimal
