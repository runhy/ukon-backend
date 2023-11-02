from flask_migrate import Migrate
from .app import create_app
from . import settings
import sys, logging

__version__ = "1.0.0"


def setup_logging():
    handler = logging.StreamHandler(sys.stderr)
    formatter = logging.Formatter(settings.LOG_FORMAT)
    handler.setFormatter(formatter)
    logging.getLogger().addHandler(handler)
    logging.getLogger().setLevel(settings.LOG_LEVEL)


setup_logging()

migrate = Migrate(compare_type=True, include_schemas=True)
