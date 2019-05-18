import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user

app = Flask(__name__)
#app.config['SECRET_KEY'] = 'dev'
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.dirname(app.root_path), 'data.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.dirname(app.root_path), os.getenv('DATABASE_FILE', 'data.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
	from mytodotoy.models import User
	user = User.query.get(int(user_id))
	return user

login_manager.login_view = 'login'

@app.context_processor
def inject_user():
	return dict(user=current_user)

from mytodotoy import views, errors, commands