from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect, request, session
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm, ReservationForm
import pymysql
import hashlib
from passlib.hash import sha256_crypt
import time
import schedule

salt = "3b0"

res_6AM = [False, False, False, False]
res_8AM = [False, False, False, False]
res_10AM = [False, False, False, False]
res_12PM = [False, False, False, False]
res_2PM = [False, False, False, False]
res_4PM = [False, False, False, False]
res_6PM = [False, False, False, False]
res_8PM = [False, False, False, False]
res_10PM = [False, False, False, False]

def wipe_res_6AM(res_6AM):
    res_6AM = [False, False, False, False]
    return res_6AM

schedule.every().day.at("00:00").do(wipe_res_6AM,res_6AM)

def checkslot (spot,reservation, res_time):
        i=0
        while i < len(spot):
            print("checkslot")
            if spot[i] == True:
                i = i + 1
                if i >= len(spot):
                    flash(f'Sorry no spaces available for {res_time}', 'error')
            elif spot[i] == False:
                spot[i] = reservation
                return

pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'


"""
# Configure database connection
cnxn = pymysql.connect(user="dpaAdmin", password="XN@mV9ztP4fe", host="dynamicparking.mysql.database.azure.com", port=3306, database="dynamicparking", ssl_ca="DigiCertGlobalRootCA.crt.pem", ssl_disabled=True)
cursor = cnxn.cursor()

print ("connected to database")
"""
posts = [
    {
        'author': 'Daniel Pay',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]


@app.route("/")
@app.route("/home")
def home():

    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/reservation", methods=['GET', 'POST'])
def reservation():
    form = ReservationForm()
    cnxn = pymysql.connect(user="dpaAdmin", password="XN@mV9ztP4fe", host="dynamicparking.mysql.database.azure.com", port=3306, database="dynamicparking", ssl_ca="DigiCertGlobalRootCA.crt.pem", ssl_disabled=True)
    cursor = cnxn.cursor()
    cursor2 = cnxn.cursor()

    last_row = cursor2.execute("SELECT * FROM camera ORDER BY camera_time DESC LIMIT 1")
    
    print(last_row)
    last_row = cursor2.fetchone()
    print(last_row)
    
    total_spaces = 4
    camera_occupied = last_row[1]
    camera_empty = last_row[2]
    percent_available = (camera_empty / total_spaces) * 100

    #print(camera_occupied)
    #print(camera_empty)
    
    license_plate  = form.license_plate.data
    res_date = form.reservation_date.data
    reservation_time = form.reservation_block.data
    handicap = form.handicap_parking.data
    
    """
    def checkSlot (spot,reservation, res_time):
        i=0
        while i < len(spot):
            print("hi")
            if spot[i] == True:
                i = i + 1
                if i >= len(spot):
                    flash(f'Sorry no spaces available for {res_time}', 'error')
            elif spot[i] == False:
                spot[i] = reservation
                return
                """

    #try:
    if form.validate_on_submit():
        print("hey")
        if 'loggedin' in session:
            print("logged in")
            #print(session['username'])
            user_id = session['id']
            user_name = session['username']
            #print(license_plate, res_date, reservation_time , handicap)
            if reservation_time == '0':
                flash(f'Please Select a Time!', 'error')
                return redirect(url_for('reservation'))
            elif reservation_time == '1':
                res_time = "6:00AM"
                print("6AM")
                checkslot( res_6AM, True, res_time)
            elif reservation_time == '2':
                res_time = "8:00AM"
                print("8AM")
                checkslot( res_8AM, True, res_time)
            elif reservation_time == '3':
                res_time = "10:00AM"
                print("10AM")
                checkslot( res_10AM, True, res_time)
            elif reservation_time == '4':
                res_time = "12:00PM"
                print("12PM")
                checkslot( res_12PM, True, res_time)
            elif reservation_time == '5':
                res_time = "2:00PM"
                print("2PM")
                checkslot( res_2PM, True, res_time)
            elif reservation_time == '6':
                res_time = "4:00PM"
                print("4PM")
                checkslot( res_4PM, True, res_time)
            elif reservation_time == '7':
                res_time = "6:00PM"
                print("6PM")
                checkslot( res_6PM, True, res_time)
            elif reservation_time == '8':
                res_time = "8:00PM"
                print("8PM")
                checkslot( res_8PM, True, res_time)
            elif reservation_time == '9':
                res_time = "10:00PM"
                print("10PM")
                checkslot( res_10PM, True, res_time)
            else:
                flash(f'Error with Time Selection')
                print("res else")
                #return redirect(url_for('reservation'))

            print(license_plate, res_date, res_time, handicap)

            cursor.execute('INSERT INTO reservations(user_id, plate, reservation_date, reservation_time, handicap) VALUES (%s, %s, %s, %s, %s)', (int(user_id), license_plate, res_date, res_time, int(handicap)))
            cnxn.commit()

            print("here")
            flash(f'Reservation Successfully Created for {user_name}!', 'success')
            #return redirect(url_for('home'))
        else:
            print(" login else")
            flash(f'Please Login before Creating a Reservation!', 'error')
            return redirect(url_for('login'))
        return redirect(url_for('home'))
    #except:
    #return redirect(url_for('home'))

    return render_template('reservation.html', title='Reservation', form=form, value = total_spaces, value2 = camera_empty, value3 = percent_available)

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    cnxn = pymysql.connect(user="dpaAdmin", password="XN@mV9ztP4fe", host="dynamicparking.mysql.database.azure.com", port=3306, database="dynamicparking", ssl_ca="DigiCertGlobalRootCA.crt.pem", ssl_disabled=True)
    cursor = cnxn.cursor()
    
    username = form.username.data
    password = form.password.data
    email = form.email.data
     
    if form.validate_on_submit():
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        account = cursor.fetchone()

        if account:
            flash(f'Account already exists!', 'error')
        else:

            #user_password = str(password)+salt
            db_password = sha256_crypt.encrypt(password)
            #db_password2 = sha256_crypt.encrypt(password)

            print(db_password)
            #print(db_password2)
            print(sha256_crypt.verify("P@ssw0rd", db_password))

            #hpass =hashlib.md5(user_password.encode())
            #print(hpass.hexdigest())

            cursor.execute('INSERT INTO users(username, user_pass, user_email) VALUES (%s, %s, %s)', (username, db_password, email,))
            cnxn.commit()

            flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    cnxn = pymysql.connect(
    	user="dpaAdmin",
        password="XN@mV9ztP4fe",
        host="dynamicparking.mysql.database.azure.com",
        port=3306,
        database="dynamicparking",
        ssl_ca="DigiCertGlobalRootCA.crt.pem",
        ssl_disabled=True)
    cursor = cnxn.cursor()
    
    #def user_login(password, email):
    username = form.username.data
    password = form.password.data

    print(type(username))
    print(type(password))
    
    if form.validate_on_submit():
        """
        db_password = sha256_crypt.encrypt(password)
        db_password2 = sha256_crypt.encrypt(password)

        print(db_password)
        print(db_password2)
        print(sha256_crypt.verify("P@ssw0rd", db_password))
        """

        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        account = cursor.fetchone()
        
        #print(sha256_crypt.verify(password, account[2]))
        
        
        
        # If account exists in form table in our database
        if account:
            print("Credentials Match!")
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account[0]
            session['username'] = account[1]
            #session.pop('notlogged_in')
            
            # Redirect to home page
            flash(f'{form.username.data} Logged in Successfully!', 'success')
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            flash(f'Account doesnt exist or username/password Incorrect!', 'error')
        
        return redirect(url_for('login'))
    return render_template('login.html', title='Login', form=form)


@app.route("/logout", methods=['GET', 'POST'])
def logout():
	# Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    session.clear()
    # Redirect to login page
    flash(f'Logged out Successfully!', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
