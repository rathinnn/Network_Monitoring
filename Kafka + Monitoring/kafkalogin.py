# init.py
from flask import Flask
from flask_login import LoginManager 
from api import api as api_blueprint
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from db import db

def getdb():
    return db

app = Flask(__name__)

app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

from models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)


from main import main as main_blueprint
app.register_blueprint(main_blueprint)

app.register_blueprint(api_blueprint)



