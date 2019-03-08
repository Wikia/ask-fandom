"""
Data providers
"""
# pylint: disable=too-few-public-methods
from ask_fandom.oracle.smw import SemanticFandomOracle


class PersonFactOracle(SemanticFandomOracle):
    """
    Provides data from a character / actor page
    """
    ANSWER_PHRASE = '{name} is played by {answer}.'

    @property
    def _answer(self):
        # {'name': 'Jake Simmonds', 'property': 'played'}
        # map a word from question to SMW property name
        if self.args['property'] == 'played':
            prop = 'Actor'
        else:
            return None

        site = self.get_mw_client('tardis.fandom.com')
        values = self.get_smw_property_for_page(site, self.args['name'], prop)

        return values[0] if values else None


class EpisodeFactOracle(SemanticFandomOracle):
    """
    Provides data from an episode page
    """
    @property
    def _answer(self):
        return None
