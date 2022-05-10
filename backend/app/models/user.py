from app.db import db
from werkzeug.security import check_password_hash

 # need to find from the root app, or will have circular import
from app.models.shop import ShopModel
from app.models.product import ProductModel

class UserModel(db.Model):
    __tablename__ = 'user'

    # string limit length: 256
    account = db.Column(db.String(256), unique = True, nullable = False, primary_key = True)
    password = db.Column(db.String(256), nullable = False)
    username = db.Column(db.String(256), nullable = False)
    phone_number = db.Column(db.String(10), nullable = False)
    latitude = db.Column(db.Float(256), nullable = False)
    longitude = db.Column(db.Float(256), nullable = False)
    role = db.Column(db.String(10), nullable = False)


    # foreign key part, later, wail until we have other models
    # we can get the user information by
    # ShopModel.user or ProductModel.user
    db_user_shop = db.relationship("ShopModel", backref="user")
    db_user_shop = db.relationship("ProductModel", backref="user")

    def __init__(self, account, password, username, phone_number, latitude, longitude, role):
        self.account = account
        self.password = password
        self.username = username
        self.phone_number = phone_number
        self.latitude = latitude
        self.longitude = longitude
        self.role = role

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @classmethod
    def find_by_account(cls, account):
        return cls.query.filter_by(account=account).first()
    
    @classmethod
    def edit_location(cls, account, latitude, longitude):
        query = cls.query.filter_by(account=account).first()
        query.latitude = latitude
        query.longitude = longitude
        db.session.commit()