import os
import importlib
from .helpers import parse_boolean, int_or_none
DEBUG = True

FLASK_ENV = "development"

APP_NAME = "ukon"

SECRET_KEY = os.getenv('SECRET_KEY', "dash123adj44da123")

# SERVER_NAME = os.getenv('SERVER_NAME', 'localhost:{0}'.format(os.getenv('DOCKER_WEB_PORT', '5001')))

ENV_FILE = './.env'
CELERY_ENV_FILE = './.env'

LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
LOG_STDOUT = parse_boolean(os.environ.get("LOG_STDOUT", "false"))
LOG_PREFIX = os.environ.get("LOG_PREFIX", "")
LOG_FORMAT = os.environ.get(
    "LOG_FORMAT",
    LOG_PREFIX + "[%(asctime)s][%(levelname)s][%(name)s] %(message)s",
)

# Connection settings for Redash's own database (where we store the queries, results, etc)
SQLALCHEMY_DATABASE_URI = os.environ.get(
    "REDASH_DATABASE_URL", os.environ.get("DATABASE_URL", "postgresql:///postgres")
)
SQLALCHEMY_MAX_OVERFLOW = int_or_none(os.environ.get("SQLALCHEMY_MAX_OVERFLOW"))
SQLALCHEMY_POOL_SIZE = int_or_none(os.environ.get("SQLALCHEMY_POOL_SIZE"))
SQLALCHEMY_DISABLE_POOL = parse_boolean(os.environ.get("SQLALCHEMY_DISABLE_POOL", "false"))
SQLALCHEMY_ENABLE_POOL_PRE_PING = parse_boolean(os.environ.get("SQLALCHEMY_ENABLE_POOL_PRE_PING", "false"))
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = False

PROXIES_COUNT = int(os.environ.get("PROXIES_COUNT", "1"))

dynamic_settings = importlib.import_module(
    os.environ.get("DYNAMIC_SETTINGS_MODULE", "backend.settings.dynamic_settings")
)

REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")

