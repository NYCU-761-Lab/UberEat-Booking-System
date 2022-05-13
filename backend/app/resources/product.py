from flask import jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
import json
import werkzeug
from models.user import UserModel
from models.shop import ShopModel
from models.product import ProductModel
import numpy as np
import cv2
import base64
import ast


##### register ########################################################################

# 1. 註冊餐點
class product_register(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('product_name', type = str, required = True, 
                        help = 'This field cannot be left blank.')
    parser.add_argument('price', type = str, required = True, 
                        help = 'This field cannot be left blank.')
    parser.add_argument('quantity', type = str, required = True, 
                        help = 'This field cannot be left blank.')
    # not sure if the picture part is correct
    # parser.add_argument('picture', type = werkzeug.FileStorage, required = True, location='form',
    #                     help = 'This field cannot be left blank.')
    parser.add_argument('picture', type = str, required = True, 
                        help = 'This field cannot be left blank.')
    

    # 2. register function
    @jwt_required(optional = True)
    def post(self):
        user_account = get_jwt_identity()
        # 2-1. check user & shop
        user = UserModel.query.filter_by(account = user_account).one_or_none() 
        if not user:
            return {'message': 'Invalid user account.'}, 401

        shop = ShopModel.query.filter_by(owner = user_account).one_or_none()
        if not shop:
            return {'message': 'This user has not registered a shop. Please register a shop first.'}, 401

        data = product_register.parser.parse_args()
        product_name     = data['product_name']
        price    = data['price']
        quantity    = data['quantity']
        picture_base64   = data['picture']

        # 2-2. price, quantity: unsigned int format filter
        if not price.isdigit():
            return {'message': 'The price type is not unsigned integer.'}, 400
        elif not quantity.isdigit():
            return {'message': 'The quantity type is not unsigned integer.'}, 400

        # 2-3. if pass the test than save to db
        # deal with the picture first
        # img_decode = base64.b64decode(picture_base64)
        img_inside_url = "/Users/yoona/Documents/4th_Sem/sql/HW2_new/UberEat-Booking-System/backend/product_image/" + user_account + "_" + product_name + ".jpeg"
        # cv2.imwrite(img_inside_url, img_decode)
        with open(img_inside_url, "wb") as fh:
            fh.write(base64.urlsafe_b64decode(picture_base64))

        # tmp shop id: 1
        product = ProductModel(2, product_name, img_inside_url, ast.literal_eval(price), ast.literal_eval(quantity), user_account, shop.shop_name)
        product.save_to_db()
        return {'message': 'Product has been created successfully.'}, 200

        # # convert to numpy array
        # npimg = np.fromstring(stream, np.uint8)
        # # convert numpy array to image
        # img = cv2.imdecode(npimg, cv2.IMREAD_UNCHANGED)
        # img_inside_url = "/Users/yoona/Documents/4th_Sem/sql/HW2_new/UberEat-Booking-System/backend/product_image" + user_account + product_name + ".jpg"
        # cv2.imwrite( img_inside_url, img)
        # ast.literal_eval(price)
        # ast.literal_eval(quantity)


##### product information of a shop ########################################################################

"""
    use user_account to get all the product in the shop

    like:
        select product_item
        from product_table
        where owner = user_account
"""
class product_of_a_shop(Resource):
    # 1. get list (all)
    parser_get = reqparse.RequestParser()
    # product owner's account, same as shop owner's account
    parser_get.add_argument('user_account', type = str, required = True, 
                        help = 'This field cannot be left blank.')

    # 2. edit certain product
    parser_edit = reqparse.RequestParser()
    parser_get.add_argument('user_account', type = str, required = True, 
                        help = 'This field cannot be left blank.')
    parser_edit.add_argument('product_id', type = str, required = True, 
                        help = 'This field cannot be left blank.')
        

    # 3. delete certain product
    parser_delete = reqparse.RequestParser()
    parser_get.add_argument('user_account', type = str, required = True, 
                        help = 'This field cannot be left blank.')
    parser_delete.add_argument('product_id', type = str, required = True, 
                        help = 'This field cannot be left blank.')


    # 1. get list (all), get all the product belong to user_account
    @jwt_required(optional = True)
    def get(self):
        pass

    # 2. edit certain product, need to check if the user_account is the product owner
    # product_price, product_number
    @jwt_required(optional = True)
    def put(self):
        pass

    # 3. delete certain product, need to check if the user_account is the product owner
    @jwt_required(optional = True)
    def delete(self):
        pass


##### product filter ########################################################################
### all return shop_name!!! ###

class product_price_filter(Resource):
    
    # 1. set up the request arguments field
    parser = reqparse.RequestParser()

    # 可以為空，但不會都為空，不然前端不會送 req!!!
    parser.add_argument('price_lower_bound', type = str)
    parser.add_argument('price_upper_bound', type = str)

    # 2. filter function
    def get(self):
        # 2-1. receive the data from the front end

        # 2-2. get all the shop that "one of their product"'s price is lower_bound<= &  <= upper_bound
        """
            1. 如果 lower_bound 為空
            2. 如果 upper_bound 為空
            3. 都不為空

            收進來 string 要先判斷是否為 float type - check_function.is_float(str)
        """
        pass



class product_name_filter(Resource):

    # 1. set up the request arguments field
    parser = reqparse.RequestParser()
    parser.add_argument('ask_product_name', type = str, required = True, 
                        help = 'This field cannot be left blank.')

    # 2. filter function
    def get(self):
        # 2-1. receive the data from the front end
        data = product_name_filter.parser.parse_args()
        ask_product_name     = data['ask_product_name']

        # 2-2. check if the product name is in db
        pass


##### get product info ########################################################################

class get_product_info_of_a_shop(Resource):

    # 1. set up the request arguments field
    parser = reqparse.RequestParser()
    parser.add_argument('shop_name', type = str, required = True, 
                        help = 'This field cannot be left blank.')

    # 2. filter function
    def get(self):
        # 2-1. receive the data from the front end
        data = get_product_info_of_a_shop.parser.parse_args()
        shop_name     = data['shop_name']

        # 2-2. use shop_name to get all the product in the shop
        #       return product_name, product_picture, price, number
        pass
