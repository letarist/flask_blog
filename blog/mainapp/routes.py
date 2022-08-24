from flask import render_template, Blueprint
from blog.models import User

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def main_page():
    return render_template('index.html')


@main.route('/contacts')
def contact():
    return render_template('contact.html')
