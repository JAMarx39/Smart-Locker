import os
from flask import Flask, request, session, url_for, redirect, render_template, abort, g, flash
from werkzeug import check_password_hash, generate_password_hash

app = Flask(__name__)

#from model import db, UserType, User, Scanner, Class, Item, Pattern, Alert, Messages
from model import db, User


SECRET_KEY = 'development key'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(app.root_path, 'model.db')

app.config.from_object(__name__)

db.init_app(app)


@app.cli.command('initdb')
def initdb_command():
    """Creates the database tables."""
    db.create_all()
    user = User.query.filter_by(username="owner").first()
    if user is None:
        db.session.add(
            User(username='owner', password=generate_password_hash("pass"), firstName="Bob", lastName="Smith"))
        db.session.commit()
        user = None
    print('Initialized the database.')


@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        g.user = User.query.filter_by(id=session['user_id']).first()


@app.route('/')
def home():
    return render_template("home.html", user=g.user)


@app.route('/login/', methods=["GET", "POST"])
def login():
    if g.user:
        return redirect(url_for('home'))

    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user is None:
            error = 'Invalid username'
        elif not check_password_hash(user.password, request.form['password']):
            error = 'Invalid password'
        else:
            flash('You were logged in')
            session['user_id'] = user.id
            return redirect(url_for('home'))

    return render_template("login.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Registers the user."""
    error = None
    if request.method == 'POST':
        rv = User.query.filter_by(username=request.form['username']).first()
        if not request.form['username']:
            error = 'You have to enter a username'
        elif not request.form['fName']:
            error = 'You have to enter your first name'
        elif not request.form['lName']:
            error = 'You have to enter your last name'
        elif not request.form['password']:
            error = 'You have to enter a password'
        elif request.form['password'] != request.form['password2']:
            error = 'The two passwords do not match'
        elif rv is not None:
            error = 'The username is already taken'
        else:
            db.session.add(
                User(username=request.form['username'], password=generate_password_hash(request.form['password']),
                     firstName=request.form['fName'], lastName=request.form['lName']))
            db.session.commit()
            flash('You were successfully registered and can login now')
            return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/items')
def items():
    return render_template("items.html", user=g.user)


@app.route('/status')
def status():
    return render_template("status.html", user=g.user)


@app.route('/schedule')
def schedule():
    return render_template("schedule.html", user=g.user)


@app.route('/notifications')
def notifications():
    return render_template("notifications.html", user=g.user)


if __name__ == '__main__':
    app.run(debug=True)
