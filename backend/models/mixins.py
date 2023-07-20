from .base import db, Column
from backend.utils.common import STATUS


class TimestampMixin(object):
    update_time = Column(db.DateTime(), default=db.func.now(), nullable=False)
    create_time = Column(db.DateTime(), default=db.func.now(), nullable=False)


class StatusMixin(object):
    status = db.Column(db.Integer, default=STATUS.NORMAL)
