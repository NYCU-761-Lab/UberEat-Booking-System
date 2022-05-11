from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_cors import CORS

import config_secret
from resources.user import auth_register, auth_login, auth_check_account, auth_account_information, auth_location

app = Flask(__name__)

# 0. set app to not be block
CORS(app)

# 1. connect to db
# from sqlalchemy import create_engine

# engine = create_engine('postgresql://scott:tiger@localhost:8080/mydatabase')
# basedir= os.path.abspath(os.path.dirname(__file__))
# app.config['SQLALCHEMY_DATABASE_URI'] = os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/yoona/Documents/4th_Sem/sql/HW2_new/UberEat-Booking-System/backend/database.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/angelahsi/UberEat-Booking-System/backend/database.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 3. jwt
app.config['JWT_SECRET_KEY'] = config_secret.jwt_secret_key
# for future formal logout
# ACCESS_EXPIRES = timedelta(hours=2)
# app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES
jwt = JWTManager(app)
# jwt_redis_blocklist = redis.StrictRedis(
#     host="localhost", port=8080, db=0, decode_responses=True
# )


# 2. create table in db
@app.before_first_request
def create_tables():
    from app.db import db
    # db.app = app
    from models.user import UserModel
    # from models.shop import ShopModel
    # from models.product import ProductModel
    db.init_app(app)
    db.create_all()

    """Future need to add migrate to migrate new and old db"""
    # migrate = Migrate(app, db)


# 4. api & URL
api = Api(app)
api.add_resource( auth_register,  "/auth/register")
api.add_resource( auth_login,  "/auth/login")
api.add_resource( auth_check_account,  "/auth/check_account")
api.add_resource( auth_account_information, "/auth/info")
api.add_resource( auth_location, "/auth/location")

if __name__ == '__main__':
    app.run( debug = True )
