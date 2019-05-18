from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from mytodotoy import db

class User(db.Model, UserMixin):
	__tablename__ = 'USERS'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20))
	username = db.Column(db.String(20), unique=True)
	password_hash = db.Column(db.String(128))

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def validate_password(self, password):
		return check_password_hash(self.password_hash, password)

class Assignment(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	target = db.Column(db.String(60))
	description = db.Column(db.String(200))
	ddl = db.Column(db.String(10))
	state = db.Column(db.Boolean, default=False)
	user_id = db.Column(db.Integer, db.ForeignKey("USERS.id"))