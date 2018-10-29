import os
from flask import Flask, request, session, url_for, redirect, render_template, abort, g, flash
from werkzeug import check_password_hash, generate_password_hash

app = Flask(__name__)

from model import db, UserType, User, Scanner, Class, Item, Pattern, Alert, Messages


SECRET_KEY = 'development key'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(app.root_path, 'model.db')

app.config.from_object(__name__)

db.init_app(app)

scheduleTime = ["07:00"]
schedulePresent = ["true"]

defaultPatternTime = ['06:00']
defaultPatternPresent = ['true']


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
            db.session.add(
                User(username=request.form['username'], password=generate_password_hash(request.form['password']),
                     firstName=request.form['fName'], lastName=request.form['lName'], userType='s'))
            db.session.commit()
            flash('You were successfully registered and can login now')
            return redirect(url_for('login'))
    return render_template('register.html', error=error)


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
            items = Item.query.filter_by(userID=session['user_id'], name=request.form['name'], tagID=request.form['rfidNum']).first()

            db.session.add(
                Pattern(userID=session['user_id'], itemID=items.id, dayOfWeek='Monday',
                        startTime=','.join(defaultPatternTime), presentItems=','.join(defaultPatternPresent))
            )
            db.session.add(
                Pattern(userID=session['user_id'], itemID=items.id, dayOfWeek='Tuesday',
                        startTime=','.join(defaultPatternTime), presentItems=','.join(defaultPatternPresent))
            )
            db.session.add(
                Pattern(userID=session['user_id'], itemID=items.id, dayOfWeek='Wednesday',
                        startTime=','.join(defaultPatternTime), presentItems=','.join(defaultPatternPresent))
            )
            db.session.add(
                Pattern(userID=session['user_id'], itemID=items.id, dayOfWeek='Thursday',
                        startTime=','.join(defaultPatternTime), presentItems=','.join(defaultPatternPresent))
            )
            db.session.add(
                Pattern(userID=session['user_id'], itemID=items.id, dayOfWeek='Friday',
                        startTime=','.join(defaultPatternTime), presentItems=','.join(defaultPatternPresent))
            )

            db.session.commit()
            items2 = Pattern.query.filter_by(userID=session['user_id'], itemID=items.id).all()

            for item in items2:
                print(item.startTime)

            flash('You were successfully added an item')
    items = Item.query.filter_by(userID=session['user_id']).all()
    return render_template("items.html", user=g.user, error=error, items=items)


@app.route('/status')
def status():
    return render_template("status.html", user=g.user)


@app.route('/schedule')
def schedule():
    return render_template("schedule.html", user=g.user)


@app.route('/notifications')
def notifications():
    return render_template("notifications.html", user=g.user)


@app.route('/register_class')
def register_class():
    return render_template("register_class.html", user=g.user)


@app.route('/logout')
def logout():
    flash('You were logged out')
    session.pop('user_id', None)
    return redirect(url_for('home'))


@app.route('/updateSchedule', methods=["GET", "POST"])
def update_schedule():
    error = None
    items = Item.query.filter_by(userID=session['user_id']).all()

    if request.method == "POST":
        time = request.form["startHours"] + ":" + request.form["startMinutes"]

        found = binarySearch(scheduleTime, 0, len(scheduleTime) - 1, time)

        if found >= 0:
            schedulePresent[found] = request.form["found"]
        else:
            tempTime, tempPresent = updatePattern(scheduleTime, schedulePresent, request.form["found"], time)

            start = 0

            while start < len(tempTime):
                scheduleTime[start] = tempTime[start]
                schedulePresent[start] = tempPresent[start]
                start = start + 1

            print(scheduleTime)
            print(schedulePresent)

    return render_template("updateSchedule.html", error=error, items=items)


@app.route('/checkStatus', methods=["GET", "POST"])
def check_time_status():
    error = None
    items = Item.query.filter_by(userID=session['user_id']).all()

    if request.method == "POST":
        time = request.form["Hours"] + ":" + request.form["Minutes"]

        found = binarySearch(scheduleTime, 0, len(scheduleTime) - 1, time)
        item = Item.query.filter_by(userID=session['user_id'], id=request.form['item']).all()
        data = request.form["found"]

        if found >= 0:
            if data == schedulePresent[found]:
                print("No Problem!")
            else:
                str = "Item " + item.name + " had a problem."
                db.session.add(
                    Alert(userID=session['user_id'], itemID=request.form['item'], message=str, dayOfWeek="Monday",
                          time=time, status=1)
                )
                db.session.commit()
                print("The was a problem!")
        else:
            res = findSpot(scheduleTime, time)
            print(res)
            if data == schedulePresent[res]:
                print("No Problem!")
            else:
                str = "Item " + request.form['item'] + " had a problem."
                db.session.add(
                    Alert(userID=session['user_id'], itemID=request.form['item'], message=str, dayOfWeek="Monday",
                          time=time, status=1)
                )
                db.session.commit()
                print("The was a problem!")

    return render_template("check.html", error=error, items=items)


@app.route("/alerts", methods=["GET", "POST"])
def alerts():
    error = None
    allAlerts = Alert.query.filter_by(userID=session['user_id']).all()
    alertNotHandled = Alert.query.filter_by(userID=session['user_id'], status=1).all()
    alertUserApproved = Alert.query.filter_by(userID=session['user_id'], status=2).all()
    alertForConcern = Alert.query.filter_by(userID=session['user_id'], status=3).all()

    if request.method == "POST":
        alert = request.form['item']
        status = request.form['found']

        print(alert)
        print(status)

        alertUpdate = Alert.query.filter_by(id=alert).first()
        alertUpdate.status = int(status)
        db.session.commit()

        allAlerts = Alert.query.filter_by(userID=session['user_id']).all()
        alertNotHandled = Alert.query.filter_by(userID=session['user_id'], status=1).all()
        alertUserApproved = Alert.query.filter_by(userID=session['user_id'], status=2).all()
        alertForConcern = Alert.query.filter_by(userID=session['user_id'], status=3).all()

    return render_template("alerts.html", error=error, allAlerts=allAlerts, alertNotHandled=alertNotHandled,
                           alertUserApproved=alertUserApproved, alertForConcern=alertForConcern)


def updatePattern(times, presentStatus, found, time):
    i = 0
    while i < len(times):
        if i < len(times) - 2:
            if times[i] <= time & times[i+1] >= time:
                times.insert(i+1, time)
                presentStatus.insert(i+1, found)
        else:
            if time[i] <= time:
                times.insert(i + 1, time)
                presentStatus.insert(i + 1, found)

        i += 1

        return times, presentStatus


def binarySearch(arr, l, r, x):
    while l <= r:
        mid = l + (r - l) // 2

        if l == 0 & r == 0:
            if arr[l] == x:
                return l;
            else:
                return -1;

        # Check if x is present at mid
        if arr[mid] == x:
            return mid
        # If x is greater, ignore left half
        elif arr[mid] < x:
            l = mid + 1
        # If x is smaller, ignore right half
        else:
            r = mid - 1

    # If we reach here, then the element
    # was not present
    return -1


def findSpot (inputArr, key):
    start = 0

    print(len(inputArr))
    while start < len(inputArr):
        if inputArr[start] < key:
            if (start + 1) == len(inputArr):
                return start
            if inputArr[start + 1] > key:
                return start
        start = start + 1

    return -1


if __name__ == '__main__':
    app.run(debug=True)
