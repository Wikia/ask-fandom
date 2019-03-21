"""
Tests Q&A intent
"""
from pytest import raises

from ask_fandom.errors import AnswerNotKnownError
from ask_fandom.intents import AnswersWikiIntent


def test_answers_wiki_intent():
    assert str(AnswersWikiIntent(question='What are faxes used for?').get_answer()) == \
           'Faxes are used to send documents from one location to another quickly.'

    answer = AnswersWikiIntent(question='Do I need a passport to travel to Italy?').get_answer()
    assert answer.answer == 'Yes, you need passport to travel in Italy unless you are the citizen of the Italy.'

    with raises(AnswerNotKnownError):
        AnswersWikiIntent(question='How can you represent bit information?').get_answer()
