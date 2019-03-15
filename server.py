"""
This script runs a web interface of ask-fandom
"""
from ask_fandom.intents.base import AskFandomIntentBase
from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/info')
def info():
    return jsonify({
        'name': 'ask-fandom',
        'intents': [intent.__name__ for intent in AskFandomIntentBase.intents()]
    })
