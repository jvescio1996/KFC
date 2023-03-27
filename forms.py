from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField, DateField, TimeField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField('Email', email_validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Login')


class ReservationForm(FlaskForm):
	username = StringField('KFCGroup')
	license_plate = StringField('License Plate', validators=[DataRequired(), Length(min=1, max=8)])
	reservation_date = DateField('Reservation Date: ',format='%Y-%m-%d')
	reservation_start_time  = TimeField('Reservation Start Time',format='%H:%M')
	reservation_end_time  = TimeField('Reservation End Time',format='%H:%M')
	handicap_parking = RadioField('Is Handicap Parking Required?', choices =[('value', 'Yes'),('value_two', 'No')], default='value_two')
	submit = SubmitField('Reserve')


