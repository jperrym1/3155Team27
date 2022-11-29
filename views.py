from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import Length, Regexp, DataRequired, EqualTo, Email
from wtforms import ValidationError
from data_models import User
from database import db

class LoginView(FlaskForm):
    class Meta:
        csrf = False
    email = StringField('Email: ', [
        Email(message='Please enter a valid email address.'),
        DataRequired(message='This is a required field.')])

    password = PasswordField('Password: ', [
        DataRequired(message="Please enter a password.")])

    submit = SubmitField('Submit')

    def validate_email(self, field):
        if db.session.query(User).filter_by(email=field.data).count() == 0:
            raise ValidationError('Incorrect username or password.')

class RegisterView(FlaskForm):
    class Meta:
        csrf = False
    firstname = StringField('First Name: ', validators=[Length(1, 100)])
    lastname = StringField('Last Name: ', validators=[Length(1, 100)])
    email = StringField('Email: ', [
        Email(message='Please enter a valid email address.'),
        DataRequired(message='This is a required field.')])
    password = PasswordField('Password: ', [
        DataRequired(message="Please enter a password."),
        EqualTo('confirmPassword', message='Passwords must match')
    ])
    confirmPassword = PasswordField('Confirm Password', validators=[
        Length(min=6, max=30)
    ])
    submit = SubmitField('Submit')
    def validate_email(self, field):
        if db.session.query(User).filter_by(email=field.data).count() != 0:
            raise ValidationError('Email already has account associated with it.')

class CreateProjectView(FlaskForm):
    class Meta:
        csrf = False
    project_name = StringField('Project Name: ', validators=[Length(min=1)])

    description = TextAreaField('Description: ', validators=[Length(min=1)])

    members = TextAreaField('Members (enter with commas separating names): ', validators=[Length(min=1)])

    tasks = TextAreaField('Tasks: ', validators=[Length(min=1)])

    submit = SubmitField('Submit')

class CommentOnProject(FlaskForm):
    class Meta:
        csrf = False
    comment = TextAreaField('Comment', validators=[Length(min=1)])
    submit = SubmitField('Add Comment')