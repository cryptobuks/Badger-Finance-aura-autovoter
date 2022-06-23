import json

import pytest
import responses

from aura_voter.cast_vote import FailedToVoteException
from aura_voter.cast_vote import cast_vote
from aura_voter.constants import SNAPSHOT_VOTE_API


@responses.activate
def test_cast_vote_happy(mocker):
    mocker.patch(
        "aura_voter.cast_vote.get_secret",
        return_value="private_key"
    )
    mocker.patch(
        "aura_voter.cast_vote.sign_message",
        return_value="signed_message"
    )
    responses.add(
        responses.POST,
        SNAPSHOT_VOTE_API,
        json={}, status=200
    )
    cast_vote(
        votes={'1': 1},
        snapshot_id="123",
    )
    body = json.loads(responses.calls[0].request.body)
    assert 'address' in body.keys()
    assert 'sig' in body.keys()
    assert 'data' in body.keys()


@responses.activate
def test_cast_vote_no_pk(mocker):
    """
    When no pk secret - should raise exc
    """
    mocker.patch(
        "aura_voter.cast_vote.get_secret",
        return_value=None
    )
    mocker.patch(
        "aura_voter.cast_vote.sign_message",
        return_value="signed_message"
    )
    responses.add(
        responses.POST,
        SNAPSHOT_VOTE_API,
        json={}, status=200
    )
    with pytest.raises(FailedToVoteException) as exc:
        cast_vote(
            votes={'1': 1},
            snapshot_id="123",
        )
    assert str(exc.value) == "Can't fetch private key"


@responses.activate
def test_cast_vote_error(mocker):
    """
    When vote didn't happen - raise exc
    """
    mocker.patch(
        "aura_voter.cast_vote.get_secret",
        return_value="pk"
    )
    mocker.patch(
        "aura_voter.cast_vote.sign_message",
        return_value="signed_message"
    )
    responses.add(
        responses.POST,
        SNAPSHOT_VOTE_API,
        json={}, status=500
    )
    with pytest.raises(FailedToVoteException) as exc:
        cast_vote(
            votes={'1': 1},
            snapshot_id="123",
        )
    assert str(exc.value) == "Voting failed on Snapshot. Error: {}"
