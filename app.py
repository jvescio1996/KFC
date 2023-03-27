from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm, ReservationForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

posts = [
    {
        'author': 'Keanu Reeves Fan Club',
        'title': 'Dynamic Parking App',
        'content': 'Hello and Welcome to the Dynamic Parking App (DPA) Homepage! ',
        'date_posted': 'September 2, 1964'
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
        #flash(f'Reservation created for {form.username.data}!', 'success')
        flash(f'Reservation created for KFCGroup!', 'success')
        return redirect(url_for('home'))
    return render_template('reservation.html', title='Reservation', form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        #if form.email.data == 'admin@dpa.com' and form.password.data == 'p@ssw0rd':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        #else:
            #flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
    app.run(debug=True)
