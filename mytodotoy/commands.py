import click

from mytodotoy import app, db
from mytodotoy.models import User, Assignment

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