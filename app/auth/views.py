from flask import render_template, redirect, request, url_for, flash
from flask_login import login_required, login_user, logout_user

from app import db
from app.auth import auth
from app.auth.forms import LoginForm, RegistrationForm
from app.models import User


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(password=form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('非法的用户名或密码！')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已经退出登录了！')
    return redirect(url_for('main.index'))


@auth.route('/register',methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        flash('你现在可以登录了！')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)