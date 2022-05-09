from flask import jsonify
from flask_restful import Resource, reqparse
from .check_function import check_username
from werkzeug.security import generate_password_hash
from flask_jwt_extended import create_access_token
import json
# from ..models.user import UserMode
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
    parser.add_argument('latitude', type = float, required = True, 
                        help = 'This field cannot be left blank.')
    parser.add_argument('longitude', type = float, required = True, 
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

        elif not (-90 <= latitude and latitude <= 90):
            return {'message': 'The latitude value range is wrong.'}, 400
        
        elif not (-180 <= longitude and longitude <= 180):
            return {'message': 'The longitude value range is wrong.'}, 400
        

        # 2-3. pass the test and need to save to db
        password = generate_password_hash(password, method='pbkdf2:sha256') # salt length seems like 16
        user = UserModel(account, password, username, phone_number, latitude, longitude)
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
            return {'message': 'Wrong account.'}, 401
        elif not user.check_password(password):
            return {'message': 'Wrong password.'}, 401

        # 2-3. pass and handout JWT
        access_token = create_access_token(identity = account)
        return {'access_token' : access_token}, 200