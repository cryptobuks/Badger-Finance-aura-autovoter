from unittest.mock import MagicMock

from aura_voter.data_collectors.snapshot_collectors import get_gauge_weight_snapshot
from aura_voter.data_collectors.snapshot_collectors import get_snapshot_by_id
from aura_voter.tests.test_data.test_data import PROPOSAL_TEST_DATA


def test_get_gauge_weight_snapshot_happy(mocker):
    mocker.patch(
        'aura_voter.data_collectors.snapshot_collectors.make_gql_client',
        return_value=MagicMock(
            execute=MagicMock(
                return_value=PROPOSAL_TEST_DATA,
            )
        )
    )
    mocker.patch(
        "aura_voter.data_collectors.snapshot_collectors.get_web3",
        return_value=MagicMock(eth=MagicMock(
            getBlock=MagicMock(
                return_value={'timestamp': 1655956810}
            )
        ))
    )
    result = get_gauge_weight_snapshot()
    assert result['title'] == "Gauge Weight for Week of 23rd June 2022"
    assert result['state'] == "active"
    assert result['space'] == {'id': 'aurafinance.eth', 'name': 'Aura Finance'}


def test_get_gauge_weight_snapshot_no_match(mocker):
    data = PROPOSAL_TEST_DATA
    mocker.patch(
        'aura_voter.data_collectors.snapshot_collectors.make_gql_client',
        return_value=MagicMock(
            execute=MagicMock(
                return_value=data,
            )
        )
    )
    mocker.patch(
        "aura_voter.data_collectors.snapshot_collectors.get_web3",
        return_value=MagicMock(eth=MagicMock(
            getBlock=MagicMock(
                return_value={'timestamp': 1648684815}
            )
        ))
    )
    assert not get_gauge_weight_snapshot()


def test_get_gauge_weight_snapshot_empty_res(mocker):
    mocker.patch("aura_voter.data_collectors.snapshot_collectors.get_web3", )
    mocker.patch(
        'aura_voter.data_collectors.snapshot_collectors.make_gql_client',
        return_value=MagicMock(
            execute=MagicMock(
                return_value={},
            )
        )
    )
    assert not get_gauge_weight_snapshot()


def test_get_gauge_weight_snapshot_time_mismatch(mocker):
    """
    Case when voting round already closed for voting, hence we should just return None
    """
    mocker.patch(
        'aura_voter.data_collectors.snapshot_collectors.make_gql_client',
        return_value=MagicMock(
            execute=MagicMock(
                return_value=PROPOSAL_TEST_DATA,
            )
        )
    )
    mocker.patch(
        "aura_voter.data_collectors.snapshot_collectors.get_web3",
        return_value=MagicMock(eth=MagicMock(
            getBlock=MagicMock(
                # Current timestamp is way in the future from the `end` of current proposal
                return_value={'timestamp': 1649116900}
            )
        ))
    )
    assert not get_gauge_weight_snapshot()


def test_get_snapshot_by_id(mocker):
    mocker.patch(
        'aura_voter.data_collectors.snapshot_collectors.make_gql_client',
        return_value=MagicMock(
            execute=MagicMock(
                return_value=PROPOSAL_TEST_DATA,
            )
        )
    )
    snapshot = get_snapshot_by_id(
        "0xabaf9275ae0533ce991059e8b5664225bf54bae81b9305ae60b48198db180ad9"
    )
    assert snapshot['title'] == 'Gauge Weight for Week of 23rd June 2022'
    assert snapshot['state'] == "active"


def test_get_snapshot_by_id_empty_res(mocker):
    mocker.patch(
        'aura_voter.data_collectors.snapshot_collectors.make_gql_client',
        return_value=MagicMock(
            execute=MagicMock(
                return_value={},
            )
        )
    )
    assert not get_snapshot_by_id(
        "0xabaf9275ae0533ce991059e8b5664225bf54bae81b9305ae60b48198db180ad9"
    )
