from datetime import datetime, timedelta
from flaskblog import db, login_manager
from flask_migrate import Migrate
from flask_login import UserMixin
from flask import current_app
import jwt

@login_manager.user_loader
def load_user(user_id): 
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    # id is primary key
    id = db.Column(db.Integer, primary_key=True)
    # 20 is max length
    username = db.Column(db.String(20), unique=True, nullable=False)
    # 120 is max length
    email = db.Column(db.String(120), unique=True, nullable=False)
    # image_file is default
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    # password is 60 characters long
    password = db.Column(db.String(128), nullable=False)
    # posts is a relationship
    posts = db.relationship('Post', backref='author', lazy=True)
    # confirmed is a boolean
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    # is_admin is a boolean
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    def get_reset_token(self, expires_sec=1800):
        payload = {'user_id': self.id, 'exp': datetime.utcnow() + timedelta(seconds=expires_sec)}
        secret_key = current_app.config['SECRET_KEY']
        token = jwt.encode(payload, secret_key, algorithm='HS256')
        return token

    @staticmethod
    def verify_reset_token(token):
        secret_key = current_app.config['SECRET_KEY']
        try:
            payload = jwt.decode(token, secret_key, algorithms=['HS256'])
            user_id = payload['user_id']
        except jwt.exceptions.ExpiredSignatureError:
            return None  # token has expired
        except jwt.exceptions.InvalidSignatureError:
            return None  # token is invalid
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"

class Post(db.Model):
    # id is primary key
    id = db.Column(db.Integer, primary_key=True)
    # 100 is max length
    title = db.Column(db.String(100), nullable=False)
    # date_posted is a date
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # content is a text
    content = db.Column(db.Text, nullable=False)
    # user_id is a foreign key
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}','{self.date_posted}')"
