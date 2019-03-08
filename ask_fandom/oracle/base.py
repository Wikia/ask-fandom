"""
Utilities used to pick the correct source of data for a given question
"""
import logging
from bllipparser import RerankingParser

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

        print(item)

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

            print()
            print('NP', items)
            print()

            # take only NNP(S) items - words of NP
            item_value = [
                item[1]
                for item in items if item[0] in ['DT', 'NNP', 'NNPS', 'IN', 'NN']  # (NNP Simmonds)
            ]

            yield item_type, ' '.join(item_value)


def get_oracle(question: str):
    """
    Selects an appriopriate oracle class based on the question

    :type question str
    :rtype: list
    """
    logger = logging.getLogger('get_oracle')
    logger.info('Parsing question: %s', question)

    parsed = parse_question(question)
    for item in parsed.all_subtrees():
        print(item, item.__class__.__name__, len(item))

    logger.info('Parsed question: %s', parsed.pretty_string())

    return []
