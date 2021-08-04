from flask_restful import Resource
from flask import request

class Image(Resource):
    def post(self):
        print(request.files)
        return {"message": request.files['image'].name}, 200