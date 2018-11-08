import logging
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from .config import Config

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
logging.getLogger().setLevel(logging.DEBUG)

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
login_manager = LoginManager()


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

login_manager.init_app(app)
bootstrap.init_app(app)
mail.init_app(app)
moment.init_app(app)

login_manager.login_view = 'login_page'
login_manager.login_message = 'please login!'
login_manager.session_protection = 'strong'
login_manager.login_message='pls login to access this page'


from app import views
