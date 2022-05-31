from decimal import Decimal

from aura_voter.data_collectors import PoolBalance
from aura_voter.voting_algorithms.poc_algorithm import POCVoter


def test_poc_algorithm_happy_simple_data():
    locked_aura = Decimal(1000)
    balances = [
        PoolBalance(
            pool_id="some_pool1",
            balance=Decimal(1),
            target_token="0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"
        ),
        PoolBalance(
            pool_id="some_pool2",
            balance=Decimal(3),
            target_token="0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"
        ),
        PoolBalance(
            pool_id="some_pool3",
            balance=Decimal(4),
            target_token="0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"
        )
    ]
    voter = POCVoter(locked_aura, balances)
    votes = voter.propose_voting_choices()
    assert votes == {
        'badger_wbtc': Decimal('99.27999999999999998223643161'),
        'some_pool1': Decimal('0.09000000000000000222044604925'),
        'some_pool2': Decimal('0.2700000000000000066613381478'),
        'some_pool3': Decimal('0.3600000000000000088817841970')
    }
    # Make sure all votes make 100% when summed up
    assert sum(votes.values()) == Decimal(100)
