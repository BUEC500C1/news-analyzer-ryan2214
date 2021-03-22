# coding:utf-8
 
from flask import Flask, render_template, request, redirect, url_for, make_response,jsonify
from flask_restful import reqparse, abort, Api, Resource
from werkzeug.utils import secure_filename
from pathlib import Path
from file_upload.pdf_parse import *
from text_analysis.senti_analyze import *
import json
import logging
import base64
import os
import cv2
import time
import pymongo
import numpy as np
from bson.objectid import ObjectId
 
from datetime import timedelta
 
# set file type permitted
ALLOWED_PICTURE_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp'])
ALLOWED_TEXT_EXTENSIONS = set(['pdf', 'txt'])
 
def is_picture(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_PICTURE_EXTENSIONS

def is_text(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_TEXT_EXTENSIONS

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o,ObjectId):
            return str(o)
        return json.JSONEncoder.default(self,o)

app = Flask(__name__)
api = Api(app)

# set static outdate time
app.send_file_max_age_default = timedelta(seconds=1)
 


##FILES = {
##    "filename": "super news",
##    "filetype": "pic" or "txt",
##    "content": "a very nice day",
##    "keyword": {"cool", "super"}
##}

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["filedb"]
myfile = mydb["files"]

FILES = {}

parser = reqparse.RequestParser()
parser.add_argument('file_name')
parser.add_argument('file_type')  # text, jpg
parser.add_argument('text')

def parse_json(data):
    return json.loads(json_util.dumps(data))

def parse_dir(root_dir):
  path = Path(root_dir)
 
  all_json_file = list(path.glob('**/*.json'))
  parse_result = []
  for json_file in all_json_file:
    mydict = {}

    with json_file.open() as f:
      json_result = parse_json(f)
    mydict["_id"]=json_result["_id"]
    mydict["file_name"]=json_result["file_name"]
    mydict["file_type"]=json_result["file_type"]
    mydict["content"]=json_result["content"]

    x = myfile.insert_one(mydict)
    #logging.debug('appending %s',file_name)


def write_result_in_file(write_path , write_content):

    with open(write_path,'w') as f:
        json.dump(write_content,f)
    #logging.debug('writing file conpleted')


def abort_if_file_doesnt_exist(file_id):
    myquery = {"_id": ObjectId(file_id) }
    
    mydoc = myfile.find(myquery)
    if not mydoc:
        abort(404, message="File {} doesn't exist".format(file_id))

# File
# shows a single file item and lets you delete a file item
class File(Resource):
    def get(self, file_id):
        abort_if_file_doesnt_exist(file_id)
        myquery = { "_id": ObjectId(file_id) }
        mydoc = myfile.find(myquery)
        return mydoc

    def delete(self, file_id):
        abort_if_file_doesnt_exist(file_id)
        myquery = { "_id": ObjectId(file_id) }
        myfile.delete_one(myquery)
        os.remove('%s.json'%file_id)
        return '', 204

    def put(self):
        args = parser.parse_args()
        file_js = {
                      'file_name': args['file_name'],
                      'file_type': args['file_type'],
                      'content': args['content']
                  }
        x = myfile.insert_one(file_js)
        file_id = JSONEncoder().encode(x.inserted_id)
        write_result_in_file('%s.json' % eval(file_id), file_js)
        return file_js, 201

# FileList
# shows a list of all FILES, and lets you POST to add new file_names
class FileList(Resource):
    def get(self):
        FILES = []
        for x in myfile.find():
            FILES.append(x)
        return FILES

    def post(self):
        args = parser.parse_args()
        file_js = {
                      'file_name': args['file_name'],
                      'file_type': args['file_type'],
                      'content': args['content']
                  }
        x = myfile.insert_one(file_js)

        file_id = JSONEncoder().encode(x.inserted_id)
        write_result_in_file('%s.json' % eval(file_id), file_js)

        myquery = { "_id": ObjectId(file_id) }
        mydoc = myfile.find(myquery)
        return mydoc, 201

##
## Actually setup the Api resource routing here
##
api.add_resource(FileList, '/files')
api.add_resource(File, '/files/<file_id>')

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/upload', methods=['POST', 'GET'])  # add upload route
def upload():
    if request.method == 'POST':
        f = request.files['file']
 
        if not (f and (is_picture(f.filename) or is_text(f.filename))):
            return jsonify({"error": 1001, "msg": "please check file type，limited to pdf, txt, png, PNG, jpg, JPG, bmp"})

        if (is_picture(f.filename)):
    
            basepath = os.path.dirname(__file__)  # current path
    
            upload_path = os.path.join(basepath, 'static/images', secure_filename(f.filename))  # make sure path exists
            f.save(upload_path)
    
            # Opencv read picture
            img = cv2.imread(upload_path)
            cv2.imwrite(os.path.join(basepath, 'static/images', 'output.jpg'), img)
            img_list = img.tolist()
            file_js = {
                      'file_name': f.filename.rsplit('.', 1)[0],
                      'file_type': "pic",
                      'content': img_list
                  }
            x = myfile.insert_one(file_js)

            file_id = JSONEncoder().encode(x.inserted_id)
            write_result_in_file(basepath+'/static/images/%s.json' % eval(file_id), file_js)
    
            return render_template('upload_pic_ok.html',val1=time.time())
        
        if (is_text(f.filename)):

            basepath = os.path.dirname(__file__)  # current path
            upload_path = os.path.join(basepath, 'static/text', secure_filename(f.filename))  # make sure pwd exists
            f.save(upload_path)
            content = ""

            if(f.filename.rsplit('.', 1)[1]=='pdf'): # process pdf
                pdf_utils = PDFUtils()
                content = pdf_utils.pdf2txt(upload_path)
                ft = open(upload_path.rsplit('.', 1)[0]+".txt",'w')
                ft.write(content)
                ft.close()
                os.remove(upload_path)
            # now we have txt in static/text
            with open(upload_path.rsplit('.', 1)[0]+".txt", "r") as f2:  # 打开文件
                content = f2.read()
            file_js = {
                      'file_name': f.filename.rsplit('.', 1)[0],
                      'file_type': "txt",
                      'content': content
                  }
            x = myfile.insert_one(file_js)
            
            file_id = eval(JSONEncoder().encode(x.inserted_id))
            file_js["_id"] = file_id
            write_result_in_file(basepath+'/static/text/%s.json' % file_id, file_js)

            return render_template('upload_text_ok.html',file_content = content)
 
    return render_template('upload.html')

@app.route('/management', methods=['POST', 'GET'])  # add upload route
def show():
    current_path = os.path.abspath('.')
    text_list = os.listdir(current_path+'/static/text')
    pic_list = os.listdir(current_path+'/static/images')
    return render_template('management.html')

@app.route('/analyse', methods=['POST', 'GET'])  # add upload route
def analyse():
    current_path = os.path.abspath('.')
    text_list = os.listdir(current_path+'/static/text')
    nlp_result = ''
    for file_name in text_list:
        contents = Path(current_path+'/static/text/'+file_name).read_text()
        nlp_result += file_name+'\t'
        nlp_result += "{:.2f}".format(text_nlp(contents))+'\n'
    return render_template('analyse.html',nlp=nlp_result)

if __name__ == '__main__':
    # app.debug = True
    parse_dir('.')
    app.run(host='0.0.0.0', port=80, debug=True)
