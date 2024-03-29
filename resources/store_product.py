import utils
from configs.constants import MAX_PER_PAGE
from models.product import ProductModel
from models.store import StoreModel

from resources.store import Store
from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity

from sqlalchemy.exc import SQLAlchemyError, DBAPIError

from models.store import StoreModel

from utils import str_to_bool

ERROR_CODES = {
    "DB_INSERTION_ERROR": "DB_INSERTION_ERROR",
    "PRODUCT_NOT_FOUND": "PRODUCT_NOT_FOUND",
    "PRODUCT_NAME_REQUIRED": "PRODUCT_NAME_REQUIRED",
    "PRODUCT_NAME_DUPLICATE": "PRODUCT_NAME_DUPLICATE",
    "INVALID_STORE": "INVALID_STORE",
    "EMPTY_STORE": "EMPTY_STORE",
    "PRODUCT_DATA_MISSING": "PRODUCT_DATA_MISSING",
}

ERROR_MSG = {
    "DB_INSERTION_ERROR": "Some Error Occured while inserting the data",
    "PRODUCT_NOT_FOUND": "No such Product found in your store",
    "PRODUCT_NAME_REQUIRED": "Product name is required",
    "PRODUCT_NAME_DUPLICATE": "There exists a product with the same name",
    "INVALID_STORE": "No such store for the user",
    "EMPTY_STORE": "No products in a store",
    "PRODUCT_DATA_MISSING": "Product data is missing",
}


class StoreProduct(Resource):
    @jwt_required()
    def get(self, sid, pid):
        # store = StoreModel.query.filter(StoreModel.id == s_id).filter(StoreModel.products.any(id=p_id)).first()
        user_id = get_jwt_identity()
        product = ProductModel.find_in_user_store_by_barcode_or_id(user_id, sid, pid)
        if not product:
            return {
                "status": False,
                "store_id": sid,
                "_id": pid,
                "error_code": ERROR_CODES["PRODUCT_NOT_FOUND"],
                "message": ERROR_MSG["PRODUCT_NOT_FOUND"],
            }, 200
        return {
            "status": True,
            "product": product.json(),
        }, 200

    @jwt_required(fresh=True)
    def put(self, sid, pid):
        # JWT required
        data = request.get_json()
        user_id = get_jwt_identity()
        product = ProductModel.find_in_user_store(user_id, sid, pid)
        if not product:
            return {
                "status": False,
                "error_code": ERROR_CODES["PRODUCT_NOT_FOUND"],
                "message": ERROR_MSG["PRODUCT_NOT_FOUND"],
            }, 400

        # TODO
        # 1. PUT method does not support any product creation, if there is no product with given id, returns an error.
        # 2. Image Url update, not supported.
        try:
            product.name = data.get("name", product.name)
            product.actual_price = data.get("actual_price", product.actual_price)
            product.wholesale_price = data.get(
                "wholesale_price", product.wholesale_price
            )
            product.retail_price = data.get("retail_price", product.retail_price)
            product.quantity = data.get("quantity", product.quantity)
            product.category = data.get("category", product.category)
            product.loose = data.get("loose", product.loose)
            product.enable = data.get("enable", product.enable)
            product.barcode = data.get("barcode", product.barcode)
            product.unit = data.get("unit", product.unit)
            product.save_to_db()
            return {"status": True, "product": product.json()}, 200
        except (SQLAlchemyError, DBAPIError) as e:
            print(e)
            return {
                "status": False,
                "error_code": ERROR_CODES["DB_INSERTION_ERROR"],
                "message": ERROR_MSG["DB_INSERTION_ERROR"],
            }, 400


class StoreProducts(Resource):
    @jwt_required()
    def get(self, sid):
        """get store products"""
        user_id = get_jwt_identity()
        product_name_search = request.args.get("name", None)
        enable = str_to_bool(request.args.get("enable", None))

        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', MAX_PER_PAGE))

        if product_name_search:
            similar_products_page = ProductModel.find_similar(user_id, sid, product_name_search, page, per_page, enable)
            return {
                "status": True,
                "products": [prod.json() for prod in similar_products_page.items],
                **utils.page_footer_json(similar_products_page),
            }

        store = StoreModel.find_by_id(user_id, sid)

        if not store:
            return {"status": False, "store_id": sid,
                    "error_code": ERROR_CODES["INVALID_STORE"],
                    "message": ERROR_MSG["INVALID_STORE"],
                    }, 200
        products = StoreModel.store_products(user_id, sid, page, per_page, enable)
        if isinstance(products.items, list):
            product_list = [p.json() for p in products.items]
            return {"status": True,
                    "store_id": sid,
                    "products": product_list,
                    **utils.page_footer_json(products),
                    }, 200
        return {"status": False, "store_id": sid,
                "error_code": ERROR_CODES["EMPTY_STORE"],
                "message": ERROR_MSG["EMPTY_STORE"],
                }, 200

    @jwt_required()
    def post(self, sid):
        # TODO:
        # Find whether the user has access to this store, only allow if he does.
        data = request.get_json()
        user_id = get_jwt_identity()
        # data = Product.parser_product.parse_args()
        name = data.get("name", None)
        if name is None:
            return {
                "status": False,
                "error_code": ERROR_CODES["PRODUCT_NAME_REQUIRED"],
                "message": ERROR_MSG["PRODUCT_NAME_REQUIRED"],
            }, 400

        # check the user access to the store.
        store = StoreModel.find_by_id(user_id, sid)
        if not store:
            return {
                "status": False,
                "error_code": ERROR_CODES["INVALID_STORE"],
                "message": ERROR_MSG["INVALID_STORE"],
            }, 400

        if ProductModel.find_by_name(user_id, sid, name):
            return {
                "status": False,
                "error_code": ERROR_CODES["PRODUCT_NAME_DUPLICATE"],
                "message": ERROR_MSG["PRODUCT_NAME_DUPLICATE"],
            }, 400
        try:
            product = ProductModel(
                name=data.get("name"),
                url=data.get("url", None),
                category=data.get("category"),
                description=data.get("description", None),
                brand=data.get("brand"),
                unit=data.get("unit"),
                actual_price=data.get("actual_price"),
                wholesale_price=data.get("wholesale_price"),
                retail_price=data.get("retail_price"),
                quantity=data.get("quantity"),
                barcode=data.get("barcode", None),
                loose=data.get("loose", False),
                enable=data.get("enable", True),
                sid=sid,
            )
        except Exception as e:
            print(e)
            return {
                "status": False,
                "error_code": ERROR_CODES["PRODUCT_DATA_MISSING"],
                "message": ERROR_MSG["PRODUCT_DATA_MISSING"],
            }, 400

        try:
            # saving only in store.products is enough and product.save_to_db() isn't needed.
            store.products.append(product)
            store.save_to_db()  # save the store after adding the product.
        except Exception as e:
            print(e)
            return {
                "status": False,
                "error_code": ERROR_CODES["DB_INSERTION_ERROR"],
                "message": ERROR_MSG["DB_INSERTION_ERROR"],
            }, 400

        return {
            "status": True,
            "message": "Insertion of the product is successfull",
        }, 201
