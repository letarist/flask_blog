from flask import render_template, Blueprint
from blog.models import User

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def main_page():
    from pathlib import Path
    from dotenv import load_dotenv
    import os

    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    dot_env = BASE_DIR / '.env'
    print(f'BASED----------------{dot_env}')
    return render_template('index.html')


@main.route('/contacts')
def contact():
    return render_template('contact.html')
