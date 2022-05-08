from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, get_jwt, set_access_cookies
from datetime import datetime
from datetime import timedelta
from datetime import timezone

from app.resources.user import Auth, Auth_login
import configSecret


app = Flask(__name__)

# 1. connect to db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/yoona/Documents/noteweb_backend/database.db'

# 2. create table in db
@app.before_first_request
def create_tables():
    from app.db import db   
    db.init_app(app)
    db.create_all()

# 3. jwt
jwt = JWTManager(app)
app.config['JWT_SECRET_KEY'] = configSecret.jwt_secret_key

# 4. api & URL
api = Api(app)
api.add_resource( Auth,  "/auth/")
api.add_resource( Auth_login,  "/auth/login")


if __name__ == '__main__':
    app.run( debug = True )