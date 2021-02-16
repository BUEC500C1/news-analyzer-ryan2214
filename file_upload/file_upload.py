# tianhel@bu.edu 2021
import json
import os

class File_Uploader():
  def __init__(self, jsname = "temp.json"):
    self.jsname = jsname

  def upload(self, filename):
    try:
        with open(filename, "r") as f:
            data = f.read()

        with open(self.jsname, "a", encoding='utf-8') as j:
            j.write(data)
            print("Upload complete!")
            return 0
    except IOError:
        print("File is not accessible.")
        return -1

  def delete(self):
  	os.remove(self.jsname)
