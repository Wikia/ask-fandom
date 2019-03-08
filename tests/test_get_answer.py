from ask import ask_fandom


def test_ask_fandom():
    assert ask_fandom('Who played Agella?') == 'Agella is played by Suzanne Danielle.'
    assert ask_fandom('Who played Alaya?') == 'Alaya is played by Neve McIntosh.'
