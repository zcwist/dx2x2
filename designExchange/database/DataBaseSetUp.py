import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


#create user data table
class User(Base):
    __tablename__ = 'userdata'
    user_id = Column(String(80),primary_key=True, nullable=False)
    user_name =  Column(String(80),primary_key=True, nullable=False)

class Survey(Base):
    __tablename__='survey'
    id = Column(Integer, primary_key=True)
    survey_key = Column(String(80), nullable=False)
    survey_name= Column(String(80))

# class Skill_List_Manager:
#     __tablename__ = 'skill_list_manager'
#     id = Column(Integer, primary_key=True)
#     skill_list_name = Column(String(80))
#     survey_id = Column(Integer, ForeignKey('survey.id'))
#     survey = relationship(Survey)
    
    
class Skill_list(Base):
    __tablename__ = 'skill_list'
    id = Column(Integer, primary_key=True)
    skill_name = Column(String(80), nullable = False)
    skill_descrip = Column(String(200))
    # skill_list_id = Column(Integer, ForeignKey('skill_list_manager.id'))
    # skill_list_manager = relationship(Skill_List_Manager)
    survey_id = Column(Integer, ForeignKey('survey.id'))
    survey = relationship(Survey)

class AxisTemplate(Base):
    __tablename__ = 'axistemplate'
    id = Column(Integer,primary_key=True)
    left = Column(String(80), nullable=False)
    right = Column(String(80), nullable=False)
    up = Column(String(80), nullable=False)
    down = Column(String(80), nullable=False)
    survey_id = Column(Integer, ForeignKey('survey.id'))

    survey = relationship(Survey)


class Canvas(Base):
    __tablename__ = 'canvas'
    id = Column(Integer, primary_key = True)
    user_id = Column(Integer, ForeignKey('userdata.user_id'))
    class_id = Column(Integer, ForeignKey('survey.id') )
    template_id = Column(Integer, ForeignKey('axistemplate.id'))
    x_axis = Column(Integer)
    y_axis = Column(Integer)
    
    axistemplate = relationship(AxisTemplate)
    userdata = relationship(User)
    survy = relationship(Survey)
    
    

engine = create_engine('sqlite:///OurDataBase.db')

Base.metadata.create_all(engine)