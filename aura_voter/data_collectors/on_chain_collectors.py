from decimal import Decimal
from typing import Optional

from aura_voter.constants import BALANCER_VAULT_ADDRESS
from aura_voter.data_collectors import PoolBalance
from aura_voter.utils import get_abi
from aura_voter.web3 import get_web3


def get_balancer_pool_token_balance(
        target_token: str, balancer_pool_id: str) -> Optional[PoolBalance]:
    """
    Returns token balance for a given balancer pool
    """
    web3 = get_web3()
    balancer_vault = web3.eth.contract(
        address=web3.toChecksumAddress(BALANCER_VAULT_ADDRESS),
        abi=get_abi("BalancerVault")
    )
    token_contract = web3.eth.contract(
        address=web3.toChecksumAddress(target_token), abi=get_abi("ERC20")
    )
    tokens, balances, _ = balancer_vault.functions.getPoolTokens(balancer_pool_id).call()
    pool_token_balance = None
    for index, token in enumerate(tokens):
        if web3.toChecksumAddress(token) == web3.toChecksumAddress(target_token):
            pool_token_balance = PoolBalance(
                target_token=target_token,
                pool_id=balancer_pool_id,
                balance=Decimal(balances[index]) / Decimal(
                    10 ** token_contract.functions.decimals().call()
                )
            )
            break
    return pool_token_balance


def does_pool_have_gauge(balancer_pool_id: str) -> bool:
    pass
