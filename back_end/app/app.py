from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api, Resource

from app.resources.user import Auth, Auth_login
import config_secret


app = Flask(__name__)

# 1. connect to db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/yoona//4th_Sem/sql/HW2/UberEat-Booking-System/database.db'

# 2. create table in db
@app.before_first_request
def create_tables():
    from app.db import db   
    db.init_app(app)
    db.create_all()

# 3. jwt
jwt = JWTManager(app)
app.config['JWT_SECRET_KEY'] = config_secret.jwt_secret_key

# 4. api & URL
api = Api(app)
api.add_resource( Auth,  "/auth/")
api.add_resource( Auth_login,  "/auth/login")


if __name__ == '__main__':
    app.run( debug = True )