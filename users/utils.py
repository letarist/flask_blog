import os
from secrets import token_hex
from PIL import Image
from flask import url_for, current_app


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
