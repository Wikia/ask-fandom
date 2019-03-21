"""
Parses a given question in natural language and picks an intent class.

Intent encapsulates handling of a specific question type.
"""
# Intents concept: https://developer.amazon.com/docs/custom-skills/episode-intents.html

# allow intents to be discovered
from .semantic_media_wiki import EpisodeFactIntent, PersonFactIntent, WoWGroupsMemberIntent
from .wiki import AnswersWikiIntent, FootballPlayerFactIntent
