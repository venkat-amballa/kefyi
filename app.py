import os

from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from db import db

from resources.home import Home, Todo

# from resources.product import Product, ProductList
from resources.product import Product, ProductItem
from resources.units import Units
from resources.categories import Categories
from resources.refund import OrderRefund
from resources.user import UserRegister, UserLogin, User, TokenRefresh, UserLogout
from resources.store import Store, StoreList, StoreOrders
from resources.customer import Customer, CustomerOrders
from resources.order import Order, OrderData

from resources.store_product import StoreProduct, StoreProducts

from block_list import BLOCKLIST

import utils

"""
400 - BAD REQUEST, for duplicate records
"""
app = Flask(__name__)
# 'sqlite:///data.db' # the database can be anytype like: postgresql, mysql etc instead of sqlite
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db').replace("://", "ql://", 1)
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "#@%~4Lo*)+_=^"
# app.config['BUNDLE_ERRORS'] = True
# app.config['PROPAGATE_EXCEPTIONS'] = True
env = os.environ["ENV"]
utils.load_config(app, env)

print(f"Connected to: {app.config['SQLALCHEMY_DATABASE_URI']}")
api = Api(app)

jwt = JWTManager(app)
# Database Migrations
db.init_app(app)
migrate = Migrate(app, db)

if env == "DEV":
    @app.before_first_request
    def create_tables():
        db.create_all()


@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:
        return {"is_admin": True}
    return {"is_admin": False}


@jwt.token_in_blocklist_loader
def token_revoked_callback(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    return jti in BLOCKLIST


@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return {
               "status": False,
               "message": "The token has expired",
               "error_code": "token_expired",
           }, 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return {
               "status": False,
               "message": "Invalid token",
               "error_code": "invalid_token",
           }, 401


@jwt.unauthorized_loader
def unauthorized_callback(error):
    return {
               "status": False,
               "message": "provide access token",
               "error_code": "authorisation_required",
           }, 401


@jwt.needs_fresh_token_loader
def needs_fresh_token_callback(jwt_header, jwt_payload):
    return {
               "status": False,
               "message": "Login again for fresh access token",
               "error_code": "needs_fresh_token",
           }, 401


@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return {
               "status": False,
               "message": "Token is revoked, login again",
               "error_code": "revoked_token"}, 401


api.add_resource(Home, "/")
api.add_resource(Todo, '/todo/<string:todo_id>', endpoint='todo_ep')

# api.add_resource(ProductList, "/all_products")
api.add_resource(ProductItem, "/products/<int:pid>")
api.add_resource(Product, "/products")
api.add_resource(Categories, "/categories")
api.add_resource(Units, "/units")

api.add_resource(Order, "/order")
api.add_resource(OrderData, "/order/<int:id>")
api.add_resource(OrderRefund, "/order/<int:order_id>/refund")

# api.add_resource(CustomerRegister, "/customer/register")
api.add_resource(Customer, "/customer")
api.add_resource(CustomerOrders, "/customer/<int:cid>/orders")

api.add_resource(UserRegister, "/user/register")
api.add_resource(User, "/user")
api.add_resource(UserLogin, "/user/login")
api.add_resource(UserLogout, "/user/logout")

api.add_resource(TokenRefresh, "/refresh")

api.add_resource(StoreList, "/stores")
api.add_resource(Store, "/stores/<int:sid>")

api.add_resource(StoreProduct, "/store/<int:sid>/product/<int:pid>")
api.add_resource(StoreProducts, "/store/<int:sid>/products")
api.add_resource(StoreOrders, "/store/<int:sid>/orders")

if __name__ == "__main__":
    # db.init_app(app)
    app.run(port=5000)
