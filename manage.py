from api import create_app
from flask.cli import FlaskGroup
from dotenv import load_dotenv
from api.helpers.helpers import create_db_
from api.extensions.extensions import celery, init_celery


load_dotenv()

app = create_app()
cli = FlaskGroup(create_app=create_app)

init_celery(celery, app)

@cli.command("create_db")
def create_db():
    """Create the database and all the tables."""
    create_db_()


if __name__ == '__main__':
    cli()