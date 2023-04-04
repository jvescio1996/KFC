from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect, request, session
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm, ReservationForm
import pymysql
import hashlib
from passlib.hash import sha256_crypt


salt = "3b0"

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
    if form.validate_on_submit():


        flash(f'Reservation created for {form.username.data}!', 'success')
        #flash(f'Reservation created for KFCGroup!', 'success')
        return redirect(url_for('home'))
    return render_template('reservation.html', title='Reservation', form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    cnxn = pymysql.connect(user="dpaAdmin", password="XN@mV9ztP4fe", host="dynamicparking.mysql.database.azure.com", port=3306, database="dynamicparking", ssl_ca="DigiCertGlobalRootCA.crt.pem", ssl_disabled=True)
    cursor = cnxn.cursor()
    
    #def user_register(username, password, email):
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
            db_password2 = sha256_crypt.encrypt(password)

            print(db_password)
            print(db_password2)
            print(sha256_crypt.verify("P@ssw0rd", db_password))

            #hpass =hashlib.md5(user_password.encode())
            #print(hpass.hexdigest())

            cursor.execute('INSERT INTO users(username, user_password, user_email) VALUES (%s, %s, %s)', (username, password, email,))
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
    print(username)
    print(password)
    
    if form.validate_on_submit():
        """
        db_password = sha256_crypt.encrypt(password)
        db_password2 = sha256_crypt.encrypt(password)

        print(db_password)
        print(db_password2)
        print(sha256_crypt.verify("P@ssw0rd", db_password))
        """

        cursor.execute('SELECT * FROM users WHERE username = %s AND user_password =  %s', (username, password,))
        account = cursor.fetchone()
        print(account)
        
        """
        myresult = cursor.fetchall()
        for x in myresult:
        	print(x)
        """
        
        # If account exists in form table in our database
        if account:
            print("Credentials Match!")
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            #session['id'] = account['id']
            #session['username'] = account['username']
            
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
    # Redirect to login page
    flash(f'Logged out Successfully!', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)