'''create users with limitation'''
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User


class RegistrationForm(FlaskForm):
    # no empty, 2<=len<=20
    username = StringField('Username',
                           validators=[DataRequired(),
                                       Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired()])  #can add Length too
    confirm_password = PasswordField(
        'Confirm Password', validators=[DataRequired(),
                                        EqualTo('password')])
    submit = SubmitField('Sign Up')

    # custom validation
    def validate_username(self, username):
        # username.data is coming from the form by user
        dup_username = User.query.filter_by(username=username.data).first()
        if dup_username:
            raise ValidationError(
                'That username is taken. Please choose a different one.')

    def validate_email(self, email):
        dup_email = User.query.filter_by(email=email.data).first()
        if dup_email:
            raise ValidationError(
                'That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    # no empty, 2<=len<=20
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired()])  #can add Length too
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
