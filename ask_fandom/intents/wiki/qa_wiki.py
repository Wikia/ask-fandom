"""
Intent handling getting answets from Q&A wikis

https://answers.wikia.com/wiki/What_are_faxes_used_for
https://answers.wikia.com/wiki/Do_I_need_a_passport_to_travel_to_Italy
"""
from .base import AskFandomIntentBase


class AnswersWikiIntent(AskFandomIntentBase):
    """
    Provides answers using Answers wiki
    """
    ANSWER_PHRASE = '{answer}'

    @staticmethod
    def is_question_supported(words: dict):
        """
        Do I need a passport to travel to Italy?
        What are faxes used for?

        :rtype: bool
        """
        return False  # We use this intent as a fallback in ask_fandom function

    @classmethod
    def get_words_mapping(cls):
        """
        Maps intent arguments into word types from the question
        :rtype: dict
        """
        return None

    def _fetch_answer(self):
        # pylint: disable=fixme
        # https://answers.wikia.com/wiki/What_are_faxes_used_for
        answers_wiki = 'answers.wikia.com'
        page = self.question.rstrip('?')

        site = self.get_mw_client(answers_wiki)

        # http://answers.wikia.com/api.php?action=query&prop=revisions&titles=Do%20I%20need%20a%20passport%20to%20travel%20to%20Italy&rvprop=timestamp%7Cuser%7Ccomment%7Ccontent&rvparse=1&format=json
        page_object = site.pages[page]

        page_title = page_object.page_title
        wiki_text = page_object.text()

        self.logger.info('Got the wikitext from <%s>: %s', page_title, wiki_text)

        # take the first line of wikitext
        answer = wiki_text.split('\n')[0]

        if answer and not answer.startswith('[[Category:'):
            self._set_wikia_reference(answers_wiki, page_title)
            return answer.strip()

        return None
