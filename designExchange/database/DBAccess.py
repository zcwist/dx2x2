from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from DataBaseSetUp import User, Base, Survey,Skill_list,AxisTemplate,Canvas


engine = create_engine('sqlite:///database/OurDataBase.db')

DBSession = sessionmaker(bind = engine)

session = DBSession()

def get_user_name(id):
    try:
        user = session.query(User).filter(User.user_id == id).one()
    except Exception as e:
        return None
    if user:
        return user.user_name


def get_list(surveyID):
    try:
        list = session.query(Skill_list).filter(Skill_list.survey.survey_id == surveyID).all()
    except Exception as e:
        return None
    if list:
        for entry in list:
            print(entry.skill_name)
            print(entry.skill_descrip)
        
        
print (get_list("SURVEY_ONE_TEST"))