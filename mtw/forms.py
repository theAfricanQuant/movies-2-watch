from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from mtw.models import User


class RegistrationForm(FlaskForm):
    ''' User registration form '''
    username = StringField('Username', validators=[DataRequired(), Length(min=5, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is already taken')


    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('That email is already in use')


class LoginForm(FlaskForm):
    ''' Login form '''
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')              
    submit = SubmitField('Log In')


class AddMovie(FlaskForm):
    ''' Add a movie manually to the users list '''
    title = StringField('Title', validators=[DataRequired()])
    year_released = IntegerField('Year Released')
    submit = SubmitField('Add Movie')


class RequestResetForm(FlaskForm):
    ''' Request a password reset form '''
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')


    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('That email does not exist. Please register first.')


class ResetPasswordForm(FlaskForm):
    ''' Change password form '''
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')


class SearchForMovie(FlaskForm):
    ''' Search for a movie to add to list '''
    search = StringField('Search Movies', validators=[DataRequired()])
    submit = SubmitField('Search')


class AddMovieFromSearch(FlaskForm):
    ''' Add a movie to the list from search results '''
    title = HiddenField('Title', validators=[DataRequired()])
    year_released = HiddenField('Year Released')
    submit = SubmitField('Add Movie')