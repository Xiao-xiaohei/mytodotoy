from flask import render_template

from mytodotoy import app

@app.errorhandler(404)
def page_not_found(e):
	return render_template('errors/404.html'), 404

@app.errorhandler(400)
def page_not_found(e):
	return render_template('errors/400.html'), 400