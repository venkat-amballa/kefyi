from flask_restful import Resource, reqparse
from flask import request
from models.customer import CustomerModel


class CustomerOrders(Resource):
    def get(self, cid):
        orders = CustomerModel.orders(cid)
        if orders:
            return {"status": True, "bills": [order.json() for order in orders]}, 200
        return {"status": True, "bills": []}, 200


class Customer(Resource):
    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument("first_name", type=str, required=True, help="First is required")
    parser.add_argument(
        "last_name", type=str, required=True, help="Last number is required"
    )
    parser.add_argument("address", type=str, required=True, help="Address is required")
    parser.add_argument("email", type=str, required=True, help="Email is required")
    parser.add_argument(
        "mobile", type=str, required=True, help="Mobile number is required"
    )

    def post(self):
        # data = Customer.parser.parse_args()
        data = request.get_json()
        mobile = data.get("mobile", None)
        if mobile is None:
            return {"status": False,
                    "error_code": "REQUIRED_FIELD",
                    "message": "mobile number is a required field"
                    }, 400
        # TODO - use marshmallow to check the data validity
        try:
            if CustomerModel.find_by_mobile(data["mobile"]):
                return {"status": False,
                        "error_code": "DUPLICATE_USER",
                        "message": "Registered already, kindly update details if needed"
                        }, 400
            customer = CustomerModel(**data)
            customer.save_to_db()
            return {"status": True, "message": "Registered Successfully!"}, 200

        except Exception as e:
            print(e)
            return {
                "status": False,
                "message": "DB ERROR, inserting into customer table failed",
            }, 500

    def get(self):
        args = request.args
        mobile = args.get("mobile", None)
        cid = args.get("id", None)

        if mobile:
            customer = CustomerModel.find_by_mobile(mobile)
        elif cid:
            customer = CustomerModel.find_by_id(cid)
        else:
            return {"status": False,
                    "error_code": "MISSING_QUERY_PARAMS",
                    "message": "customer id or mobile needs to be passed as query params",
                    }, 400
        if customer:
            return {"status": True, "customer": customer.json()}, 200

        return {"status": False,
                "error_code": "INVALID_ID_OR_MOBILE",
                "message": "No customer with the id or mobile"
                }, 404

    def put(self):
        args = request.args
        mobile = args.get("mobile", None)
        cid = args.get("id", None)

        if mobile:
            customer = CustomerModel.find_by_mobile(mobile)
        elif cid:
            customer = CustomerModel.find_by_id(cid)
        else:
            return {"status": False,
                    "error_code": "MISSING_QUERY_PARAMS",
                    "message": "customer id or mobile needs to be passed as query params",
                    }, 400
        if customer:
            return {"status": True, "customer": customer.json()}, 200

        return {"status": False,
                "error_code": "INVALID_ID_OR_MOBILE",
                "message": "No customer with the id or mobile"
                }, 404
