from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from blog.config import Conf
from flask_mail import Mail

db = SQLAlchemy()
users_manager = LoginManager()
bcrypt = Bcrypt()
mail = Mail()


def create_application(config_class=Conf):
    application = Flask(__name__)
    application.config.from_object(Conf)
    bcrypt.init_app(application)
    mail.init_app(application)
    from blog.mainapp.routes import main
    from users.routes import users
    from posts.routes import posts
    application.register_blueprint(posts)
    application.register_blueprint(users)
    application.register_blueprint(main)
    users_manager.init_app(application)
    db.init_app(application)
    return application
