from app.db import db

# use to record the permanent base64 code of a image
class ImgPerModel(db.Model):
    __tablename__ = 'img_per'
    __table_args__ = {'extend_existing': True}

    # either one of the composite primary key no need to be unique
    per_id = db.Column(db.String(256), nullable = False, primary_key = True)
    base64 = db.Column(db.String(), nullable = False)   # the limit is 2^31 - 1

    # 給 order_details 的 backref, product image 的 per_id
    db_img_per_product = db.relationship("ProductModel", backref="img_per")
    db_img_per_order_details = db.relationship("OrderDetailsModel", backref="img_per")


    def __init__(self, per_id, base64):
        self.per_id = per_id        # image permanent id
        self.base64 = base64        # image base64 code
    

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def add_to_flush(self): # add the "whole" object, not edit the existing object
        db.session.add(self)
        db.session.flush()