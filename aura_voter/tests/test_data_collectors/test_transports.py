from aura_voter.data_collectors.transports import make_gql_client


def test_make_gql_client():
    url = "https://some.url"
    client = make_gql_client(url)
    assert client is not None
    assert client.transport.url == "https://some.url"  # noqa
