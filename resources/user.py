from werkzeug.security import safe_str_cmp

from flask_restful import Resource, reqparse
from models.user import UserModel

from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token, 
    jwt_required, 
    get_jwt_identity,
    get_jwt
)


class UserRegister(Resource):
    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument(
        "first_name", type=str, required=True, 
        help="First Name is a Mandatory field",
    )
    parser.add_argument(
        "last_name", type=str,
        help="Last Name of the user is Optional",
    )
    parser.add_argument(
        "password", type=str, required=True, 
        help="Password for the user is required"
    )
    parser.add_argument(
        "email", type=str,  
        help="Email of the user is Optional"
    )
    parser.add_argument(
        "address", type=str, 
        help="Address of the user is Optional"
    )
    parser.add_argument(
        "mobile", type=str, required=True,
        help="Mobile number is required"
    )

    def post(self):
        # JWT required
        """
        User is getting registered, here.
        """
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_first_name(data.get("first_name")):
            return {"message": "User exists already"}, 400

        # if data.get('password') != data.get('retype-password'):
        #     return {"message": "Password entered in retype password, password must be same"}, 400
        try:
            user = UserModel(**data)
            user.save_to_db()
        except Exception:
            return {"message": "Error while creating user, in db"}, 500

        return {"status":True, "message": user.json()}, 201

_user_parser = reqparse.RequestParser(bundle_errors=True)
_user_parser.add_argument(
    "first_name", type=str, required=True, help="First Neame of the user is a Mandatory field",
)
_user_parser.add_argument(
    "password", type=str, required=True, help="Password for the user is needed"
)

class User(Resource):
    '''
    CRUD for the user
    '''
    @classmethod
    def get(cls, first_name):
        data = _user_parser.parse_args()

        user = UserModel.find_by_first_name(data.get(first_name, None))
        if not user:
            return {"message": "User Not Found"}, 404
        return user.json(), 200

    @classmethod
    def delete(cls, id):
        user = UserModel.find_by_id(id)
        if not user:
            return {"message": "User Not Found"}, 404
        user.delete_from_db()

        return {"message": "User deleted Successfully"}, 200


class UserLogin(Resource):
    @classmethod
    def get(cls):
        data = _user_parser.parse_args()
        user = UserModel.find_by_first_name(data.get("first_name", None))

        if user and safe_str_cmp(user.password, data.get("password", None)):
            jwt_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {"access_token": jwt_token, "refresh_token": refresh_token}, 200

        return {"message": "Invalid Credentials"}, 401


class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        # We will have a valid jwt, if we reach here. So there will be a user id attached.
        user_id = get_jwt_identity()
        refresh_token = create_access_token(identity=user_id, fresh=False)
        return {"access_token":refresh_token}, 200


class UserLogout(Resource):
    @jwt_required()
    def post(self):
        # jri = get_jwt()
        # try:
        #     raise Exception("")
        # except Exception as e:
        #     print("Not Implemented The EndPoint")
        return {"error":"not_implemented","message":"Not Implemented The EndPoint"}, 200
    