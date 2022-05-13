from app.db import db

class ProductModel(db.Model):
    __tablename__ = 'product'
    __table_args__ = {'extend_existing': True}


    # string limit length: 256
    # the picture will store as the url(String type) to access it, 
    # "file route" + "product_id", use product_id.jpg as its name
    product_id = db.Column(db.String(32), unique = True, nullable = False, primary_key = True)
    product_name = db.Column(db.String(256), nullable = False)
    picture = db.Column(db.String(256), nullable = False)
    price = db.Column(db.Float(256), nullable = False)
    quantity = db.Column(db.Integer(), nullable = False)  # need to be int
    
    # foreign key part, later, wail until we have other models
    # db.ForeignKey('table_name.primary_key')
    owner = db.Column(db.String(256), db.ForeignKey('user.account'), unique = True, nullable = False)
    belong_shop_name = db.Column(db.String(256), db.ForeignKey('shop.shop_name'), unique = True, nullable = False)
    
    def __init__(self, product_id, product_name, picture, price, quantity, user_account, shop_name):
        self.product_id = product_id
        self.product_name = product_name
        self.picture = picture
        self.price = price
        self.quantity = quantity
        self.owner = user_account
        self.belong_shop_name = shop_name

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_product_id(cls, product_id):
        return cls.query.filter_by(product_id=product_id).first()
