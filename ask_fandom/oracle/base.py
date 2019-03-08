"""
Base class for asking Fandom
"""
import logging

from mwclient import Site


class AskFandomOracle:
    """
    An abstract class for getting data from our wikis
    """
    ANSWER_PHRASE = ''

    def __init__(self, question: str, **kwargs):
        """
        :type question str
        :type kwargs dict
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self.question = question
        self.args = kwargs

        self.logger.info("You've asked: '%s' (%s)", self.question, self.args)

    def __repr__(self):
        return '<{}> {}'.format(self.__class__.__name__, self.question)

    def answer(self):
        """
        Returns fully formatted answer

        :rtype: str|None
        """
        answer = self._answer

        if answer is None:
            return None

        params = {"answer": answer}
        params.update(self.args)

        return self.ANSWER_PHRASE.format(**params)

    @property
    def _answer(self):
        """
        :rtype: str
        """
        raise NotImplementedError()

    @staticmethod
    def get_mw_client(wiki_domain: str):
        """
        :type wiki_domain str
        :rtype: Site
        """
        return Site(host=('http', wiki_domain), path='/')
