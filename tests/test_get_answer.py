from ask import ask_fandom


def test_ask_fandom():
    assert ask_fandom('Who played Agella?') == 'Agella is played by Suzanne Danielle.'
    assert ask_fandom('Who played Alaya?') == 'Alaya is played by Neve McIntosh.'

    assert ask_fandom('Who directed The Big Bang episode?') == \
        '"The Big Bang episode" episode has been directed by Toby Haynes.'

    assert ask_fandom('Who produced The Big Bang episode?') == \
        '"The Big Bang episode" episode has been produced by Peter Bennett.'
