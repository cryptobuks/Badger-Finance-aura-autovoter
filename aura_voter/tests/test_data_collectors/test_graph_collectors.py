from unittest.mock import MagicMock

from aura_voter.data_collectors.graph_collectors import get_all_aura_bribes
from aura_voter.data_collectors.graph_collectors import get_all_balancer_pools
from aura_voter.tests.test_data.bribes_graph_data import AURA_BRIBES_DATA
from aura_voter.tests.test_data.balancer_graph_data import BALANCER_POOLS_DATA


def test_get_bal_pools_happy(mocker):
    client = mocker.patch(
        'aura_voter.data_collectors.graph_collectors.make_gql_client',
        return_value=MagicMock(
            execute=MagicMock(
                return_value=BALANCER_POOLS_DATA,
            )
        )
    )
    result = get_all_balancer_pools()
    assert client.return_value.execute.called
    client.return_value.execute.assert_called_once()
    assert result == BALANCER_POOLS_DATA['pools']


def test_get_all_aura_bribes_happy(mocker):
    client = mocker.patch(
        'aura_voter.data_collectors.graph_collectors.make_gql_client',
        return_value=MagicMock(
            execute=MagicMock(
                return_value=AURA_BRIBES_DATA,
            )
        )
    )
    bribes = get_all_aura_bribes()
    assert client.return_value.execute.called
    client.return_value.execute.assert_called_once()
    assert bribes == AURA_BRIBES_DATA['bribes']
