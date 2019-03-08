"""
Intent handling WoWWiki questions
"""
from .base import SemanticFandomIntent


class WoWGroupsMemberIntent(SemanticFandomIntent):
    """
    Provides World Of Warcraft nations membership data
    """
    ANSWER_PHRASE = '{name} is a member of "{answer}" {group}.'

    @property
    def _answer(self):
        # https://wowwiki.fandom.com/wiki/Special:Browse/Alterac
        # ({'name': 'the Alterac', 'group': 'faction'}
        name = str(self.args['name'])

        # remove 'the'
        if name.lower().startswith('the '):
            self.args['name'] = name = name[4:]

        site = self.get_mw_client('wowwiki.fandom.com')
        values = self.get_smw_property_for_page(site, name, self.args['group'])

        return values[0] if values else None
