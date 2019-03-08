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
    oracle = get_oracle(question)
    print(oracle)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    ask_fandom("When was Jake Simmonds born?")
