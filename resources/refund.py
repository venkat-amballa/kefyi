from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request

from models.order import CustomerOrderModel


class OrderRefund(Resource):
    @jwt_required()
    def post(self):
        """
        1. Find the order
        2.
        """
        data = request.get_json()

        order_id = data.get("order_id", None)
        customer_id = data.get("customer_id", None)
        return_products = data.get("products", None)
        returns_dict = {_product["id"]: _product for _product in return_products}

        product_ids = return_products.keys()
        ordered_products = CustomerOrderModel.products_in_order(order_id, product_ids)
        for _product in ordered_products:
            return_item = returns_dict.get(_product.id, None)
            if return_item:
                """
                1. not paid : "P",
                2. Paid: "S", partial : decide based on amount.
                3. "R": 
                """
        return {"status": True, "data": [op.json() for op in ordered_products]}
