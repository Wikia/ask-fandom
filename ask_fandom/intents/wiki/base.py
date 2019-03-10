"""
Base class for asking wiki templates
"""
import json
import re
from mwclient import Site

from ask_fandom.intents.base import AskFandomIntentBase


def extract_link(text):
    """
    :type text str
    :rtype: str|None
    """
    matches = extract_links(text)

    return matches[0] if matches else None


def extract_links(text):
    """
    ' FlagiconITA [[Juventus F.C.|Juventus]]\n' => 'Juventus F.C.

    :type text str
    :rtype: str|None
    """
    matches = re.findall(r'\[\[([^\]|]+)', text)

    return matches if matches else None


class WikiTemplatesIntent(AskFandomIntentBase):
    """
    A base class for intents using templates data
    """
    # pylint: disable=abstract-method

    @staticmethod
    def _get_templates_from_article(site: Site, title: str):
        """
        :type site Site
        :type title str
        :rtype: list[dict]
        """
        # https://nfs.fandom.com/wikia.php?controller=TemplatesApiController&method=getMetadata&title=Ferrari_355_F1
        res = json.loads(site.raw_call(
            http_method='GET',
            script='wikia',
            data={
                'controller': 'TemplatesApiController',
                'method': 'getMetadata',
                'title': title
            }
        ))

        return res['templates']

    def get_infobox_parameter(self, wiki_domain: str, page: str,
                              template_name: str, parameter_name: str):
        """
        :type wiki_domain str
        :type page str
        :type template_name str
        :type parameter_name str
        :rtype: str|None
        """
        self.logger.info("Asking %s wiki for '%s' page\'s '%s' template '%s' parameter",
                         wiki_domain, page, template_name, parameter_name)

        site = self.get_mw_client(wiki_domain)
        templates = self._get_templates_from_article(site, page)

        # print(templates)

        for template in templates:
            if template['name'] != template_name:
                continue

            value = template['parameters'].get(parameter_name)
            if value:
                return value

        return None
