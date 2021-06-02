import os

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.home import Home
from resources.product import Product, ProductList
from resources.user import UserRegister, UserLogin, User, TokenRefresh, UserLogout
from resources.store import Store, StoreList

from block_list import BLOCKLIST

import utils

app = Flask(__name__)
# app.config['BUNDLE_ERRORS'] = True

api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWTManager(app)

@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:
        return {"is_admin":True}
    return {"is_admin":False}

@jwt.token_in_blocklist_loader
def token_revoked_callback(jwt_header, jwt_payload):
    # print(jwt_header, jwt_payload)
    return False

'''
Callbacks to override default responses in callbacks
 When ever there is some unexpected behaviour, the flask sends its defaut responses. But,
 incase of you want to override those. You can use these callback functions.
 [ref] https://flask-jwt-extended.readthedocs.io/en/stable/api/

    1. @jwt.expired_token_loader        -       when the token had expired, 
                                                instead of default respopnse, the decorated method response will be sent
                                                
    2. @jwt.invalid_token_loader        -       When JWT Token is invalid
    3. @jwt.unauthorized_loader         -       when there is no JWT in Authorisation header, 
                                                Default Response:
                                                {
                                                    "msg": "Missing Authorization Header"
                                                }
                                                
    4. @jwt.needs_fresh_token_loader    -       This decorator sets the callback function for returning a custom response
                                                when a valid and non-fresh token is used on an endpoint that is marked as `fresh=True`.
    5. @jwt.revoked_token_loader        -       This decorator sets the callback function for returning a custom response when a revoked token is encountered.
    6. @jwt.token_in_blocklist_loader   -       # Callback function to check if a JWT exists in a persistent db blocklist, Ex: redis, sqlite, etc
'''

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return {
        "message": "The token has expired", 
        "error": "token_expired"
    }, 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return {
        "message": "Invalid token", 
        "error": "invalid_token", 
        "error":error
        }, 401

@jwt.unauthorized_loader
def unauthorized_callback(error):
    return {
        "message": "provide access token", 
        "error":"authorisation_required", 
        "error":error
        }, 401

@jwt.needs_fresh_token_loader
def needs_fresh_token_callback(jwt_header, jwt_payload):
    return {
        "message": "Login again for fresh access token", 
        "error": "needs_fresh_token"
    }, 401

@jwt.revoked_token_loader
def revoked_token_callback():
    return {
        "message": "Token is revoked, login again", 
        "error": "revoked_token"
    }, 401

api.add_resource(Home, "/")

api.add_resource(ProductList, "/products")
api.add_resource(Product, "/products/<string:name>")

api.add_resource(StoreList, "/stores")
api.add_resource(Store, "/stores/<int:id>")

api.add_resource(UserRegister, "/register")
api.add_resource(User, "/user/<int:id>")
api.add_resource(UserLogin, "/login")
api.add_resource(UserLogout, "/logout")

api.add_resource(TokenRefresh, "/refresh")


if __name__ == "__main__":
    from db import db
    env = os.environ['ENV']
    utils.load_config(app, env)

    db.init_app(app)
   
    app.run(debug=True)

