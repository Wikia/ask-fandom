"""
Main entry point

Ask a question and get an answer in your command line
"""
import logging
from sys import argv

from ask_fandom.intents.base import AskFandomIntentBase
from ask_fandom.intents.selector import get_intent


def ask_fandom(question: str):
    """
    :type question str
    :rtype: ask_fandom.intents.base.Answer
    """
    logging.info('Available intents: %s', AskFandomIntentBase.intents())

    (intent_class, intent_args) = get_intent(question)
    logging.info('Using %s intent (%s)', intent_class, intent_args)

    intent = intent_class(question, **intent_args)

    return intent.get_answer()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # https://tardis.fandom.com/wiki/Special:Browse/Jake_Simmonds
    user_question = "Who played Jake Simmonds?" if len(argv) < 2 else argv[1]

    answer = ask_fandom(user_question)
    logging.info('%s -> %s (%s: %s)',
                 answer.question, answer.answer, answer.intent.__name__, answer.meta)

    print('---')
    print(user_question)
    print(answer)
