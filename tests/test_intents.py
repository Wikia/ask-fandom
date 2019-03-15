"""
Tests intents
"""
from ask_fandom.intents import FootballPlayerFactIntent


def test_football_intent():
    assert FootballPlayerFactIntent.get_example_questions() == [
        'Which club Cristiano Ronaldo plays for?',
        'Where is Lionel Messi playing now?',
    ]
