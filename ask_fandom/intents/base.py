"""
Base class for asking Fandom
"""
import logging

from mwclient import Site

from ask_fandom.answer import Answer
from ask_fandom.errors import AnswerNotKnownError


class AskFandomIntentBase:
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

    def get_answer(self):
        """
        Returns fully formatted answer

        :rtype: Answer
        :raise: AnswerNotKnownError
        """
        answer = self._fetch_answer()

        if answer is None:
            raise AnswerNotKnownError(self.question)

        meta = {"answer": answer}
        meta.update(self.args)

        return Answer(
            question=self.question,
            answer=self.ANSWER_PHRASE.format(**meta),
            intent=self.__class__,
            meta=meta
        )

    def _fetch_answer(self):
        """
        :rtype: str
        """
        raise NotImplementedError()

    @staticmethod
    def is_question_supported(words: dict):
        """
        :rtype: bool
        """
        raise NotImplementedError()

    @classmethod
    def get_words_mapping(cls):
        """
        Maps intent arguments into word types from the question
        :rtype: dict
        """
        raise NotImplementedError()

    @classmethod
    def intents(cls):
        """
        Get the list of all registered intents

        :rtype: list[AskFandomIntentBase]
        """
        ret = []

        for intent in cls.__subclasses__():
            # more subclasses?
            if intent.__subclasses__():
                ret += [
                    sub_intent
                    for sub_intent in intent.__subclasses__()
                ]
            else:
                ret.append(intent)

        return ret

    @staticmethod
    def get_mw_client(wiki_domain: str):
        """
        :type wiki_domain str
        :rtype: Site
        """
        return Site(host=('http', wiki_domain), path='/')
