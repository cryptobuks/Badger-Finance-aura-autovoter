from decimal import Decimal
from enum import Enum
from typing import Dict

from aura_voter.constants import BALANCER_VAULT_ADDRESS_ETH
from aura_voter.utils import get_abi
from aura_voter.web3 import get_web3


class PoolType(Enum):
    """
    Enum of all known Balancer pool types
    """
    Element = "Element"
    Weighted = "Weighted"
    Investment = "Investment"
    Stable = "Stable"
    MetaStable = "MetaStable"
    StablePhantom = "StablePhantom"
    ERC4626Linear = "ERC4626Linear"
    LiquidityBootstrapping = "LiquidityBootstrapping"
    AaveLinear = "AaveLinear"


def get_balancer_pool_token_balance(target_token: str, balancer_pool_id: str) -> Dict[str, Dict]:
    """
    Returns token balance for a given balancer pool
    """
    web3 = get_web3()
    balancer_vault = web3.eth.contract(
        address=web3.toChecksumAddress(BALANCER_VAULT_ADDRESS_ETH),
        abi=get_abi("BalancerVault")
    )
    token_contract = web3.eth.contract(
        address=web3.toChecksumAddress(target_token), abi=get_abi("ERC20")
    )
    pool_token_balance = {}
    tokens, balances, _ = balancer_vault.functions.getPoolTokens(balancer_pool_id).call()
    for index, token in enumerate(tokens):
        if web3.toChecksumAddress(token) == web3.toChecksumAddress(target_token):
            pool_token_balance[balancer_pool_id] = {
                token: Decimal(balances[index]) / Decimal(
                    10 ** token_contract.functions.decimals().call()
                )
            }
    return pool_token_balance
