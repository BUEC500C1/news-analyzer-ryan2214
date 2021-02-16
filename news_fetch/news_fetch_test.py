# tianhel@bu.edu 2021
from news_fetch import *

def test_get_from_url():
    res = get_from_url("https://www.youtube.com/")

    i = len(res)
    assert i > 0