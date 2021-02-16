# tianhel@bu.edu 2021
from file_upload import *

def test_read_json():
    with open("test.txt","w") as f:
        f.write("supercool")

    fu = File_Uploader("test.json")
    i = fu.upload("test.txt")
    data = read_json("test.json")
    assert len(data) > 0
