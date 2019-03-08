"""
Utilities used to pick the correct source of data for a given question
"""
import logging

from ask_fandom.errors import QuestionNotUnderstoodError
from ask_fandom.intents.base import AskFandomIntentBase
from ask_fandom.parser import NLPParser, filter_parsed_question


def get_intent(question: str):
    """
    Selects an appropriate intent class based on the question

    :type question str
    :rtype: AskFandomIntent
    :raises: QuestionNotUnderstoodError
    """
    logger = logging.getLogger('get_intent')
    logger.info('Parsing question: %s', question)

    parsed = NLPParser.parse_question(question)
    filtered = list(filter_parsed_question(parsed))

    logger.info('Parsed and filtered question: %s', filtered)

    # pick the longer token of a given type
    # ('NP', 'The End of Time episode')
    # ('NP', 'The End')
    words = dict()

    for _type, item in filtered:
        if _type not in words:
            words[_type] = item
        elif len(words[_type]) < len(item):
            words[_type] = item

    logger.info('Filtered words of the question: %s', words)

    # now try to ask each intent if it supports a given question
    intents = AskFandomIntentBase.intents()
    logger.info('Available intents: %s', [intent.__name__ for intent in intents])

    for intent in intents:
        logging.info('Trying %s ...', intent.__name__)

        if not intent.is_question_supported(words):
            # try a next one
            continue

        # words to arguments mapping
        mapping = intent.get_words_mapping()
        intent_args = dict()

        for args_key, words_key in mapping.items():
            # {'name': 'NP', 'property': 'VBD'}
            # args['name'] = words['NP'] ...

            # cast to list
            words_key = [words_key] if isinstance(words_key, str) else words_key

            for word_key in words_key:
                # is a given word defined? if so, pass it to intent arguments
                # {'name': 'NP', 'property': ('VBD', 'VBN')}
                if word_key in words and args_key not in intent_args:
                    intent_args[args_key] = words[word_key]

        logging.info('Selected %s with %s', intent, intent_args)

        # we have a match!
        return [intent, intent_args]

    raise QuestionNotUnderstoodError(question)
