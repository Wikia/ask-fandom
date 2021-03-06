from pytest import raises

from ask_fandom.errors import QuestionNotUnderstoodError
from ask_fandom.intents import \
    PersonFactIntent, EpisodeFactIntent, \
    WoWGroupsMemberIntent, \
    FootballPlayerFactIntent
from ask_fandom.intents.selector import get_intent


def test_get_intent():
    # https://tardis.fandom.com/wiki/Special:Browse/Jake_Simmonds

    # get_intent returns three items: intent, passed params and words segments of the question
    assert get_intent(question='Who played Jake Simmonds?') == \
           [PersonFactIntent, {'name': 'Jake Simmonds', 'property': 'played'},
            {'NP': 'Jake Simmonds', 'VBD': 'played', 'WP': 'who'}]

    assert get_intent(question='When was Jake Simmonds born?')[:2] == \
           [PersonFactIntent, {'name': 'Jake Simmonds', 'property': 'born'}]

    # https://tardis.fandom.com/wiki/Special:Browse/The Big Bang
    assert get_intent(question='Who directed The Big Bang episode?')[:2] == \
           [EpisodeFactIntent, {'name': 'The Big Bang episode', 'property': 'directed'}]

    assert get_intent(question='Who played in The End of Time episode?')[:2] == \
           [EpisodeFactIntent, {'name': 'The End of Time episode', 'property': 'played'}]

    # https://wowwiki.fandom.com/wiki/Special:Browse/Alterac
    assert get_intent(question='Which faction does the Alterac belong to?')[:2] == \
           [WoWGroupsMemberIntent, {'name': 'the Alterac', 'group': 'faction'}]


def test_get_intent_football():
    assert get_intent(question='Where does Cristiano Ronaldo play?')[:2] == \
           [FootballPlayerFactIntent, {'name': 'Cristiano Ronaldo', 'property': 'play'}]

    assert get_intent(question='Where is Cristiano Ronaldo playing now?')[:2] == \
           [FootballPlayerFactIntent, {'name': 'Cristiano Ronaldo', 'property': 'playing'}]

    assert get_intent(question='Which club Cristiano Ronaldo plays for?')[:2] == \
           [FootballPlayerFactIntent, {'name': 'Cristiano Ronaldo', 'property': 'plays'}]


def test_get_intent_not_understood():
    with raises(QuestionNotUnderstoodError):
        get_intent(question='Is foo a bar?')
