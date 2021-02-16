# tianhel@bu.edu 2021
from file_upload import *

def test_success_file_upload():
    with open("test.txt","w") as f:
        f.write("supercool")

    fu = File_Uploader("test.json");
    assert fu.upload("test.txt") == 0

def test_fail_file_upload():
    fu = File_Uploader("test.json");
    assert fu.upload("test.txt") == -1