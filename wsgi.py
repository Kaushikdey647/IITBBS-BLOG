from flaskblog import create_app, db
from dotenv import load_dotenv
from flask.cli import with_appcontext
import click

load_dotenv()
app = create_app()

@click.command(name='reset_db')
@with_appcontext
def reset_db():
    db.drop_all()
    db.create_all()
    db.session.commit()
    click.echo('Database has been reset.')

app.cli.add_command(reset_db)
if __name__ == '__main__':
    app.run(debug=True)