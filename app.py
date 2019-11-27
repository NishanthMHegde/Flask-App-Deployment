import os
from flask import Flask
from flask_restful import Resource,Api
from flask_jwt import JWT
from security import authenticate,identity
from resources.userregister import UserRegister
from resources.item import Item
from resources.itemlist import ItemsList
from resources.store import Store
from resources.storelist import StoreList

app = Flask(__name__)
#create a secret key for app for encoding purpose
app.secret_key = "nishanth"
#load the DATABASE_URL sent by Heroku Postgres and if not available, only then load sqlite db.
#psycopg2 is needed for interaction between Heroku Postgresql and app.
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
#use below database uri only when using sqliteDB from SQLAlchemy
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#create table before every request is fired. This elminates the need to create tables all the time
#This will automatically create table with fields specified in the model before first request is fired 



#add our app to our API
api = Api(app)
#add the authenticate and identity methods we created in security. 
"""
this results in looking for an /auth endpoint request which has body like:
{
	"username": "username",
	"password": "password"
}
"""
jwt = JWT(app, authenticate, identity)  
#an items list which is globally accessible
# items = []

#add our resources to our API and also specify the common endpoints for all our HTTP requests
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemsList, '/items')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')

#run our app only if this app.py file is called as the main function
if __name__ == "__main__":
	from db import db
	db.init_app(app)
	app.run(port=5002)