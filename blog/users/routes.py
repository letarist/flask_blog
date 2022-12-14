from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from blog import db, bcrypt
from blog.models import User, Post
from blog.users.forms import RegForm, ResetPasswordForm, ResetEmailForm, LoginForm, EditForm
from blog.users.utils import save_picture, send_reset_email

users = Blueprint('users', __name__)


@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('posts.all_posts'))
    form = RegForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Учетная запись успешно создана!', 'success')
        return redirect(url_for('posts.all_posts'))
    return render_template('register.html', title='Register', form=form)


@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('posts.all_posts'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('posts.all_posts'))
        else:
            flash('Введены неверные данные', 'Внимание')
    return render_template('login.html', title='Вход', form=form)


@users.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
        return redirect(url_for('main.main_page'))


@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = EditForm()
    if form.validate_on_submit():
        if form.avatars.data:
            picture_file = save_picture(form.avatars.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Ваш аккаунт был обновлен!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        page = request.args.get('page', 1, type=int)
        user = User.query.filter_by(username=form.username.data).first_or_404()
        posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@users.route('/user/<string:username>')
@login_required
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=3)
    return render_template('user_posts.html', posts=posts, user=user)


@users.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if current_user.is_authenticated:
        return redirect(url_for('posts.all_posts'))
    form = ResetEmailForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('Письмо о смене пароля отправлено на почту')
        return redirect(url_for('main.main_page'))
    return render_template('reset_password.html', title='Сброс пароля', form=form)


@users.route('/reset_password/<token>',methods=['GET','POST'])
def reset_token(token):
    user = User.confirm_token(token)
    if user is None:
        flash('Недействительный токен', 'warning')
        return redirect(url_for('posts.all_posts'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_pass
        db.session.commit()
        flash('Ваш пароль был заменен','success')
        return redirect(url_for('posts.all_posts'))
    return render_template('reset_token.html',title='Сброс пароля',form=form)
