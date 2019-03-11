"""
This script emits Markdown-formatted documentation of available intents.
"""
from ask_fandom.intents.base import AskFandomIntentBase

if __name__ == "__main__":
    print('Intents')
    print('=======')
    print('This file documents all available intents that can answer various types of questions.')

    for intent in AskFandomIntentBase.intents():
        print('')
        print(intent.get_documentation())
