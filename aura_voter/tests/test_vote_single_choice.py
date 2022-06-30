import pytest
import responses

from aura_voter.cast_vote import FailedToVoteException
from aura_voter.vote_single_choice import vote_single_choice


@responses.activate
def test_voting_single_choice(mocker):
    """
    Dummy test to make sure everything works
    """
    cast_vote = mocker.patch('aura_voter.vote_single_choice.cast_single_choice_vote')
    vote_single_choice()
    assert cast_vote.called


@responses.activate
def test_voter_voting_raises(mocker):
    cast_vote = mocker.patch(
        'aura_voter.vote_single_choice.cast_single_choice_vote',
        side_effect=FailedToVoteException
    )

    with pytest.raises(FailedToVoteException):
        vote_single_choice()
    assert cast_vote.called
