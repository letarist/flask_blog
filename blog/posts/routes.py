from blog.models import User, Post
from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from blog import db
from .forms import CreatePost

posts = Blueprint('posts', __name__)


@posts.route("/allposts")
def all_posts():
    page = request.args.get('page', type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=3)
    return render_template('all_posts.html', posts=posts)


@posts.route('/createpost/new', methods=['POST', 'GET'])
@login_required
def new_post():
    form = CreatePost()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.text.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Вы создали пост', 'Success')
        return redirect(url_for('posts.all_posts'))
    return render_template('create_post.html', form=form, legend='Создайте свой пост')


@posts.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post, post_id=post_id)


@posts.route('/post/<int:post_id>/update/', methods=['GET', 'POST'])
@login_required
def update(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = CreatePost()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.text.data
        db.session.commit()
        flash('Ваш пост обновлен!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.text.data = post.content
    return render_template('create_post.html', title='Обновление поста',
                           form=form, legend='Обновление поста')



@posts.route('/post/<int:post_id>/delete/', methods=['POST'])
@login_required
def delete(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Пост был полностью удален', 'success')
    return redirect(url_for('posts.all_posts'))
