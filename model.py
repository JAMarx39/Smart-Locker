from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

enrolled = db.Table('enrolled',
    db.Column('student_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('class_id', db.Integer, db.ForeignKey('class.id'))
)


class UserType(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    userType = db.Column(db.String(24), nullable=False)

    def __init__(self):
        self.userType = ""


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(24), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    firstName = db.Column(db.String(24), nullable=False)
    lastName = db.Column(db.String(24), nullable=False)
    userType = db.Column(db.CHAR, nullable=False)

    classes = db.relationship('Class', backref='student')

    def __init__(self, username, password, firstName, lastName, userType):
        self.username = username
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
    code = db.Column(db.String(24), nullable=False)
    location = db.Column(db.String(24), nullable=True)
    teacherID = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    startTime = db.Column(db.String(24), nullable=False)
    endTime = db.Column(db.String(24), nullable=False)

    students = db.relationship('User', secondary=enrolled, backref=db.backref('enrolled_in', lazy='dynamic'),
                               lazy='dynamic')

    def __init__(self, name, code, teacherID, startTime, endTime):
        self.name = name
        self.code = code
        self.teacherID = teacherID
        self.startTime = startTime
        self.endTime = endTime


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

    def __init__(self):
        self.userID = 0
        self.itemID = 0
        self.dayOfWeek = ""


class Alert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    itemID = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    message = db.Column(db.String(128), nullable=False)
    time = db.Column(db.DateTime, nullable=False)

    def __init__(self):
        self.userID = 0
        self.itemID = 0
        self.message = ""
        self.time = '1000-01-01 00:00:00.000000'


class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    message = db.Column(db.String(128), nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    itemID = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)

    def __init__(self):
        self.userID = 0
        self.message = ""
        self.time = '1000-01-01 00:00:00.000000'
        self.timeID = 0