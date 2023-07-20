from backend.models.base import db, primary_key
from backend.models.mixins import TimestampMixin, StatusMixin
from backend.utils.common import ADMIN
from datetime import datetime
import hashlib


class Users(TimestampMixin, StatusMixin, db.Model):
    __tablename__ = 'users'

    id = primary_key('Users')
    name = db.Column(db.String(20), comment='name')
    phone = db.Column(db.String(11), nullable=False, index=True, unique=True)
    password = db.Column(db.String(128), comment='password')
    last_login = db.Column(db.DateTime, comment='last login time')

    @staticmethod
    def get_by_id(pid):
        return Users.query.filter(Users.id == pid).first()

    @staticmethod
    def get_by_name(name):
        return Users.query.filter(Users.name == name, Users.is_admin == ADMIN.YES).first()

    @staticmethod
    def get_by_phone(phone):
        return Users.query.filter(Users.phone == phone).scalar()

    @staticmethod
    def get_by_phone_password(phone, password):
        return Users.query.filter(Users.phone == phone, Users.password == password).first()

    @staticmethod
    def get_by_name_password(name, password):
        return Users.query.filter(Users.name == name, Users.password == password).first()

    @staticmethod
    def md5_password(password):
        """password encryption"""
        m = hashlib.md5()
        m.update(password.encode())
        return m.hexdigest()

    def update_last_login(self):
        self.last_login = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def info(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
        }
