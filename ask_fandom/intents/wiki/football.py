"""
Intent handling football players and clubs

Which club Cristiano Ronaldo plays for?
Cristiano Ronaldo plays for Juventus F.C. now.
---
Where does Lionel Messi play?
Lionel Messi plays for FC Barcelona now.
"""
from .base import WikiTemplatesIntent, extract_link


class FootballPlayerFactIntent(WikiTemplatesIntent):
    """
    Provides data for a football player
    """
    ANSWER_PHRASE = '{name} plays for {answer} now.'

    @staticmethod
    def is_question_supported(words: dict):
        """
        Which club Cristiano Ronaldo plays for?
        Where is Lionel Messi playing now?

        :rtype: bool
        """
        if words.get('WRB') == 'where':
            # Where does Cristiano Ronaldo play?
            # {'WRB': 'Where', 'VBZ': 'does', 'NP': 'Cristiano Ronaldo', 'VB': 'play'}
            if words.get('VB') == 'play':
                return True

            # Where is Cristiano Ronaldo playing now?
            if words.get('VBG') == 'playing':
                return True

        if words.get('WDT') == 'which':
            # Which club Cristiano Ronaldo plays for?
            if words.get('VBZ') == 'plays' and words.get('IN') == 'for':
                return True

        return False

    @classmethod
    def get_words_mapping(cls):
        """
        Maps intent arguments into word types from the question
        :rtype: dict
        """
        return {'name': 'NP', 'property': ('VB', 'VBG', 'VBZ')}  # play, plays, playing

    def _fetch_answer(self):
        # https://football.fandom.com/wiki/Cristiano_Ronaldo
        # {'name': 'Cristiano Ronaldo', 'property': 'plays'}
        if str(self.args['property']).startswith('play'):

            value = self.get_infobox_parameter(
                wiki_domain='football.fandom.com',
                page=self.args['name'],
                template_name='Infobox Biography',
                parameter_name='currentclub',
            )

            # 'currentclub': ' FlagiconITA [[Juventus F.C.|Juventus]]\n'
            if value:
                self._set_wikia_reference('football.fandom.com', article_name=self.args['name'])
                return extract_link(value)

        return None
