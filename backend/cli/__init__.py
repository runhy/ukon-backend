from flask import current_app as current
from flask.cli import FlaskGroup, run_command, with_appcontext
from flask_migrate import MigrateCommand
import click
from backend import create_app, __version__
from backend.cli import initialize, database


def create():
    app = current or create_app()

    @app.shell_context_processor
    def shell_context():
        from backend import models, settings

        return {"models": models, "settings": settings}

    return app


@click.group(cls=FlaskGroup, create_app=create)
def manager():
    """Management script"""


manager.add_command(database.manager, "database")
manager.add_command(initialize.manager, 'init')
manager.add_command(run_command, "runserver")


@manager.command()
def version():
    """version."""
    print(__version__)
