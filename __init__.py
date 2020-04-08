# -*- coding: utf-8 -*-

"""
This file create structure in database and need only for init structure for test
"""

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker


Base = declarative_base()

internal_users = ["Jone", "Bill", "Bella", "Jake"]

external_users = ["Jone", "Bill", "Bella", "Jake", "Stupid Guy"]


class InternalUser(Base):
    """
    Base class for test table structure
    """

    def __init__(self, _name=None):
        self.name = _name

    __tablename__ = 'internal_users'

    id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(String(50))


class ExternalUser(Base):
    """
    Base class for test table structure
    """

    def __init__(self, _name=None):
        self.name = _name

    __tablename__ = 'external_users'

    id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(String(50))


engine = create_engine('mysql://test_user:test_password@localhost/test_db')

Session = sessionmaker()

Session.configure(bind=engine)

session = Session()

if __name__ == '__main__':
    Base.metadata.create_all(engine)

    for name in internal_users:
        o = InternalUser(name)

        session.add(o)

    for name in external_users:
        o = ExternalUser(name)

        session.add(o)

    session.commit()

