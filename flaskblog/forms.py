'''create users with limitation'''
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
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


class UpdateAccountForm(FlaskForm):
    # no empty, 2<=len<=20
    username = StringField('Username',
                           validators=[DataRequired(),
                                       Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField(
        'Update Profile Picture',
        # fileallowed should include a list
        validators=[FileAllowed(['jpeg', 'jpg', 'png'])])
    submit = SubmitField('Update')

    # custom validation
    def validate_username(self, username):
        # we want to validate if username != current username
        if username.data != current_user.username:
            dup_username = User.query.filter_by(username=username.data).first()
            if dup_username:
                raise ValidationError(
                    'That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            dup_email = User.query.filter_by(email=email.data).first()
            if dup_email:
                raise ValidationError(
                    'That email is taken. Please choose a different one.')


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        dup_email = User.query.filter_by(email=email.data).first()
        if dup_email is None:
            raise ValidationError(
                'There is no account with that email. You must register first.'
            )


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField(
        'Confirm Password', validators=[DataRequired(),
                                        EqualTo('password')])

    submit = SubmitField('Reset Password')
