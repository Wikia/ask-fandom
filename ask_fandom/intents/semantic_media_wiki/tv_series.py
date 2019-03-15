"""
Intent handling episodes and characters questions
"""
from .base import SemanticFandomIntent


class PersonFactIntent(SemanticFandomIntent):
    """
    Provides data from "Doctor Who" character / actor page
    """
    ANSWER_PHRASE = '{name} is played by {answer}.'

    @staticmethod
    def is_question_supported(words: dict):
        """
        Who played Jake Simmonds?

        :rtype: bool
        """
        # Who played Jake Simmonds?
        # {'WP': 'Who', 'VBD': 'played', 'NP': 'Jake Simmonds'}
        if words.get('WP') == 'who' and words.get('VBD') == 'played' and 'IN' not in words:
            return True

        # When was Jake Simmonds born?
        # {'NP': 'Jake Simmonds', 'WRB': 'When', 'VBN': 'born', 'VBD': 'was'}
        if words.get('WRB') == 'when' and words.get('VBD') == 'was':
            return True

        return False

    @classmethod
    def get_words_mapping(cls):
        """
        Maps intent arguments into word types from the question
        :rtype: dict
        """
        return {'name': 'NP', 'property': ('VBN', 'VBD')}

    def _fetch_answer(self):
        # https://tardis.fandom.com/wiki/Special:Browse/Jake_Simmonds
        # {'name': 'Jake Simmonds', 'property': 'played'}
        # map a word from question to SMW property name
        if self.args['property'] == 'played':
            prop = 'Actor'
        else:
            return None

        values = self.get_smw_property_for_page('tardis.fandom.com', self.args['name'], prop)

        return values[0] if values else None


class EpisodeFactIntent(SemanticFandomIntent):
    """
    Provides data from "Doctor Who" episode page
    """
    ANSWER_PHRASE = '"{name}" episode has been {property} by {answer}.'

    @staticmethod
    def is_question_supported(words: dict):
        """
        Who directed The Big Bang episode?

        :rtype: bool
        """
        # {'WP': 'Who', 'VBD': 'directed', 'NP': 'The Big Bang episode', 'NN': 'episode'}
        if words.get('WP') == 'who' and words.get('NN') == 'episode':
            return True

        return False

    @classmethod
    def get_words_mapping(cls):
        """
        Maps intent arguments into word types from the question
        :rtype: dict
        """
        return {'name': 'NP', 'property': 'VBD'}

    def _fetch_answer(self):
        # https://tardis.fandom.com/wiki/Special:Browse/The_Big_Bang
        # {'name': 'The Big Bang episode', 'property': 'directed'}
        if self.args['property'] == 'directed':
            prop = 'Director'
        elif self.args['property'] == 'produced':
            prop = 'Producer'
        else:
            return None

        name = str(self.args['name'])

        # remove trailing 'episode'
        if name.endswith(' episode'):
            name = self.args['name'] = name[:-8]

        values = self.get_smw_property_for_page('tardis.fandom.com', name, prop)

        return values[0] if values else None
