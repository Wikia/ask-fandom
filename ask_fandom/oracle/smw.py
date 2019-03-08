"""
Base class for asking SemanticMediaWiki wikis
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


class SemanticFandomOracle(AskFandomOracle):
    """
    A base class for oracles that queries SemanticMediaWiki data
    """
    @property
    def _answer(self):
        """
        :rtype: str
        """
        raise NotImplementedError()

    def get_smw_property_for_page(self, site: Site, page: str, prop: str):
        """
        Get page property from SMW

        :type site Site
        :type page str
        :type prop str
        :rtype: list[str]|None
        """
        self.logger.info("Asking SMW for '%s' page %s property", page, prop)

        # https://poznan.fandom.com/api.php?action=browsebysubject&subject=Karol_Libelt&format=json
        res = site.get(action='browsebysubject', subject=page)
        query_data = res['query']['data']

        for item in query_data:
            # we've found the property we're looking for
            if item['property'] == prop:
                values = [
                    # 'Andrew_Hayden-Smith#0#'
                    str(value['item']).replace('#0#', '').replace('_', ' ')
                    for value in item['dataitem']
                ]

                self.logger.info("Got the value for %s: %s", prop, values)

                return values

        return None