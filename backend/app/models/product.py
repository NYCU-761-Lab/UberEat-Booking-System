from app.db import db

class ProductModel(db.Model):
    __tablename__ = 'product'
    __table_args__ = {'extend_existing': True}

    # composite primary key: (product_name, belong_shop_name) -> this tuple need to be unique -> no need product_id anymore
    # product_name & shop_name & owner any single of them need to be unique!!!!
    product_name = db.Column(db.String(256), nullable = False, primary_key = True)
    picture = db.Column(db.String(256), nullable = False)
    price = db.Column(db.Float(256), nullable = False)
    quantity = db.Column(db.Integer(), nullable = False)  # need to be int
    
    # db.ForeignKey('table_name.primary_key')
    # These 2 no need not to be unique!!! -> we can have multiple products belong to a shop or owner
    owner = db.Column(db.String(256), db.ForeignKey('user.account'), nullable = False)
    belong_shop_name = db.Column(db.String(256), db.ForeignKey('shop.shop_name'), nullable = False, primary_key = True)
    
    def __init__(self, product_name, picture, price, quantity, user_account, shop_name):
        self.product_name = product_name
        self.picture = picture            # url of local host to access the picture
        self.price = price
        self.quantity = quantity
        self.owner = user_account
        self.belong_shop_name = shop_name

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_product_name(cls, product_name):
        return cls.query.filter_by(product_name=product_name).first()

    @classmethod
    def edit_price(cls, product_name, belong_shop_name, edit_price):
        query = cls.query.filter_by(product_name=product_name, belong_shop_name = belong_shop_name).first()
        query.price = edit_price
        db.session.commit()

    @classmethod
    def edit_quantity(cls, product_name, belong_shop_name, edit_quantity):
        query = cls.query.filter_by(product_name=product_name, belong_shop_name = belong_shop_name).first()
        query.quantity = edit_quantity
        db.session.commit()
    
    @classmethod
    def delete_product(cls, product_name, belong_shop_name):
        query = cls.query.filter_by(product_name=product_name, belong_shop_name = belong_shop_name).first()
        db.session.delete(query)
        db.session.commit()
