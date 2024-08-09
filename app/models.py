#create tables
#models for sqlalchemy
from sqlalchemy import Column,Integer,Date,String,Enum as SqlEnum,Text,DateTime
from .database import Base
from sqlalchemy.sql import func
from enum import Enum


#class for the status column
class StatusEnum(str, Enum):
    active = "active"
    completed = "completed"
    archived = "archived"

#table for projects
class Projects(Base):
    __tablename__ = "projects" #table name

    id = Column(Integer, primary_key=True,index=True)
    title = Column(String)
    description = Column(String)
    Url = Column(String) #url for the projects
    technologies = Column(String) #what programming language was used
    date_created = Column(Date) #date project was created
    date_completed = Column(Date) #date project was completed
    status = Column(SqlEnum(StatusEnum))  #e.g(active,completed or archived)

#tables for blogs
class Blog(Base):
    __tablename__ = "blogs" #table name

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    content = Column(Text)
    date_created = Column(DateTime, default=func.now())
    author = Column(String(100))

#tables for contact information
class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String)
    phone = Column(Integer)
    office = Column(String)

#tables for login authentication
class User(Base):
    __tablename__ = "login_info"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String)
    password = Column(String)
