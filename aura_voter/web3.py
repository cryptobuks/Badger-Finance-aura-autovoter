import os

from web3 import Web3

from aura_voter.aws import get_secret
from aura_voter.constants import ETHNODEURL_SECRET_ID
from aura_voter.constants import ETHNODEURL_SECRET_KEY


class EthNodeNotFound(Exception):
    pass


def get_web3() -> Web3:
    """
    Returns Web3 instance connected to RPC node
    """
    ethnode = os.getenv('ETHNODEURL') or get_secret(
        secret_id=ETHNODEURL_SECRET_ID,
        secret_key=ETHNODEURL_SECRET_KEY,
    )
    if not ethnode:
        raise EthNodeNotFound("ETHNODEURL not found")
    return Web3(Web3.HTTPProvider(ethnode))
