from flask import render_template, session, redirect, url_for, current_app,abort, flash
from flask_login import login_required, current_user
from .. import db
from . import main
from ..models import User, Permission, Role, Post
from ..email import send_email
from .forms import NameForm, EditProfileForm, EditProfileAdminForm, PostForm
from datetime import datetime
from app.decorators import admin_required, permission_required


@main.route('/', methods=['GET', 'POST'])
def index():
    form = PostForm()
    if current_user.can(Permission.WRITE_ARTICLES) and form.validate_on_submit():
        post = Post(body=form.body.data, author=current_user._get_current_object())
        db.session.add(post)
        return redirect(url_for('.index'))
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('index.html', form=form, posts=posts)
    # form = NameForm()
    # if form.validate_on_submit():
    #     user = User.query.filter_by(username=form.name.data).first()
    #     if user is None:
    #         user = User(username=form.name.data)
    #         db.session.add(user)
    #         session['known'] = False
    #         if current_app.config['FLASKY_ADMIN']:
    #             send_email(current_app.config['FLASKY_ADMIN'], '新用户',
    #                        'mail/new_user', user=user)
    #     else:
    #         session['known'] = True
    #     session['name'] = form.name.data
    #     form.name.data = ''
    #     return redirect(url_for('.index'))
    # return render_template('index.html',
    #                        form=form, name=session.get('name'),
    #                        known = session.get('known', False),
    #                        current_time=datetime.utcnow())


# 为了测试权限函数
@main.route('/admin')
@login_required
@admin_required
def for_admins_only():
    return "为了部落！"


@main.route('/moderator')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def for_moderators_only():
    return '为了联盟！'


# 用户资料页
@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    posts = user.posts.order_by(Post.timestamp.desc()).all()
    return render_template('user.html', user=user, posts=posts)


# 用户编辑个人资料
@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash('您的个人资料已经更新')
        return redirect(url_for('main.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)


# 管理员编辑个人资料
@main.route('/edit-profile-admin/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):

    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        if form.password.data:
            user.password = form.password.data
        user.confirmed = form.comfirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        flash('该用户个人资料已经更新')
        return redirect(url_for('main.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.comfirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_admin_profile.html', form=form, user=user)


# @main.route('/', methods=['GET', 'POST'])
# def index()
