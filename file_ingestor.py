# coding:utf-8
 
from flask import Flask, render_template, request, redirect, url_for, make_response,jsonify
from flask_restful import reqparse, abort, Api, Resource
from werkzeug.utils import secure_filename
from pathlib import Path
from file_upload.pdf_parse import *
import json
import logging
import base64
import os
import cv2
import time
 
from datetime import timedelta
 
# set file type permitted
ALLOWED_PICTURE_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp'])
ALLOWED_TEXT_EXTENSIONS = set(['pdf', 'txt'])
 
def is_picture(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_PICTURE_EXTENSIONS

def is_text(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_TEXT_EXTENSIONS
 
app = Flask(__name__)
api = Api(app)

# set static outdate time
app.send_file_max_age_default = timedelta(seconds=1)
 


##FILES = {
##    'file1': {'file_name': 'cool news'},
##    'file2': {'file_name': '?????'},
##    'file3': {'file_name': 'super cool news!'},
##}

FILES = {}

parser = reqparse.RequestParser()
parser.add_argument('file_name')
parser.add_argument('file_type')  # text, jpg
parser.add_argument('text')

def refresh_files_with_local_json(root_dir):
    
    path = Path(root_dir)

    all_json_file = list(path.glob('**/*.json'))
    
    for json_file in all_json_file:

        with json_file.open() as f:
            json_result = json.load(f)
        file_name = str(json_file.stem)
        FILES[file_name] = json_result
        #logging.debug('appending %s',file_name)


def write_result_in_file(write_path , write_content):

    with open(write_path,'w') as f:
        json.dump(write_content,f)
    #logging.debug('writing file conpleted')


def abort_if_file_doesnt_exist(file_id):
    if file_id not in FILES:
        abort(404, message="File {} doesn't exist".format(file_id))

# File
# shows a single file item and lets you delete a file item
class File(Resource):
    def get(self, file_id):
        abort_if_file_doesnt_exist(file_id)
        return FILES[file_id]

    def delete(self, file_id):
        abort_if_file_doesnt_exist(file_id)
        del FILES[file_id]
        os.remove('%s.json'%file_id)
        return '', 204

    def put(self, file_id):
        args = parser.parse_args()
        file_js = {
                      'file_name': args['file_name'],
                      'text': args['text']
                  }
        FILES[file_id] = file_js
        return file_js, 201

# FileList
# shows a list of all FILES, and lets you POST to add new file_names
class FileList(Resource):
    def get(self):
        return FILES

    def post(self):
        args = parser.parse_args()
        file_js = {
                      'file_name': args['file_name'],
                      'text': args['text']
                  }

        file_id = int(max(FILES.keys()).lstrip('file')) + 1
        write_result_in_file('file%i.json' % file_id, file_js)

        file_id = 'file%i' % file_id
        FILES[file_id] = file_js

        return FILES[file_id], 201

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
    
            return render_template('upload_pic_ok.html',val1=time.time())
        
        if (is_text(f.filename)):

            basepath = os.path.dirname(__file__)  # current path
            upload_path = os.path.join(basepath, 'static/text', secure_filename(f.filename))  # make sure pwd exists
            f.save(upload_path)

            if(f.filename.rsplit('.', 1)[1]=='pdf'): # process pdf
                pdf_utils = PDFUtils()
                content = pdf_utils.pdf2txt(upload_path)
                print(f.filename)
                ft = open(upload_path.rsplit('.', 1)[0]+".txt",'w')
                ft.write(content)
                ft.close()
                os.remove(upload_path)
                return render_template('upload_text_ok.html',file_content = content)
 
    return render_template('upload.html')

@app.route('/management', methods=['POST', 'GET'])  # add upload route
def show():
    current_path = os.path.abspath('.')
    text_list = os.listdir(current_path+'/static/text')
    pic_list = os.listdir(current_path+'/static/images')
    return render_template('management.html')

if __name__ == '__main__':
    # app.debug = True
    refresh_files_with_local_json('.')
    app.run(host='0.0.0.0', port=80, debug=True)
