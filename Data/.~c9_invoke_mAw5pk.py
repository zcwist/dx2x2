import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

User data
​​user_id, username, class_id
​​
​​Skill list table
​​skill_id, name, description, skill_list_id
​​
​​Skill manager
​​skill_list_id, skill_list_name
​​
​​2x2 template
​​template_id, axis, description
​​
​​Class table
​​class_id, class_name, skill_list_id, template_id
​​
​​Canvas data table
​​canvas_id, user_id, class_id, version, date,  x, y */
#create user data tab
class User(Base):
    __tablename__ = 'userdata'
    user_id =(Integer, primary_key=True)
    user_name()

engine = create_engine('sqlite:///2by2DataBase.db')

Base.metadata.create_all(engine)