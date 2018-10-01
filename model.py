from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class UserType(db.Model):
	ID = db.Column(db.Integer, primary_key=False)
	userType = db.Column(db.String(24), nullable=False)
	

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(24), nullable=False)
	password = db.Column(db.String(64), nullable=False)
	firstName = db.Column(db.String(24), nullable=False)
	lastName = db.Column(db.String(24), nullable=False)
	userType = db.Column(db.Integer, db.ForeignKey("usertype.id"), nullable=False)
	
class Scanner(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	userID = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
	scannerName = db.Column(db.String(64), nullable=False)

class Class(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(24), nullable=False)
	location = db.Column(db.String(24), nullable=False)
	teacherID = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
	StartTime = db.Column(db.DateTime, nullable=False)
	EndTime = db.Column(db.DateTime, nullable=False)
	
class Item(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	tagID = db.Column(db.String(64), nullable=False)
	name = db.Column(db.String(24), nullable=False)
	classID = db.Column(db.Integer, db.ForeignKey("class.id"), nullable=True)

class Pattern(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	userID = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
	itemID = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
	dayOfWeek = db.Column(db.String(9), nullable=False)
	startTime = db.Column(ARRAY[DateTime])
	presentItem = db.Column(ARRAY[Integer])
	
class Alert(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	userID = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
	itemID = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
	message = db.Column(db.String(128), nullable=False)
	time = db.Column(db.DateTime, nullable=False)
	
class Messages(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	userID = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
	message = db.Column(db.String(128), nullable=False)
	time = db.Column(db.DateTime, nullable=False)
	itemID = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
	