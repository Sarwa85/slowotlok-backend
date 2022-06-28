from sqlalchemy import Column, String, Integer
from flaskr.base import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    gid  = Column(Integer)
    name = Column(String)
    email = Column(String)
    profile_pic = Column(String)


from flask_login import UserMixin


class FlaskUser(UserMixin):
    def __init__(self, id_, name, email, profile_pic):
        self.id = id_
        self.name = name
        self.email = email
        self.profile_pic = profile_pic