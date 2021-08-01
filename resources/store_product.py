from models.product import ProductModel
from models.store import StoreModel

from resources.store import Store
from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity

from models.store import StoreModel

class StoreProduct(Resource):
    def get(self,s_id, p_id):
        # store = StoreModel.query.filter(StoreModel.id == s_id).filter(StoreModel.products.any(id=p_id)).first()
        product = ProductModel.find_in_store(s_id, p_id)
        if product:
            product = product.json()
        else:
            product = None
        return {"status":True, "store_id":s_id, "product_id":p_id, "product":product}, 200

    @jwt_required(fresh=True)
    def put(self, s_id, p_id):
        # JWT required
        data = request.get_json()
        product = ProductModel.find_in_store(s_id, p_id)
        if not product:
            return {"status": False,
                    "error_code": "PRODUCT_NOT_DOUND",
                    "message": "No product with the given id, to update"
                    }, 400

        # TODO
        # PUT method doesnot support any product creation, if there is no product with given id, returns an error.
        # else:
        #     product = ProductModel(name, **data)
        try:
            product.name = data.get("name", product.name)
            product.actual_price = data.get("actual_price", product.actual_price)
            product.wholesale_price = data.get("wholesale_price", product.wholesale_price)
            product.retail_price = data.get("retail_price", product.retail_price)
            product.quantity = data.get("quantity", product.quantity)
            product.category = data.get("category", product.category)

            product.save_to_db()
        except Exception as error:
            error_dict = errors['DB']['DB_INSERTION_ERROR']
            return error_dict['RESPONSE'], error_dict['STATUS_CODE']

        return {"status": True, "message": "Product update successfull"}, 200


class StoreProducts(Resource):
    @jwt_required()
    def get(self, s_id):
        products = ProductModel.find_all(s_id)
        product_list = []
        if products:
            product_list = [p.json() for p in products]
        return {"status":True, "store_id":s_id, "products":product_list}, 200

    @jwt_required()
    def post(self, s_id):
        product = request.get_json()
        # JWT required
        # TODO:
        # Find wherther the user has access to this store, only allow if he does.
        data = request.get_json()
        # data = Product.parser_product.parse_args()
        name = data.get("name", None)
        if name is None:
            return {"status": False, "error_code": "PRODUCT_NAME_REQUIRED", "message": "Product name is required"}, 400

        store = StoreModel.find_by_id(s_id)
        if not store:
            return {"status": False, "error_code": "INVALID_STORE", "message": "No store with the given id"}, 400
        # check the user access to the store.

        if ProductModel.find_by_name(name):
            return {"status": False, "error_code": "PRODUCT_NAME_DUPLICATE",
                    "message": "There exists an Product with the same name"}, 400

        product = ProductModel(**data)

        # saving only in store.products is enough and product.save_to_db() isn't needed.
        store.products.append(product)
        try:
            store.save_to_db()   # save the store after adding the product.
        except Exception as e:
            return {
                "status": False,
                "error_code":"DB_INSERTION_ERROR",
                "message": "Some Error Occured while inserting the data. (Insertion into product or store db failed)"
                }, 400

        return {"status":True, "message":"Insertion of the product is successfull"}, 201

