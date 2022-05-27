import logging
from typing import Optional

from gql import Client
from gql.transport.requests import RequestsHTTPTransport
from gql.transport.requests import log

log.setLevel(logging.WARNING)


def make_gql_client(url: str) -> Optional[Client]:
    transport = RequestsHTTPTransport(url=url, retries=3)
    return Client(
        transport=transport, fetch_schema_from_transport=True, execute_timeout=60
    )
