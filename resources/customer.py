from flask_restful import Resource, reqparse
from flask import request
from models.cutomer import CustomerModel

class Customer(Resource):
    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument("first_name", type=str, required=True, help="First is required")
    parser.add_argument("last_name", type=str, required=True, help="Last number is required")
    parser.add_argument("address", type=str, required=True, help="Address is required")
    parser.add_argument("email", type=str, required=True, help="Email is required")
    parser.add_argument("mobile", type=str, required=True, help="Mobile number is required")

    def post(self):
        data = Customer.parser.parse_args()
        if data:
            try:
                if CustomerModel.find_by_email(data['email']):
                    return {"status":True, "message":"Registered already"}, 400
                customer = CustomerModel(**data)
                customer.save_to_db()
            except Exception as e:
                return {"status":False, "message":"DB ERROR, inserting into customer table failed"},500
            return {"status":True, "message":"Registered Successfully!"}, 200

        return {"status":False, "message":"Invalid Request"}, 400

    def get(self):
        # data = request.
        return {"status":False, "message":"Not implemented, yet..!"}, 500