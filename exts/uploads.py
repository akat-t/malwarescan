import click
from flask_cli import with_appcontext
from flask import current_app
from flask_uploads import UploadSet
from flask_uploads import ALL
from flask_uploads import configure_uploads
from flask_uploads import patch_request_class

submissions = UploadSet('files', ALL)


def setup_app(app):
    """Initialize Flask-Uploads."""
    # Set default configuration
    patch_request_class(app, 256 * 1024 * 1024)
    configure_uploads(app, submissions)
    # Add extension CLI to application.
    # app.cli.add_command(testupload)


@click.command()
@with_appcontext
def testupload():
    """Test File Uploads operation."""
    click.echo(f"Current app name: {current_app.name}")
    click.echo(submissions.config.tuple)
