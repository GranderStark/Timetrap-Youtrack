# coding: utf-8
from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Entry(Base):
    """
    Entry of timesheet
    """
    __tablename__ = 'entries'

    id = Column(Integer, primary_key=True)
    note = Column(String(255))
    start = Column(TIMESTAMP)
    end = Column(TIMESTAMP)
    sheet = Column(String(255))


class Meta(Base):
    """
    Timesheets
    """
    __tablename__ = 'meta'

    id = Column(Integer, primary_key=True)
    key = Column(String(255))
    value = Column(String(255))
