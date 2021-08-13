from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request

from models.order import CustomerOrderModel
from models.product import ProductModel
from models.refund import RefundsModel
from models.secondary_tables import ProductRefundAssociation

"""
1. not paid : "P",
2. Paid: "S", partial : decide based on amount.
3. "R": 
"""


def is_valid(return_products, order_id=None):
    refund_item_dict = {_product["id"]: {**_product, **{"status": False}} for _product in return_products}
    product_ids = refund_item_dict.keys()
    ordered_products = CustomerOrderModel.products_in_order(order_id, product_ids)
    refund_amount = 0
    refund_valid = True
    for order_product in ordered_products:
        refund_item = refund_item_dict.get(order_product.product_id, None)
        if refund_item and refund_item["quantity"] < order_product.quantity:
            refund_item["status"] = True
            refund_item["price"] = order_product.price
            refund_amount += order_product.price * refund_item["quantity"]
        else:
            refund_valid = False

    return refund_valid, refund_amount, list(refund_item_dict.values())


class OrderRefund(Resource):
    @jwt_required()
    def post(self, order_id):
        """
        1. find all the refund products in the order
        2. check with the quantity, if not less status=False, else true
        3. If all status are true:
        4. Insert the records
        """
        data = request.get_json()
        user_id = get_jwt_identity()

        # order_id = data.get("order_id", None)
        customer_id = data.get("customer_id", None)
        store_id = data.get("store_id", None)
        refund_products = data.get("products", None)

        refund_valid, amount, response_list = is_valid(refund_products, order_id=order_id)
        if not refund_valid:
            return {"status": False,
                    "ERROR_CODE": "INVALID_REFUND",
                    "message": "Invalid Refund Request",
                    "products": response_list
                    }, 400

        # 2. calculate amount to be given back, including any special promotions
        # 3.
        try:
            refund = RefundsModel(
                order_id=order_id,
                amount=amount
              )
            for order_item in response_list:
                product_id = order_item["id"]
                product_quantity = order_item["quantity"]
                price = order_item["price"]
                product = ProductModel.find_by_id(user_id, store_id, product_id)

                a = ProductRefundAssociation(
                    price=price,
                    quantity=product_quantity,
                )
                a.product = product
                refund.return_items.append(a)
            refund.save_to_db()
        except Exception as e:
            return {"status": False,
                    "error_code": "DB_INSERTION_ERROR",
                    "message": "Error while inserting data into database"
                    }, 500
        return {"status": True, "amount": amount, "data": response_list}, 200
