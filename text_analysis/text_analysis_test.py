# tianhel@bu.edu 2021
from file_upload import *
from text_analysis import *

def test_read_json():
    with open("test.txt","w") as f:
        f.write("supercool")

    fu = File_Uploader("ta_test.json")
    i = fu.upload("test.txt")

    data = read_json("ta_test.json")
    assert len(data) > 0
