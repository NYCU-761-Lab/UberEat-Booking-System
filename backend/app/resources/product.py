from flask import jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
import json
import werkzeug

##### register ########################################################################

class product_register(Resource):
    
    # 1. set up the request arguments field
    parser = reqparse.RequestParser()
    parser.add_argument('product_name', type = str, required = True, 
                        help = 'This field cannot be left blank.')
    parser.add_argument('price', type = str, required = True, 
                        help = 'This field cannot be left blank.')
    parser.add_argument('quantity', type = str, required = True, 
                        help = 'This field cannot be left blank.')

    # not sure if the picture part is correct
    parser.add_argument('picture', type = werkzeug.FileStorage, required = True, location='files',
                        help = 'This field cannot be left blank.')
    # owner account
    parser.add_argument('user_account', type = str, required = True, 
                        help = 'This field cannot be left blank.')
    

    # 2. register function
    def post(self):
        # 2-1. receive the data from the front end
        data = product_register.parser.parse_args()
        product_name     = data['product_name']
        price    = data['price']
        quantity    = data['quantity']
        picture   = data['picture']
        user_account = data['user_account']

        # 2-2. format & unique filter
        # check format first, than check unique
        """
        notice
            format:
                1. string 格式正確性
                2. 用 string 接收到的 float / int 是否真的為 float / int 格式，
                   是的話再轉數字並判斷 range 是否符合。
                   ref: resource/user.py    latitude, longitude part
            unique:
                1. ckeck 是否被註冊過

            img 接收與處理: https://stackoverflow.com/questions/28982974/flask-restful-upload-image
        """
        
        # 2-3. if pass the test than save to db



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
