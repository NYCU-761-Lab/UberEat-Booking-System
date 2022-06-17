from flask import jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
import json
import werkzeug
from models.user import UserModel
from models.shop import ShopModel
from models.product import ProductModel
from models.img_per import ImgPerModel
import numpy as np
import cv2
import base64
import ast
import os
import uuid


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
    parser.add_argument('picture', type = str, required = True, 
                        help = 'This field cannot be left blank.')
    
    # 2. register function
    @jwt_required(optional = True)
    def post(self):
        user_account = get_jwt_identity()
        # 2-1. check user & shop is valid
        user = UserModel.query.filter_by(account = user_account).one_or_none() 
        if not user:
            return {'message': 'Invalid user account.'}, 401

        shop = ShopModel.query.filter_by(owner = user_account).one_or_none()
        if not shop:
            return {'message': 'This user has not registered a shop. Please register a shop first.'}, 400

        data = product_register.parser.parse_args()
        product_name     = data['product_name']
        price    = data['price']
        quantity    = data['quantity']
        picture_base64   = data['picture']

        # 2-2. price, quantity: unsigned int format filter, check the product_name is unique in the same shop
        if not price.isdigit():
            return {'message': 'The price type is not unsigned integer.'}, 400
        elif not quantity.isdigit():
            return {'message': 'The quantity type is not unsigned integer.'}, 400
        elif ProductModel.query.filter_by( product_name = product_name, belong_shop_name = shop.shop_name ).one_or_none():
            return {'message': 'The product name has already been registered in the shop.'}, 409

        # try:
        #     base64.urlsafe_b64decode(pure_picture_base64)
        # except:
        #     {'message': 'The picture is not valid.'}, 400

        # 2-3. if pass the test than save to db
        # can save type: jpg(jpeg), png, bmp (svg will fail)
        img_type = picture_base64[ picture_base64.find("/")+1 : picture_base64.find(";") ]
        pure_picture_base64 = picture_base64[ picture_base64.find(",")+1 :]  # delete header
        img_inside_url = "/Users/yoona/Downloads/HW3_team30_test/UberEat-Booking-System/backend/product_image3/" + user_account + "_" + product_name + "." + img_type
        # img_inside_url = "/Users/angelahsi/Desktop/NYCU/大二下課程/資料庫/HW2/UberEat-Booking-System/backend/product_image/" + user_account + "_" + product_name + "." + img_type
        with open(img_inside_url, "wb") as fh:
            fh.write(base64.urlsafe_b64decode(pure_picture_base64))

        # ** changed here **
        img_per_id = str(uuid.uuid4())
        while ImgPerModel.query.filter_by(per_id = img_per_id).one_or_none() != None:
            img_per_id = str(uuid.uuid4())
        product = ProductModel(product_name, img_inside_url, ast.literal_eval(price), ast.literal_eval(quantity), user_account, shop.shop_name, img_per_id)
        product.save_to_db()
        img_per = ImgPerModel(img_per_id, picture_base64)
        img_per.save_to_db()
        return {'message': 'Product has been created successfully.'}, 200

##### edit product ########################################################################

"""
    use user_account to get all the product in the shop

    like:
        select product_item
        from product_table
        where owner = user_account
"""

