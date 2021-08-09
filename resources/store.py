from flask_restful import Resource, reqparse

from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity

from models.store import StoreModel
from models.order import CustomerOrderModel

_store_parser = reqparse.RequestParser(bundle_errors=True)
_store_parser.add_argument("name", type=str, required=True, help="{error_msg}")
_store_parser.add_argument("address", type=str, required=True, help="{error_msg}")
_store_parser.add_argument("contact", type=str, required=True, help="{error_msg}")
# _store_parser.add_argument("user_id", type=str, required=True, help="{error_msg}")

ERROR_CODES = {
    "STORE_NOT_FOUND": "STORE_NOT_FOUND",
}

ERROR_MSGS = {
    "STORE_NOT_FOUND": "No such store exist",
}

class StoreOrders(Resource):
    @jwt_required()
    def get(self, store_id):
        user_id = get_jwt_identity()
        orders = StoreModel.store_orders(user_id, store_id)
        if isinstance(orders, list):
            return {"status": True, "orders": [order.json() for order in orders]}, 200
        return {"status": False,
                "error_code": ERROR_CODES["STORE_NOT_FOUND"],
                "message": ERROR_MSGS["STORE_NOT_FOUND"]
                }, 200


class StoreList(Resource):
    @jwt_required()
    def get(self):
        """
        Returns all the stores of a particular user
        """
        uid = get_jwt_identity()
        stores = StoreModel.find_by_user_id(uid)
        # print('stores:', StoreModel.query.all())
        if stores:
            return {"status": True, "stores": [store.json() for store in stores]}, 200
        return {
            "status": True,
            "stores": [],
            "message": "No stores available, kindly add one",
        }, 404

    @jwt_required()
    def post(self):
        """
        Add a store to particular user
        """
        id = get_jwt_identity()
        # TODO:
        #  1. check whether this user has necessary access to change something in the store.

        data = _store_parser.parse_args()
        store = StoreModel.find_by_name(id, data.get("name", None))
        if store:
            return {
                "status": False,
                "message": "A store exists with the name",
                "error": "duplicate_record_insert",
            }, 400
        try:
            store = StoreModel(user_id=id, **data)
            store.save_to_db()
        except Exception as e:
            # TODO - LOGGER TO SAVE ERROR INFO
            return {
                "status": False,
                "message": "Exception while inserting data",
                "error": "DB_INSERTION_ERROR",
            }
        return {"status": True, "stores": [store.json()]}, 201


class Store(Resource):
    @jwt_required()
    def get(self, id):
        """
        GET method, to get the complete product list of a store.
        """
        user_id = get_jwt_identity()
        store = StoreModel.find_by_id(user_id, id)
        if store:
            return store.json(), 200
        return {"status": False, "message": "Store Not Found"}, 404

    def put(self, id):
        return {"status": False, "message": "not implemented, put"}

    def delete(self, id):
        return {"status": False, "message": "not implemented, delete"}
