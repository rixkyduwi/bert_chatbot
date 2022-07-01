from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
app = Flask(__name__)
SERVER_NAME = '192.168.100.63:5000'
app.config['SERVER_NAME']=SERVER_NAME
app.config['SECRET_KEY'] = 'secret-key-goes-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bigprojeks2.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= True
app.config.update(dict(
SECRET_KEY="powerful secretkey",
WTF_CSRF_SECRET_KEY="a csrf secret key"
    ))
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message = u"selamat datang"
login_manager.login_message_category = "info"
login_manager.init_app(app)
db.init_app(app)
from application.models import ADMIN,SISWA,HISTORY,GURU

@login_manager.user_loader
def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return ADMIN.query.get(int(user_id))
    # blueprint for auth routes in our app
from application.auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

# blueprint for non-auth parts of app
from application.main import main as main_blueprint
app.register_blueprint(main_blueprint)

login_manager.init_app(app)
db.init_app(app)