# 2. 修改餐點價格
class product_edit_price(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('product_name', type = str, required = True, 
                        help = 'This field cannot be left blank.')
    parser.add_argument('edit_price', type = str, required = True, 
                        help = 'This field cannot be left blank.')

    @jwt_required(optional = True)
    def put(self):
        user_account = get_jwt_identity()
        data = product_edit_price.parser.parse_args()
        product_name     = data['product_name']
        edit_price       = data['edit_price']
        
        # 1. check if the user own a shop and the product is in that shop
        user = UserModel.query.filter_by(account = user_account).one_or_none() 
        if not user:
            return {'message': 'Invalid user account.'}, 401

        shop = ShopModel.query.filter_by(owner = user_account).one_or_none() 
        if not shop:
            return {'message': 'This user has not registered a shop.'}, 400
        
        product = ProductModel.query.filter_by( product_name = product_name, owner = user.account ).one_or_none()
        if not product:
            return {'message': 'Invalid product name. The shop does not have this product.'}, 400

        # 2. check if the edit_price is valid
        if not edit_price.isdigit():
            return {'message': 'The price type is not unsigned integer.'}, 400

        # 3. pass the test than save edit to db
        ProductModel.edit_price(product_name, product.belong_shop_name, ast.literal_eval(edit_price))
        return {'message': 'The price has been edited successfully.'}, 200


# 3. 修改餐點數量
class product_edit_quantity(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('product_name', type = str, required = True, 
                        help = 'This field cannot be left blank.')
    parser.add_argument('edit_quantity', type = str, required = True, 
                        help = 'This field cannot be left blank.')

    @jwt_required(optional = True)
    def put(self):
        user_account = get_jwt_identity()
        data = product_edit_quantity.parser.parse_args()
        product_name     = data['product_name']
        edit_quantity       = data['edit_quantity']
        
        # 1. check if the user own a shop and the product is in that shop
        user = UserModel.query.filter_by(account = user_account).one_or_none() 
        if not user:
            return {'message': 'Invalid user account.'}, 401

        shop = ShopModel.query.filter_by(owner = user_account).one_or_none() 
        if not shop:
            return {'message': 'This user has not registered a shop.'}, 400
        
        product = ProductModel.query.filter_by( product_name = product_name, owner = user.account ).one_or_none()
        if not product:
            return {'message': 'Invalid product name. The shop does not have this product'}, 400

        # 2. check if the edit_quantity is valid
        if not edit_quantity.isdigit():
            return {'message': 'The quantity type is not unsigned integer.'}, 400

        # 3. pass the test than save edit to db
        ProductModel.edit_quantity(product_name, product.belong_shop_name, ast.literal_eval(edit_quantity))
        return {'message': 'The quantity has been edited successfully.'}, 200


# 4. 刪除餐點
class product_delete(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('product_name', type = str, required = True, 
                        help = 'This field cannot be left blank.')

    @jwt_required(optional = True)
    def delete(self):
        user_account = get_jwt_identity()
        data = product_delete.parser.parse_args()
        product_name     = data['product_name']
        
        # 1. check if the user own a shop and the product is in that shop
        user = UserModel.query.filter_by(account = user_account).one_or_none() 
        if not user:
            return {'message': 'Invalid user account.'}, 401
        
        shop = ShopModel.query.filter_by(owner = user_account).one_or_none() 
        if not shop:
            return {'message': 'This user has not registered a shop.'}, 400

        product = ProductModel.query.filter_by( product_name = product_name, owner = user.account ).one_or_none()
        if not product:
            return {'message': 'Invalid product name. The shop does not have this product.'}, 400

        # 3. pass the test than save edit to db
        ProductModel.delete_product(product_name, product.belong_shop_name)
        os.remove(product.picture)  # delete picture img
        return {'message': 'The product has been delete successfully.'}, 200


##### product filter ########################################################################
### all return shop_name!!! ###

# 5. 過濾餐點價格
class product_price_filter(Resource):
    
    parser = reqparse.RequestParser()

    # 可以為空，但不會都為空，不然前端不會送 req!!!
    # 空："null"
    parser.add_argument('price_lower_bound', type = str)
    parser.add_argument('price_upper_bound', type = str)

    def post(self):
        data = product_price_filter.parser.parse_args()
        price_lower_bound     = data['price_lower_bound']
        price_upper_bound     = data['price_upper_bound']
        if price_lower_bound != "null" and (not price_lower_bound.isdigit()):
            return {'message': 'The value of price lower bound is not unsigned integer or null.' }, 400
        elif price_upper_bound != "null" and (not price_upper_bound.isdigit()):
            return {'message': 'The value of price upper bound is not unsigned integer or null.' }, 400

        # 1. get all the shop that "one of their product"'s price is lower_bound<= &  <= upper_bound
        """
            1. 如果 lower_bound 為空
            2. 如果 upper_bound 為空
            3. 都為空
            4. 都不為空

            收進來 string 要先判斷是否為 unsigned int type - isdigit()
        """
        valid_shop_name = []
        all_product = ProductModel.query.all()
        for product in all_product:
            if price_upper_bound == "null" and price_lower_bound == "null":  # both side no constraint
                if (product.belong_shop_name not in valid_shop_name):
                        valid_shop_name.append(product.belong_shop_name)

            elif price_lower_bound == "null":
                if (product.price <= ast.literal_eval(price_upper_bound)):
                    if (product.belong_shop_name not in valid_shop_name):
                        valid_shop_name.append(product.belong_shop_name)
                
            elif price_upper_bound == "null":
                if (ast.literal_eval(price_lower_bound) <= product.price):
                    if (product.belong_shop_name not in valid_shop_name):
                        valid_shop_name.append(product.belong_shop_name)

            else:  
                if (ast.literal_eval(price_lower_bound) <= product.price and product.price <= ast.literal_eval(price_upper_bound)):
                    if (product.belong_shop_name not in valid_shop_name):
                        valid_shop_name.append(product.belong_shop_name)
        
        return {'valid_shops_name': valid_shop_name }, 200    


# 6. 過濾餐點名稱
class product_name_filter(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('ask_product_name', type = str, required = True, 
                        help = 'This field cannot be left blank.')

    def post(self):
        data = product_name_filter.parser.parse_args()
        ask_product_name     = data['ask_product_name']

        # 1. check if the product name is in db
        valid_products = ProductModel.query.filter(ProductModel.product_name.ilike(f'%{ask_product_name}%')).all()  # query will return a list of tuple
        valid_shop_name = []
        for valid_product_entity in valid_products:
            if valid_product_entity.belong_shop_name not in valid_shop_name:
                valid_shop_name.append(valid_product_entity.belong_shop_name)
        return {'valid_shops_name': valid_shop_name }, 200


##### get product info ########################################################################

# 7. 查詢餐點資訊 - name, picture_url, price, quantity
class get_product_info_of_a_shop(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('shop_name', type = str, required = True, 
                        help = 'This field cannot be left blank.')

    def post(self):
        data = get_product_info_of_a_shop.parser.parse_args()
        shop_name     = data['shop_name']

        # 2. use shop_name to get all the product in the shop
        #    return product_name, product_picture, price, number
        query = ProductModel.query.filter_by( belong_shop_name = shop_name ).all()
        product_list = []
        for item in query:
            info_list = [ item.product_name, item.picture, item.price, item.quantity ]
            product_list.append(info_list)
        
        return {'Product list of the shop': product_list}, 200
