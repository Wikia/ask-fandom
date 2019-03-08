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
    :rtype: str
    """
    oracle_spec = get_intent(question)

    (oracle_class, oracle_args) = oracle_spec
    oracle = oracle_class(question, **oracle_args)

    return oracle.answer()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # https://tardis.fandom.com/wiki/Special:Browse/Jake_Simmonds
    user_question = "Who played Jake Simmonds?" if len(argv) < 2 else argv[1]

    answer = ask_fandom(user_question)

    print('---')
    print(user_question)
    print(answer)
