"""
Base class for asking Fandom
"""
import logging

from mwclient import Site

from ask_fandom.errors import AnswerNotKnownError


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

        :rtype: Answer
        :raise: AnswerNotKnownError
        """
        answer = self._answer

        if answer is None:
            raise AnswerNotKnownError(self.question)

        params = {"answer": answer}
        params.update(self.args)

        return Answer(
            question=self.question,
            answer=self.ANSWER_PHRASE.format(**params),
            meta=self.args
        )

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


class Answer:
    """
    A simple wrapper for an answer.
    Keeps its string representation, metadata and references.
    """
    # pylint: disable=too-few-public-methods
    def __init__(self, question: str, answer: str, meta: dict = None, reference: str = None):
        """
        Constructor
        """
        self.question = question
        self.answer = answer
        self.meta = meta
        self.reference = reference

    def __str__(self):
        """
        :rtype: str
        """
        return self.answer
