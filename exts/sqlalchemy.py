import click
from flask_cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
from flask_registry import ModuleAutoDiscoveryRegistry, RegistryProxy

db = SQLAlchemy()
# migrate = Migrate()

models = RegistryProxy(
    'models',  # Registry namespace
    ModuleAutoDiscoveryRegistry,
    'models'  # Module name (i.e. models.py)
)


def setup_app(app):
    # Set default configuration
    # Add extension CLI to application.
    app.cli.add_command(initdb)
    app.cli.add_command(initdemo)
    db.init_app(app)
    # migrate.init_app(app, db)


@click.command()
@with_appcontext
def initdb():
    """Initialize/Re-initialize database."""
    click.echo("Dropping previous database tables...")
    db.drop_all()
    click.echo("Creating all database tables...")
    db.create_all()
    click.echo("Finished database initialization!")


@click.command()
@with_appcontext
def initdemo():
    """Fill database with demo data (Also set API_DEMO to True)"""
    with open("contrib/demodata.sql", "r") as fd:
        sql_data = fd.read()
        try:
            click.echo("Populating database with demo data...")
            db.session.execute(sql_data)
            db.session.commit()
        except:  # noqa: E722
            click.echo("ERROR: Database already has demo data, or populated")
            raise
    click.echo("Finished database initialization!")
