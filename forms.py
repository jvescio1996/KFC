from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField, DateField, TimeField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo
import pymysql

class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=2, max=30)])
	email = StringField('Email', validators=[DataRequired(), Email(), Length(min=2, max=50)])
	password = PasswordField('Password', validators=[DataRequired(), Length(min=2, max=30)])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Login')

class ReservationForm(FlaskForm):
	#total_spots = StringField('Total Spots ', )
	#available spots = StringField('Available Spots')
	license_plate = StringField('License Plate ', validators=[DataRequired(), Length(min=1, max=8)])
	reservation_date = DateField('Reservation Date ',format='%Y-%m-%d')
	reservation_block  = SelectField(u'Reservation Time (2 hour time periods)', choices =[('0','Select a Time Slot'), ('1','6:00AM'),
	('2','8:00AM'), ('3','10:00AM'), ('4','12:00PM'), ('5','2:00PM'), ('6','4:00PM'), ('7','6:00PM'), ('8','8:00PM'), ('9','10:00PM')])
	handicap_parking = RadioField('Is Handicap Parking Required?', choices =[(1, 'Yes'),(0, 'No')], default = 0)
	submit = SubmitField('Reserve')


