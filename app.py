from flask import Flask, request, jsonify, flash, g
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from flask_login import LoginManager, login_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import time

from config import service_conf

app = Flask(__name__)
app.config['SECRET_KEY'] = service_conf.secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = service_conf.database
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CAPTCHA_WEBSITE_KEY= service_conf.captcha_web_site_key
CAPTCHA_SERVER_KEY= service_conf.captcha_site_key
AVILABLE_SOFTWARE_JSON="config/available_software.json"

# db
db = SQLAlchemy(app)

#Basic Auth for API
auth = HTTPBasicAuth()

#Login for GUI
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

from contextlib import contextmanager

@contextmanager
def no_expire():
    s = db.session()
    s.expire_on_commit = False
    try:
        yield
    finally:
        s.expire_on_commit = True

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(32), index = True)
    password_hash = db.Column(db.String(64))
    email = db.Column(db.String(100))

    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def generate_auth_token(self, expires_in=600):
        return jwt.encode(
            {'id': self.id, 'exp': time.time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def check_and_log_user(username, password, remember):
    user = User.query.filter_by(username=username).first()
    if not user:
        return False
    if user.verify_password(password):
        login_user(user, remember=remember)
        return True 
    else:
        return False
  
def verify_auth_token(token):
    try:
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
    except:
        return
    return User.query.get(data['id'])

@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username=username_or_token).first()
        if not user:
            flash("Username not found or token not valid")
            return False       
        if not user.verify_password(password):
            flash("Password incorrect")
            return False
    g.user = user
    return True

def create_app():
    login_manager.init_app(app)

    from blueprints.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from blueprints.dashboard import dashboard as dashboard_blueprint
    app.register_blueprint(dashboard_blueprint)

    from blueprints.api import api as api_blueprint
    app.register_blueprint(api_blueprint)
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

