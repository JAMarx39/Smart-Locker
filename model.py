from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


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
    location = db.Column(db.String(24), nullable=False)
    teacherID = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    startTime = db.Column(db.DateTime, nullable=False)
    endTime = db.Column(db.DateTime, nullable=False)

    def __init__(self):
        self.name = ""
        self.location = ""
        self.teacherID = 0
        self.startTime = '1000-01-01 00:00:00.000000'
        self.endTime = '1000-01-01 00:00:00.000000'


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tagID = db.Column(db.String(64), nullable=False)
    name = db.Column(db.String(24), nullable=False)
    userID = db.Column(db.Integer, nullable=False)

    def __init__(self, name, tagID, userID):
        self.name = name
        self.tagID = tagID
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
    userID = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    message = db.Column(db.String(128), nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    itemID = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)

    def __init__(self):
        self.userID = 0
        self.message = ""
        self.time = '1000-01-01 00:00:00.000000'
        self.timeID = 0
