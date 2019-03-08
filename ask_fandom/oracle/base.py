"""
Utilities used to pick the correct source of data for a given question
"""
import logging
from bllipparser import RerankingParser

from .oracles import EpisodeFactOracle, PersonFactOracle


# https://pypi.org/project/bllipparser/
PARSER = RerankingParser.fetch_and_load('WSJ-PTB3', verbose=True)


def parse_question(question: str):
    """
    Parses given question into NLP tree

    :type question str
    :rtype: bllipparser.RerankingParser.Tree
    """
    return PARSER.parse(question)[0].ptb_parse


def filter_parsed_question(tree):
    """
    Filters and flattens a given NLP tree
    and keeps only most important parts of it

    :type tree tree
    :rtype: list[str, str]
    """
    def get_item_type_and_value(_item: str):
        """
        :type _item str
        :rtype: (str, str)
        """
        # (NNP Jake) -> NNP Jake
        _item = str(_item)[1:-1]
        return _item.split(' ', 1)

    for item in tree.all_subtrees():
        # (WHADVP (WRB When)) -> WHADVP
        (item_type, item_value) = get_item_type_and_value(item)

        item_len = len(item)

        # (WP Who)
        # (WRB When)
        # (VBD was)
        # (VBN born)
        # (IN in)
        # (NN episode)
        if item_len == 0 and item_type in ['WP', 'WRB', 'VBD', 'VBN', 'IN', 'NN']:
            yield item_type, item_value

        # (NP (NNP Jake) (NNP Simmonds))
        # (NP (DT The) (NNP Big) (NNP Bang) (NN episode)
        # (NP (NP (DT The) (NN End)) (PP (IN of) (NP (NNP Time) (NN episode))))
        elif item_type == 'NP':
            # merge subtrees into a single NP item
            items = [
                get_item_type_and_value(sub_item)
                for sub_item in item.all_subtrees()
            ]

            # take only NNP(S) items - words of NP
            item_value = [
                item[1]
                for item in items if item[0] in ['DT', 'NNP', 'NNPS', 'IN', 'NN']  # (NNP Simmonds)
            ]

            yield item_type, ' '.join(item_value)


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
