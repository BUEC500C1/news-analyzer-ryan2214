# news-analyzer-ryan2214
news-analyzer-ryan2214 created by GitHub Classroom

File upload, text analysis and Web search.

# Level

/ : main page

/upload : deal with uploading pictures or text

/management : manage file uploaded

/analyse : process text file by NLP

# File Upload

1. choose file

2. click upload

# Web Fetch

get list of link node in url:  res = get_from_url(url)

upload list to json:  store_list_to_json(res,jsname)

# Text Analysis

read from json file:  data = read_json(jsname)

# Resources about Flask-RESTful

https://flask-restful.readthedocs.io/en/latest/quickstart.html#full-example
