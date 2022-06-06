from flask import jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
import json
import werkzeug
from models.user import UserModel
from models.shop import ShopModel
from models.product import ProductModel
from models.transaction import TransactionModel
import numpy as np
import cv2
import base64
import ast
import os

class transaction_type_filter(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('req_type', type = str, required = True, 
                        help = 'This field cannot be left blank.')

    @jwt_required(optional = True)  # remember to all (optional = True)!!! will raise TypeError(f'Object of type {o.__class__.__name__} 'TypeError: Object of type function is not JSON serializable
    def post(self):

        # 1. checkout account
        identity = get_jwt_identity()
        user = UserModel.query.filter_by(account=identity).first()
        if not user:
            return {'message': 'This user does not exist.'}, 400

        # 2. check type format
        data = transaction_type_filter.parser.parse_args()
        req_type     = data['req_type']

        if req_type != "payment" and req_type != "receive" and req_type != "recharge":
            return {'message': 'The format of request type is wrong.'}, 400

        query = TransactionModel.query.filter_by(owner = identity, type = req_type).all()
        transaction_list = []
        for single_record in query:
            single_list = [single_record.transaction_id, single_record.type, single_record.time, single_record.trader, single_record.amount_of_money]
            print(single_record.trader)
            transaction_list.append(single_list)
        
        return {'transaction_list': transaction_list}, 200
