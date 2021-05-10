from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_marshmallow import Marshmallow


from .config import Config

app = Flask(__name__)
app.config.from_object(Config)




# Flask-Login login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
db = SQLAlchemy(app)
ma = Marshmallow(app)
socketio = SocketIO(app)


from app import views
