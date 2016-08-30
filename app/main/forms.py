from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class NameForm(Form):
    name = StringField('你的名字？', validators=[DataRequired()])
    submit = SubmitField('提交')
