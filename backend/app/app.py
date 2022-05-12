from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_cors import CORS

import config_secret
from resources.user import auth_register, auth_login, auth_check_account, auth_account_information, auth_location
from resources.shop import shop_register, shop_name_filter, shop_distance_filter, shop_type_filter, get_shop_type, get_shop_distance, get_shop_latitude, get_shop_longitude, get_shop_name_of_user

app = Flask(__name__)

# 0. set app to not be block
CORS(app)

# 1. connect to db
# for future engine
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
    from models.shop import ShopModel
    from models.product import ProductModel
    db.init_app(app)
    db.create_all()

    """Future need to add migrate to migrate new and old db"""
    # migrate = Migrate(app, db)


# 4. api & URL
api = Api(app)

# user api
api.add_resource( auth_register,  "/auth/register")
api.add_resource( auth_login,  "/auth/login")
api.add_resource( auth_check_account,  "/auth/check_account")
api.add_resource( auth_account_information, "/auth/get_account_info") # original: /auth/info (如果一次都沒改過的話是 /auth)
api.add_resource( auth_location, "/auth/edit_location") # original: /auth/location

# shop api
api.add_resource( shop_register, "/shop/register")
api.add_resource( shop_name_filter, "/shop/name_filter")
api.add_resource( shop_distance_filter, "/shop/distance_filter")
api.add_resource( shop_type_filter, "/shop/type_filter")

api.add_resource( get_shop_type, "/shop/get_shop_type")
api.add_resource( get_shop_distance, "/shop/get_shop_distance")
api.add_resource( get_shop_latitude, "/shop/get_shop_latitude")
api.add_resource( get_shop_longitude, "/shop/get_shop_longitude")
api.add_resource( get_shop_name_of_user, "/shop/get_shop_name_of_user")




if __name__ == '__main__':
    app.run( debug = True )
