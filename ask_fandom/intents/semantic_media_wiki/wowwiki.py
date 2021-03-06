"""
Intent handling WoWWiki questions
"""
from .base import SemanticFandomIntent


class WoWGroupsMemberIntent(SemanticFandomIntent):
    """
    Provides World Of Warcraft nations membership data
    """
    ANSWER_PHRASE = '{name} is a member of "{answer}" {group}.'

    @staticmethod
    def is_question_supported(words: dict):
        """
        Which faction does the Alterac belong to?

        :rtype: bool
        """
        # {'WDT': 'Which', 'NN': 'faction', 'VBZ': 'does',
        # 'NP': 'the Alterac', 'VB': 'belong', 'TO': 'to'}
        if words.get('WDT') == 'which' and words.get('VB') == 'belong' and words.get('TO', 'to'):
            return True

        return False

    @classmethod
    def get_words_mapping(cls):
        """
        Maps intent arguments into word types from the question
        :rtype: dict
        """
        return {'name': 'NP', 'group': 'NN'}

    def _fetch_answer(self):
        # https://wowwiki.fandom.com/wiki/Special:Browse/Alterac
        # ({'name': 'the Alterac', 'group': 'faction'}
        name = str(self.args['name'])

        # remove 'the'
        if name.lower().startswith('the '):
            self.args['name'] = name = name[4:]

        values = self.get_smw_property_for_page('wowwiki.fandom.com', name, self.args['group'])

        return values[0] if values else None
