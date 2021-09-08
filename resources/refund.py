from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request

from models.order import CustomerOrderModel
from models.product import ProductModel
from models.refund import RefundsModel
from models.secondary_tables import ProductRefundAssociation

from configs.constants import SALE_STATUS_CODE

"""
1. not paid : "P",
2. Paid: "S", partial : decide based on amount.
3. "R": 
"""


def is_valid(ordered_products, refund_item_dict):
    """
    :returns:
        - refund_valid: True if refund is valid, else invalid
        - refund_amount: amount to be  refunded, based on return items
        - refund_items: list of all the items requested for refund
    """
    refund_amount = 0
    refund_valid = True

    for order_product in ordered_products:
        refund_item = refund_item_dict.get(order_product.product_id, None)
        if refund_item and refund_item["quantity"] < order_product.quantity:
            refund_item["status"] = True
            refund_item["price"] = order_product.price
            refund_amount += order_product.price * refund_item["quantity"]
        refund_valid &= refund_item["status"]
    refund_items = list(refund_item_dict.values())
    return refund_valid, refund_amount, refund_items


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

        customer_id = data.get("customer_id", None)
        store_id = data.get("store_id", None)
        refund_products = data.get("products", None)

        order = CustomerOrderModel.find_by_id(order_id)
        if not order:
            return {"status": False,
                    "error_code": "INVALID_ORDER",
                    "message": "no such order exists"
                    }, 404
        if order.status == SALE_STATUS_CODE["REFUND"]:
            return {"status": False,
                    "error_code": "ORDER_STATUS_REFUND",
                    "message": "Order is refunded already, cant refund twice"
                    }, 400
        if order.status != SALE_STATUS_CODE["PAID"]:
            return {"status": False,
                    "error_code": "ORDER_STATUS_NOT_PAID",
                    "message": "status of the order should be paid, to process the refund"
                    }, 400
        if order.customer_id != customer_id:
            return {"status": False,
                    "error_code": "CUSTOMER_ORDER_MISMATCH",
                    "message": "ordered customer is different than the one provide"
                    }, 400
        refund_item_dict = {_product["id"]: {**_product, **{"status": False}} for _product in refund_products}
        product_ids = refund_item_dict.keys()
        ordered_products = CustomerOrderModel.products_in_order(order_id, product_ids)
        if len(ordered_products) < 1:
            return {"status": False,
                    "error_code": "ORDER_EMPTY",
                    "message": "order has no items in it"
                    }, 400
        refund_valid, amount, response_list = is_valid(ordered_products, refund_item_dict)
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
            for refund_item in response_list:
                product_id = refund_item["id"]
                product_quantity = refund_item["quantity"]
                price = refund_item["price"]
                product = ProductModel.find_by_id(user_id, store_id, product_id)
                # update the refund quantity in inventory
                product.quantity += product_quantity
                a = ProductRefundAssociation(
                    price=price,
                    quantity=product_quantity,
                )
                a.product = product
                refund.return_items.append(a)
                product.save_to_db()
            # update the status of the order to refund
            order.status = SALE_STATUS_CODE['REFUND']
            order.save_to_db()
            refund.save_to_db()
        except Exception as e:
            print(e)
            return {"status": False,
                    "error_code": "DB_INSERTION_ERROR",
                    "message": "Error while inserting data into database"
                    }, 500
        return {"status": True, "amount": amount, "data": response_list}, 200
