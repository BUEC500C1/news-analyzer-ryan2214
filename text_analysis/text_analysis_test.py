# tianhel@bu.edu 2021
from senti_analyze import *

def test_senti_analyze():
    assert text_nlp("Good morning!\nHave a nice day!") > 0
