from ask_fandom.oracle.base import get_oracle
from ask_fandom.oracle.oracles import PersonFactOracle, EpisodeFactOracle


def test_get_oracle():
    # # https://tardis.fandom.com/wiki/Special:Browse/Jake_Simmonds
    assert get_oracle(question='Who played Jake Simmonds?') == \
        [PersonFactOracle, {'name': 'Jake Simmonds', 'property': 'played'}]

    assert get_oracle(question='When was Jake Simmonds born?') == \
        [PersonFactOracle, {'name': 'Jake Simmonds', 'property': 'born'}]

    # https://tardis.fandom.com/wiki/Special:Browse/The Big Bang
    assert get_oracle(question='Who directed The Big Bang episode?') == \
        [EpisodeFactOracle, {'name': 'The Big Bang episode', 'property': 'directed'}]

    assert get_oracle(question='Who played in The End of Time episode?') == \
        [EpisodeFactOracle, {'name': 'The End of Time episode', 'property': 'played'}]
