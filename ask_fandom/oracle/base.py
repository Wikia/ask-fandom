"""
Utilities used to pick the correct source of data for a given question
"""
import logging

from ask_fandom.parser import parse_question, filter_parsed_question
from .oracles import EpisodeFactOracle, PersonFactOracle


def get_oracle(question: str):
    """
    Selects an appropriate oracle class based on the question

    :type question str
    :rtype: (str, dict)|None
    """
    logger = logging.getLogger('get_oracle')
    logger.info('Parsing question: %s', question)

    parsed = parse_question(question)
    filtered = list(filter_parsed_question(parsed))

    logger.info('Parsed question: %s', filtered)

    # pick the longer token of a given type
    # ('NP', 'The End of Time episode')
    # ('NP', 'The End')
    words = dict()

    for _type, item in filtered:
        if _type not in words:
            words[_type] = item
        elif len(words[_type]) < len(item):
            words[_type] = item

    print(words, filtered)

    # When was Jake Simmonds born?
    # {'NP': 'Jake Simmonds', 'WRB': 'When', 'VBN': 'born', 'VBD': 'was'}
    if words.get('WRB') == 'When' and words.get('VBD') == 'was':
        return [
            PersonFactOracle.__name__,
            {'name': words.get('NP'), 'property': words.get('VBN')}
        ]

    # Who directed The Big Bang episode?
    # {'WP': 'Who', 'VBD': 'directed', 'NP': 'The Big Bang episode', 'NN': 'episode'}
    if words.get('WP') == 'Who' and words.get('NN') == 'episode':
        return [
            EpisodeFactOracle.__name__,
            {'name': words.get('NP'), 'property': words.get('VBD')}
        ]

    # Who played in The End of Time episode?
    # {'WP': 'Who', 'VBD': 'played', 'IN': 'of', 'NP': 'Time episode', 'NN': 'episode'}
    if words.get('WP') == 'Who' and words.get('NN') == 'episode':
        return [
            EpisodeFactOracle.__name__,
            {'name': words.get('NP'), 'property': words.get('VBD')}
        ]

    return None
