import os
import click
from flask import Flask, render_template, request, url_for, redirect, flash

# SQL
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'dev'

db = SQLAlchemy(app)

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20))

class Assignment(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	target = db.Column(db.String(60))
	description = db.Column(db.String(200))
	ddl = db.Column(db.String(10))

@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
	if drop:
		db.drop_all()
	db.create_all()
	click.echo('Initialized database.')

@app.cli.command()
def forge():
	db.create_all()

	name = 'Zeyu Yuan'
	homeworks = [
		{'target': 'GMM-UBM', 'description': 'awsl', 'ddl': '2019-05-19'},
		{'target': 'Music-Math', 'description': 'GG', 'ddl': '2019-05-25'},
		{'target': 'Database', 'description': 'bu xiang xie', 'ddl': '2019-05-19'},
		{'target': 'Kaggle', 'description': 'bu hui xie', 'ddl': '2019-06-01'}
	]    

	user = User(name=name)
	db.session.add(user)
	for hw in homeworks:
		homework = Assignment(target=hw['target'], description=hw['description'], ddl=hw['ddl'])
		db.session.add(homework)

	db.session.commit()
	click.echo('Done.')

@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method == 'POST':
		target = request.form.get('target')
		description = request.form.get('description')
		if not description:
			description = 'None'
		ddl = request.form.get('ddl')
		if not target or not ddl or len(ddl) > 10 or len(target) > 60:
			flash('Invalid input.')
			return redirect(url_for('index'))
		assignment = Assignment(target=target, description=description, ddl=ddl)
		db.session.add(assignment)
		db.session.commit()
		flash('Item created.')
		return redirect(url_for('index'))

	homeworks = Assignment.query.all()
	return render_template('index.html', homeworks=homeworks)

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

@app.errorhandler(400)
def page_not_found(e):
	return render_template('400.html'), 400

@app.context_processor
def inject_user():
	user = User.query.first()
	return dict(user=user)

