from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import UserModel
from models.shop import ShopModel
from .check_function import is_float
import ast
from haversine import haversine, Unit


##### register ########################################################################

# 1. 註冊商店
class shop_register(Resource):
    # 1. set up the request arguments field
    parser = reqparse.RequestParser()
    parser.add_argument('shop_name', type = str, required = True, 
                        help = 'This field cannot be left blank.')
    parser.add_argument('shop_type', type = str, required = True, 
                        help = 'This field cannot be left blank.')
    parser.add_argument('latitude', type = str, required = True, 
                        help = 'This field cannot be left blank.')
    parser.add_argument('longitude', type = str, required = True, 
                        help = 'This field cannot be left blank.')
    
    # 2. register function
    @jwt_required(optional = True)
    def post(self):
        # 2-1. receive the data from the front end
        user_account = get_jwt_identity()
        data = shop_register.parser.parse_args()
        shop_name     = data['shop_name']
        shop_type    = data['shop_type']
        latitude    = data['latitude']
        longitude   = data['longitude']

        # 2-2. check if the user is valid
        user = UserModel.query.filter_by(account = user_account).one_or_none()
        if not user:
            return {'message': 'Invalid user account.'}, 401

        # 2-2. format & unique filter
        """
        notice
            format:
                1. string 格式正確性
                2. 用 string 接收到的 float / int 是否真的為 float / int 格式，
                   是的話再轉數字並判斷 range 是否符合。
                   ref: resource/user.py    latitude, longitude part
            unique:
                1. ckeck 是否被註冊過(shop_name only need to check this, no limit for the format)
        """
        if ShopModel.find_shop_by_owner(user_account):
            return {'message': 'The user has already registered a shop'}, 409
        elif ShopModel.find_by_shop_name(shop_name):
            return {'message': 'The shop name is already being used.'}, 409

        elif not is_float( latitude ):
            return {'message': 'The latitude is not float type.'}, 400
        elif not (-90 <= ast.literal_eval(latitude) and ast.literal_eval(latitude) <= 90):
            return {'message': 'The latitude value range is wrong.'}, 400

        elif not is_float( longitude ):
            return {'message': 'The longitude is not float type.'}, 400
        elif not (-180 <= ast.literal_eval(longitude) and ast.literal_eval(longitude) <= 180):
            return {'message': 'The longitude value range is wrong.'}, 400

        # 2-3. if pass the test than save to db
        shop = ShopModel(shop_name, ast.literal_eval(latitude), ast.literal_eval(longitude), shop_type, user_account)
        shop.save_to_db()

        # 2-4. change the role to manager (never change back)
        UserModel.edit_role(user_account)

        # 2-5. return
        return {'message': 'Shop has been registered successfully. And the role changed to manager.'}, 200


##### shop filter ########################################################################

# 2. 過濾店名
class shop_name_filter(Resource):   

    parser = reqparse.RequestParser()
    parser.add_argument('ask_shop_name', type = str, required = True, 
                        help = 'This field cannot be left blank.')

    def post(self):
        data = shop_name_filter.parser.parse_args()
        ask_shop_name     = data['ask_shop_name']

        # 2-2. check if "ask_shop_name" is in db
        valid_shops = ShopModel.query.filter(ShopModel.shop_name.ilike(f'%{ask_shop_name}%')).all()  # query will return a list of tuple
        valid_shops_name = [valid_shops_entity.shop_name for valid_shops_entity in valid_shops]
        return {'valid_shops_name': valid_shops_name }, 200
        

# 3. 過濾店距離
class shop_distance_filter(Resource):

    parser = reqparse.RequestParser()
    # need user_account to count for the relative distance
    parser.add_argument('req_distance', type = str, required = True, 
                        help = 'This field cannot be left blank.')

    @jwt_required(optional = True)
    def post(self):
        # 2-1. get the user's latitude and longitude
        user_account = get_jwt_identity()
        now_user = UserModel.query.filter_by(account=user_account).first()
        if not now_user:
            return {'message': 'No this user account.'}, 401
        now_place = (now_user.latitude, now_user.longitude)

        data = shop_distance_filter.parser.parse_args()
        req_distance     = data['req_distance']

        if req_distance != 'near' and (req_distance != 'moderate' and req_distance != 'far'):
            return {'message': 'Invalid required distance.' }, 400

        # 2-2. get the all the store name in the req_distance range
        valid_shops_name = []
        all_shop = ShopModel.query.all()
        for shop in all_shop:
            dist = haversine(now_place, (shop.latitude, shop.longitude), unit=Unit.KILOMETERS)
            if req_distance == 'near' and dist <= 2:
                valid_shops_name.append(shop.shop_name)
            elif req_distance == 'moderate' and (2 < dist and dist <= 5):
                valid_shops_name.append(shop.shop_name)
            elif req_distance == 'far' and (5 < dist):  # far
                valid_shops_name.append(shop.shop_name)

        return {'valid_shops_name': valid_shops_name }, 200
        
