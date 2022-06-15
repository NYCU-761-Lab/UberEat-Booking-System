from app.db import db

class OrderDetailsModel(db.Model):
    __tablename__ = 'order_details'
    __table_args__ = {'extend_existing': True}

    # either one of the composite primary key no need to be unique
    order_id = db.Column(db.String(256), db.ForeignKey('order.order_id'), nullable = False, primary_key = True)
    product_name = db.Column(db.String(256), db.ForeignKey('product.product_name'), nullable = False, primary_key = True)
    product_number = db.Column(db.Integer(), nullable = False)
    
    def __init__(self, order_id, product_name, product_number):
        self.order_id = order_id                # 訂單編號
        self.product_name = product_name        # 訂單內的 "單項" 商品
        self.product_number = product_number    # 該 "單項" 商品的數量

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def add_to_flush(self): # add the "whole" object, not edit the existing object
        db.session.add(self)
        db.session.flush()