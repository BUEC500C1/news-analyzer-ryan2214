from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from pathlib import Path
import json
import logging

app = Flask(__name__)
api = Api(app)

##FILES = {
##    'file1': {'file_name': 'cool news'},
##    'file2': {'file_name': '?????'},
##    'file3': {'file_name': 'super cool news!'},
##}

FILES = {
    'files/file1': {
                      'file_name': 'cool news',
                      'text':'a cool story.'
    }
}

def refresh_files_with_local_json(root_dir):
    FILES = {}

    path = Path(root_dir)
    all_json_file = list(path.glob('*.json'))

    for json_file in all_json_file:
        file_name = json_file.parent.stem
        with json_file.open() as f:
            json_result = json.load(f)

        file_obj = {file_name:json_result}
        FILES.append(file_obj)

def write_result_in_file(write_path , write_content):

    with open(write_path,'w') as f:
        json.dump(write_content,f)
    logging.debug('writing file conpleted')


def abort_if_file_doesnt_exist(file_id):
    if file_id not in FILES:
        abort(404, message="File {} doesn't exist".format(file_id))

parser = reqparse.RequestParser()
parser.add_argument('file_name')
parser.add_argument('text')

# File
# shows a single file item and lets you delete a file item
class File(Resource):
    def get(self, file_id):
        abort_if_file_doesnt_exist(file_id)
        return FILES[file_id]

    def delete(self, file_id):
        abort_if_file_doesnt_exist(file_id)
        del FILES[file_id]
        return '', 204

    def put(self, file_id):
        args = parser.parse_args()
        file_name = {'file_name': args['file_name']}
        FILES[file_id] = file_name
        return file_name, 201


# FileList
# shows a list of all FILES, and lets you POST to add new file_names
class FileList(Resource):
    def get(self):
        return FILES

    def post(self):
        args = parser.parse_args()
        file_id = int(max(FILES.keys()).lstrip('files/file')) + 1
        file_id = 'files/file%i' % file_id
        FILES[file_id] = {
                              'file_name': args['file_name'],
                              'text': args['text']
                          }
        return FILES[file_id], 201

##
## Actually setup the Api resource routing here
##
api.add_resource(FileList, '/files')
api.add_resource(File, '/files/<file_id>')
refresh_files_with_local_json(".")

if __name__ == '__main__':
    app.run(debug=True)
## host = 'XX.XX.XX.XX' ,port = 5000, debug = 'True'
## accroding to EC2 public IP