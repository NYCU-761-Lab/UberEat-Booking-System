from flask import jsonify
from flask_restful import Resource, reqparse
from .check_function import check_username, is_float
from werkzeug.security import generate_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import ast

# from ..models.user import UserModel
import sys
sys.path.append('..')
from models.user import UserModel

class auth_register(Resource):
    
    # 1. set up the request arguments field
    parser = reqparse.RequestParser()
    parser.add_argument('account', type = str, required = True, 
                        help = 'This field cannot be left blank.')
    parser.add_argument('password', type = str, required = True, 
                        help = 'This field cannot be left blank.')
    parser.add_argument('username', type = str, required = True, 
                        help = 'This field cannot be left blank.')
    parser.add_argument('phone_number', type = str, required = True, 
                        help = 'This field cannot be left blank.')
    # change the feild of latitude & longitude into str in parser 
    # in order to better handle all the situations
    parser.add_argument('latitude', type = str, required = True, 
                        help = 'This field cannot be left blank.')
    parser.add_argument('longitude', type = str, required = True, 
                        help = 'This field cannot be left blank.')
    
    # 2. register function
    def post(self):
        # 2-1. receive the data from the front end
        data = auth_register.parser.parse_args()
        account     = data['account']
        password    = data['password']
        username    = data['username']
        phone_number    = data['phone_number']
        latitude    = data['latitude']
        longitude   = data['longitude']
        role        = 'user'

        # 2-2. format & unique filter
        # check format first, than check unique
        if not account.isalnum() or not (0 < len(account) and len(account) <= 256):
            return {'message': 'The account format is wrong.'}, 400
        elif UserModel.find_by_account(account):
            return {'message': 'The account is already being used.'}, 409

        elif not password.isalnum() or not (0 < len(password) and len(password) <= 256):
            return {'message': 'The password format is wrong.'}, 400

        elif not check_username(username):
            return {'message': 'The username format is wrong.'}, 400
            
        elif not phone_number.isdigit() or len(phone_number) != 10:
            return {'message': 'The phone number format is wrong.'}, 400

        elif not is_float( latitude ):
            return {'message': 'The latitude is not float type.'}, 400
        elif not (-90 <= ast.literal_eval(latitude) and ast.literal_eval(latitude) <= 90):
            return {'message': 'The latitude value range is wrong.'}, 400

        elif not is_float( longitude ):
            return {'message': 'The longitude is not float type.'}, 400
        elif not (-180 <= ast.literal_eval(longitude) and ast.literal_eval(longitude) <= 180):
            return {'message': 'The longitude value range is wrong.'}, 400
        

        # 2-3. pass the test and need to save to db
        password = generate_password_hash(password, method='pbkdf2:sha256') # salt length seems like 16
        user = UserModel(account, password, username, phone_number, ast.literal_eval(latitude), ast.literal_eval(longitude), role)
        user.save_to_db()
        access_token = create_access_token(identity = account)
        return {'message': 'User has been created successfully.',
                'access_token' : access_token
                }, 200


class auth_login(Resource):
    
    # 1. set up the request arguments field
    parser = reqparse.RequestParser()
    parser.add_argument('account', type = str, required = True, 
                        help = 'This field cannot be left blank.')
    parser.add_argument('password', type = str, required = True, 
                        help = 'This field cannot be left blank.')
    
    # 2. login function
    def post(self):
        # 2-1. receive the data from the front end
        data = auth_login.parser.parse_args()
        account     = data['account']
        password    = data['password']

        # 2-2. check account & password
        user = UserModel.query.filter_by(account = account).one_or_none()
        if not user:
            return {'message': 'This account has not registered yet.'}, 401
        elif not user.check_password(password):
            return {'message': 'Wrong password.'}, 401

        # 2-3. pass and handout JWT
        access_token = create_access_token(identity = account)
        return {'access_token' : access_token}, 200


class auth_check_account(Resource):
    # 1. set up the request arguments field
    parser = reqparse.RequestParser()
    parser.add_argument('account', type = str, required = True, 
                        help = 'This field cannot be left blank.')
    # 2. check account function
    def post(self):
        # 2-1. receive the data from the front end
        data = auth_check_account.parser.parse_args()
        account     = data['account']

        # 2-2. check account & password
        if not account.isalnum() or not (0 < len(account) and len(account) <= 256):
            return {'message': 'The account format is wrong.'}, 400
        elif UserModel.find_by_account(account):
            return {'message': 'The account is already being used.'}, 409
        else:
            return {'message': 'The account has not been used.'}, 200


class auth_account_information(Resource):
    @jwt_required(optional = True)
    def post(self):
        identity = get_jwt_identity()
        account_information = UserModel.find_by_account(identity)

        username = account_information.username
        phone_number = account_information.phone_number
        latitude = account_information.latitude
        longitude = account_information.longitude
        role = account_information.role
        
        return {'account': identity,
                'username': username, 
                'phone_number': phone_number, 
                'latitude': latitude, 
                'longitude': longitude, 
                'role': role}, 200


class auth_location(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('latitude', type = str, required = True, 
                        help = 'This field cannot be left blank.')
    parser.add_argument('longitude', type = str, required = True, 
                        help = 'This field cannot be left blank.')

    @jwt_required(optional = True)
    def put(self):
        # check account
        identity = get_jwt_identity()
        user = UserModel.query.filter_by(account = identity).one_or_none()
        if not user:
            return {'message': 'No this account.'}, 401
        
        # check value
        data = auth_location.parser.parse_args()
        latitude    = data['latitude']
        longitude   = data['longitude']

        if not is_float( latitude ):
            return {'message': 'The latitude is not float type.'}, 400
        elif not (-90 <= ast.literal_eval(latitude) and ast.literal_eval(latitude) <= 90):
            return {'message': 'The latitude value range is wrong.'}, 400

        elif not is_float( longitude ):
            return {'message': 'The longitude is not float type.'}, 400
        elif not (-180 <= ast.literal_eval(longitude) and ast.literal_eval(longitude) <= 180):
            return {'message': 'The longitude value range is wrong.'}, 400

        # edit db
        latitude = ast.literal_eval(latitude)
        longitude = ast.literal_eval(longitude)
        UserModel.edit_location(identity, latitude, longitude)
        return {'message': 'The locaton has been edited successfully.'}, 200
