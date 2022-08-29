from pathlib import Path
import os

BASE_DIR = Path(__file__).parent
dot_env = BASE_DIR / '.env'


class Conf:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SECRET_KEY = '95739fj5nfgirnsh49503m38mndp43'
    # MAIL_SERVER = os.getenv('MAIL_SERVER')
    # MAIL_PORT = os.getenv('MAIL_PORT')
    # MAIL_USE_TLS = os.getenv('MAIL_USE_TLS')
    # MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    # MAIL_PASSWORD = os.getenv('MAIL_USERNAME')
    MAIL_SERVER = 'smtp.rambler.ru'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USERNAME = 'freedayz@rambler.ru'
    MAIL_PASSWORD = '121212Qwer'
