"""
Main entry point

Ask a question and get an answer in your command line
"""
import logging
from sys import argv

from ask_fandom.intents.selector import get_intent


def ask_fandom(question: str):
    """
    :type question str
    :rtype: ask_fandom.intents.base.Answer
    """
    (oracle_class, oracle_args) = get_intent(question)
    logging.info('Using %s intent (%s)', oracle_class, oracle_args)

    oracle = oracle_class(question, **oracle_args)

    return oracle.get_answer()


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
