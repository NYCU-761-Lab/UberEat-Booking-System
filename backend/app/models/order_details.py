from app.db import db

class OrderDetailsModel(db.Model):
    __tablename__ = 'order_details'
    __table_args__ = {'extend_existing': True}

    # either one of the composite primary key no need to be unique
    order_id = db.Column(db.String(256), db.ForeignKey('order.order_id'), nullable = False, primary_key = True)
    # ***** 10 stars *****
    # still store and be the "primary key", just simply store the product_name and not be the "foreignkey"(when delete product -> something wrong)
    product_name = db.Column(db.String(256), nullable = False, primary_key = True)
    product_number = db.Column(db.Integer(), nullable = False)
    product_then_price = db.Column(db.Float(256), nullable = False)
    product_img_per_id = db.Column(db.String(256), db.ForeignKey('img_per.per_id'), nullable = False) # no need to be unique
    
    def __init__(self, order_id, product_name, product_number, product_then_price, product_img_per_id):
        self.order_id = order_id                # 訂單編號
        self.product_name = product_name        # 訂單內的 "單項" 商品
        self.product_number = product_number    # 該 "單項" 商品的數量
        self.product_then_price = product_then_price    # 商品當時價格
        self.product_img_per_id = product_img_per_id    # 商品當時圖片的 img_per_id


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def add_to_flush(self): # add the "whole" object, not edit the existing object
        db.session.add(self)
        db.session.flush()