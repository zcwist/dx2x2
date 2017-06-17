from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from csvreader import get_user_list
from DataBaseSetUp import User, Base, Survey,Skill_Entry,Skill_List_Manager, AxisTemplate,Canvas
import config
Str = config.getDBStr()
engine = create_engine(Str)
# engine = create_engine('sqlite:///OurDataBase.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

Base.metadata.drop_all(engine)   # all tables are deleted


