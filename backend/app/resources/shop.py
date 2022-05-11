# from flask import jsonify
# from flask_restful import Resource, reqparse
# import json

# ##### register ########################################################################

# class shop_register(Resource):
    
#     # 1. set up the request arguments field
#     parser = reqparse.RequestParser()
#     parser.add_argument('shop_name', type = str, required = True, 
#                         help = 'This field cannot be left blank.')
#     parser.add_argument('shop_type', type = str, required = True, 
#                         help = 'This field cannot be left blank.')
#     parser.add_argument('latitude', type = str, required = True, 
#                         help = 'This field cannot be left blank.')
#     parser.add_argument('longitude', type = str, required = True, 
#                         help = 'This field cannot be left blank.')
#     # owner account
#     parser.add_argument('user_account', type = str, required = True, 
#                         help = 'This field cannot be left blank.')
    
#     # 2. register function
#     def post(self):
#         # 2-1. receive the data from the front end
#         data = shop_register.parser.parse_args()
#         shop_name     = data['shop_name']
#         shop_type    = data['shop_type']
#         latitude    = data['latitude']
#         longitude   = data['longitude']
#         user_account   = data['user_account']

#         # 2-2. format & unique filter
#         # check format first, than check unique
#         """
#         notice
#             format:
#                 1. string 格式正確性
#                 2. 用 string 接收到的 float / int 是否真的為 float / int 格式，
#                    是的話再轉數字並判斷 range 是否符合。
#                    ref: resource/user.py    latitude, longitude part
#             unique:
#                 1. ckeck 是否被註冊過
#         """
        
#         # 2-3. if pass the test than save to db


# ##### shop filter ########################################################################

# class shop_name_filter(Resource):
    
#     # 1. set up the request arguments field
#     parser = reqparse.RequestParser()
#     parser.add_argument('ask_shop_name', type = str, required = True, 
#                         help = 'This field cannot be left blank.')

#     # 2. filter function
#     def get(self):
#         # 2-1. receive the data from the front end
#         data = shop_name_filter.parser.parse_args()
#         ask_shop_name     = data['ask_shop_name']

#         # 2-2. check if "ask_shop_name" is in db
        

# class shop_distance_filter(Resource):
    
#     # 1. set up the request arguments field
#     parser = reqparse.RequestParser()
#     # need user_account to count for the relative distance
#     parser.add_argument('user_account', type = str, required = True, 
#                         help = 'This field cannot be left blank.')
#     parser.add_argument('req_distance', type = str, required = True, 
#                         help = 'This field cannot be left blank.')

#     # 2. filter function
#     def get(self):
#         # 2-1. receive the data from the front end
#         data = shop_distance_filter.parser.parse_args()
#         user_account     = data['user_account']
#         req_distance     = data['req_distance']

#         # 2-2. get the all the store name in the req_distance range



# class shop_type_filter(Resource):
    
#     # 1. set up the request arguments field
#     parser = reqparse.RequestParser()
#     parser.add_argument('req_type', type = str, required = True, 
#                         help = 'This field cannot be left blank.')

#     # 2. filter function
#     def get(self):
#         # 2-1. receive the data from the front end
#         data = shop_type_filter.parser.parse_args()
#         req_type     = data['req_type']

#         # 2-2. get the all the store name in the req_distance range


# ##### get shop info ########################################################################
# # 1. shop_type
# # 2. shop_distance

# # 3. shop_latitude
# # 4. shop_longitude

# class get_shop_type(Resource):
    
#     # 1. set up the request arguments field
#     parser = reqparse.RequestParser()
#     parser.add_argument('shop_name', type = str, required = True, 
#                         help = 'This field cannot be left blank.')

#     # 2. get info function
#     def get(self):
#         # 2-1. receive the data from the front end
#         data = get_shop_type.parser.parse_args()
#         shop_name     = data['shop_name']

#         # 2-2. return the shop_type of the shop_name



# class get_shop_distance(Resource):
    
#     # 1. set up the request arguments field
#     parser = reqparse.RequestParser()
#     parser.add_argument('user_account', type = str, required = True, 
#                         help = 'This field cannot be left blank.')
#     parser.add_argument('shop_name', type = str, required = True, 
#                         help = 'This field cannot be left blank.')

#     # 2. get info function
#     def get(self):
#         # 2-1. receive the data from the front end
#         data = get_shop_distance.parser.parse_args()
#         user_account     = data['user_account']
#         shop_name     = data['shop_name']

#         # 2-2. use the shop_name and user_account to get the distance between them



# class get_shop_latitude(Resource):
    
#     # 1. set up the request arguments field
#     parser = reqparse.RequestParser()
#     parser.add_argument('shop_name', type = str, required = True, 
#                         help = 'This field cannot be left blank.')

#     # 2. get info function
#     def get(self):
#         # 2-1. receive the data from the front end
#         data = get_shop_latitude.parser.parse_args()
#         shop_name     = data['shop_name']

#         # 2-2. use the shop_name to get it's info



# class get_shop_longitude(Resource):
    
#     # 1. set up the request arguments field
#     parser = reqparse.RequestParser()
#     parser.add_argument('shop_name', type = str, required = True, 
#                         help = 'This field cannot be left blank.')

#     # 2. get info function
#     def get(self):
#         # 2-1. receive the data from the front end
#         data = get_shop_longitude.parser.parse_args()
#         shop_name     = data['shop_name']

#         # 2-2. use the shop_name to get it's info