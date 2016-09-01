from flask import render_template, redirect, request, url_for, flash
from flask_login import login_required, login_user, logout_user, current_user
from app import db
from app.auth import auth
from app.auth.forms import LoginForm, RegistrationForm, ChangePasswordForm, PasswordResetRequestForm, PasswordResetForm
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


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, '确认您的账号', 'auth/mail/confirm', user=user, token=token)
        flash('一封确认邮件已发送到您的邮箱，请注意查收！')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    elif current_user.confirm(token):
        flash('您已经成功确认了您的账号,现在可以正常使用了')
    else:
        flash('该确认链接已失效，请重新获取！')
    return redirect(url_for('main.index'))


@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if (not current_user.confirmed) and request.endpoint[:5] != 'auth.' and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')



@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, '再次确认您的账号', 'auth/mail/confirm', user=current_user, token=token)
    flash('一封新的确认邮件已发送到您的邮箱，请注意查收！')
    return redirect(url_for('main.index'))


@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data) :
            current_user.password = form.new_password.data
            logout_user()
            flash('您现在可以用新密码登陆了！')
            return redirect(url_for('auth.login'))
        else:
            flash('原密码错误，可再次尝试！')
            return redirect(url_for('auth.change_password'))
    return render_template('auth/change_password.html', form=form)


@auth.route('/reset-password-request', methods=['GET', 'POST'])
def reset_password_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first() or User.query.filter_by(username=form.email.data).first()
        if user:
            token = user.generate_reset_password_token()
            send_email(user.email, '密码重置', 'auth/mail/reset_password', user=user, token=token)
            flash('重置密码的邮件已发送到您的邮箱，请注意查收！')
            return redirect(url_for('main.index'))
        else:
            flash('您输入的账户不存在，可以重试')
            return redirect(url_for('auth.reset_password_request'))
    return render_template('auth/reset_password_request.html', form=form)


@auth.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first() or User.query.filter_by(username=form.email.data).first()
        if user and user.reset_password(token):
            user.password = form.new_password.data
            user.password = form.new_password.data
            flash('您现在可以用新密码登陆了！')
            return redirect(url_for('auth.login'))
        else:
            flash('非法的密码重置，请重新操作！')
        return redirect(url_for('auth.reset_password_request'))
    return render_template('auth/reset_password.html', form=form)

