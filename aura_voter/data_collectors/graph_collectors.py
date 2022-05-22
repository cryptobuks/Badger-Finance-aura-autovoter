from typing import Dict
from typing import List
from typing import Optional

from gql import gql

from aura_voter.constants import BALANCER_GQL_URL
from aura_voter.data_collectors.transports import make_gql_client

GET_BAL_POOLS_QUERY = """
query {{
  pools(first: {first}, skip: {skip}) {{
    id
    address
    poolType
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
