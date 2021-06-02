from flask_restful import Resource, reqparse

from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity

from models.store import StoreModel

_store_parser = reqparse.RequestParser(bundle_errors=True)
_store_parser.add_argument("name", type=str, required=True, help="{error_msg}")
_store_parser.add_argument("address", type=str, required=True, help="{error_msg}")
_store_parser.add_argument("contact", type=str, required=True, help="{error_msg}")
# _store_parser.add_argument("user_id", type=str, required=True, help="{error_msg}")


class StoreList(Resource):
    def get(self):
        stores = StoreModel.find_all()
        # print('stores:', StoreModel.query.all())
        if stores:
            # print('stores -------------------:', stores[0].json())
            return {"stores": [store.json() for store in stores]}, 200
        return {"message": "No stores Found"}, 404
    
    @jwt_required()
    def post(self):
        id = get_jwt_identity()
        # TODO:
        #  1. check whether this user has necessary access to change something in the store.

        print("jwt identity:", id)
        data = _store_parser.parse_args()
        store = StoreModel(user_id=id, **data)
        if store.find_by_name(store.name):
            return {
                "message": "A store exists with the name",
                "error": "duplicate_record_insert"
                }, 400

        store.save_to_db()
        return {"msg": store.json()}, 201


class Store(Resource):

    def get(self, id):
        store = StoreModel.find_by_id(id)
        print(store.name)
        if store:
            return store.json(), 200
        return {"message": "Store Not Found"}, 404

    
    def patch(self, id):
        return {"msg": "patch method response"}
    
    def delete(self, id):
        return {"message": "delete response"}
