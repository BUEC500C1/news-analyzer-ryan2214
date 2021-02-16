# tianhel@bu.edu 2021
from file_upload import *
import os

def test_success_file_upload():
    with open("test.txt","w") as f:
        f.write("supercool")

    fu = File_Uploader("test.json");
    i = fu.upload("test.txt")
    os.remove("test.txt")
    assert i == 0

def test_fail_file_upload():
    fu = File_Uploader("test.json");
    assert fu.upload("test.txt") == -1

def test_delete_file_upload():
    with open("test.txt","w") as f:
        f.write("supercool")

    fu = File_Uploader("test.json");
    i = fu.upload("test.txt")
    fu.delete()

    assert os.path.isfile("test.json") == 0
