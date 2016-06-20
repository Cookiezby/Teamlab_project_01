from flask.ext.wtf import Form
from wtforms import StringField,PasswordField,TextAreaField,IntegerField



class LoginForm(Form):
    name = StringField('name')
    password = PasswordField('password')


class RegisterForm(Form):
    name = StringField('name')
    password = PasswordField('password')
    pwd_confirm = PasswordField('pwd_confirm')


class PostForm(Form):
    body = TextAreaField('body')


class ProfileForm(Form):
    user_info = TextAreaField('user_info')


