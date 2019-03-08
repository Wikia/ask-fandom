"""
Handles parsing of questions
"""
import logging
from ask_fandom.oracle import get_oracle


def ask_fandom(question: str):
    """
    :type question str
    :rtype: str
    """
    oracle_spec = get_oracle(question)

    if oracle_spec is None:
        raise NotImplemented('I did not understand your question :(')

    (oracle_class, oracle_args) = oracle_spec
    oracle = oracle_class(question, **oracle_args)

    return oracle.answer()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # https://tardis.fandom.com/wiki/Special:Browse/Jake_Simmonds
    answer = ask_fandom("Who played Jake Simmonds?")

    print(answer)
