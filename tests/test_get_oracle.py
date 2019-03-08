from ask_fandom.oracle.base import get_oracle


def test_get_oracle():
    assert get_oracle(question='When was Jake Simmonds born?') == \
        ['PersonFactOracle', {'name': 'Jake Simmonds', 'property': 'born'}]

    assert get_oracle(question='Who directed The Big Bang episode?') == \
        ['EpisodeFactOracle', {'name': 'The Big Bang episode', 'property': 'directed'}]

    assert get_oracle(question='Who played in The End of Time episode?') == \
        ['EpisodeFactOracle', {'name': 'The End of Time episode', 'property': 'played'}]
