# tianhel@bu.edu 2021
import json

def read_json(jsname):
    with open(jsname, "r", encoding='utf-8', errors='ignore') as f:
        #data = json.load(f)
        #data contains list of content

        data = json.load(f, strict=False)

        return data
