# coding:utf-8
 
from flask import Flask, render_template, request, redirect, url_for, make_response,jsonify
from werkzeug.utils import secure_filename
import os
import cv2
import time
 
from datetime import timedelta
 
# set file type permitted
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
 
app = Flask(__name__)
# set static outdate time
app.send_file_max_age_default = timedelta(seconds=1)
 
 
# @app.route('/upload', methods=['POST', 'GET'])
@app.route('/upload', methods=['POST', 'GET'])  # add upload route
def upload():
    if request.method == 'POST':
        f = request.files['file']
 
        if not (f and allowed_file(f.filename)):
            return jsonify({"error": 1001, "msg": "please check file type，limited to png, PNG, jpg, JPG, bmp"})
 
        user_input = request.form.get("name")
 
        basepath = os.path.dirname(__file__)  # current path
 
        upload_path = os.path.join(basepath, 'static/images', secure_filename(f.filename))  # make sure pwd exists
        f.save(upload_path)
 
        # Opencv read picture
        img = cv2.imread(upload_path)
        cv2.imwrite(os.path.join(basepath, 'static/images', 'test.jpg'), img)
 
        return render_template('upload_ok.html',userinput=user_input,val1=time.time())
 
    return render_template('upload.html')
 
 
if __name__ == '__main__':
    # app.debug = True
    app.run(host='0.0.0.0', port=8987, debug=True)
