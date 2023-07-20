import time

from flask.cli import AppGroup
from flask_migrate import stamp
import sqlalchemy
from sqlalchemy.exc import DatabaseError
from backend import settings

manager = AppGroup(help="Manage the database (create/drop tables.).")


def _wait_for_db_connection(db):
    retried = False
    while not retried:
        try:
            db.engine.execute("SELECT 1;")
            return
        except DatabaseError:
            time.sleep(30)

        retried = True


def is_db_empty():
    from backend.models import db

    table_names = sqlalchemy.inspect(db.get_engine()).get_table_names()
    return len(table_names) == 0


def load_extensions(db):
    with db.engine.connect() as connection:
        for extension in settings.dynamic_settings.database_extensions:
            connection.execute(f'CREATE EXTENSION IF NOT EXISTS "{extension}";')


@manager.command()
def create_tables():
    """Create the database tables."""
    from backend.models import db

    _wait_for_db_connection(db)

    # We need to make sure we run this only if the DB is empty, because otherwise calling
    # stamp() will stamp it with the latest migration value and migrations won't run.
    if is_db_empty():
        load_extensions(db)

        # To create triggers for searchable models, we need to call configure_mappers().
        sqlalchemy.orm.configure_mappers()
        db.create_all()

        # Need to mark current DB as up to date
        stamp()


@manager.command()
def drop_tables():
    """Drop the database tables."""
    from backend.models import db

    _wait_for_db_connection(db)
    db.drop_all()

