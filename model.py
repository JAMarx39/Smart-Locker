from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

enrolled_in = db.Table('enrolled_in',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('class_id', db.Integer, db.ForeignKey('class.id'))
)

sent_to = db.Table('sent_to',
    db.Column('messages_id', db.Integer, db.ForeignKey('messages.id')),
    db.Column('class_id', db.Integer, db.ForeignKey('class.id'))
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(24), nullable=False)
    email = db.Column(db.String(24), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    firstName = db.Column(db.String(24), nullable=False)
    lastName = db.Column(db.String(24), nullable=False)
    userType = db.Column(db.CHAR, nullable=False)

    classes = db.relationship('Class', backref='student')

    def __init__(self, username, email, password, firstName, lastName, userType):
        self.username = username
        self.email = email
        self.password = password
        self.firstName = firstName
        self.lastName = lastName
        self.userType = userType


class Scanner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    scannerName = db.Column(db.String(64), nullable=False)

    def __init__(self):
        self.userID = 0
        self.scannerName = ""


class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(24), nullable=False)
    location = db.Column(db.String(24), nullable=True)
    code = db.Column(db.String(24), nullable=True)
    teacherID = db.Column(db.Integer, nullable=False)
    startTime = db.Column(db.String(24), nullable=False)
    endTime = db.Column(db.String(24), nullable=False)
    studentID = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    students = db.relationship('User', secondary='enrolled_in', backref=db.backref('student_in', lazy='dynamic'), lazy='dynamic')

    messages = db.relationship('Messages', secondary='sent_to', backref=db.backref('sent_from', lazy='dynamic'), lazy='dynamic')

    def __init__(self, name, code, teacherID, startTime, endTime, studentID=0):
        self.name = name
        self.code = code
        self.teacherID = teacherID
        self.startTime = startTime
        self.endTime = endTime
        self.studentID = studentID


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tagID = db.Column(db.String(64), nullable=False)
    name = db.Column(db.String(24), nullable=False)
    classID = db.Column(db.Integer, db.ForeignKey("class.id"), nullable=True)
    userID = db.Column(db.Integer, nullable=False)

    def __init__(self, name, tagID, userID):
        self.name = name
        self.tagID = tagID
        self.classID = ""
        self.userID = userID


class Pattern(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    itemID = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    dayOfWeek = db.Column(db.String(9), nullable=False)
    startTime = db.Column(db.String(130), nullable=False)
    presentItem = db.Column(db.String(52), nullable=False)

    def __init__(self, userID, itemID, dayOfWeek, startTime, presentItems):
        self.userID = userID
        self.itemID = itemID
        self.dayOfWeek = dayOfWeek
        self.startTime = startTime
        self.presentItem = presentItems


class Alert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    itemID = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    message = db.Column(db.String(128), nullable=False)
    dayOfWeek = db.Column(db.String(9), nullable=False)
    time = db.Column(db.String(5), nullable=False)
    status = db.Column(db.Integer, nullable=False)

    def __init__(self, userID, itemID, message, dayOfWeek, time, status):
        self.userID = userID
        self.itemID = itemID
        self.message = message
        self.dayOfWeek = dayOfWeek
        self.time = time
        self.status = status


class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(128), nullable=False)
    code = db.Column(db.String(32), nullable=False)
    time = db.Column(db.DateTime, nullable=True)

    def __init__(self, message, code):
        self.message = message
        self.code = code