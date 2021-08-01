from flask import request
from flask_restful import Resource, reqparse

from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity

from models.product import ProductModel
from models.store import StoreModel

from configs.errors import errors

'''
class ProductList(Resource):
    \'''
    TODO:
    Remove this functinality not required
    \'''
    @jwt_required(optional=True)
    def get(self):
        user_id = get_jwt_identity()
        products = ProductModel.find_all()

        # if, JWT is present
        if user_id:
            # if URL ARGUMENTS are present, /products?name=<name>&catoegory=<category>&price_high=<upper_limiit_price> ...... 
            args_name = request.args.get("name", None)
            if args_name:
                products = ProductModel.find_similar(args_name)
                if products:
                    return {
                        "search_key": args_name,
                        "search_Products": [product.json() for product in products],
                    }, 200
            
            # else, RETURN ALL PRODUCTS, as json
            return {"Products": [product.json() for product in products]}, 200
        else:
            return {
                "user_id":user_id,
                "Products": [product.name for product in products],
                "message": "for more results, Login reqiuired"
            }, 200
'''
class ProdctItem(Resource):

    @jwt_required()
    def get(self, id):
        # find by id
        product = ProductModel.find_by_id(id)
        if product:
            return product.json(), 200
        return {"message": "Product Not Found"}, 404

    @jwt_required(fresh=True)
    def put(self, id):
        # JWT required
        data = request.get_json()
        print(data)
        # NOTE-THIS
        # data = request.json
        product = ProductModel.find_by_id(id)
        if product:
            product.name = data.get("name", product.name)
            product.actual_price = data.get("actual_price", product.actual_price)
            product.wholesale_price = data.get("wholesale_price", product.wholesale_price)
            product.retail_price = data.get("retail_price", product.retail_price)
            product.quantity = data.get("quantity", product.quantity)
            product.category = data.get("category", product.category)
        else:
            return {"status":False, "error_code":"PRODUCT_NOT_DOUND", "message":"No product with the given id, to update"}, 400
        # TODO
        # PUT method doesnot support any product creation, if there is no product with given id, returns an error.
        # else:
        #     product = ProductModel(name, **data)
        try:
            product.save_to_db()
        except Exception as error:
            error_dict = errors['DB']['DB_INSERTION_ERROR']
            return error_dict['RESPONSE'],error_dict['STATUS_CODE'] 

        return {"status":True, "message":"Product update successfull"}, 200

    @jwt_required(fresh=True)
    def delete(self, id):
        claims = get_jwt()
        if not claims["is_admin"]:
            return {"message":"Required admin privilages!!"}, 401

        product = ProductModel.find_by_id(id)
        if product:
            product.delete_from_db()
            return {"Status": "Deleted Successfully"}, 200
        return {"status": "Cant delete, Product not Found"}, 404

class Product(Resource):
    parser_product = reqparse.RequestParser(bundle_errors=True)
    parser_product.add_argument("name", type=str, required=True, help="Product name, error: {error_msg}")
    parser_product.add_argument("actual_price", type=float, required=True, help="Invalid Actual Amount, error: {error_msg}")
    parser_product.add_argument("wholesale_price", type=float, required=True, help="Invalid Wholsesale Amount, error: {error_msg}")
    parser_product.add_argument("retail_price", type=float, required=True, help="Invalid Retail Amount, error: {error_msg}")
    parser_product.add_argument("quantity", type=int, required=True, help="Invalid Quantity: error: {error_msg}")
    parser_product.add_argument("category", type=str, required=True, help="Category name, error: {error_msg}")
    parser_product.add_argument("store_id",  type=int, required=False, help="Store id: error: {error_msg}")

    

    @jwt_required()
    def post(self):
        '''
        Add products to a store, owned by a user.
        '''
        # JWT required
        # TODO:
        # Find wherther the user has access to this store, only allow if he does.
        data = request.get_json()
        # data = Product.parser_product.parse_args()
        name = data.get("name", None)
        if name is None:
            return {"status":False, "error_code":"PRODUCT_NAME_REQUIRED","message": "Product name is required"}, 400
        
        store = StoreModel.find_by_id(data.store_id)
        if not store:
            return {"status":False, "error_code":"INVALID_STORE","message": "No store with the given id"}, 400
        # check the user access to the store.
        
        if ProductModel.find_by_name(name):
            return {"status":False, "error_code":"PRODUCT_NAME_DUPLICATE","message": "There exists an Product with the same name"}, 400
        
        product = ProductModel(**data)
        # saving only in store.products is enough and product.save_to_db() isn't needed.
        store.products.append(product)
        try:
            product.save_to_db() # save the product to product db
            store.save_to_db()   # save the store after adding the product.
        except Exception as e:
            return {
                "status": False,
                "error_code":"DB_INSERTION_ERROR",
                "message": "Some Error Occured while inserting the data. (Insertion into product or store db failed)"
                }, 400

        return {"status":True, "message":"Insertion of the product is successfull"}, 201

