import logging
import re
from typing import Dict
from typing import Optional

from gql import gql

from aura_voter.constants import SNAPSHOT_GQL_API_URL
from aura_voter.constants import SNAPSHOT_MIN_AMOUNT_POOLS
from aura_voter.constants import SNAPSHOT_STATE_PENDING
from aura_voter.data_collectors.transports import make_gql_client
from gql.transport.requests import log

from aura_voter.web3 import get_web3

log.setLevel(logging.WARNING)

GET_ACTIVE_PROPOSALS_Q = """
query {{
  proposals (
    first: {first},
    skip: {skip},
    where: {{
      space_in: ["aurafinance.eth"],
      state: "active"
      network_in: ["1"]
    }},
    orderBy: "created",
    orderDirection: desc
  ) {{
    id
    title
    body
    start
    end
    snapshot
    choices
    network
    state
    author
    space {{
      id
      name
    }}
  }}
}}
"""


GET_ALL_PROPOSALS_Q = """
query {{
  proposals (
    first: {first},
    skip: {skip},
    where: {{
      space_in: ["aurafinance.eth"],
      network_in: ["1"]
    }},
    orderBy: "created",
    orderDirection: desc
  ) {{
    id
    title
    body
    start
    end
    snapshot
    choices
    network
    state
    author
    space {{
      id
      name
    }}
  }}
}}
"""


GET_SINGLE_PROPOSAL_Q = lambda snapshot_id: gql(f"""
query {{
  proposals (
    first: 1,
    skip: 0,
    where: {{
      space_in: ["aurafinance.eth"],
      network_in: ["1"]
      id: "{snapshot_id}"
    }},
    orderBy: "created",
    orderDirection: desc
  ) {{
    id
    title
    body
    start
    end
    snapshot
    choices
    network
    state
    author
    space {{
      id
      name
    }}
  }}
}}
""")


def get_gauge_weight_snapshot() -> Optional[Dict]:
    """
    Using title re match and some pool heuristics, tries to get current active
    gauge voting proposal. If not found, returns None
    """
    client = make_gql_client(SNAPSHOT_GQL_API_URL)
    web3 = get_web3()
    limit = 100
    offset = 0
    while True:
        result = client.execute(gql(GET_ACTIVE_PROPOSALS_Q.format(first=limit, skip=offset)))
        if not result or not result.get("proposals"):
            break
        gauge_proposal = None
        for proposal in result['proposals']:
            match = re.match(r"Gauge Weight for Week of .+", proposal['title'])
            number_of_choices = len(proposal['choices'])
            current_timestamp = web3.eth.getBlock(web3.eth.get_block_number())['timestamp']
            # Use heuristics to find out latest gauge proposal since there is no other way
            # to filter out CVX proposals
            if match and number_of_choices > SNAPSHOT_MIN_AMOUNT_POOLS:
                # Sanity check: proposal should have been started before current date and
                # should end after
                if proposal['end'] > current_timestamp > proposal['start']:
                    gauge_proposal = proposal
                    break
        return gauge_proposal


def get_amount_of_aura_proposals() -> Optional[int]:
    # TODO: Find ordinal number by snapshot ID instead of always taking last proposal ID
    """
    Utility function that calculates amount of gauge weight snapshot proposals for Aura.
    This is needed for data processing of HH bribes in other places
    """
    client = make_gql_client(SNAPSHOT_GQL_API_URL)
    limit = 100
    offset = 0
    gauge_weight_proposal_count = 0
    while True:
        result = client.execute(gql(GET_ALL_PROPOSALS_Q.format(first=limit, skip=offset)))
        offset += limit
        if not result or not result.get("proposals"):
            break
        for proposal in result['proposals']:
            match = re.match(r"Gauge Weight for Week of .+", proposal['title'])
            if match and proposal['state'] != SNAPSHOT_STATE_PENDING:
                gauge_weight_proposal_count += 1

    return gauge_weight_proposal_count


def get_snapshot_by_id(snapshot_id: str) -> Optional[Dict]:
    """
    Get single snapshot by id
    """
    client = make_gql_client(SNAPSHOT_GQL_API_URL)
    result = client.execute(GET_SINGLE_PROPOSAL_Q(snapshot_id))
    if not result or not result.get("proposals"):
        return
    return result['proposals'][0]
