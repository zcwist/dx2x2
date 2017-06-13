from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from csvreader import get_user_list
from DataBaseSetUp import User, Base, Survey,Skill_list,AxisTemplate,Canvas

engine = create_engine('sqlite:///OurDataBase.db')
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
###add survey 
survey1 = Survey(survey_key = "SURVEY_ONE_TEST")
session.add(survey1)
session.commit()

print "added survey!"

###add skill_list
skill_list = get_user_list("../Data/skill.csv")
for item in skill_list:
    skill = Skill_list(skill_name = item[0], skill_descrip = item[1], survey = survey1)
    session.add(skill)
    session.commit()
print "added skill_list!"


##add AxisTemplate
axis1 = AxisTemplate(left = "Design Skills i don't have", right = "Design Skills i have", 
                    up = "Design Skills i want to hone", down = "Design Skills i don't want to hone")
session.add(axis1)
session.commit()

print "added Axis!"

###Fake add some Canvas user input