# tianhel@bu.edu 2021
from file_upload import *

def test_success_file_upload():
    with open("test.txt","w") as f:
        f.write("supercool")

    fu = File_Uploader("test.json");
    i = fu.upload("test.txt")
    assert i == 0

    with open("test.json", "r", encoding='utf-8') as f:
        data = json.load(f)

    assert data = "supercool"