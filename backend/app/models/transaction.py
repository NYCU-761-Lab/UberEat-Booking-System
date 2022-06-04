from app.db import db

class TransactionModel(db.Model):
    __tablename__ = 'transaction'
    __table_args__ = {'extend_existing': True}

    transaction_id = db.Column(db.String(256), nullable = False, primary_key = True, unique = True) # need to be unique
    type = db.Column(db.String(256), nullable = False)
    amount_of_money = db.Column(db.Float(), nullable = False)
    time = db.Column(db.String(256), nullable = False)
    
    # 訂單擁有人
    owner = db.Column(db.String(256), db.ForeignKey('user.account'), nullable = False)
    # 交易對象
    trader = db.Column(db.String(256), nullable = False) # 應該不用設成 foreign key, 因為有可能是店名或使用者，單一型態難處理

    def __init__(self, transaction_id, type, amount_of_money, time, owner, trader):
        self.transaction_id = transaction_id
        self.type = type
        self.amount_of_money = amount_of_money
        self.time = time
        self.owner = owner      # 訂單擁有人
        self.trader = trader    # 交易對象

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
