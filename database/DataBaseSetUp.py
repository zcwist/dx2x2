import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.types import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import Boolean
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


#create user data table
class User(Base):
    __tablename__ = 'userdata'
    user_id = Column(String(80),primary_key=True, nullable=False)
    user_name =  Column(String(80),primary_key=True, nullable=False)



class Skill_List_Manager(Base):
    __tablename__ = 'skill_list_manager'
    id = Column(Integer, primary_key=True)
    skill_list_name = Column(String(80), nullable=False)
    skill_list_descrip = Column(String(80))

    
    
class Skill_Entry(Base):
    __tablename__ = 'skill_entry'
    id = Column(Integer, primary_key=True)
    skill_name = Column(String(80), nullable = False)
    skill_descrip = Column(String(200))
    skill_list_id = Column(Integer, ForeignKey('skill_list_manager.id'), nullable=False)
    skill_list_manager = relationship(Skill_List_Manager)


class AxisTemplate(Base):
    __tablename__ = 'axistemplate'
    id = Column(Integer,primary_key=True)
    left = Column(String(80), nullable=False)
    right = Column(String(80), nullable=False)
    up = Column(String(80), nullable=False)
    down = Column(String(80), nullable=False)


class Survey(Base):
    __tablename__='survey'
    id = Column(Integer, primary_key=True)
    survey_key = Column(String(80), nullable=False)
    survey_name= Column(String(80))
    isOpen = Column(Boolean, default=True)
    skill_list_id = Column(Integer, ForeignKey('skill_list_manager.id'), nullable=False)
    template_id = Column(Integer, ForeignKey('axistemplate.id'), nullable=False)
    
    skill_list_manager = relationship(Skill_List_Manager)
    axistemplate = relationship(AxisTemplate)


class Canvas(Base):
    __tablename__ = 'canvas'
    id = Column(Integer, primary_key = True)
    user_id = Column(String(80), ForeignKey('userdata.user_id'))
    class_id = Column(Integer, ForeignKey('survey.id') )
    version = Column(Integer, default=1)
    date = Column(DateTime)
    coordinates = Column(JSON)
    
    
    userdata = relationship(User)
    survy = relationship(Survey)
    


Str = 'mysql://kaiyuewang:wangkaiyue94@testdb.c7rdqxze62rp.us-east-1.rds.amazonaws.com:3306/testdb'
engine = create_engine(Str)

# engine = create_engine('sqlite:///OurDataBase.db')

Base.metadata.create_all(engine)