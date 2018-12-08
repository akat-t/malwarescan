import click
from flask import current_app
from flask_cli import with_appcontext
from flask_mail import Mail

mail = Mail()


def setup_app(app):
    # Set default configuration
    mail.init_app(app)
    init_email_error_handler(app)
    # Add extension CLI to application.
    app.cli.add_command(testmail)


@click.command()
@with_appcontext
def testmail():
    """Test SMTP handler operations."""
    click.echo(f"Current app name: {current_app.name}")
    click.echo("Sending current app name as ERROR email... ")
    current_app.logger.error(f"Current app name: {current_app.name}")


def init_email_error_handler(app):
    """
    Initialize a logger to send emails on error-level messages.
    Unhandled exceptions will now send an email message to app.config.ADMINS.
    """
    # Do not send error emails while developing
    if app.debug:
        return
    # Retrieve email settings from app.config
    host = app.config['MAIL_SERVER']
    port = app.config['MAIL_PORT']
    from_addr = app.config['MAIL_DEFAULT_SENDER']
    # username = app.config['MAIL_USERNAME']
    # password = app.config['MAIL_PASSWORD']
    secure = () if app.config.get('MAIL_USE_TLS') else None
    to_addr_list = app.config['ADMINS']
    subject = app.config.get('APP_SYSTEM_ERROR_SUBJECT_LINE', 'System Error')
    # Setup an SMTP mail handler for error-level messages
    import logging
    from logging.handlers import SMTPHandler
    mail_handler = SMTPHandler(
        mailhost=(host, port),  # Mail host and port
        fromaddr=from_addr,  # From address
        toaddrs=to_addr_list,  # To address
        subject=subject,  # Subject line
        # credentials=(username, password),  # Credentials
        credentials=None,  # Anonymous
        secure=secure,
    )
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)