# 4. 過濾店類別
class shop_type_filter(Resource):
    
    parser = reqparse.RequestParser()
    parser.add_argument('req_type', type = str, required = True, 
                        help = 'This field cannot be left blank.')

    def post(self):
        # 2-2. get the all the store name that req_type match
        data = shop_type_filter.parser.parse_args()
        req_type     = data['req_type']
        valid_shops = ShopModel.query.filter(ShopModel.shop_type.ilike(f'%{req_type}%')).all()  # query will return a list of tuple
        valid_shops_name = [valid_shops_entity.shop_name for valid_shops_entity in valid_shops]
        return {'valid_shops_name': valid_shops_name }, 200


##### get shop info ########################################################################
# 1. shop_type
# 2. shop_distance
# 3. shop_latitude
# 4. shop_longitude
# 5. shop_name_of_a_user

# 5. 顯示店類別
class get_shop_type(Resource):
    
    parser = reqparse.RequestParser()
    parser.add_argument('shop_name', type = str, required = True, 
                        help = 'This field cannot be left blank.')

    def post(self):
        # 2-1. check if the shop exist
        data = get_shop_type.parser.parse_args()
        shop_name     = data['shop_name']
        query = ShopModel.query.filter_by(shop_name = shop_name).first()  # shop_name is unique
        if not query:
            return {'message': 'No this shop.'}, 401

        # 2-2. return the shop_type of the shop_name
        return {'shop_type of the shop_name': query.shop_type }, 200


# 6. 顯示店距離
class get_shop_distance(Resource):
    
    parser = reqparse.RequestParser()
    parser.add_argument('shop_name', type = str, required = True, 
                        help = 'This field cannot be left blank.')

    @jwt_required(optional = True)
    def post(self):
        # 2-1. check if the user exist
        user_account = get_jwt_identity()
        now_user = UserModel.query.filter_by(account=user_account).first()
        if not now_user:
            return {'message': 'No this user account.'}, 401

        # 2-2. check if the shop exist
        data = get_shop_distance.parser.parse_args()
        shop_name     = data['shop_name']
        shop = ShopModel.query.filter_by(shop_name = shop_name).first()
        if not shop:
            return {'message': 'No this shop.'}, 401

        # 2-3. use the shop_name and user_account to get the distance between them
        dist = haversine((now_user.latitude, now_user.longitude), (shop.latitude, shop.longitude), unit=Unit.KILOMETERS)
        return {'Distance to the shop (km)': dist }, 200


# 7. 顯示店經度
class get_shop_latitude(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('shop_name', type = str, required = True, 
                        help = 'This field cannot be left blank.')

    def post(self):
        data = get_shop_latitude.parser.parse_args()
        shop_name     = data['shop_name']
        query = ShopModel.query.filter_by(shop_name = shop_name).first()  # shop_name is unique
        # 2-1. check if the shop exist
        if not query:
            return {'message': 'No this shop.'}, 401

        # 2-2. return the latitude of the shop_name
        return {'latitude of the shop_name': query.latitude }, 200


# 8. 顯示店緯度
class get_shop_longitude(Resource):
    
    parser = reqparse.RequestParser()
    parser.add_argument('shop_name', type = str, required = True, 
                        help = 'This field cannot be left blank.')

    def post(self):
        data = get_shop_longitude.parser.parse_args()
        shop_name     = data['shop_name']
        query = ShopModel.query.filter_by(shop_name = shop_name).first()  # shop_name is unique
        # 2-1. check if the shop exist
        if not query:
            return {'message': 'No this shop.'}, 401

        # 2-2. return the longitude of the shop_name
        return {'longitude of the shop_name': query.longitude }, 200


# 9. 查詢店名
class get_shop_name_of_user(Resource):

    @jwt_required(optional = True)
    def post(self):
        user_account = get_jwt_identity()
        now_user = UserModel.query.filter_by(account=user_account).first()
        if not now_user:
            return {'message': 'No this user account.'}, 401

        shop = ShopModel.query.filter_by(owner=user_account).first()
        if not shop:
            return {'message': 'This user does not own a shop.'}, 401

        # 2-2. get the all the store name in the req_distance range
        return {'shop_name of the user': shop.shop_name }, 200