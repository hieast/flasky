from flask_wtf import Form
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, ValidationError
from wtforms.widgets import TextArea

from app.models import User, Role


class NameForm(Form):
    name = StringField('你的名字？', validators=[DataRequired()])
    submit = SubmitField('提交')


class EditProfileForm(Form):
    name = StringField('真实姓名', validators=[Length(0, 64)])
    location = StringField('地理位置', validators=[Length(0, 64)])
    about_me = TextAreaField('自我介绍')
    submit = SubmitField('提交')


class EditProfileAdminForm(Form):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('用户名', validators=[
        DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_]*$', 0,
                                              '用户名必须以字母开头，并且只包含字母、数字和下划线')])
    password = PasswordField('密码', validators=[Length(0, 64),
        EqualTo('password2', message="密码不一致")])
    password2 = PasswordField('确认密码', validators=[])
    comfirmed = BooleanField('是否确认')
    role = SelectField('权限级别', coerce=int)
    name = StringField('真实姓名', validators=[Length(0, 64)])
    location = StringField('地理位置', validators=[Length(0, 64)])
    about_me = TextAreaField('自我介绍', default='这个主人很忙，没时间叫累了。')
    submit = SubmitField('提交')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name) for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已注册！')

    def validate_username(self, field):
        if field.data != self.user.username and User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已注册！')


class PostForm(Form):
    body = TextAreaField('微博内容', validators=[DataRequired()])
    submit = SubmitField('提交')