from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from flask_login import current_user
from blog.models import User


class RegForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(min=2, max=15)])
    email = StringField('Ваша почта: ', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Введите пароль еще раз', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Пользователь с таким именем уже существует')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('Эта почта уже занята')


class LoginForm(FlaskForm):
    email = StringField('Ваша почта', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember = BooleanField('Напомнить пароль')
    submit = SubmitField('Войти')


class EditForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(min=2, max=15)])
    email = StringField('Почта', validators=[DataRequired(), Email()])
    avatars = FileField('Обновить аватарку', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Изменить информацию')

    def validate_username(self, username):
        if username != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Имя занято')

    def validate_email(self, email):
        if email != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Пользователь с такой почой уже зарегистрирован')


class ResetEmailForm(FlaskForm):
    email = StringField('Почта', validators=[DataRequired(), Email()])
    submit = SubmitField('Отправить')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('Аккаунт на данную почту не зарегистрирован')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Повтор пароля', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Поменять пароль')
