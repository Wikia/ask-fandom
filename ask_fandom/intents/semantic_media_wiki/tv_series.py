"""
Intent handling episodes and characters questions
"""
from .base import SemanticFandomIntent


class PersonFactIntent(SemanticFandomIntent):
    """
    Provides data from a character / actor page
    """
    ANSWER_PHRASE = '{name} is played by {answer}.'

    @property
    def _answer(self):
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
    Provides data from an episode page
    """
    ANSWER_PHRASE = '"{name}" episode has been {property} by {answer}.'

    @property
    def _answer(self):
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
            name = name[:-8]

        values = self.get_smw_property_for_page('tardis.fandom.com', name, prop)

        return values[0] if values else None
