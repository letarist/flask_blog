from blog.models import User
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, SubmitField
from wtforms.validators import DataRequired, Length


class CreatePost(FlaskForm):
    title = StringField('Название', validators=[DataRequired(), Length(min=5)])
    text = TextAreaField('Текст блога', validators=[DataRequired()])
    submit = SubmitField('Опубликовать')
