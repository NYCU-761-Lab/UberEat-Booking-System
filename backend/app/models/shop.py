from app.db import db

class ShopModel(db.Model):
    __tablename__ = 'shop'

    # string limit length: 256
    shop_name = db.Column(db.String(256), unique = True, nullable = False, primary_key = True)
    shop_type = db.Column(db.String(256), nullable = False)
    latitude = db.Column(db.Float(256), nullable = False)
    longitude = db.Column(db.Float(256), nullable = False)

    # foreign key part, later, wail until we have other models
    # db.ForeignKey('table_name.primary_key'), table_name seems like no need to import
    user_account = db.Column(db.String(256), db.ForeignKey('user.account'), unique = True, nullable = False)
    
    def __init__(self, shop_name, latitude, longitude, shop_type):
        self.shop_name = shop_name
        self.latitude = latitude
        self.longitude = longitude
        self.shop_type = shop_type

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_shop_name(cls, shop_name):
        return cls.query.filter_by(shop_name=shop_name).first()
