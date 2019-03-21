"""
Base class for asking SemanticMediaWiki wikis
"""
from ask_fandom.intents.base import AskFandomIntentBase


class SemanticFandomIntent(AskFandomIntentBase):
    """
    A base class for an intent that queries SemanticMediaWiki data
    """
    # pylint: disable=abstract-method

    def get_smw_property_for_page(self, wiki_domain: str, page: str, prop: str):
        """
        Get page property from SMW

        :type wiki_domain str
        :type page str
        :type prop str
        :rtype: list[str]|None
        """
        self.logger.info("Asking %s SMW for '%s' page %s property", wiki_domain, page, prop)

        site = self.get_mw_client(wiki_domain)

        # https://poznan.fandom.com/api.php?action=browsebysubject&subject=Karol_Libelt&format=json
        res = site.get(action='browsebysubject', subject=page)
        query_data = res['query']['data']

        for item in query_data:
            # we've found the property we're looking for (case-insensitive)
            if item['property'].lower() == prop.lower():
                values = [
                    # 'Andrew_Hayden-Smith#0#'
                    str(value['item']).replace('#0#', '').replace('_', ' ')
                    for value in item['dataitem']
                ]

                self.logger.info("Got the value for %s: %s", prop, values)

                self._set_wikia_reference(wiki_domain, article_name=page)
                return values

        return None
