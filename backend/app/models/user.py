from app.db import db
from werkzeug.security import check_password_hash

 # need to find from the root app, or will have circular import
from app.models.shop import ShopModel

class UserModel(db.Model):
    __tablename__ = 'user'

    # now is no limit of length (not sure if is ok for sqlite) <fix>
    account = db.Column(db.String(256), unique = True, nullable = False, primary_key = True)
    password = db.Column(db.String(256), nullable = False)
    username = db.Column(db.String(256), nullable = False)
    phone_number = db.Column(db.String(10), nullable = False)
    latitude = db.Column(db.Float(256), nullable = False)
    longitude = db.Column(db.Float(256), nullable = False)


    # foreign key part, later, wail until we have other models
    db_user_shop = db.relationship("ShopModel", backref="user")

    def __init__(self, account, password, username, phone_number, latitude, longitude):
        self.account = account
        self.password = password
        self.username = username
        self.phone_number = phone_number
        self.latitude = latitude
        self.longitude = longitude

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @classmethod
    def find_by_account(cls, account):
        return cls.query.filter_by(account=account).first()
