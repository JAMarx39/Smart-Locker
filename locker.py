import os
from flask import Flask, request, session, url_for, redirect, render_template, abort, g, flash
from werkzeug import check_password_hash, generate_password_hash
from datetime import datetime

app = Flask(__name__)

from model import db, UserType, User, Scanner, Class, Item, Pattern, Alert, Messages


SECRET_KEY = 'development key'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(app.root_path, 'model.db')

app.config.from_object(__name__)

db.init_app(app)


@app.cli.command('initdb')
def initdb_command():
    """Creates the database tables."""
    db.create_all()
    db.session.add(
        User(username='ADMIN', password=generate_password_hash('ADMIN'),
             firstName='ADMIN', lastName='ADMIN', userType='a'))
    db.session.commit()
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
    error = None

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

    return render_template("login.html", error=error)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Registers the user."""
    error = None
    if request.method == 'POST':
        rv = User.query.filter_by(username=request.form['username']).first()
        error = None
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
            if g.user:
                db.session.add(
                    User(username=request.form['username'], password=generate_password_hash(request.form['password']),
                         firstName=request.form['fName'], lastName=request.form['lName'], userType='t'))
                db.session.commit()
                flash('You successfully created a teacher account')
            else:
                db.session.add(
                    User(username=request.form['username'], password=generate_password_hash(request.form['password']),
                         firstName=request.form['fName'], lastName=request.form['lName'], userType='s'))
                db.session.commit()
                flash('You were successfully registered and can login now')
            return redirect(url_for('login'))
    return render_template('register.html', user=g.user, error=error)


@app.route('/items', methods=["GET", "POST"])
def items():
    error = None
    if request.method == 'POST':
        error = None
        if not request.form['name']:
            error = 'You have to enter a item name'
        elif not request.form['rfidNum']:
            error = 'You have to enter the RFID number'
        else:
            db.session.add(
                Item(name=request.form['name'], tagID=request.form['rfidNum'], userID=session['user_id']))
            db.session.commit()
            flash('You were successfully added an item')
    items = Item.query.filter_by(userID=session['user_id']).all()
    return render_template("items.html", user=g.user, error=error, items=items)


@app.route('/status', methods=["GET", "POST"])
def status():
    return render_template("status.html", user=g.user)


@app.route('/schedule', methods=["GET", "POST"])
def schedule():
    error = None
    if request.method == 'POST':
        error = None
        if not request.form['code']:
            error = 'You have to enter a course code'
        else:
            student = User.query.filter_by(id=session['user_id']).first()
            course = Class.query.filter_by(code=request.form['code']).first()
            if course is not None:
                course.students.append(student)
                student.classes.append(course)
                db.session.commit()

                flash('You successfully added a course')
            else:
                error = 'Not a valid course code'

    student = User.query.filter_by(id=session['user_id']).first()
    return render_template("schedule.html", user=g.user, error=error, classes=student.classes)


@app.route('/notifications')
def notifications():
    student = User.query.filter_by(id=session['user_id']).first()
    courses = student.classes
    messages = []
    for course in courses:
        messages.append((course.messages, course.name))
    return render_template("notifications.html", user=g.user, notifications=messages)


@app.route('/classes', methods=["GET", "POST"])
def classes():
    error = None
    if request.method == 'POST':
        error = None
        if not request.form['code']:
            error = 'You have to enter a course code'
        elif not request.form['message']:
            error = 'You did not enter an alert'
        else:
            teacher = User.query.filter_by(id=session['user_id']).first()
            course = Class.query.filter_by(code=request.form['code']).first()
            if course.teacherID == teacher.id:
                message = Messages(message=request.form['message'], course=course.id)
                db.session.add(message)
                course.messages.append(message)
                db.session.commit()
                flash('You successfully sent an alert')
            else:
                error = 'Not a valid course code'
    classlist = Class.query.filter_by(teacherID=session['user_id']).all()
    return render_template("classes.html", user=g.user, error=error, classes=classlist)


@app.route('/register_class', methods=["GET", "POST"])
def register_class():
    error = None
    if request.method == 'POST':
        error = None
        if not request.form['className']:
            error = 'You have to enter a class name'
        elif not request.form['code']:
            error = 'You have to enter a course code'
        elif not request.form['teacherName']:
            error = 'You have to enter a teacher\'s name'
        elif not request.form['startHours'] or not request.form['startHours']:
            error = 'You have to enter the start time'
        elif not request.form['endHours'] or not request.form['endHours']:
            error = 'You have to enter the end time'
        else:
            teacher = User.query.filter_by(username=request.form['teacherName']).first()
            if teacher and teacher.userType == "t":
                timeStart = request.form['startHours'] + request.form['startHours']
                timeEnd = request.form['endHours'] + request.form['endHours']
                if timeStart < timeEnd:
                    db.session.add(
                        Class(name=request.form['className'], code=request.form['code'], teacherID=teacher.id,
                              startTime=timeStart, endTime=timeEnd))
                    db.session.commit()
                    flash('You were successfully added a class')
                else:
                    error="The end time must be later than the start time"
            else:
                error="That teacher username does not exist"
    return render_template("register_class.html", user=g.user, error=error)


@app.route('/logout')
def logout():
    flash('You were logged out')
    session.pop('user_id', None)
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
