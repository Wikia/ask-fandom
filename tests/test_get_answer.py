from pytest import raises

from ask import ask_fandom
from ask_fandom.errors import AnswerNotKnownError


def test_ask_fandom():
    test_cases = {
        # question: answer
        'Who played Agella?': 'Agella is played by Suzanne Danielle.',
        'Who played Alaya?': 'Alaya is played by Neve McIntosh.',
        'Who directed The Big Bang episode?': '"The Big Bang" episode has been directed by Toby Haynes.',
        'Who produced The Big Bang episode?': '"The Big Bang" episode has been produced by Peter Bennett.',
        'Which faction does the Alterac belong to?':  'Alterac is a member of "Contested territory" faction.',
        'Which government does Alterac belong to?': 'Alterac is a member of "Hereditary monarchy" government.',

        # football
        'Which club Romelu Lukaku plays for?': 'Romelu Lukaku plays for Manchester United F.C. now.',

        # similar questions
        'Which club Cristiano Ronaldo plays for?': 'Cristiano Ronaldo plays for Juventus F.C. now.',
        'Where is Cristiano Ronaldo playing now?': 'Cristiano Ronaldo plays for Juventus F.C. now.',
        'Where does Cristiano Ronaldo play?': 'Cristiano Ronaldo plays for Juventus F.C. now.',

        # normalization
        'who directed The Big Bang episode': '"The Big Bang" episode has been directed by Toby Haynes.',
    }

    for question, expected_answer in test_cases.items():
        answer = ask_fandom(question)
        print(answer)
        assert str(answer) == expected_answer, question


def test_ask_fandom_dont_know():
    with raises(AnswerNotKnownError):
        ask_fandom('Who played Unknown Character?')
