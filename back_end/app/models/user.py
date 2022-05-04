from app.db import db
from werkzeug.security import hmac

class UserModel(db.Model):
    __tablename__ = 'user'

    # now is no limit of length (not sure if is ok for sqlite) <fix>
    account = db.Column(db.String(), unique = True, nullable = False)
    password = db.Column(db.String(), nullable = False)
    username = db.Column(db.String(), nullable = False)
    phone_number = db.Column(db.String(10), nullable = False)
    latitude = db.Column(db.Float(), nullable = False)
    longitude = db.Column(db.Float(), nullable = False)


    # foreign key part, later, wail until we have other models

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
        return hmac.compare_digest(self.password, password)

    @classmethod
    def find_by_account(cls, account):
        return cls.query.filter_by(account=account).first()
        