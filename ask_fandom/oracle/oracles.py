"""
Data providers
"""
# pylint: disable=too-few-public-methods
from ask_fandom.oracle.smw import SemanticFandomOracle


class PersonFactOracle(SemanticFandomOracle):
    """
    Provides data from a character / actor page
    """
    def answer(self):
        pass


class EpisodeFactOracle(SemanticFandomOracle):
    """
    Provides data from an episode page
    """
    def answer(self):
        pass
