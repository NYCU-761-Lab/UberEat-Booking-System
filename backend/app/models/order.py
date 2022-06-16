from app.db import db

class OrderModel(db.Model):
    __tablename__ = 'order'
    __table_args__ = {'extend_existing': True}

    order_id = db.Column(db.String(256), nullable = False, primary_key = True, unique = True) # need to be unique
    status = db.Column(db.String(256), nullable = False)
    start_time = db.Column(db.String(256), nullable = False)
    end_time = db.Column(db.String(256), nullable = False)  # will be "" if the order is not "Finised" status
    delivery_type = db.Column(db.String(256), nullable = False)
    delivery_distance = db.Column(db.Float(), nullable = False)
    delivery_fee = db.Column(db.Float(), nullable = False)
    sub_total = db.Column(db.Float(), nullable = False)
    total = db.Column(db.Float(), nullable = False)
    
    # 訂單擁有人  *是下單的使用者*
    owner = db.Column(db.String(256), db.ForeignKey('user.account'), nullable = False)
    # 下單店家
    shop_name = db.Column(db.String(256), db.ForeignKey('shop.shop_name'), nullable = False) # 應該不用設成 foreign key, 因為有可能是店名或使用者，單一型態難處理

    # 給 order_details 的 backref, order table 內的 order_details backref
    db_order_order_details = db.relationship("OrderDetailsModel", backref="order")

    def __init__(self, order_id, status, start_time, end_time, delivery_type, delivery_distance, delivery_fee, sub_total, total, owner, shop_name):
        self.order_id = order_id
        self.status = status
        self.start_time = start_time
        self.end_time = end_time
        self.delivery_type = delivery_type
        self.delivery_distance = delivery_distance
        self.delivery_fee = delivery_fee
        self.sub_total = sub_total
        self.total = total
        self.owner = owner          # 訂單擁有人
        self.shop_name = shop_name  # 下單店家

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def add_to_flush(self): # add the whole object, not edit the existing object
        db.session.add(self)
        db.session.flush()
    
    def flush_to_db(self): # add the whole object, not edit the existing object
        db.session.flush()

    # session.begin() can't use and didn't adopt by me
    @classmethod  # can be called by the class
    def begin_order_session(self):
        db.session.begin()
        # with db.session.begin():
    
    @classmethod
    def commit_order_session(self):
        db.session.commit()
    
    @classmethod
    def rollback_order_session(self):
        db.session.rollback()
