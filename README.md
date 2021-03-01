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

flask ops:

json file structure: {"file_name":"", "text":""}

get file list: curl http://localhost:5000/files

get a single file: curl http://localhost:5000/files/file2

add a new file: curl http://localhost:5000/files -d "file_name=something new" -X POST -v

delete: curl http://localhost:5000/files/file2 -X DELETE -v

update a file desc: curl http://localhost:5000/files/file3 -d "file_name=something different" -X PUT -v

# Web Fetch

get list of link node in url:  res = get_from_url(url)

upload list to json:  store_list_to_json(res,jsname)

# Text Analysis

read from json file:  data = read_json(jsname)

# Resources about Flask-RESTful

https://flask-restful.readthedocs.io/en/latest/quickstart.html#full-example
