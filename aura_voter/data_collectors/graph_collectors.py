from typing import Dict
from typing import List
from typing import Optional

from gql import gql

from aura_voter.constants import BALANCER_GQL_URL
from aura_voter.constants import HIDDEN_HAND_BRIBES_GQL_URL
from aura_voter.data_collectors.transports import make_gql_client

GET_BAL_POOLS_QUERY = """
query {{
  pools(first: {first}, skip: {skip}) {{
    id
    address
    poolType
    tokens{{
      id
      address
      symbol
    }}
  }}
}}
"""


GET_BRIBES_QUERY = """
query {{
  bribes(first: {first}, skip: {skip}) {{
    id
    proposal
    token
    amount
  }}
}}
"""


def get_all_balancer_pools() -> Optional[List[Dict]]:
    """
    """
    client = make_gql_client(BALANCER_GQL_URL)
    all_pools = []
    limit = 100
    offset = 0
    while True:
        result = client.execute(gql(GET_BAL_POOLS_QUERY.format(first=limit, skip=offset)))
        all_pools.extend(result['pools'])
        offset += limit
        if len(result['pools']) < limit - 1:
            break
    return all_pools


def get_all_aura_bribes() -> Optional[List[Dict]]:
    """
    Get all bribes that were emitted as events from DepositBribe event in AuraBribe contract
    """
    client = make_gql_client(HIDDEN_HAND_BRIBES_GQL_URL)
    limit = 100
    offset = 0
    bribes = []
    while True:
        result = client.execute(
            gql(
                GET_BRIBES_QUERY.format(first=limit, skip=offset),
            )
        )
        bribes.extend(result['bribes'])
        offset += limit
        if len(result['bribes']) < limit - 1:
            break
    return bribes
