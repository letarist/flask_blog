from datetime import datetime, timezone, timedelta
from jwt import encode, decode
from blog import db, users_manager
from flask import current_app
from flask_login import UserMixin, current_user


@users_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    image_file = db.Column(db.String(50), nullable=False, default='default_picture.jpg')
    password = db.Column(db.String(50), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def reset_token(self, expirations=1800):
        reset_token = encode({"confirm": self.id, "exp": datetime.now(tz=timezone.utc) + timedelta(seconds=expirations)},
            current_app.config['SECRET_KEY'],
            algorithm="HS256"
            )
        return reset_token

    @staticmethod
    def confirm_token(token):
        try:
            data = decode(
                token,
                current_app.config['SECRET_KEY'],
                conf_time=timedelta(seconds=10),
                algorithms="HS256"
            )
        except:
            return False
        if data.get('confirm') != current_user.id:
            return False
        return User.query.get(data.get('confirm'))


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
