"""
Answer wrapper
"""


class Answer:
    """
    A simple wrapper for an answer.
    Keeps its string representation, metadata and references.
    """
    # pylint: disable=too-few-public-methods, too-many-arguments
    def __init__(self, question: str, answer: str, intent: type,
                 meta: dict = None, reference: str = None):
        """
        Constructor
        """
        self.question = question
        self.answer = answer
        self.intent = intent
        self.meta = meta
        self.reference = reference

    def __str__(self):
        """
        :rtype: str
        """
        return self.answer
