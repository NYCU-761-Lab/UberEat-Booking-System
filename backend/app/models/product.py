from app.db import db

class ProductModel(db.Model):
    __tablename__ = 'product'

    # string limit length: 256
    # the picture will store as the url(String type) to access it, 
    # "file route" + "product_id", use product_id.jpg as its name
    product_id = db.Column(db.String(32), unique = True, nullable = False, primary_key = True)
    product_name = db.Column(db.String(256), nullable = False)
    picture = db.Column(db.String(256), nullable = False)
    price = db.Column(db.Float(256), nullable = False)
    quantity = db.Column(db.Integer(256), nullable = False)  # need to be int
    
    # foreign key part, later, wail until we have other models
    # db.ForeignKey('table_name.primary_key')
    user_account = db.Column(db.String(256), db.ForeignKey('user.account'), unique = True, nullable = False)
    shop_name = db.Column(db.String(256), db.ForeignKey('shop.shop_name'), unique = True, nullable = False)
    
    def __init__(self, product_id, product_name, picture, price, quantity):
        self.product_id = product_id
        self.product_name = product_name
        self.picture = picture
        self.price = price
        self.quantity = quantity

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_product_id(cls, product_id):
        return cls.query.filter_by(product_id=product_id).first()
