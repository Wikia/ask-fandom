from pytest import raises

from ask_fandom.errors import QuestionNotUnderstoodError
from ask_fandom.intents import PersonFactIntent, EpisodeFactIntent, WoWGroupsMemberIntent
from ask_fandom.intents.selector import get_intent


def test_get_oracle():
    # https://tardis.fandom.com/wiki/Special:Browse/Jake_Simmonds
    assert get_intent(question='Who played Jake Simmonds?') == \
           [PersonFactIntent, {'name': 'Jake Simmonds', 'property': 'played'}]

    assert get_intent(question='When was Jake Simmonds born?') == \
           [PersonFactIntent, {'name': 'Jake Simmonds', 'property': 'born'}]

    # https://tardis.fandom.com/wiki/Special:Browse/The Big Bang
    assert get_intent(question='Who directed The Big Bang episode?') == \
           [EpisodeFactIntent, {'name': 'The Big Bang episode', 'property': 'directed'}]

    assert get_intent(question='Who played in The End of Time episode?') == \
           [EpisodeFactIntent, {'name': 'The End of Time episode', 'property': 'played'}]

    # https://wowwiki.fandom.com/wiki/Special:Browse/Alterac
    assert get_intent(question='Which faction does the Alterac belong to?') == \
           [WoWGroupsMemberIntent, {'name': 'the Alterac', 'group': 'faction'}]


def test_get_oracle_not_understood():
    with raises(QuestionNotUnderstoodError):
        get_intent(question='Is foo a bar?')
