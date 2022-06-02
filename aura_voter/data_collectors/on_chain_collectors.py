from decimal import Decimal
from typing import Optional

from eth_utils import is_address

from aura_voter.constants import BALANCER_LIQUIDITY_GAUGE_FACTORY
from aura_voter.constants import BALANCER_VAULT_ADDRESS
from aura_voter.constants import DEFAULT_ADDRESS
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
    """
    Helper func to determine if balancer pool has gauge and we can vote for it
    """
    web3 = get_web3()
    if is_address(balancer_pool_id):
        raise ValueError("balancer_pool_id should not be an address")
    balancer_vault = web3.eth.contract(
        address=web3.toChecksumAddress(BALANCER_VAULT_ADDRESS),
        abi=get_abi("BalancerVault")
    )
    balancer_pool_address, _ = balancer_vault.functions.getPool(balancer_pool_id).call()
    liquidity_gauge_factory = web3.eth.contract(
        address=web3.toChecksumAddress(BALANCER_LIQUIDITY_GAUGE_FACTORY),
        abi=get_abi("LiquidityGaugeFactory")
    )
    pool_gauge = liquidity_gauge_factory.functions.getPoolGauge(balancer_pool_address).call()
    if web3.toChecksumAddress(pool_gauge) == web3.toChecksumAddress(DEFAULT_ADDRESS):
        return False
    else:
        return True
