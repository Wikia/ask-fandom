"""
Main entry point

Ask a question and get an answer in your command line
"""
import logging
from os import getenv
from sys import argv

from ask_fandom.errors import AskFandomError
from ask_fandom.intents import AnswersWikiIntent  # a temporary fallback for ask_fandom
from ask_fandom.intents.selector import get_intent


def ask_fandom(question: str):
    """
    :type question str
    :rtype: tuple[ask_fandom.intents.base, ask_fandom.intents.base.Answer]
    """
    try:
        (intent_class, intent_args, words) = get_intent(question)
        intent = intent_class(question, **intent_args)

        return intent, words, intent.get_answer()

    except AskFandomError as ex:
        try:
            # fall back to Q&A wiki site for an answer
            # TODO: fully index questions and answers and extract knowledge from them
            return AnswersWikiIntent, None, AnswersWikiIntent(question).get_answer()

        except AskFandomError:
            # return the original exception
            raise ex


if __name__ == "__main__":
    # Run with DEBUG=1 env variable to have more verbose logging
    logging.basicConfig(level=logging.DEBUG if getenv('DEBUG') == '1' else logging.INFO)

    # https://tardis.fandom.com/wiki/Special:Browse/Jake_Simmonds
    # default_question = 'Who played Jake Simmonds?'

    # https://football.fandom.com/wiki/Cristiano_Ronaldo
    default_question = 'Which club Cristiano Ronaldo plays for?'

    user_question = default_question if len(argv) < 2 else argv[1]

    (_, words, answer) = ask_fandom(user_question)
    logging.info('%s (%s) -> %s (%s: %s)',
                 answer.question, words, answer.answer, answer.intent.__name__, answer.meta)

    print('---')
    print(user_question)
    print(answer)
