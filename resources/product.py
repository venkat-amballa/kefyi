from flask import request
from flask_restful import Resource, reqparse

from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity

from models.product import ProductModel
from models.store import StoreModel


class ProductList(Resource):
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

        

class Product(Resource):
    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument(
        "price", type=float, required=True, help="Invalid Amount, {error_msg}"
    )
    parser.add_argument(
        "quantity", type=int, required=True, help="Invalid Quantity: {error_msg}"
    )
    parser.add_argument(
        "store_id",  type=int, required=False, help="Store id: {error_msg}"
    )

    @jwt_required()
    def get(self, name):
        # find by name
        product = ProductModel.find_by_name(name)
        if product:
            return product.json(), 200
        return {"message": "Product Not Found"}, 404

    @jwt_required()
    def post(self, name):
        '''
        Add products to a store, owned by a user.
        '''
        # JWT required
        # TODO:
        # Find wherther the user has access to this store.

        data = Product.parser.parse_args()
        store = StoreModel.find_by_id(data.store_id)
        if not store:
            return {"message": "No store with that id"}
        # check the user access to the store.

        if ProductModel.find_by_name(name):
            return {"message": "There exists an Product with the same name"}
        
        print(data)
        product = ProductModel(name, price=data["price"], quantity=data["quantity"])
        # product.stores.append(store)
        store.products.append(product)
        try:
            product.save_to_db() # save the product to product db
            store.save_to_db()   # save the store after adding the product.
        except Exception as e:
            return {
                "error": str(e),
                "message": "Some Error Occured while inserting the data",
                "info": "Insertion into product or store db failed"}, 503

        return product.json(), 201

    @jwt_required(fresh=True)
    def put(self, name):
        # JWT required
        data = Product.parser.parse_args()
        # NOTE-THIS
        # data = request.json

        print(data)
        product = ProductModel.find_by_name(name)

        if product:
            product.price = data.get("price", product.price)
            product.quantity = data.get("quantity", product.quantity)
        else:
            product = ProductModel(name, **data)

        product.save_to_db()

        return product.json(), 200

    @jwt_required(fresh=True)
    def delete(self, name):
        claims = get_jwt()
        if not claims["is_admin"]:
            return {"message":"Required admin privilages!!"}, 401

        product = ProductModel.find_by_name(name)
        if product:
            product.delete_from_db()
            return {"Status": "Deleted Successfully"}, 200
        return {"Status": "Cant delete, Product not Found"}, 404
