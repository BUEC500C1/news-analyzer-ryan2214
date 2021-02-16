# tianhel@bu.edu 2021
from file_upload import *

def test_success_file_upload():
    with open("test.txt","w") as f:
        f.write("supercool")

    fu = File_Uploader("test.json");
    assert fu.upload("test.txt") == 0

    with open("test.json", "r", encoding='utf-8') as f:
        assert json.load(f) = "supercool"