"""
Parser a question in natural language into a syntax tree
"""
from bllipparser import RerankingParser


class NLPParser:
    """
    Natural language questions parses using bllipparser model
    """
    # pylint: disable=too-few-public-methods
    instance = None

    @classmethod
    def parse_question(cls, question: str):
        """
        Parses given question into NLP tree

        :type question str
        :rtype: bllipparser.RerankingParser.Tree
        """
        if cls.instance is None:
            # https://pypi.org/project/bllipparser/
            cls.instance = RerankingParser.fetch_and_load('WSJ-PTB3', verbose=True)

        return cls.instance.parse(question)[0].ptb_parse


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
        # print(item)

        # (WHADVP (WRB When)) -> WHADVP
        (item_type, item_value) = get_item_type_and_value(item)

        item_len = len(item)

        # (WP Who)
        # (WRB When)
        # (VBD was)
        # (VBN born)
        # (IN in)
        # (NN episode)
        # (WDT Which)
        # (VB belong)
        # (TO to)
        # (VBZ does)
        if item_len == 0 and \
                item_type in ['WP', 'WRB', 'VBD', 'VBN', 'IN', 'NN', 'WDT', 'VB', 'TO', 'VBZ']:
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
