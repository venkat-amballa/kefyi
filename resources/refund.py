from flask_restful import Resource
from flask_jwt_extended import jwt_required,get_jwt_identity

class OrderRefund(Resource):
    @jwt_required()
    def post(self):
        pass

