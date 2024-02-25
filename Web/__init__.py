from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt


db = SQLAlchemy()
app = Flask(__name__)
login_manager = LoginManager(app)
bcrypt = Bcrypt(app)
app.config.from_object("config")
db.init_app(app)

login_manager.login_message = "Először be kell jelentkezned!"
login_manager.login_message_category = "warning"
login_manager.login_view = "login"

from Web import routes