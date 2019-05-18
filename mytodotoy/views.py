from flask import render_template, request, url_for, redirect, flash
from flask_login import login_user, login_required, logout_user, current_user

from mytodotoy import app, db
from mytodotoy.models import User, Assignment

@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
	if request.method == 'POST':
		target = request.form.get('target')
		description = request.form.get('description')
		if not description:
			description = 'None'
		ddl = request.form.get('ddl')
		if not target or not ddl or len(ddl) > 10 or len(target) > 60 or not if_ddl(ddl):
			flash('Invalid input.')
			return redirect(url_for('index'))
		assignment = Assignment(target=target, description=description, ddl=ddl, user_id=current_user.id)
		db.session.add(assignment)
		db.session.commit()
		flash('Item created.')
		return redirect(url_for('index'))

	homeworks = Assignment.query.filter_by(user_id=current_user.id).all()
	return render_template('index.html', homeworks=homeworks)

@app.route('/change/<int:hw_id>', methods=['POST'])
def change(hw_id):
	hw = Assignment.query.get_or_404(hw_id)
	hw.state = not hw.state
	db.session.commit()
	flash("Hw's state has changed.")
	return redirect(url_for('index'))

@app.route('/edit/<int:hw_id>', methods=['GET', 'POST'])
@login_required
def edit(hw_id):
	hw = Assignment.query.get_or_404(hw_id)
	if request.method == 'POST':
		target = request.form.get('target')
		description = request.form.get('description')
		ddl = request.form.get('ddl')
		
		if not target or not ddl or len(ddl) > 10 or len(target) > 60 or not if_ddl(ddl):
			flash('Invalid input.')
			return redirect(url_for('edit', hw_id=hw_id))

		hw.target = target
		hw.description = description
		hw.ddl = ddl
		db.session.commit()
		flash('Item updated.')
		return redirect(url_for('index'))

	return render_template('edit.html', hw=hw)

@app.route('/delete/<int:hw_id>', methods=['POST'])
@login_required
def delete(hw_id):
	hw = Assignment.query.get_or_404(hw_id)
	db.session.delete(hw)
	db.session.commit()
	flash('Item deleted.')
	return redirect(url_for('index'))

@app.route('/')
def welcome():
	return render_template('welcome.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
	if request.method == 'POST':
		new_user = User(name=request.form.get('name'), username=request.form.get('username'))
		new_user.set_password(request.form.get('password'))
		db.session.add(new_user)
		db.session.commit()
		flash('User created.')
		return redirect(url_for('index'))

	return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		now_username = request.form.get('username')
		now_user = User.query.filter_by(username=now_username).first()
		if now_user and now_user.validate_password(request.form.get('password')):
			login_user(now_user)
			flash('Login success.')
			return redirect(url_for('index'))

		flash('Invalid username or password.')
		return redirect(url_for('login'))

	return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
	logout_user()
	flash('Goodbye.')
	return redirect(url_for('welcome'))

def if_ddl(ddl):
	tmp = ddl.split('-')
	if int(tmp[-2]) < 1 or int(tmp[-2]) > 12:
		return False
	if int(tmp[-1]) < 1 or int(tmp[-1]) > 31:
		return False
	return True

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
	if request.method == 'POST':
		name = request.form.get('new_name')
		if not name or len(name) > 20:
			flash('Invalid input.')
			return redirect(url_for('settings'))
		
		current_user.name = name
		db.session.commit()
		flash('You\'ve get a new name.')
		return redirect(url_for('index'))

	return render_template('settings.html')