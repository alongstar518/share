import os
import shutil

from flask import Flask
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('string', type=str, default=False, required=True)

to_delete = [
    "userdata-qemu.img",
    "snapshots"
]


def _clean_android_user_data(avd_name):
    avd_folder_path = os.path.expanduser("~/.android/avd")
    avd_folder_path = os.path.join(avd_folder_path, f"{avd_name}.avd")
    for target in to_delete:
        file_path = os.path.join(avd_folder_path, target)
        if os.path.exists(file_path):
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path, ignore_errors=True)


class Clean(Resource):
    def get(self):
        args = parser.parse_args()
        avd_name = args['avd_name']
        _clean_android_user_data(avd_name)
        return 'Sucess'


api.add_resource(Clean, '/clean')

if __name__ == '__main__':
    app.run(debug=True, port=8000, host='0.0.0.0')
