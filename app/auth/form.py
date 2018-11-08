from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, ValidationError, SubmitField, BooleanField

from wtforms.validators import Required, DataRequired, Length, Regexp, EqualTo, Email

from app.models import User


class UserForm(FlaskForm):
    email = StringField('邮箱',validators=[DataRequired(), Length(1,64),Email()],render_kw={"placeholder":"请输入用户名"})
    password = PasswordField('密码', validators=[DataRequired()])
    remenber_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Length(1, 64), Email()], render_kw={"placeholder": "请输入用户名"})
    username = StringField('Username', validators=[DataRequired(), Length(1, 64),
                                                   Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                  'Usernames must have only letters, '
                                                  'numbers, dots or underscores')])
    password = PasswordField('密码', validators=[DataRequired(),EqualTo('password2', message='两次密码必须一致')],render_kw={"placeholder":"两次密码必须一致"})
    password2 = PasswordField('确认密码',validators=[DataRequired()],render_kw={"placeholder":"两次密码必须一致"})
    submit = SubmitField('注册')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱已被注册')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已存在')
