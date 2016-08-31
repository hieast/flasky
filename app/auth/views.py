from flask import render_template, redirect, request, url_for, flash
from flask_login import login_required, login_user, logout_user, current_user
from app import db
from app.auth import auth
from app.auth.forms import LoginForm, RegistrationForm
from app.email import send_email
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
        db.session.commit()
        token = user.generate_confirm_token()
        send_email(user.email, '确认您的账号', 'auth/mail/confirm', user=user, token=token)
        flash('一封确认邮件已发送到您的邮箱，请注意查收！')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)


@auth.route('confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    elif current_user.confirm(token):
        flash('您已经成功确认了您的账号,现在可以正常使用了')
    else:
        flash('该确认链接已失效，请重新获取！')
    return redirect(url_for('main.index'))