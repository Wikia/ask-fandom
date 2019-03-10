from pytest import raises

from ask import ask_fandom
from ask_fandom.errors import AnswerNotKnownError


def test_ask_fandom():
    assert str(ask_fandom('Who played Agella?')) == 'Agella is played by Suzanne Danielle.'
    assert str(ask_fandom('Who played Alaya?')) == 'Alaya is played by Neve McIntosh.'

    assert str(ask_fandom('Who directed The Big Bang episode?')) == \
        '"The Big Bang episode" episode has been directed by Toby Haynes.'

    assert str(ask_fandom('Who produced The Big Bang episode?')) == \
        '"The Big Bang episode" episode has been produced by Peter Bennett.'

    assert str(ask_fandom('Which faction does the Alterac belong to?')) == \
        'Alterac is a member of "Contested territory" faction.'

    assert str(ask_fandom('Which government does Alterac belong to?')) == \
        'Alterac is a member of "Hereditary monarchy" government.'


def test_football():
    assert str(ask_fandom('Which club Romelu Lukaku plays for?')) == \
        'Romelu Lukaku plays for Manchester United F.C. now.'


def test_football_same_question():
    assert str(ask_fandom('Which club Cristiano Ronaldo plays for?')) == \
        'Cristiano Ronaldo plays for Juventus F.C. now.'

    assert str(ask_fandom('Where is Cristiano Ronaldo playing now?')) == \
        'Cristiano Ronaldo plays for Juventus F.C. now.'

    assert str(ask_fandom('Where does Cristiano Ronaldo play?')) == \
        'Cristiano Ronaldo plays for Juventus F.C. now.'


def test_ask_fandom_dont_know():
    with raises(AnswerNotKnownError):
        ask_fandom('Who played Unknown Character?')
