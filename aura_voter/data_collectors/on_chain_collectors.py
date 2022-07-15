from decimal import Decimal
from typing import Optional

from eth_utils import is_address

from aura_voter.constants import AURA_LOCKER_ADDRESS
from aura_voter.constants import BADGER_VOTER_ADDRESS
from aura_voter.constants import BALANCER_LIQUIDITY_GAUGE_FACTORY
from aura_voter.constants import BALANCER_VAULT_ADDRESS
from aura_voter.constants import GRAVIAURA
from aura_voter.constants import TREASURY_WALLETS
from aura_voter.constants import ZERO_ADDRESS
from aura_voter.data_collectors import PoolBalance
from aura_voter.utils import get_abi
from aura_voter.web3 import get_web3


def get_locked_graviaura_amount() -> Decimal:
    web3 = get_web3()
    abi = get_abi("AuraLocker")
    contract = web3.eth.contract(address=web3.toChecksumAddress(AURA_LOCKER_ADDRESS), abi=abi)
    vl_aura_amount = contract.functions.getVotes(
        web3.toChecksumAddress(BADGER_VOTER_ADDRESS)).call()

    return Decimal(vl_aura_amount) / Decimal(
        10 ** contract.functions.decimals().call()
    )


def get_treasury_controlled_naked_graviaura() -> Decimal:
    """
    Iterate through every treasury wallet and accumulate graviAURA balances into one value.
    Note: this graviAURA is naked, meaning it's not deposited in any pool
    """
    web3 = get_web3()
    abi = get_abi("ERC20")
    contract = web3.eth.contract(address=web3.toChecksumAddress(GRAVIAURA), abi=abi)
    treasury_graviaura_controlled_amount = 0.0
    for wallet in TREASURY_WALLETS:
        treasury_graviaura_controlled_amount += contract.functions.balanceOf(
            web3.toChecksumAddress(wallet)
        ).call()
    return Decimal(treasury_graviaura_controlled_amount) / Decimal(
        10 ** contract.functions.decimals().call()
    )


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
    pool_gauge_address = web3.toChecksumAddress(
        liquidity_gauge_factory.functions.getPoolGauge(balancer_pool_address).call()
    )
    if pool_gauge_address == web3.toChecksumAddress(ZERO_ADDRESS):
        return False
    gauge_contract = web3.eth.contract(
        address=web3.toChecksumAddress(pool_gauge_address),
        abi=get_abi("BalancerGauge")
    )
    is_gauge_killed = gauge_contract.functions.is_killed().call()
    working_supply = gauge_contract.functions.working_supply().call()
    # This condition means that pool gauge was killed or has no liquidity so we can't vote for it
    if is_gauge_killed is True or working_supply == 0:
        return False
    else:
        return True
