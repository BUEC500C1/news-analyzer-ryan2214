# tianhel@bu.edu 2021
import json
import requests
import lxml.html

def get_from_url(url):
    html = requests.get(url).content
    selector = lxml.html.fromstring(html)
    res = selector.xpath("///a/text()")
    res1 = selector.xpath("///a/@href")

    return res;
    # print(res)
    # print(res1)

    #for i,s in enumerate(res):
    #    print(res1[i])
    #    print(s)

def store_list_to_json(res,jsname):
    with open(jsname, "a", encoding='utf-8') as j:
        j.write(data)
        print("json appended from list!")
        return 0