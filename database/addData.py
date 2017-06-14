from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from csvreader import get_user_list
from DataBaseSetUp import User, Base, Survey,Skill_Entry,Skill_List_Manager, AxisTemplate,Canvas
Str = 'mysql://kaiyuewang:wangkaiyue94@testdb.c7rdqxze62rp.us-east-1.rds.amazonaws.com:3306/testdb'
engine = create_engine(Str)
# engine = create_engine('sqlite:///OurDataBase.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

###add user from the CVS to User table
user_list = get_user_list("../Data/user.csv")
for item in user_list:
    user = User(user_id = item[0], user_name = item[1])
    session.add(user)
    session.commit()
    
print "added user"

###add skill_list
skill_listManager = Skill_List_Manager(skill_list_name = "List of Skills", skill_list_descrip = "this is the list created for instructional purpose in ME292C")
session.add(skill_listManager)
session.commit()


print "created a skill list"

###add skill to skill list
skill_list = get_user_list("../Data/skill.csv")
for item in skill_list:
    skill = Skill_Entry(skill_name = item[0], skill_descrip = item[1], skill_list_manager = skill_listManager)
    session.add(skill)
    session.commit()
print "added skill to skill list!"


##add AxisTemplate
axis1 = AxisTemplate(left = "Design Skills i don't have", right = "Design Skills i have", 
                    up = "Design Skills i want to hone", down = "Design Skills i don't want to hone")
session.add(axis1)
session.commit()

print "added Axis!"


##add survey 
survey1 = Survey(survey_key = "T1", skill_list_manager = skill_listManager, axistemplate = axis1)
session.add(survey1)
session.commit()
print "added survey"

###Fake add some Canvas user input
