from flask_restful import Resource, reqparse
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.order import CustomerOrderModel
from models.product import ProductModel
from models.secondary_tables import ProductOrders

from configs.errors import errors
from configs.constants import STATUS_CODE, SALE_TYPES

from helpers.order_helper import OrderHelper

DB_INSERT_ERROR = errors["DB"]["DB_INSERTION_ERROR"]


class OrderData(Resource):
    @jwt_required()
    def get(self, id):
        order = CustomerOrderModel.find_by_id(id)
        if order:
            return {"status": True, "order": order.json()}, 200
        return {"status": False, "message": "No such order exists"}, 200


class Order(Resource):
    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument(
        "customer_id", type=int, required=True, help="Customer id is required"
    )
    parser.add_argument(
        "store_id", type=int, required=True, help="store id is required"
    )
    parser.add_argument(
        "sale_type", type=str, required=True, help="Sale type is required"
    )
    parser.add_argument(
        "products", type=dict, required=True, help="Products cant be ordered if invalid"
    )

    @jwt_required()
    def post(self):
        # data = Order.parser.parse_args()
        data = request.get_json()
        # print(data)
        # TODO:
        # Each item in the producs should be unique, if required more of same item specify quantity.

        user_id = get_jwt_identity()
        # customer_id check
        customer_id = data.get("customer_id", None)
        if not customer_id:
            return {"status": False, "message": "customer id cant be empty"}, 400

        # store id check
        store_id = data.get("store_id", None)
        if not store_id:
            return {"status": False, "message": "store id cant be empty"}, 400

        # products check
        products = data.get("products")
        if products is None or len(products) == 0:
            return {"status": False, "message": "Invalid items in the order"}, 400

        # sale_type check
        sale_type = data.get("sale_type", None)
        if sale_type not in SALE_TYPES:
            return {
                "status": False,
                "message": f"sale type should be one of {', '.join(SALE_TYPES)}",
            }, 400
        if sale_type == "custom":
            return {
                "suggestion": "Its in the bucket list ..!, enjoy a quick breath while we develop it",
                "message": "In the request body add the `custom price` as well, along the item body",
            }, 400
        # TODO - Do we need saletype for every order item, looks like it can come in handy
        #      - when the a complete sale is either retail or wholesale,
        #        but a couple of items in the order are of type custom, with custom price for them
        status = False
        order_help_obj = OrderHelper(products, user_id=user_id, store_id=store_id)
        order_valid, response_products = order_help_obj.is_order_valid()
        print("order_valid", order_valid)

        if order_valid:  # TODO
            try:
                # TODO updating and calculating the order. Change it not recommended

                # add an entry in order
                order_amount, order_list = order_help_obj.calculate_order_amount(sale_type)

                p = CustomerOrderModel(
                    customer_id=customer_id,
                    store_id=store_id,
                    sale_type=sale_type,
                    status=STATUS_CODE["PENDING"],
                    amount=order_amount,
                )
                for order_item in order_list:
                    # create parent, append a child via association
                    a = ProductOrders(
                        price=order_item["price"], quantity=order_item["quantity"]
                    )
                    a.product = order_item["product"]
                    p.products.append(a)

                p.save_to_db()
                # update quantity in db
                update_status = order_help_obj.update_items()
                print("update status", update_status)
                if not update_status:
                    # return DB_INSERT_ERROR["RESPONSE"], DB_INSERT_ERROR['STATUS_CODE']
                    return {
                        "status": status,
                        "message": "cant update the quantity in db",
                    }
                status = True
                return {"status": status, "order_id": p.id, "amount": order_amount}, 200

            except Exception as error:
                return DB_INSERT_ERROR["RESPONSE"], DB_INSERT_ERROR["STATUS_CODE"]
        return {"status": status, "products": response_products}, 400

    @jwt_required()
    def put(self):
        """
        To update the status of order, if amount is received successfully.
        """

        data = request.get_json()
        order_id = data.get("order_id", None)
        order_status = data.get("status", None)
        # order of the current customer
        customer_order = CustomerOrderModel.find_by_id(order_id)
        return_status = False
        message = "Unable to update status of order"

        if customer_order and order_status:
            return_status = True
            message = "order status updated successfully"
            customer_order.status = STATUS_CODE["SUCCESS"]
            customer_order.save_to_db()

        return {"status": return_status, "message": message}, 200
