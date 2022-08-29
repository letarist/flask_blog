import os
from secrets import token_hex
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from blog import mail


def save_picture(from_picture):
    random_hex = token_hex(8)
    _, f_ext = os.path.splitext(from_picture.filename)
    picture_check = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_check)

    size = (100, 100)
    image = Image.open(from_picture)
    image.thumbnail(size)
    image.save(picture_path)

    return picture_check


def send_reset_email(user):
    token = user.reset_token()
    message = Message('Запрос на смену пароля', sender='freedayz@rambler.ru', recipients=[user.email])
    message.body = f'Чтобы сбросить пароль перейдите по ссылке {url_for("users.reset_password", token=token, _external=True)}'
    mail.send(message)
