"""
Ask Fandpm exceptions
"""


class AskFandomError(Exception):
    """
    Base exception
    """


class QuestionNotUnderstoodError(AskFandomError):
    """
    We could not understand your question
    """


class AnswerNotKnownError(AskFandomError):
    """
    We could not find an answer for your valid question
    """
