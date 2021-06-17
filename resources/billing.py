from flask_restful import Resource, reqparse
from flask import request

from models.billing import BillingHelper

from configs.errors import errors

DB_INSERT_ERROR = errors["DB"]["DB_INSERTION_ERROR"]

class Billing(Resource):
    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument("customer_id", type=int, required=True, help="Customer id is required")
    parser.add_argument("sale_type", type=int, required=True, help="Customer id is required")
    parser.add_argument("products", type=dict, required=True, help="Products cant be billed if invalid")

    def post(self):
        # data = Billing.parser.parse_args()
        data = request.get_json()
        # print(data)
        # TODO:
        # Each item in the producs should be unique, if required more of same item specify quantity.

        products = data.get('products')
        sale_type = ["wholesale", "retail", "custom"]
        if products is None:
            return {"status":False, "message":"Invalid items in the billing"}, 404
        
        res = None
        status = False

        order_valid, product_items = BillingHelper.is_order_valid(products)
        print("order_valid", order_valid)
        if order_valid: # TODO
            # try:
                # TODO updating and calculating the bill. Change it not recommended
                # res, bill_amount = BillingHelper.update_items(products)
            res, bill_amount = BillingHelper.calculate_bill(products)
            status = True
            # except Exception as error:
            #     # print(str(error.orig) + " for parameters" + str(error.params))
            #     return DB_INSERT_ERROR["RESPONSE"], DB_INSERT_ERROR['STATUS_CODE']
        else:
            return {"status":status, "products":product_items}, 400
        return {"status":status, "amount":bill_amount, "data":res}, 200