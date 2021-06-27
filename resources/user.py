from werkzeug.security import safe_str_cmp

from flask_restful import Resource, reqparse
from models.user import UserModel

from configs.errors import errors


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
        "username", type=str, required=True, 
        help="usernmae is a Mandatory field")
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
        if UserModel.find_by_username(data.get("username", None)):
            return {"status":False, "message": "User exists already"}, 400
        username= data.get("username", '')
        
        # TODO: add regex to verify this
        if(len(username.strip())<5):
            return {"status":False, "message": "Username length should be greater than 4"}, 400
        # if data.get('password') != data.get('retype-password'):
        #     return {"message": "Password entered in retype password, password must be same"}, 400
        try:
            user = UserModel(**data)
            user.save_to_db()
        except Exception:
            return {"status":False, "message": "Error while creating user, in db"}, 500
        return {"status":True, "message": user.json()}, 201

_user_parser = reqparse.RequestParser(bundle_errors=True)
_user_parser.add_argument(
    "username", type=str, required=True, help="First Neame of the user is a Mandatory field",
)
_user_parser.add_argument(
    "password", type=str, required=True, help="Password for the user is needed"
)

class User(Resource):
    '''
    CRUD for the user
    '''
    @classmethod
    @jwt_required()
    def get(cls):
        id = get_jwt_identity()
        data = _user_parser.parse_args()
        user = UserModel.find_by_id(id)
        if not user:
            return {"status":False, "message": "User Not Found"}, 404

        if user.username == data.get("username", None) and safe_str_cmp(user.password, data.get("password", None)):
            response = {
                "status":True,
                "user":user.json()
            }
            return response, 200
        return {"status":False, "message":"Invalid username/password"}, 404
    
    @classmethod
    @jwt_required(fresh=True)
    def delete(cls):
        id = get_jwt_identity()
        user = UserModel.find_by_id(id)
        
        if not user:
            return {"status":False, "message": "User Not Found"}, 404
        try:
            user.delete_from_db()
        except Exception as e:
            print(e)
            return {"status":False, "message": "User cant be deleted, Exception in user delete"}
        return {"status":True, "message": "User deleted Successfully"}, 200


class UserLogin(Resource):
    '''
    get - login/
    '''
    @classmethod
    def get(cls):
        login_status = False
        data = _user_parser.parse_args()
        user = UserModel.find_by_username(data.get("username", None))
        print("user login request received")
        if user and safe_str_cmp(user.password, data.get("password", None)):
            login_status=True
            jwt_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {"access_token": jwt_token, "refresh_token": refresh_token}, 200

        return {"status":login_status, "message": "Invalid Credentials"}, 401


class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        # We will have a valid jwt, if we reach here. So there will be a user id attached.
        user_id = get_jwt_identity()
        refresh_token = create_access_token(identity=user_id, fresh=False)
        return {"status":True, "access_token":refresh_token}, 200


class UserLogout(Resource):
    @jwt_required()
    def post(self):
        # jri = get_jwt()
        # try:
        #     raise Exception("")
        # except Exception as e:
        #     print("Not Implemented The EndPoint")
        return {"error":"not_implemented","message":"Not Implemented The EndPoint"}, 200
    