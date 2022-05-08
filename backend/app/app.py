from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api

import config_secret

from resources.user import auth_register, auth_login

from flask_cors import CORS

app = Flask(__name__)

# 0. set app to not be block
CORS(app)

# 1. connect to db
# from sqlalchemy import create_engine
# engine = create_engine('postgresql://scott:tiger@localhost:8080/mydatabase')
# basedir= os.path.abspath(os.path.dirname(__file__))
# app.config['SQLALCHEMY_DATABASE_URI'] = os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/yoona/Documents/4th_Sem/sql/HW2/UberEat-Booking-System/backend/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 3. jwt
jwt = JWTManager(app)
app.config['JWT_SECRET_KEY'] = config_secret.jwt_secret_key


# 2. create table in db
@app.before_first_request
def create_tables():
    from app.db import db
    # db.app = app
    from models.user import UserModel
    db.init_app(app)
    db.create_all()


# 4. api & URL
api = Api(app)
api.add_resource( auth_register,  "/auth/register")
api.add_resource( auth_login,  "/auth/login")


if __name__ == '__main__':
    app.run( debug = True )
