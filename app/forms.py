from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User

class LoginForm(FlaskForm):
    company_name = StringField('Company Name', validators=[DataRequired()],render_kw={"placeholder": "Company's Name"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Password"})
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')




class RegistrationForm(FlaskForm):
    company_name = StringField('Company Name', validators=[DataRequired()],render_kw={"placeholder": "Company's Name"})
    email = StringField('Email', validators=[DataRequired(), Email()],render_kw={"placeholder": "Enter Email"})
    address = StringField('Address', validators=[DataRequired()],render_kw={"placeholder": "Enter Address"})
    contact = IntegerField('Contact', validators=[DataRequired()],render_kw={"placeholder": "Enter Contact Number"})
    password = PasswordField('Password', validators=[DataRequired()],render_kw={"placeholder": "Password"})
    # password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')],render_kw={"placeholder": "Confirm Password"})
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')