"""
Utilities used to pick the correct source of data for a given question
"""
import logging

from ask_fandom.errors import QuestionNotUnderstoodError
from ask_fandom.parser import NLPParser, filter_parsed_question
from .oracles import EpisodeFactOracle, PersonFactOracle, WoWGroupsMemberOracle


def get_oracle(question: str):
    """
    Selects an appropriate oracle class based on the question

    :type question str
    :rtype: AskFandomOracle
    :raises: QuestionNotUnderstoodError
    """
    logger = logging.getLogger('get_oracle')
    logger.info('Parsing question: %s', question)

    parsed = NLPParser.parse_question(question)
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

    # print(words, filtered)

    # Who played Jake Simmonds?
    # {'WP': 'Who', 'VBD': 'played', 'NP': 'Jake Simmonds'}
    if words.get('WP') == 'Who' and words.get('VBD') == 'played' and 'IN' not in words:
        return [
            PersonFactOracle,
            {'name': words.get('NP'), 'property': words.get('VBD')}
        ]

    # When was Jake Simmonds born?
    # {'NP': 'Jake Simmonds', 'WRB': 'When', 'VBN': 'born', 'VBD': 'was'}
    if words.get('WRB') == 'When' and words.get('VBD') == 'was':
        return [
            PersonFactOracle,
            {'name': words.get('NP'), 'property': words.get('VBN')}
        ]

    # Who directed The Big Bang episode?
    # {'WP': 'Who', 'VBD': 'directed', 'NP': 'The Big Bang episode', 'NN': 'episode'}
    if words.get('WP') == 'Who' and words.get('NN') == 'episode':
        return [
            EpisodeFactOracle,
            {'name': words.get('NP'), 'property': words.get('VBD')}
        ]

    # Who played in The End of Time episode?
    # {'WP': 'Who', 'VBD': 'played', 'IN': 'of', 'NP': 'Time episode', 'NN': 'episode'}
    if words.get('WP') == 'Who' and words.get('NN') == 'episode':
        return [
            EpisodeFactOracle,
            {'name': words.get('NP'), 'property': words.get('VBD')}
        ]

    # Which faction does the Alterac belong to?
    # {'WDT': 'Which', 'NN': 'faction', 'VBZ': 'does',
    # 'NP': 'the Alterac', 'VB': 'belong', 'TO': 'to'}
    if words.get('WDT') == 'Which' and words.get('VB') == 'belong' and words.get('TO', 'to'):
        return [
            WoWGroupsMemberOracle,
            {'name': words.get('NP'), 'group': words.get('NN')}
        ]

    raise QuestionNotUnderstoodError(question)
