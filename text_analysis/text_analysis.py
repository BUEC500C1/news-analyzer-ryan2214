# tianhel@bu.edu 2021
import json

def read_json(jsname):
    with open(jsname, "r", encoding='utf-8') as f:
        #data = json.loads(f)
        #data contains list of content
        data = []

        for line in f.readlines():
            line = line.strip()   # 使用strip函数去除空行
            if len(line) != 0:
                json_data = json.loads(line)
                data.append(json_data)

        return data
