from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

FILES = {
    'file1': {'file_name': 'cool news'},
    'file2': {'file_name': '?????'},
    'file3': {'file_name': 'super cool news!'},
}


def abort_if_file_doesnt_exist(file_id):
    if file_id not in FILES:
        abort(404, message="File {} doesn't exist".format(file_id))

parser = reqparse.RequestParser()
parser.add_argument('file_name')


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
        file_id = int(max(FILES.keys()).lstrip('file')) + 1
        file_id = 'file%i' % file_id
        FILES[file_id] = {'file_name': args['file_name']}
        return FILES[file_id], 201

##
## Actually setup the Api resource routing here
##
api.add_resource(FileList, '/files')
api.add_resource(File, '/files/<file_id>')


if __name__ == '__main__':
    app.run(debug=True)
