"""
Base class for asking SemanticMediaWiki wikis
"""
from mwclient import Site
from .base import AskFandomIntentBase


class SemanticFandomIntent(AskFandomIntentBase):
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
            if item['property'].lower() == prop.lower():
                values = [
                    # 'Andrew_Hayden-Smith#0#'
                    str(value['item']).replace('#0#', '').replace('_', ' ')
                    for value in item['dataitem']
                ]

                self.logger.info("Got the value for %s: %s", prop, values)

                return values

        return None
