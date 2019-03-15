"""
This script runs a web interface of ask-fandom
"""
import logging

from ask_fandom.intents.base import AskFandomIntentBase
from ask_fandom.errors import AskFandomError, QuestionNotUnderstoodError
from ask_fandom.intents.selector import get_intent
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)


def ask_fandom(question: str):
    """
    :type question str
    :rtype: tuple[ask_fandom.intents.base, ask_fandom.intents.base.Answer]
    """
    (intent_class, intent_args, words) = get_intent(question)
    intent = intent_class(question, **intent_args)

    return intent, words, intent.get_answer()


def get_example_questions():
    """
    :rtype: list[str]
    """
    ret = []

    for intent in AskFandomIntentBase.intents():
        ret += intent.get_example_questions()

    return sorted(ret)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/ask')
def ask():
    question = request.args.get('q')

    # you need to specify a question
    if not question:
        return jsonify({'error': 'You need to specify a question'}), 400  # Bad request

    app.logger.info('Question: %s', question)

    try:
        intent, words, answer = ask_fandom(question)
    except QuestionNotUnderstoodError:
        return jsonify({'error': 'I could not understand your question'}), 422  # UNPROCESSABLE ENTITY
    except AskFandomError as ex:
        return jsonify({'error': ex.__class__.__name__}), 404  # Not found the answer

    return jsonify({
        'answer': str(answer),
        '_intent': intent.__class__.__name__,
        '_meta': answer.meta,
        '_words': words,  # how the question has been understood by NLP system
        '_reference': answer.reference  # a link to the answer source
    })


@app.route('/examples')
def examples():
    return jsonify({
        'questions': get_example_questions()
    })


@app.route('/info')
def info():
    return jsonify({
        'name': 'ask-fandom',
        'intents': [intent.__name__ for intent in AskFandomIntentBase.intents()]
    })
