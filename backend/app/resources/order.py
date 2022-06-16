from flask import jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
import json
import werkzeug
from models.user import UserModel
from models.shop import ShopModel
from models.product import ProductModel
from models.order import OrderModel
from models.transaction import TransactionModel
from models.order_details import OrderDetailsModel
from models.img_per import ImgPerModel
import numpy as np
import cv2
import base64
import ast
import os
from haversine import haversine, Unit   # count for distance
import datetime
import uuid

# 1. 建立訂單
class order_make(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('order_shop_name', type = str, required = True,  # 計算距離, SID
                        help = 'This field cannot be left blank.')
    parser.add_argument('order_details', type = list, required = True, action='append',   # erect record in order details, *** allow append to receive multiple item
                        help = 'This field cannot be left blank.')
    parser.add_argument('delivery_type', type = str, required = True,    # count for fee
                        help = 'This field cannot be left blank.')
    parser.add_argument('front_total_price', type = int, required = True,    # count for fee
                        help = 'This field cannot be left blank.')

    # Need a valid user account to make an order
    @jwt_required(optional = True)
    def post(self):
        user_account = get_jwt_identity()
        # 1. check is valid user
        user = UserModel.query.filter_by(account = user_account).one_or_none() 
        if not user:
            return {'message': 'This user does not exist.'}, 400

        # unfold data and check
        data = order_make.parser.parse_args()
        order_shop_name     = data['order_shop_name']
        order_details    = data['order_details']    # not sure
        delivery_type    = data['delivery_type']
        front_total_price = data['front_total_price']

        # 2. check shop name
        shop = ShopModel.query.filter_by(shop_name = order_shop_name).one_or_none()
        if not shop:
            return {'message': 'This shop does not exist.'}, 400

        # check order_details, type: list of tuples('product_name', 'quantity')
        # 如果前端顯示的東西與後端現有內容不同(?) -> 用 total price 擋下來
        """*** Q ***"""
        for tuple in order_details:
            product_name = tuple[0]
            quantity = tuple[1]

            # 3. check product exist "in that shop"
            product = ProductModel.query.filter_by(belong_shop_name = order_shop_name, product_name = product_name).one_or_none()
            if not product:
                return {'message': 'The shop does not sell this product'}, 400

            # 4. check product number
            # (1) is positive integer
            if not quantity.isdigit():  # isdigit -> 只能有數字，不可以有負號、小數點
                return {'message': 'The order quality of the product is not positive integer.'}, 400
            elif quantity[0] == '0':    # 也不能是 0 or 0 開頭
                return {'message': 'The order quality of the product is not positive integer.'}, 400

            # (2) is enough for the order
            if product.quantity < ast.literal_eval(quantity):
                return {'message': 'The order quality outnumber the product quantity in the stock.'}, 400
        

        # 5. valid the delevery type
        if delivery_type != "delivery" and delivery_type != "pickup":
            return {'message': 'Invalid delivery type.'}, 400

        # 6. pass the check -> count for the total_price = (price * quantity) * n + dilevery fee
        # (1) count the delivery fee 
        #     - 距離(km)* 10 (若為自取運費為0)
        #     - 每筆訂單最低外送費$10
        #     - 金額計算完需四捨五入至整數
        delivery_fee = 0
        dist = 0
        if delivery_type == "delivery":
            # the distance between user and shop, unit-km
            dist = haversine((user.latitude, user.longitude), (shop.latitude, shop.longitude), unit=Unit.KILOMETERS)
            delivery_fee = dist*10
            delivery_fee = np.round(delivery_fee)   # default to be 0 decimal
            if delivery_fee < 10:
                delivery_fee = 10

        # (2) count the items price
        sub_total = 0
        for tuple in order_details:
            product_name = tuple[0]
            quantity = tuple[1]
            quantity = ast.literal_eval(quantity) # change the quantity into positive integer
            product = ProductModel.query.filter_by(belong_shop_name = order_shop_name, product_name = product_name).one_or_none()
            if not product: # 操作前(product.price)再確認一次，以防很快時間差內的資料庫改變程式出錯
                return {'message': 'The shop does not sell this product'}, 400
            sub_total += product.price * quantity
        
        total_price = sub_total + delivery_fee

        # **** 6.5 **** check total price same as front
        if total_price != front_total_price:
            return {'message': 'The total price has changed, please order again.'}, 400

        # 7. check user balance
        if user.balance < total_price:
            return {'message': 'The order\'s total price outnumber your balance. Please Recharge first.'}, 400

        # 8. operatae the database in a row -> *** transaction ***
        # *** the things about db is handed to model
        try: 
            """
            0. 先訂下交易時間
            1. 修改庫存數量 -> ProductModel.quantity

            --- here won't check total_price again -> directly +/- based on the total_price counted above -> ＊不會有損失發生＊
            2. (1) 修改 user 錢包  (2) 加一筆 user 交易紀錄
            3. (1) 修改 shop_owner 錢包  (2) 加一筆 shop_owner 交易紀錄
            ---

            4. 建立 Order
            5. 建立 OrderDetails
            """

            # 0. 先訂下交易時間
            nowtime = datetime.datetime.now() # 先訂下交易時間 -> transaction, order 
            time_string = nowtime.strftime("%Y-%m-%d %H:%M:%S")  # return type is string

            # 1. 修改庫存數量 -> 每個 product 都要改到
            for tuple in order_details:
                product_name = tuple[0]
                quantity = tuple[1]
                quantity = ast.literal_eval(quantity) # change the quantity into positive integer
                product = ProductModel.query.filter_by(belong_shop_name = order_shop_name, product_name = product_name).one_or_none()
                if product.quantity - quantity < 0:
                    raise   # 手動 raise exception
                else:
                    product.quantity -= quantity
                    product.flush_to_db()
        
            # 2. (1) 修改 user 錢包
            user = UserModel.query.filter_by(account = user_account).one_or_none() 
            if user.balance < total_price:
                raise
            else:
                user.balance -= total_price
                user.flush_to_db()

            # 2. (2) 加一筆 user 交易紀錄
            transaction_id_user = str(uuid.uuid4())
            # check that the id is not used since uuid4 is generated by the random number
            while TransactionModel.query.filter_by(transaction_id = transaction_id_user).one_or_none() != None:
                transaction_id_user = str(uuid.uuid4())
            transaction_user = TransactionModel(transaction_id_user, "payment", total_price, time_string, user.account, shop.shop_name) # tran_owner, store_name
            transaction_user.add_to_flush()

            # 3. (1) 修改 shop_owner 錢包  
            shop_owner = UserModel.query.filter_by(account = shop.owner).one_or_none()  # owner is user account
            shop_owner.balance += total_price
            shop_owner.flush_to_db()
            
            # 3. (2) 加一筆 shop_owner 交易紀錄
            transaction_id_shop_owner = str(uuid.uuid4())
            # check that the id is not used since uuid4 is generated by the random number
            while TransactionModel.query.filter_by(transaction_id = transaction_id_shop_owner).one_or_none() != None:
                transaction_id_shop_owner = str(uuid.uuid4())
            transaction_shop_owner = TransactionModel(transaction_id_shop_owner, "receive", total_price, time_string, shop_owner.account, user.account) # tran_owner, orderer
            transaction_shop_owner.add_to_flush()

            # 4. 建立 Order
            # self, order_id, status, start_time, end_time, delivery_type, delivery_distance, delivery_fee, sub_total, total, owner, shop_name
            """order 內有一條 order 就足夠 買家 & 店家查詢了，所以只會塞一條 order"""
            order_id =  str(uuid.uuid4())
            while OrderModel.query.filter_by(order_id = order_id).one_or_none() != None:
                order_id = str(uuid.uuid4())
            order = OrderModel(order_id, "Not Finish", time_string, "", delivery_type, dist, delivery_fee, sub_total, total_price, user.account, shop.shop_name)
            order.add_to_flush() # add new item into flush

            # 5. 建立 OrderDetails for each product
            for tuple in order_details:
                product_name = tuple[0]
                quantity = tuple[1]
                quantity = ast.literal_eval(quantity) # change the quantity into positive integer
                product = ProductModel.query.filter_by(belong_shop_name = order_shop_name, product_name = product_name).one_or_none()
                # (self, order_id, product_name, product_number, product_then_price, product_img_per_id):
                order_detail = OrderDetailsModel(order_id, product_name, quantity, product.price, product.img_per_id)
                order_detail.add_to_flush()

            # 6. commit all the flush in different models, represented by OrderModel
            OrderModel.commit_order_session()

            return {'message': 'Successfully made the order!'}, 200
            
        except Exception as e:   # catch 手動 raise exception
            print(e)    # print exception -> 自己 raise 好像是 none
            OrderModel.rollback_order_session()
            return {'message': 'Fault in db process! : ('}, 400




#----------------------------------------- filter / detail -----------------------------------------

# 5. 訂單詳情 order_detail
# ** order detail 的權限對 user, shop 是一樣的 **
# -> 直接看 OID 拿資料就好
class order_detail(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('order_id', type = str, required = True,    # order_id is enough -> it is primary key in order table
                        help = 'This field cannot be left blank.')

    @jwt_required(optional = True)
    def post(self):
        user_account = get_jwt_identity()
        # 1. check is valid user
        user = UserModel.query.filter_by(account = user_account).one_or_none() 
        if not user:
            return {'message': 'This user does not exist.'}, 400

        # unfold data and check
        data = order_detail.parser.parse_args()
        order_id     = data['order_id']

        # 2. 確認 order 存在
        order = OrderModel.query.filter_by(order_id = order_id).one_or_none() 
        if not order:
            return {'message': 'This order does not exist.'}, 400
        
        # 3. 確認 user 是該 order 的 (1)下單者 (2)下單店家擁有人  其一，管控查看權限 -> 防非前端駭客
        if not (order.owner == user.account):
            user_shop = ShopModel.query.filter_by(owner = user.account).one_or_none()    # 找出該 user 擁有的 shop
            # print(user_shop.shop_name, order.shop_name)
            if not user_shop:   # 如果不是下單者，確認該 user 是否擁有店家
                return {'message': 'Forbidden to access.'}, 403
            elif user_shop.shop_name != order.shop_name:    # & 該 user 擁有的 shop是下單店家   
                return {'message': 'Forbidden to access.'}, 403
        
        # 4. 成功返回 order detail
        # 找出所有 order_id 對應的 order_detail
        order_details = OrderDetailsModel.query.filter_by(order_id = order.order_id).all()    # 有很多筆
        if not order_details:
            return {'message': 'Can not find order details.'}, 400

        order_item_list = []
        for single_detail in order_details:
            # find the image base64 code for the order detail
            img_per = ImgPerModel.query.filter_by(per_id = single_detail.product_img_per_id).one_or_none()  # 只有一筆
            if not img_per:
                return {'message': 'Can not find the image base64 code for a image.'}, 400
            
            # query 都沒問題了
            info_list = [  img_per.base64,
                           single_detail.product_name,
                           single_detail.product_then_price,
                           single_detail.product_number, ]
            order_item_list.append(info_list)
        
        order_price_list = [order.sub_total, order.delivery_fee, order.total]
        
        return { 'order_item_detail': order_item_list,
                 'order_price_list' : order_price_list
        }, 200


# 6. user 訂單 filter
class order_user_filter(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('req_status', type = str, required = True,  
                        help = 'This field cannot be left blank.')

    @jwt_required(optional = True)
    def post(self):
        user_account = get_jwt_identity()
        # 1. check is valid user
        user = UserModel.query.filter_by(account = user_account).one_or_none() 
        if not user:
            return {'message': 'This user does not exist.'}, 400

        # unfold data and check
        data = order_user_filter.parser.parse_args()
        req_status     = data['req_status']

        # 2. req_status 錯誤
        if req_status != "Finished" and req_status != "Not Finish" and req_status != "Cancel": # 一個都對不上
            return {'message': 'The format of request status is wrong.'}, 400
        
        # 3. 成功取得 order, order.owner 是下單的人
        my_order_list = []
        all_order = OrderModel.query.filter_by(owner = user.account, status = req_status).all()  # query will return a list of tuple
        for single_order in all_order:
            action = []
            if single_order.status == "Not Finish": # only option: 未完成可取消
                action = ["cancel"]

            info_list = [ single_order.order_id,
                          single_order.status, 
                          single_order.start_time, 
                          single_order.end_time, 
                          single_order.shop_name,   # user 向誰下單
                          single_order.total,
                          action ]

            my_order_list.append(info_list)
        
        return {'my_order_list': my_order_list}, 200


# 7. shop 訂單 filter
class order_shop_filter(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('req_status', type = str, required = True,  
                        help = 'This field cannot be left blank.')

    @jwt_required(optional = True)
    def post(self):
        user_account = get_jwt_identity()
        # 1. check is valid user
        user = UserModel.query.filter_by(account = user_account).one_or_none() 
        if not user:
            return {'message': 'This user does not exist.'}, 400

        # unfold data and check
        data = order_shop_filter.parser.parse_args()
        req_status    = data['req_status']

        # 2. shop 不存在 
        shop = ShopModel.query.filter_by(owner = user.account).one_or_none()
        if not shop:
            return {'message': 'This user does not have a shop.'}, 400

        # 3. req_status 錯誤
        if req_status != "Finished" and req_status != "Not Finish" and req_status != "Cancel": # 一個都對不上
            return {'message': 'The format of request status is wrong.'}, 400
        
        # 4. 成功取得 order, order.owner 是下單的人
        shop_order_list = []
        all_order = OrderModel.query.filter_by(shop_name = shop.shop_name, status = req_status).all()  # query will return a list of tuple
        for single_order in all_order:
            action = []
            if single_order.status == "Not Finish": # only option: 未完成可取消、未完成可以完成
                action = ["cancel", "done"]

            info_list = [ single_order.order_id,
                          single_order.status, 
                          single_order.start_time, 
                          single_order.end_time, 
                          single_order.owner,   # shop 被誰下訂單
                          single_order.total,
                          action ]

            shop_order_list.append(info_list)
        
        return {'shop_order_list': shop_order_list}, 200
        