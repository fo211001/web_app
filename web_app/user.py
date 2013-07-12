#coding: utf-8
#from . import Base
from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column,  String, Integer, PickleType, create_engine
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm.exc import NoResultFound
Base = declarative_base()

import md5
import random
import string  # pylint: disable=W0402



engine = create_engine('sqlite:///foo.db')
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

def rndstr(length=32):
        chars = string.ascii_letters + string.digits
        return ''.join(
            random.choice(chars) for x in range(length))



class User(Base):
    """ User class for keeping employee info & credentials """

    __tablename__ = "user"
    _password = None

    id = Column(Integer, primary_key=True)

    name = Column(String(255))
    email = Column(String(50))
    _salt = Column("salt", String(32))
    hpass = Column(String(32))



    @hybrid_property
    def salt(self):
        if self._salt:
            return self._salt
        self._salt = rndstr(32)
        return self._salt

    @salt.expression    # pyflakes: disable=W806
    def salt(cls):      # pylint: disable=E0213
        return cls._salt

    @salt.setter
    def salt(self, value):
        if not self._salt:
            self._salt = rndstr(32)()
        self._salt = value

    @property
    def password(self):
        """ Gets a transient password """
        return self._password

    @password.setter
    def password(self, value):
        """ set transient password and updates password
            hash if password is not empty
        """
        if not value:
            return
        self._password = value
        self.hpass = User.get_hashed_password(self)

    def check_password(self, passwd):
        return self.hpass == User.get_hashed_password(self, passwd)

    @staticmethod
    def get_hashed_password(user, pwd=None):
        pwd = pwd or user.password
        if pwd is None:
            raise Exception("Hashed password of None")
        mhash = md5.new()
        mhash.update(pwd)
        mhash.update(user.salt)
        return mhash.hexdigest()


class WebSong(Base):


    __tablename__ = "songs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id))

    title = Column(String)
    song = Column(PickleType)
    applicatures = Column(PickleType)
    user = relationship(User, backref="songs")

def pas_gen():
    return ''.join(random.choice(string.letters + string.digits) for i in range(10))


class EmailExistError(Exception):
    pass


def register(name, email, password):
    session = Session()
    query = session.query(User).filter(User.email == email)
    try:
        user = query.one()
        #raise EmailExistError(u'Такой почтовый ящик уже существует')
        return False
    except NoResultFound:
        # Создаем нового пользователя
        user = User(name=name.decode('utf-8'), email=email)
        ##TODO SMTP mail
        user.password = password
        session.add(user)
        session.commit()
        return user


def login(email, password):
    """
    Функция проверяет наличие почтового ящика в БД и сверяет пароль
    :param email: ПЯ введенный пользователем
    :param password: пароль введенный пользовытелем
    :return: True - пользователь найден в базе
    """
    session = Session()
    query = session.query(User).filter(User.email == email)
    try:
        user = query.one()
        if User.get_hashed_password(user, password) == user.hpass:
            return True
        else:
            return False
    except NoResultFound:
        return False


def all_users():
    session = Session
    for u in session.query(User):
        print u.name, u.email

def del_all():
    session= Session
    for u in session.query(User):
        session.delete(u)
    session.commit()