# -*- coding: utf-8 -*-

"""
This file create structure in database and need only for init structure for test
"""

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class SomeObject(Base):
    """
    Base class for test table structure
    """

    __tablename__ = 'some_objects'

    id = Column(Integer, primary_key=True)

    name = Column(String(50))


engine = create_engine('mysql://test_user:test_password@localhost/test_db')

if __name__ == '__main__':
    Base.metadata.create_all(engine)



