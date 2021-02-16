# news-analyzer-ryan2214
news-analyzer-ryan2214 created by GitHub Classroom

File upload, text analysis and Web search.

All the test cases are actually the best use cases.

# Json

{"filename": "a.txt", "data": "super\n"}

# File Upload

init:  f = File_Uploader(jsname)

upload txt:  f.upload(filename)

delete json:  f.delete()

# Web Fetch

get list of link node in url:  res = get_from_url(url)

upload list to json:  store_list_to_json(res,jsname)

# Text Analysis

read from json file:  data = read_json(jsname)
