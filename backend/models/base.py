import functools
from flask_sqlalchemy import BaseQuery, SQLAlchemy
from sqlalchemy.pool import NullPool
from backend.utils import json_dumps
from backend import settings
from sqlalchemy_searchable import make_searchable


class UkonSQLAlchemy(SQLAlchemy):
    def apply_driver_hacks(self, app, info, options):
        options.update(json_serializer=json_dumps)
        if settings.SQLALCHEMY_ENABLE_POOL_PRE_PING:
            options.update(pool_pre_ping=True)
        return super(UkonSQLAlchemy, self).apply_driver_hacks(app, info, options)

    def apply_pool_defaults(self, app, options):
        super(UkonSQLAlchemy, self).apply_pool_defaults(app, options)
        if settings.SQLALCHEMY_ENABLE_POOL_PRE_PING:
            options["pool_pre_ping"] = True
        if settings.SQLALCHEMY_DISABLE_POOL:
            options["poolclass"] = NullPool
            # Remove options NullPool does not support:
            options.pop("max_overflow", None)
        return options


db = UkonSQLAlchemy()

# This is required by SQLAlchemy-Searchable as it adds DDL listeners
# on the configuration phase of models.
db.configure_mappers()

# listen to a few database events to set up functions, trigger updates
# and indexes for the full text search
make_searchable(options={"regconfig": "pg_catalog.simple"})

Column = functools.partial(db.Column, nullable=False)

key_definitions = settings.dynamic_settings.database_key_definitions((db.Integer, {}))


def key_type(name):
    return key_definitions[name][0]


def primary_key(name):
    key, kwargs = key_definitions[name]
    return Column(key, primary_key=True, index=True, unique=True, autoincrement=True, **kwargs)


def status_key(name):
    key, kwargs = key_definitions[name]
    return Column(key, primary_key=True, index=True, unique=True, autoincrement=True, **kwargs)


class Version(db.Model):
    __tablename__ = 'versions'

    id = db.Column(db.Integer, primary_key=True)
    ver = db.Column(db.Integer)
    classifies = db.Column(db.String(256), unique=True)
