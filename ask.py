"""
Main entry point

Ask a question and get an answer in your command line
"""
import logging
from os import getenv
from sys import argv

from ask_fandom.intents.selector import get_intent


def ask_fandom(question: str):
    """
    :type question str
    :rtype: ask_fandom.intents.base.Answer
    """
    (intent_class, intent_args, _) = get_intent(question)
    intent = intent_class(question, **intent_args)

    return intent.get_answer()


if __name__ == "__main__":
    # Run with DEBUG=1 env variable to have more verbose logging
    logging.basicConfig(level=logging.DEBUG if getenv('DEBUG') == '1' else logging.INFO)

    # https://tardis.fandom.com/wiki/Special:Browse/Jake_Simmonds
    # default_question = 'Who played Jake Simmonds?'

    # https://football.fandom.com/wiki/Cristiano_Ronaldo
    default_question = 'Which club Cristiano Ronaldo plays for?'

    user_question = default_question if len(argv) < 2 else argv[1]

    answer = ask_fandom(user_question)
    logging.info('%s -> %s (%s: %s)',
                 answer.question, answer.answer, answer.intent.__name__, answer.meta)

    print('---')
    print(user_question)
    print(answer)
